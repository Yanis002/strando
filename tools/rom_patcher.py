#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 stgz team
# SPDX-License-Identifier: GPL-3.0-only

import argparse
import re
import subprocess
import struct
import yaml

from dataclasses import dataclass
from pathlib import Path

INDENT = " " * 4

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--extract", type=Path, required=True)
parser.add_argument("-o", "--obj_list", dest="obj_list", nargs="+", help="list of .o file paths", required=True)
parser.add_argument("-m", "--main_max_size", required=True)
parser.add_argument("-j", "--hooks_obj_list", dest="hooks_obj_list", nargs="+", help="list of .o hooks file paths", required=True)
parser.add_argument("-n", "--hooks_max_size", required=True)
parser.add_argument("-a", "--address", required=True)
parser.add_argument("-d", "--hooks_build_dir", type=Path, required=True)
parser.add_argument("--elf", required=True)
parser.add_argument("--map", type=Path, required=True)
parser.add_argument("--hooks_elf", required=True)
parser.add_argument("--hooks_bin", type=Path, required=True)
parser.add_argument("--hooks_game_bin", type=Path, required=True)
args = parser.parse_args()

@dataclass
class Symbol:
    name: str
    addr: int

    @staticmethod
    def new(name: str, elf_path: str = args.elf):
        nm_path = Path("tools/binutils/arm-none-eabi-nm").resolve()
        assert nm_path.exists(), "binutils is missing"
        lines = subprocess.check_output([str(nm_path), elf_path], text=True).split("\n")

        found = False
        line = None
        for line in lines:
            if name in line:
                found = True
                break

        assert line is not None and found, "symbol not found!"
        return Symbol(name, int(line.split(" ")[0], base=16))

    def to_asm(self):
        return f".definelabel {self.name}, 0x{self.addr:08X}"


class SetupASM:
    def __init__(self, obj_list: list[str], hooks_obj_list: list[str], hooks_build_dir: Path, version: str):
        self.obj_list = obj_list
        self.hooks_obj_list = hooks_obj_list
        self.hooks_build_dir = hooks_build_dir
        self.version = version

    @staticmethod
    def new(version: str, obj_list: list[str], hooks_obj_list: list[str], hooks_build_dir: Path):
        return SetupASM(obj_list, hooks_obj_list, hooks_build_dir, version)

    def to_asm(self):
        # not sure yet if it's a good idea to generate this entire file but whatever

        lines = [
            "; This file was created by `tools/rom_patcher.py`",
            "\n",
            ".nds",
            ".relativeinclude on",
            ".erroronwarning on",
            "\n",
            Symbol.new("GZ_InitHook", elf_path=args.hooks_elf).to_asm(),
            "\n",
            ".open ITCM_BIN, ITCM_MOD_BIN, 0x01FF8000",
            INDENT + "; load the hooks into ITCM",
            INDENT + ".org HOOKS_ADDR",
            INDENT * 2 + ".area HOOKS_SIZE, 0xFF",
            INDENT * 3 + f'.incbin "../../../{args.hooks_bin}"',
            INDENT * 2 + ".endarea",
            ".close",
            "\n",
            ".open ARM9_BIN, ARM9_MOD_BIN, 0x02000000",
            INDENT + ".org HOOKS_GAME_ADDR",
            INDENT * 2 + ".area 0x390, 0x00",
            INDENT * 3 + f'.incbin "../../../{args.hooks_game_bin}"',
            INDENT * 2 + ".endarea",
            ".close",
            "\n",
            ".open OVL018_BIN, OVL018_MOD_BIN, OVL018_ADDR",
            INDENT + "; apply init hook",
            INDENT + ".org HOOK_INIT",
            INDENT * 2 + ".arm",
            INDENT * 2 + ".area 0x04",
            INDENT * 3 + "bl GZ_InitHook",
            INDENT * 2 + ".endarea",
            ".close",
            "\n",
        ]

        return "\n".join(lines)

    def write(self):
        self.hooks_build_dir.mkdir(exist_ok=True)
        setup_asm_file = self.hooks_build_dir / "setup.asm"
        setup_asm_file.resolve().write_text(self.to_asm())
        print("setup.asm is OK!")


def check_code_size(obj_list: list[str], max_size: int, kind: str):
    split = subprocess.check_output(["size", "--totals", *obj_list], text=True).split("\n")

    for elem in split:
        if "TOTALS" in elem:
            code_size = int(elem.split("\t")[-2].strip(), base=16)
            print(f"{kind} code size is OK! (code size: 0x{code_size:X} < max: 0x{max_size:X})")
            assert code_size < max_size, f"{kind} code size exceeds the available space! (code size: 0x{code_size:X} >= max: 0x{max_size:X})"
            break


def patch_arm9(extracted_dir: Path, base_addr: int, offset: int):
    # open and read file
    assert extracted_dir.exists()
    arm9_file = extracted_dir / "arm9" / "arm9.bin"
    arm9 = arm9_file.read_bytes()

    # update overlay hi
    arm9 = arm9.replace(struct.pack("<I", base_addr), struct.pack("<I", base_addr + offset))

    # write and close file
    arm9_file.with_name("arm9_patched.bin").write_bytes(arm9)


def get_extra_overlay(file_id: int):
    out = {"id": file_id}

    map_path: Path = args.map.resolve()
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


def update_yaml(extracted_dir: Path):
    # update arm9.bin and itcm.bin filenames
    config_yaml = extracted_dir / "config.yaml"

    with open(config_yaml, "r", encoding="utf-8") as file:
        yaml_file = yaml.safe_load(file)

    do_write = False

    if "_mod" not in  yaml_file["arm9_bin"]:
        yaml_file["arm9_bin"] = f"{yaml_file['arm9_bin'][:-4]}_mod.bin"
        do_write = True

    if "_mod" not in  yaml_file["itcm"]["bin"]:
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

    for overlay in yaml_file["overlays"]:
        if overlay.get("id") == 18 and "_mod" not in overlay["file_name"]:
            overlay["file_name"] = f"{overlay['file_name'].removesuffix('.bin')}_mod.bin"
            break

    is_extra_overlay_present = args.map.stem in yaml_file["overlays"][-1]["file_name"]
    file_id = len(yaml_file["overlays"]) - 1 if is_extra_overlay_present else len(yaml_file["overlays"])
    extra_overlay = get_extra_overlay(file_id)

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
    main_max_size = int(args.main_max_size, base=16)
    extracted_path: Path = args.extract.resolve()

    # make sure the overlay code size is ok
    check_code_size(args.obj_list, main_max_size, "Main")

    # make sure the hooks code size is ok
    check_code_size(args.hooks_obj_list, int(args.hooks_max_size, base=16), "Hooks")

    # patch the arm9 binary
    patch_arm9(extracted_path, int(args.address, base=16), main_max_size)

    # generate setup.asm
    setup_asm = SetupASM.new(extracted_path.stem, args.obj_list, args.hooks_obj_list, args.hooks_build_dir)
    setup_asm.write()

    # update yaml files
    update_yaml(extracted_path)


if __name__ == "__main__":
    main()
