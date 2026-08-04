#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 strando team
# SPDX-License-Identifier: GPL-3.0-only

import re
import yaml

from pathlib import Path


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
                overlay["file_name"] = f"{overlay['file_name'].removesuffix('.bin')}_mod.bin"
                break

    is_extra_overlay_present = map_path.stem in yaml_file["overlays"][-1]["file_name"]
    file_id = len(yaml_file["overlays"]) - 1 if is_extra_overlay_present else len(yaml_file["overlays"])
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
