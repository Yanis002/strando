#!/usr/bin/env python3

import struct

from ndspy import lz10 as LZSS
from ndspy import narc
from pathlib import Path


actor_ids = [
    "GORY", # Goron Village Shop Keeper
    "YUKY", # Snow Sanctuary Shop Keeper
    "WAWY", # Papuzia Shop Keeper
    "TERY", # Beedle
    "FOMY", # Mayscore Shop Keeper
    "CAMY", # Castle Town Shop Keeper
    "SZKU", # Tears of Light
    "KEYN", # Freestanding Small Keys
]

mapobj_ids = [
    "TRES",
    "TRED",
    "TREW",
    "TREN",
    "TRWS",
    "TRLN",
    "TRLS",
    "TRLD",
    "TRLW",
    "GELG",
]


def get_zmb(lzss_path: Path):
    assert lzss_path.exists()

    lzss_bytes = LZSS.decompressFromFile(lzss_path)
    archive = narc.NARC(lzss_bytes)

    found_file = None
    filename = None
    for i, file in enumerate(archive.files):
        if file.startswith(b"BPAM"):
            found_file = file
            filename = archive.filenames[i]
            break

    if found_file is not None and filename is not None:
        # print("found:", filename)
        return lzss_bytes, archive, found_file, filename

    return None


if __name__ == "__main__":
    VERSION = "eur"

    base_dir = Path("extract") / VERSION / "files"
    map_dir = base_dir / "Map"
    assert map_dir.exists()

    l = []
    for lzss_path in map_dir.rglob("map*.bin"):
        # filter out unreachable maps
        if "e3_" in lzss_path.parent.stem:
            continue

        lzss_bytes, archive, zmb_data, zmb_filename = get_zmb(lzss_path.resolve())

        # filter out maps without zmb data
        if zmb_data is None:
            continue

        # filter out maps without any actor or map objects
        if b"ACPN" not in zmb_data and b"BOPM" not in zmb_data:
            continue

        # filter out maps that don't contain any of the IDs we want to change 
        all_ids = actor_ids + mapobj_ids
        for id in all_ids:
            if struct.pack("<4s", id[::-1].encode()) in zmb_data:
                if "d_main/map01.bin" in str(lzss_path):
                    pass
                l.append(lzss_path)
                break

    for lzss_path in l:
        print(lzss_path)
    print(len(l))
