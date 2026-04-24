# st-rando

The Legend of Zelda: Spirit Tracks randomizer prototype.

**IMPORTANT**: this project doesn't provide any protected IPs, users are required to provide the necessary files by their own means and we won't help anyone in this regard.

## Patching

To apply a PPF patch, you need to follow the following steps:
- Go to [RomPatcher.js](https://www.marcrobledo.com/RomPatcher.js/) by Marc Robledo.
- In the "ROM file" field, open the path to the baserom. Make sure the sha1 hash match one of [these](extract/README.md).
- In the "Patch file" field, open the path to the PPF patch (from the releases or by running `make patch`).
- Click on "Apply Patch".

Note: you need to use a baserom corresponding to the region indicated in the filename of the PPF patch.

## Building

You will need the following packages/tools:
- `git`
- `make`
- `cmake`
- `gcc-arm-none-eabi` ([arch-based users](https://aur.archlinux.org/packages/gcc-arm-none-eabi-bin), [debian-based users](https://launchpad.net/ubuntu/+source/gcc-arm-none-eabi))

Steps:
- Place a baserom in the `extract` folder and name it `baserom_st_REGION.nds`, `REGION` being `eur`, `us` or `jp` (Note: only the european version is supported currently).
- `git submodule update --init --recursive`
- `make init`
- `make setup`
- `make`

## Contributing

Any help is welcome!

If you wish to help on this project, clone the repo then follow the build instructions.

**Warning**: if you're altering decomp symbols in any way, make sure to run `make libs` to generate the new symbol libraries and the asm files inside `src/thumb`.

## Project Structure

- `.github/workflows/`: hosts the actions workflows
- `extract/`: the folder where the rom will be extracted to
- `hooks/`: root directory for hooks source code
- `include/`: root directory for source code headers
- `libs/`: hosts libraries and symbol libraries generated from `make libs`, for use by the linker
- `resources/`: for general resources and also external projects that aren't tools
- `src/`: root directory for stgz source code
- `src/thumb/`: hosts the generated thumb assembly files for thumb compatibility when calling such functions from the game
- `tools/`: various programs, python scripts and misc files

## Credits

Referenced projects:
- [ds-rom](https://github.com/AetiasHax/ds-rom), made by Aetias.
- [armips](https://github.com/Kingcom/armips), made by Kingcom and many contributors.
- [PPF](https://github.com/meunierd/ppf), made by Icarus/Paradox.

Made with ♥ by me.
