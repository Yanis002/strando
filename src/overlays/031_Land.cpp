#include "036_MapA5.hpp"
#include "ItemIdMaps.hpp"
#include "rando.hpp"
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

struct UnkStruct_ov049_02137ef4 {
    /* 00 */ AdventureFlag flag;
    /* 04 */ unk32 unk_04;
    /* 08 */ bool unk_08;
    /* 09 */ u8 unk_09[3];
    /* 0C */ void* unk_0C;
};
extern UnkStruct_ov049_02137ef4 data_ov049_02137ef4[];

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

bool IsTosSection(ItemId itemId) {
    if (itemId >= ExtraItemId_TowerSection_1 && itemId <= ExtraItemId_TowerSection_5) {
        return true;
    }

    return false;
}

ItemId GetProgressiveToSSection(ItemId requestedItemId) {
    ItemId itemId = requestedItemId;
    AdventureFlag* pFlags = data_027e09b8->mAdventureFlags;

    switch (requestedItemId) {
        case ExtraItemId_TowerSection_1:
        case ExtraItemId_TowerSection_2:
        case ExtraItemId_TowerSection_3:
        case ExtraItemId_TowerSection_4:
        case ExtraItemId_TowerSection_5:
            if (!GET_FLAG(pFlags, RandoAdventureFlag_TowerSection_1)) {
                itemId = ExtraItemId_TowerSection_1;
            } else if (!GET_FLAG(pFlags, RandoAdventureFlag_TowerSection_2)) {
                itemId = ExtraItemId_TowerSection_2;
            } else if (!GET_FLAG(pFlags, RandoAdventureFlag_TowerSection_3)) {
                itemId = ExtraItemId_TowerSection_3;
            } else if (!GET_FLAG(pFlags, RandoAdventureFlag_TowerSection_4)) {
                itemId = ExtraItemId_TowerSection_4;
            } else if (!GET_FLAG(pFlags, RandoAdventureFlag_TowerSection_5)) {
                itemId = ExtraItemId_TowerSection_5;
            }
            break;
        default:
            break;
    }

    return itemId;
}

