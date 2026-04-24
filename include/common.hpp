#pragma once

#include <Unknown/UnkStruct_027e09a4.hpp>
#include <types.h>

typedef void (*GZAction)(u32 params);
typedef bool (*GZCheckCallback)(int itemIndex);

struct RoomIndicesInfos {
    const u8* ptr;
    u8 count;
};

extern const RoomIndicesInfos gRoomIndicesPtrs[SceneIndex_Max];

// from oot-gc
extern "C" char* strcat(char* dst, const char* src);

extern "C" void DisplayDebugText(int, void*, int, int, const char*);
extern "C" void DisplayDebugTextF(int, void*, int, int, const char*, ...);
extern "C" void GXS_SetGraphicsMode(int);
extern "C" void func_0201b180(bool, bool);
extern "C" void DC_func_0004(void*, int);
extern "C" void GXS_LoadBG0Scr(void*, int, int);
extern "C" void func_ov000_02070af8(UnkStruct_027e09a4*);
extern "C" void func_ov000_02071000(UnkStruct_WarpUnk1*, UnkStruct_SceneChange1*, unk32);
