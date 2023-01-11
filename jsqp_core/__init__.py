from .logging import add_custom_handler, log, LoggerAdapter

from .logging import JSQPCustomFormatter as C
JSQP_CORE_LOGGER_NAME = f"{C.pink_grey}JSQP{C.red}_{C.clay}CORE{C.reset}"

jsqp_core_logger = add_custom_handler(log.getLogger(JSQP_CORE_LOGGER_NAME)); jsqp_core_logger.setLevel(log.INFO)
"""The logger object for jsqp core."""

# Useful objects.
# -----------------
from .objects.package import FilePackage

from .objects.texture_pack import TexturePack