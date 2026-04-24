OUTPUT_FORMAT("elf32-littlearm", "elf32-littlearm", "elf32-littlearm")
OUTPUT_ARCH(arm)

SECTIONS
{
    . = HOOKS_ADDR;

    _hooks_start = .;

    __hooks_text_start = .;
    .text : {
        KEEP(*(.text))
        *(.text.*)
        *(.glue_7)
        *(.glue_7t)
        . = ALIGN(4);
    }
    __hooks_text_end = .;

    __hooks_rodata_start = .;
    .rodata : {
        KEEP(*(.rodata))
        *(.rodata.*)
        . = ALIGN(4);
    }
    __hooks_rodata_end = .;

    __hooks_data_start = .;
    .data : {
        KEEP(*(.data))
        *(.data.*)
        . = ALIGN(4);
    }
    __hooks_data_end = .;

    __hooks_bss_start = .;
    __hooks_bss_end = .;
    .bss : {
        KEEP(*(.bss))
        *(.bss.*)
        *(COMMON)
        . = ALIGN(4);
    }
    __hooks_bss_end = .;

    __hooks_init_start = .;
    .init : {
        KEEP(*(.init))
        . = ALIGN(4);
    }
    __hooks_init_end = .;

    __hooks_ctor_start = .;
    .ctor : {
        KEEP(*(.ctor))
        KEEP(*(.ctors))
        KEEP(*(.init_array*))
        . = ALIGN(4);
    }
    __hooks_ctor_end = .;

    /DISCARD/ : {
        *(.comment)
        *(.ARM.attributes)
    }
}
