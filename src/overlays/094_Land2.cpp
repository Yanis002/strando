#include <MapObject/MapObjectUnkWDST.hpp>
#include <Unknown/UnkStruct_027e09b8.hpp>
#include <Unknown/UnkStruct_027e0d34.hpp>

// patch for func_ov094_02172290 (songs item give)
class CustomMapObjectUnkWDST : public MapObjectUnkWDST {
public:
    CustomMapObjectUnkWDST() {}

    void TryItemGive(void);
};

void CustomMapObjectUnkWDST::TryItemGive(void) {
    if (!data_027e09b8->func_01ffd420()) {
        data_027e0d34->TryItemGive(this->mUnk_B8);
        this->func_ov094_02172c94(5);
    }
}
