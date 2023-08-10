"""
A script used by us to compare texture pack file differences between two minecraft versions using the mappings available.
"""
import os
import sys
from pathlib import Path
from devgoldyutils import Colours

jsqp_dir = str(Path(os.path.split(__file__)[0]).parent)

sys.path.insert(0, jsqp_dir)

import json
from jsqp_core.logger import core_logger
from jsqp_core.packages.texture_pack import maps

MAPPINGS_PATH = os.path.split(maps.__file__)[0]


def get_map_files(map: dict):
    """Function that returns all files from a texture pack map as a list."""
    list = []

    for key, value in map.items():
        if key == "files":
            list.extend(value)
            continue

        list.extend(get_map_files(value))

    return list


try:
    mapping_1 = json.load(open(MAPPINGS_PATH + f"/{sys.argv[1]}.json"))
    mapping_2 = json.load(open(MAPPINGS_PATH + f"/{sys.argv[2]}.json"))

    mapping_1_files = set(get_map_files(mapping_1))
    mapping_2_files = set(get_map_files(mapping_2))

    added_files = mapping_2_files - mapping_1_files
    removed_files = mapping_1_files - mapping_2_files

    print(Colours.GREEN.apply("[added]:"), added_files)
    print(Colours.RED.apply("[removed]:"), removed_files)

except IndexError as e:
    core_logger.error(
        f"You dumb dumb, you forgot the enter minecraft version! ERROR -> {e}"
    )