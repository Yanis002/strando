#pragma once

#include "mem.hpp"

#include <Item/Item.hpp>
#include <Player/TouchControl.hpp>
#include <Save/SaveManager.hpp>
#include <System/OverlayManager.hpp>
#include <Unknown/Common.hpp>
#include <Unknown/UnkStruct_02049b18.hpp>
#include <Unknown/UnkStruct_02049b74.hpp>
#include <Unknown/UnkStruct_0204a110.hpp>
#include <mem.h>
#include <nitro/card.h>
#include <nitro/os.h>
#include <nitro/pad.h>
#include <nitro/reg.h>

#define data_027fffa8 (*(u16*)0x027FFFA8)

class GameGZ;

typedef ItemId ExtraItemId;
enum ExtraItemId_ {
    ExtraItemId_TearLight_1 = ItemId_EngineerUniform + 1, // ToS Section 1
    ExtraItemId_TearLight_2, // ToS Section 2
    ExtraItemId_TearLight_3, // ToS Section 3
    ExtraItemId_TearLight_4, // ToS Section 4
    ExtraItemId_TearLight_5, // ToS Section 5

    ExtraItemId_NormalKey_2, // ToS Section 2
    ExtraItemId_NormalKey_4, // ToS Section 4
    ExtraItemId_NormalKey_5, // ToS Section 5
    ExtraItemId_NormalKey_6, // ToS Section 6
    ExtraItemId_NormalKey_Tunnel,
    ExtraItemId_NormalKey_Wooded,
    ExtraItemId_NormalKey_Blizzard,
    ExtraItemId_NormalKey_Marine,
    ExtraItemId_NormalKey_Mountain,
    ExtraItemId_NormalKey_Desert,

    ExtraItemId_ForestSource,
    ExtraItemId_SnowSource,
    ExtraItemId_OceanSource,
    ExtraItemId_FireSource,
    ExtraItemId_SandSource,

    ExtraItemId_StampTowerOfSpirits,
    ExtraItemId_StampCastleTown,
    ExtraItemId_StampOutsetVillage,
    ExtraItemId_StampMayscore,
    ExtraItemId_StampWoodlandSanctuary,
    ExtraItemId_StampAnoukiVillage,
    ExtraItemId_StampSnowfallSanctuary,
    ExtraItemId_StampPapuziaVillage,
    ExtraItemId_StampIslandSanctuary,
    ExtraItemId_StampGoronVillage,
    ExtraItemId_StampValleySanctuary,
    ExtraItemId_StampDuneSanctuary,
    ExtraItemId_StampWoodedTemple,
    ExtraItemId_StampBlizzardTemple,
    ExtraItemId_StampMarineTemple,
    ExtraItemId_StampMountainTemple,
    ExtraItemId_StampDesertTemple,
    ExtraItemId_StampPirateHideout,
    ExtraItemId_StampTradingPost,
    ExtraItemId_StampIcySpring,

    ExtraItemId_PassengerAnoukiNoko,
    ExtraItemId_PassengerAnoukiKofu,
    ExtraItemId_PassengerCastleTownMona,
    ExtraItemId_PassengerCastleTownAlfonzo,
    ExtraItemId_PassengerSnowRealmFerrus,
    ExtraItemId_PassengerFireRealmFerrus,
    ExtraItemId_PassengerGoronVillageSnowGoron,
    ExtraItemId_PassengerGoronVillageCityGoron,
    ExtraItemId_PassengerMayscoreDovok,
    ExtraItemId_PassengerMayscoreMash,
    ExtraItemId_PassengerMayscoreMorris,
    ExtraItemId_PassengerMayscoreYamahiko,
    ExtraItemId_PassengerMayscoreWood,
    ExtraItemId_PassengerOutsetJoe,
    ExtraItemId_PassengerPirateHideoutWadatsumi,
    ExtraItemId_PassengerBridgeWorkersHomeKenzo,
    ExtraItemId_PassengerTradingPostKenzo,
    ExtraItemId_PassengerPapuziaVillageCarben,

    ExtraItemId_Max,
};

enum SceneLoadState_ {
    SceneLoadState_Wait,
    SceneLoadState_Init,
    SceneLoadState_Post,
};

/*
passenger trips:
- anouki to icy Spring
- outset to Beedle
- castle town to rabbit Haven
- mayscore to papuzia
- trading post to anouki
- snow realm to outset (ferrus)
- fire realm to marine temple (ferrus)
- goron village to anouki
- anouki to goron village
- goron village to castle town
- pirate hideout to papuzia
*/

enum Passenger_ {
    Passenger_None = -1,
    Passenger_AnoukiNoko, // mega ice
    Passenger_AnoukiKofu, // goron village
    Passenger_CastleTownMona, // rabbit haven
    Passenger_CastleTownAlfonzo,
    Passenger_SnowRealmFerrus,
    Passenger_FireRealmFerrus,
    Passenger_GoronVillageSnowGoron,
    Passenger_GoronVillageCityGoron,
    Passenger_MayscoreDovok,
    Passenger_MayscoreMash, // no item at destination
    Passenger_MayscoreMorris, // no item at destination
    Passenger_MayscoreYamahiko, // no item at destination
    Passenger_MayscoreWood, // no item at destination
    Passenger_OutsetJoe,
    Passenger_PirateHideoutWadatsumi,
    Passenger_BridgeWorkersHomeKenzo, // no item at destination
    Passenger_TradingPostKenzo, // no item at destination
    Passenger_PapuziaVillageCarben,
    Passenger_Max,
};

