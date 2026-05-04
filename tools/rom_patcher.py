#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 strando team
# SPDX-License-Identifier: GPL-3.0-only

import argparse
import re
import subprocess
import yaml

from dataclasses import dataclass
from pathlib import Path

CONFIG_DIR = Path("resources/decomp/config").resolve()
EXTRACTED_DIR = Path("extract")
INDENT = " " * 4

# dummy item based on force gems, we basically are copy pasting the thing and just changing the palette
# TODO: make a proper implementation?
DUMMY = f""".open "../../../extract/VERSION/files/Player/get/frcY.nsbmd", "../../../extract/VERSION/files/Player/get/dumy.nsbmd", 0x0
.close

.open "../../../extract/VERSION/files/Player/get/frcY.nsbtx", "../../../extract/VERSION/files/Player/get/dumy.nsbtx", 0x0
    .org 0x5C
        .area 0x04
        .word 0x0000007F
        .endarea

    .org 0x124
        .area 0x04
        .word 0x58284847
        .endarea

    .org 0x128
        .area 0x04
        .word 0x64296029
        .endarea

    .org 0x12C
        .area 0x04
        .word 0x6C8C6C4A
        .endarea

    .org 0x130
        .area 0x04
        .word 0x6DF36D0F
        .endarea
.close
"""


# from https://github.com/yaml/pyyaml/issues/127#issuecomment-525800484
class MyDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


@dataclass
class Symbol:
    name: str
    addr: int

    @staticmethod
    def new(name: str, elf_path: str):
        nm_path = Path("tools/binutils/arm-none-eabi-nm").resolve()
        assert nm_path.exists(), "binutils is missing"
        lines = subprocess.check_output([str(nm_path), elf_path], text=True).split("\n")

        found = False
        line = None
        for line in lines:
            if name in line:
                found = True
                break

        if line is None or not found:
            raise ValueError("symbol not found!")

        return Symbol(name, int(line.split(" ")[0], base=16))

    def to_asm(self):
        return f".definelabel {self.name}, 0x{self.addr:08X}"


@dataclass
class Constant:
    at_addr: int
    new_sym: Symbol | int

    def to_asm(self):
        addr = self.new_sym.addr if isinstance(self.new_sym, Symbol) else self.new_sym

        return [
            INDENT + f".org 0x{self.at_addr:08X}",
            INDENT * 2 + ".arm",
            INDENT * 2 + ".area 0x04",
            INDENT * 3 + f".word 0x{addr:08X}",
            INDENT * 2 + ".endarea",
        ]


@dataclass
class Instruction:
    at_addr: int
    new_sym: Symbol | None  # if none it will perform a nop instead of a bl
    is_blx: bool = False

    def to_asm(self):
        if self.new_sym is not None:
            instr = (
                f"blx {self.new_sym.name}" if self.is_blx else f"bl {self.new_sym.name}"
            )
        else:
            instr = "nop"

        return [
            INDENT + f".org 0x{self.at_addr:08X}",
            INDENT * 2 + ".arm",
            INDENT * 2 + ".area 0x04",
            INDENT * 3 + instr,
            INDENT * 2 + ".endarea",
        ]


@dataclass
class IncBin:
    at_addr: int
    size: int
    path: Path

    def to_asm(self):
        return [
            INDENT + f".org 0x{self.at_addr:08X}",
            INDENT * 2 + ".arm",
            INDENT * 2 + f".area 0x{self.size:02X}, 0x00",
            INDENT * 3 + f'.incbin "../../../{self.path}"',
            INDENT * 2 + ".endarea",
        ]


