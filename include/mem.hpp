#pragma once

#include <mem.h>
#include <stddef.h>
#include <types.h>

#include <Unknown/UnkMemFuncs.h>

extern "C" u8 _heap_start[];
extern "C" u8 _overlay_end[];

#define FREE 'EERF'
#define USED 'DESU'

struct HeapHandler {
    u32 magic;
    void* heapLo;
    void* heapHi;
    size_t heapSize;

    struct HeapSlot {
        u32 state;
        size_t size;
        HeapSlot* prev;
        HeapSlot* next;

        HeapSlot() { this->Reset(); }

        void* GetStart() { return (void*)((u8*)this + sizeof(HeapSlot)); }

        void SetFree() { this->state = FREE; }

        void SetUsed() { this->state = USED; }

        bool IsFree() { return this->state == FREE; }

        void Clear() { memset(this->GetStart(), 0, this->size); }

        void Reset() {
            this->SetFree();
            this->size = 0;
            this->prev = nullptr;
            this->next = nullptr;
        }
    };

    size_t GetHeapSize() { return this->heapSize; }

    static HeapHandler* GetHeapHandler();
    HeapHandler();
    HeapSlot* FindSlot(size_t size);
    void* Alloc(size_t size);
    void Free(void* ptr);
};

inline void* operator new(size_t size) {
    HeapHandler* pHandler = HeapHandler::GetHeapHandler();

    // abort if the requested size doesn't fit
    if (size > pHandler->GetHeapSize() || size == 0) {
        size = 1;
    }

    // do the allocation with the requested size aligned
    return pHandler->Alloc((size + (4 - 1)) & ~(4 - 1));
}

inline void* operator new[](size_t size) {
    HeapHandler* pHandler = HeapHandler::GetHeapHandler();

    if (size > pHandler->GetHeapSize() || size == 0) {
        size = 1;
    }

    return pHandler->Alloc((size + (4 - 1)) & ~(4 - 1));
}

inline void operator delete(void* ptr) {
    if (ptr != nullptr) {
        HeapHandler::GetHeapHandler()->Free(ptr);
    }
}

inline void operator delete[](void* ptr) {
    if (ptr != nullptr) {
        HeapHandler::GetHeapHandler()->Free(ptr);
    }
}

inline void operator delete(void* ptr, unsigned int) {
    if (ptr != nullptr) {
        HeapHandler::GetHeapHandler()->Free(ptr);
    }
}

inline void operator delete[](void* ptr, unsigned int) {
    if (ptr != nullptr) {
        HeapHandler::GetHeapHandler()->Free(ptr);
    }
}
