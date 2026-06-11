#include "gz.hpp"
#include "036_MapA5.hpp"
#include "ItemIdMaps.hpp"
#include "settings.hpp"

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
#include <nitro/pad.h>
#include <nitro/reg.h>

extern "C" bool CustomTryItemGive(UnkStruct_027e0d34_04* thisx, ItemId requestedItemId);
extern "C" void func_ov000_02070af8(UnkStruct_027e09a4*);

GZ gGZ;
s32 gCardLockId = -3;

void GZ::Init() {
    gCardLockId = OS_GetLockID();

    {
        // read save data
        CardLock lock;
        lock.ReadSave(0xF5000, this->mRandoSave, sizeof(this->mRandoSave));
    }

    // reset if the data is unset, the first byte would be tears amount, this can't be 0xFF
    if (*(u8*)this->mRandoSave == 0xFF) {
        memset(this->mRandoSave, 0, sizeof(this->mRandoSave));
        this->mRandoSave[0].ClearItemQueue();
        this->mRandoSave[1].ClearItemQueue();
    }
}

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

        if (gSettings.GetShuffleSettings()->forest_glyph == ForestGlyphMode_Startwith && data_027e09b8 != NULL) {
            AdventureFlag* pFlags = data_027e09b8->mAdventureFlags;

            SET_FLAG(pFlags, AdventureFlag_ObtainedForestGlyph);
            SET_FLAG(pFlags, RandoAdventureFlag_ForestGlyph);
        }
    }
}

static inline TitleScreenManager* GetTitleScreenManager() { return (TitleScreenManager*)gpCurrentGameModeMgr; }

struct PassengerAtDestInfos {
    u8 sceneIndex;
    AdventureFlag_Half requiredFlag;
    AdventureFlag_Half destFlags[3];
};

static PassengerAtDestInfos sPassengerAtDestInfos[Passenger_Max] = {
    // Passenger_AnoukiNoko
    {
        SceneIndex_f_tetsuo,
        RandoAdventureFlag_PassengerAnoukiNoko,
        {
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
        },
    },
    // Passenger_AnoukiKofu
    {
        SceneIndex_f_flame5,
        RandoAdventureFlag_PassengerAnoukiKofu,
        {
            AdventureFlag_CompletedKofuSidequest,
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
        },
    },
    // Passenger_CastleTownMona
    {
        SceneIndex_f_rabbit,
        RandoAdventureFlag_PassengerCastleTownMona,
        {
            AdventureFlag_WatchedBunnioMonaCS,
            AdventureFlag_CompletedMonaSidequest,
            AdventureFlag_Nothing,
        },
    },
    // Passenger_CastleTownAlfonzo
    {
        SceneIndex_f_first,
        RandoAdventureFlag_PassengerCastleTownAlfonzo,
        {
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
        },
    },
    // Passenger_SnowRealmFerrus
    {
        SceneIndex_f_first,
        RandoAdventureFlag_PassengerSnowRealmFerrus,
        {
            AdventureFlag_CompletedFerrusSidequest1,
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
        },
    },
    // Passenger_FireRealmFerrus
    {
        SceneIndex_d_water27,
        RandoAdventureFlag_PassengerFireRealmFerrus,
        {
            AdventureFlag_CompletedFerrusSidequest2,
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
        },
    },
    // Passenger_GoronVillageSnowGoron
    {
        SceneIndex_f_snow,
        RandoAdventureFlag_PassengerGoronVillageSnowGoron,
        {
            AdventureFlag_CompletedGoronAdultSidequest,
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
        },
    },
    // Passenger_GoronVillageCityGoron
    {
        SceneIndex_f_htown,
        RandoAdventureFlag_PassengerGoronVillageCityGoron,
        {
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
        },
    },
    // Passenger_MayscoreDovok
    {
        SceneIndex_f_water,
        RandoAdventureFlag_PassengerMayscoreDovok,
        {
            AdventureFlag_WatchedOrcaDovokCS,
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
        },
    },
    // Passenger_MayscoreMash
    {
        SceneIndex_f_water,
        RandoAdventureFlag_PassengerMayscoreMash,
        {
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
        },
    },
    // Passenger_MayscoreMorris
    {
        SceneIndex_f_water,
        RandoAdventureFlag_PassengerMayscoreMorris,
        {
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
        },
    },
    // Passenger_MayscoreYamahiko
    {
        SceneIndex_f_water,
        RandoAdventureFlag_PassengerMayscoreYamahiko,
        {
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
        },
    },
    // Passenger_MayscoreWood
    {
        SceneIndex_f_water,
        RandoAdventureFlag_PassengerMayscoreWood,
        {
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
        },
    },
    // Passenger_OutsetJoe
    {
        SceneIndex_f_trnnpc,
        RandoAdventureFlag_PassengerOutsetJoe,
        {
            AdventureFlag_LeftBeedleAfterJoeSidequest,
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
        },
    },
    // Passenger_PirateHideoutWadatsumi
    {
        SceneIndex_f_water,
        RandoAdventureFlag_PassengerPirateHideoutWadatsumi,
        {
            AdventureFlag_WadatsumiMeetsOrca,
            AdventureFlag_WatchedOrcaWadatsumiCS,
            AdventureFlag_WatchedOrcaWadatsumiCS2,
        },
    },
    // Passenger_BridgeWorkersHomeKenzo
    {
        SceneIndex_f_bridge2,
        RandoAdventureFlag_PassengerBridgeWorkersHomeKenzo,
        {
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
        },
    },
    // Passenger_TradingPostKenzo
    {
        SceneIndex_f_snow,
        RandoAdventureFlag_PassengerTradingPostKenzo,
        {
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
            AdventureFlag_Nothing,
        },
    },
    // Passenger_PapuziaVillageCarben
    {
        SceneIndex_f_water2,
        RandoAdventureFlag_PassengerPapuziaVillageCarben,
        {
            AdventureFlag_WonCarbenPirateAmbush,
            AdventureFlag_CarbenEnterSanctuary,
            AdventureFlag_Nothing,
        },
    },
};

