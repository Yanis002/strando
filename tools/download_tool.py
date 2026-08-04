#!/usr/bin/env python3

import argparse
import io
import os
import requests
import stat
import zipfile

from pathlib import Path
from get_platform import get_platform


if __name__ == "__main__":
    root_path = Path(__file__).parent.parent

    parser = argparse.ArgumentParser()
    parser.add_argument("tool")
    parser.add_argument("tag")
    parser.add_argument("--path", "-p", type=Path, required=True)
    parser.add_argument("--system", "-s", type=str.lower, required=False)
    args = parser.parse_args()

    platform = get_platform()
    if platform is None:
        exit(1)

    system = args.system if args.system is not None else platform.system
    exe = platform.exe if args.system is None else ".exe" if args.system == "windows" else ""

    def dsdrom_url(tag: str) -> str:
        return f"https://github.com/AetiasHax/ds-rom/releases/download/{tag}/dsrom-{system}-{platform.machine}{exe}"

    def binutils_url(tag: str) -> str:
        return f"https://github.com/Yanis002/mips-binutils/releases/download/{tag}/{system}-{platform.machine}.zip"

    def flips_url(tag: str) -> str:
        return f"https://github.com/Yanis002/Flips/releases/download/{tag}/flips-{system}.zip"

    TOOLS = {
        "dsrom": dsdrom_url,
        "binutils": binutils_url,
        "flips": flips_url,
    }

    download_url = TOOLS[args.tool](args.tag)
    print(f"Downloading {args.tool} {args.tag}...")
    response = requests.get(download_url)

    if download_url.endswith(".zip"):
        out_path: Path = args.path / args.tool
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        zip_file.extractall(out_path)

        for dirpath, dirnames, filenames in os.walk(out_path):
            dir_path = Path(dirpath).resolve()

            for file in filenames:
                cur_path = dir_path / file
                cur_path.chmod(cur_path.stat().st_mode | stat.S_IEXEC)
    else:
        out_path: Path = args.path / f"{args.tool}{'.exe' if args.system is not None and args.system == 'windows' else ''}"
        with out_path.open("wb") as f:
            f.write(response.content)
        out_path.chmod(out_path.stat().st_mode | stat.S_IEXEC)
