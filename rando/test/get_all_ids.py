#!/usr/bin/env python3

import random
import struct
import time
import yaml

from dataclasses import dataclass
from ndspy import lz10 as LZSS
from ndspy import narc
from pathlib import Path
from rando.constants import ItemId, ItemKind, ItemWeight, item_id_to_name, shop_actor_ids, actor_ids, mapobj_ids


# from https://github.com/yaml/pyyaml/issues/127#issuecomment-525800484
class MyDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


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

    is_shop: bool
    raw_data: bytes

    format = "<4sHHHHHHHHII"
    entry_size = 0x20

    def __post_init__(self):
        assert self.raw_data == self.to_bytes(), f"{self.raw_data}, {self.to_bytes()}"

    @property
    def id_hash(self):
        return f"{self.id}_0x{self.x:04X}_0x{self.y:04X}"

    @staticmethod
    def from_bytes(data: bytes):
        # print(data)
        raw_id, raw_x, raw_y, raw_z, raw_angle, raw_param1, raw_param2, raw_param3, raw_param4, raw_unk_18, raw_unk_1C = struct.unpack_from(ActorEntry.format, data)
        id = raw_id[::-1].decode()
        return ActorEntry(
            id,
            raw_x,
            raw_y,
            raw_z,
            raw_angle,
            [raw_param1, raw_param2, raw_param3, raw_param4],
            raw_unk_18,
            raw_unk_1C,
            id in shop_actor_ids,
            data[:ActorEntry.entry_size - 4],
        )

    def to_bytes(self):
        return struct.pack(
            ActorEntry.format,
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

    def get_params(self):
        if self.is_shop:
            return [
                {"Top Left": item_id_to_name[f"0x{self.params[0] & 0xFF:02X}"]},
                {"Middle": item_id_to_name[f"0x{(self.params[0] >> 8) & 0xFF:02X}"]},
                {"Top Right": item_id_to_name[f"0x{self.params[1] & 0xFF:02X}"]},
                {"Bottom Left": item_id_to_name[f"0x{(self.params[1] >> 8) & 0xFF:02X}"]},
                {"Bottom Right": item_id_to_name[f"0x{self.params[2] & 0xFF:02X}"]},
            ]

        return item_id_to_name[f"0x{self.params[0]:02X}"]


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

    format = "<4sBBHBBBBIIII"
    entry_size = 0x1C

    def __post_init__(self):
        assert self.raw_data == self.to_bytes()

    @property
    def id_hash(self):
        return f"{self.id}_0x{self.tile_x:02X}_0x{self.tile_y:02X}"

    @staticmethod
    def from_bytes(data: bytes):
        raw_id, raw_x, raw_y, raw_angle, raw_param1, raw_param2, raw_param3, raw_param4, raw_unk_0C, raw_unk_10, raw_unk_14, raw_unk_18 = struct.unpack_from(MapObjectEntry.format, data)
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
            data[:MapObjectEntry.entry_size],
        )

    def to_bytes(self):
        return struct.pack(
            MapObjectEntry.format,
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
    
    def get_params(self):
        return item_id_to_name[f"0x{self.params[0]:02X}"]


@dataclass
class EntranceDef:
    name: str
    cond: str


@dataclass
class LocationDef:
    name: str
    cond: str


class LocationNode:
    def __init__(self, name: str, scene_name: str, room_index: int):
        self.name = name
        self.scene_name = scene_name
        self.room_index = room_index
        self.is_shop = False
        self.entrances: list[EntranceDef] = []
        self.locations: list[LocationDef] = []

        self.fix_id_to_dir = {
            "d_snow26": "d_snow",
            "d_water27": "d_water",
        }
        self.fix_dir_to_id = {v: k for k, v in self.fix_id_to_dir.items()}

        self.lzss = Path(f"files/Map/{self.fix_id_to_dir.get(self.scene_name, self.scene_name)}/map{self.room_index:02}.bin")

    def export(self):
        scene_name = self.scene_name.removeprefix("files/Map/").split("/map")[0].split("/")[-1]
        data = {
            "scene": self.fix_dir_to_id.get(scene_name, scene_name),
            "room_index": self.room_index,
        }

        if self.is_shop:
            data["is_shop"] = True

        if len(self.entrances) > 0:
            data["entrances"] = {entry.name: entry.cond for entry in self.entrances}

        if len(self.locations) > 0:
            data["locations"] = {entry.name: entry.cond for entry in self.locations}

        return {f"{self.name}": data}


class SpoilerLogEntry:
    def __init__(self, scene_name: str, is_shop: bool):
        self.scene_name = scene_name
        self.actors: list[ActorEntry] = []
        self.mapobj: list[MapObjectEntry] = []
        self.is_shop = is_shop

    def allow_export(self):
        return len(self.actors) > 0 or len(self.mapobj) > 0

    def print(self):
        room_index = int(self.scene_name.split("/map")[-1].removesuffix(".bin"))
        return f"LocationNode({self.scene_name}, {self.scene_name}, {room_index})"

    def export(self):
        room_index = int(self.scene_name.split("/map")[-1].removesuffix(".bin"))
        node = LocationNode(self.scene_name, self.scene_name, room_index)

        if len(self.actors) > 0:
            self.actors.sort(key=lambda entry: entry.id_hash)
            node.locations.extend([LocationDef(entry.id_hash, f"NPCA - {entry.id};{entry.x};{entry.y}") for entry in self.actors])

        if len(self.mapobj) > 0:
            self.mapobj.sort(key=lambda entry: entry.id_hash)
            node.locations.extend([LocationDef(entry.id_hash, f"MPOB - {entry.id};{entry.tile_x};{entry.tile_y}") for entry in self.mapobj])

        node.is_shop = self.is_shop
        return node.export()


class SpoilerLog:
    def __init__(self):
        self.entries: list[SpoilerLogEntry] = []

    def print(self):
        self.entries.sort(key=lambda entry: entry.scene_name)

        for entry in self.entries:
            assert entry.allow_export()
            print(entry.export())

    def export(self):
        self.entries.sort(key=lambda entry: entry.scene_name)
        entries = [entry.export() for entry in self.entries if entry.allow_export()]

        yaml_file = {}
        for entry in entries:
            yaml_file.update(entry)

        with open(Path("rando/test/actors.yaml"), "w", encoding="utf-8") as file:
            yaml.dump(yaml_file, file, sort_keys=False, Dumper=MyDumper)


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

    return None, None, None, None


def get_offset(data: bytes, magic: bytes):
    try:
        return data.index(magic)
    except ValueError:
        return None


shop_scene_list = [
    "files/Map/f_flame5/map06.bin",
    "files/Map/f_forest1/map05.bin",
    "files/Map/f_htown/map10.bin",
    "files/Map/f_snow2/map03.bin",
    "files/Map/f_trnnpc/map03.bin",
    "files/Map/f_water/map02.bin",
]

exclude = [
    "WPHL",
    "FNCE",
    "BLCM",
    "SWST",
    "BFSP",
    "DRDS",
    "DRKY",
    "DRSW",
    "DRCK",
    "DRTC",
    "EXIT",
    "GRSS",
    "SWHT",
    "BMFL",
    "TSUB",
    "SKBN",
    "BREX",
    "TATZ",
    "STSP",
    "FSSN",
    "FRAI",
    "DRBK",
    "TREE",
    "STNE",
    "DRHS",
    "KNBN",
    "DRTY",
    "BLCK",
    "SWWN",
    "SWEY",
    "FRWL",
    "PTFL",
    "DRSN",
    "LVCM",
    "STSV",
    "PLV2",
    "DRBR",
    "WLMP",
    "LEVS",
    "SKDI",

    "AROW",
    "ASYU",
    "BAEY",
    "BAFO",
    "BAPH",
    "BBLE",
    "BDEA",
    "BDEM",
    "BLBL",
    "BLCK",
    "BLJF",
    "BMOC",
    "BOMB",
    "BSFC",
    "BSKM",
    "CASL",
    "CHUC",
    "CLLT",
    "CNBL",
    "CROW",
    "CTFS",
    "DKCL",
    "DKTR",
    "DLPN",
    "DSBB",
    "DSBH",
    "DSBN",
    "ENGE",
    "EVIC",
    "EWHI",
    "FBBH",
    "FCHL",
    "FIBB",
    "FIFI",
    "FIMA",
    "FIML",
    "FIRB",
    "FKTR",
    "FLCT",
    "FMAS",
    "FMLS",
    "FRBS",
    "FSSF",
    "FSST",
    "FTRN",
    "GOKI",
    "HERT",
    "KETH",
    "KEYB",
    "KIMA",
    "KLTR",
    "KMOS",
    "KMSO",
    "KOKO",
    "LAVA",
    "LBRC",
    "MABC",
    "MDYG",
    "MIFR",
    "MRDO",
    "NLTR",
    "NSHD",
    "NSSW",
    "NTTZ",
    "OCTA",
    "OCTS",
    "OCTW",
    "PCTG",
    "PHEY",
    "PHTM",
    "PMST",
    "PMTB",
    "PMTC",
    "PMTD",
    "PRSP",
    "PSBK",
    "PSBL",
    "PSWB",
    "RAT0",
    "RB1F",
    "RBFR",
    "RBNT",
    "RBRP",
    "RCHU",
    "RLST",
    "RMBC",
    "RMBD",
    "RMS0",
    "RMS1",
    "RMS2",
    "RMS3",
    "RMS4",
    "RMS5",
    "RMSD",
    "RMSF",
    "RMSS",
    "RMST",
    "RMSV",
    "RMSW",
    "RMTE",
    "ROCK",
    # "RUPE",
    "RYAW",
    "SCCN",
    "SEFS",
    "SHDL",
    "SNMA",
    "SNMB",
    "SNST",
    "SPAR",
    "SPBM",
    "SPID",
    "SPTR",
    "STFH",
    "STLF",
    "STTG",
    "SWBM",
    "TBRD",
    "TCOW",
    "TGTZ",
    "THER",
    "TPDO",
    "TRAP",
    "TRBC",
    "TRCB",
    "TRLY",
    "TRRL",
    "TRSG",
    "TRSP",
    "TRTT",
    "TRUP",
    "TTET",
    "TVLR",
    "WDBA",
    "WDRD",
    "WIDR",
    "WIDT",
    "WKTR",
    "WWFS",
    "ZLSL",
    "ZSRS",
    "ZSTG",
    "LIRA",
]


def main():
    VERSION = "eur"

    base_dir = Path("extract").resolve() / VERSION / "files" / "Map"
    assert base_dir.exists()

    spoiler_log = SpoilerLog()

    for scene in base_dir.rglob("map*.bin"):
        lzss_path = base_dir / scene
        lzss_bytes, archive, zmb_data, zmb_filename = get_zmb(lzss_path)

        if lzss_bytes is None:
            continue

        is_shop = False
        for s in shop_scene_list:
            if s in str(scene):
                is_shop = True
                break

        spoiler_entry = SpoilerLogEntry(str(scene), is_shop)

        assert b"ACPN" in zmb_data or b"BOPM" in zmb_data

        actor_offset = get_offset(zmb_data, b"ACPN")
        if actor_offset is not None:
            magic, size, actor_count, unk_0A = struct.unpack_from("<4sIHh", zmb_data, actor_offset)

            if actor_count > 0:
                offset = actor_offset + 0x0C
                for i in range(actor_count):
                    entry = ActorEntry.from_bytes(zmb_data[offset:offset + ActorEntry.entry_size])

                    if entry.id not in exclude:
                        spoiler_entry.actors.append(entry)
                    offset += ActorEntry.entry_size

        mapobj_offset = get_offset(zmb_data, b"BOPM")
        if mapobj_offset is not None:
            magic, size, count, unk_0A = struct.unpack_from("<4sIHh", zmb_data, mapobj_offset)

            if count > 0:
                offset = mapobj_offset + 0x0C
                for i in range(count):
                    entry = MapObjectEntry.from_bytes(zmb_data[offset:offset + MapObjectEntry.entry_size])
                    if entry.id not in exclude:
                        spoiler_entry.mapobj.append(entry)
                    offset += MapObjectEntry.entry_size

        # assert len(spoiler_entry.actors) > 0 or len(spoiler_entry.mapobj) > 0
        spoiler_log.entries.append(spoiler_entry)

    spoiler_log.export()

if __name__ == "__main__":
    main()
