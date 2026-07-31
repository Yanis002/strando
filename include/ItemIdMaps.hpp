#pragma once

#include <types.h>

// 0x40 is the BMG group of rando.bmg
#define MSG(idx) ((0x40 << 16) | (idx))

extern u32 gGetItemMap[];
extern u32 gBMGMap[];
extern u16 gAdvFlagMap[];
