"""
A script used by me to create texture pack json maps for the texture pack parser.
"""
import os
import sys
from pathlib import Path

jsqp_dir = str(Path(os.path.split(__file__)[0]).parent)
print(f"JSQP_DIR = {jsqp_dir}")

sys.path.insert(0, jsqp_dir)

import json
from jsqp_core import TexturePack, core_logger

try:
    pack = TexturePack(sys.argv[1])

    json.dump(pack.pack_parser.map, open(f"{pack.name}.json", mode="w"))

except IndexError as e:
    core_logger.error(
        f"You dumb dumb, you forgot the pack_path argument! ERROR -> {e}"
    )