class Hook:
    def __init__(
        self,
        module: str,
        instrs: list[Instruction],
        constants: list[Constant] = list(),
        incbins: list[IncBin] = list(),
    ):
        self.module = module
        self.instrs = instrs
        self.constants = constants
        self.incbins = incbins

    def to_asm(self, version: str):
        base_dir = CONFIG_DIR / version / "arm9"

        match self.module:
            case "itcm":
                config_dir = base_dir / "itcm"
                bin_path = EXTRACTED_DIR / version / "arm9" / "itcm.bin"
            case "main":
                config_dir = base_dir
                bin_path = EXTRACTED_DIR / version / "arm9" / "arm9.bin"
            case _:
                config_dir = base_dir / "overlays" / self.module
                bin_path = (
                    EXTRACTED_DIR / version / "arm9_overlays" / f"{self.module}.bin"
                )
        assert config_dir.exists(), f"{config_dir} ({self.module})"
        assert bin_path.exists(), f"{bin_path} ({self.module})"

        if self.module == "itcm":
            module_addr = 0x01FF8000
        elif self.module == "main":
            module_addr = 0x02000000
        else:
            symbols = (config_dir / "symbols.txt").read_text().splitlines()
            module_addr = int(symbols[0].split("addr:")[-1].split(" ")[0], base=16)

        all_list: list[str] = []

        has_instrs = len(self.instrs) > 0
        has_constants = len(self.constants) > 0
        has_incbins = len(self.incbins) > 0

        if has_instrs:
            all_list.append(INDENT + "; instructions")
        for instr in self.instrs:
            all_list.extend(instr.to_asm())

        if has_constants:
            newline = ""
            if has_instrs:
                newline = "\n"

            all_list.append(newline + INDENT + "; constants")
        for const in self.constants:
            all_list.extend(const.to_asm())

        if has_incbins:
            newline = ""
            if has_instrs or has_constants:
                newline = "\n"

            all_list.append(newline + INDENT + "; incbins")
        for incbin in self.incbins:
            all_list.extend(incbin.to_asm())

        module = "arm9" if self.module == "main" else self.module
        return "\n".join(
            [
                f'.open "../../../{bin_path}", "../../../{bin_path.with_stem(f"{module}_mod")}", 0x{module_addr:08X}',
                "\n".join(all_list),
                ".close\n",
            ]
        )


@dataclass
class HooksConfig:
    version: str
    address: int
    size: int
    elf_path: Path
    hook_elf_path: Path
    hooks_bin: Path
    hooks_game_bin: Path
    hooks_size: int
    hooks_addr: int
    hooks_game_addr: int

    def __post_init__(self):
        self.hook_list = [
            Hook(
                "itcm",
                list(),
                incbins=[IncBin(self.hooks_addr, self.hooks_size, self.hooks_bin)],
            ),
            Hook(
                "main",
                list(),
                [
                    Constant(0x02012454, self.address + self.size),
                    Constant(0x02027914, self.address + self.size),
                ],
                [IncBin(self.hooks_game_addr, 0x390, self.hooks_game_bin)],
            ),
        ] + self.from_yaml()

    def from_yaml(self):
        data_dir = Path("hooks/data").resolve()
        assert data_dir.exists()

        hook_list: list[Hook] = []
        for yaml_path in data_dir.rglob("*.yaml"):
            with yaml_path.open("r") as file:
                yaml_file: dict = yaml.safe_load(file)

            def get_sym(in_sym: str):
                try:
                    return Symbol.new(in_sym, self.elf_path)
                except ValueError:
                    return Symbol.new(in_sym, self.hook_elf_path)

            instrs: list[Instruction] = []
            if "instructions" in yaml_file:
                def parse_bl(data: dict, is_blx: bool):
                    for target_sym, to_addrs in data.items():
                        for to_addr in to_addrs:
                            instrs.append(Instruction(int(to_addr, base=16), get_sym(target_sym), is_blx))

                if "bl" in yaml_file["instructions"]:
                    parse_bl(yaml_file["instructions"]["bl"], False)

                if "blx" in yaml_file["instructions"]:
                    parse_bl(yaml_file["instructions"]["blx"], True)

                if "nop" in yaml_file["instructions"]:
                    for to_addr in yaml_file["instructions"]["nop"]:
                        instrs.append(Instruction(int(to_addr, base=16), None))

            consts: list[Constant] = []
            if "constants" in yaml_file:
                for target_sym, to_addrs in yaml_file["constants"].items():
                    for to_addr in to_addrs:
                        sym = int(target_sym, base=16) if target_sym.startswith("0x") else get_sym(target_sym)
                        consts.append(Constant(int(to_addr, base=16), sym))

            incbins: list[IncBin] = []
            if "incbins" in yaml_file:
                for data in yaml_file["incbins"]:
                    for at_addr, infos in data.items():
                        incbins.append(IncBin(int(at_addr, base=16), int(infos["size"], base=16), Path(infos["path"])))

            hook_list.append(Hook(yaml_path.stem, instrs, consts, incbins))

        return hook_list

    def to_yaml(self):
        # unused function but keeping it anyway

        for hook in self.hook_list:
            yaml_file = {}

            if len(hook.instrs) > 0:
                yaml_file["instructions"] = {}

            for instr in hook.instrs:
                if instr.new_sym is not None:
                    sym = instr.new_sym.name

                    if instr.is_blx:
                        kind = "blx"
                    else:
                        kind = "bl"
                else:
                    sym = "None"
                    kind = "nop"

                at = f"0x{instr.at_addr:08X}"

                if kind == "nop":
                    if kind not in yaml_file["instructions"]:
                        yaml_file["instructions"][kind] = []

                    yaml_file["instructions"][kind].append(at)
                else:
                    if kind not in yaml_file["instructions"]:
                        yaml_file["instructions"][kind] = {}

                    if sym not in yaml_file["instructions"][kind]:
                        yaml_file["instructions"][kind][sym] = []

                    yaml_file["instructions"][kind][sym].append(at)

            if len(hook.constants) > 0:
                yaml_file["constants"] = {}

            for const in hook.constants:
                if isinstance(const.new_sym, Symbol):
                    sym = const.new_sym.name
                else:
                    sym = f"0x{const.new_sym:08X}"

                if sym not in yaml_file["constants"]:
                    yaml_file["constants"][sym] = []

                yaml_file["constants"][sym].append(f"0x{const.at_addr:08X}")

            if len(hook.incbins) > 0: 
                yaml_file["incbins"] = []

            for incbin in hook.incbins:
                yaml_file["incbins"].append(
                    {
                        f"0x{incbin.at_addr:08X}": {
                            "path": str(incbin.path),
                            "size": f"0x{incbin.size:02X}",
                        }
                    }
                )

            with open(Path(f"hook_defs/{hook.module}.yaml"), "w", encoding="utf-8") as file:
                yaml.dump(yaml_file, file, sort_keys=False, Dumper=MyDumper, default_flow_style=None, width=130)

    def get_ovl_list(self):
        ovl_list: list[int] = []

        for hook in self.hook_list:
            if hook.module.startswith("ov"):
                ovl = int(hook.module.removeprefix("ov"))

                if ovl not in ovl_list:
                    ovl_list.append(ovl)

        return ovl_list

    def get_instr_list(self):
        all_instrs: list[str] = []

        for hook in self.hook_list:
            for instr in hook.instrs:
                if instr.new_sym is not None:
                    asm = instr.new_sym.to_asm()

                    if asm not in all_instrs:
                        all_instrs.append(asm)

        return all_instrs

    def gen_hooks(self):
        all_instrs = self.get_instr_list()

        lines = [
            "; This file was created by `tools/gen_hooks.py`\n",
            ".nds",
            ".relativeinclude on",
            ".erroronwarning on\n",
            "\n".join(all_instrs) + "\n",
            "\n".join(hook.to_asm(self.version) for hook in self.hook_list) + "\n",
        ]

        return "\n".join(lines) + DUMMY.replace("VERSION", self.version)


