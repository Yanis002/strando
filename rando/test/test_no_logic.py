#!/usr/bin/env python3

import hashlib
import random
import re
import string
import struct
import time
import yaml

from dataclasses import dataclass
from ndspy import lz10 as LZSS, narc, bmg
from pathlib import Path
from rando.constants import (
    ItemId,
    ItemKind,
    ItemWeight,
    CustomSafeYAMLDumper,
    item_id_to_name,
    item_name_to_id,
    shop_actor_ids,
    shop_item_positions,
    tos_room_map,
)
from rando.settings import Settings, LocationSettings

TOS_SECTION_1_INDEX = 0
TOS_SECTION_2_INDEX = 1
TOS_SECTION_3_INDEX = 2
TOS_SECTION_4_INDEX = 3
TOS_SECTION_5_INDEX = 4
TOS_SECTION_6_INDEX = 5


@dataclass
class ActorEntry:
    id: str  # u32 (+0x00)
    x: int  # u16 (+0x04)
    y: int  # u16 (+0x06)
    z: int  # u16 (+0x08)
    angle: int  # u16 (+0x0A)
    params: list[int]  # u16[4] (+0x0C)
    unk_18: int  # undetermined
    unk_1C: int  # undetermined

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
        (
            raw_id,
            raw_x,
            raw_y,
            raw_z,
            raw_angle,
            raw_param1,
            raw_param2,
            raw_param3,
            raw_param4,
            raw_unk_18,
            raw_unk_1C,
        ) = struct.unpack_from(ActorEntry.format, data)
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
            data[: ActorEntry.entry_size - 4],
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
    id: str  # u32
    tile_x: int  # u8
    tile_y: int  # u8
    angle: int  # u16
    params: list[int]  # u16[4]
    unk_0C: int  # undetermined
    unk_10: int  # undetermined
    unk_14: int  # undetermined

    raw_data: bytes

    format = "<4sBBHHHHHIII"
    entry_size = 0x1C

    def __post_init__(self):
        assert self.raw_data == self.to_bytes()

    @property
    def id_hash(self):
        return f"{self.id}_0x{self.tile_x:02X}_0x{self.tile_y:02X}"

    @staticmethod
    def from_bytes(data: bytes):
        (
            raw_id,
            raw_x,
            raw_y,
            raw_angle,
            raw_param1,
            raw_param2,
            raw_param3,
            raw_param4,
            raw_unk_0C,
            raw_unk_10,
            raw_unk_14,
        ) = struct.unpack_from(MapObjectEntry.format, data)
        return MapObjectEntry(
            raw_id[::-1].decode(),
            raw_x,
            raw_y,
            raw_angle,
            [raw_param1, raw_param2, raw_param3, raw_param4],
            raw_unk_0C,
            raw_unk_10,
            raw_unk_14,
            data[: MapObjectEntry.entry_size],
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
        )


def get_tos_section_from_room(room_index: int):
    for section, room_indices in tos_room_map.items():
        if room_index in room_indices:
            return section

    return None


def get_item_name_suffix(settings: Settings, kind: ItemKind | None) -> str:
    if kind is None:
        return ""

    if (settings.shuffle.rabbitpack and kind == ItemKind.Rabbit) or (
        settings.shuffle_dgn.is_tearsanity_enabled() and settings.shuffle_dgn.tear_ring and kind == ItemKind.Tear
    ):
        # "X Rabbit Pack" or "X Tear of Light Pack"
        return " Pack"

    if settings.shuffle_dgn.is_keysanity_enabled() and settings.shuffle_dgn.keyring and kind == ItemKind.DungeonKey:
        # "X Key Ring"
        return " Ring"

    if settings.shuffle_dgn.is_bksanity_enabled() and settings.shuffle_dgn.bkeyring and kind == ItemKind.DungeonKey:
        # "X Boss Key Ring"
        return " Ring"

    return ""


@dataclass
class ItemDef:
    id: ItemId
    kind: ItemKind
    weight: ItemWeight

    def is_random_treasure(self):
        return self.id.value >= ItemId.RandCommonTreasure.value and self.id.value <= ItemId.RandLegendaryTreasure.value

    def is_small_key(self):
        return (
            self.id.value >= ItemId.ExtraItemId_NormalKey_2.value
            and self.id.value <= ItemId.ExtraItemId_NormalKey_Desert.value
        )

    def is_boss_key(self):
        return (
            self.id.value >= ItemId.ExtraItemId_BossKey_3.value and self.id.value <= ItemId.ExtraItemId_BossKey_Desert.value
        )

    def is_light_tear(self):
        return (
            self.id.value >= ItemId.ExtraItemId_TearLight_1.value and self.id.value <= ItemId.ExtraItemId_TearLight_5.value
        )

    def is_rabbit_net(self):
        return self.id.value == ItemId.RabbitNet.value

    def get_tos_section_from_tear(self):
        if not self.is_light_tear():
            return None

        match self.id.value:
            case ItemId.ExtraItemId_TearLight_1.value:
                return 1
            case ItemId.ExtraItemId_TearLight_2.value:
                return 2
            case ItemId.ExtraItemId_TearLight_3.value:
                return 3
            case ItemId.ExtraItemId_TearLight_4.value:
                return 4
            case ItemId.ExtraItemId_TearLight_5.value:
                return 5
            case _:
                return None


shop_item_map = {
    "GORY": [
        ItemDef(ItemId.BombsRefill, ItemKind.Default, ItemWeight.Normal),
        ItemDef(ItemId.YellowPotion, ItemKind.Default, ItemWeight.Normal),
        ItemDef(ItemId.PurplePotion, ItemKind.Default, ItemWeight.Normal),
        ItemDef(ItemId.NormalShield, ItemKind.Default, ItemWeight.Priority),
        ItemDef(ItemId.TenPriceCard, ItemKind.Default, ItemWeight.Priority),
    ],
    "YUKY": [
        ItemDef(ItemId.NormalShield, ItemKind.Default, ItemWeight.Priority),
        ItemDef(ItemId.RedPotion, ItemKind.Default, ItemWeight.Normal),
        ItemDef(ItemId.PurplePotion, ItemKind.Default, ItemWeight.Normal),
        ItemDef(ItemId.TenPriceCard, ItemKind.Default, ItemWeight.Priority),
        ItemDef(ItemId.RandRareTreasure, ItemKind.Default, ItemWeight.Normal),
    ],
    "WAWY": [
        ItemDef(ItemId.BombsRefill, ItemKind.Default, ItemWeight.Normal),
        ItemDef(ItemId.YellowPotion, ItemKind.Default, ItemWeight.Normal),
        ItemDef(ItemId.PurplePotion, ItemKind.Default, ItemWeight.Normal),
        ItemDef(ItemId.ArrowsRefill, ItemKind.Default, ItemWeight.Normal),
        ItemDef(ItemId.TenPriceCard, ItemKind.Default, ItemWeight.Priority),
    ],
    "TERY": [
        ItemDef(ItemId.PurplePotion, ItemKind.Default, ItemWeight.Normal),
        ItemDef(ItemId.BombsRefill, ItemKind.Default, ItemWeight.Normal),
        ItemDef(ItemId.RedPotion, ItemKind.Default, ItemWeight.Normal),
        ItemDef(ItemId.RandRareTreasure, ItemKind.Default, ItemWeight.Normal),
        ItemDef(ItemId.RandRareTreasure, ItemKind.Default, ItemWeight.Normal),
    ],
    "FOMY": [
        ItemDef(ItemId.NormalShield, ItemKind.Default, ItemWeight.Priority),
        ItemDef(ItemId.TenPriceCard, ItemKind.Default, ItemWeight.Priority),
        ItemDef(ItemId.RedPotion, ItemKind.Default, ItemWeight.Normal),
        ItemDef(ItemId.RandRareTreasure, ItemKind.Default, ItemWeight.Normal),
        ItemDef(ItemId.RandRareTreasure, ItemKind.Default, ItemWeight.Normal),
    ],
    "CAMY": [
        ItemDef(ItemId.NormalShield, ItemKind.Default, ItemWeight.Priority),
        ItemDef(ItemId.TenPriceCard, ItemKind.Default, ItemWeight.Priority),
        ItemDef(ItemId.RedPotion, ItemKind.Default, ItemWeight.Normal),
        ItemDef(ItemId.RandRareTreasure, ItemKind.Default, ItemWeight.Normal),
        ItemDef(ItemId.RandRareTreasure, ItemKind.Default, ItemWeight.Normal),
    ],
}

