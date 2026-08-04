#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 strando team
# SPDX-License-Identifier: GPL-3.0-only

import traceback
import sys
import hashlib
import yaml
import subprocess
import shutil

from typing import Any, TYPE_CHECKING
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QTabWidget,
    QFileDialog,
    QWidget,
    QMessageBox,
    QCheckBox,
    QDialog,
    QSpinBox,
    QComboBox,
)

from ui.patcher_ui import Ui_TabWidget
from ui.preset_save_ui import Ui_PresetSave
from constants import CustomSafeYAMLDumper
from generator import Generator
from apply_patches import apply_patches
from rom_patcher import update_yaml

# it seems there's a module named the same way (natively?), workaround to make the linter happy
if TYPE_CHECKING:
    from .settings import Settings
else:
    from settings import Settings

EXE = ".exe" if sys.platform == "nt" else ""

# make sure this is set to False for releases
IS_DEBUG = True

# version: sha1 hash
ROM_VERSION_TO_HASH = {
    "eur0": "9e99cc803a14ce038eb908db585431f8254f09ee",  # EUR Revision 0
}
ROM_HASH_TO_VERSION = {sha1: version for version, sha1 in ROM_VERSION_TO_HASH.items()}
VALID_ROM_HASHES = list(ROM_VERSION_TO_HASH.values())

MODULE_PATH = Path(sys.argv[0]).resolve().parent
PRESET_DIR = MODULE_PATH / "presets"
EXTRACT_DIR = MODULE_PATH / "extract"
RES_DIR = MODULE_PATH / "res"
BIOS_PATH = RES_DIR / "arm7_bios.bin"
RANDO_OVL_NAME = "ovgz"


def show_message(parent: QWidget, title: str, icon: QMessageBox.Icon, text: str):
    message_box = QMessageBox(parent)
    message_box.setWindowTitle(title)
    message_box.setIcon(icon)
    message_box.setText(text)
    message_box.show()


def show_error(parent: QWidget, text: str):
    show_message(parent, "Error", QMessageBox.Icon.Critical, text)