void GZ::SetAllPassengerFlags() {
    for (int i = 0; i < Passenger_Max; i++) {
        PassengerAtDestInfos* pEntry = &sPassengerAtDestInfos[i];

        for (int j = 0; j < ARRAY_LEN(pEntry->destFlags); j++) {
            if (pEntry->destFlags[j] != AdventureFlag_Nothing) {
                SET_FLAG(data_027e09b8->mAdventureFlags, pEntry->destFlags[j]);
            }
        }

        SetAdventureFlagsAtPickUp(i);
    }
}

void GZ::TryGiveItemFromPassengerDestInfos(SceneIndex destSceneIndex) {
    for (int i = 0; i < Passenger_Max; i++) {
        PassengerAtDestInfos* pEntry = &sPassengerAtDestInfos[i];

        // if the flag is set it means we got the item (the flag is set when the item is received)
        if (pEntry->sceneIndex == destSceneIndex && GET_FLAG(data_027e09b8->mAdventureFlags, pEntry->requiredFlag)) {
            ItemId itemId = gSettings.GetPassengerAtDestItemId(i);

            if (itemId != ItemId_None && !GET_FLAG(data_027e09b8->mAdventureFlags, gAdvFlagMap[itemId])) {
                // only give the item id if the related flag is unset
                this->TryAddItemIfNotInQueue(itemId);
                SET_FLAG(data_027e09b8->mAdventureFlags, gAdvFlagMap[itemId]);

                for (int j = 0; j < ARRAY_LEN(pEntry->destFlags); j++) {
                    if (pEntry->destFlags[j] != AdventureFlag_Nothing) {
                        SET_FLAG(data_027e09b8->mAdventureFlags, pEntry->destFlags[j]);
                    }
                }
            }
        }
    }
}

