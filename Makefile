MAKEFLAGS += --no-builtin-rules

# os-based file extension
ifeq ($(OS),Windows_NT)
EXE := .exe
else
EXE :=
endif

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
STRANDO_DECOMP_DIR ?= resources/decomp
STRANDO_EMULATOR ?=

# game region, only eur is supported atm
VERSION := eur

# region and region addresses
ifeq ($(VERSION),eur)
OVLRANDO_ADDR := 0x0218A380
HOOKS_ADDR := 0x01FFFE20
HOOKS_GAME_ADDR := 0x02013394

OVERLAY_0_SLOT_ADDR := 0x02043E50 # in reality this is the address of gOverlayManager
else
$(error Unsupported version $(VERSION))
endif

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
DSROM := tools/dsrom$(EXE)
DSROM_VERSION := v0.8.0

# armips setup
ARMIPS_DIR := tools/armips
ARMIPS ?= $(ARMIPS_DIR)/out/armips

# main source/objects
BUILD_DIR := build/$(VERSION)
ALL_FILES := $(sort $(shell find src/ -path "src/thumb" -prune -o -print))
ASM_FILES := $(filter %.s, $(ALL_FILES))
C_FILES := $(filter %.c, $(ALL_FILES))
CPP_FILES := $(filter %.cpp, $(ALL_FILES))
OBJ := $(foreach f,$(ASM_FILES),$(BUILD_DIR)/$(f:.s=.o)) $(foreach f,$(C_FILES),$(BUILD_DIR)/$(f:.c=.o)) $(foreach f,$(CPP_FILES),$(BUILD_DIR)/$(f:.cpp=.o)) $(BUILD_DIR)/src/thumb/thumb-$(VERSION).o
DEPS := $(foreach f,$(ASM_FILES),$(BUILD_DIR)/$(f:.s=.d)) $(foreach f,$(C_FILES),$(BUILD_DIR)/$(f:.c=.d)) $(foreach f,$(CPP_FILES),$(BUILD_DIR)/$(f:.cpp=.d))

