#!/usr/bin/env python3

import struct
import random
import copy

from dataclasses import dataclass
from ndspy import lz10 as LZSS
from ndspy import narc
from pathlib import Path


@dataclass
class ActorEntry:
    id: str # u32
    x: int # u16
    y: int # u16
    z: int # u16
    angle: int # u16
    params: list[int] # u16[4]
    unk_18: int # undetermined
    unk_1C: int # undetermined

    raw_data: bytes

    def __post_init__(self):
        assert self.raw_data == self.to_bytes(), f"{self.raw_data}, {self.to_bytes()}"

    @staticmethod
    def from_bytes(data: bytes):
        # print(data)
        raw_id, raw_x, raw_y, raw_z, raw_angle, raw_param1, raw_param2, raw_param3, raw_param4, raw_unk_18, raw_unk_1C = struct.unpack_from("<4sHHHHHHHHII", data)
        return ActorEntry(
            raw_id[::-1].decode(),
            raw_x,
            raw_y,
            raw_z,
            raw_angle,
            [raw_param1, raw_param2, raw_param3, raw_param4],
            raw_unk_18,
            raw_unk_1C,
            data[:0x20 - 4],
        )

    def to_bytes(self):
        return struct.pack(
            "<4sHHHHHHHHII",
            self.id[::-1].encode(),
            self.x,
            self.y,
            self.z,
            self.angle,
            self.params[0],
            self.params[1],
            self.params[2],
            self.params[3],
            self.unk_18,
            self.unk_1C,
        )


@dataclass
class MapObjectEntry:
    id: str # u32
    tile_x: int # u8
    tile_y: int # u8
    angle: int # u16
    params: list[int] # u8[4]
    unk_0C: int # undetermined
    unk_10: int # undetermined
    unk_14: int # undetermined
    unk_18: int # undetermined

    raw_data: bytes

    def __post_init__(self):
        assert self.raw_data == self.to_bytes()

    @staticmethod
    def from_bytes(data: bytes):
        raw_id, raw_x, raw_y, raw_angle, raw_param1, raw_param2, raw_param3, raw_param4, raw_unk_0C, raw_unk_10, raw_unk_14, raw_unk_18 = struct.unpack_from("<4sBBHBBBBIIII", data)
        return MapObjectEntry(
            raw_id[::-1].decode(),
            raw_x,
            raw_y,
            raw_angle,
            [raw_param1, raw_param2, raw_param3, raw_param4],
            raw_unk_0C,
            raw_unk_10,
            raw_unk_14,
            raw_unk_18,
            data[:0x1C],
        )

    def to_bytes(self):
        return struct.pack(
            "<4sBBHBBBBIIII",
            self.id[::-1].encode(),
            self.tile_x,
            self.tile_y,
            self.angle,
            self.params[0],
            self.params[1],
            self.params[2],
            self.params[3],
            self.unk_0C,
            self.unk_10,
            self.unk_14,
            self.unk_18,
        )


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
        print("found:", filename)
        return lzss_bytes, archive, found_file, filename

    return None

picked_items = []
def get_random_item():
    if len(picked_items) >= 116:
        picked_items.clear()
        print("WARNING: ran out of items")
        # raise ValueError("out of items")

    random_item = random.randint(1, 116)

    while random_item in picked_items:
        random_item = random.randint(1, 116)

    picked_items.append(random_item)
    return random_item