extern s32 gCardLockId;

// automatic lock and unlock for convenience
struct CardLock {
    u16 id;

    CardLock() { CARD_LockBackup(gCardLockId); }

    ~CardLock() { CARD_UnlockBackup(gCardLockId); }

    void ReadSave(u32 offset, void* buf, u32 size) {
        CARD_ReadWriteBackupAsync(offset, buf, size, NULL, NULL, 1, 6, 1, 0);
    }

    void WriteSave(u32 offset, void* buf, u32 size) {
        CARD_ReadWriteBackupAsync((u32)buf, (void*)offset, size, NULL, NULL, 1, 7, 10, 2);
    }
};

// defines a randomizer save, it's just a savestate in the end (it doesn't even matter)
struct RandoSave {
    u8 tearsAmounts[5];
    u8 keyAmounts[10];

    RandoSave() {
        memset(this->tearsAmounts, 0, sizeof(this->tearsAmounts));
        memset(this->keyAmounts, 0, sizeof(this->keyAmounts));
    }
} __attribute__((aligned(4)));

class GZ {
  private:
    Input mButtons;
    TouchControl* mpTouchControl;
    ItemId mItemId;
    u8 mSceneLoadState;
    u8 pad[3];
    RandoSave mRandoSave[MAX_SAVE_SLOTS];

  public:
    GZ()
        : mpTouchControl(&data_02049b18.mUnk_06.mTouchControl), mItemId(ItemId_None),
          mSceneLoadState(SceneLoadState_Wait) {}
    ~GZ() {}

    void SetItemId(ItemId itemId) { this->mItemId = itemId; }

    u8 GetTearsAmount(u8 index) { return this->GetCurrentSave()->tearsAmounts[index]; }

    u8 GetKeyAmount(u8 index) { return this->GetCurrentSave()->keyAmounts[index]; }

    u8 GetSceneLoadState() { return this->mSceneLoadState; }

    void SetSceneLoadState(u8 state) { this->mSceneLoadState = state; }

    void IncrementTearsAmount(u8 index) {
        RandoSave* pSave = this->GetCurrentSave();
        pSave->tearsAmounts[index]++;

        if (pSave->tearsAmounts[index] > MAX_TEARS_OF_LIGHT) {
            pSave->tearsAmounts[index] = MAX_TEARS_OF_LIGHT;
        }
    }

    void IncrementKeyAmount(u8 index) {
        RandoSave* pSave = this->GetCurrentSave();
        pSave->keyAmounts[index]++;

        if (pSave->keyAmounts[index] > MAX_KEYS) {
            pSave->keyAmounts[index] = MAX_KEYS;
        }
    }

    Input* GetInput() { return &this->mButtons; }

    void UpdateInputs() {
        // the game has functions but it's better to do it manually to make sure
        // we have the right values when we execute stuff later
        u16 input = ((REG_KEYINPUT | data_027fffa8) ^ 0x2FFF) & 0x2FFF;
        this->mButtons.press = input & ~this->mButtons.cur;
        this->mButtons.release = ~input & this->mButtons.cur;
        this->mButtons.cur = input;
    }

    bool IsAdventureMode() { return gOverlayManager.mLoadedOverlays[OverlaySlot_4] == OverlayIndex_MainGame; }

    bool IsBattleMode() { return gOverlayManager.mLoadedOverlays[OverlaySlot_4] == OverlayIndex_BattleGame; }

    bool IsFileSelect() { return gOverlayManager.mLoadedOverlays[OverlaySlot_4] == OverlayIndex_MainSelect; }

    bool IsTitleScreen() { return gOverlayManager.mLoadedOverlays[OverlaySlot_4] == OverlayIndex_Title; }

    bool IsOnLand() { return gOverlayManager.mLoadedOverlays[OverlaySlot_6] == OverlayIndex_Land; }

    bool IsSceneInit() { return gOverlayManager.mLoadedOverlays[OverlaySlot_1] == OverlayIndex_SceneInit; }

    bool IsStb() { return gOverlayManager.mLoadedOverlays[OverlaySlot_9] == OverlayIndex_Stb; }

    // global init
    void Init();

    // global update
    void Update();

    // called on new game mode init
    void OnGameModeInit();

    // called on game mode update
    void OnGameModeUpdate();

    // called as soon as a scene change is detected
    void OnScenePreInit();

    // called when the scene init process is completed
    void OnScenePostInit();

    void ApplyTearsAmounts();
    void ApplyKeyAmounts();

    RandoSave* GetCurrentSave();
    void Save(); //! TODO: execute this when we want to save the game
};

extern GZ gGZ;
