#!/usr/bin/env python3

import random
import struct
import time
import yaml

from dataclasses import dataclass
from ndspy import lz10 as LZSS
from ndspy import narc
from pathlib import Path
from rando.constants import ItemId, ItemKind, ItemWeight, item_id_to_name, shop_actor_ids, max_keys_map, tos_room_map, extra_id_to_scene


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


@dataclass
class ItemDef:
    id: ItemId
    kind: ItemKind
    weight: ItemWeight

    def is_random_treasure(self):
        return self.id >= ItemId.RandCommonTreasure and self.id <= ItemId.RandLegendaryTreasure


class BMGOffsets:
    def __init__(self):
        self.english: list[str] = []
        self.french: list[str] = []
        self.german: list[str] = []
        self.italian: list[str] = []
        self.spanish: list[str] = []

    def set_from_english(self, bmg: str):
        with Path("rando/data/bmg/flw1_offsets.yaml").open("r") as file:
            flw1_offsets = yaml.safe_load(file)

        flw1_offset_en = int(flw1_offsets["English"][bmg], base=16)

        for lang, data in flw1_offsets.items():
            flw1_offset = int(data[bmg], base=16)

            if lang == "English":
                continue

            do_sub = flw1_offset_en > flw1_offset
            diff = abs(flw1_offset_en - flw1_offset)
            for offset_s in self.english:
                offset = int(offset_s, base=16)
                new_offset = offset - diff if do_sub else offset + diff
                getattr(self, lang.lower()).append(f"0x{new_offset:X}")


class LocationInfo:
    def __init__(self, name: str, scene: str, room_index: int):
        self.name = name
        self.scene = scene
        self.room_index = room_index

        self.is_actor = False
        self.is_mapobj = False
        self.id_hash = str()

        self.is_bmg = False
        self.bmg = str()
        self.bmg_offsets = BMGOffsets()

        self.is_cs = False
        self.item_flag = str()

    @staticmethod
    def from_data(name: str, data: dict):
        new_info = LocationInfo(name, data["scene"], data["room_index"])

        if "is_bmg" in data:
            new_info.is_bmg = data["is_bmg"]
        else:
            if "is_actor" in data:
                new_info.is_actor = data["is_actor"]
            elif "is_mapobj" in data:
                new_info.is_mapobj = data["is_mapobj"]

            if "is_cs" in data:
                new_info.is_cs = data["is_cs"]

        if new_info.is_actor or new_info.is_mapobj:
            new_info.id_hash = data["id_hash"]
        elif new_info.is_bmg:
            new_info.bmg = data["bmg"]

            for lang, offsets in data["offsets"].items():
                getattr(new_info.bmg_offsets, lang).extend(offsets)

            new_info.bmg_offsets.set_from_english(new_info.bmg)

        return new_info

    @staticmethod
    def from_yaml(yaml_path: Path):
        infos: list["LocationInfo"] = []

        with yaml_path.open("r") as file:
            yaml_file: dict[str, dict] = yaml.safe_load(file)

        for name, data in yaml_file.items():
            infos.append(LocationInfo.from_data(name, data))

        return infos


@dataclass
class EntranceDef:
    name: str
    cond: str


class LocationDef:
    def __init__(self, name: str, cond: str, infos: LocationInfo):
        self.name = name
        self.cond = cond
        self.infos = infos

        # need 5 for shops
        self.items: list[ItemDef] = []


class LocationNode:
    def __init__(self, name: str, scene_name: str, room_index: int):
        self.name = name
        self.scene_name = scene_name
        self.room_index = room_index
        self.is_shop = False
        self.entrances: list[EntranceDef] = []
        self.locations: list[LocationDef] = []

        fix_map = {
            "d_snow26": "d_snow",
            "d_water27": "d_water",
        }

        self.lzss = Path(f"files/Map/{fix_map.get(self.scene_name, self.scene_name)}/map{self.room_index:02}.bin")

    @staticmethod
    def from_data(name: str, data: dict, info_entries: list[LocationInfo]):
        new_node = LocationNode(name, data["scene"], data["room_index"])

        if "is_shop" in data:
            new_node.is_shop = data["is_shop"]

        if "entrances" in data:
            for entry_name, entry_cond in data["entrances"].items():
                new_node.entrances.append(EntranceDef(entry_name, entry_cond))

        if "locations" in data:
            infos = None
            for entry_name, entry_cond in data["locations"].items():
                # get location info entry
                for info in info_entries:
                    if info.name == entry_name:
                        infos = info
                        break

                new_node.locations.append(LocationDef(entry_name, entry_cond, infos))

        return new_node

    @staticmethod
    def from_yaml(yaml_path: Path, yaml_infos: Path):
        info_entries = LocationInfo.from_yaml(yaml_infos)

        nodes: list["LocationNode"] = []

        with yaml_path.open("r") as file:
            yaml_file: dict[str, dict] = yaml.safe_load(file)

        for name, data in yaml_file.items():
            nodes.append(LocationNode.from_data(name, data, info_entries))

        return nodes

    def export(self):
        data = {
            '"scene"': self.scene_name,
            '"room_index"': self.room_index,
        }

        if self.is_shop:
            data['"is_shop"'] = True

        if len(self.entrances) > 0:
            data['"entrances"'] = {entry.name: entry.cond for entry in self.entrances}

        if len(self.locations) > 0:
            data['"locations"'] = {entry.name: entry.cond for entry in self.locations}

        return {f'"{self.name}"': data}