void GZ::OnGameModeUpdate() {
    if (this->IsTitleScreen()) {
        // faster title screen
        if (gpCurrentGameModeMgr == NULL) {
            return;
        }

        TitleScreen* pTitleScreen = (TitleScreen*)GetTitleScreenManager()->mpGameMode;

        if (pTitleScreen == NULL || pTitleScreen->mShowUI) {
            return;
        }

        pTitleScreen->func_ov025_020c4e54();
        data_ov000_020b5214.func_ov000_0206db44(0x0B);
        pTitleScreen->func_ov025_020c4ea0(TitleScreenState_ToFileSelect);
    } else if (this->IsAdventureMode()) {
        // special handling for alfonzo passenger
        // basically if the board flag is set
        // then give the item and unset said flag
        ItemId itemId = gSettings.GetPassengerPickUpItemId(Passenger_CastleTownAlfonzo);
        if (!this->IsItemInQueue(itemId) &&
            GET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_AlfonzoBoardsTrainToOutsetVillage)) {
            // unset previously set flag
            UNSET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_AlfonzoBoardsTrainToOutsetVillage);

            // otherwise zelda won't let us leave...
            UNSET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_TalkedToAlfonzoHyruleCastle);

            // set item id to give
            this->TryAddItemToQueue(itemId);

            // reload the area otherwise we end up leaving castle town
            func_ov000_02070af8(data_027e09a4);
        }

        // handle passenger destination item give for passengers we have
        this->TryGiveItemFromPassengerDestInfos(data_027e09a4->CurrentSceneIndex());

        this->ProcessItemQueue();
    }
}

void GZ::OnScenePreInit() {
    if (this->IsAdventureMode()) {
        if (gSettings.GetShuffleSettings()->passengers == PassengerMode_Remove) {
            this->SetAllPassengerFlags();
        }
    }
}

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
        RandoSave* pSave = this->GetCurrentSave();

        if (pCurrent->mSceneIndex != SceneIndex_d_main) {
            return;
        }

        if ((pCurrent->mRoomIndex >= 0 && pCurrent->mRoomIndex <= 2) || pCurrent->mRoomIndex == 40) {
            // section 1
            amount = pSave->tearsAmounts[0];
        } else if ((pCurrent->mRoomIndex >= 3 && pCurrent->mRoomIndex <= 6) || pCurrent->mRoomIndex == 41) {
            // section 2
            amount = pSave->tearsAmounts[1];
        } else if ((pCurrent->mRoomIndex >= 7 && pCurrent->mRoomIndex <= 11) || pCurrent->mRoomIndex == 21 ||
                   pCurrent->mRoomIndex == 22 || pCurrent->mRoomIndex == 42) {
            // section 3
            amount = pSave->tearsAmounts[2];
        } else if ((pCurrent->mRoomIndex >= 12 && pCurrent->mRoomIndex <= 16) || pCurrent->mRoomIndex == 43) {
            // section 4
            amount = pSave->tearsAmounts[3];
        } else if ((pCurrent->mRoomIndex >= 17 && pCurrent->mRoomIndex <= 20) || pCurrent->mRoomIndex == 23 ||
                   pCurrent->mRoomIndex == 24 || pCurrent->mRoomIndex == 46) {
            // section 5
            amount = pSave->tearsAmounts[4];
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
        RandoSave* pSave = this->GetCurrentSave();

        switch (pCurrent->mSceneIndex) {
            case SceneIndex_d_main:
                if (pCurrent->mRoomIndex >= 3 && pCurrent->mRoomIndex <= 6) {
                    // section 2
                    amount = pSave->keyAmounts[0];
                    break;
                }

                if (pCurrent->mRoomIndex >= 12 && pCurrent->mRoomIndex <= 16) {
                    // section 4
                    amount = pSave->keyAmounts[1];
                    break;
                }

                if ((pCurrent->mRoomIndex >= 17 && pCurrent->mRoomIndex <= 20) || pCurrent->mRoomIndex == 23 ||
                    pCurrent->mRoomIndex == 24) {
                    // section 5
                    amount = pSave->keyAmounts[2];
                    break;
                }

                if (pCurrent->mRoomIndex >= 29 && pCurrent->mRoomIndex <= 36) {
                    // section 6
                    amount = pSave->keyAmounts[3];
                    break;
                }

                return;
            case SceneIndex_d_tutorial:
                amount = pSave->keyAmounts[4];
                break;
            case SceneIndex_d_forest:
                amount = pSave->keyAmounts[5];
                break;
            case SceneIndex_d_snow26:
                amount = pSave->keyAmounts[6];
                break;
            case SceneIndex_d_water27:
                amount = pSave->keyAmounts[7];
                break;
            case SceneIndex_d_flame:
                amount = pSave->keyAmounts[8];
                break;
            case SceneIndex_d_sand:
                amount = pSave->keyAmounts[9];
                break;
            default:
                return;
        }

        pItemMgr->mKeyAmount = amount;
    }
}

