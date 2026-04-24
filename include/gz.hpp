#pragma once

#include "mem.hpp"

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

struct GZState {
    bool isPaused; // pauses the game
    u32 requestedFrames; // how many frames to allow for frame advance
    bool doRNGUpdatesDuringPause; // allow the RNG seed to be updated in `ExecutePause`
    bool isRNGPaused; // stops the RNG seed from updating in the main loop (TODO: entirely stop RNG from updating?)

    GZState() { memset(this, 0, sizeof(GZState)); }
};

class GZ {
  private:
    Input mButtons;
    TouchControl* mpTouchControl;
    GZState mState;

  public:
    GZ() : mpTouchControl(&data_02049b18.mUnk_06.mTouchControl) {}
    ~GZ() {}

    Input* GetInput() { return &this->mButtons; }

    GZState* GetState() { return &this->mState; }

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
