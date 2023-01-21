from __future__ import annotations

import os
import pathlib
import shutil
from io import FileIO
import zipfile
from abc import ABC, abstractmethod

from ... import jsqp_core_logger, LoggerAdapter
from .file_types import FileTypes
from ...errors import PackageAlreadyExist
from ...paths import Paths

class Package(): #TODO: Might make this into a dataclass.
    """The base class for a package."""
    def __init__(self, name:str):
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

class FilePackage(Package):
    """A package represented as an actual file."""
    def __init__(self, path_to_file:str):
        self.__path_to_file = path_to_file
        self.logger = LoggerAdapter(jsqp_core_logger, "FilePackage")

        super().__init__("UwUDummyName")

        self.__file = self.open_file(path_to_file)

    # Abstract methods
    # ------------------
    @property
    @abstractmethod
    def install_location(self) -> str:
        """Returns the path this package want's to be installed to."""
        return Paths().jsqp_core_appdata_dir + "/packages"
    
    # Other attributes
    # -------------------
    @property
    def path(self) -> str:
        """Returns the path of this package."""
        return self.__path_to_file

    @property
    def full_path(self) -> str:
        """Returns the full path location of this package."""
        return os.path.abspath(self.__path_to_file)

    @property
    def file(self) -> FileIO|None:
        """Returns the file object of this package. Returns none if it doesn't exist."""
        return self.__file

    @property
    def file_name(self) -> str|None:
        """Returns file name even if the file object is unavailable."""
        if self.file is None:
            return os.path.split(self.full_path)[1]

        return os.path.split(self.file.name)[1]

    def file_rename(self, new_name:str):
        """Renames the package's file. You got to also include file extension here."""
        os.rename(self.full_path, os.path.split(self.full_path)[0] + new_name)
        return True
        
    def open_file(self, path_to_file:str) -> None|FileIO:
        self.logger.debug(f"Checking if file exists...")
        if os.path.exists(path_to_file):
            if self.file_type == FileTypes.FOLDER:
                self.logger.debug(f"'{self.name}' is a folder so the file object will be None and file name will be referred to as actual package name.")
                return None
            
            self.logger.debug(f"Opening and reading file at '{os.path.abspath(path_to_file)}'...")
            file = open(path_to_file, "r")
            file.close()
            return file

        self.logger.error(f"File package at '{os.path.abspath(path_to_file)}' cannot be found.")
        return None
    
    def move(self, move_to_path:str, overwrite_if_exist:bool=False) -> bool:
        """Allows you to move this file package to another location. Raises ``FileNotFoundError`` if path or file does not exist."""
        new_file_path = f"{move_to_path}/{os.path.split(self.full_path)[1]}"

        if os.path.exists(new_file_path):
            if overwrite_if_exist:
                old_package = FilePackage(new_file_path)
                old_package.delete()
            else:
                raise PackageAlreadyExist(self, new_file_path)

        self.logger.info(f"Moving '{self.file_name}' to '{new_file_path}'...")
        shutil.move(self.full_path, move_to_path)

        # Update path
        self.__path_to_file = move_to_path

        self.logger.info(f"Moved to '{move_to_path}'!")
        return True

    def zip(self, zip_name:str=None) -> bool:
        """Turn file package into a zip if it is a folder."""
        if zip_name is None:
            zip_name = self.name + ".zip"

        if self.file_type == FileTypes.FOLDER:
            self.logger.info(f"Getting directory files of '{self.file_name}'...")
            directory = pathlib.Path(self.full_path)

            zip_name = (lambda x: x if x[-4:] == ".zip" else (x + ".zip"))(zip_name)
            path_to_zip = self.full_path.replace(os.path.split(self.path)[-1], zip_name)

            self.logger.info(f"Zipping {self.file_name} to '{path_to_zip}'...")
            
            # Zipping each file in directory.
            # --------------------------------
            with zipfile.ZipFile(path_to_zip, mode="w") as archive:
                for file_path in directory.iterdir():
                    #TODO: Change this to set the texture pack folder as the root folder of zip.
                    archive.write(file_path, arcname=file_path.name)
                    self.logger.debug(f"Zipped '{file_path}'.") #TODO: Find a way to print every file being zipped.
            
            # Updating path and file object.
            self.__path_to_file = path_to_zip
            self.__file = self.open_file(path_to_zip)

            return True

        if self.file_type == FileTypes.ZIP:
            self.logger.warn(f"'{self.file_name}' is already a zip so no need to zip it.")
            return False

        self.logger.error(f"'{self.file_name}' can't be zipped because it isn't a folder/directory.")
        return False

    def delete(self) -> bool:
        """Completely deletes the package with it's file."""
        self.logger.info(f"Deleting '{self.name}' at '{self.full_path}'...")
        os.remove(self.full_path)
        self.logger.debug(f"'{self.full_path}' deleted!")
        return True

    @property
    def file_type(self) -> FileTypes|None:
        """Returns the type of the actual file. Is it a folder? Is it a file?"""
        
        if os.path.isfile(self.__path_to_file):
            if os.path.splitext(self.__path_to_file)[-1] == ".zip":
                return FileTypes.ZIP
            else:
                return FileTypes.FILE
        if os.path.isdir(self.__path_to_file):
            return FileTypes.FOLDER
        if os.path.islink(self.__path_to_file):
            return FileTypes.SYMBOLIC_LINK

        return None