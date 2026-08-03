#include "settings.hpp"

extern "C" void func_ov067_02159144(void* thisx);
extern "C" void _ZN18MapObjectChestBase19func_ov031_02103878Ev(void* thisx);

extern "C" void Custom_ov067_02159144(void* thisx) {
    // prevents the goron from having pointers to both chests
    if (!gpSettings->GetShuffleSettings()->goron_range) {
        func_ov067_02159144(thisx);
    }
}

extern "C" void Custom_ov031_02103878(void* thisx) {
    // prevents the goron and PlayerGet from changing the state of the other chest
    if (!gpSettings->GetShuffleSettings()->goron_range) {
        _ZN18MapObjectChestBase19func_ov031_02103878Ev(thisx);
    }
}
