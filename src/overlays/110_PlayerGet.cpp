#include "036_MapA5.hpp"
#include "ItemIdMaps.hpp"
#include "gz.hpp"
#include "settings.hpp"

#include <MainGame/MiscAdvManager.hpp>
#include <Player/PlayerGet.hpp>
#include <Save/SaveManager.hpp>
#include <System/OverlayManager.hpp>
#include <Unknown/UICounterManager.hpp>
#include <Unknown/UnkStruct_027e09b8.hpp>

extern const UnkStruct_ov110_02185dc8 data_ov110_02185dc8[8];
extern "C" void func_ov024_020d6370(unk32*, ItemId);

static inline s16 GetItemFlag(ItemId itemId) {
    for (u32 i = 0; i < ARRAY_LEN(data_ov110_02185dc8); i++) {
        if (itemId == data_ov110_02185dc8[i].mItemId) {
            return data_ov110_02185dc8[i].mItemFlag;
        }
    }

    return ItemFlag_None;
}

void SetAdventureFlagsAtPickUp(u8 passenger) {
    // set flags that would normally set at the destination to simulate the train ride itself

    switch (passenger) {
        case Passenger_AnoukiNoko:
            SET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_GotNokoToIcySpring);
            break;
        case Passenger_AnoukiKofu:
            // there's no flag at the destination
            break;
        case Passenger_CastleTownMona:
            SET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_GotMonaToRabbitHaven);
            break;
        case Passenger_CastleTownAlfonzo:
            // has special handling in GZ::OnGameModeUpdate
            break;
        case Passenger_SnowRealmFerrus:
            SET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_GotFerrusToOutsetVillage);
            break;
        case Passenger_FireRealmFerrus:
            // there's no flag at the destination
            break;
        case Passenger_GoronVillageSnowGoron:
            // there's no flag at the destination
            break;
        case Passenger_GoronVillageCityGoron:
            SET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_GotChildGoronToCastleTown);
            break;
        case Passenger_MayscoreDovok:
            SET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_GotDovokToPapuzia);
            break;
        case Passenger_MayscoreMash:
            SET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_GotMashToPapuzia);
            SET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_WatchedOrcaMashCS);
            break;
        case Passenger_MayscoreMorris:
            SET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_GotMorrisToPapuzia);
            SET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_WatchedOrcaMorrisCS);
            break;
        case Passenger_MayscoreYamahiko:
            SET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_GotYamahikoToPapuzia);
            SET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_WatchedOrcaYamahikoCS);
            break;
        case Passenger_MayscoreWood:
            SET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_Unk_1B1);
            SET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_Unk_1C9);
            break;
        case Passenger_OutsetJoe:
            SET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_GotJoeToBeedlesAirShop);
            break;
        case Passenger_PirateHideoutWadatsumi:
            // there's no flag at the destination
            break;
        case Passenger_BridgeWorkersHomeKenzo:
            SET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_GotKenzoToTradingPost);
            break;
        case Passenger_TradingPostKenzo:
            SET_FLAG(data_027e09b8->mAdventureFlags, AdventureFlag_GotKenzoToAnouki);
            break;
        case Passenger_PapuziaVillageCarben:
            // there's no flag at the destination
            break;
        default:
            break;
    }
}

