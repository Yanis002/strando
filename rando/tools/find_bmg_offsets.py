#!/usr/bin/env python3
import yaml

from pathlib import Path

# from https://github.com/yaml/pyyaml/issues/127#issuecomment-525800484
class MyDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()

if __name__ == "__main__":
    languages = [
        "English",
        "French",
        "German",
        "Italian",
        "Spanish",
    ]

    data = {}
    for lang in languages:
        bmg_dir = Path("extract").resolve() / "eur" / "files" / lang / "Message"

        data[lang] = {}
        for bmg_file in bmg_dir.rglob("*.bmg"):
            bmg_data = bmg_file.read_bytes()

            try:
                data[lang][bmg_file.stem + bmg_file.suffix] = f"0x{bmg_data.index(b"FLW1"):X}"
            except ValueError:
                pass

    with Path("rando/data/bmg/flw1_offsets.yaml").open("w") as file:
        yaml.dump(data, file, Dumper=MyDumper)
