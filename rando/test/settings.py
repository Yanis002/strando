import struct
import yaml

from pathlib import Path


class LocationSettings:
    def __init__(self):
        self.rupeesanity = False
        self.glyphs_and_sources = False # this is not actually a bool but we just need to check if it's vanilla or not
        self.duets = False
        self.sword_training = False
        self.whip_race = str()
        self.goron_range = False
        self.pirate_hideout = str()
        self.take_em_all_on = str()
        self.stamps = False
        self.stamps_rewards = 0
        self.stamp_book = False
        self.passengers = False
        self.cargo = False
        self.rabbitsanity: str | None = None


class MinigamesSettings:
    def __init__(self):
        self.sword_training = False
        self.whip_race: list[str] = []
        self.goron_range = False
        self.pirate_hideout: list[str] = []
        self.take_em_all_on: list[str] = []

    def validate(self):
        if not isinstance(self.sword_training, bool):
            raise ValueError("minigame sword_training is not valid")

        if not isinstance(self.goron_range, bool):
            raise ValueError("minigame sword_training is not valid")

        difficulties = ["easy", "hard", "expert"]

        for difficulty in self.whip_race:
            if difficulty not in difficulties:
                raise ValueError("minigame whip_race is not valid")

        for difficulty in self.pirate_hideout:
            if difficulty not in difficulties:
                raise ValueError("minigame pirate_hideout is not valid")

        for difficulty in self.take_em_all_on:
            if difficulty not in difficulties:
                raise ValueError("minigame take_em_all_on is not valid")

    def to_yaml(self):
        return {
            "sword_training": self.sword_training,
            "whip_race": self.whip_race,
            "goron_range": self.goron_range,
            "pirate_hideout": self.pirate_hideout,
            "take_em_all_on": self.take_em_all_on,
        }


class ShuffleSettings:
    def __init__(self):
        self.shopsanity = -1
        self.rupeesanity = False
        self.passengers = str()
        self.cargo = str()
        self.glyphs_and_sources = str()
        self.forest_glyph = str()
        self.duets = False
        self.minigames = MinigamesSettings()

        self.stamps = False
        self.stamps_rewards: list[int] = []
        self.stamp_book = False

        self.rabbitsanity: list[str] = []
        self.rabbitpack = False

        self.passengers_mode = ["remove", "vanilla", "abstract", "anywhere"]
        self.passengers_mode_map = {mode: i for i, mode in enumerate(self.passengers_mode)}

        self.cargo_mode = ["remove", "vanilla", "abstract", "anywhere"]
        self.cargo_mode_map = {mode: i for i, mode in enumerate(self.cargo_mode)}

        self.glyphs_and_sources_mode = ["vanilla", "anywhere", "prog_realm", "prog_world"]
        self.glyphs_and_sources_mode_map = {mode: i for i, mode in enumerate(self.glyphs_and_sources_mode)}

        self.forest_glyph_mode = ["startwith", "anywhere"]
        self.forest_glyph_mode_map = {mode: i for i, mode in enumerate(self.forest_glyph_mode)}

    def is_rabbitsanity_enabled(self):
        return len(self.rabbitsanity) > 0 and "none" not in self.rabbitsanity

    def validate(self):
        if self.shopsanity < 0 or self.shopsanity > 5:
            raise ValueError("shopsanity can't be negative or more than 5")

        if not isinstance(self.rupeesanity, bool):
            raise ValueError("rupee_sanity must be true or false")

        if self.passengers not in self.passengers_mode:
            raise ValueError("passengers is not valid")

        if self.cargo not in self.cargo_mode:
            raise ValueError("cargo is not valid")

        if self.glyphs_and_sources not in self.glyphs_and_sources_mode:
            raise ValueError("glyphs_and_sources is not valid")

        if self.forest_glyph not in self.forest_glyph_mode:
            raise ValueError("forest_glyph is not valid")

        if not isinstance(self.duets, bool):
            raise ValueError("duets must be true or false")

        self.minigames.validate()

        if not isinstance(self.stamps, bool):
            raise ValueError("minigames is not valid")

        for value in self.stamps_rewards:
            if value not in [10, 15, 20]:
                raise ValueError("stamps_rewards is not valid")

        if not isinstance(self.stamp_book, bool):
            raise ValueError("stamp_book must be true or false")

        for value in self.rabbitsanity:
            if value not in ["grass", "snow", "water", "fire", "sand", "all"]:
                raise ValueError("rabbit_sanity is not valid")

        if not isinstance(self.rabbitpack, bool):
            raise ValueError("rabbit_pack must be true or false")

    @staticmethod
    def from_yaml(data: dict):
        settings = ShuffleSettings()

        if "shop_sanity" in data:
            settings.shopsanity = data["shop_sanity"]

        if "rupee_sanity" in data:
            settings.rupeesanity = data["rupee_sanity"]

        if "passengers" in data:
            settings.passengers = data["passengers"]

        if "cargo" in data:
            settings.cargo = data["cargo"]

        if "glyphs_and_sources" in data:
            settings.glyphs_and_sources = data["glyphs_and_sources"]

        if "forest_glyph" in data:
            settings.forest_glyph = data["forest_glyph"]

        if "duets" in data:
            settings.duets = data["duets"]

        if "minigames" in data:
            if "sword_training" in data["minigames"]:
                settings.minigames.sword_training = data["minigames"]["sword_training"]

            if "whip_race" in data["minigames"]:
                minigame: list[str] = data["minigames"]["whip_race"]
                settings.minigames.whip_race = minigame

            if "goron_range" in data["minigames"]:
                settings.minigames.goron_range = data["minigames"]["goron_range"]

            if "pirate_hideout" in data["minigames"]:
                minigame: list[str] = data["minigames"]["pirate_hideout"]
                settings.minigames.pirate_hideout = minigame

            if "take_em_all_on" in data["minigames"]:
                minigame: list[str] = data["minigames"]["take_em_all_on"]
                settings.minigames.take_em_all_on = minigame

        if "stamps" in data:
            settings.stamps = data["stamps"]

        if "stamps_rewards" in data:
            settings.stamps_rewards = data["stamps_rewards"]

        if "stamp_book" in data:
            settings.stamp_book = data["stamp_book"]

        if "rabbit_sanity" in data:
            settings.rabbitsanity = data["rabbit_sanity"]

        if "rabbit_pack" in data:
            settings.rabbitpack = data["rabbit_pack"]

        settings.validate()
        return settings

    def to_bin(self):
        rabbitsanity = 0
        rabbit_map = {
            "grass": 1 << 0,
            "snow": 1 << 1,
            "water": 1 << 2,
            "mountain": 1 << 3,
            "sand": 1 << 4,
            "all": 0x1F,
        }
        for value in self.rabbitsanity:
            rabbitsanity |= rabbit_map[value]

        return struct.pack(
            "<BBBBBBBBBBB",
            self.shopsanity,
            self.rupeesanity,
            self.passengers_mode_map[self.passengers],
            self.cargo_mode_map[self.cargo],
            self.glyphs_and_sources_mode_map[self.glyphs_and_sources],
            self.forest_glyph_mode_map[self.forest_glyph],
            self.duets,
            self.minigames.goron_range,
            self.stamps,
            rabbitsanity,
            self.rabbitpack,
        )

    def to_yaml(self):
        return {
            "shop_sanity": self.shopsanity,
            "rupee_sanity": self.rupeesanity,
            "passengers": self.passengers,
            "cargo": self.cargo,
            "glyphs_and_sources": self.glyphs_and_sources,
            "forest_glyph": self.forest_glyph,
            "duets": self.duets,
            "minigames": self.minigames.to_yaml(),
            "stamps": self.stamps,
            "stamps_rewards": self.stamps_rewards,
            "stamp_book": self.stamp_book,
            "rabbit_sanity": self.rabbitsanity,
            "rabbit_pack": self.rabbitpack,
        }


