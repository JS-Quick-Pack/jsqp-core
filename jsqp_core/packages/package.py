from __future__ import annotations

from devgoldyutils import LoggerAdapter

from ..logger import core_logger

__all__ = ("Package",)

class Package():
    """The base class of all packages."""
    def __init__(self, name: str):
        self.__name = name

        self.logger = LoggerAdapter(core_logger, "Package")

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        self.logger.debug(f"Updated package name to '{value}'!")