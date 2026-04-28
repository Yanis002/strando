MAKEFLAGS += --no-builtin-rules

# Set PACKAGE_NAME define for printing commit name
ifeq ($(origin PACKAGE_NAME), undefined)
  PACKAGE_NAME := "$(shell git log -1 --pretty=%s | tr -d '()`"\n' | tr -d "'" | sed 's/\"/\\\"/g')"
  ifeq ($(PACKAGE_NAME),"")
    PACKAGE_NAME := "Unknown name"
  endif
endif

# Set PACKAGE_COMMIT_AUTHOR for printing commit author
ifeq ($(origin PACKAGE_COMMIT_AUTHOR), undefined)
  PACKAGE_COMMIT_AUTHOR := "$(shell git log -1 --pretty=format:'%an' | tr -d '\n' | sed 's/\"/\\\"/g')"
  ifeq ($(PACKAGE_COMMIT_AUTHOR),"")
    PACKAGE_COMMIT_AUTHOR := "Unknown author"
  endif
endif

# Set PACKAGE_AUTHOR define for printing author's git name
ifeq ($(origin PACKAGE_AUTHOR), undefined)
  PACKAGE_AUTHOR := "$(shell git config --get user.name | tr -d '\n' | sed 's/\"/\\\"/g')"
  ifeq ($(PACKAGE_AUTHOR),"")
    PACKAGE_AUTHOR := "Unknown author"
  endif
endif

# Set PACKAGE_VERSION define for printing commit hash
ifeq ($(origin PACKAGE_VERSION), undefined)
  PACKAGE_VERSION := "$(shell git log -1 --pretty=%h | tr -d '\n' | sed 's/\"/\\\"/g')"
  ifeq ($(PACKAGE_VERSION),"")
    PACKAGE_VERSION := "Unknown version"
  endif
endif

-include tools/print_rules.mk

# disable ds-rom output
export RUST_LOG = ds_rom::rom::rom=warn

# Ensure the build fails if a piped command fails
SHELL = /usr/bin/env bash
.SHELLFLAGS = -o pipefail -c

# path to decomp, defaults to the submodule's path
STGZ_DECOMP_DIR ?= resources/decomp
STGZ_EMULATOR ?=

# game region, only eur is supported atm
REGION := eur
VERSION := $(shell echo $(REGION) | tr '[:lower:]' '[:upper:]')

COMPARE ?= 1
OUT_HASH ?= 0

### project tools ###

MAKE = make
MKDIR ?= mkdir
CMAKE ?= cmake
RM ?= rm
CP ?= cp -v

# python
VENV := .venv
PYTHON ?= $(VENV)/bin/python3

# download tool (took from st decomp)
DL_TOOL := $(PYTHON) tools/download_tool.py

# rom patcher tool
ROM_PATCHER := $(PYTHON) tools/rom_patcher.py

# ds-rom
DSROM := tools/dsrom

# armips setup
ARMIPS_DIR := tools/armips
ARMIPS ?= $(ARMIPS_DIR)/out/armips

# PPF
MAKEPPF3 ?= tools/ppf/makeppf3

# main source/objects
BUILD_DIR := build/$(REGION)
ALL_FILES := $(sort $(shell find src/ -path "src/thumb" -prune -o -print))
ASM_FILES := $(filter %.s, $(ALL_FILES))
C_FILES := $(filter %.c, $(ALL_FILES))
CPP_FILES := $(filter %.cpp, $(ALL_FILES))
OBJ := $(foreach f,$(ASM_FILES),$(BUILD_DIR)/$(f:.s=.o)) $(foreach f,$(C_FILES),$(BUILD_DIR)/$(f:.c=.o)) $(foreach f,$(CPP_FILES),$(BUILD_DIR)/$(f:.cpp=.o)) $(BUILD_DIR)/src/thumb/thumb-$(REGION).o
DEPS := $(foreach f,$(ASM_FILES),$(BUILD_DIR)/$(f:.s=.d)) $(foreach f,$(C_FILES),$(BUILD_DIR)/$(f:.c=.d)) $(foreach f,$(CPP_FILES),$(BUILD_DIR)/$(f:.cpp=.d))