class ShuffleDungeonSettings:
    def __init__(self):
        self.keysanity = str()
        self.bksanity = str()
        self.tear_sanity = str()
        self.keyring = False
        self.bkeyring = False
        self.tear_ring = False
        self.tos_sections = False
        self.tos_section_reward = False

        self.keysanity_mode = ["off", "dungeon", "anywhere", "removed"]
        self.keysanity_mode_map = {mode: i for i, mode in enumerate(self.keysanity_mode)}

        self.bksanity_mode = ["off", "dungeon", "anywhere", "removed"]
        self.bksanity_mode_map = {mode: i for i, mode in enumerate(self.bksanity_mode)}

        self.tear_sanity_mode = ["off", "section", "dungeon", "anywhere", "removed"]
        self.tear_sanity_mode_map = {mode: i for i, mode in enumerate(self.tear_sanity_mode)}

    def validate(self):
        if self.keysanity not in self.keysanity_mode:
            raise ValueError("keysanity is not valid")

        if self.bksanity not in self.bksanity_mode:
            raise ValueError("bksanity is not valid")

        if self.tear_sanity not in self.tear_sanity_mode:
            raise ValueError("keysatear_sanitynity is not valid")

        if not isinstance(self.keyring, bool):
            raise ValueError("keyring must be true or false")

        if not isinstance(self.bkeyring, bool):
            raise ValueError("bkeyring must be true or false")

        if not isinstance(self.tear_ring, bool):
            raise ValueError("tear_ring must be true or false")

        if not isinstance(self.tos_sections, bool):
            raise ValueError("tos_sections must be true or false")

        if not isinstance(self.tos_section_reward, bool):
            raise ValueError("tos_section_reward must be true or false")

    @staticmethod
    def from_yaml(data: dict):
        settings = ShuffleDungeonSettings()

        if "key_sanity" in data:
            settings.keysanity = data["key_sanity"]

        if "bosskey_sanity" in data:
            settings.bksanity = data["bosskey_sanity"]

        if "tear_sanity" in data:
            settings.tear_sanity = data["tear_sanity"]

        if "key_ring" in data:
            settings.keyring = data["key_ring"]

        if "bosskey_ring" in data:
            settings.bkeyring = data["bosskey_ring"]

        if "tear_ring" in data:
            settings.tear_ring = data["tear_ring"]

        if "tos_sections" in data:
            settings.tos_sections = data["tos_sections"]

        if "tos_section_reward" in data:
            settings.tos_section_reward = data["tos_section_reward"]

        settings.validate()
        return settings

    def to_bin(self):
        return struct.pack(
            "<BBBBBBBB",
            self.keysanity_mode_map[self.keysanity],
            self.bksanity_mode_map[self.bksanity],
            self.tear_sanity_mode_map[self.tear_sanity],
            self.keyring,
            self.bkeyring,
            self.tear_ring,
            self.tos_sections,
            self.tos_section_reward,
        )

    def to_yaml(self):
        return {
            "key_sanity": self.keysanity,
            "bosskey_sanity": self.bksanity,
            "tear_sanity": self.tear_sanity,
            "key_ring": self.keyring,
            "bosskey_ring": self.bkeyring,
            "tear_ring": self.tear_ring,
            "tos_sections": self.tos_sections,
            "tos_section_reward": self.tos_section_reward,
        }