itemdef_nothing = ItemDef(ItemId.Nothing, ItemKind.Default, ItemWeight.Normal)

item_defs: list[ItemDef] = [
    itemdef_nothing,
    ItemDef(ItemId.NormalShield, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.NormalSword, ItemKind.Default, ItemWeight.Progression),
    ItemDef(ItemId.Whirlwind, ItemKind.Default, ItemWeight.Progression),
    ItemDef(ItemId.BombBag, ItemKind.Default, ItemWeight.Progression),
    ItemDef(ItemId.NormalBow, ItemKind.Default, ItemWeight.Progression),
    ItemDef(ItemId.Boomerang, ItemKind.Default, ItemWeight.Progression),
    ItemDef(ItemId.Whip, ItemKind.Default, ItemWeight.Progression),
    ItemDef(ItemId.SandRod, ItemKind.Default, ItemWeight.Progression),
    ItemDef(ItemId.Unk_9, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.BossKey, ItemKind.Default, ItemWeight.Progression),
    ItemDef(ItemId.GreenRupee, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.BlueRupee, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.RedRupee, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.BigGreenRupee, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.BigRedRupee, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.BigGoldRupee, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.FinalTrack, ItemKind.Default, ItemWeight.Progression),
    ItemDef(ItemId.Unk_31, ItemKind.Default, ItemWeight.Progression),
    ItemDef(ItemId.Unk_33, ItemKind.Default, ItemWeight.Progression),
    ItemDef(ItemId.Unk_34, ItemKind.Default, ItemWeight.Progression),
    ItemDef(ItemId.RecruitUniform, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.PostmasterLetter, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.QuiverMedium, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.BombBagMedium, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ForceGem_57, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.PanFlute, ItemKind.Default, ItemWeight.Progression),
    ItemDef(ItemId.LightBow, ItemKind.Default, ItemWeight.Progression),
    ItemDef(ItemId.LokomoSword, ItemKind.Default, ItemWeight.Progression),
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
    ItemDef(
        ItemId.RegalRing, ItemKind.Default, ItemWeight.Progression
    ),  # we consider the regal ring is a progression item because of how you get to ocean land
    ItemDef(ItemId.ArrowsRefill, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.BombsRefill, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.SoldOutSign, ItemKind.Default, ItemWeight.Normal),  # doesn't crash but buggy graphics
    ItemDef(ItemId.AncientShield, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.QuiverLarge, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.BombBagLarge, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.RandCommonTreasure, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.RandUncommonTreasure, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.RandRareTreasure, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.RandLegendaryTreasure, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.LightCompass, ItemKind.Default, ItemWeight.Progression),
    ItemDef(ItemId.ScrollSpinAttack, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.ScrollBeam, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.LinebeckLetter, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.PanFluteSong_101, ItemKind.Song, ItemWeight.Progression),
    ItemDef(ItemId.PanFluteSong_102, ItemKind.Song, ItemWeight.Progression),
    ItemDef(ItemId.PanFluteSong_103, ItemKind.Song, ItemWeight.Progression),
    ItemDef(ItemId.PanFluteSong_104, ItemKind.Song, ItemWeight.Progression),
    ItemDef(ItemId.PanFluteSong_105, ItemKind.Song, ItemWeight.Progression),
    ItemDef(ItemId.RabbitNet, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.BeedleCard, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.SilverCard, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.GoldCard, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.PlatinumCard, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.DiamondCard, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.FreebieCard, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.QuintupleCard, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.CarbenLetter, ItemKind.Default, ItemWeight.Normal),
    ItemDef(ItemId.RecruitUniform2, ItemKind.Default, ItemWeight.Priority),
    ItemDef(ItemId.EngineerUniform, ItemKind.Default, ItemWeight.Priority),
]


