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

#include <MainGame/CargoManager.hpp>
#include <Unknown/Common.hpp>
#include <Unknown/UnkStruct_027e09a4.hpp>
#include <Unknown/UnkStruct_027e09b8.hpp>
#include <Unknown/UnkStruct_027e0ce0.hpp>
#include <Unknown/UnkStruct_027e0d34.hpp>
#include <Unknown/UnkStruct_ov000_020b5214.hpp>
#include <flags.h>
#include <nitro/pad.h>
#include <nitro/reg.h>

extern "C" void func_ov000_02070af8(UnkStruct_027e09a4*);
extern TrainSpeedPreset data_ov026_02135fec[];

struct CargoInfos {
    /* 00 */ u16 timerMax;
    /* 02 */ s8 amountDecr;
    /* 03 */ s8 amountDamageDecr;
    /* 04 */ s16 amount;
    /* 06 */
};
extern CargoInfos sCargoInfos[];

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
        this->mRandoSave[0].Init();
        this->mRandoSave[1].Init();
    }
}

void GZ::Update() { this->UpdateInputs(); }

void GZ::OnGameModeInit() {}

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

        if (this->IsOnTrain()) {
            TrainSpeedPreset* pDefault = &data_ov026_02135fec[TrainPresetType_Default];

            // new default speed preset
            // changes:
            // - reverse speed x2
            // - slow and fast speeds x3
            // - related `unk_04` set to 256 (unsure what it is)
            // - `unk_24` set to 0xFFFF, this is what lets us change the state instantly (for some reasons)
            // - "emergency break" duration x2
            static TrainSpeedPreset sDefaultSpeedPreset = {
                .reverse = {.speed = -143 * 2, .unk_04 = 256},
                .stop = {.speed = 0, .unk_04 = 0},
                .slow = {.speed = 115 * 3, .unk_04 = 256},
                .fast = {.speed = 193 * 3, .unk_04 = 256},
                .unk_20 = 0,
                .unk_24 = 0xFFFF,
                .unk_28 = 0,
                .unk_2C = 50,
                .unk_30 = 143,
                .unk_34 = 5,
                .unk_38 = 30 * 2,
                .unk_3C = FLOAT_TO_FX32(225.0f),
            };

            if (pDefault->fast.speed != sDefaultSpeedPreset.fast.speed) {
                MI_CpuCopyFast(&sDefaultSpeedPreset, pDefault, sizeof(TrainSpeedPreset));
            }

            if (data_027e0478.train.mUnk_058 != NULL && data_027e0478.train.mUnk_058->mUnk_33C > 0) {
                // tchou tchouuuuuuuuuuuu !!!
                data_027e0478.train.mUnk_058->mUnk_338 = 0;
            }
        }
    }
}

static SceneIndex_Half sCargoTypeToSceneIndex[CargoDelivery_Max] = {
    SceneIndex_f_water, // CargoDelivery_PapuziaIce
    SceneIndex_f_flame5, // CargoDelivery_GoronVillageIce
    SceneIndex_f_htown, // CargoDelivery_CastleTownFish
    SceneIndex_f_sand, // CargoDelivery_LokomoCuccos
    SceneIndex_f_first, // CargoDelivery_OutsetCuccos
    SceneIndex_f_forest1, // CargoDelivery_MayscoreSteel
    SceneIndex_f_snow, // CargoDelivery_AnoukiVillageFence
    SceneIndex_f_snow2, // CargoDelivery_LokomoVessel
    SceneIndex_f_bridge2, // CargoDelivery_TradingPostDarkOre
};

