/**
 * @file: hooks.c
 *
 * This file implements the hooks that are replacing vanilla functions so we can run custom code.
 * Make sure to make it as small as possible!
 */

extern void _ZN4Game19func_ov018_020c48f8Ev(void* ptr);
extern void FS_LoadOverlay(int param1, int overlayID);
extern void GZ_Init();

#ifndef __INTELLISENSE__
#ifndef GZ_OVL_ID
#error "overlay id is not defined!"
#endif

#ifndef OVERLAY_0_SLOT_ADDR
#error "address of overlay 0 is not defined!"
#endif
#else
#define GZ_OVL_ID 0
#define OVERLAY_0_SLOT_ADDR 0
#endif

#define nOverlay0 (*(unsigned int*)OVERLAY_0_SLOT_ADDR)

// init hook: replace the `func_ov018_020c48f8` call from `GameModeStartUp::vfunc_0C` so we can load and init the gz
// overlay
void GZ_InitHook(void* ptr) {
    _ZN4Game19func_ov018_020c48f8Ev(ptr);

    // make sure overlay 0 has completed loading
    while (nOverlay0 != 0) {}

    // load our overlay
    FS_LoadOverlay(0, GZ_OVL_ID);

    // call the init function
    GZ_Init();
}