# hooks source/objects
HOOKS_BUILD_DIR := hooks/build/$(REGION)
HOOKS_SRC := $(wildcard hooks/src/*.c)
HOOKS_OBJ := $(foreach f,$(HOOKS_SRC:hooks/%=%),$(HOOKS_BUILD_DIR)/$(f:.c=.o))
HOOKS_DEPS := $(foreach f,$(HOOKS_SRC:hooks/%=%),$(HOOKS_BUILD_DIR)/$(f:.c=.d))
HOOKS_GAME_SRC := $(wildcard hooks/src/*.cpp)
HOOKS_GAME_OBJ := $(foreach f,$(HOOKS_GAME_SRC:hooks/%=%),$(HOOKS_BUILD_DIR)/$(f:.cpp=.o))
HOOKS_GAME_DEPS := $(foreach f,$(HOOKS_GAME_SRC:hooks/%=%),$(HOOKS_BUILD_DIR)/$(f:.cpp=.d))

ALL_DEPS := $(sort $(DEPS) $(HOOKS_DEPS) $(HOOKS_GAME_DEPS))

# region addresses
ifeq ($(REGION),eur)
OVL018_ADDR := 0x020C4840
OVLGZ_ADDR := 0x0218A380
HOOK_INIT := 0x020C4DD0
HOOK_UPDATE := 0x02013464
MAIN_ADDR := 0x02000BC8
OVERLAY_0_SLOT_ADDR := 0x02043E50 # in reality this is the address of gOverlayManager
HOOKS_ADDR := 0x01FFFE20
HOOKS_GAME_ADDR := 0x02013394

# shops
OVL036_ADDR := 0x02118FC0
HOOK_PRICE_1_ADDR := 0x0211CDF4
HOOK_PRICE_2_ADDR := 0x0211CE3C
HOOK_PRICE_3_ADDR := 0x0211CE64
HOOK_PRICE_4_ADDR := 0x0211CE8C
HOOK_PRICE_5_ADDR := 0x0211CEB4
HOOK_PRICE_6_ADDR := 0x0211CEDC

# songs
OVL094_ADDR := 0x021658A0
HOOK_SONGS_ADDR := 0x02171F34
HOOK_SONGS_FLAG_ADDR := 0x02172078 # prevents WDST actor from setting the song flag

# constants patch: item give (31), shops (36) and freestandings (70, 71)
PATCH_OVL_ARG := "{31: [0x020D9840], 36: [0x0211B148, 0x0211B420, 0x0211B6F8, 0x0211B9E8, 0x0211BCB0, 0x0211C02C], 70: [0x02142140], 71: [0x0215FF3C]}"
else
$(error "Region not supported: $(REGION)")
endif

OVLGZ_SIZE := 0x10000
HOOKS_SIZE := 0x1E0
RESERVED_SIZE := 0x10

# compiler settings
CFLAGS_BASE := -marm -mthumb-interwork -march=armv5te -mtune=arm946e-s -nostdlib -nodefaultlibs -nostartfiles
CC := arm-none-eabi-gcc $(CFLAGS_BASE)
CXX := arm-none-eabi-g++ $(CFLAGS_BASE)
WARNINGS := -Wall -Wno-multichar -Wno-unknown-pragmas -Wno-strict-aliasing -Wno-unused-variable
INCLUDES := -I include -I $(STGZ_DECOMP_DIR)/include -I $(STGZ_DECOMP_DIR)/libs/c/include -I $(STGZ_DECOMP_DIR)/libs/cpp/include -I $(STGZ_DECOMP_DIR)/libs/nitro/include -I $(STGZ_DECOMP_DIR)/libs/nns/include -I $(STGZ_DECOMP_DIR)/libs/runtime/include
CPP_DEFINES := -DGZ_OVL_ID=114 -DPACKAGE_VERSION='$(PACKAGE_VERSION)' -DPACKAGE_NAME='$(PACKAGE_NAME)' -DPACKAGE_COMMIT_AUTHOR='$(PACKAGE_COMMIT_AUTHOR)' -DPACKAGE_AUTHOR='$(PACKAGE_AUTHOR)' -DVERSION=$(VERSION)
CFLAGS := -Os -fno-short-enums -fomit-frame-pointer -ffast-math -fno-builtin -fshort-wchar -MMD -MP $(WARNINGS) $(INCLUDES) $(CPP_DEFINES)
CPP_FLAGS := $(CFLAGS) -fno-rtti -fno-exceptions -fno-threadsafe-statics -std=c++2c

ELF := $(BUILD_DIR)/ovgz.elf
BIN := $(ELF:.elf=.bin)
MAP := $(ELF:.elf=.map)
LD := $(CC)
LDFLAGS := -T libs/ovgz.ld -Llibs -lst-$(REGION) -Wl,-Map,$(MAP) -specs=nosys.specs -Wl,--gc-sections -Wl,--defsym=OVLGZ_ADDR=$(OVLGZ_ADDR) -Wl,--defsym=OVLGZ_SIZE=$(OVLGZ_SIZE) -Wl,--defsym=RESERVED_SIZE=$(RESERVED_SIZE)
OBJCOPY := tools/binutils/arm-none-eabi-objcopy

HOOKS_ELF := $(HOOKS_BUILD_DIR)/hooks.elf
HOOKS_BIN := $(HOOKS_ELF:.elf=.bin)
HOOKS_MAP := $(HOOKS_ELF:.elf=.map)
HOOKS_LD := $(CC)
HOOKS_LDFLAGS := -T hooks/hooks.ld -Llibs -lst-$(REGION) -lgz -specs=nosys.specs -Wl,--gc-sections

HOOKS_GAME_ELF := $(HOOKS_BUILD_DIR)/game.elf
HOOKS_GAME_BIN := $(HOOKS_GAME_ELF:.elf=.bin)
HOOKS_GAME_MAP := $(HOOKS_GAME_ELF:.elf=.map)

# create output directories
$(shell $(MKDIR) -p $(BUILD_DIR)/src/overlays)
$(shell $(MKDIR) -p $(BUILD_DIR)/src/thumb)
$(shell $(MKDIR) -p $(HOOKS_BUILD_DIR)/src)

### project settings ###

EXTRACT_DIR := extract
EXTRACTED_DIR := $(EXTRACT_DIR)/$(REGION)
BASEROM := $(EXTRACT_DIR)/baserom_st_$(REGION).nds
ARM7_BIOS ?= $(EXTRACT_DIR)/arm7_bios.bin

ifeq ($(OUT_HASH),1)
OUT_ROM := stgz-$(REGION)-$(PACKAGE_VERSION).nds
else
OUT_ROM := stgz-$(REGION).nds
endif
OUT_PPF := $(OUT_ROM:.nds=.ppf)

EXTRACTED_REL := ../../../$(EXTRACTED_DIR)
ARMIPS_ARGS ?= \
				-strequ OVL018_BIN "$(EXTRACTED_REL)/arm9_overlays/ov018.bin" \
				-strequ OVL018_MOD_BIN "$(EXTRACTED_REL)/arm9_overlays/ov018_mod.bin" \
				-strequ OVL036_BIN "$(EXTRACTED_REL)/arm9_overlays/ov036_patched.bin" \
				-strequ OVL036_MOD_BIN "$(EXTRACTED_REL)/arm9_overlays/ov036_mod.bin" \
				-strequ OVL094_BIN "$(EXTRACTED_REL)/arm9_overlays/ov094.bin" \
				-strequ OVL094_MOD_BIN "$(EXTRACTED_REL)/arm9_overlays/ov094_mod.bin" \
				-strequ ARM9_BIN "$(EXTRACTED_REL)/arm9/arm9_patched.bin" \
				-strequ ARM9_MOD_BIN "$(EXTRACTED_REL)/arm9/arm9_mod.bin" \
				-strequ ITCM_BIN "$(EXTRACTED_REL)/arm9/itcm.bin" \
				-strequ ITCM_MOD_BIN "$(EXTRACTED_REL)/arm9/itcm_mod.bin" \
				-equ OVL018_ADDR $(OVL018_ADDR) \
				-equ OVL036_ADDR $(OVL036_ADDR) \
				-equ OVL094_ADDR $(OVL094_ADDR) \
				-equ HOOKS_SIZE $(HOOKS_SIZE) \
				-equ HOOKS_ADDR $(HOOKS_ADDR) \
				-equ HOOKS_GAME_ADDR $(HOOKS_GAME_ADDR) \
				-equ HOOK_UPDATE $(HOOK_UPDATE) \
				-equ HOOK_INIT $(HOOK_INIT) \
				-equ HOOK_SONGS $(HOOK_SONGS_ADDR) \
				-equ HOOK_SONGS_FLAG $(HOOK_SONGS_FLAG_ADDR) \
				-equ HOOK_PRICE_1 $(HOOK_PRICE_1_ADDR) \
				-equ HOOK_PRICE_2 $(HOOK_PRICE_2_ADDR) \
				-equ HOOK_PRICE_3 $(HOOK_PRICE_3_ADDR) \
				-equ HOOK_PRICE_4 $(HOOK_PRICE_4_ADDR) \
				-equ HOOK_PRICE_5 $(HOOK_PRICE_5_ADDR) \
				-equ HOOK_PRICE_6 $(HOOK_PRICE_6_ADDR)

### project targets ###

all: $(OUT_ROM) infos

build: hooks
	$(call print_no_args,Patching the game...)
	$(V)$(ROM_PATCHER) -e $(EXTRACTED_DIR) -o $(OBJ) -m $(OVLGZ_SIZE) -j $(HOOKS_OBJ) -n $(HOOKS_SIZE) -a $(OVLGZ_ADDR) -d $(HOOKS_BUILD_DIR) --elf $(ELF) --map $(MAP) --hooks_bin $(HOOKS_BIN) --hooks_elf $(HOOKS_ELF) --hooks_game_bin $(HOOKS_GAME_BIN) --patch_ovl $(PATCH_OVL_ARG)
	$(call print_no_args,Applying hooks and adding new code...)
	$(V)$(ARMIPS) $(HOOKS_BUILD_DIR)/setup.asm $(ARMIPS_ARGS)
	$(call print_no_args,Success!)

clean:
	$(V)$(RM) -r $(BUILD_DIR) $(HOOKS_BUILD_DIR)
	$(V)$(RM) $(OUT_ROM)
	$(call print_no_args,Success!)

distclean: clean
	$(V)$(RM) -r $(EXTRACTED_DIR)
	$(call print_no_args,Success!)

extract:
	$(call print_no_args,Extracting the rom...)
	$(V)$(DSROM) extract --rom $(BASEROM) --path $(EXTRACTED_DIR) --arm7-bios $(ARM7_BIOS)
	$(call print_no_args,Success!)

hooks: overlay $(HOOKS_BIN) $(HOOKS_GAME_BIN)

init: venv
	$(call print_no_args,Verifying baserom checksum...)
ifeq ($(COMPARE),1)
	$(V)sha1sum -c $(EXTRACT_DIR)/baserom_st_$(REGION).sha1
endif
	$(V)$(DL_TOOL) -p tools/ dsrom v0.7.0
	$(V)$(DL_TOOL) -p tools/ binutils arm-2.42-0
ifeq ("$(wildcard $(ARMIPS_DIR))", "")
	$(error armips not found!)
else
ifeq ("$(wildcard $(ARMIPS_DIR)/out)", "")
	$(call print_no_args,Building armips...)
	$(V)$(MKDIR) $(ARMIPS_DIR)/out && cd $(ARMIPS_DIR)/out && $(CMAKE) -DCMAKE_BUILD_TYPE=Release .. && $(CMAKE) --build .
endif
endif
	$(call print_no_args,Building PPF3 tools...)
	$(V)$(MAKE) -C tools/ppf

infos:
	$(call print_no_args,Success!)
	@$(PRINT) "==== Build Options ====$(NO_COL)\n"
	@$(PRINT) "${GREEN}Game Region: $(BLUE)$(REGION)$(NO_COL)\n"
	@$(PRINT) "${GREEN}Rom Path: $(BLUE)$(OUT_ROM) ($(OUT_PPF))$(NO_COL)\n"
	@$(PRINT) "${GREEN}Code Version: $(BLUE)$(PACKAGE_VERSION)$(NO_COL)\n"
	@$(PRINT) "${GREEN}Build Author: $(BLUE)$(PACKAGE_AUTHOR)$(NO_COL)\n"
	@$(PRINT) "${GREEN}Commit Author: $(BLUE)$(PACKAGE_COMMIT_AUTHOR)$(NO_COL)\n"
	@$(PRINT) "${BLINK}Build succeeded.\n$(NO_COL)"

libs:
	$(call print_no_args,Generating game symbol library...)
	$(V)$(PYTHON) tools/gen_libs.py -m libst -d $(STGZ_DECOMP_DIR)
	$(call print_no_args,Success!)

overlay: $(BIN)
	$(call print_no_args,Generating stgz symbol library...)
	$(V)$(PYTHON) tools/gen_libs.py -m libgz -e $(ELF)
	$(call print_no_args,Success!)

patch: $(OUT_ROM)
	$(call print_no_args,Creating PPF patch...)
	$(V)$(MAKEPPF3) c "$(BASEROM)" "$(OUT_ROM)" "$(OUT_PPF)"
	$(V)$(MAKE) infos

run: all
ifeq ($(STGZ_EMULATOR),)
	$(error "Emulator path not set.")
endif
	$(STGZ_EMULATOR) $(OUT_ROM)

setup: extract

test_no_logic: build
	$(call print_no_args,Randomizing items...)
	$(V)$(PYTHON) rando/test/test_no_logic.py
	$(V)$(MAKE) $(OUT_ROM)

venv:
# Create the virtual environment if it doesn't exist.
# Delete the virtual environment directory if creation fails.
	$(call print_no_args,Creating python virtual environment...)
	$(V)test -d $(VENV) || python3 -m venv $(VENV) || { rm -rf $(VENV); false; }
	$(V)$(PYTHON) -m pip install -U pip
	$(V)$(PYTHON) -m pip install -U -r tools/requirements.txt
	$(call print_no_args,Success!)

.PHONY: all build clean distclean extract hooks init infos libs patch overlay run setup test_no_logic venv

### misc project recipes ###

# add dependencies
-include $(ALL_DEPS)

## process auto-generated thumb definitions (necessary to avoid crashes when calling thumb functions) ##

$(BUILD_DIR)/src/thumb/thumb-$(REGION).o: src/thumb/thumb-$(REGION).s
	$(V)$(CC) $(CFLAGS) -fverbose-asm -Os -x assembler-with-cpp -fomit-frame-pointer -c "$<" -o "$@"

## process source files ##

$(BUILD_DIR)/src/%.o: src/%.s
	$(call print_two_args,Assembling:,$<,$@)
	$(V)$(CC) $(CFLAGS) -fverbose-asm -Os -x assembler-with-cpp -fomit-frame-pointer -c "$<" -o "$@"

$(BUILD_DIR)/src/%.o: src/%.c
	$(call print_two_args,Compiling:,$<,$@)
	$(V)$(CC) $(CFLAGS) -c "$<" -o "$@"

$(BUILD_DIR)/src/%.o: src/%.cpp
	$(call print_two_args,Compiling:,$<,$@)
	$(V)$(CXX) $(CPP_FLAGS) -c "$<" -o "$@"

$(HOOKS_BUILD_DIR)/src/%.o: hooks/src/%.c
	$(call print_two_args,Compiling hooks:,$<,$@)
	$(V)$(CC) $(CFLAGS) -DOVERLAY_0_SLOT_ADDR=$(OVERLAY_0_SLOT_ADDR) -c "$<" -o "$@"

$(HOOKS_BUILD_DIR)/src/%.o: hooks/src/%.cpp
	$(call print_two_args,Compiling hooks:,$<,$@)
	$(V)$(CXX) $(CPP_FLAGS) -c "$<" -o "$@"

## process build artifacts ##

$(ELF): $(OBJ)
	$(call print_one_arg,Linking:,$@)
	$(V)$(LD) -o $@ $^ $(LDFLAGS)

$(BIN): $(ELF)
	$(call print_two_args,Wrapping binary to ELF:,$<,$@)
	$(V)$(OBJCOPY) -S -O binary $< $@
	$(V)$(CP) $@ $(EXTRACTED_DIR)/arm9_overlays/ovgz.bin

$(HOOKS_ELF): $(HOOKS_OBJ)
	$(call print_one_arg,Linking hooks:,$@)
	$(V)$(LD) -o $@ $^ $(HOOKS_LDFLAGS) -Wl,-Map,$(HOOKS_MAP) -Wl,--defsym=HOOKS_ADDR=$(HOOKS_ADDR)

$(HOOKS_BIN): $(HOOKS_ELF)
	$(call print_two_args,Wrapping hooks binary to ELF:,$<,$@)
	$(V)$(OBJCOPY) -S -O binary $< $@

$(HOOKS_GAME_ELF): $(HOOKS_GAME_OBJ)
	$(call print_one_arg,Linking hooks:,$@)
	$(V)$(LD) -o $@ $^ $(HOOKS_LDFLAGS) -Wl,-Map,$(HOOKS_GAME_MAP) -Wl,--defsym=HOOKS_ADDR=$(HOOKS_GAME_ADDR)

$(HOOKS_GAME_BIN): $(HOOKS_GAME_ELF)
	$(call print_two_args,Wrapping hooks binary to ELF:,$<,$@)
	$(V)$(OBJCOPY) -S -O binary $< $@

$(OUT_ROM): build
	$(call print_one_arg,Assembling the rom:,$@)
	$(V)$(DSROM) build --config $(EXTRACTED_DIR)/config.yaml --rom $@ --arm7-bios $(ARM7_BIOS)
