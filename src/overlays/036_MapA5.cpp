#include <Actor/Actor.hpp>
#include <Item/Item.hpp>
#include <Item/ItemManager.hpp>

typedef unk32 ShopItemPosition;
enum ShopItemPosition_ {
    ShopItemPosition_TopLeft,
    ShopItemPosition_Middle,
    ShopItemPosition_TopRight,
    ShopItemPosition_BottomLeft,
    ShopItemPosition_BottomRight,
};

// generic class since it's gonna be used for each shop keepers:
// - ActorUnkCAMY::func_ov036_0211b148 - hyrule town shop
// - ActorUnkFOMY::func_ov036_0211b420 - mayscore shop
// - ActorUnkYUKY::func_ov036_0211b6f8 - snow sanctuary shop
// - ActorUnkWAWY::func_ov036_0211b9e8 - papuzia village shop
// - ActorUnkGORY::func_ov036_0211bcb0 - goron village shop
// - ActorUnkTERY::func_ov036_0211c02c - beedle shop

class CustomShopKeeper : public Actor {
    /* 94 */ STRUCT_PAD(0x94, 0xE4);
    /* E4 */ ItemId mItemId;

    CustomShopKeeper() {}

    ItemId GetShopItemId(ShopItemPosition itemPos);
    u16 GetShopItemPrice(void);
};

ItemId CustomShopKeeper::GetShopItemId(ShopItemPosition itemPos) {
    u8* actorParams = (u8*)this->mUnk_5C.mParams;
    u8 item;

    switch (itemPos) {
        case ShopItemPosition_TopLeft:
        case ShopItemPosition_Middle:
        case ShopItemPosition_TopRight:
        case ShopItemPosition_BottomLeft:
        case ShopItemPosition_BottomRight:
            item = actorParams[itemPos];
            return item > ItemId_Nothing ? item : ItemId_SoldOutSign;
        default:
            break;
    }

    return ItemId_SoldOutSign;
}

