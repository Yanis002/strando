#pragma once

#include "gz.hpp"

#include <mem.h>
#include <types.h>

enum PassengerMode_ {
    PassengerMode_Remove,
    PassengerMode_Vanilla,
    PassengerMode_Abstract,
    PassengerMode_Anywhere,
};

enum CargoMode_ {
    CargoMode_Remove,
    CargoMode_Vanilla,
    CargoMode_Abstract,
    CargoMode_Anywhere,
};

enum GlyphsAndSourceMode_ {
    GlyphsAndSourceMode_Vanilla,
    GlyphsAndSourceMode_Anywhere,
    GlyphsAndSourceMode_ProgRealm,
    GlyphsAndSourceMode_Abstract,
};

enum ForestGlyphMode_ {
    ForestGlyphMode_Startwith,
    ForestGlyphMode_Anywhere,
};

enum StampMode_ {
    StampMode_Off,
    StampMode_Anywhere,
    StampMode_Shuffled,
};

struct ShuffleSettings {
    u8 shopsanity;
    bool rupeesanity;
    u8 passengers;
    u8 cargo;
    u8 glyphs_and_sources;
    u8 forest_glyph;
    bool duets;
    bool goron_range;
    bool stamps;
    bool rabbitsanity;
    bool rabbitpack;

    ShuffleSettings() { memset(this, 0, sizeof(ShuffleSettings)); }
};

enum KeysanityMode_ {
    KeysanityMode_Off,
    KeysanityMode_Dungeon,
    KeysanityMode_Anywhere,
    KeysanityMode_Removed,
};

enum BossKeysanityMode_ {
    BossKeysanityMode_Off,
    BossKeysanityMode_Dungeon,
    BossKeysanityMode_Anywhere,
    BossKeysanityMode_Removed,
};

enum TearSanityMode_ {
    TearSanityMode__Off,
    TearSanityMode__Section,
    TearSanityMode__Dungeon,
    TearSanityMode__Anywhere,
    TearSanityMode__Removed,
};

struct ShuffleDungeonSettings {
    u8 keysanity;
    u8 bksanity;
    u8 tear_sanity;
    bool keyring;
    bool bkeyring;
    bool tear_ring;
    bool tos_sections;
    bool tos_section_reward;

    ShuffleDungeonSettings() { memset(this, 0, sizeof(ShuffleDungeonSettings)); }
};

enum DarkRealmMode_ {
    DarkRealmMode_Open,
    DarkRealmMode_Dungeons,
    DarkRealmMode_Compass,
    DarkRealmMode_Restoration_songs,
};

struct GoalSettings {
    u8 unlock_dark_realm;
    u8 dungeon_amount;

    GoalSettings() { memset(this, 0, sizeof(GoalSettings)); }
};

class Settings {
  private:
    u32 mMagic;
    ShuffleSettings mShuffle;
    ShuffleDungeonSettings mShuffleDgn;
    GoalSettings mGoal;
    u8 mPassengerPickUpIds[Passenger_Max]; // passenger item ids
    u8 mPassengerAtDestIds[Passenger_Max]; // passenger item ids

  public:
    Settings();

    ShuffleSettings* GetShuffleSettings() { return &this->mShuffle; }
    ShuffleDungeonSettings* GetShuffleDungeonSettings() { return &this->mShuffleDgn; }
    GoalSettings* GetGoalSettings() { return &this->mGoal; }
    u8 GetPassengerPickUpItemId(u8 passenger) { return this->mPassengerPickUpIds[passenger]; }
    u8 GetPassengerAtDestItemId(u8 passenger) { return this->mPassengerAtDestIds[passenger]; }
};

extern Settings gSettings;