# hooks source/objects
HOOKS_BUILD_DIR := hooks/build/$(VERSION)
HOOKS_SRC := $(wildcard hooks/src/*.c)
HOOKS_OBJ := $(foreach f,$(HOOKS_SRC:hooks/%=%),$(HOOKS_BUILD_DIR)/$(f:.c=.o))
HOOKS_DEPS := $(foreach f,$(HOOKS_SRC:hooks/%=%),$(HOOKS_BUILD_DIR)/$(f:.c=.d))
HOOKS_GAME_SRC := $(wildcard hooks/src/*.cpp)
HOOKS_GAME_OBJ := $(foreach f,$(HOOKS_GAME_SRC:hooks/%=%),$(HOOKS_BUILD_DIR)/$(f:.cpp=.o))
HOOKS_GAME_DEPS := $(foreach f,$(HOOKS_GAME_SRC:hooks/%=%),$(HOOKS_BUILD_DIR)/$(f:.cpp=.d))

ALL_DEPS := $(sort $(DEPS) $(HOOKS_DEPS) $(HOOKS_GAME_DEPS))

OVLRANDO_SIZE := 0x10000
HOOKS_SIZE := 0x1E0
RESERVED_SIZE := 0x10

# compiler settings
CFLAGS_BASE := -marm -mthumb-interwork -march=armv5te -mtune=arm946e-s -nostdlib -nodefaultlibs -nostartfiles
CC := arm-none-eabi-gcc $(CFLAGS_BASE)
CXX := arm-none-eabi-g++ $(CFLAGS_BASE)
WARNINGS := -Wall -Wno-multichar -Wno-unknown-pragmas -Wno-strict-aliasing -Wno-unused-variable -Wno-unused-but-set-variable -Wno-return-local-addr
INCLUDES := -I include -I $(STRANDO_DECOMP_DIR)/include -I $(STRANDO_DECOMP_DIR)/libs/c/include -I $(STRANDO_DECOMP_DIR)/libs/cpp/include -I $(STRANDO_DECOMP_DIR)/libs/nitro/include -I $(STRANDO_DECOMP_DIR)/libs/nns/include -I $(STRANDO_DECOMP_DIR)/libs/runtime/include
CPP_DEFINES := -DRANDO_OVL_ID=114 -DPACKAGE_VERSION='$(PACKAGE_VERSION)' -DPACKAGE_NAME='$(PACKAGE_NAME)' -DPACKAGE_COMMIT_AUTHOR='$(PACKAGE_COMMIT_AUTHOR)' -DPACKAGE_AUTHOR='$(PACKAGE_AUTHOR)' -DVERSION=$(VERSION)
CFLAGS := -Os -fno-short-enums -fomit-frame-pointer -ffast-math -fno-builtin -fshort-wchar -MMD -MP $(WARNINGS) $(INCLUDES) $(CPP_DEFINES)
CPP_FLAGS := $(CFLAGS) -fno-rtti -fno-exceptions -fno-threadsafe-statics -std=c++20 -Wno-volatile -Wno-overloaded-virtual # TODO: remove -Wno-overloaded-virtual once it's fixed in decomp

OVL_NAME := ovrando
ELF := $(BUILD_DIR)/$(OVL_NAME).elf
BIN := $(ELF:.elf=.bin)
MAP := $(ELF:.elf=.map)
LD := $(CC)
LDFLAGS := -T libs/$(OVL_NAME).ld -Llibs -lst-$(VERSION) -Wl,-Map,$(MAP) -Wl,--gc-sections -Wl,--defsym=OVLRANDO_ADDR=$(OVLRANDO_ADDR) -Wl,--defsym=OVLRANDO_SIZE=$(OVLRANDO_SIZE) -Wl,--defsym=RESERVED_SIZE=$(RESERVED_SIZE)
OBJCOPY := tools/binutils/arm-none-eabi-objcopy

HOOKS_ELF := $(HOOKS_BUILD_DIR)/hooks.elf
HOOKS_BIN := $(HOOKS_ELF:.elf=.bin)
HOOKS_MAP := $(HOOKS_ELF:.elf=.map)
HOOKS_LD := $(CC)
HOOKS_LDFLAGS := -T hooks/hooks.ld -Llibs -lst-$(VERSION) -lrando -Wl,--gc-sections

HOOKS_GAME_ELF := $(HOOKS_BUILD_DIR)/game.elf
HOOKS_GAME_BIN := $(HOOKS_GAME_ELF:.elf=.bin)
HOOKS_GAME_MAP := $(HOOKS_GAME_ELF:.elf=.map)

# create output directories
$(shell $(MKDIR) -p $(BUILD_DIR)/src/settings)
$(shell $(MKDIR) -p $(BUILD_DIR)/src/overlays)
$(shell $(MKDIR) -p $(BUILD_DIR)/src/thumb)
$(shell $(MKDIR) -p $(HOOKS_BUILD_DIR)/src)

### project settings ###

EXTRACT_DIR := extract
EXTRACTED_DIR := $(EXTRACT_DIR)/$(VERSION)
BASEROM := $(EXTRACT_DIR)/baserom_st_$(VERSION).nds
ARM7_BIOS ?= $(EXTRACT_DIR)/arm7_bios.bin

ifeq ($(OUT_HASH),1)
OUT_ROM := strando-$(VERSION)-$(PACKAGE_VERSION).nds
else
OUT_ROM := strando-$(VERSION).nds
endif

### project targets ###

all: $(OUT_ROM) infos

build: hooks
	$(call print_no_args,Patching the game...)
	$(V)$(ROM_PATCHER) --version $(VERSION) --address $(OVLRANDO_ADDR) --size $(OVLRANDO_SIZE) --elf $(ELF) --hooks_elf $(HOOKS_ELF) --hooks_game_bin $(HOOKS_GAME_BIN) --hooks_size $(HOOKS_SIZE) --hooks_addr $(HOOKS_ADDR) --hooks_game_addr $(HOOKS_GAME_ADDR)
	$(call print_no_args,Applying hooks and adding new code...)
	$(V)$(ARMIPS) $(HOOKS_BUILD_DIR)/setup.asm
	$(call print_no_args,Success!)

clean:
	$(V)$(RM) -r $(BUILD_DIR) $(HOOKS_BUILD_DIR)
	$(V)$(RM) $(OUT_ROM)
	$(call print_no_args,Success!)

distclean: clean
	$(V)$(RM) -r $(EXTRACTED_DIR)
	$(V)$(RM) src/settings/settings.bin
	$(call print_no_args,Success!)

extract:
	$(call print_no_args,Extracting the rom...)
	$(V)$(DSROM) extract --rom $(BASEROM) --path $(EXTRACTED_DIR) --arm7-bios $(ARM7_BIOS)
	$(call print_no_args,Success!)

hooks: overlay $(HOOKS_BIN) $(HOOKS_GAME_BIN)

init: venv
	$(call print_no_args,Verifying baserom checksum...)
ifeq ($(COMPARE),1)
	$(V)sha1sum -c $(EXTRACT_DIR)/baserom_st_$(VERSION).sha1
endif
	$(V)$(DL_TOOL) -p tools/ dsrom $(DSROM_VERSION)
	$(V)$(DL_TOOL) -p tools/ binutils arm-2.42-0
	$(V)$(DL_TOOL) -p tools/ flips v200
ifeq ("$(wildcard $(ARMIPS_DIR))", "")
	$(error armips not found!)
else
ifeq ("$(wildcard $(ARMIPS_DIR)/out/armips)", "")
	$(call print_no_args,Building armips...)
	$(V)$(MKDIR) -p $(ARMIPS_DIR)/out && cd $(ARMIPS_DIR)/out && $(CMAKE) -DCMAKE_BUILD_TYPE=Release .. && $(CMAKE) --build .
endif
endif

infos:
	$(call print_no_args,Success!)
	@$(PRINT) "==== Build Options ====$(NO_COL)\n"
	@$(PRINT) "${GREEN}Game Version: $(BLUE)$(VERSION)$(NO_COL)\n"
	@$(PRINT) "${GREEN}Rom Path: $(BLUE)$(OUT_ROM)$(NO_COL)\n"
	@$(PRINT) "${GREEN}Code Version: $(BLUE)$(PACKAGE_VERSION)$(NO_COL)\n"
	@$(PRINT) "${GREEN}Build Author: $(BLUE)$(PACKAGE_AUTHOR)$(NO_COL)\n"
	@$(PRINT) "${GREEN}Commit Author: $(BLUE)$(PACKAGE_COMMIT_AUTHOR)$(NO_COL)\n"
	@$(PRINT) "${BLINK}Build succeeded.\n$(NO_COL)"

libs:
	$(call print_no_args,Generating game symbol library...)
	$(V)$(PYTHON) tools/gen_libs.py -m libst -d $(STRANDO_DECOMP_DIR)
	$(call print_no_args,Success!)

overlay: $(BIN)
	$(call print_no_args,Generating strando symbol library...)
	$(V)$(PYTHON) tools/gen_libs.py -m librando -e $(ELF)
	$(call print_no_args,Success!)

patches: $(OUT_ROM)
	$(call print_no_args,Creating BPS patches...)
	$(V)$(PYTHON) tools/create_patches.py $(EXTRACTED_DIR)
	$(V)$(MAKE) infos

# copies the necessary files for the patcher into `rando/res/`
release: patches
	$(call print_no_args,Preparing release files...)
	$(V)$(CP) $(BIN) rando/res/$(OVL_NAME).bin
	$(V)$(CP) $(MAP) rando/res/$(OVL_NAME).map
	$(V)$(CP) -r tools/flips/ rando/res/flips/
	$(V)$(DL_TOOL) -p rando/res/ dsrom $(DSROM_VERSION) -s linux
	$(V)$(DL_TOOL) -p rando/res/ dsrom $(DSROM_VERSION) -s windows
	$(call print_no_args,Success!)

run: all
ifeq ($(STRANDO_EMULATOR),)
	$(error "Emulator path not set.")
endif
	$(STRANDO_EMULATOR) $(OUT_ROM)

setup: extract

test_no_logic:
	$(call print_no_args,Randomizing items...)
	$(V)$(PYTHON) rando/generator.py
	$(V)$(MAKE) $(OUT_ROM)

venv:
# Create the virtual environment if it doesn't exist.
# Delete the virtual environment directory if creation fails.
	$(call print_no_args,Creating python virtual environment...)
	$(V)test -d $(VENV) || python3 -m venv --system-site-packages $(VENV) || { rm -rf $(VENV); false; }
	$(V)$(PYTHON) -m pip install -U pip
	$(V)$(PYTHON) -m pip install -U -r tools/requirements.txt
	$(call print_no_args,Success!)

.PHONY: all build clean distclean extract hooks init infos libs patches overlay release run setup test_no_logic venv

### misc project recipes ###

# add dependencies
-include $(ALL_DEPS)

## process auto-generated thumb definitions (necessary to avoid crashes when calling thumb functions) ##

$(BUILD_DIR)/src/thumb/thumb-$(VERSION).o: src/thumb/thumb-$(VERSION).s
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
	$(V)$(CP) $@ $(EXTRACTED_DIR)/arm9_overlays/$(OVL_NAME).bin

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