class SpoilerLogEntry:
    def __init__(self, node: LocationNode):
        self.node = node

    def get_params(self, items: list[ItemDef], is_shop: bool):
        if is_shop:
            return [
                {"Top Left": item_id_to_name[items[0].id.value]},
                {"Middle": item_id_to_name[items[1].id.value]},
                {"Top Right": item_id_to_name[items[2].id.value]},
                {"Bottom Left": item_id_to_name[items[3].id.value]},
                {"Bottom Right": item_id_to_name[items[4].id.value]},
            ]

        return item_id_to_name[items[0].id.value]

    def export(self):
        data = {}

        for location in self.node.locations:
            is_shop = len(location.items) > 1 and "Shop Keeper" in location.name
            data[location.name] = self.get_params(location.items, is_shop)

        return {self.node.name: {"locations": data}}


class SpoilerLog:
    def __init__(self, path: Path):
        self.path = path
        self.entries: list[SpoilerLogEntry] = []
        self.path.parent.mkdir(exist_ok=True)

    def export(self):
        self.entries.sort(key=lambda entry: entry.node.scene_name)
        entries = [entry.export() for entry in self.entries]

        yaml_file = {}
        for entry in entries:
            yaml_file.update(entry)

        with open(self.path, "w", encoding="utf-8") as file:
            yaml.dump(yaml_file, file, sort_keys=False, Dumper=MyDumper)


shop_scene_list = [
    "files/Map/f_flame5/map06.bin",
    "files/Map/f_forest1/map05.bin",
    "files/Map/f_htown/map10.bin",
    "files/Map/f_snow2/map03.bin",
    "files/Map/f_trnnpc/map03.bin",
    "files/Map/f_water/map02.bin",
]


item_defs: list[ItemDef] = [
    ItemDef(ItemId.Nothing, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.NormalShield, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.NormalSword, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.Whirlwind, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.BombBag, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.NormalBow, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.Boomerang, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.Whip, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.SandRod, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.Unk_9, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.BossKey, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.GreenRupee, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.BlueRupee, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.RedRupee, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.BigGreenRupee, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.BigRedRupee, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.BigGoldRupee, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.ForceGem_18, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_19, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_20, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForestGlyph, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.SnowGlyph, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.OceanGlyph, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.FireGlyph, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.Unk_25, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.Unk_26, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.Unk_27, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.Unk_28, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.Unk_29, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.FinalTrack, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.Unk_31, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.Unk_32, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.Unk_33, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.Unk_34, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.ForceGem_35, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_36, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_37, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.RecruitUniform, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.PostmasterLetter, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.HeartContainer, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.QuiverMedium, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.BombBagMedium, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.ForceGem_43, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_44, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_45, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_46, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_47, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_48, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_49, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_50, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_51, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_52, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_53, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_54, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_55, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_56, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_57, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_58, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_59, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_60, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_61, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.PanFlute, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.StampBook, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.LightBow, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.LokomoSword, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.TenPriceCard, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.RedPotion, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.PurplePotion, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.YellowPotion, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.DemonFossil, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.StalfosSkull, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.StarFragment, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.BeeLarvae, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.WoodHeart, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.DarkPearlLoop, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.WhitePearlLoop, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.RutoCrown, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.DragonScale, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.PirateNecklace, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.PalaceDish, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.GoronAmber, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.MysticJade, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.AncientCoin, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.PricelessStone, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.RegalRing, ItemKind.Default, ItemWeight.Progressive), # we consider the regal ring is a progressive item because of how you get to ocean land
    ItemDef(ItemId.ArrowsRefill, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.BombsRefill, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.SoldOutSign, ItemKind.Default, ItemWeight.Normal), # doesn't crash but buggy graphics
    ItemDef(ItemId.AncientShield, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.QuiverLarge, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.BombBagLarge, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.RandCommonTreasure, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.RandUncommonTreasure, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.RandRareTreasure, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.RandLegendaryTreasure, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.LightCompass, ItemKind.Default, ItemWeight.Progressive),
    ItemDef(ItemId.ScrollSpinAttack, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ScrollBeam, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.LinebeckLetter, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.PanFluteSong_101, ItemKind.Song, ItemWeight.Progressive),
    ItemDef(ItemId.PanFluteSong_102, ItemKind.Song, ItemWeight.Progressive),
    ItemDef(ItemId.PanFluteSong_103, ItemKind.Song, ItemWeight.Progressive),
    ItemDef(ItemId.PanFluteSong_104, ItemKind.Song, ItemWeight.Progressive),
    ItemDef(ItemId.PanFluteSong_105, ItemKind.Song, ItemWeight.Progressive),
    ItemDef(ItemId.RabbitNet, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.BeedleCard, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.SilverCard, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.GoldCard, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.PlatinumCard, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.DiamondCard, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.FreebieCard, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.QuintupleCard, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.CarbenLetter, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.RecruitUniform2, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.EngineerUniform, ItemKind.Default, ItemWeight.Priority),
]

