#include "036_MapA5.hpp"
#include "ItemIdMaps.hpp"
#include "gz.hpp"

#include <Player/PlayerGet.hpp>
#include <System/OverlayManager.hpp>
#include <Unknown/UnkStruct_020d8698.hpp>
#include <Unknown/UnkStruct_027e09b8.hpp>

extern const UnkStruct_ov110_02185dc8 data_ov110_02185dc8[8];
extern unk32* data_ov024_020d86b0;
extern "C" void func_ov024_020d6370(unk32*, ItemId);

static inline s16 GetItemFlag(ItemId itemId) {
    for (u32 i = 0; i < ARRAY_LEN(data_ov110_02185dc8); i++) {
        if (itemId == data_ov110_02185dc8[i].mItemId) {
            return data_ov110_02185dc8[i].mItemFlag;
        }
    }

    return ItemFlag_None;
}

// overriding func_ov110_02184a40 to handle our custom items
extern "C" bool ItemGiveImpl(ItemManager* thisx, ItemId itemId) {
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
        case ItemId_NormalKey:
            thisx->func_ov000_020a87c8(1);
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

            thisx->mArrowAmount = thisx->func_ov000_020a8728();
            break;
        case ItemId_BombBagMedium:
        case ItemId_BombBagLarge:
            if (thisx->mBombBagCapacity < UpgradeCapacity_Tier3) {
                thisx->mBombBagCapacity++;
            }

            thisx->mBombAmount = thisx->func_ov000_020a8748();
            break;
        case ItemId_RedPotion:
            thisx->func_ov000_020a888c(PotionType_Red);
            break;
        case ItemId_PurplePotion:
            thisx->func_ov000_020a888c(PotionType_Purple);
            break;
        case ItemId_YellowPotion:
            thisx->func_ov000_020a888c(PotionType_Yellow);
            break;
        case ItemId_ArrowsRefill:
            thisx->func_ov000_020a87ec(10);
            break;
        case ItemId_BombsRefill:
            thisx->func_ov000_020a8820(10);
            break;
        case ItemId_TearLight:
            if (thisx->mTearsAmount >= 3) {
                thisx->mTearsAmount = 3;
            } else {
                thisx->mTearsAmount++;
            }
            break;
        default:
            ItemFlag itemFlag = ItemManager::func_ov000_020a8984(itemId);

            if (itemFlag != (ItemFlag)ItemFlag_None) {
                thisx->func_ov000_020a863c(itemFlag);

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
                    data_ov024_020d8698->func_ov024_020cd458(thisx->mEquippedItem, 0);
                }
            } else {
                itemFlag = GetItemFlag(itemId);

                if (itemFlag != (ItemFlag)ItemFlag_None) {
                    thisx->func_ov000_020a863c(itemFlag);
                }
            }
            break;
    }

    SET_FLAG(data_027e09b8->mAdventureFlags, gAdvFlagMap[itemId]);

    if (itemId <= ItemId_EngineerUniform) {
        AdventureFlag advFlag = ItemManager::func_ov110_02185db4(itemId);

        if (advFlag != AdventureFlag_Nothing) {
            advFlag &= 0xFFFF;
            SET_FLAG(data_027e09b8->mAdventureFlags, advFlag);
        }
    }

    data_027e0ce0->mUnk_34->func_ov110_02185d3c(itemId);
    data_ov000_020b6510->func_ov000_020aa0ac(itemId);
    func_ov024_020d6370(data_ov024_020d86b0, itemId);

    if (!GET_FLAG(thisx->mUnk_08, ItemFlag_LokomoSword)) {
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
