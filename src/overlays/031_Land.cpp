#include "036_MapA5.hpp"
#include "ItemIdMaps.hpp"
#include "gz.hpp"
#include "settings.hpp"

#include <Actor/ActorRupee.hpp>
#include <MapObject/MapObject.hpp>
#include <Unknown/UnkStruct_027e09b8.hpp>
#include <Unknown/UnkStruct_027e0ce0.hpp>
#include <Unknown/UnkStruct_027e0d34.hpp>
#include <nitro/math.h>

extern "C" unk32 func_02017158(unk32);
extern "C" unk32 _ZN16MapObjectUnkSPTB19func_ov031_0210b6e4Ev(void*);
extern "C" bool _ZN16MapObjectUnkSPTB19func_ov031_0210b51cEv(void*);
extern "C" void func_ov000_02068194(UnkStruct_ov000_020b504c*, u32, int, Vec2s*);

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
        ItemFlag* pFlags = data_027e0ce0->mUnk_2C->mFlags;

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

#define TRAIN_GET_ITEM_MSG MSG(ExtraItemId_Max * 2)

extern "C" bool CustomTryItemGive(UnkStruct_027e0d34_04* thisx, ItemId requestedItemId) {
    return RandoTryItemGive(requestedItemId);
}

bool RandoTryItemGive(ItemId requestedItemId) {
    ItemId itemId;

    // handle progressive items
    itemId = GetProgressiveItemId(requestedItemId);

    if (!gGZ.IsOnLand()) {
        // if on not on land just add to the item queue
        gGZ.TryAddItemToQueue(itemId);

        // show text
        Vec2s local(135, 100);
        func_ov000_02068194(&data_ov000_020b504c, TRAIN_GET_ITEM_MSG, 0, &local);
        return true;
    }

    if (data_027e0d34 != NULL && data_027e0d34->mUnk_04 != NULL) {
        return data_027e0d34->mUnk_04->func_ov000_02093bc8(itemId);
    }

    return false;
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

    this->SetState(ActorRupeeState_5);

    if (this->mUnk_5C.mUnk_24 >= 0 && this->mUnk_5C.mUnk_1A != 0) {
        this->func_ov000_02098a88(0, 1);
    }

    this->func_ov031_020e8fec();
}

extern "C" bool StampMonumentInit(MapObject* thisx) {
    bool result = _ZN16MapObjectUnkSPTB19func_ov031_0210b51cEv(thisx);

    // overriding vfunc_00 just to set "give item" mode (based on chests)
    if (gSettings.GetShuffleSettings()->stamps) {
        thisx->mUnk_18[0] = 0x0D;
    }

    return result;
}

extern "C" unk32 StampMonumentItemGive(MapObject* thisx) {
    // if stamps aren't shuffled simply run the original function and return
    if (!gSettings.GetShuffleSettings()->stamps) {
        return _ZN16MapObjectUnkSPTB19func_ov031_0210b6e4Ev(thisx);
    }

    // since "give item" mode is enabled we just have to return the item it here
    UNSET_FLAG(thisx->mFlags, MapObjFlag_9);
    return thisx->mUnk_20.mUnk_00[3];
}