ItemId GetProgressiveItemId(ItemId requestedItemId) {
    ItemId itemId = requestedItemId;

    if (IsTosSection(requestedItemId)) {
        if (gpSettings->GetShuffleDungeonSettings()->tos_sections == ToSSectionsMode_Progressive) {
            itemId = GetProgressiveToSSection(requestedItemId);
        }
    } else if (IsGlyphOrSource(requestedItemId)) {
        switch (gpSettings->GetShuffleSettings()->glyphs_and_sources) {
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
        Inventory* pInv = data_027e0ce0->mUnk_2C->GetInventory();

        switch (requestedItemId) {
            // progressive shield
            case ItemId_NormalShield:
            case ItemId_AncientShield:
                if (pInv->HasItem(ItemFlag_Shield)) {
                    itemId = ItemId_AncientShield;
                } else {
                    itemId = ItemId_NormalShield;
                }
                break;

            // progressive sword
            case ItemId_NormalSword:
            case ItemId_LokomoSword:
                if (pInv->HasItem(ItemFlag_Sword)) {
                    itemId = ItemId_LokomoSword;
                } else {
                    itemId = ItemId_NormalSword;
                }
                break;

            // progressive bomb bag
            case ItemId_BombBag:
            case ItemId_BombBagMedium:
            case ItemId_BombBagLarge:
                if (!pInv->HasItem(ItemFlag_Bombs)) {
                    itemId = ItemId_BombBag;
                    break;
                }

                if (data_027e0ce0->mUnk_2C->GetBombsCap() == UpgradeCapacity_Tier2) {
                    itemId = ItemId_BombBagLarge;
                } else if (data_027e0ce0->mUnk_2C->GetBombsCap() == UpgradeCapacity_Tier1) {
                    itemId = ItemId_BombBagMedium;
                } else {
                    itemId = ItemId_BombBag;
                }
                break;

            // progressive quiver
            case ItemId_NormalBow:
            case ItemId_QuiverMedium:
            case ItemId_QuiverLarge:
                if (!pInv->HasItem(ItemFlag_Bow)) {
                    itemId = ItemId_NormalBow;
                    break;
                }

                if (data_027e0ce0->mUnk_2C->GetQuiverCap() == UpgradeCapacity_Tier2) {
                    itemId = ItemId_QuiverLarge;
                } else if (data_027e0ce0->mUnk_2C->GetQuiverCap() == UpgradeCapacity_Tier1) {
                    itemId = ItemId_QuiverMedium;
                } else {
                    itemId = ItemId_NormalBow;
                }
                break;

            case ItemId_LightBow:
                if (!pInv->HasItem(ItemFlag_Bow)) {
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
    bool doDefault = true;

    // if we're trying to give a letter and the shuffle is enabled, give the randomized item
    if (gpSettings->GetShuffleSettings()->letters != LetterMode_Off) {
        if (requestedItemId == ItemId_PostmasterLetter && gRando.IsMapC3()) {
            struct Postman {
                STRUCT_PAD(0x00, 0x2AC);
                unk32 mUnk_2AC;
            };

            Postman* pPostman = (Postman*)gRando.FindActor(ActorId_PTMN);

            if (pPostman != NULL) {
                itemId = gpSettings->GetLetterItemId((data_ov049_02137ef4[pPostman->mUnk_2AC].flag & 0xFFFF) -
                                                     AdventureFlag_MetPostmanFirstLetter);
                doDefault = false;
            }
        } else if (requestedItemId == ItemId_CarbenLetter) {
            itemId = gpSettings->GetLetterItemId(LetterType_ReceivedCarbens);
            doDefault = false;
        } else if (requestedItemId == ItemId_LinebeckLetter) {
            itemId = gpSettings->GetLetterItemId(LetterType_ObtainedLinebecks);
            doDefault = false;
        }
    }

    if (doDefault) {
        // handle progressive items
        itemId = GetProgressiveItemId(requestedItemId);
    }

    if (!gRando.IsOnLand()) {
        // if on not on land just add to the item queue
        gRando.TryAddItemToQueue(itemId);

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
    if (!gpSettings->GetShuffleSettings()->rupeesanity || this->mUnk_5C.mParams[1] == 0) {
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

void CustomRupee::Custom_ov031_020e9068() {
    // if rupeesanity is disabled or this is a spawned rupee, simply run the original function
    if (!gpSettings->GetShuffleSettings()->rupeesanity || this->mUnk_5C.mParams[1] == 0) {
        this->func_ov031_020e9068();
        return;
    }

    this->SetState(ActorRupeeState_5);

    if (this->mUnk_5C.mUnk_24 >= 0 && this->mUnk_5C.mUnk_1A[0] != 0) {
        this->func_ov000_02098a88(0, 1);
    }

    this->func_ov031_020e8fec();
}

extern "C" bool StampMonumentInit(MapObject* thisx) {
    bool result = _ZN16MapObjectUnkSPTB19func_ov031_0210b51cEv(thisx);

    // overriding vfunc_00 just to set "give item" mode (based on chests)
    if (gpSettings->GetShuffleSettings()->stamps) {
        thisx->mUnk_18[0] = 0x0D;

        if (data_027e09b8->HasAdventureFlag(gAdvFlagMap[thisx->mUnk_20.mParams[3]])) {
            UNSET_FLAG(thisx->mFlags, MapObjFlag_9);
        }
    }

    return result;
}

extern "C" unk32 StampMonumentItemGive(MapObject* thisx) {
    // if stamps aren't shuffled simply run the original function and return
    if (!gpSettings->GetShuffleSettings()->stamps) {
        return _ZN16MapObjectUnkSPTB19func_ov031_0210b6e4Ev(thisx);
    }

    // since "give item" mode is enabled we just have to return the item it here
    UNSET_FLAG(thisx->mFlags, MapObjFlag_9);
    return thisx->mUnk_20.mParams[3];
}