// overriding func_ov110_02184a40 to handle our custom items
extern "C" bool ItemGiveImpl(ItemManager* thisx, ItemId itemId) {
    RandoSave* pRandoSave = gGZ.GetCurrentSave();
    bool setAdvFlag = true;
    int rabbitType = -1;

    switch (itemId) {
        case ExtraItemId_TearLight_1:
        case ExtraItemId_TearLight_2:
        case ExtraItemId_TearLight_3:
        case ExtraItemId_TearLight_4:
        case ExtraItemId_TearLight_5:
            gGZ.IncrementTearsAmount(itemId - ExtraItemId_TearLight_1);
            gGZ.ApplyTearsAmounts();
            break;
        case ExtraItemId_NormalKey_2:
        case ExtraItemId_NormalKey_4:
        case ExtraItemId_NormalKey_5:
        case ExtraItemId_NormalKey_6:
        case ExtraItemId_NormalKey_Tunnel:
        case ExtraItemId_NormalKey_Wooded:
        case ExtraItemId_NormalKey_Blizzard:
        case ExtraItemId_NormalKey_Marine:
        case ExtraItemId_NormalKey_Mountain:
        case ExtraItemId_NormalKey_Desert:
            gGZ.IncrementKeyAmount(itemId - ExtraItemId_NormalKey_2);
            gGZ.ApplyKeyAmounts();
            break;
        case ExtraItemId_StampTowerOfSpirits:
        case ExtraItemId_StampCastleTown:
        case ExtraItemId_StampOutsetVillage:
        case ExtraItemId_StampMayscore:
        case ExtraItemId_StampWoodlandSanctuary:
        case ExtraItemId_StampAnoukiVillage:
        case ExtraItemId_StampSnowfallSanctuary:
        case ExtraItemId_StampPapuziaVillage:
        case ExtraItemId_StampIslandSanctuary:
        case ExtraItemId_StampGoronVillage:
        case ExtraItemId_StampValleySanctuary:
        case ExtraItemId_StampDuneSanctuary:
        case ExtraItemId_StampWoodedTemple:
        case ExtraItemId_StampBlizzardTemple:
        case ExtraItemId_StampMarineTemple:
        case ExtraItemId_StampMountainTemple:
        case ExtraItemId_StampDesertTemple:
        case ExtraItemId_StampPirateHideout:
        case ExtraItemId_StampTradingPost:
        case ExtraItemId_StampIcySpring: {
            u8 stampType = itemId - ExtraItemId_StampTowerOfSpirits;

            if (stampType > StampType_None && stampType < StampType_Max) {
                // we could just call gpMiscAdvManager->func_ov024_020d64b4 but we have more control if we set the
                // values directly
                gpMiscAdvManager->mObtainedStamps[stampType] = stampType;
                gpMiscAdvManager->mStampDates[stampType] =
                    (9 << 9) | (12 << 5) | 7; // 7/12/2009 aka the release date of the game Okayge
                gpMiscAdvManager->mStampPositions[stampType] = Vec2b(70, 72);
                gpMiscAdvManager->mStampsFlag |= (1 << stampType);
            }
            break;
        }
        case ExtraItemId_PassengerAnoukiNoko:
        case ExtraItemId_PassengerAnoukiKofu:
        case ExtraItemId_PassengerCastleTownMona:
        case ExtraItemId_PassengerCastleTownAlfonzo:
        case ExtraItemId_PassengerSnowRealmFerrus:
        case ExtraItemId_PassengerFireRealmFerrus:
        case ExtraItemId_PassengerGoronVillageSnowGoron:
        case ExtraItemId_PassengerGoronVillageCityGoron:
        case ExtraItemId_PassengerMayscoreDovok:
        case ExtraItemId_PassengerMayscoreMash:
        case ExtraItemId_PassengerMayscoreMorris:
        case ExtraItemId_PassengerMayscoreYamahiko:
        case ExtraItemId_PassengerMayscoreWood:
        case ExtraItemId_PassengerOutsetJoe:
        case ExtraItemId_PassengerPirateHideoutWadatsumi:
        case ExtraItemId_PassengerBridgeWorkersHomeKenzo:
        case ExtraItemId_PassengerTradingPostKenzo:
        case ExtraItemId_PassengerPapuziaVillageCarben:
            SetAdventureFlagsAtPickUp(itemId - ExtraItemId_PassengerAnoukiNoko);
            break;
        case ExtraItemId_CargoMegaIce:
        case ExtraItemId_CargoWood:
        case ExtraItemId_CargoIron:
        case ExtraItemId_CargoFish:
        case ExtraItemId_CargoCuccos:
        case ExtraItemId_CargoVessel:
        case ExtraItemId_CargoDarkOre:
            // nothing to do except setting the flag (which is done later)
            break;
        case ExtraItemId_RabbitGrass:
        case ExtraItemId_RabbitSnow:
        case ExtraItemId_RabbitWater:
        case ExtraItemId_RabbitMountain:
        case ExtraItemId_RabbitSand:
            rabbitType = itemId - ExtraItemId_RabbitGrass;

            if (gSettings.GetShuffleSettings()->rabbitpack) {
                // all in one
                int startingFlag = rabbitType * 10; // see RabbitFlag

                for (int i = startingFlag; i < (startingFlag + 10); i++) {
                    SET_FLAG(gSaveManager.GetUnk000()->unk_B78.rabbitFlags, i);
                }

                pRandoSave->rabbitIndices[rabbitType] = 10;
            } else {
                SET_FLAG(gSaveManager.GetUnk000()->unk_B78.rabbitFlags, pRandoSave->rabbitIndices[rabbitType]);
                pRandoSave->rabbitIndices[rabbitType]++;
            }

            // only set the item adventure flag on the last rabbit
            if (pRandoSave->rabbitIndices[rabbitType] < 10) {
                setAdvFlag = false;
            }
            break;
        case ItemId_NormalKey:
            thisx->GiveSmallKeys(1);
            break;
        case ItemId_GreenRupee:
            thisx->GiveRupees(1, true, true);
            break;
        case ItemId_BlueRupee:
            thisx->GiveRupees(5, true, true);
            break;
        case ItemId_RedRupee:
            thisx->GiveRupees(20, true, true);
            break;
        case ItemId_BigGreenRupee:
            thisx->GiveRupees(100, true, true);
            break;
        case ItemId_BigRedRupee:
            thisx->GiveRupees(200, true, true);
            break;
        case ItemId_BigGoldRupee:
            thisx->GiveRupees(300, true, true);
            break;
        case ItemId_HeartContainer:
            data_027e0ce0->func_ov000_0208a318(4, 1, 1);
            break;
        case ItemId_QuiverMedium:
        case ItemId_QuiverLarge:
            if (thisx->mQuiverCapacity < UpgradeCapacity_Tier3) {
                thisx->mQuiverCapacity++;
            }

            thisx->mArrowAmount = thisx->GetQuiverCapacity();
            break;
        case ItemId_BombBagMedium:
        case ItemId_BombBagLarge:
            if (thisx->mBombBagCapacity < UpgradeCapacity_Tier3) {
                thisx->mBombBagCapacity++;
            }

            thisx->mBombAmount = thisx->GetBombBagCapacity();
            break;
        case ItemId_RedPotion:
            thisx->GivePotion(PotionType_Red);
            break;
        case ItemId_PurplePotion:
            thisx->GivePotion(PotionType_Purple);
            break;
        case ItemId_YellowPotion:
            thisx->GivePotion(PotionType_Yellow);
            break;
        case ItemId_ArrowsRefill:
            thisx->GiveArrows(10);
            break;
        case ItemId_BombsRefill:
            thisx->GiveBombs(10);
            break;
        case ItemId_TearLight:
            if (thisx->mTearsAmount >= 3) {
                thisx->mTearsAmount = 3;
            } else {
                thisx->mTearsAmount++;
            }
            break;
        default:
            ItemFlag itemFlag = ItemManager::GetEquippedItemFlag(itemId);

            if (itemFlag != (ItemFlag)ItemFlag_None) {
                thisx->SetFlag(itemFlag);

                switch (itemFlag) {
                    case ItemFlag_Bombs:
                        thisx->mBombBagCapacity = UpgradeCapacity_Tier1;
                        thisx->mBombAmount = gBombBagCapacities[UpgradeCapacity_Tier1];
                        break;
                    case ItemFlag_Bow:
                        thisx->mQuiverCapacity = UpgradeCapacity_Tier1;
                        thisx->mArrowAmount = gQuiverCapacities[UpgradeCapacity_Tier1];
                        break;
                    default:
                        break;
                }

                if (thisx->mEquippedItem == (ItemFlag)ItemFlag_None) {
                    thisx->mEquippedItem = itemFlag;
                    gpUICounterManager->func_ov024_020cd458(thisx->mEquippedItem, false);
                }
            } else {
                itemFlag = GetItemFlag(itemId);

                if (itemFlag != (ItemFlag)ItemFlag_None) {
                    thisx->SetFlag(itemFlag);
                }
            }
            break;
    }

    if (setAdvFlag) {
        SET_FLAG(data_027e09b8->mAdventureFlags, gAdvFlagMap[itemId]);
    }

    if (itemId <= ItemId_EngineerUniform) {
        AdventureFlag advFlag = ItemManager::GetAdvFlagFromItem(itemId);

        if (advFlag != AdventureFlag_Nothing) {
            advFlag &= 0xFFFF;
            SET_FLAG(data_027e09b8->mAdventureFlags, advFlag);
        }
    }

    data_027e0ce0->mUnk_34->func_ov110_02185d3c(itemId);
    gpTreasureManager->func_ov000_020aa0ac(itemId);
    gpMiscAdvManager->GiveLetterOrPriceCard(itemId);

    if (!GET_FLAG(thisx->mFlags, ItemFlag_LokomoSword)) {
        u8 nAmount = 0;

        if (itemId >= ExtraItemId_TearLight_1 && itemId <= ExtraItemId_TearLight_5) {
            nAmount = gGZ.GetTearsAmount(itemId - ExtraItemId_TearLight_1);
        } else if (itemId == ItemId_TearLight) {
            nAmount = thisx->mTearsAmount;
        }

        if (nAmount == MAX_TEARS_OF_LIGHT && gOverlayManager.mLoadedOverlays[OverlaySlot_8] == OverlayIndex_Tower) {
            return true;
        }
    }

    return false;
}
