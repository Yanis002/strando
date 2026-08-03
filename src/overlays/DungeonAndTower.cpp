#include "settings.hpp"

#include <Actor/ActorManager.hpp>
#include <Actor/ActorUnkKEYN.hpp>
#include <Actor/ActorUnkSZKU.hpp>
#include <Unknown/UnkStruct_027e09b8.hpp>
#include <Unknown/UnkStruct_027e0d34.hpp>

// patch for func_ov070_02142140 & func_ov071_0215ff3c (small key & tears of light item give)
class CustomFreestandingActor : public Actor {
  public:
    CustomFreestandingActor() {}

    void TryItemGive(void);
};

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wvolatile"

// KEYN and SKZU happens to share the exact same function in vanilla so let's use the same for both
void CustomFreestandingActor::TryItemGive(void) {
    if (this->mUnk_50 < this->mUnk_52) {
        this->mUnk_50++;
    }

    if (!data_027e09b8->func_01ffd420()) {
        if (data_027e0d34->TryItemGive(this->mUnk_5C.mParams[0])) {
            this->func_ov000_02098a88(0, 1);
            this->Kill();
            this->func_ov000_020984f0();
        }
    }
}

#pragma GCC diagnostic pop

// set item id to the KEYN spawned by MKUR actor
extern "C" void _ZN12ActorUnkKEYN19func_ov070_021418e0Ev(ActorUnkKEYN*, const VecFx32*);

extern "C" void CustomSpinnitKEYNSpawn(ActorRef* param1, const VecFx32* pPos, ActorRef param3, unk16 param4, u8 param5,
                                       u16 param6) {
    ActorParams params;

    params.mUnk_28 = 0;
    params.func_ov000_020975f8();

    params.mInitialPos.x = pPos->x;
    params.mInitialPos.y = pPos->y;
    params.mInitialPos.z = pPos->z;

    params.mUnk_28 = param3;
    params.mUnk_24 = param4;
    params.mUnk_18[0] = param5;
    params.mUnk_1A[0] = param6;

    // should always find the right actor since there's only one of them
    Actor* pMKUR = gGZ.FindActor(ActorId_MKUR);

    if (pMKUR != NULL) {
        switch (gpSettings->GetShuffleDungeonSettings()->keysanity) {
            case KeysanityMode_Dungeon:
            case KeysanityMode_Anywhere:
                // copy randomized item id, param3 is set to MKUR's actor ref
                params.mParams[0] = pMKUR->mUnk_5C.mParams[3];
                break;
            default:
                break;
        }
    }

    Actor::func_ov000_020973f4(param1, &data_ov000_020b539c_eur, ActorId_KEYN, &params, 0);
    _ZN12ActorUnkKEYN19func_ov070_021418e0Ev(((ActorUnkKEYN*)gpActorManager->func_01fff3b4(*param1)), pPos);
}
