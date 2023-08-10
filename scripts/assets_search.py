"""
A script used by us to search for assets in all minecraft versions.
"""
import os
import sys
from pathlib import Path
from devgoldyutils import Colours, pprint

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
    query = input(Colours.BLUE.apply("Query > ")) if len(sys.argv) < 2 else sys.argv[1]
    mappings = os.listdir(MAPPINGS_PATH)
    mappings.remove("__init__.py")
    mappings.remove("__pycache__")

    results = {}

    for map in mappings:
        version = map.removesuffix(".json")
        map_files = get_map_files(json.load(open(MAPPINGS_PATH + f"/{map}")))

        results[version] = []
        
        for file in map_files:

            if query.lower() in file:
                results[version].append(file)

    for result in results:
        print(f"> {Colours.PURPLE.apply(result)}: {results[result]}")

except IndexError as e:
    core_logger.error(
        f"You dumb dumb, you forgot the enter minecraft version! ERROR -> {e}"
    )