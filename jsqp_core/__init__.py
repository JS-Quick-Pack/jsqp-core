"""
🟣 JS:QP Core, an open source minecraft package management library.
"""
import logging
from typing import Final
from devgoldyutils import add_custom_handler, Colours

from .configuration import Config
config = Config()

core_logger = add_custom_handler(
    logger = logging.getLogger(f"{Colours.PINK_GREY}JSQP{Colours.RED}_{Colours.CLAY}CORE{Colours.RESET}"),
    level = logging.DEBUG if config.debug_mode else logging.INFO
)
"""The jsqp core logger."""

# Clear the temporary directory.
from .utils.temp import clear_temp
clear_temp()

from .configuration import Config
config = Config()


# Module imports
# ---------------
from .mc_versions import MCVersions
from .packages.texture_pack import TexturePack, TexturePackParser


__version__: Final[str] = "1.0dev1"