if __name__ == "__main__":
    scene_whitelist = [
        "t_area0",
        "t_area1",
        "t_area2",
        "t_area3",
        "t_tutorial",
        "t_forest",
        "t_smarine",
        "t_smount",
        "t_smount2",
        "t_smount3",
        "t_minigame",
        "t_dark",
        "t_eviltrain",
        "t_eviltrain2",
        "t_eviltrain3",
        "d_main",
        "d_main_f",
        "d_main_s",
        "d_main_a",
        "d_main_w",
        "d_tutorial",
        "d_forest",
        "d_snow",
        "d_water",
        "d_flame",
        "d_sand",
        "b_forest",
        "b_snow",
        "b_water",
        "b_flame",
        "b_sand",
        "b_deago",
        "b_last1",
        "b_last2",
        "b_last22",
        "b_last23",
        "f_hyral",
        "f_htown",
        "f_forest1",
        "f_snow",
        "f_water",
        "f_flame",
        "f_flame5",
        "f_first",
        "f_forest2",
        "f_snow2",
        "f_water2",
        "f_flame2",
        "f_sand",
        "f_tetsuo",
        "f_bridge",
        "f_bridge2",
        "f_forest3",
        "f_water3",
        "f_ajito",
        "f_ajito2",
        "f_flame3",
        "f_flame4",
        "f_rabbit",
        "f_kakushi1",
        "f_kakushi2",
        "f_kakushi3",
        "f_kakushi4",
        "f_pirate",
        "f_passenger",
        "f_trnnpc",
        "tekiya00",
        "tekiya01",
        "tekiya02",
        "tekiya03",
        "tekiya04",
        "tekiya05",
        "tekiya06",
        "tekiya07",
        "tekiya08",
        "tekiya09",
    ]

    actor_ids = [
        "GORY",
        "YUKY",
        "WAWY",
        "TERY",
        "FOMY",
        "CAMY",
        "SZKU",
        "KEYN",
    ]

    mapobj_ids = [
        "TRES",
        "TRED",
        "TREW",
        "TREN",
        "TRWS",
        "GELG",
        "TRLN",
        "TRLS",
        "TRLD",
        "TRLW",
    ]

    VERSION = "eur"

    map_dir = Path("extract").resolve() / VERSION / "files" / "Map"
    assert map_dir.exists()
    binary_list = list(map_dir.rglob("map*.bin"))
    random.shuffle(binary_list)

    final_list: list[Path] = []
    for lzss_path in binary_list:
        if lzss_path.parent.stem not in scene_whitelist:
            continue
        
        final_list.append(lzss_path)

    for lzss_path in final_list:
        lzss_bytes, archive, zmb_data, zmb_filename = get_zmb(lzss_path)

        if zmb_data is None:
            continue

        old_actor_entries: list[ActorEntry] = []
        old_mapobj_entries: list[MapObjectEntry] = []
        actor_entries: list[ActorEntry] = []
        mapobj_entries: list[MapObjectEntry] = []
        try:
            actor_offset = zmb_data.index(b"ACPN")

            magic, size, count, unk_0A = struct.unpack_from('<4sIHh', zmb_data, actor_offset)
            offset = actor_offset + 0x0C

            for i in range(count):
                actor_entries.append(ActorEntry.from_bytes(zmb_data[offset:offset + 0x20]))
                old_actor_entries.append(copy.copy(actor_entries[-1]))
                offset += 0x20

            for entry in actor_entries:
                for actor_id in actor_ids:
                    if entry.id == actor_id:
                        if entry.id in ["SZKU", "KEYN"]:
                            entry.params[0] = get_random_item()
                        else:
                            entry.params[0] = (get_random_item() << 8) | get_random_item()
                            entry.params[1] = (get_random_item() << 8) | get_random_item()
                            entry.params[2] = get_random_item()
        except ValueError:
            pass

        try:
            mapobj_offset = zmb_data.index(b"BOPM")

            magic, size, count, unk_0A = struct.unpack_from('<4sIHh', zmb_data, mapobj_offset)
            offset = mapobj_offset + 0x0C

            for i in range(count):
                mapobj_entries.append(MapObjectEntry.from_bytes(zmb_data[offset:offset + 0x1C]))
                old_mapobj_entries.append(copy.copy(mapobj_entries[-1]))
                offset += 0x1C
            
            for entry in mapobj_entries:
                for mapobj_id in mapobj_ids:
                    if entry.id == mapobj_id:
                        entry.params[0] = get_random_item()
        except ValueError:
            pass

        for i, entry in enumerate(actor_entries):
            old_data = old_actor_entries[i].raw_data
            new_data = entry.to_bytes()
            assert len(new_data) == len(old_data), f"{len(new_data)}, {len(old_data)}"
            assert old_data in zmb_data
            zmb_data = zmb_data.replace(old_data, new_data)
            assert new_data in zmb_data

        for i, entry in enumerate(mapobj_entries):
            old_data = old_mapobj_entries[i].raw_data
            new_data = entry.to_bytes()
            assert len(new_data) == len(old_data), f"{len(new_data)}, {len(old_data)}"
            assert old_data in zmb_data
            zmb_data = zmb_data.replace(old_data, new_data)
            assert new_data in zmb_data

        archive.setFileByName(zmb_filename, zmb_data)
        LZSS.compressToFile(archive.save(), lzss_path)

    print("placed", len(picked_items), "items")
