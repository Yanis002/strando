import struct
import random

from dataclasses import dataclass
from ndspy import lz10 as LZSS
from ndspy import narc
from pathlib import Path

lzss_file = Path("rando/map00.bin").resolve()
assert lzss_file.exists()

narc_bytes = LZSS.decompressFromFile(lzss_file)
narc_file = lzss_file.with_suffix(".narc")
narc_file.write_bytes(narc_bytes)
archive = narc.NARC.fromFile(narc_file)

found_file = None
filename = None
for i, file in enumerate(archive.files):
    if file.startswith(b"BPAM"):
        found_file = file
        filename = archive.filenames[i]
        break

assert found_file is not None and filename is not None
print("found:", filename)

base_offset = found_file.index(b"BOPM")
start_offset = base_offset + 0x0C
magic, size, count, unk_0A = struct.unpack_from('<4sIHh', found_file, base_offset)

@dataclass
class MapObjectEntry:
    id: str # u32
    tile_x: int # u8
    tile_y: int # u8
    angle: int # u16
    params: list[int] # u8[4]
    unk_0C: int # undetermined
    unk_10: int # undetermined
    unk_14: int # undetermined
    unk_18: int # undetermined

    raw_data: bytes

    def __post_init__(self):
        assert self.raw_data == self.to_bytes()

    @staticmethod
    def from_bytes(data: bytes):
        raw_id, raw_x, raw_y, raw_angle, raw_param1, raw_param2, raw_param3, raw_param4, raw_unk_0C, raw_unk_10, raw_unk_14, raw_unk_18 = struct.unpack_from("<4sBBHBBBBIIII", data)
        return MapObjectEntry(
            raw_id[::-1].decode(),
            raw_x,
            raw_y,
            raw_angle,
            [raw_param1, raw_param2, raw_param3, raw_param4],
            raw_unk_0C,
            raw_unk_10,
            raw_unk_14,
            raw_unk_18,
            data[:0x1C],
        )

    def to_bytes(self):
        return struct.pack(
            "<4sBBHBBBBIIII",
            self.id[::-1].encode(),
            self.tile_x,
            self.tile_y,
            self.angle,
            self.params[0],
            self.params[1],
            self.params[2],
            self.params[3],
            self.unk_0C,
            self.unk_10,
            self.unk_14,
            self.unk_18,
        )

entries: list[MapObjectEntry] = []
offset = start_offset
for i in range(count):
    entries.append(MapObjectEntry.from_bytes(found_file[offset:]))
    offset += 0x1C

old_data = b"".join(entry.to_bytes() for entry in entries)

picked_items = []
for entry in entries:
    if entry.id == "TRES":
        random_item = random.randint(1, 116)
        while random_item in picked_items:
            random_item = random.randint(1, 116)

        entry.params[0] = random_item
        picked_items.append(random_item)

new_data = b"".join(entry.to_bytes() for entry in entries)
assert len(new_data) == len(old_data), f"{len(new_data)}, {len(old_data)}"

found_file = found_file.replace(old_data, new_data)
archive.setFileByName(filename, found_file)
archive.saveToFile(Path("rando/test.narc"))
LZSS.compressToFile(archive.save(), lzss_file.with_name("map00_mod.bin"))
