#include "gz.hpp"
#include "settings.hpp"

#include <Actor/ActorUnkRB1T.hpp>
#include <Save/SaveManager.hpp>
#include <flags.h>

extern UnkActorDataStruct1 data_ov026_02137edc;

class CustomRabbit : public ActorUnkRB1T {
  public:
    void CustomSetFlag();
    bool CustomSpawnOrKill(unk32 param1);
};

bool IsRabbitValid(RabbitFlag flag) {
    u8 mode = gSettings.GetShuffleSettings()->rabbitsanity & RabbitMode_All;

    if (mode == RabbitMode_All) {
        return true;
    }

    if (flag >= RabbitFlag_Grass_01 && flag <= RabbitFlag_Grass_10) {
        return (mode & RabbitMode_Grass) != 0;
    }

    if (flag >= RabbitFlag_Snow_01 && flag <= RabbitFlag_Snow_10) {
        return (mode & RabbitMode_Snow) != 0;
    }

    if (flag >= RabbitFlag_Water_01 && flag <= RabbitFlag_Water_10) {
        return (mode & RabbitMode_Water) != 0;
    }

    if (flag >= RabbitFlag_Mountain_01 && flag <= RabbitFlag_Mountain_10) {
        return (mode & RabbitMode_Mountain) != 0;
    }

    if (flag >= RabbitFlag_Sand_01 && flag <= RabbitFlag_Sand_10) {
        return (mode & RabbitMode_Sand) != 0;
    }

    return false;
}

void CustomRabbit::CustomSetFlag() {
    // if the rabbit is not valid it means it's not meant to be shuffled
    // so we execute the vanilla behavior instead of giving the item
    if (IsRabbitValid(this->mUnk_5C.mParams[1])) {
        RandoTryItemGive(this->mUnk_5C.mParams[0]);
        SET_FLAG(gGZ.GetCurrentSave()->rabbitFlags, this->mUnk_5C.mParams[1]);
    } else {
        SET_FLAG(gSaveManager.GetUnk000()->unk_B78.rabbitFlags, this->mUnk_5C.mParams[1]);
    }

    this->vfunc_98(4);
    this->mUnk_280 = 0;
}

bool CustomRabbit::CustomSpawnOrKill(unk32 param1) {
    // if the rabbit is not valid it means it's not meant to be shuffled
    // so we execute the vanilla behavior instead of checking if we got the item
    if (IsRabbitValid(this->mUnk_5C.mParams[1])) {
        if (GET_FLAG(gGZ.GetCurrentSave()->rabbitFlags, this->mUnk_5C.mParams[1])) {
            // kill the actor if we already got the item
            this->Kill();
            return true;
        }

        this->Actor_Derived1::vfunc_18(param1);
        this->mUnk_0E4 = (void (*)())ActorUnkRB1T::func_ov026_021208a0;

        int result = this->func_ov026_0211e6cc();
        func_ov000_02099ddc(&this->mUnk_300, data_ov026_02137edc, 0x1000, result << 12);

        this->func_ov026_0211e554();

        this->mUnk_36C = 0;
        this->mUnk_36D = 0;
        this->mUnk_36E = 0;
        this->mUnk_36F = 0;
        this->mUnk_370 = 0;
        this->mUnk_371 = 0;
        this->mUnk_372 = 0;
        this->mUnk_373 = 0;
        this->mUnk_374 = 0;
        this->mUnk_375 = 0;
        this->mUnk_376 = 0;
        this->mUnk_377 = 0;
        return true;
    }

    return this->func_ov026_0211e3e0(param1);
}
