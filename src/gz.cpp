#include "gz.hpp"

#include <Cutscene/Cutscene.hpp>
#include <Save/SaveManager.hpp>
#include <System/Random.hpp>

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Winaccessible-base"
#include <TitleScreen/TitleScreen.hpp>
#pragma GCC diagnostic pop

#include <Unknown/UnkStruct_027e09a4.hpp>
#include <Unknown/UnkStruct_027e09b8.hpp>
#include <Unknown/UnkStruct_027e0ce0.hpp>
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
    AdventureFlag_MetStavenInTOSAfterFireGlyphCS, // prevents warp to a cutscene
    AdventureFlag_ForestTracksRestoredFromGlyphCS, // prevents warp to a cutscene
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

void GZ::OnScenePreInit() {}

void GZ::OnScenePostInit() {
    if (this->IsAdventureMode()) {
        this->ApplyTearsAmounts();
        this->ApplyKeyAmounts();
    }
}

void GZ::ApplyTearsAmounts() {
    if (data_027e0ce0 != NULL && data_027e0ce0->mUnk_2C != NULL && data_027e09a4 != NULL &&
        data_027e09a4->mpWarpUnk1 != NULL) {
        ItemManager* pItemMgr = data_027e0ce0->mUnk_2C;
        UnkStruct_SceneChange1* pCurrent = &data_027e09a4->mpWarpUnk1->mUnk_78;
        u8 amount = pItemMgr->mTearsAmount;

        if (pCurrent->mNextSceneIndex != SceneIndex_d_main) {
            return;
        }

        if ((pCurrent->mRoomIndex >= 0 && pCurrent->mRoomIndex <= 2) || pCurrent->mRoomIndex == 40) {
            // section 1
            amount = this->mTearsAmounts[0];
        } else if ((pCurrent->mRoomIndex >= 3 && pCurrent->mRoomIndex <= 6) || pCurrent->mRoomIndex == 41) {
            // section 2
            amount = this->mTearsAmounts[1];
        } else if ((pCurrent->mRoomIndex >= 7 && pCurrent->mRoomIndex <= 11) || pCurrent->mRoomIndex == 21 ||
                   pCurrent->mRoomIndex == 22 || pCurrent->mRoomIndex == 42) {
            // section 3
            amount = this->mTearsAmounts[2];
        } else if ((pCurrent->mRoomIndex >= 12 && pCurrent->mRoomIndex <= 16) || pCurrent->mRoomIndex == 43) {
            // section 4
            amount = this->mTearsAmounts[3];
        } else if ((pCurrent->mRoomIndex >= 17 && pCurrent->mRoomIndex <= 20) || pCurrent->mRoomIndex == 23 ||
                   pCurrent->mRoomIndex == 24 || pCurrent->mRoomIndex == 46) {
            // section 5
            amount = this->mTearsAmounts[4];
        }

        pItemMgr->mTearsAmount = amount;
    }
}

void GZ::ApplyKeyAmounts() {
    if (data_027e0ce0 != NULL && data_027e0ce0->mUnk_2C != NULL && data_027e09a4 != NULL &&
        data_027e09a4->mpWarpUnk1 != NULL) {
        ItemManager* pItemMgr = data_027e0ce0->mUnk_2C;
        UnkStruct_SceneChange1* pCurrent = &data_027e09a4->mpWarpUnk1->mUnk_78;
        u8 amount = pItemMgr->mKeyAmount;

        switch (pCurrent->mNextSceneIndex) {
            case SceneIndex_d_main:
                if (pCurrent->mRoomIndex >= 3 && pCurrent->mRoomIndex <= 6) {
                    // section 2
                    amount = this->mKeyAmounts[0];
                    break;
                }

                if (pCurrent->mRoomIndex >= 12 && pCurrent->mRoomIndex <= 16) {
                    // section 4
                    amount = this->mKeyAmounts[1];
                    break;
                }

                if ((pCurrent->mRoomIndex >= 17 && pCurrent->mRoomIndex <= 20) || pCurrent->mRoomIndex == 23 ||
                    pCurrent->mRoomIndex == 24) {
                    // section 5
                    amount = this->mKeyAmounts[2];
                    break;
                }

                if (pCurrent->mRoomIndex >= 29 && pCurrent->mRoomIndex <= 36) {
                    // section 6
                    amount = this->mKeyAmounts[3];
                    break;
                }

                return;
            case SceneIndex_d_tutorial:
                amount = this->mKeyAmounts[4];
                break;
            case SceneIndex_d_forest:
                amount = this->mKeyAmounts[5];
                break;
            case SceneIndex_d_snow26:
                amount = this->mKeyAmounts[6];
                break;
            case SceneIndex_d_water27:
                amount = this->mKeyAmounts[7];
                break;
            case SceneIndex_d_flame:
                amount = this->mKeyAmounts[8];
                break;
            case SceneIndex_d_sand:
                amount = this->mKeyAmounts[9];
                break;
            default:
                return;
        }

        pItemMgr->mKeyAmount = amount;
    }
}