u16 CustomShopKeeper::GetShopItemPrice(void) {
    switch (this->mItemId) {
        case ItemId_NormalShield: {
            u16 param = this->mUnk_5C.mParams[3];
            if (param == 4) {
                return 200;
            }
            if (param == 2) {
                return 150;
            }
            return 80;
        }
        case ItemId_RedPotion:
            return 100;
        case ItemId_PurplePotion:
            return 150;
        case ItemId_YellowPotion:
            return 200;
        case ItemId_TenPriceCard:
            return 100;
        case ItemId_DemonFossil:
        case ItemId_StalfosSkull:
        case ItemId_StarFragment:
        case ItemId_BeeLarvae:
        case ItemId_WoodHeart:
        case ItemId_DarkPearlLoop:
        case ItemId_WhitePearlLoop:
        case ItemId_RutoCrown:
        case ItemId_DragonScale:
        case ItemId_PirateNecklace:
        case ItemId_PalaceDish:
        case ItemId_GoronAmber:
        case ItemId_MysticJade:
        case ItemId_AncientCoin:
        case ItemId_PricelessStone:
        case ItemId_RegalRing: {
            return data_ov000_020b6510->func_ov000_020a9b4c(this->mItemId - ItemId_DemonFossil) * 2;
        }
        case ItemId_HeartContainer:
            return 2000;
        case ItemId_BombsRefill: {
            u16 param = this->mUnk_5C.mParams[3];

            if (param == 4) {
                return 200;
            }

            if (param == 3) {
                return 150;
            }

            return 100;
        }
        case ItemId_ArrowsRefill:
            return 50;
        case ItemId_QuiverMedium:
        case ItemId_QuiverLarge:
            return 2000;
        case ItemId_BombBag:
        case ItemId_BombBagMedium:
        case ItemId_BombBagLarge:
            return 500;
        case ItemId_Nothing:
            break;
        case ItemId_NormalSword:
            break;
        case ItemId_Whirlwind:
            break;
        case ItemId_NormalBow:
            break;
        case ItemId_Boomerang:
            break;
        case ItemId_Whip:
            break;
        case ItemId_SandRod:
            break;
        case ItemId_9:
            break;
        case ItemId_NormalKey:
            break;
        case ItemId_BossKey:
            break;
        case ItemId_GreenRupee:
            break;
        case ItemId_BlueRupee:
            break;
        case ItemId_RedRupee:
            break;
        case ItemId_BigGreenRupee:
            break;
        case ItemId_BigRedRupee:
            break;
        case ItemId_BigGoldRupee:
            break;
        case ItemId_ForceGem_18:
            break;
        case ItemId_ForceGem_19:
            break;
        case ItemId_ForceGem_20:
            break;
        case ItemId_ForestGlyph:
            break;
        case ItemId_SnowGlyph:
            break;
        case ItemId_OceanGlyph:
            break;
        case ItemId_FireGlyph:
            break;
        case ItemId_25:
            break;
        case ItemId_26:
            break;
        case ItemId_27:
            break;
        case ItemId_28:
            break;
        case ItemId_29:
            break;
        case ItemId_FinalTrack:
            break;
        case ItemId_31:
            break;
        case ItemId_32:
            break;
        case ItemId_33:
            break;
        case ItemId_34:
            break;
        case ItemId_ForceGem_35:
            break;
        case ItemId_ForceGem_36:
            break;
        case ItemId_ForceGem_37:
            break;
        case ItemId_RecruitUniform:
            break;
        case ItemId_PostmasterLetter:
            break;
        case ItemId_ForceGem_43:
            break;
        case ItemId_ForceGem_44:
            break;
        case ItemId_ForceGem_45:
            break;
        case ItemId_ForceGem_46:
            break;
        case ItemId_ForceGem_47:
            break;
        case ItemId_ForceGem_48:
            break;
        case ItemId_ForceGem_49:
            break;
        case ItemId_ForceGem_50:
            break;
        case ItemId_ForceGem_51:
            break;
        case ItemId_ForceGem_52:
            break;
        case ItemId_ForceGem_53:
            break;
        case ItemId_ForceGem_54:
            break;
        case ItemId_ForceGem_55:
            break;
        case ItemId_ForceGem_56:
            break;
        case ItemId_ForceGem_57:
            break;
        case ItemId_ForceGem_58:
            break;
        case ItemId_ForceGem_59:
            break;
        case ItemId_ForceGem_60:
            break;
        case ItemId_ForceGem_61:
            break;
        case ItemId_PanFlute:
            break;
        case ItemId_StampBook:
            break;
        case ItemId_LightBow:
            break;
        case ItemId_LokomoSword:
            break;
        case ItemId_SoldOutSign:
            return 9999;
        case ItemId_AncientShield:
            break;
        case ItemId_RandCommonTreasure:
            break;
        case ItemId_RandUncommonTreasure:
            break;
        case ItemId_RandRareTreasure:
            break;
        case ItemId_RandLegendaryTreasure:
            break;
        case ItemId_TearLight:
            break;
        case ItemId_LightCompass:
            break;
        case ItemId_ScrollSpinAttack:
            break;
        case ItemId_ScrollBeam:
            break;
        case ItemId_LinebeckLetter:
            break;
        case ItemId_PanFluteSong_101:
            break;
        case ItemId_PanFluteSong_102:
            break;
        case ItemId_PanFluteSong_103:
            break;
        case ItemId_PanFluteSong_104:
            break;
        case ItemId_PanFluteSong_105:
            break;
        case ItemId_RabbitNet:
            break;
        case ItemId_BeedleCard:
            break;
        case ItemId_SilverCard:
            break;
        case ItemId_GoldCard:
            break;
        case ItemId_PlatinumCard:
            break;
        case ItemId_DiamondCard:
            break;
        case ItemId_FreebieCard:
            break;
        case ItemId_QuintupleCard:
            break;
        case ItemId_CarbenLetter:
            break;
        case ItemId_RecruitUniform2:
            break;
        case ItemId_EngineerUniform:
            break;
        default:
            break;
    }

    return 500;
}
