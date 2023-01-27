from .logging import add_custom_handler, log, LoggerAdapter

from .logging import JSQPCustomFormatter as C
JSQP_CORE_LOGGER_NAME = f"{C.pink_grey}JSQP{C.red}_{C.clay}CORE{C.reset}"

jsqp_core_logger = add_custom_handler(log.getLogger(JSQP_CORE_LOGGER_NAME)); jsqp_core_logger.setLevel(log.INFO)
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