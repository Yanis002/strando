-include ../print_rules.mk

all:
	$(V)gcc -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE makeppf3.c -o makeppf3 -Wno-multichar
	$(V)gcc -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE patchppf3.c -o patchppf3 -Wno-multichar

clean:
	$(V)rm makeppf3 patchppf3
