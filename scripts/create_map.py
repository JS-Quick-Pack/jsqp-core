"""
A script used by use to create json mapings of texture packs for the texture pack parser.
"""
import os
import sys
from pathlib import Path
from devgoldyutils import Colours

jsqp_dir = str(Path(os.path.split(__file__)[0]).parent)
print(Colours.PURPLE.apply(f"JSQP_DIR = {jsqp_dir}"))

sys.path.insert(0, jsqp_dir)

import json
from jsqp_core.logger import core_logger
from jsqp_core.packages import TexturePack

try:
    pack = TexturePack(sys.argv[1])
    json_name = pack.name

    try:
        json_name = sys.argv[2]
    except IndexError:
        pass

    json.dump(pack.parser.map, open(f"{json_name}.json", mode="w"))
    print(Colours.GREEN.apply("Done!"))

except IndexError as e:
    core_logger.error(
        f"You dumb dumb, you forgot the pack_path argument! ERROR -> {e}"
    )
