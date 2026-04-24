#include <Game/Game.hpp>
#include <System/OverlayManager.hpp>
#include <System/Random.hpp>
#include <Unknown/UnkStruct_02049b74.hpp>
#include <Unknown/UnkStruct_02049bd4.hpp>
#include <Unknown/UnkStruct_0204a110.hpp>
#include <Unknown/UnkStruct_0204e64c.hpp>
#include <Unknown/UnkStruct_027e0208.hpp>
#include <regs.h>

extern "C" void GZ_Main();

class StartUpMain : public Game {
    void Run();
};

extern "C" void func_020196fc();
extern "C" void FlushGfxQueue();
extern "C" void func_020132c8();
extern "C" void func_020132dc();
extern "C" void func_02013354();
extern "C" void func_0201328c();
extern "C" int OS_DisableInterrupts_Irq();
extern "C" void OS_RestoreInterrupts(int enabled);
extern Mat3p gGeomMatrix;

struct SomeSaveFileStruct {
    /* 00 */ SaveFile* mpSaveFiles[MAX_SAVE_SLOTS];

    SomeSaveFileStruct(unk32 param1);
    ~SomeSaveFileStruct();
};

// shorter version of the main loop specifically for boot time, no idea if this affects things later though...
void StartUpMain::Run() {
    this->func_ov018_020c48a4();

    do {
        // initialization of the next game mode
        if (this->createCallback != NULL) {
            data_0204999c.func_02013014();

            {
                SomeSaveFileStruct local_28(0x1300);
                this->mpSaveFile = local_28.mpSaveFiles[0];

                this->mpCurrentGameMode = this->createCallback();
                this->createCallback = NULL;
                this->mpCurrentGameMode->vfunc_08();
                this->mpSaveFile = NULL;
            }

            data_0204999c.func_02013070();
        }

        // update of the current game mode
        if (this->mpCurrentGameMode != NULL) {
            if (data_0204a110.func_02019514() == 0 && data_0204e64c.mUnk_00.mUnk_0B == 0) {
                this->mpCurrentGameMode->vfunc_0C();
            }

            if (data_0204e64c.mUnk_00.mUnk_0B == 0) {
                data_0204a110.func_02019408();
            }
        }

        {
            int enabled = OS_DisableInterrupts_Irq();
            this->mUnk_1C.func_02013e18((void*)func_020132dc, 0);
            REG_SWAP_BUFFERS = 3;
            OS_RestoreInterrupts(enabled);
        }

        func_020132c8();
    } while (gOverlayManager.mLoadedOverlays[OverlaySlot_4] == OverlayIndex_StartUp);

    GZ_Main();
}
