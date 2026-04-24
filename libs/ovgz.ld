OUTPUT_FORMAT("elf32-littlearm", "elf32-littlearm", "elf32-littlearm")
OUTPUT_ARCH(arm)

SECTIONS
{
    . = OVLGZ_ADDR;

    _overlay_start = .;
    _overlay_end = _overlay_start + OVLGZ_SIZE - RESERVED_SIZE;

    __text_start = .;
    .text : {
        KEEP(*(.text))
        *(.text.*)
        *(.glue_7)
        *(.glue_7t)
        . = ALIGN(32);
    }
    __text_end = .;

    __rodata_start = .;
    .rodata : {
        KEEP(*(.rodata))
        *(.rodata.*)
        . = ALIGN(32);
    }
    __rodata_end = .;

    __data_start = .;
    .data : {
        KEEP(*(.data))
        *(.data.*)
        . = ALIGN(32);
    }
    __data_end = .;

    __bss_start = .;
    __bss_end = .;
    .bss : {
        KEEP(*(.bss))
        *(.bss.*)
        *(COMMON)
        . = ALIGN(32);
    }
    __bss_end = .;

    __init_start = .;
    .init : {
        KEEP(*(.init))
        . = ALIGN(32);
    }
    __init_end = .;

    __ctor_start = .;
    .ctor : {
        KEEP(*(.ctor))
        KEEP(*(.ctors))
        KEEP(*(.init_array*))
        . = ALIGN(32);
    }
    __ctor_end = .;

    _heap_start = .;

    __dso_handle = 0;

    /DISCARD/ : {
        *(.comment)
        *(.ARM.attributes)
    }
}