class GoalSettings:
    def __init__(self):
        self.unlock_dark_realm = str()
        self.unlock_dark_realm = str()
        self.dungeon_amount = -1

        self.unlock_dark_realm_mode = ["open", "dungeons", "compass", "restoration_songs"]
        self.unlock_dark_realm_mode_map = {mode: i for i, mode in enumerate(self.unlock_dark_realm_mode)}

    def validate(self):
        if self.unlock_dark_realm not in self.unlock_dark_realm_mode:
            raise ValueError("unlock_dark_realm is not valid")

        if self.unlock_dark_realm == "dungeons" and (self.dungeon_amount < 1 or self.dungeon_amount > 5):
            raise ValueError(f"dungeon_amount has an invalid value of {self.dungeon_amount}")

    @staticmethod
    def from_yaml(data: dict):
        settings = GoalSettings()

        if "unlock_dark_realm" in data:
            settings.unlock_dark_realm = data["unlock_dark_realm"]

        if "dungeon_amount" in data:
            settings.dungeon_amount = data["dungeon_amount"]

        settings.validate()
        return settings

    def to_bin(self):
        return struct.pack(
            "<BB",
            self.unlock_dark_realm_mode_map[self.unlock_dark_realm],
            self.dungeon_amount
        )

    def to_yaml(self):
        return {
            "unlock_dark_realm": self.unlock_dark_realm,
            "dungeon_amount": self.dungeon_amount,
        }


class Settings:
    def __init__(self, shuffle: ShuffleSettings, shuffle_dgn: ShuffleDungeonSettings, goal: GoalSettings):
        self.seed = "Unknown"
        self.shuffle = shuffle
        self.shuffle_dgn = shuffle_dgn
        self.goal = goal
        self.passenger_pick_ids: list[int] = []
        self.passenger_dest_ids: list[int] = []
        self.cargo_pick_ids: list[int] = []

    @staticmethod
    def from_yaml(yaml_path: Path):
        with yaml_path.open("r") as file:
            yaml_file = yaml.safe_load(file)

        return Settings(
            ShuffleSettings.from_yaml(yaml_file["settings"]["shuffle"]),
            ShuffleDungeonSettings.from_yaml(yaml_file["settings"]["shuffle_dungeon"]),
            GoalSettings.from_yaml(yaml_file["settings"]["goal"]),
        )

    def to_bin(self):
        passenger_pick_ids = b""
        assert len(self.passenger_pick_ids) == 18, f"len is {len(self.passenger_pick_ids)}" # passenger max
        for i in self.passenger_pick_ids:
            passenger_pick_ids += i.to_bytes(1, byteorder="little")

        passenger_dest_ids = b""
        assert len(self.passenger_dest_ids) == 18, f"len is {len(self.passenger_dest_ids)}" # passenger max
        for i in self.passenger_dest_ids:
            passenger_dest_ids += i.to_bytes(1, byteorder="little")

        cargo_pick_ids = b""
        assert len(self.cargo_pick_ids) == 7, f"len is {len(self.cargo_pick_ids)}" # cargo pick up max
        for i in self.cargo_pick_ids:
            cargo_pick_ids += i.to_bytes(1, byteorder="little")

        extras = passenger_pick_ids + passenger_dest_ids + cargo_pick_ids
        return struct.pack("<4s", b"RANDO") + self.shuffle.to_bin() + self.shuffle_dgn.to_bin() + self.goal.to_bin() + extras

    def to_yaml(self):
        return {
            "settings": {
                "seed": self.seed,
                "shuffle": self.shuffle.to_yaml(),
                "shuffle_dungeon": self.shuffle_dgn.to_yaml(),
                "goal": self.goal.to_yaml(),
            },
        }
