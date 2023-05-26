"""
🟣 JS:QP Core, an open source minecraft package management library.
"""
import logging
from typing import Final
from devgoldyutils import add_custom_handler, Colours

core_logger = add_custom_handler(
    logger = logging.getLogger(f"{Colours.PINK_GREY}JSQP{Colours.RED}_{Colours.CLAY}CORE{Colours.RESET}"),
    level = logging.INFO
)
"""The jsqp core logger."""

# Clear the temporary directory.
from .utils.temp import clear_temp
clear_temp()


# Module imports
# ---------------
from .packages.texture_pack import TexturePack


__version__: Final[str] = "1.0dev1"