#!/usr/bin/env python3

from ndspy import bmg
from pathlib import Path
from rando.constants import ItemId, item_id_to_name


if __name__ == "__main__":
    msg_list = []

    RED = bmg.Message.Escape(255, b"\x00\x00\x01\x00")
    WHITE = bmg.Message.Escape(255, b"\x00\x00\x00\x00")
    INFO = b"\xCE\x00\x00\x01"

    for i in range(0, 117):
        prefix = "You got the "

        if i == ItemId.Nothing.value:
            prefix = "You got "

        msg_parts = [prefix, RED, item_id_to_name[i], WHITE, "!"]
        msg = bmg.Message(INFO, msg_parts)
        msg_list.append(msg)

    for i in range(0, 117):
        msg_parts = [RED, item_id_to_name[i], WHITE]
        msg = bmg.Message(INFO, msg_parts)
        msg_list.append(msg)

    bmg_file = bmg.BMG.fromMessages(msg_list, id=0x1F)
    bmg_file.saveToFile(Path("extract/eur/files/English/Message/rando.bmg").resolve())
