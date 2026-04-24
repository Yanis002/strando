#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 stgz team
# SPDX-License-Identifier: GPL-3.0-only

import argparse
import os
import re
import subprocess

from dataclasses import dataclass
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", required=True)
parser.add_argument("-d", "--decomp", type=Path)
parser.add_argument("-e", "--elf")
args = parser.parse_args()


def gen_libst(libs_dir: Path):
    assert args.decomp is not None, "decomp path should be set"
    decomp_path: Path = args.decomp.resolve()
    config_path = decomp_path / "config"

    versions = [Path(path).stem for path, _, _ in os.walk(str(config_path)) if Path(path).parent.name == config_path.name]

    out_libs = {}
    out_thumbs = {}
    for version in versions:
        out_libs[version] = ""
        out_thumbs[version] = ""

    for version in versions:
        ver_cfg_path = config_path / version

        for sym_path in ver_cfg_path.rglob("symbols.txt"):
            filelines = sym_path.read_text().splitlines()

            for line in filelines:
                split = line.split(" ")
                sym_name = split.pop(0)

                is_local = False
                for elem in split:
                    if "local" in elem:
                        is_local = True
                        break

                # ignore static initializers, local and anonymous symbols (TODO: solve sqrt oddity)
                if "sinit" in sym_name or sym_name.startswith("@") or is_local or sym_name == "Sqrt":
                    continue

                kind_match = re.search(r"kind:function\(([a-zA-Z]*),", line)
                is_thumb_func = kind_match is not None and kind_match.group(1) == "thumb"

                addr_match = re.search(r"addr:0x([a-fA-F0-9]*)", line)
                assert addr_match is not None, f"address of {sym_name} not found"
                sym_addr = f"0x{addr_match.group(1).upper()}"
                addr = int(sym_addr, 16)

                if is_thumb_func:
                    addr += 1
                    out_thumbs[version] += f"thumb_func {sym_name}, 0x{addr:08X}\n"

                out_libs[version] += f"{sym_name} = 0x{addr:08X};\n"

    thumb_dir = Path("src").resolve() / "thumb"
    thumb_dir.mkdir(exist_ok=True, parents=True)

    thumb_header = [
        ".syntax unified\n",
        ".macro thumb_func name, addr",
        "    .global \\name",
        "    .type \\name, %function",
        "    .set \\name, \\addr",
        ".endm\n\n",
    ]

    for version in versions:
        symbols_path = libs_dir / f"libst-{version}.a"
        symbols_path.write_text(out_libs[version])
        print(f"libst-{version}.a is OK!")

        thumbs_file = thumb_dir / f"thumb-{version}.s"
        thumbs_file.write_text("\n".join(thumb_header) + out_thumbs[version])
        print(f"thumb-{version}.s is OK!")


@dataclass
class Symbol:
    name: str
    addr: int

    def to_txt(self):
        return f"{self.name} = 0x{self.addr:08X};"


class Symbols:
    def __init__(self):
        self.entries: list[Symbol] = []

        assert args.elf is not None, "argument missing: '--elf'"
        nm_path = Path("tools/binutils/arm-none-eabi-nm").resolve()
        assert nm_path.exists(), "binutils is missing"
        lines = subprocess.check_output([str(nm_path), args.elf], text=True).splitlines()

        for line in lines:
            sym_addr, sym_type, sym_name = line.split(" ")

            if sym_type != "A":
                self.entries.append(Symbol(sym_name, int(f"0x{sym_addr}", base=16)))

        assert len(self.entries) > 0, "symbols not found"

    def to_txt(self):
        return "\n".join(sym.to_txt() for sym in self.entries) + "\n"


def main():
    libs_dir = Path("libs").resolve()
    libs_dir.mkdir(exist_ok=True)

    if args.mode == "libst":
        gen_libst(libs_dir)
    elif args.mode == "libgz":
        libgz_path = libs_dir / "libgz.a"
        libgz_path.write_text(Symbols().to_txt())
        print("libgz.a is OK!")
    else:
        raise ValueError(f"ERROR: unknown mode '{args.mode}'")


if __name__ == "__main__":
    main()
