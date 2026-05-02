#pragma once

#include "mem.hpp"

#include <Item/Item.hpp>
#include <Player/TouchControl.hpp>
#include <System/OverlayManager.hpp>
#include <Unknown/Common.hpp>
#include <Unknown/UnkStruct_02049b18.hpp>
#include <Unknown/UnkStruct_02049b74.hpp>
#include <Unknown/UnkStruct_0204a110.hpp>
#include <mem.h>
#include <nitro/button.h>
#include <regs.h>

#define data_027fffa8 (*(u16*)0x027FFFA8)

class GameGZ;

enum Dungeon_ {
    Dungeon_ToS_1,
    Dungeon_ToS_2,
    Dungeon_ToS_3,
    Dungeon_ToS_4,
    Dungeon_ToS_5,
    Dungeon_ToS_6,
    Dungeon_Tunnel,
    Dungeon_Wooded,
    Dungeon_Blizzard,
    Dungeon_Marine,
    Dungeon_Mountain,
    Dungeon_Desert,
};

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

    ExtraItemId_Max,
};

class GZ {
  private:
    Input mButtons;
    TouchControl* mpTouchControl;
    ItemId mItemId;
    u8 mTearsAmounts[5];
    u8 mKeyAmounts[10];

  public:
    GZ() : mpTouchControl(&data_02049b18.mUnk_06.mTouchControl), mItemId(ItemId_None) {}
    ~GZ() {}

    void SetItemId(ItemId itemId) { this->mItemId = itemId; }

    u8 GetTearsAmount(u8 index) { return this->mTearsAmounts[index]; }

    u8 GetKeyAmount(u8 index) { return this->mKeyAmounts[index]; }

    void IncrementTearsAmount(u8 index) {
        this->mTearsAmounts[index]++;

        if (this->mTearsAmounts[index] > MAX_TEARS_OF_LIGHT) {
            this->mTearsAmounts[index] = MAX_TEARS_OF_LIGHT;
        }
    }

    void IncrementKeyAmount(u8 index) {
        this->mKeyAmounts[index]++;

        if (this->mKeyAmounts[index] > MAX_KEYS) {
            this->mKeyAmounts[index] = MAX_KEYS;
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
};

extern GZ gGZ;
