"""
🟣 JS:QP Core, an open source minecraft package management library.

Copyright (c) 2023-present Goldy
"""
from typing import Final, Tuple

# Clear the temporary directory.
from .utils.temp import clear_temp
clear_temp() # TODO: We need to change this.

from .configuration import Config
config = Config()

__all__: Final[Tuple[str]] = ("config",)
__version__: Final[str] = "1.0dev2"