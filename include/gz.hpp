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

enum SceneLoadState_ {
    SceneLoadState_Wait,
    SceneLoadState_Init,
    SceneLoadState_Post,
};

class GZ {
  private:
    /* 00 */ Input mButtons;
    /* 08 */ TouchControl* mpTouchControl;
    /* 0C */ ItemId mItemId;
    /* 10 */ u8 mTearsAmounts[5];
    /* 15 */ u8 mKeyAmounts[10];
    /* 1F */ u8 mSceneLoadState;
    /* 20 */

  public:
    GZ()
        : mpTouchControl(&data_02049b18.mUnk_06.mTouchControl), mItemId(ItemId_None),
          mSceneLoadState(SceneLoadState_Wait) {
        memset(this->mTearsAmounts, 0, sizeof(this->mTearsAmounts));
        memset(this->mKeyAmounts, 0, sizeof(this->mKeyAmounts));
    }
    ~GZ() {}

    void SetItemId(ItemId itemId) { this->mItemId = itemId; }

    u8 GetTearsAmount(u8 index) { return this->mTearsAmounts[index]; }

    u8 GetKeyAmount(u8 index) { return this->mKeyAmounts[index]; }

    u8 GetSceneLoadState() { return this->mSceneLoadState; }

    void SetSceneLoadState(u8 state) { this->mSceneLoadState = state; }

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

    // called as soon as a scene change is detected
    void OnScenePreInit();

    // called when the scene init process is completed
    void OnScenePostInit();

    void ApplyTearsAmounts();
    void ApplyKeyAmounts();
};

extern GZ gGZ;
