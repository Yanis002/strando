#include <nitro/math.h>
#include <Unknown/UnkStruct_027e0d34.hpp>
#include <Unknown/UnkStruct_027e0ce0.hpp>

ItemId GetProgressiveItemId(ItemId requestedItemId) {
    ItemId itemId = requestedItemId;

    if (data_027e0ce0 != NULL && data_027e0ce0->mUnk_2C != NULL) {
        ItemFlag* pFlags = data_027e0ce0->mUnk_2C->mUnk_08;

        switch (requestedItemId) {
            case ItemId_AncientShield:
                if (!GET_FLAG(pFlags, ItemFlag_Shield)) {
                    itemId = ItemId_NormalShield;
                }
                break;

            case ItemId_LokomoSword:
                if (!GET_FLAG(pFlags, ItemFlag_Sword)) {
                    itemId = ItemId_NormalSword;
                }
                break;

            case ItemId_BombBagMedium:
            case ItemId_BombBagLarge:
                if (!GET_FLAG(pFlags, ItemFlag_Bombs)) {
                    itemId = ItemId_BombBag;
                } else if (requestedItemId == ItemId_BombBagLarge) {
                    if (data_027e0ce0->mUnk_2C->mBombBagCapacity == UpgradeCapacity_Tier1) {
                        itemId = ItemId_BombBagMedium;
                    }
                }
                break;

            case ItemId_QuiverMedium:
            case ItemId_QuiverLarge:
            case ItemId_LightBow:
                if (!GET_FLAG(pFlags, ItemFlag_Bow)) {
                    itemId = ItemId_NormalBow;
                } else if (requestedItemId == ItemId_QuiverLarge) {
                    if (data_027e0ce0->mUnk_2C->mQuiverCapacity == UpgradeCapacity_Tier1) {
                        itemId = ItemId_QuiverMedium;
                    }
                }
                break;

            default:
                break;
        }
    }

    return itemId;
}

extern "C" bool CustomTryItemGive(UnkStruct_027e0d34_04* thisx, ItemId requestedItemId) {
    ItemId itemId;

    // handle progressive items
    itemId = GetProgressiveItemId(requestedItemId);

    return thisx->func_ov000_02093bc8(itemId);
}