void GZ::OnScenePreInit() {
    if (this->IsAdventureMode()) {
        UnkStruct_SceneChange1* pNext = &data_027e09a4->mpWarpUnk1->mUnk_8C;

        // prevent reaching all forest realm stations (except castle town, outset and the tower)
        // if the forest glyph is shuffled and we don't have it yet
        // this just overrides the next scene and spawn indices
        if (this->IsOnTrain() && gSettings.GetShuffleSettings()->forest_glyph == ForestGlyphMode_Anywhere &&
            !GET_FLAG(data_027e09b8->mAdventureFlags, RandoAdventureFlag_ForestGlyph)) {
            int spawn = -1;

            switch (pNext->mSceneIndex) {
                case SceneIndex_t_forest:
                    spawn = 5;
                    break;
                case SceneIndex_d_forest:
                    spawn = 4;
                    break;
                case SceneIndex_f_forest1:
                    spawn = 2;
                    break;
                case SceneIndex_f_forest2:
                    spawn = 3;
                    break;
                case SceneIndex_f_bridge2:
                    spawn = 7;
                    break;
                case SceneIndex_f_rabbit:
                    spawn = 8;
                    break;
                default:
                    break;
            }

            if (spawn != -1) {
                pNext->mSceneIndex = SceneIndex_t_area0;
                pNext->mSpawnIndex = spawn;
            }
        }

        // other sections are handled in `GZ::OnScenePostInit`
        // we only need to prevent loading the scene if we don't have section 1
        // otherwise we are blocked by default by the game, assuming the flag is unset
        if (this->IsOnLand() && gSettings.GetShuffleDungeonSettings()->tos_sections &&
            !GET_FLAG(data_027e09b8->mAdventureFlags, RandoAdventureFlag_TowerSection_1)) {
            if (pNext->mSceneIndex == SceneIndex_d_main_w) {
                pNext->mSceneIndex = SceneIndex_d_main_f;
                pNext->mSpawnIndex = 1;
            }
        }

        if (gSettings.GetShuffleSettings()->passengers == PassengerMode_Remove) {
            this->SetAllPassengerFlags();
        }

        switch (gSettings.GetShuffleSettings()->cargo) {
            case CargoMode_Remove:
                SET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_GiveMegaIceToKagoron);
                UNSET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_MegaIceToGoronVillageMainQuest);
                break;
            case CargoMode_Vanilla:
                break;
            case CargoMode_Abstract:
            case CargoMode_Anywhere:
                if (gpCargoManager->GetCargo()->IsTypeSet()) {
                    // reset when leaving the scene
                    gpCargoManager->Reset();
                } else if (data_027e09a4->mpWarpUnk1 != NULL) {
                    // set the cargo if we have the cargo item and the destination scene is about to load
                    SceneIndex nextScene = data_027e09a4->mpWarpUnk1->mUnk_8C.mSceneIndex;

                    for (int i = 0; i < CargoDelivery_Max; i++) {
                        if (GET_FLAG(data_027e09b8->mAdventureFlags, gAdvFlagMap[ExtraItemId_CargoMegaIce + i]) &&
                            sCargoTypeToSceneIndex[i] == nextScene) {
                            // I wanted to set to 9999 but the cargo counter don't like it :(
                            gpCargoManager->Init(i, 99);
                        }
                    }
                }
                break;
            default:
                break;
        }
    }
}

void GZ::OnScenePostInit() {
    if (this->IsAdventureMode()) {
        this->ApplyTearsAmounts();
        this->ApplyKeyAmounts();

        if (this->IsCourseExec()) {
            // remove cargo timers and damage stuff
            memset(sCargoInfos, 0, sizeof(CargoInfos) * CargoType_Max);
        }

        // remove the source flag if we don't have the corresponding section flag
        // (except section 1, see `GZ::OnScenePreInit`)
        if (gSettings.GetShuffleDungeonSettings()->tos_sections) {
            static AdventureFlag_Half sSourceFlags[] = {
                AdventureFlag_ObtainedForestSource,
                AdventureFlag_ObtainedSnowSource,
                AdventureFlag_ObtainedOceanSource,
                AdventureFlag_ObtainedFireSource,
            };

            static AdventureFlag_Half sToSSectionFlags[] = {
                RandoAdventureFlag_TowerSection_2,
                RandoAdventureFlag_TowerSection_3,
                RandoAdventureFlag_TowerSection_4,
                RandoAdventureFlag_TowerSection_5,
            };

            for (int i = 0; i < ARRAY_LEN(sSourceFlags); i++) {
                if (GET_FLAG(data_027e09b8->mAdventureFlags, sSourceFlags[i]) &&
                    !GET_FLAG(data_027e09b8->mAdventureFlags, sToSSectionFlags[i])) {
                    UNSET_FLAG(data_027e09b8->mAdventureFlags, sSourceFlags[i]);
                }
            }
        }
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

RandoSave::RandoSave() { this->Init(); }

void RandoSave::Init() {
    memset(this, 0, sizeof(RandoSave));
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

        // remove the item from the queue only on a successful item give
        // note: RandoTryItemGive can return true when on train without giving the item
        // but we already made sure we're on land so it's safe
        if (itemId != ItemId_None && itemId < ExtraItemId_Max && RandoTryItemGive(itemId)) {
            pSave->itemQueue[i] = (u8)ItemId_None;

            if (this->mItemQueueIndex > 0) {
                this->mItemQueueIndex--;
            }

            // we need to wait for the next game update before we can giving another item
            break;
        }
    }
}