class BMGOffsets:
    def __init__(self):
        self.english: list[str] = []
        self.french: list[str] = []
        self.german: list[str] = []
        self.italian: list[str] = []
        self.spanish: list[str] = []

    def set_from_english(self, bmg: str):
        with Path("rando/data/bmg/flw1_offsets.yaml").open("r", encoding="utf-8") as file:
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
    def __init__(self, name: str, scene: str, room_index: int, rando_settings: Settings):
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

        self.settings = LocationSettings()
        self.rando_settings = rando_settings

        self.is_passenger_pick_up = False
        self.is_passenger_at_dest = False

        self.is_cargo_pick_up = False
        self.is_cargo_at_dest = False

        self.tos_section: int | None = None

    @staticmethod
    def from_data(name: str, data: dict, rando_settings: Settings):
        new_info = LocationInfo(name, data["scene"], data["room_index"], rando_settings)

        if "is_passenger_pick_up" in data:
            new_info.is_passenger_pick_up = data["is_passenger_pick_up"]
        elif "is_passenger_at_dest" in data:
            new_info.is_passenger_at_dest = data["is_passenger_at_dest"]

        if "is_cargo_pick_up" in data:
            new_info.is_cargo_pick_up = data["is_cargo_pick_up"]
        elif "is_cargo_at_dest" in data:
            new_info.is_cargo_at_dest = data["is_cargo_at_dest"]

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

        if "tos_section" in data:
            new_info.tos_section = data["tos_section"]
            assert new_info.tos_section == get_tos_section_from_room(new_info.room_index)

        if "settings" in data:

            def set_value_cond(
                value: str, valid_params: list[str], invalid_params: list[str], attr: str, is_bool: bool = True
            ):
                if value in valid_params:
                    setattr(new_info.settings, attr, True if is_bool else value)

                if getattr(new_info.settings, attr) and value in invalid_params:
                    setattr(new_info.settings, attr, False if is_bool else None)

            for elem in data["settings"]:
                split = elem.split("-")

                match split[0]:
                    case "rupee_sanity":
                        new_info.settings.rupeesanity = True
                    case "glyphs_and_sources":
                        new_info.settings.glyphs_and_sources = True
                    case "duets":
                        new_info.settings.duets = True
                    case "sword_training":
                        new_info.settings.sword_training = True
                    case "whip_race":
                        new_info.settings.whip_race = split[1]
                    case "goron_range":
                        new_info.settings.goron_range = True
                    case "pirate_hideout":
                        new_info.settings.pirate_hideout = split[1]
                    case "take_em_all_on":
                        new_info.settings.take_em_all_on = split[1]
                    case "stamps":
                        new_info.settings.stamps = True
                    case "stamps_rewards":
                        new_info.settings.stamps_rewards = int(split[1], base=0)
                    case "stamp_book":
                        new_info.settings.stamp_book = True
                    case "passengers":
                        set_value_cond(split[1], ["abstract", "anywhere"], ["remove", "vanilla"], "passengers")
                    case "cargo":
                        set_value_cond(split[1], ["abstract", "anywhere"], ["remove", "vanilla"], "cargo")
                    case "rabbit":
                        set_value_cond(
                            split[1],
                            ["grass", "snow", "water", "fire", "sand", "all"],
                            ["none"],
                            "rabbitsanity",
                            is_bool=False,
                        )
                    case "keysanity":
                        set_value_cond(split[1], ["dungeon", "anywhere"], ["removed", "vanilla"], "keysanity")
                    case "bkeysanity":
                        set_value_cond(split[1], ["dungeon", "anywhere"], ["removed", "vanilla"], "bkeysanity")
                    case "tearsanity":
                        set_value_cond(split[1], ["section", "dungeon", "anywhere"], ["removed", "vanilla"], "tearsanity")
                    case _:
                        print(f"WARNING: ignoring unknown setting {repr(elem)}!")

        return new_info

    @staticmethod
    def from_yaml(yaml_path: Path, settings: Settings):
        infos: list["LocationInfo"] = []

        with yaml_path.open("r") as file:
            yaml_file: dict[str, dict] = yaml.safe_load(file)

        for name, data in yaml_file.items():
            infos.append(LocationInfo.from_data(name, data, settings))

        return infos

    def check_settings(self):
        # ignore location if rupeesanity is disabled
        if self.settings.rupeesanity and not self.rando_settings.shuffle.rupeesanity:
            return False

        # ignore location if glyphs_and_sources is disabled (aka set to vanilla)
        if self.settings.glyphs_and_sources and not self.rando_settings.shuffle.glyphs_and_sources != "vanilla":
            return False

        # ignore duets if disabled
        if self.settings.duets and not self.rando_settings.shuffle.duets:
            return False

        # ignoring minigames we don't want
        if self.settings.sword_training and not self.rando_settings.shuffle.minigames.sword_training:
            return False

        if (
            len(self.settings.whip_race) > 0
            and self.settings.whip_race not in self.rando_settings.shuffle.minigames.whip_race
        ):
            return False

        if self.settings.goron_range and not self.rando_settings.shuffle.minigames.goron_range:
            return False

        if (
            len(self.settings.pirate_hideout) > 0
            and self.settings.pirate_hideout not in self.rando_settings.shuffle.minigames.pirate_hideout
        ):
            return False

        if (
            len(self.settings.take_em_all_on) > 0
            and self.settings.take_em_all_on not in self.rando_settings.shuffle.minigames.take_em_all_on
        ):
            return False

        # ignore stamps if we don't want them
        if self.settings.stamps and not self.rando_settings.shuffle.stamps:
            return False

        # ignore stamp rewards we don't want
        if (
            self.settings.stamps_rewards != 0
            and self.settings.stamps_rewards not in self.rando_settings.shuffle.stamps_rewards
        ):
            return False

        # ignore stamp book if we don't want it
        if self.settings.stamp_book and not self.rando_settings.shuffle.stamp_book:
            return False

        # ignore passenger location if we don't want it
        if self.settings.passengers and self.rando_settings.shuffle.passengers in ["remove", "vanilla"]:
            return False

        # ignore cargo location if we don't want it
        if self.settings.cargo and self.rando_settings.shuffle.cargo in ["remove", "vanilla"]:
            return False

        # ignore rabbit location if we don't want it
        if (
            self.settings.rabbitsanity is not None
            and "all" not in self.rando_settings.shuffle.rabbitsanity
            and self.settings.rabbitsanity not in self.rando_settings.shuffle.rabbitsanity
        ):
            return False

        # ignore keysanity if we don't want it
        # for "remove" mode we allow this location and we'll set the item to nothing later
        if self.settings.keysanity and self.rando_settings.shuffle_dgn == "vanilla":
            return False

        # ignore bkeysanity if we don't want it
        if self.settings.bkeysanity and self.rando_settings.shuffle_dgn == "vanilla":
            return False

        # ignore tearsanity if we don't want it
        if self.settings.tearsanity and self.rando_settings.shuffle_dgn == "vanilla":
            return False

        return True


@dataclass
class EntranceDef:
    name: str
    cond: str


class LocationDef:
    def __init__(self, name: str, cond: str, infos: LocationInfo):
        self.name = name
        self.cond = cond
        self.infos = infos

        dungeons = [
            "d_main",
            "d_tutorial",
            "d_forest",
            "d_snow26",
            "d_water27",
            "d_flame",
            "d_sand",
        ]
        self.is_dungeon = self.infos.scene in dungeons

        # need 1-5 for shops
        self.items: list[ItemDef] = []

    def allow_assign(self, settings: Settings, item: ItemDef):
        # don't process the picked item if the location is a rabbit and the picked item is the rabbit net
        if item.is_rabbit_net() and self.infos.settings.rabbitsanity is not None:
            return False

        if item.is_small_key() and settings.shuffle_dgn.keysanity == "dungeon" and not self.is_dungeon:
            return False

        if item.is_boss_key() and settings.shuffle_dgn.bksanity == "dungeon" and not self.is_dungeon:
            return False

        if item.is_light_tear():
            if settings.shuffle_dgn.tear_sanity == "dungeon" and not self.is_dungeon:
                return False

            if settings.shuffle_dgn.tear_sanity == "section":
                tear_section = item.get_tos_section_from_tear()

                if not self.is_dungeon or self.infos.tos_section is None or self.infos.tos_section != tear_section:
                    return False

        return True


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

        if "entrances" in data and data["entrances"] is not None:
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

                if infos is not None and infos.check_settings():
                    new_node.locations.append(LocationDef(entry_name, entry_cond, infos))

        return new_node

    @staticmethod
    def from_yaml(yaml_path: Path, yaml_infos: Path, settings: Settings):
        info_entries = LocationInfo.from_yaml(yaml_infos, settings)

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


class SeedLogEntry:
    def __init__(self, node: LocationNode):
        self.node = node

    def get_params(self, items: list[ItemDef], is_shop: bool, settings: Settings):
        if is_shop:
            ret = []
            for i, item in enumerate(items):
                ret.append(
                    {shop_item_positions[i]: item_id_to_name[item.id.value] + get_item_name_suffix(settings, item.kind)}
                )
            return ret

        return item_id_to_name[items[0].id.value] + get_item_name_suffix(settings, items[0].kind)

    def export(self, settings: Settings):
        data = {}

        for location in self.node.locations:
            is_shop = len(location.items) > 1 and "Shop Keeper" in location.name
            data[location.name] = self.get_params(location.items, is_shop, settings)

        return {self.node.name: {"locations": data}}


class SeedLog:
    def __init__(self, path: Path, seed: str, settings_string: str, yaml_file: dict | None = None):
        self.path = path
        self.seed = seed
        self.settings_string = settings_string
        self.yaml_file = yaml_file
        self.entries: list[SeedLogEntry] = []
        self.path.parent.mkdir(exist_ok=True)

    @staticmethod
    def from_yaml(yaml_path: Path) -> tuple["SeedLog", Settings]:
        with yaml_path.open("r") as file:
            yaml_file: dict[str, dict] = yaml.safe_load(file)

        settings = Settings.from_yaml(yaml_file["settings"])
        yaml_file.pop("settings")

        settings_string = settings.to_str()
        assert yaml_file["settings"]["string"] == settings_string
        new_log = SeedLog(yaml_path.with_stem(f"spoiler_{settings.seed}_parsed"), settings.seed, settings_string, yaml_file)
        return new_log, settings

    def export(self, settings: Settings):
        self.entries.sort(key=lambda entry: entry.node.scene_name)
        entries = [entry.export(settings) for entry in self.entries]

        yaml_file = settings.to_yaml()
        yaml_file["settings"]["string"] = settings.to_str()

        for entry in entries:
            yaml_file.update(entry)

        with open(self.path, "w", encoding="utf-8") as file:
            yaml.dump(yaml_file, file, sort_keys=False, Dumper=CustomSafeYAMLDumper)


class DungeonDef:
    def __init__(self, name: str, tos_section: int | None = None):
        self.name = name
        self.tos_section = tos_section
        self.keys: list[ItemDef] = []
        self.boss_keys: list[ItemDef] = []
        self.tears: list[ItemDef] = []
        self.locations: list[LocationDef] = []

    def fill_locations(self, locations: list[LocationDef], check_tos_section: bool = False):
        for loc in locations:
            if (
                check_tos_section
                and loc.infos.tos_section is not None
                and self.tos_section is not None
                and loc.infos.tos_section != self.tos_section
            ):
                continue

            if loc.is_dungeon and self.name == loc.infos.scene:
                self.locations.append(loc)


