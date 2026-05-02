#pragma once

#include <types.h>

// 0x1F is the BMG group of rando.bmg
#define MSG(idx) ((0x1F << 16) | (idx))

extern u32 gGetItemMap[];
extern u32 gBMGMap[];
extern u16 gAdvFlagMap[];
