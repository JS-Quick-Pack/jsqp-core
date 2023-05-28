from __future__ import annotations

import os
import shutil
from zipfile import ZipFile
from io import FileIO
from enum import Enum
from pathlib import Path
from abc import abstractmethod
from devgoldyutils import LoggerAdapter

from . import Package
from .. import core_logger, errors, config
from ..paths import Paths


class FileTypes(Enum):
    """Enum of all the supported file types."""
    FILE = 0
    FOLDER = 1
    SYMBOLIC_LINK = 2
    ZIP = 3

class FilePackage(Package):
    """A package represented as an actual file."""
    def __init__(
        self, 
        path: str | Path, 
    ):
        self.logger = LoggerAdapter(core_logger, "FilePackage")

        if isinstance(path, str):
            path = Path(path)

        if not path.exists():
            raise errors.FilePackageDoesNotExist(path)
        
        # If package is a zip, extract it into a temp folder and open that as path.
        if path.is_file() and path.suffix == ".zip":
            self.logger.debug("Extracting zip to temp directory...")
            temp_path = Paths().temp_dir + f"/{path.name[:-4]}"

            ZipFile(path.absolute()).extractall(temp_path)

            path = Path(temp_path)

        self.__path = path

        super().__init__(
            path.name if path.is_file() else os.path.split(path.absolute())[1]
        )

    @property
    @abstractmethod
    def install_location(self) -> str:
        """Returns the jsqp install location for this file package."""
        return Paths().jsqp_core_appdata_dir + "/packages"

    @property
    def path(self) -> Path:
        """Returns the path object of this package."""
        return self.__path
    
    @path.setter
    def path(self, value: Path | str):
        # We use setters here for the sole purpose of logging.
        self.__path = Path(value) if isinstance(value, str) else value
        self.logger.debug(f"Updated file package path object to '{str(value)}'!")

    @property
    def file(self) -> FileIO | None:
        """Returns the file object of this package. Returns none if this package isn't a file."""
        if self.__path.is_file():
            file = open(str(self.__path), "r")
            file.close()
            return file

        return None

    @property
    def type(self) -> FileTypes:
        """Returns the type of FilePackage. Is it a folder? Is it a file?"""

        if self.path.is_file():
            if self.path.suffix == ".zip":
                return FileTypes.ZIP

            return FileTypes.FILE
    
        elif self.path.is_dir():
            return FileTypes.FOLDER
        elif self.path.is_symlink():
            return FileTypes.SYMBOLIC_LINK
        
    def add(self):
        """Adds the package to the jsqp repository."""
        self.logger.info(f"Adding '{self.name}' to jsqp repository...")
        # Zip it if it's not already a zip.
        if self.type == FileTypes.FOLDER:
            self.zip(self.name + ".zip", config.performance_mode)

        # Move the package to JSQPCore install location directory.
        try:
            self.move(self.install_location, True, config.no_copy)
        except FileNotFoundError:
            # Repair and try again if file is not found.
            # -------------------------------------------
            Paths().repair_app_data_dir([
                self.install_location
            ])

            self.move(self.install_location, True, config.no_copy)
    
    def move(self, path: str, overwrite_if_exist: bool = False, copy_it: bool = False) -> None:
        """Allows you to move this file package to another location. Raises ``FileNotFoundError`` if path or file does not exist."""
        new_path = f"{path}/{self.path.name}"

        if os.path.exists(new_path):
            if overwrite_if_exist:
                FilePackage(new_path).delete()
            else:
                if copy_it is False: # Don't delete if I am asked to only copy the file while moving.
                    self.delete()

                raise errors.PackageAlreadyExist(self, new_path)

        self.logger.info(f"Moving '{self.path.name}' to '{new_path}'...")
        shutil.copy2(self.path.absolute(), new_path)

        # Delete if the user only doesn't want to copy the file.
        if copy_it is False:
            self.delete()

        # Update path
        self.path = Path(new_path)

        self.logger.info(f"Moved to '{new_path}'!")

    def zip(self, zip_name: str = None, performance_mode: bool = False) -> bool:
        """Turn file package into a zip if it is a folder."""
        if zip_name is None:
            zip_name = self.name + ".zip"

        if self.type == FileTypes.FOLDER:
            zip_name = (lambda x: x if x[-4:] == ".zip" else x + ".zip")(zip_name)
            path_to_zip = Path(str(self.path.parent) + f"/{zip_name}")

            self.logger.info(f"Zipping {self.path} to '{path_to_zip}'...")
            
            # Zipping each file in directory.
            # --------------------------------
            with ZipFile(path_to_zip.absolute(), mode = "w") as archive:

                if core_logger.level == 10 and performance_mode is False: # DEBUG MODE!
                    for file_path in self.path.rglob("*"):
                        archive.write(file_path, arcname = file_path.__str__().partition(self.path.name + os.path.sep)[2])
                        self.logger.debug(f"Zipped '{file_path.name}'.")
                
                else: # If debug logging level is not set we can zip much FASTER!
                    for file_path in self.path.rglob("*"):
                        archive.write(file_path, arcname = file_path.__str__().partition(self.path.name + os.path.sep)[2])

            self.logger.info(f"Done zipping to '{path_to_zip.absolute()}'!")
            
            # Updating path object.
            self.path = path_to_zip

            return True

        if self.type == FileTypes.ZIP:
            self.logger.warn(f"'{self.name}' is already a zip so no need to zip it.")
            return False

        self.logger.error(f"'{self.name}' can't be zipped because it isn't a folder/directory.")
        return False

    def delete(self) -> bool:
        """Completely deletes the package with it's file."""
        absolute_path = self.path.absolute()
        self.logger.info(f"Deleting '{self.name}' at '{absolute_path}'...")

        if self.path.is_dir():
            shutil.rmtree(absolute_path, True)
        else:
            os.remove(absolute_path)

        self.logger.debug(f"'{absolute_path}' deleted!")
        return True