class Randomizer:
    def __init__(
        self, version: str, settings_path: Path, world_path: Path, loc_tbl_path: Path, seed_log_path: Path | None = None
    ):
        self.version = version
        self.extracted_dir = Path("extract").resolve() / self.version
        assert self.extracted_dir.exists()

        if seed_log_path is not None:
            self.seed_log, self.settings = SeedLog.from_yaml(seed_log_path)
        else:
            self.seed_log = None
            self.settings = Settings.from_yaml(settings_path)
            self.create_seed()

        self.dgn_tos_defs = [DungeonDef("d_main", tos_section=i) for i in range(1, 7)]
        self.dgn_tos_map = {section: dgn_def for section, dgn_def in enumerate(self.dgn_tos_defs)}

        self.dgn_tunnel_def = DungeonDef("d_tutorial")
        self.dgn_forest_def = DungeonDef("d_forest")
        self.dgn_snow_def = DungeonDef("d_snow26")
        self.dgn_marine_def = DungeonDef("d_water27")
        self.dgn_mount_def = DungeonDef("d_flame")
        self.dgn_sand_def = DungeonDef("d_sand")

        self.dgn_defs = self.dgn_tos_defs + [
            self.dgn_tunnel_def,
            self.dgn_forest_def,
            self.dgn_snow_def,
            self.dgn_marine_def,
            self.dgn_mount_def,
            self.dgn_sand_def,
        ]
        self.dgn_def_map = {i: dgn_def for i, dgn_def in enumerate(self.dgn_defs)}

        self.nodes = LocationNode.from_yaml(world_path, loc_tbl_path, self.settings)
        self.create_item_pool()

        # list of item ids that will be exported in the settings binary
        # "settings binary" refers to the data that is sent to the game from this generator
        self.passenger_pick_ids: list[int] = []
        self.passenger_dest_ids: list[int] = []
        self.cargo_pick_ids: list[int] = []

        # will assign items from the seed log if it's set
        # we can't do it earlier since we need the nodes and the item pool
        if self.seed_log is not None and self.seed_log.yaml_file is not None:
            self.assign_items_from_log()

        self.seed_num = 0
        self.set_seed_num()
        random.seed(self.seed_num)

    def create_item_pool(self):
        ## add additionnal items
        # 5 from dungeons, 8 from side quests
        heart_containers = [ItemDef(ItemId.HeartContainer, ItemKind.Default, ItemWeight.Normal)] * 13
        item_defs.extend(heart_containers)

        # add extra tears
        if self.settings.shuffle_dgn.is_tearsanity_enabled():
            for i in range(0, 5):
                assert i + 1 == self.dgn_tos_defs[i].tos_section

                self.dgn_tos_defs[i].tears = [
                    ItemDef(getattr(ItemId, f"ExtraItemId_TearLight_{i + 1}"), ItemKind.Tear, ItemWeight.Progression)
                ] * 3
                item_defs.extend(self.dgn_tos_defs[i].tears)

        add_keys = True
        if self.settings.shuffle_dgn.is_bksanity_enabled() and self.settings.shuffle_dgn.bkeyring:
            add_keys = False

        # add extra keys
        # TODO: improve this horrible thing
        if self.settings.shuffle_dgn.is_keysanity_enabled() and add_keys:
            self.dgn_tos_map[TOS_SECTION_2_INDEX].keys = [
                ItemDef(ItemId.ExtraItemId_NormalKey_2, ItemKind.DungeonKey, ItemWeight.Progression)
            ] * 2
            self.dgn_tos_map[TOS_SECTION_4_INDEX].keys = [
                ItemDef(ItemId.ExtraItemId_NormalKey_4, ItemKind.DungeonKey, ItemWeight.Progression)
            ] * 3
            self.dgn_tos_map[TOS_SECTION_5_INDEX].keys = [
                ItemDef(ItemId.ExtraItemId_NormalKey_5, ItemKind.DungeonKey, ItemWeight.Progression)
            ] * 2
            self.dgn_tos_map[TOS_SECTION_6_INDEX].keys = [
                ItemDef(ItemId.ExtraItemId_NormalKey_6, ItemKind.DungeonKey, ItemWeight.Progression)
            ] * 3
            self.dgn_tunnel_def.keys = [
                ItemDef(ItemId.ExtraItemId_NormalKey_Tunnel, ItemKind.DungeonKey, ItemWeight.Progression)
            ] * 1
            self.dgn_forest_def.keys = [
                ItemDef(ItemId.ExtraItemId_NormalKey_Wooded, ItemKind.DungeonKey, ItemWeight.Progression)
            ] * 2
            self.dgn_snow_def.keys = [
                ItemDef(ItemId.ExtraItemId_NormalKey_Blizzard, ItemKind.DungeonKey, ItemWeight.Progression)
            ] * 1
            self.dgn_marine_def.keys = [
                ItemDef(ItemId.ExtraItemId_NormalKey_Marine, ItemKind.DungeonKey, ItemWeight.Progression)
            ] * 2
            self.dgn_mount_def.keys = [
                ItemDef(ItemId.ExtraItemId_NormalKey_Mountain, ItemKind.DungeonKey, ItemWeight.Progression)
            ] * 3
            self.dgn_sand_def.keys = [
                ItemDef(ItemId.ExtraItemId_NormalKey_Desert, ItemKind.DungeonKey, ItemWeight.Progression)
            ] * 2

            item_defs.extend(
                self.dgn_tos_map[TOS_SECTION_2_INDEX].keys
                + self.dgn_tos_map[TOS_SECTION_4_INDEX].keys
                + self.dgn_tos_map[TOS_SECTION_5_INDEX].keys
                + self.dgn_tos_map[TOS_SECTION_6_INDEX].keys
                + self.dgn_tunnel_def.keys
                + self.dgn_forest_def.keys
                + self.dgn_snow_def.keys
                + self.dgn_marine_def.keys
                + self.dgn_mount_def.keys
                + self.dgn_sand_def.keys
            )

        # add extra boss keys
        if self.settings.shuffle_dgn.is_bksanity_enabled():
            self.dgn_tos_map[TOS_SECTION_3_INDEX].boss_keys = [
                ItemDef(ItemId.ExtraItemId_BossKey_3, ItemKind.DungeonKey, ItemWeight.Progression)
            ]
            self.dgn_tos_map[TOS_SECTION_5_INDEX].boss_keys = [
                ItemDef(ItemId.ExtraItemId_BossKey_5, ItemKind.DungeonKey, ItemWeight.Progression)
            ]
            self.dgn_forest_def.boss_keys = [
                ItemDef(ItemId.ExtraItemId_BossKey_Wooded, ItemKind.DungeonKey, ItemWeight.Progression)
            ]
            self.dgn_snow_def.boss_keys = [
                ItemDef(ItemId.ExtraItemId_BossKey_Blizzard, ItemKind.DungeonKey, ItemWeight.Progression)
            ]
            self.dgn_marine_def.boss_keys = [
                ItemDef(ItemId.ExtraItemId_BossKey_Marine, ItemKind.DungeonKey, ItemWeight.Progression)
            ]
            self.dgn_mount_def.boss_keys = [
                ItemDef(ItemId.ExtraItemId_BossKey_Mountain, ItemKind.DungeonKey, ItemWeight.Progression)
            ]
            self.dgn_sand_def.boss_keys = [
                ItemDef(ItemId.ExtraItemId_BossKey_Desert, ItemKind.DungeonKey, ItemWeight.Progression)
            ]

            item_defs.extend(
                self.dgn_tos_map[TOS_SECTION_3_INDEX].boss_keys
                + self.dgn_tos_map[TOS_SECTION_5_INDEX].boss_keys
                + self.dgn_forest_def.boss_keys
                + self.dgn_snow_def.boss_keys
                + self.dgn_marine_def.boss_keys
                + self.dgn_mount_def.boss_keys
                + self.dgn_sand_def.boss_keys
            )

        # add tower sections
        if self.settings.shuffle_dgn.tos_sections:
            sections = []
            for i in range(1, 6):
                sections.append(
                    ItemDef(getattr(ItemId, f"ExtraItemId_TowerSection_{i}"), ItemKind.Default, ItemWeight.Progression)
                )

        ## apply settings
        for _, shop_items in shop_item_map.items():
            for i in range(self.settings.shuffle.shopsanity):
                item_defs.append(shop_items[i])

        if self.settings.shuffle.rupeesanity:
            # rupeesanity adds 20 red rupees, 14 blue rupees and 4 big green rupees
            red_rupees = [ItemDef(ItemId.RedRupee, ItemKind.Default, ItemWeight.Normal)] * 20
            blue_rupees = [ItemDef(ItemId.BlueRupee, ItemKind.Default, ItemWeight.Normal)] * 14
            big_rupees = [ItemDef(ItemId.BigGreenRupee, ItemKind.Default, ItemWeight.Normal)] * 4
            item_defs.extend(red_rupees + blue_rupees + big_rupees)

        # only add glyphs/sources if we want them shuffled
        if self.settings.shuffle.glyphs_and_sources != "vanilla":
            glyphs = [
                ItemDef(ItemId.SnowGlyph, ItemKind.Default, ItemWeight.Progression),
                ItemDef(ItemId.OceanGlyph, ItemKind.Default, ItemWeight.Progression),
                ItemDef(ItemId.FireGlyph, ItemKind.Default, ItemWeight.Progression),
            ]

            # only add the forest glyph if we want it shuffled
            if self.settings.shuffle.forest_glyph == "anywhere":
                glyphs.append(ItemDef(ItemId.ForestGlyph, ItemKind.Default, ItemWeight.Progression))

            sources = [
                ItemDef(ItemId.ExtraItemId_ForestSource, ItemKind.Default, ItemWeight.Progression),
                ItemDef(ItemId.ExtraItemId_SnowSource, ItemKind.Default, ItemWeight.Progression),
                ItemDef(ItemId.ExtraItemId_OceanSource, ItemKind.Default, ItemWeight.Progression),
                ItemDef(ItemId.ExtraItemId_FireSource, ItemKind.Default, ItemWeight.Progression),
                ItemDef(ItemId.ExtraItemId_SandSource, ItemKind.Default, ItemWeight.Progression),
            ]

            item_defs.extend(glyphs + sources)

        # only add restoration songs if we want them shuffled
        if self.settings.shuffle.duets:
            songs = [
                ItemDef(ItemId.Unk_25, ItemKind.Default, ItemWeight.Progression),
                ItemDef(ItemId.Unk_26, ItemKind.Default, ItemWeight.Progression),
                ItemDef(ItemId.Unk_27, ItemKind.Default, ItemWeight.Progression),
                ItemDef(ItemId.Unk_28, ItemKind.Default, ItemWeight.Progression),
                ItemDef(ItemId.Unk_29, ItemKind.Default, ItemWeight.Progression),
            ]
            item_defs.extend(songs)

        # only add stamp stations if we want them shuffled
        if self.settings.shuffle.stamps:
            stamps = [
                ItemDef(ItemId.ExtraItemId_StampTowerOfSpirits, ItemKind.Default, ItemWeight.Priority),
                ItemDef(ItemId.ExtraItemId_StampCastleTown, ItemKind.Default, ItemWeight.Priority),
                ItemDef(ItemId.ExtraItemId_StampOutsetVillage, ItemKind.Default, ItemWeight.Priority),
                ItemDef(ItemId.ExtraItemId_StampMayscore, ItemKind.Default, ItemWeight.Priority),
                ItemDef(ItemId.ExtraItemId_StampWoodlandSanctuary, ItemKind.Default, ItemWeight.Priority),
                ItemDef(ItemId.ExtraItemId_StampAnoukiVillage, ItemKind.Default, ItemWeight.Priority),
                ItemDef(ItemId.ExtraItemId_StampSnowfallSanctuary, ItemKind.Default, ItemWeight.Priority),
                ItemDef(ItemId.ExtraItemId_StampPapuziaVillage, ItemKind.Default, ItemWeight.Priority),
                ItemDef(ItemId.ExtraItemId_StampIslandSanctuary, ItemKind.Default, ItemWeight.Priority),
                ItemDef(ItemId.ExtraItemId_StampGoronVillage, ItemKind.Default, ItemWeight.Priority),
                ItemDef(ItemId.ExtraItemId_StampValleySanctuary, ItemKind.Default, ItemWeight.Priority),
                ItemDef(ItemId.ExtraItemId_StampDuneSanctuary, ItemKind.Default, ItemWeight.Priority),
                ItemDef(ItemId.ExtraItemId_StampWoodedTemple, ItemKind.Default, ItemWeight.Priority),
                ItemDef(ItemId.ExtraItemId_StampBlizzardTemple, ItemKind.Default, ItemWeight.Priority),
                ItemDef(ItemId.ExtraItemId_StampMarineTemple, ItemKind.Default, ItemWeight.Priority),
                ItemDef(ItemId.ExtraItemId_StampMountainTemple, ItemKind.Default, ItemWeight.Priority),
                ItemDef(ItemId.ExtraItemId_StampDesertTemple, ItemKind.Default, ItemWeight.Priority),
                ItemDef(ItemId.ExtraItemId_StampPirateHideout, ItemKind.Default, ItemWeight.Priority),
                ItemDef(ItemId.ExtraItemId_StampTradingPost, ItemKind.Default, ItemWeight.Priority),
                ItemDef(ItemId.ExtraItemId_StampIcySpring, ItemKind.Default, ItemWeight.Priority),
            ]
            item_defs.extend(stamps)

        if self.settings.shuffle.stamp_book:
            item_defs.append(ItemDef(ItemId.StampBook, ItemKind.Default, ItemWeight.Priority))

        self.passenger_pick_pool = [
            ItemDef(ItemId.ExtraItemId_PassengerAnoukiNoko, ItemKind.PassengerPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_PassengerAnoukiKofu, ItemKind.PassengerPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_PassengerCastleTownMona, ItemKind.PassengerPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_PassengerCastleTownAlfonzo, ItemKind.PassengerPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_PassengerSnowRealmFerrus, ItemKind.PassengerPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_PassengerFireRealmFerrus, ItemKind.PassengerPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_PassengerGoronVillageSnowGoron, ItemKind.PassengerPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_PassengerGoronVillageCityGoron, ItemKind.PassengerPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_PassengerMayscoreDovok, ItemKind.PassengerPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_PassengerMayscoreMash, ItemKind.PassengerPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_PassengerMayscoreMorris, ItemKind.PassengerPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_PassengerMayscoreYamahiko, ItemKind.PassengerPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_PassengerMayscoreWood, ItemKind.PassengerPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_PassengerOutsetJoe, ItemKind.PassengerPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_PassengerPirateHideoutWadatsumi, ItemKind.PassengerPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_PassengerBridgeWorkersHomeKenzo, ItemKind.PassengerPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_PassengerTradingPostKenzo, ItemKind.PassengerPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_PassengerPapuziaVillageCarben, ItemKind.PassengerPickUp, ItemWeight.Progression),
        ]

        self.passenger_dest_pool: list[ItemDef | None] = [
            ItemDef(ItemId.ForceGem_53, ItemKind.PassengerAtDest, ItemWeight.Priority),  # Passenger_AnoukiNoko
            ItemDef(ItemId.ForceGem_36, ItemKind.PassengerAtDest, ItemWeight.Priority),  # Passenger_AnoukiKofu
            ItemDef(ItemId.ForceGem_48, ItemKind.PassengerAtDest, ItemWeight.Priority),  # Passenger_CastleTownMona
            ItemDef(ItemId.TrainCannon, ItemKind.PassengerAtDest, ItemWeight.Progression),  # Passenger_CastleTownAlfonzo
            ItemDef(ItemId.ForceGem_51, ItemKind.PassengerAtDest, ItemWeight.Priority),  # Passenger_SnowRealmFerrus
            ItemDef(ItemId.ForceGem_35, ItemKind.PassengerAtDest, ItemWeight.Priority),  # Passenger_FireRealmFerrus
            ItemDef(ItemId.ForceGem_54, ItemKind.PassengerAtDest, ItemWeight.Priority),  # Passenger_GoronVillageSnowGoron
            ItemDef(ItemId.ForceGem_37, ItemKind.PassengerAtDest, ItemWeight.Priority),  # Passenger_GoronVillageCityGoron
            ItemDef(ItemId.ForceGem_44, ItemKind.PassengerAtDest, ItemWeight.Priority),  # Passenger_MayscoreDovok
            None,  # Passenger_MayscoreMash
            None,  # Passenger_MayscoreMorris
            None,  # Passenger_MayscoreYamahiko
            None,  # Passenger_MayscoreWood
            ItemDef(ItemId.ForceGem_47, ItemKind.PassengerAtDest, ItemWeight.Priority),  # Passenger_OutsetJoe
            ItemDef(ItemId.ForceGem_18, ItemKind.PassengerAtDest, ItemWeight.Priority),  # Passenger_PirateHideoutWadatsumi
            None,  # Passenger_BridgeWorkersHomeKenzo
            None,  # Passenger_TradingPostKenzo
            ItemDef(ItemId.ForceGem_45, ItemKind.PassengerAtDest, ItemWeight.Priority),  # Passenger_PapuziaVillageCarben
        ]

        if self.settings.shuffle.passengers == "anywhere":
            item_defs.extend(self.passenger_pick_pool)

        if self.settings.shuffle.passengers != "remove":
            passenger_dest_pool = [item for item in self.passenger_dest_pool if item is not None]
            item_defs.extend(passenger_dest_pool)

        self.cargo_pick_pool = [
            ItemDef(ItemId.ExtraItemId_CargoMegaIce, ItemKind.CargoPickUp, ItemWeight.Progression),
            ItemDef(ItemId.ExtraItemId_CargoWood, ItemKind.CargoPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_CargoIron, ItemKind.CargoPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_CargoFish, ItemKind.CargoPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_CargoCuccos, ItemKind.CargoPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_CargoVessel, ItemKind.CargoPickUp, ItemWeight.Priority),
            ItemDef(ItemId.ExtraItemId_CargoDarkOre, ItemKind.CargoPickUp, ItemWeight.Priority),
        ]

        self.cargo_dest_pool = [
            ItemDef(ItemId.ForceGem_19, ItemKind.CargoAtDest, ItemWeight.Priority),  # papuzia ice
            ItemDef(ItemId.ForceGem_20, ItemKind.CargoAtDest, ItemWeight.Priority),  # goron village ice (2nd time?)
            ItemDef(ItemId.ForceGem_43, ItemKind.CargoAtDest, ItemWeight.Priority),  # castle town fish
            ItemDef(ItemId.ForceGem_46, ItemKind.CargoAtDest, ItemWeight.Priority),  # lokomo cuccos
            ItemDef(ItemId.ForceGem_49, ItemKind.CargoAtDest, ItemWeight.Priority),  # outset cuccos
            ItemDef(ItemId.ForceGem_50, ItemKind.CargoAtDest, ItemWeight.Priority),  # mayscore steel
            ItemDef(ItemId.ForceGem_52, ItemKind.CargoAtDest, ItemWeight.Priority),  # anouki fence wood
            ItemDef(ItemId.ForceGem_55, ItemKind.CargoAtDest, ItemWeight.Priority),  # lokomo vessel
            ItemDef(ItemId.ForceGem_56, ItemKind.CargoAtDest, ItemWeight.Priority),  # linebeck dark ore
        ]

        if self.settings.shuffle.cargo == "anywhere":
            item_defs.extend(self.cargo_pick_pool)

        if self.settings.shuffle.cargo != "remove":
            item_defs.extend(self.cargo_dest_pool)

        if self.settings.shuffle.is_rabbitsanity_enabled():
            rabbit_pool: list[ItemDef] = []
            is_all = "all" in self.settings.shuffle.rabbitsanity
            factor = 1 if self.settings.shuffle.rabbitpack else 10

            if is_all or "grass" in self.settings.shuffle.rabbitsanity:
                rabbit_pool.extend([ItemDef(ItemId.ExtraItemId_RabbitGrass, ItemKind.Rabbit, ItemWeight.Priority)] * factor)

            if is_all or "snow" in self.settings.shuffle.rabbitsanity:
                rabbit_pool.extend([ItemDef(ItemId.ExtraItemId_RabbitSnow, ItemKind.Rabbit, ItemWeight.Priority)] * factor)

            if is_all or "water" in self.settings.shuffle.rabbitsanity:
                rabbit_pool.extend([ItemDef(ItemId.ExtraItemId_RabbitWater, ItemKind.Rabbit, ItemWeight.Priority)] * factor)

            if is_all or "mountain" in self.settings.shuffle.rabbitsanity:
                rabbit_pool.extend(
                    [ItemDef(ItemId.ExtraItemId_RabbitMountain, ItemKind.Rabbit, ItemWeight.Priority)] * factor
                )

            if is_all or "sand" in self.settings.shuffle.rabbitsanity:
                rabbit_pool.extend([ItemDef(ItemId.ExtraItemId_RabbitSand, ItemKind.Rabbit, ItemWeight.Priority)] * factor)

            item_defs.extend(rabbit_pool)

        ## create the pools
        self.progression_item_pool = [item_def for item_def in item_defs if item_def.weight == ItemWeight.Progression]
        self.priority_item_pool = [item_def for item_def in item_defs if item_def.weight == ItemWeight.Priority]
        self.normal_item_pool = [item_def for item_def in item_defs if item_def.weight == ItemWeight.Normal]
        self.all_item_pool = item_defs[:]

    # seed methods from https://github.com/OoTRandomizer/OoT-Randomizer/blob/2900fedb4a5ccd6937db85ec4f15721556656815/Settings.py#L253-L270
    def sanitize(self, s):
        return re.sub(r"[^a-zA-Z0-9_-]", "", s)

    def create_seed(self):
        self.settings.seed = self.sanitize("".join(random.choices(string.ascii_uppercase + string.digits, k=10)))

    def set_seed_num(self):
        final_seed = self.settings.seed
        self.seed_num = int(hashlib.sha256(final_seed.encode("utf-8")).hexdigest(), base=16)

    def get_zmb(self, lzss_path: Path):
        assert lzss_path.exists()

        lzss_bytes = LZSS.decompressFromFile(lzss_path)
        archive = narc.NARC(lzss_bytes)

        found_file = None
        filename = None
        for i, file in enumerate(archive.files):
            if file.startswith(b"BPAM1BMZ"):
                found_file = file
                filename = str(archive.filenames[i])
                break

        if found_file is not None and filename is not None:
            # print("found:", filename)
            assert b"ACPN" in found_file or b"BOPM" in found_file
            return lzss_bytes, archive, found_file, filename

        raise ValueError("ERROR: unexpected result")

    def update_zmb(self, entry: ActorEntry | MapObjectEntry, base_data: bytes):
        old_data = entry.raw_data
        new_data = entry.to_bytes()
        assert len(new_data) == len(old_data), f"{len(new_data)}, {len(old_data)}"

        assert old_data in base_data
        new_zmb_data = base_data.replace(old_data, new_data)
        assert new_data in new_zmb_data

        return new_zmb_data

    def init_id_lists(self):
        """Initializes the item id lists that will be exported in the settings binary"""

        if self.settings.shuffle.passengers != "anywhere":
            # if not anywhere keep it vanilla
            self.passenger_dest_ids.clear()

            for item in self.passenger_dest_pool:
                # 0xFF for ItemId_None
                self.passenger_dest_ids.append(item.id.value if item is not None else 0xFF)

            self.passenger_pick_ids = [item.id.value for item in self.passenger_pick_pool]

        if self.settings.shuffle.cargo != "anywhere":
            self.cargo_pick_ids = [item.id.value for item in self.cargo_pick_pool]

    def add_elem_to_id_lists(self, location: LocationDef, item: ItemDef):
        """Tries to add the item's id to the lists that will be exported in the settings binary"""

        if self.settings.shuffle.passengers == "anywhere":
            if location.infos.is_passenger_pick_up:
                self.passenger_pick_ids.append(item.id.value)
            elif location.infos.is_passenger_at_dest:
                self.passenger_dest_ids.append(item.id.value)

        if self.settings.shuffle.cargo == "anywhere":
            if location.infos.is_cargo_pick_up:
                self.cargo_pick_ids.append(item.id.value)

    def copy_id_lists_to_settings(self):
        """Copies the item id lists to the settings"""

        self.settings.passenger_pick_ids = self.passenger_pick_ids[:]
        self.settings.passenger_dest_ids = self.passenger_dest_ids[:]
        self.settings.cargo_pick_ids = self.cargo_pick_ids[:]

    def assign_items_from_log(self):
        assert self.seed_log is not None and self.seed_log.yaml_file is not None

        def find_item_def(item_id: int):
            for item_def in self.all_item_pool:
                if item_def.id.value == item_id:
                    return item_def

            return None

        def strip_name(name: str):
            if name.endswith(" Rabbit Pack"):
                return name.removesuffix(" Pack")
            return name

        self.init_id_lists()

        for node in self.nodes:
            for location in node.locations:
                elem: list | str = self.seed_log.yaml_file[node.name]["locations"][location.name]

                if isinstance(elem, str):
                    item_def = find_item_def(item_name_to_id[strip_name(elem)])
                    assert item_def is not None, f"item_def is none ({elem})"
                    location.items.append(item_def)
                    self.add_elem_to_id_lists(location, item_def)
                elif isinstance(elem, list):
                    for i in range(0, 5):
                        item_def = find_item_def(item_name_to_id[strip_name(elem[i][shop_item_positions[i]])])
                        assert item_def is not None, f"item_def is none ({elem})"
                        location.items.append(item_def)
                        self.add_elem_to_id_lists(location, item_def)
                else:
                    raise ValueError(f"unexpected type: {type(elem)}")

            self.seed_log.entries.append(SeedLogEntry(node))

        self.copy_id_lists_to_settings()

    def assign_items_randomly(self):
        all_locations: list[LocationDef] = []

        # shuffle nodes, fetch locations and shuffle that list
        random.shuffle(self.nodes)
        for node in self.nodes:
            all_locations.extend(node.locations)
        assert len(all_locations) > 0
        random.shuffle(all_locations)

        # shuffle prog pool
        prog_pool = self.progression_item_pool[:]
        random.shuffle(prog_pool)

        # shuffle prio pool
        prio_pool = self.priority_item_pool[:]
        random.shuffle(prio_pool)

        # shuffle normal pool
        misc_pool = self.normal_item_pool[:]
        random.shuffle(misc_pool)

        item_pool = prog_pool + prio_pool + misc_pool
        random.shuffle(item_pool)

        self.init_id_lists()

        def do_assign(loc: LocationDef, size: int = 1, is_pre_assign: bool = False):
            while len(loc.items) < size:
                if len(item_pool) > 0:
                    picked_item = random.choice(item_pool)

                    if is_pre_assign and picked_item.kind != ItemKind.Tear:
                        continue

                    if not loc.allow_assign(self.settings, picked_item):
                        continue

                    item_pool.remove(picked_item)
                else:
                    # avoids having more than one major item per shop
                    picked_item = random.choice(misc_pool)

                loc.items.append(picked_item)
                self.add_elem_to_id_lists(loc, picked_item)

        def do_specialized_assign(item_defs: list[ItemDef], locations: list[LocationDef]):
            while len(item_defs) > 0:
                # choose randomly a location and a dungeon item (key, boss key, tear of light)
                loc = random.choice(locations)
                picked_item = random.choice(item_defs)
                loc.items.append(picked_item)

                # remove both from the local lists
                locations.remove(loc)
                item_defs.remove(picked_item)

                # remove both from the global lists
                all_locations.remove(loc)
                item_pool.remove(picked_item)

        # assign tears first if shuffled by section
        if self.settings.shuffle_dgn.tear_sanity == "section":
            for dgn_def in self.dgn_tos_defs:
                if dgn_def.tos_section == 6:
                    continue

                dgn_def.fill_locations(all_locations, check_tos_section=True)
                do_specialized_assign(dgn_def.tears, dgn_def.locations)

        attr_map = {
            "keysanity": "keys",
            "bksanity": "boss_keys",
            "tear_sanity": "tears",
        }

        # for each type
        for attr_settings, attr_def in attr_map.items():
            # if the type's setting is set to "dungeon"
            if getattr(self.settings.shuffle_dgn, attr_settings) == "dungeon":
                # create location and item maps for every dungeons
                locs_map: dict[int, list[LocationDef]] = {}
                items_map: dict[int, list[ItemDef]] = {}

                for i, dgn_def in self.dgn_def_map.items():
                    if i not in locs_map:
                        locs_map[i] = []

                    if i not in items_map:
                        items_map[i] = []

                    dgn_def.fill_locations(all_locations)
                    locs_map[i].extend(dgn_def.locations)
                    items_map[i].extend(getattr(dgn_def, attr_def))

                # then assign the items to the locations
                for i, dgn_def in self.dgn_def_map.items():
                    do_specialized_assign(items_map[i], locs_map[i])

        for loc in all_locations:
            size = self.settings.shuffle.shopsanity if "Shop Keeper" in loc.name else 1
            set_to_nothing = False

            # with "remove" mode we put nothing in chests and skip to the next location
            if loc.infos.settings.keysanity and self.settings.shuffle_dgn.keysanity == "removed":
                set_to_nothing = True
            elif loc.infos.settings.bkeysanity and self.settings.shuffle_dgn.bksanity == "removed":
                set_to_nothing = True
            elif loc.infos.settings.tearsanity and self.settings.shuffle_dgn.tear_sanity == "removed":
                set_to_nothing = True

            if set_to_nothing:
                loc.items.append(itemdef_nothing)
            else:
                do_assign(loc, size=size)

        self.copy_id_lists_to_settings()

        assert len(item_pool) == 0
        self.nodes.sort(key=lambda entry: entry.name)

    def get_offset(self, data: bytes, magic: bytes):
        try:
            return data.index(magic)
        except ValueError:
            return None

    def patch_rom(self):
        languages = [
            "English",
            "French",
            "German",
            "Italian",
            "Spanish",
        ]

        # patch the files
        for i, node in enumerate(self.nodes):
            lzss_path = self.extracted_dir / node.lzss
            _, archive, zmb_data, zmb_filename = self.get_zmb(lzss_path)

            do_save_narc = False
            for location in node.locations:
                assert location.infos is not None
                assert node.scene_name == location.infos.scene
                assert node.room_index == location.infos.room_index

                if location.infos.is_passenger_pick_up or location.infos.is_passenger_at_dest:
                    # passengers are exported into the shared settings binary, set by `assign_items_randomly`
                    continue

                if location.infos.is_cargo_pick_up:
                    # cargos are exported into the shared settings binary, set by `assign_items_randomly`
                    # cargo destination are set from the bmg though
                    continue

                if location.infos.is_bmg:
                    for lang in languages:
                        bmg_path = self.extracted_dir / "files" / lang / "Message" / location.infos.bmg
                        assert bmg_path.exists()

                        bmg_data = bmg_path.read_bytes()
                        bmg_data_array = bytearray(bmg_data)

                        for raw_offset in getattr(location.infos.bmg_offsets, lang.lower()):
                            offset = int(raw_offset, base=16)
                            assert bmg_data[offset + 0x00] == 0x03  # FLW1 "event" instruction
                            assert bmg_data[offset + 0x01] == 0x09  # function callback index

                            # function callback parameters
                            bmg_data_array[offset + 0x04] = location.items[0].id.value

                        bmg_path.write_bytes(bytes(bmg_data_array))
                else:
                    # probably completely useless? whatever
                    if location.infos.settings.passengers or location.infos.settings.cargo:
                        continue

                    id, x, y = location.infos.id_hash.split("_")

                    length = 1 if location.infos.is_mapobj else 2
                    x_bytes = int(x, base=16).to_bytes(length, byteorder="little")
                    y_bytes = int(y, base=16).to_bytes(length, byteorder="little")

                    hash = id[::-1].encode() + x_bytes + y_bytes
                    offset = self.get_offset(zmb_data, hash)
                    assert offset is not None

                    if location.infos.is_actor:
                        entry = ActorEntry.from_bytes(zmb_data[offset : offset + ActorEntry.entry_size])
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
                        elif (
                            (self.settings.shuffle.rupeesanity and entry.id == "RUPE")
                            or (self.settings.shuffle_dgn.is_bksanity_enabled() and entry.id in ["KEYB", "KEYT"])
                            or (self.settings.shuffle_dgn.is_keysanity_enabled() and entry.id == "MKUR")
                        ):
                            # for rupees, boss keys and spinnit, param 0 and 1 are used so we use 3 since it seems unused
                            entry.params[3] = location.items[0].id.value
                        else:
                            entry.params[0] = location.items[0].id.value

                        zmb_data = self.update_zmb(entry, zmb_data)
                    elif location.infos.is_mapobj:
                        entry = MapObjectEntry.from_bytes(zmb_data[offset : offset + MapObjectEntry.entry_size])
                        do_save_narc = True

                        # ignore glyphs if it's set to vanilla
                        if self.settings.shuffle.glyphs_and_sources == "vanilla" and entry.id == "GELG":
                            continue

                        # we could just use index 0 for stamp stations but better be safe
                        if self.settings.shuffle.stamps and entry.id == "SPTB":
                            entry.params[3] = location.items[0].id.value
                        else:
                            entry.params[0] = location.items[0].id.value

                        zmb_data = self.update_zmb(entry, zmb_data)

            if do_save_narc:
                archive.setFileByName(zmb_filename, zmb_data)
                LZSS.compressToFile(archive.save(), lzss_path)

            print(f"({(i / (len(self.nodes) - 1)) * 100:.2f}%) Processed", node.name)

        # create/update rando.bmg
        for lang in languages:
            self.generate_bmg(lang)
        print("Created rando.bmg!")

    def create_log(self):
        spoiler_log = SeedLog(Path(f"output/spoiler_{self.settings.seed}.yaml"), self.settings.to_str(), self.settings.seed)

        for node in self.nodes:
            spoiler_log.entries.append(SeedLogEntry(node))

        spoiler_log.export(self.settings)

    def generate_seed(self):
        initial_time = time.time()
        print(
            f"Randomizing with {len(self.progression_item_pool)} progression items, {len(self.priority_item_pool)} priority items and {len(self.normal_item_pool)} remaining items..."
        )

        # 2. assign the items
        if self.seed_log is None:
            prev_time = time.time()
            self.assign_items_randomly()
            print(f"Item assigned successfully in {time.time() - prev_time:.3f}s!")

        self.patch_rom()

        # 3. update the rom files
        if self.seed_log is None:
            # 4. generate spoiler log
            self.create_log()

        print(f"Seed {self.settings.seed} was generated successfully in {time.time() - initial_time:.3f}s!")

    def generate_bmg(self, lang: str):
        use_lang = lang

        # lang: [default, nothing, rabbits]
        prefix_map: dict[str, list[str]] = {
            "English": ["You got the ", "You got ", "You got a "],
            "French": [],  # TODO
            "German": [],  # TODO
            "Italian": [],  # TODO
            "Spanish": [],  # TODO
        }

        if len(prefix_map[use_lang]) == 0:
            use_lang = "English"

        msg_list = []

        RED = bmg.Message.Escape(255, b"\x00\x00\x01\x00")
        WHITE = bmg.Message.Escape(255, b"\x00\x00\x00\x00")
        INFO = b"\xce\x00\x00\x01"
        ITEM_MAX = max(list(item_id_to_name.keys())) + 1

        def get_kind(index: int):
            if index >= ItemId.ExtraItemId_RabbitGrass.value and index <= ItemId.ExtraItemId_RabbitSand.value:
                return ItemKind.Rabbit

            if index >= ItemId.ExtraItemId_TearLight_1.value and index <= ItemId.ExtraItemId_TearLight_5.value:
                return ItemKind.Tear

            if index >= ItemId.ExtraItemId_NormalKey_2.value and index <= ItemId.ExtraItemId_NormalKey_Desert.value:
                return ItemKind.DungeonKey

            if index >= ItemId.ExtraItemId_BossKey_3.value and index <= ItemId.ExtraItemId_BossKey_Desert.value:
                return ItemKind.DungeonKey

            return None

        for i in range(0, ITEM_MAX):
            kind = get_kind(i)
            prefix_index = 1 if i == ItemId.Nothing.value else 2 if kind is not None and kind == ItemKind.Rabbit else 0
            prefix = prefix_map[use_lang][prefix_index]
            suffix = get_item_name_suffix(self.settings, kind)

            # only there to determine the potential length of the string if it's on one line
            fake_str = prefix + item_id_to_name[i] + suffix + "!"

            if len(fake_str) > 26:
                msg_parts = [prefix + "\n", str(RED), item_id_to_name[i], suffix, str(WHITE), "!"]
            else:
                msg_parts = [prefix, str(RED), item_id_to_name[i], suffix, str(WHITE), "!"]

            msg = bmg.Message(INFO, msg_parts)
            msg_list.append(msg)

        for i in range(0, ITEM_MAX):
            msg_parts = [str(RED), item_id_to_name[i], str(WHITE)]
            msg = bmg.Message(INFO, msg_parts)
            msg_list.append(msg)

        # print("Train item message at index", len(msg_list), "for", lang)
        text_map = {
            "English": "You found a new item!\nGo to a station to find out!",
            "French": "Vous avez trouvé un objet!\nDécouvrez-le à une station!",
            "German": "",  # TODO
            "Italian": "",  # TODO
            "Spanish": "",  # TODO
        }
        msg = bmg.Message(INFO, [text_map[lang] if len(text_map[lang]) > 0 else text_map["English"]])
        msg_list.append(msg)

        bmg_file = bmg.BMG.fromMessages(msg_list, id=0x40)
        bmg_file.saveToFile(self.extracted_dir / "files" / lang / "Message" / "rando.bmg")

    def export_settings(self):
        settings_path = Path("src/settings/settings.bin")
        settings_path.write_bytes(self.settings.to_bin())


def main():
    rando = Randomizer(
        "eur",
        Path("rando/test/settings.yaml"),
        Path("rando/test/test_world.yaml"),
        Path("rando/data/location_table.yaml"),
        # plando mode
        # Path("output/seed.yaml"),
    )

    rando.generate_seed()
    rando.export_settings()


if __name__ == "__main__":
    main()
