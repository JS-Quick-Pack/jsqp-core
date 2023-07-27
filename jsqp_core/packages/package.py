from __future__ import annotations
from typing import Tuple

from io import StringIO
from devgoldyutils import LoggerAdapter, Colours, pprint

from ..logger import core_logger

__all__ = ("Package",)

class Package():
    """The base class of all packages."""
    def __init__(self, name: str):
        self.__name = name

        self.logger = LoggerAdapter(core_logger, "Package")

        super().__init__()

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self.logger.debug(f"Updated package name to '{value}'!")

    @property
    def ___package_repr___(self) -> Tuple[str, dict]:
        return f"📦  {Colours.ORANGE.apply(self.__class__.__name__)} = ", {"name": self.name}
    
    def __str__(self) -> str:
        prefix, attributes = self.___package_repr___

        stream = StringIO()
        pprint(
            attributes, 
            stream = stream
        )
        stream.seek(0)

        return prefix + stream.read()