RandoSave::RandoSave() {
    memset(this->tearsAmounts, 0, sizeof(this->tearsAmounts));
    memset(this->keyAmounts, 0, sizeof(this->keyAmounts));
    this->ClearItemQueue();
}

void RandoSave::ClearItemQueue() {
    for (int i = 0; i < ARRAY_LEN(this->itemQueue); i++) {
        this->itemQueue[i] = (u8)ItemId_None;
    }
}

RandoSave* GZ::GetCurrentSave() { return &this->mRandoSave[gSaveManager.mUnk_206]; }

void GZ::Save() {
    CardLock lock;

    // 0xF5000 is the offset inside the save data, it's unused space we can use
    lock.WriteSave(0xF5000, this->mRandoSave, sizeof(this->mRandoSave));
}

bool GZ::IsItemInQueue(ItemId itemId) {
    RandoSave* pSave = this->GetCurrentSave();

    for (int i = 0; i < ARRAY_LEN(pSave->itemQueue); i++) {
        if (pSave->itemQueue[i] == itemId) {
            return true;
        }
    }

    return false;
}

void GZ::TryAddItemToQueue(ItemId itemId) {
    // ignore if the item id is none
    if (itemId == ItemId_None) {
        return;
    }

    RandoSave* pSave = this->GetCurrentSave();
    if (this->mItemQueueIndex < ARRAY_LEN(pSave->itemQueue)) {
        pSave->itemQueue[this->mItemQueueIndex] = itemId;
        this->mItemQueueIndex++;
    }
}

void GZ::TryAddItemIfNotInQueue(ItemId itemId) {
    // ignore if the item is already present in the queue
    if (!this->IsItemInQueue(itemId)) {
        this->TryAddItemToQueue(itemId);
    }
}

void GZ::ProcessItemQueue() {
    // give item if:
    // - not during scene init process
    // - not in a cutscene
    // - land overlay loaded
    // - item id is set and less than max
    // - not in a blocking interaction (`data_027e09b8->mUnk_00->mUnk_FD0`)
    if (this->IsSceneInit() || this->IsStb() || !this->IsOnLand() ||
        data_027e09a4->CurrentCSIndex() != CutsceneIndex_None ||
        !(data_027e09b8->mUnk_00 != NULL && data_027e09b8->mUnk_00->mUnk_FD0 == 0)) {
        return;
    }

    RandoSave* pSave = this->GetCurrentSave();
    for (int i = 0; i < ARRAY_LEN(pSave->itemQueue); i++) {
        ItemId itemId = pSave->itemQueue[i];

        if (itemId != ItemId_None && itemId < ExtraItemId_Max) {
            CustomTryItemGive(data_027e0d34->mUnk_04, itemId);
            pSave->itemQueue[i] = (u8)ItemId_None;

            if (this->mItemQueueIndex > 0) {
                this->mItemQueueIndex--;
            }

            // we need to wait for the next game update before we can giving another item
            break;
        }
    }
}
