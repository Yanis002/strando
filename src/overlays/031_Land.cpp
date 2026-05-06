#include "036_MapA5.hpp"
#include "ItemIdMaps.hpp"
#include "gz.hpp"
#include "settings.hpp"

#include <Actor/ActorRupee.hpp>
#include <Unknown/UnkStruct_027e09b8.hpp>
#include <Unknown/UnkStruct_027e0ce0.hpp>
#include <Unknown/UnkStruct_027e0d34.hpp>
#include <nitro/math.h>

extern "C" unk32 func_02017158(unk32);

bool IsGlyphOrSource(ItemId itemId) {
    if (itemId >= ItemId_ForestGlyph && itemId <= ItemId_FireGlyph) {
        return true;
    }

    if (itemId >= ExtraItemId_ForestSource && itemId <= ExtraItemId_SandSource) {
        return true;
    }

    return false;
}

ItemId GetProgressiveRealmGlyphOrSource(ItemId requestedItemId) {
    ItemId itemId = requestedItemId;
    AdventureFlag* pFlags = data_027e09b8->mAdventureFlags;

    switch (requestedItemId) {
        case ItemId_ForestGlyph:
        case ExtraItemId_ForestSource:
            if (GET_FLAG(pFlags, RandoAdventureFlag_ForestGlyph)) {
                itemId = ExtraItemId_ForestSource;
            } else {
                itemId = ItemId_ForestGlyph;
            }
            break;

        case ItemId_SnowGlyph:
        case ExtraItemId_SnowSource:
            if (GET_FLAG(pFlags, RandoAdventureFlag_SnowGlyph)) {
                itemId = ExtraItemId_SnowSource;
            } else {
                itemId = ItemId_SnowGlyph;
            }
            break;

        case ItemId_OceanGlyph:
        case ExtraItemId_OceanSource:
            if (GET_FLAG(pFlags, RandoAdventureFlag_OceanGlyph)) {
                itemId = ExtraItemId_OceanSource;
            } else {
                itemId = ItemId_OceanGlyph;
            }
            break;

        case ItemId_FireGlyph:
        case ExtraItemId_FireSource:
            if (GET_FLAG(pFlags, RandoAdventureFlag_FireGlyph)) {
                itemId = ExtraItemId_FireSource;
            } else {
                itemId = ItemId_FireGlyph;
            }
            break;
        default:
            break;
    }

    return itemId;
}

ItemId GetProgressiveWorldGlyphOrSource(ItemId requestedItemId) {
    ItemId itemId = requestedItemId;
    AdventureFlag* pFlags = data_027e09b8->mAdventureFlags;

    switch (requestedItemId) {
        case ItemId_ForestGlyph:
        case ItemId_SnowGlyph:
        case ItemId_OceanGlyph:
        case ItemId_FireGlyph:
        case ExtraItemId_ForestSource:
        case ExtraItemId_SnowSource:
        case ExtraItemId_OceanSource:
        case ExtraItemId_FireSource:
        case ExtraItemId_SandSource:
            if (!GET_FLAG(pFlags, RandoAdventureFlag_ForestGlyph)) {
                itemId = ItemId_ForestGlyph;
            } else if (!GET_FLAG(pFlags, RandoAdventureFlag_ForestSource)) {
                itemId = ExtraItemId_ForestSource;
            } else if (!GET_FLAG(pFlags, RandoAdventureFlag_SnowGlyph)) {
                itemId = ItemId_SnowGlyph;
            } else if (!GET_FLAG(pFlags, RandoAdventureFlag_SnowSource)) {
                itemId = ExtraItemId_SnowSource;
            } else if (!GET_FLAG(pFlags, RandoAdventureFlag_OceanGlyph)) {
                itemId = ItemId_OceanGlyph;
            } else if (!GET_FLAG(pFlags, RandoAdventureFlag_OceanSource)) {
                itemId = ExtraItemId_OceanSource;
            } else if (!GET_FLAG(pFlags, RandoAdventureFlag_FireGlyph)) {
                itemId = ItemId_FireGlyph;
            } else if (!GET_FLAG(pFlags, RandoAdventureFlag_FireSource)) {
                itemId = ExtraItemId_FireSource;
            } else {
                itemId = ExtraItemId_SandSource;
            }
            break;
        default:
            break;
    }

    return itemId;
}

ItemId GetProgressiveItemId(ItemId requestedItemId) {
    ItemId itemId = requestedItemId;

    if (IsGlyphOrSource(requestedItemId)) {
        switch (gSettings.GetShuffleSettings()->glyphs_and_sources) {
            case GlyphsAndSourceMode_ProgRealm:
                itemId = GetProgressiveRealmGlyphOrSource(requestedItemId);
                break;
            case GlyphsAndSourceMode_Abstract:
                itemId = GetProgressiveWorldGlyphOrSource(requestedItemId);
                break;
            default:
                break;
        }
    } else if (data_027e0ce0 != NULL && data_027e0ce0->mUnk_2C != NULL) {
        ItemFlag* pFlags = data_027e0ce0->mUnk_2C->mUnk_08;

        switch (requestedItemId) {
            // progressive shield
            case ItemId_NormalShield:
            case ItemId_AncientShield:
                if (GET_FLAG(pFlags, ItemFlag_Shield)) {
                    itemId = ItemId_AncientShield;
                } else {
                    itemId = ItemId_NormalShield;
                }
                break;

            // progressive sword
            case ItemId_NormalSword:
            case ItemId_LokomoSword:
                if (GET_FLAG(pFlags, ItemFlag_Sword)) {
                    itemId = ItemId_LokomoSword;
                } else {
                    itemId = ItemId_NormalSword;
                }
                break;

            // progressive bomb bag
            case ItemId_BombBag:
            case ItemId_BombBagMedium:
            case ItemId_BombBagLarge:
                if (!GET_FLAG(pFlags, ItemFlag_Bombs)) {
                    itemId = ItemId_BombBag;
                    break;
                }

                if (data_027e0ce0->mUnk_2C->mBombBagCapacity == UpgradeCapacity_Tier2) {
                    itemId = ItemId_BombBagLarge;
                } else if (data_027e0ce0->mUnk_2C->mBombBagCapacity == UpgradeCapacity_Tier1) {
                    itemId = ItemId_BombBagMedium;
                } else {
                    itemId = ItemId_BombBag;
                }
                break;

            // progressive quiver
            case ItemId_NormalBow:
            case ItemId_QuiverMedium:
            case ItemId_QuiverLarge:
                if (!GET_FLAG(pFlags, ItemFlag_Bow)) {
                    itemId = ItemId_NormalBow;
                    break;
                }

                if (data_027e0ce0->mUnk_2C->mQuiverCapacity == UpgradeCapacity_Tier2) {
                    itemId = ItemId_QuiverLarge;
                } else if (data_027e0ce0->mUnk_2C->mQuiverCapacity == UpgradeCapacity_Tier1) {
                    itemId = ItemId_QuiverMedium;
                } else {
                    itemId = ItemId_NormalBow;
                }
                break;

            case ItemId_LightBow:
                if (!GET_FLAG(pFlags, ItemFlag_Bow)) {
                    itemId = ItemId_NormalBow;
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
