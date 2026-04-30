#include "gz.hpp"

#include <Cutscene/Cutscene.hpp>
#include <Save/SaveManager.hpp>
#include <System/Random.hpp>
#include <TitleScreen/TitleScreen.hpp>
#include <Unknown/UnkStruct_027e09a4.hpp>
#include <Unknown/UnkStruct_027e09b8.hpp>
#include <Unknown/UnkStruct_027e0d34.hpp>
#include <Unknown/UnkStruct_ov000_020b5214.hpp>
#include <flags.h>
#include <nitro/button.h>
#include <regs.h>

extern "C" bool CustomTryItemGive(UnkStruct_027e0d34_04* thisx, ItemId requestedItemId);

GZ gGZ;

void GZ::Init() {}

void GZ::Update() { this->UpdateInputs(); }

static u32 sAdventureFlagsToSet[] = {
    AdventureFlag_ObtainedSpiritTrain,
    AdventureFlag_CompletedSwordTutorial,
    AdventureFlag_PlayedHyruleGuardGetLostText,
    AdventureFlag_HyruleGuardMovesAfterCole,
    AdventureFlag_WatchedHyruleGuardColeCS,

    //! TODO: for some reasons having this flag set triggers the AP
    // AdventureFlag_WatchedZeldasBedroomFirstCS,

    AdventureFlag_WatchedSpiritTowerSplitCS,
    AdventureFlag_MetAnjeanFirstTime,
    AdventureFlag_FleeFirstPhantomTOS,
    AdventureFlag_SpawnFirstPhantomTOS,
    AdventureFlag_RouteDrawTutorial,
    AdventureFlag_WatchedHyruleCastleSpiritZeldaCS,
    AdventureFlag_WatchedThroneRoomSpiritZeldaCS,
    AdventureFlag_BeatSnowRealmRocktite,
    AdventureFlag_WatchedWarpPhantomFirstTimeWarpingCS,
    AdventureFlag_TextPhantomInLava,
    AdventureFlag_TextTOSEntrance4F,
    AdventureFlag_WatchedIntroCS,
    AdventureFlag_WatchedFirstPhantomPossessionCS,
    AdventureFlag_WatchedForestTempleCompletedCS,
    AdventureFlag_TalkedToZeldaMayscoreFirstTime,
    AdventureFlag_TalkedToZeldaPhantomPossessionFirstTime,
    AdventureFlag_WhipMinigameTutorial,
    AdventureFlag_HyruleCastleZeldaControlsTutorial,
    AdventureFlag_WatchedZeldaSpiritThroneCS,
    AdventureFlag_WatchedEnterZeldasBedroomCS,
    AdventureFlag_SnowSongPracticeDone,
    AdventureFlag_SandSongPraticeDone,
    AdventureFlag_FerrusPassengerTutorial,
    AdventureFlag_TextRockNearRabbitland,
    AdventureFlag_CannonTutorial,
    AdventureFlag_WatchedOutsetTrainGarageCS,
    AdventureFlag_ZeldaTextTOS8F,
    AdventureFlag_ZeldaTextTOS13F,
    AdventureFlag_ZeldaTextTorchPhantomTOS9F,
    AdventureFlag_ZeldaTextKeyMastersTOS10F,
    AdventureFlag_FireSongPracticeDone,
    AdventureFlag_WatchedStavenPostBattleCS,
    AdventureFlag_WatchedMalladusOnTOSSummitCS,
    AdventureFlag_WatchedMountainTempleCompletedCS,
    AdventureFlag_SafeZoneTutorial,
    AdventureFlag_DefeatedRocktiteEastTunnelFireLand,
};

void GZ::OnGameModeInit() {
    if (this->IsAdventureMode()) {
        for (int i = 0; i < ARRAY_LEN(sAdventureFlagsToSet); i++) {
            u32 flag = sAdventureFlagsToSet[i];
            UnkStruct_027e09b8* pUnkStruct_027e09b8 = data_027e09b8;

            if (pUnkStruct_027e09b8 != NULL) {
                u32* pFlags = pUnkStruct_027e09b8->mAdventureFlags;

                if (!GET_FLAG(pFlags, flag)) {
                    SET_FLAG(pFlags, flag);
                }
            }
        }
    }
}

void GZ::OnGameModeUpdate() {
    if (this->IsTitleScreen()) {
        // faster title screen
        if (data_027e0994 == NULL) {
            return;
        }

        TitleScreen* pTitleScreen = data_027e0994->GetTitleScreen();

        if (pTitleScreen == NULL || pTitleScreen->mShowUI) {
            return;
        }

        pTitleScreen->func_ov025_020c4e54();
        data_ov000_020b5214.func_ov000_0206db44(0x0B);
        pTitleScreen->func_ov025_020c4ea0(TitleScreenState_ToFileSelect);
    } else if (this->IsAdventureMode()) {
        if (!this->IsSceneInit() && !this->IsStb() && this->IsOnLand()) {
            // give item after cutscene
            if (data_027e09a4->mCutsceneIndex != CutsceneIndex_None && this->mItemId != ItemId_None) {
                CustomTryItemGive(data_027e0d34->mUnk_04, this->mItemId);
                this->mItemId = ItemId_None;
            }
        }
    }
}
