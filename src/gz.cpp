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

#include <Actor/ActorManager.hpp>
#include <MainGame/CargoManager.hpp>
#include <MapObject/MapObjectManager.hpp>
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

static AdventureFlag_Half sSourceFlags[] = {
    AdventureFlag_ObtainedForestSource, AdventureFlag_ObtainedSnowSource,   AdventureFlag_ObtainedOceanSource,
    AdventureFlag_ObtainedFireSource,   AdventureFlag_ObtainedDesertSource,
};

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
            ItemId itemId = gpSettings->GetPassengerAtDestItemId(i);

            if (itemId != ItemId_None && !this->CheckAdvFlag(itemId)) {
                // only give the item id if the related flag is unset
                this->TryAddItemIfNotInQueue(itemId);
                this->SetAdvFlag(itemId, false);

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
        RandoSave* pSave = this->GetCurrentSave();

        // special handling for alfonzo passenger
        // basically if the board flag is set
        // then give the item and unset said flag
        ItemId itemId = gpSettings->GetPassengerPickUpItemId(Passenger_CastleTownAlfonzo);
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
        } else {
            for (int i = 0; i < ARRAY_LEN(sSourceFlags); i++) {
                if (GET_FLAG(data_027e09b8->mAdventureFlags, sSourceFlags[i])) {
                    this->GetCurrentSave()->completedDungeons[i] = true;
                }
            }

            u8 tos_sections = gpSettings->GetShuffleDungeonSettings()->tos_sections;

            // set tower as complete if we opened the chest and we have access to the other sections
            if (this->IsTowerFinal()) {
                bool canReachToSSections = false;

                if (tos_sections == ToSSectionsMode_Progressive) {
                    int i;

                    static u8 sSectionIds[] = {
                        ExtraItemId_TowerSection_1, ExtraItemId_TowerSection_2, ExtraItemId_TowerSection_3,
                        ExtraItemId_TowerSection_4, ExtraItemId_TowerSection_5,
                    };

                    // consider sections reachable unless we have unset section flags
                    canReachToSSections = true;

                    for (i = 0; i < ARRAY_LEN(sSectionIds); i++) {
                        if (!this->CheckAdvFlag(sSectionIds[i])) {
                            canReachToSSections = false;
                            break;
                        }
                    }
                } else {
                    // consider sections reachable if section shuffle is disabled
                    // we can do that since we also look for the final chest to be opened
                    canReachToSSections = true;
                }

                MapObject* pTRLS = this->FindMapObject(MapObjectId_TRLS);
                if (pTRLS != NULL && pTRLS->mState == 8 && canReachToSSections) {
                    pSave->completedDungeons[5] = true;
                }
            }

            // make section 6 accessible if it's supposed to be opened
            if (data_027e09a4->mpWarpUnk1 != NULL &&
                data_027e09a4->mpWarpUnk1->mCurEntrance.sceneIndex == SceneIndex_d_main_s &&
                tos_sections == ToSSectionsMode_Open) {
                MapObject* pAltarStairs = this->FindMapObject(MapObjectId_STAL);

                if (pAltarStairs != NULL) {
                    // 0x01 will raise the stairs even if the eyes aren't activated
                    pAltarStairs->mState = 0x01;
                }
            }

            // handle dark realm requirements
            if (!this->CheckAdvFlag(ItemId_FinalTrack)) {
                GoalSettings* pGoal = gpSettings->GetGoalSettings();
                bool give = false;
                int value = 0;

                switch (pGoal->unlock_dark_realm) {
                    case DarkRealmMode_Open:
                        give = true;
                        break;
                    case DarkRealmMode_Dungeons:
                        value = 0;
                        for (int i = 0; i < ARRAY_LEN(pSave->completedDungeons); i++) {
                            if (!pGoal->is_tos_dungeon && i == 5) {
                                break;
                            }

                            if (pSave->completedDungeons[i]) {
                                value++;
                            }
                        }

                        if (value == pGoal->dungeon_amount) {
                            give = true;
                        }
                        break;
                    case DarkRealmMode_Compass:
                        if (this->CheckAdvFlag(ItemId_LightCompass)) {
                            give = true;
                        }
                        break;
                    case DarkRealmMode_RestorationSongs: {
                        static AdventureFlag_Half sRestorationSongFlags[] = {
                            RandoAdventureFlag_RestoredForestGlyph,      RandoAdventureFlag_RestoredSnowGlyph,
                            RandoAdventureFlag_RestoredOceanGlyph,       RandoAdventureFlag_RestoredFireGlyph,
                            RandoAdventureFlag_RestoredDesertOceanGlyph,
                        };

                        value = 0;
                        for (int i = 0; i < ARRAY_LEN(sRestorationSongFlags); i++) {
                            if (GET_FLAG(data_027e09b8->mAdventureFlags, sRestorationSongFlags[i])) {
                                value++;
                            }
                        }

                        if (value == ARRAY_LEN(sRestorationSongFlags)) {
                            give = true;
                        }
                        break;
                    }
                    default:
                        give = false;
                        break;
                }

                if (give) {
                    this->TryAddItemIfNotInQueue(ItemId_FinalTrack);
                }
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
        EntranceInfo* pNext = &data_027e09a4->mpWarpUnk1->mNextEntrance;

        // prevent reaching all forest realm stations (except castle town, outset and the tower)
        // if the forest glyph is shuffled and we don't have it yet
        // this just overrides the next scene and spawn indices
        if (this->IsOnTrain() && gpSettings->GetShuffleSettings()->forest_glyph == ForestGlyphMode_Anywhere &&
            !GET_FLAG(data_027e09b8->mAdventureFlags, RandoAdventureFlag_ForestGlyph)) {
            int spawn = -1;

            switch (pNext->sceneIndex) {
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
                pNext->sceneIndex = SceneIndex_t_area0;
                pNext->spawnIndex = spawn;
            }
        }

        // other sections are handled in `GZ::OnScenePostInit`
        // we only need to prevent loading the scene if we don't have section 1
        // otherwise we are blocked by default by the game, assuming the flag is unset
        if (this->IsOnLand() && gpSettings->GetShuffleDungeonSettings()->tos_sections == ToSSectionsMode_Progressive &&
            !GET_FLAG(data_027e09b8->mAdventureFlags, RandoAdventureFlag_TowerSection_1)) {
            if (pNext->sceneIndex == SceneIndex_d_main_w) {
                pNext->sceneIndex = SceneIndex_d_main_f;
                pNext->spawnIndex = 1;
            }
        }

        if (gpSettings->GetShuffleSettings()->passengers == PassengerMode_Remove) {
            this->SetAllPassengerFlags();
        }

        switch (gpSettings->GetShuffleSettings()->cargo) {
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
                    SceneIndex nextScene = data_027e09a4->mpWarpUnk1->mNextEntrance.sceneIndex;

                    for (int i = 0; i < CargoDelivery_Max; i++) {
                        if (this->CheckAdvFlag(ExtraItemId_CargoMegaIce + i) &&
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

        static AdventureFlag_Half sToSSectionFlags[] = {
            RandoAdventureFlag_TowerSection_2,
            RandoAdventureFlag_TowerSection_3,
            RandoAdventureFlag_TowerSection_4,
            RandoAdventureFlag_TowerSection_5,
            AdventureFlag_Nothing,
        };

        switch (gpSettings->GetShuffleDungeonSettings()->tos_sections) {
            case ToSSectionsMode_Progressive:
                // remove the source flag if we don't have the corresponding section flag
                // (except section 1, see `GZ::OnScenePreInit`)
                for (int i = 0; i < ARRAY_LEN(sSourceFlags); i++) {
                    if (GET_FLAG(data_027e09b8->mAdventureFlags, sSourceFlags[i]) &&
                        !GET_FLAG(data_027e09b8->mAdventureFlags, sToSSectionFlags[i])) {
                        UNSET_FLAG(data_027e09b8->mAdventureFlags, sSourceFlags[i]);
                    }
                }
                break;
            default:
                break;
        }

        // prevents zelda's text to show in ToS final room (giving the final track item)
        if (this->IsTowerFinal()) {
            // for some reasons editing the ctor with a hook crashes
            Actor* pTLKT = this->FindActor(ActorId_TLKT);

            if (pTLKT != NULL) {
                pTLKT->Kill();
            }
        }
    }
}

int GetTowerSectionFromRoom(int* pIndex) {
    u8 roomIndex = data_027e09a4->mpWarpUnk1->mCurEntrance.roomIndex;
    int index = -1;

    if ((roomIndex >= 0 && roomIndex <= 2) || roomIndex == 40) {
        // section 1
        return 0;
    } else if ((roomIndex >= 3 && roomIndex <= 6) || roomIndex == 41) {
        // section 2
        index = 0;
        return 1;
    } else if ((roomIndex >= 7 && roomIndex <= 11) || roomIndex == 21 || roomIndex == 22 || roomIndex == 42) {
        // section 3
        return 2;
    } else if ((roomIndex >= 12 && roomIndex <= 16) || roomIndex == 43) {
        // section 4
        index = 1;
        return 3;
    } else if ((roomIndex >= 17 && roomIndex <= 20) || roomIndex == 23 || roomIndex == 24 || roomIndex == 46) {
        // section 5
        index = 2;
        return 4;
    } else if (roomIndex >= 29 && roomIndex <= 36) {
        // section 6
        index = 3;
        return 5;
    }

    if (pIndex != NULL && index >= 0) {
        *pIndex = index;
    }

    return -1;
}

void GZ::ApplyTearsAmounts() {
    if (data_027e0ce0 != NULL && data_027e0ce0->mUnk_2C != NULL && data_027e09a4 != NULL &&
        data_027e09a4->mpWarpUnk1 != NULL) {
        ItemManager* pItemMgr = data_027e0ce0->mUnk_2C;
        EntranceInfo* pCurrent = &data_027e09a4->mpWarpUnk1->mCurEntrance;
        u8 amount = pItemMgr->GetTearsAmount();
        RandoSave* pSave = this->GetCurrentSave();
        int towerSection = GetTowerSectionFromRoom(NULL);

        if (pCurrent->sceneIndex != SceneIndex_d_main || towerSection < 0 || towerSection == 5) {
            return;
        }

        pItemMgr->SetTearsAmount(pSave->tearsAmounts[towerSection]);
    }
}

void GZ::ApplyKeyAmounts() {
    if (data_027e0ce0 != NULL && data_027e0ce0->mUnk_2C != NULL && data_027e09a4 != NULL &&
        data_027e09a4->mpWarpUnk1 != NULL) {
        ItemManager* pItemMgr = data_027e0ce0->mUnk_2C;
        EntranceInfo* pCurrent = &data_027e09a4->mpWarpUnk1->mCurEntrance;
        u8 amount = pItemMgr->GetKeyAmount();
        RandoSave* pSave = this->GetCurrentSave();
        int index = -1;
        int towerSection = GetTowerSectionFromRoom(&index);

        switch (pCurrent->sceneIndex) {
            case SceneIndex_d_main:
                if (index < 0 || towerSection < 0 || towerSection == 0 || towerSection == 1 || towerSection == 3) {
                    return;
                }

                amount = pSave->keyAmounts[index];
                break;
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

        pItemMgr->SetKeyAmount(amount);
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

void GZ::IncrementTearsAmount(u8 index) {
    RandoSave* pSave = this->GetCurrentSave();

    if (gpSettings->GetShuffleDungeonSettings()->tear_ring) {
        pSave->tearsAmounts[index] = MAX_TEARS_OF_LIGHT;
    } else {
        pSave->tearsAmounts[index]++;

        if (pSave->tearsAmounts[index] > MAX_TEARS_OF_LIGHT) {
            pSave->tearsAmounts[index] = MAX_TEARS_OF_LIGHT;
        }
    }
}

u8 GetMaxKeys(ItemId itemId) {
    switch (itemId) {
        case ExtraItemId_NormalKey_2:
        case ExtraItemId_NormalKey_5:
        case ExtraItemId_NormalKey_Wooded:
        case ExtraItemId_NormalKey_Marine:
        case ExtraItemId_NormalKey_Desert:
            return 2;
        case ExtraItemId_NormalKey_4:
        case ExtraItemId_NormalKey_6:
        case ExtraItemId_NormalKey_Mountain:
            return 3;
        case ExtraItemId_NormalKey_Tunnel:
        case ExtraItemId_NormalKey_Blizzard:
            return 1;
        default:
            break;
    }

    return 0;
}

ItemId GetKeyFromBossKey(ItemId itemId) {
    switch (itemId) {
        case ExtraItemId_BossKey_3:
            break;

        case ExtraItemId_BossKey_5:
            return ExtraItemId_NormalKey_5;

        case ExtraItemId_BossKey_Wooded:
            return ExtraItemId_NormalKey_Wooded;

        case ExtraItemId_BossKey_Blizzard:
            return ExtraItemId_NormalKey_Blizzard;

        case ExtraItemId_BossKey_Marine:
            return ExtraItemId_NormalKey_Marine;

        case ExtraItemId_BossKey_Mountain:
            return ExtraItemId_NormalKey_Mountain;

        case ExtraItemId_BossKey_Desert:
            return ExtraItemId_NormalKey_Desert;

        default:
            break;
    }

    return ItemId_None;
}

void GZ::IncrementKeyAmount(ItemId itemId) {
    RandoSave* pSave = this->GetCurrentSave();
    ShuffleDungeonSettings* pSettings = gpSettings->GetShuffleDungeonSettings();

    if (pSettings->bkeyring) {
        itemId = GetKeyFromBossKey(itemId);
    }

    if (itemId != ItemId_None) {
        u8 index = itemId - ExtraItemId_NormalKey_2;
        u8 max = GetMaxKeys(itemId);

        if ((pSettings->keyring || pSettings->bkeyring) && max > 0) {
            pSave->keyAmounts[index] = max;
        } else {
            pSave->keyAmounts[index]++;
        }

        if (pSave->keyAmounts[index] > MAX_KEYS) {
            pSave->keyAmounts[index] = MAX_KEYS;
        }
    }
}

Actor* GZ::FindActor(ActorId actorId) {
    Actor** ppTable = gpActorManager->mActorTable;
    Actor** ppTableEnd = gpActorManager->mActorTableEnd;

    for (Actor** ppEntry = ppTable; ppEntry < ppTableEnd; ppEntry++) {
        if (ppEntry != NULL) {
            Actor* pEntry = *ppEntry;

            if (pEntry != NULL && pEntry->GetActorId() == actorId) {
                return pEntry;
            }
        }
    }

    return NULL;
}

MapObject* GZ::FindMapObject(MapObjectId mapObjId) {
    MapObject** ppTable = gpMapObjManager->mMapObjTable;
    MapObject** ppTableEnd = gpMapObjManager->mMapObjTableEnd;

    for (MapObject** ppEntry = ppTable; ppEntry < ppTableEnd; ppEntry++) {
        if (ppEntry != NULL) {
            MapObject* pEntry = *ppEntry;

            if (pEntry != NULL && pEntry->GetMapObjectId() == mapObjId) {
                return pEntry;
            }
        }
    }

    return NULL;
}

bool GZ::IsTowerFinal() {
    if (data_027e09a4 != NULL && data_027e09a4->mpWarpUnk1 != NULL) {
        if (data_027e09a4->mpWarpUnk1->mCurEntrance.sceneIndex == SceneIndex_d_main &&
            data_027e09a4->mpWarpUnk1->mCurEntrance.roomIndex == 35) {
            return true;
        }
    }

    return false;
}

bool GZ::CheckAdvFlag(ItemId itemId) { return GET_FLAG(data_027e09b8->mAdventureFlags, gAdvFlagMap[itemId]); }

void GZ::SetAdvFlag(ItemId itemId, bool unset) {
    if (unset) {
        UNSET_FLAG(data_027e09b8->mAdventureFlags, gAdvFlagMap[itemId]);
    } else {
        SET_FLAG(data_027e09b8->mAdventureFlags, gAdvFlagMap[itemId]);
    }
}
