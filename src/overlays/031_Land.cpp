#include "settings.hpp"

#include <Actor/ActorRupee.hpp>
#include <Unknown/UnkStruct_027e09b8.hpp>
#include <Unknown/UnkStruct_027e0ce0.hpp>
#include <Unknown/UnkStruct_027e0d34.hpp>
#include <nitro/math.h>

extern "C" unk32 func_02017158(unk32);

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

class CustomRupee : public ActorRupee {
  public:
    void ItemGive();
    void Custom_ov031_020e9068();
};

void CustomRupee::ItemGive() {
    // if rupeesanity is disabled or this is a spawned rupee, simply run the original function
    if (!gSettings.GetShuffleSettings()->rupeesanity || this->mUnk_5C.mParams[1] == 0) {
        this->func_ov031_020e951c();
        return;
    }

    // our custom version truly begins here, based on func_ov031_020e951c
    if (data_027e09b8->func_01ffd420() != 0) {
        return;
    }

    ItemId itemId = this->mUnk_5C.mParams[3];
    if (itemId != ItemId_None && !data_027e0d34->TryItemGive(itemId)) {
        return;
    }

    this->func_ov000_020984d0();
}

ARM void CustomRupee::Custom_ov031_020e9068() {
    // if rupeesanity is disabled or this is a spawned rupee, simply run the original function
    if (!gSettings.GetShuffleSettings()->rupeesanity || this->mUnk_5C.mParams[1] == 0) {
        this->func_ov031_020e9068();
        return;
    }

    this->func_ov031_020e9904(5);

    if (this->mUnk_5C.mUnk_24 >= 0 && this->mUnk_5C.mUnk_1A != 0) {
        this->func_ov000_02098a88(0, 1);
    }

    this->func_ov031_020e8fec();
}
