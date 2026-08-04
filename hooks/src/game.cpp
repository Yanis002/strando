#include <Game/Game.hpp>
#include <System/OverlayManager.hpp>
#include <System/Random.hpp>
#include <Unknown/UnkStruct_02049b74.hpp>
#include <Unknown/UnkStruct_02049bd4.hpp>
#include <Unknown/UnkStruct_0204a110.hpp>
#include <Unknown/UnkStruct_0204e64c.hpp>
#include <Unknown/UnkStruct_027e0208.hpp>
#include <nitro/os.h>
#include <nitro/reg.h>

extern "C" void Rando_Main();

class StartUpMain : public Game {
    void Run();
};

extern "C" void func_020196fc();
extern "C" void FlushGfxQueue();
extern "C" void func_020132c8();
extern "C" void func_020132dc();
extern "C" void func_02013354();
extern "C" void func_0201328c();
extern Mat3p gGeomMatrix;

// shorter version of the main loop specifically for boot time, no idea if this affects things later though...
void StartUpMain::Run() {
    this->func_ov018_020c48a4();

    do {
        // initialization of the next game mode
        if (this->createCallback != NULL) {
            data_0204999c.func_02013014();

            {
                UnkDataStruct2 local_28(sizeof(GameSaveSlot));
                this->mpSaveSlot = (GameSaveSlot*)local_28.unk_00;

                this->mpCurrentGameMode = this->createCallback();
                this->createCallback = NULL;
                this->mpCurrentGameMode->vfunc_08();
                this->mpSaveSlot = NULL;
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
            REG_GFX_FIFO_SWAP_BUFFERS = 3;
            OS_RestoreInterrupts(enabled);
        }

        func_020132c8();
    } while (gOverlayManager.mLoadedOverlays[OverlaySlot_4] == OverlayIndex_StartUp);

    Rando_Main();
}
