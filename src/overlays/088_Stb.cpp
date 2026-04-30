#include <Item/ItemManager.hpp>

extern "C" void GiveItemDuringCS(ItemManager* thisx, ItemFlag itemFlag) {
    if (itemFlag != ItemFlag_LokomoSword && itemFlag != ItemFlag_PanFlute) {
        return;
    }

    SET_FLAG(thisx->mUnk_08, itemFlag);
}
