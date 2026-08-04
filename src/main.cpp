#include "game.hpp"
#include "rando.hpp"

extern "C" int __aeabi_atexit(void*, void (*)(void*), void*) { return 0; }

// this function is called by the init hook, see `Rando_InitHook`
extern "C" void Rando_Init() { gRando.Init(); }

// this function is called by the main hook, see `StartUpMain::Run`
extern "C" void Rando_Main() { ((CustomGame*)&gGame)->Run(); }
