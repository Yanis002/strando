#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 strando team
# SPDX-License-Identifier: GPL-3.0-only

import sys
import subprocess

from pathlib import Path


def apply_patches(extracted_dir: Path, bps_dir: Path = Path("res/patches/")):
    assert extracted_dir.exists()

    in_dir = bps_dir.resolve()
    in_dir.mkdir(exist_ok=True)

    exe = ".exe" if sys.platform == "nt" else ""
    program = Path(f"tools/flips/flips{exe}").resolve()
    assert program.exists()
    command_base = f"{program} --apply"

    for ovl_path in (extracted_dir / "arm9_overlays").rglob("*.bin"):
        if "_mod" in ovl_path.stem:
            continue

        ovl = ovl_path.stem.split("_")[0]
        ovl_mod_path = ovl_path.with_name(f"{ovl}_mod.bin")
        assert ovl_path.exists()
        bps_path = in_dir / f"{ovl}.bps"

        if bps_path.exists():
            command = f"{command_base} {str(bps_path)} {str(ovl_path)} {str(ovl_mod_path)}"
            subprocess.run(command, shell=True)

    command = f"{command_base} {str(in_dir / 'arm9.bps')} {str(extracted_dir / 'arm9' / 'arm9.bin')} {str(extracted_dir / 'arm9' / 'arm9_mod.bin')}"
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    command = f"{command_base} {str(in_dir / 'itcm.bps')} {str(extracted_dir / 'arm9' / 'itcm.bin')} {str(extracted_dir / 'arm9' / 'itcm_mod.bin')}"
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    extracted_dir = Path(sys.argv[1])  # extract/version/
    # extracted_dir = Path("extract/eur/")
    apply_patches(extracted_dir)


if __name__ == "__main__":
    main()