def check_code_size(bin_path: Path, max_size: int, kind: str):
    hooks_data = bin_path.read_bytes()
    hooks_size = len(hooks_data)

    if len(hooks_data) < max_size:
        print(
            f"{kind} code size is OK! (code size: 0x{hooks_size:X} < max: 0x{max_size:X})"
        )
    else:
        raise ValueError(
            f"{kind} code size exceeds the available space! (code size: 0x{hooks_size:X} >= max: 0x{max_size:X})"
        )


def get_extra_overlay(map_path: Path, file_id: int):
    out = {"id": file_id}

    map_path: Path = map_path.resolve()
    assert map_path.exists(), "map file not found"
    filedata = map_path.read_text()

    data_match = re.search(r"\s*(0x[a-fA-F0-9]*)\s*_overlay_start = \.", filedata)
    assert data_match is not None, "overlay start not found in the map"
    out["base_address"] = int(data_match.group(1), base=16)

    data_match = re.search(r"\.text\s*0x[a-fA-F0-9]*\s*(0x[a-fA-F0-9]*)\n", filedata)
    assert data_match is not None, ".text size not found in the map"
    out["code_size"] = int(data_match.group(1), base=16)

    data_match = re.search(r"\.bss\s*0x[a-fA-F0-9]*\s*(0x[a-fA-F0-9]*)\n", filedata)
    assert data_match is not None, ".bss size not found in the map"
    out["bss_size"] = int(data_match.group(1), base=16)

    data_match = re.search(r"\.ctor\s*(0x[a-fA-F0-9]*)\s*(0x[a-fA-F0-9]*)\n", filedata)
    assert data_match is not None, ".ctor size not found in the map"
    out["ctor_start"] = int(data_match.group(1), base=16)
    out["ctor_end"] = out["ctor_start"] + int(data_match.group(2), base=16)

    out["file_id"] = file_id
    out["compressed"] = True
    out["signed"] = False
    out["file_name"] = f"{map_path.stem}.bin"
    return out


