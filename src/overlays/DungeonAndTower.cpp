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
