#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 strando team
# SPDX-License-Identifier: GPL-3.0-only

import sys
import subprocess

from pathlib import Path


def create_patches(extracted_dir: Path):
    assert extracted_dir.exists()

    out_dir = Path("rando/res/patches/").resolve()
    out_dir.mkdir(exist_ok=True)

    exe = ".exe" if sys.platform == "nt" else ""
    program = Path(f"tools/flips/flips{exe}").resolve()
    assert program.exists()
    command_base = f"{program} --create --bps-delta"

    for ovl_mod_path in (extracted_dir / "arm9_overlays").rglob("*_mod.bin"):
        ovl = ovl_mod_path.stem.split("_")[0]
        ovl_path = ovl_mod_path.with_name(f"{ovl}.bin")
        assert ovl_path.exists()
        command = f"{command_base} {str(ovl_path)} {str(ovl_mod_path)} {str(out_dir / f'{ovl}.bps')}"
        subprocess.run(command, shell=True)

    command = f"{command_base} {str(extracted_dir / 'arm9' / 'arm9.bin')} {str(extracted_dir / 'arm9' / 'arm9_mod.bin')} {str(out_dir / 'arm9.bps')}"
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    command = f"{command_base} {str(extracted_dir / 'arm9' / 'itcm.bin')} {str(extracted_dir / 'arm9' / 'itcm_mod.bin')} {str(out_dir / 'itcm.bps')}"
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    extracted_dir = Path(sys.argv[1])  # extract/version/
    # extracted_dir = Path("extract/eur/")
    create_patches(extracted_dir)


if __name__ == "__main__":
    main()