# add extra tears
for i in range(1, 6):
    extra_defs = [ItemDef(getattr(ItemId, f"ExtraItemId_TearLight_{i}"), ItemKind.Default, ItemWeight.Progressive)] * 3
    item_defs.extend(extra_defs)

# add extra keys
for item_id, max_keys in max_keys_map.items():
    extra_defs = [ItemDef(item_id, ItemKind.Default, ItemWeight.Progressive)] * max_keys
    item_defs.extend(extra_defs)

progressive_item_pool = [item_def for item_def in item_defs if item_def.weight == ItemWeight.Progressive]
random.shuffle(progressive_item_pool)

priority_item_pool = [item_def for item_def in item_defs if item_def.weight == ItemWeight.Priority]
random.shuffle(priority_item_pool)

normal_item_pool = [item_def for item_def in item_defs if item_def.weight == ItemWeight.Normal]
random.shuffle(normal_item_pool)


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
        assert b"ACPN" in found_file or b"BOPM" in found_file
        return lzss_bytes, archive, found_file, filename

    return None


def replace_data(entry: ActorEntry | MapObjectEntry, base_data: bytes):
    old_data = entry.raw_data
    new_data = entry.to_bytes()
    assert len(new_data) == len(old_data), f"{len(new_data)}, {len(old_data)}"

    assert old_data in base_data
    new_zmb_data = base_data.replace(old_data, new_data)
    assert new_data in new_zmb_data

    return new_zmb_data


def get_random_itemdef(is_shop: bool):
    prog_length = len(progressive_item_pool)
    prio_length = len(priority_item_pool)
    normal_length = len(normal_item_pool)

    # each list is shuffled and we pick a random item as an attempt to create more randomness
    if prog_length > 0:
        index = 0 if (prog_length - 1) <= 1 else random.randint(1, prog_length - 1)
        item_def = progressive_item_pool.pop(index)
        # print("picked progression item!")
    elif prio_length > 0:
        index = 0 if (prio_length - 1) <= 1 else random.randint(1, prio_length - 1)
        item_def = priority_item_pool.pop(index)
        # print("picked priority item!")
    else:
        item_def = normal_item_pool[random.randint(1, normal_length - 1)]
        # print("picked normal item!")

    # prevent a crash with shops
    if is_shop and item_def.is_random_treasure():
        random_id = random.randint(ItemId.DemonFossil, ItemId.PricelessStone)

        for elem in item_defs:
            if elem.id.value == random_id:
                item_def = elem
                break

    return item_def


def get_random_item(is_shop: bool = False):
    return get_random_itemdef(is_shop).id


def get_offset(data: bytes, magic: bytes):
    try:
        return data.index(magic)
    except ValueError:
        return None