class PresetSaveDialog(QDialog):
    def __init__(self, parent: "MainWindow"):
        super().__init__(parent)

        self.ui = Ui_PresetSave()
        self.ui.setupUi(self)
        self.setup_connections()

        self.main = parent
        self.ui.name.setText(self.main.ui.gen_combo_preset.currentText())

    def setup_connections(self):
        self.ui.btn_box.accepted.connect(self.do_accept)
        self.ui.btn_box.rejected.connect(self.reject)

    # connection callbacks

    def do_accept(self):
        name = self.ui.name.text()

        if len(name) == 0:
            show_error(self, "Preset name is unset.")
            return

        preset_path = PRESET_DIR / f"{name.lower()}.yaml"

        if preset_path.exists():
            answer = QMessageBox.question(
                self,
                "Overwrite existing preset?",
                f"Are you sure you want to overwrite the existing preset {repr(name)}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )

            if answer == QMessageBox.StandardButton.No:
                return

        # save the state
        self.main.save_preset(None)

        # export the preset
        yaml_file = self.main.live_preset.to_yaml()
        yaml_file["name"] = name

        with open(preset_path, "w", encoding="utf-8") as file:
            yaml.dump(yaml_file, file, sort_keys=False, Dumper=CustomSafeYAMLDumper)

        # update preset list
        self.main.setup_presets()
        assert name in self.main.presets, "unexpected error"
        self.main.ui.gen_combo_preset.setCurrentIndex(list(self.main.presets.keys()).index(name) + 1)

        self.accept()


class MainWindow(QTabWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_TabWidget()
        self.ui.setupUi(self)

        self.presets: dict[str, Settings] = {}
        self.live_preset = Settings.empty()  # tracks the settings changed in real time
        self.disable_live_preset_update = False
        self.rom_version: str | None = None

        try:
            self.setup_connections()

            if IS_DEBUG:
                # convenience settings
                self.set_rom_path(Path("extract/baserom_st_eur.nds").resolve())
                self.ui.out_path.setText(str(MODULE_PATH / "output"))

            self.setup_presets()
        except Exception:
            show_error(self, f"An error occurred\n\n{traceback.format_exc()}")

    def setup_connections(self):
        ### General

        self.ui.rom_btn.pressed.connect(self.do_select_rom)
        self.ui.out_btn_select.pressed.connect(self.do_select_out_folder)
        self.ui.out_btn_generate.pressed.connect(self.do_generate)
        self.ui.gen_combo_preset.currentIndexChanged.connect(self.do_change_preset)
        self.ui.gen_btn_preset.pressed.connect(self.do_save_preset)
        self.ui.gen_string.textEdited.connect(self.do_settings_string_update)

        ### Settings

        # since it will be too annoying to connect everything manually
        # we're iterating through child widgets of the settings tab
        # to connect the signals of each type of widget used
        for widget in self.ui.tab_settings.findChildren(QWidget):
            if isinstance(widget, QCheckBox):
                widget.checkStateChanged.connect(self.do_live_preset_update)
            elif isinstance(widget, QSpinBox):
                widget.valueChanged.connect(self.do_live_preset_update)
            elif isinstance(widget, QComboBox):
                widget.currentIndexChanged.connect(self.do_live_preset_update)

    def set_rom_path(self, rom_path: Path):
        """Sets the baserom's path"""

        valid_txt = "Invalid ROM"
        is_valid = False
        self.rom_version = None

        if len(str(rom_path)) > 0:
            rom_hash = hashlib.sha1(rom_path.read_bytes()).hexdigest().lower()

            if rom_hash in VALID_ROM_HASHES:
                self.rom_version = ROM_HASH_TO_VERSION[rom_hash]
                self.try_extract_rom(rom_path)

                valid_txt = "Valid ROM"
                is_valid = True
            else:
                show_error(self, f"Selected ROM is invalid!\n\nDetected Hash:\n{rom_hash}")

            # disable
            self.ui.tab_settings.setEnabled(is_valid)
            self.ui.gen_group.setEnabled(is_valid)
            self.ui.out_group.setEnabled(is_valid)
            self.ui.rom_path.setText(str(rom_path))

        self.ui.rom_lbl.setText(valid_txt)

    def try_extract_rom(self, rom_path: Path):
        if self.rom_version is None:
            return

        EXTRACT_DIR.mkdir(exist_ok=True)
        assert RES_DIR.exists(), "unexpected error"
        assert BIOS_PATH.exists(), "arm7 bios is missing"

        command = f"{RES_DIR / f'dsrom{EXE}'} extract --rom {rom_path} --path {EXTRACT_DIR / self.rom_version} --arm7-bios {BIOS_PATH}"
        subprocess.run(command, shell=True)

    def try_pack_rom(self, out_path: Path):
        if self.rom_version is None:
            return

        assert EXTRACT_DIR.exists(), "unexpected error"
        assert RES_DIR.exists(), "unexpected error"
        assert BIOS_PATH.exists(), "arm7 bios is missing"

        command = f"{RES_DIR / f'dsrom{EXE}'} build --config {EXTRACT_DIR / self.rom_version / 'config.yaml'} --rom {out_path} --arm7-bios {BIOS_PATH}"
        subprocess.run(command, shell=True)

    def setup_presets(self):
        """Populates the preset list"""

        assert PRESET_DIR.exists(), str(PRESET_DIR)

        self.presets.clear()

        self.ui.gen_combo_preset.clear()
        self.ui.gen_combo_preset.addItem("Custom")

        for i, preset_path in enumerate(PRESET_DIR.rglob("*.yaml")):
            with preset_path.open("r") as file:
                yaml_data: dict = yaml.safe_load(file)

            name = yaml_data.get("name", f"Unknown Preset {i + 1}")
            self.ui.gen_combo_preset.addItem(name)
            self.presets[name] = Settings.from_yaml(yaml_data["settings"])

        self.ui.gen_combo_preset.setCurrentIndex(1 if len(self.presets) > 0 else 0)

    def apply_preset(self, preset: str | None):
        """Updates the settings on the UI following the preset's data"""

        if preset == str():
            return

        self.disable_live_preset_update = True

        if preset is not None and preset != "Custom":
            assert preset in self.presets, f"missing preset {repr(preset)}"
            settings = self.presets[preset]
            self.ui.gen_combo_preset.setCurrentIndex(list(self.presets.keys()).index(preset) + 1)
        else:
            settings = self.live_preset
            self.ui.gen_combo_preset.setCurrentIndex(0)

        ### General

        self.ui.gen_string.setText(settings.to_str())
        self.ui.gen_radio_custom.setChecked(True)
        self.ui.gen_radio_random.setChecked(False)

        ### Settings - Shuffle Land

        # Minigames
        def apply_minigame(kind: str, data: list[str]):
            widget: QCheckBox = getattr(self.ui, f"minigame_{kind}_easy")
            widget.setChecked("easy" in data)

            widget: QCheckBox = getattr(self.ui, f"minigame_{kind}_hard")
            widget.setChecked("hard" in data)

            widget: QCheckBox = getattr(self.ui, f"minigame_{kind}_expert")
            widget.setChecked("expert" in data)

        apply_minigame("whip", settings.shuffle.minigames.whip_race)
        apply_minigame("pirate", settings.shuffle.minigames.pirate_hideout)
        apply_minigame("takeem", settings.shuffle.minigames.take_em_all_on)

        self.ui.minigame_sword.setChecked(settings.shuffle.minigames.sword_training)
        self.ui.minigame_goron.setChecked(settings.shuffle.minigames.goron_range)

        # Shop Sanity
        self.ui.shop_amount.setValue(settings.shuffle.shopsanity)

        # Stamps
        self.ui.stamps.setChecked(settings.shuffle.stamps)
        self.ui.stamp_book.setChecked(settings.shuffle.stamp_book)
        self.ui.stamp_reward_10.setChecked(10 in settings.shuffle.stamps_rewards)
        self.ui.stamp_reward_15.setChecked(15 in settings.shuffle.stamps_rewards)
        self.ui.stamp_reward_20.setChecked(20 in settings.shuffle.stamps_rewards)

        # Misc
        self.ui.rupeesanity.setChecked(settings.shuffle.rupeesanity)
        self.ui.duets.setChecked(settings.shuffle.duets)

        ### Settings - Shuffle Train

        # Glyphs and Sources
        self.ui.glyphsrc_combo_box.setCurrentIndex(
            settings.shuffle.glyphs_and_sources_mode_map[settings.shuffle.glyphs_and_sources]
        )
        self.ui.glyphsrc_forest_start_box.setChecked(settings.shuffle.forest_glyph == "startwith")

        # Rabbits
        def rabbit_reset():
            self.ui.rabbit_all.setChecked(False)
            self.ui.rabbit_grass.setChecked(False)
            self.ui.rabbit_snow.setChecked(False)
            self.ui.rabbit_water.setChecked(False)
            self.ui.rabbit_fire.setChecked(False)
            self.ui.rabbit_sand.setChecked(False)

        rabbit_reset()
        for rabbit_mode in settings.shuffle.rabbitsanity:
            match rabbit_mode:
                case "grass":
                    self.ui.rabbit_grass.setChecked(True)
                case "snow":
                    self.ui.rabbit_snow.setChecked(True)
                case "water":
                    self.ui.rabbit_water.setChecked(True)
                case "fire":
                    self.ui.rabbit_fire.setChecked(True)
                case "sand":
                    self.ui.rabbit_sand.setChecked(True)
                case "all":
                    rabbit_reset()
                    self.ui.rabbit_all.setChecked(True)
                    break
                case _:
                    show_error(self, f"unsupported rabbit mode: {repr(rabbit_mode)}")

        self.ui.rabbit_pack.setChecked(settings.shuffle.rabbitpack)

        # Passengers
        self.ui.passenger_combo_box.setCurrentIndex(settings.shuffle.passengers_mode_map[settings.shuffle.passengers])

        # Cargo
        self.ui.cargo_combo_box.setCurrentIndex(settings.shuffle.cargo_mode_map[settings.shuffle.cargo])

        ### Settings - Dungeon Shuffle

        # Key Sanity
        self.ui.dgnshuffle_key_combo.setCurrentIndex(settings.shuffle_dgn.keysanity_mode_map[settings.shuffle_dgn.keysanity])
        self.ui.dgnshuffle_keyrings.setChecked(settings.shuffle_dgn.keyring)

        # Boss Key Sanity
        self.ui.dgnshuffle_bkey_combo.setCurrentIndex(settings.shuffle_dgn.bksanity_mode_map[settings.shuffle_dgn.bksanity])
        self.ui.dgnshuffle_bkeyrings.setChecked(settings.shuffle_dgn.bkeyring)

        # Tower Sections
        self.ui.dgnshuffle_sections_combo.setCurrentIndex(
            settings.shuffle_dgn.tos_sections_mode_map[settings.shuffle_dgn.tos_sections]
        )

        # Tear Sanity
        self.ui.dgnshuffle_tear_combo.setCurrentIndex(
            settings.shuffle_dgn.tear_sanity_mode_map[settings.shuffle_dgn.tear_sanity]
        )
        self.ui.dgnshuffle_tear_packs.setChecked(settings.shuffle_dgn.tear_ring)

        ### Settings - Goal

        # Dungeons
        self.ui.goal_dgn_tower_toggle.setChecked(settings.goal.is_tos_dungeon)
        self.ui.goal_dgn_amount.setValue(settings.goal.dungeon_amount)

        # Dark Realm
        self.ui.goal_dark_combo.setCurrentIndex(settings.goal.unlock_dark_realm_mode_map[settings.goal.unlock_dark_realm])

        self.disable_live_preset_update = False

    def save_preset(self, preset: str | None):
        """Updates the settings the preset's data following the current UI's state"""

        if preset == str():
            return

        if preset is not None and preset != "Custom":
            assert preset in self.presets, f"missing preset {repr(preset)}"
            settings = self.presets[preset]
        else:
            settings = self.live_preset

        ### Settings - Shuffle Land

        # Minigames
        def get_minigame_levels(kind: str) -> list[str]:
            levels = []

            widget: QCheckBox = getattr(self.ui, f"minigame_{kind}_easy")
            if widget.isChecked():
                levels.append("easy")

            widget: QCheckBox = getattr(self.ui, f"minigame_{kind}_hard")
            if widget.isChecked():
                levels.append("hard")

            widget: QCheckBox = getattr(self.ui, f"minigame_{kind}_expert")
            if widget.isChecked():
                levels.append("expert")

            return levels

        settings.shuffle.minigames.whip_race = get_minigame_levels("whip")
        settings.shuffle.minigames.pirate_hideout = get_minigame_levels("pirate")
        settings.shuffle.minigames.take_em_all_on = get_minigame_levels("takeem")
        settings.shuffle.minigames.sword_training = self.ui.minigame_sword.isChecked()
        settings.shuffle.minigames.goron_range = self.ui.minigame_goron.isChecked()

        # Shop Sanity
        settings.shuffle.shopsanity = self.ui.shop_amount.value()

        # Stamps
        settings.shuffle.stamps = self.ui.stamps.isChecked()
        settings.shuffle.stamp_book = self.ui.stamp_book.isChecked()

        settings.shuffle.stamps_rewards.clear()
        if self.ui.stamp_reward_10.isChecked():
            settings.shuffle.stamps_rewards.append(10)

        if self.ui.stamp_reward_15.isChecked():
            settings.shuffle.stamps_rewards.append(15)

        if self.ui.stamp_reward_20.isChecked():
            settings.shuffle.stamps_rewards.append(20)

        # Misc
        settings.shuffle.rupeesanity = self.ui.rupeesanity.isChecked()
        settings.shuffle.duets = self.ui.duets.isChecked()

        ### Settings - Shuffle Train

        # Glyphs and Sources
        settings.shuffle.glyphs_and_sources = settings.shuffle.glyphs_and_sources_mode_invmap[
            self.ui.glyphsrc_combo_box.currentIndex()
        ]
        settings.shuffle.forest_glyph = "startwith" if self.ui.glyphsrc_forest_start_box.isChecked() else "anywhere"

        # Rabbits
        settings.shuffle.rabbitsanity.clear()
        for rabbit_mode in settings.shuffle.rabbitsanity_mode:
            widget: QCheckBox = getattr(self.ui, f"rabbit_{rabbit_mode}")

            if widget.isChecked():
                if rabbit_mode == "all":
                    settings.shuffle.rabbitsanity = ["all"]
                    break

                settings.shuffle.rabbitsanity.append(rabbit_mode)

        settings.shuffle.rabbitpack = self.ui.rabbit_pack.isChecked()

        # Passengers
        settings.shuffle.passengers = settings.shuffle.passengers_mode_invmap[self.ui.passenger_combo_box.currentIndex()]

        # Cargo
        settings.shuffle.cargo = settings.shuffle.cargo_mode_invmap[self.ui.cargo_combo_box.currentIndex()]

        ### Settings - Dungeon Shuffle

        # Key Sanity
        settings.shuffle_dgn.keysanity = settings.shuffle_dgn.keysanity_mode_invmap[
            self.ui.dgnshuffle_key_combo.currentIndex()
        ]
        settings.shuffle_dgn.keyring = self.ui.dgnshuffle_keyrings.isChecked()

        # Boss Key Sanity
        settings.shuffle_dgn.bksanity = settings.shuffle_dgn.bksanity_mode_invmap[
            self.ui.dgnshuffle_bkey_combo.currentIndex()
        ]
        settings.shuffle_dgn.bkeyring = self.ui.dgnshuffle_bkeyrings.isChecked()

        # Tower Sections
        settings.shuffle_dgn.tos_sections = settings.shuffle_dgn.tos_sections_mode_invmap[
            self.ui.dgnshuffle_sections_combo.currentIndex()
        ]

        # Tear Sanity
        settings.shuffle_dgn.tear_sanity = settings.shuffle_dgn.tear_sanity_mode_invmap[
            self.ui.dgnshuffle_tear_combo.currentIndex()
        ]
        settings.shuffle_dgn.tear_ring = self.ui.dgnshuffle_tear_packs.isChecked()

        ### Settings - Goal

        # Dungeons
        settings.goal.is_tos_dungeon = self.ui.goal_dgn_tower_toggle.isChecked()
        settings.goal.dungeon_amount = self.ui.goal_dgn_amount.value()

        # Dark Realm
        settings.goal.unlock_dark_realm = settings.goal.unlock_dark_realm_mode_invmap[self.ui.goal_dark_combo.currentIndex()]

        self.ui.gen_string.setText(settings.to_str())

    # connection callbacks

    def do_select_rom(self):
        try:
            path = QFileDialog.getOpenFileName(
                None, "Open ROM (Supported: EUR Revision 0)", str(Path.cwd()), "(*.nds *.srl)"
            )[0]

            self.set_rom_path(Path(path))
        except Exception:
            show_error(self, f"An error occurred\n\n{traceback.format_exc()}")

    def do_select_out_folder(self):
        try:
            path = QFileDialog.getExistingDirectory(None, "Choose Output Folder", str(Path.cwd()))

            if len(path) > 0:
                self.ui.out_path.setText(path)
        except Exception:
            show_error(self, f"An error occurred\n\n{traceback.format_exc()}")

    def do_generate(self):
        if self.rom_version is None:
            return

        try:
            extracted_dir = EXTRACT_DIR / self.rom_version
            assert extracted_dir.exists(), "unexpected error"

            # create output folder
            out_path = Path(self.ui.out_path.text())

            if len(str(out_path)) == 0:
                raise ValueError("The output path is not set.")

            # checking the parent directory since the actual out folder might need to be created
            if not out_path.parent.exists():
                raise ValueError("The output path does not exist.")

            out_path.mkdir(exist_ok=True)

            # patch the code and update config
            apply_patches(extracted_dir, bps_dir=RES_DIR / "patches")
            ovl_list = [int(bps_path.stem.removeprefix("ov")) for bps_path in (RES_DIR / "patches").rglob("ov*.bps")]
            update_yaml(extracted_dir, RES_DIR / f"{RANDO_OVL_NAME}.map", ovl_list)
            (RES_DIR / f"{RANDO_OVL_NAME}.bin").copy(extracted_dir / "arm9_overlays" / f"{RANDO_OVL_NAME}.bin")

            # fetch preset
            preset_name = self.ui.gen_combo_preset.currentText()

            if preset_name != "Custom":
                preset = self.presets[preset_name]
            else:
                preset = self.live_preset

            # create generator instance
            gen = Generator(
                self.rom_version,
                preset,
                MODULE_PATH / "test" / "test_world.yaml",  # TODO: change that once the logic is done
                MODULE_PATH / "data" / "location_table.yaml",
                EXTRACT_DIR,
                out_path,
                do_create_log=self.ui.out_enable_spoilerlog.isChecked(),
            )

            # fetch the seed from the UI, if empty generate a new seed number
            seed = self.ui.gen_seed.text()

            if seed != str():
                gen.settings.seed = seed
            else:
                gen.create_seed()
                self.ui.gen_seed.setText(gen.settings.seed)

            # generate the seed
            self.ui.out_progress_bar.setValue(0)
            gen.generate_seed(patcher=self)
            gen.export_settings()

            # finally, repack the rom
            self.try_pack_rom(out_path / f"strando-{self.rom_version}-{gen.settings.seed}.nds")
        except Exception:
            show_error(self, f"An error occurred\n\n{traceback.format_exc()}")

    def do_change_preset(self, index: int):
        if index != 0:
            self.apply_preset(self.ui.gen_combo_preset.currentText())
        else:
            self.ui.gen_string.setText(self.live_preset.to_str())

    def do_save_preset(self):
        dialog = PresetSaveDialog(self)
        dialog.show()

    def do_live_preset_update(self, arg: Any):
        if self.disable_live_preset_update:
            return

        if self.ui.gen_combo_preset.currentText() != "Custom":
            self.ui.gen_combo_preset.setCurrentIndex(0)

        self.save_preset(None)

    def do_settings_string_update(self, text: str):
        try:
            self.live_preset = Settings.from_str(text)
            self.apply_preset(None)
        except Exception:
            show_error(self, f"An error occurred\n\n{traceback.format_exc()}")

    # overrides

    def closeEvent(self, a0):
        # remove generated files and folders
        if EXTRACT_DIR.exists():
            shutil.rmtree(EXTRACT_DIR)

        super().closeEvent(a0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
