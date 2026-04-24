#include "common.hpp"

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wparentheses"

// from oot-gc
extern "C" char* strcat(char* dst, const char* src) {
    const u8* p = (u8*)src - 1;
    u8* q = (u8*)dst - 1;

    while (*++q)
        ;

    q--;

    while (*++q = *++p)
        ;

    return (dst);
}

#pragma GCC diagnostic pop