def update_yaml(extracted_dir: Path, map_path: Path, ovl_list: list[int]):
    # update arm9.bin and itcm.bin filenames
    config_yaml = extracted_dir / "config.yaml"

    with open(config_yaml, "r", encoding="utf-8") as file:
        yaml_file = yaml.safe_load(file)

    do_write = False

    if "_mod" not in yaml_file["arm9_bin"]:
        yaml_file["arm9_bin"] = f"{yaml_file['arm9_bin'][:-4]}_mod.bin"
        do_write = True

    if "_mod" not in yaml_file["itcm"]["bin"]:
        yaml_file["itcm"]["bin"] = f"{yaml_file['itcm']['bin'][:-4]}_mod.bin"
        do_write = True

    if do_write:
        with open(config_yaml, "w", encoding="utf-8") as file:
            yaml.safe_dump(yaml_file, file, sort_keys=False)

    # update itcm code size
    itcm_yaml = extracted_dir / "arm9" / "itcm.yaml"
    with open(itcm_yaml, "r", encoding="utf-8") as file:
        yaml_file = yaml.safe_load(file)

    yaml_file["code_size"] = 32768

    with open(itcm_yaml, "w", encoding="utf-8") as file:
        yaml.safe_dump(yaml_file, file, sort_keys=False)

    # add or update overlays
    overlays_yaml = extracted_dir / "arm9_overlays" / "overlays.yaml"

    with open(overlays_yaml, "r", encoding="utf-8") as file:
        yaml_file = yaml.safe_load(file)

    for ovl_id in ovl_list:
        for overlay in yaml_file["overlays"]:
            if overlay.get("id") == ovl_id and "_mod" not in overlay["file_name"]:
                overlay["file_name"] = (
                    f"{overlay['file_name'].removesuffix('.bin')}_mod.bin"
                )
                break

    is_extra_overlay_present = map_path.stem in yaml_file["overlays"][-1]["file_name"]
    file_id = (
        len(yaml_file["overlays"]) - 1
        if is_extra_overlay_present
        else len(yaml_file["overlays"])
    )
    extra_overlay = get_extra_overlay(map_path, file_id)

    if is_extra_overlay_present:
        # extra overlay is there, update it
        overlay = yaml_file["overlays"][-1]
        overlay["base_address"] = extra_overlay["base_address"]
        overlay["code_size"] = extra_overlay["code_size"]
        overlay["bss_size"] = extra_overlay["bss_size"]
        overlay["ctor_start"] = extra_overlay["ctor_start"]
        overlay["ctor_end"] = extra_overlay["ctor_end"]
        overlay["file_id"] = extra_overlay["file_id"]
        overlay["compressed"] = extra_overlay["compressed"]
        overlay["signed"] = extra_overlay["signed"]
        overlay["file_name"] = extra_overlay["file_name"]
    else:
        # extra overlay is not there, add it
        yaml_file["overlays"].append(extra_overlay)

    with open(overlays_yaml, "w", encoding="utf-8") as file:
        yaml.safe_dump(yaml_file, file, sort_keys=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", type=str.lower, required=True)
    parser.add_argument("--address", required=True)
    parser.add_argument("--size", required=True)
    parser.add_argument("--elf", type=Path, required=True)
    parser.add_argument("--hooks_addr", required=True)
    parser.add_argument("--hooks_elf", type=Path, required=True)
    parser.add_argument("--hooks_game_addr", required=True)
    parser.add_argument("--hooks_game_bin", type=Path, required=True)
    parser.add_argument("--hooks_size", required=True)
    args = parser.parse_args()

    main_addr = int(args.address, base=16)
    hooks_addr = int(args.hooks_addr, base=16)
    hooks_game_addr = int(args.hooks_game_addr, base=16)
    max_main_size = int(args.size, base=16)
    max_hooks_size = int(args.hooks_size, base=16)

    hooks_dir: Path = args.hooks_elf.parent.resolve()
    assert hooks_dir.exists()

    hooks_bin: Path = args.hooks_elf.with_suffix(".bin")
    main_map: Path = args.elf.with_suffix(".map")

    config = HooksConfig(
        args.version,
        main_addr,
        max_main_size,
        args.elf,
        args.hooks_elf,
        hooks_bin,
        args.hooks_game_bin,
        max_hooks_size,
        hooks_addr,
        hooks_game_addr,
    )

    hooks_asm = config.gen_hooks()

    setup_asm_file = hooks_dir / "setup.asm"
    setup_asm_file.resolve().write_text(hooks_asm)
    print("setup.asm is OK!")

    # make sure the overlay code size is ok
    check_code_size(args.elf.with_suffix(".bin"), max_main_size, "Main")

    # make sure the hooks code size is ok
    check_code_size(hooks_bin, max_hooks_size, "Hooks")

    # update yaml files
    update_yaml(EXTRACTED_DIR.resolve() / args.version, main_map, config.get_ovl_list())


if __name__ == "__main__":
    main()