def assign_items(nodes: list[LocationNode]):
    random.shuffle(nodes)

    tos_map = {
        ItemId.ExtraItemId_TearLight_1: 1,
        ItemId.ExtraItemId_TearLight_2: 2,
        ItemId.ExtraItemId_TearLight_3: 3,
        ItemId.ExtraItemId_TearLight_4: 4,
        ItemId.ExtraItemId_TearLight_5: 5,
        ItemId.ExtraItemId_NormalKey_2: 2,
        ItemId.ExtraItemId_NormalKey_4: 4,
        ItemId.ExtraItemId_NormalKey_5: 5,
        ItemId.ExtraItemId_NormalKey_6: 6,
    }

    # assign the items randomly
    for node in nodes:
        assert len(node.locations) > 0
        random.shuffle(node.locations)

        for loc_def in node.locations:
            if node.is_shop and "Shop Keeper" in loc_def.name:
                for _ in range(5):
                    loc_def.items.append(get_random_itemdef(True))
            else:
                loc_def.items.append(get_random_itemdef(False))

        node.locations.sort(key=lambda entry: entry.name)

    nodes.sort(key=lambda entry: entry.name)


def patch_rom(base_dir: Path, nodes: list[LocationNode]):
    spoiler_log = SpoilerLog(Path("output/spoiler.yaml"))

    languages = [
        "English",
        "French",
        "German",
        "Italian",
        "Spanish",
    ]

    # patch the files
    for i, node in enumerate(nodes):
        lzss_path = base_dir / node.lzss
        lzss_bytes, archive, zmb_data, zmb_filename = get_zmb(lzss_path)

        do_save_narc = False
        for location in node.locations:
            assert node.scene_name == location.infos.scene
            assert node.room_index == location.infos.room_index

            if location.infos.is_bmg:
                for lang in languages:
                    bmg_path = base_dir / "files" / lang / "Message" / location.infos.bmg
                    assert bmg_path.exists()

                    bmg_data = bmg_path.read_bytes()
                    bmg_data_array = bytearray(bmg_data)

                    for raw_offset in getattr(location.infos.bmg_offsets, lang.lower()):
                        offset = int(raw_offset, base=16)
                        assert bmg_data[offset + 0x00] == 0x03 # FLW1 "event" instruction
                        assert bmg_data[offset + 0x01] == 0x09 # function callback index

                        # function callback parameters
                        bmg_data_array[offset + 0x04] = location.items[0].id.value

                    bmg_path.write_bytes(bytes(bmg_data_array))
            else:
                id, x, y = location.infos.id_hash.split("_")

                length = 1 if location.infos.is_mapobj else 2
                x_bytes = int(x, base=16).to_bytes(length, byteorder="little")
                y_bytes = int(y, base=16).to_bytes(length, byteorder="little")

                hash = id[::-1].encode() + x_bytes + y_bytes
                offset = get_offset(zmb_data, hash)
                assert offset is not None

                if location.infos.is_actor:
                    entry = ActorEntry.from_bytes(zmb_data[offset:offset + ActorEntry.entry_size])
                    do_save_narc = True

                    if entry.is_shop:
                        assert entry.is_shop == node.is_shop
                        top_left = location.items[0]
                        middle = location.items[1]
                        top_right = location.items[2]
                        bottom_left = location.items[3]
                        bottom_right = location.items[4]

                        entry.params[0] = (middle.id.value << 8) | top_left.id.value
                        entry.params[1] = (bottom_left.id.value << 8) | top_right.id.value
                        entry.params[2] = bottom_right.id.value
                    else:
                        entry.params[0] = location.items[0].id.value

                    zmb_data = replace_data(entry, zmb_data)
                elif location.infos.is_mapobj:
                    do_save_narc = True
                    entry = MapObjectEntry.from_bytes(zmb_data[offset:offset + MapObjectEntry.entry_size])
                    entry.params[0] = location.items[0].id.value
                    zmb_data = replace_data(entry, zmb_data)

        if do_save_narc:
            archive.setFileByName(zmb_filename, zmb_data)
            LZSS.compressToFile(archive.save(), lzss_path)

        spoiler_log.entries.append(SpoilerLogEntry(node))
        print(f"({(i / (len(nodes) - 1)) * 100:.2f}%) Processed", node.name)

    spoiler_log.export()


def main():
    VERSION = "eur"

    base_dir = Path("extract").resolve() / VERSION
    assert base_dir.exists()

    # 1. get location node list
    nodes = LocationNode.from_yaml(Path("rando/test/test_world.yaml"), Path("rando/data/location_table.yaml"))

    # 2. assign the items
    assign_items(nodes)

    # 3. update the rom files
    patch_rom(base_dir, nodes)


if __name__ == "__main__":
    print(f"Randomizing with {len(progressive_item_pool)} progressive items, {len(priority_item_pool)} priority items and {len(normal_item_pool)} remaining items...")
    prev_time = time.time()
    main()
    print(f"Done in {time.time() - prev_time:.3f}s!")
