import logging
from decouple import config
from devgoldyutils import add_custom_handler, Colours

core_logger = add_custom_handler(
    logger = logging.getLogger(f"{Colours.PINK_GREY}JSQP{Colours.RED}_{Colours.CLAY}CORE{Colours.RESET}"),
    level = logging.DEBUG if config("jsqp_debug", default = False) else logging.INFO
)
"""The jsqp core logger."""