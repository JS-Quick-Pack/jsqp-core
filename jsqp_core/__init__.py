"""
🟣 JS:QP Core, an open source minecraft package management library.
"""
import logging
from typing import Final
from devgoldyutils import add_custom_handler, Colours

core_logger = add_custom_handler(
    logger = logging.getLogger(f"{Colours.PINK_GREY}JSQP{Colours.RED}_{Colours.CLAY}CORE"),
    level = logging.INFO
)
"""The jsqp core logger."""

# Module imports
# ---------------


__version__: Final[str] = "1.0dev1"