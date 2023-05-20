from typing import Final
import logging
from devgoldyutils import add_custom_handler, Colours

JSQP_CORE_LOGGER_NAME = f"{Colours.PINK_GREY}JSQP{Colours.RED}_{Colours.CLAY}CORE{Colours.RESET}"

jsqp_core_logger = add_custom_handler(logging.getLogger(JSQP_CORE_LOGGER_NAME), level=logging.INFO)
"""The logger object for jsqp core."""

from .errors import *

#  Useful objects
# ----------------
from .objects.mc_versions import MCVersions


#  Installers
# ------------

# Minecraft Java Edition
# ------------------------
from .installers.minecraft_java import MinecraftJava

#  Packages
# -----------
from .packages.texture_pack import TexturePack


__version__: Final[str] = "1.0dev1"