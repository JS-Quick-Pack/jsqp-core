from __future__ import annotations

import os
from io import FileIO

from file_types import FileTypes

class Package:
    """The base class for a package."""

    def __init__(self):
        pass

class FilePackage(Package):
    """A package represented as an actual file."""
    def __init__(self, path_to_file:str):
        self.__path_to_file = path_to_file

        self.__file = open(path_to_file, "r")
        super().__init__()

    @property
    def path(self) -> str:
        """Returns the path of this package."""
        return self.__path_to_file

    @property
    def file(self) -> FileIO:
        """Returns the file object of this package."""
        return self.__file
    
    def move(self, move_to_path:str):
        """Allows you to move this file to another location."""
        ...

    @property
    def file_type(self) -> FileTypes|None:
        """Returns the type of the actual file. Is it a folder? Is it a file?"""
        
        if os.path.isfile(self.__path_to_file):
            return FileTypes.FILE
        if os.path.isdir(self.__path_to_file):
            return FileTypes.FOLDER
        if os.path.islink(self.__path_to_file):
            return FileTypes.SYMBOLIC_LINK

        return None