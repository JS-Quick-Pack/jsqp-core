from __future__ import annotations
from typing import TYPE_CHECKING

import os
import shutil
import hashlib
from enum import Enum
from pathlib import Path
from zipfile import ZipFile
from abc import abstractmethod, ABC
from devgoldyutils import LoggerAdapter

if TYPE_CHECKING:
    from io import BufferedReader

from ..paths import Paths
from .package import Package
from .. import errors, config
from ..logger import core_logger

__all__ = ("FileTypes", "FilePackage")

class FileTypes(Enum):
    """Enum of all the supported file types."""
    FILE = 0
    FOLDER = 1
    SYMBOLIC_LINK = 2
    ZIP = 3

class FilePackage(Package, ABC):
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
    def display_name(self) -> str:
        """Returns the display name of this package."""
        ...

    @property
    @abstractmethod
    def package_install_path(self) -> str:
        """Location of where this package is supposed to be installed. NOT the actual installed location."""
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
    def file(self) -> BufferedReader | None:
        """Returns the file object of this package. Returns none if this package isn't a file."""
        if self.__path.is_file():
            return open(str(self.__path), "rb")

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

    @property
    def hash(self) -> str | None:
        """Returns the hash of the package's file. Returns None if self.file is none."""
        file = self.file

        if file is not None:
            md5 = hashlib.md5()

            with file as f:
                md5.update(f.read())

            return md5.hexdigest()

        return None

    def add(self, overwrite: bool = False):
        """Adds the package to your jsqp storage."""
        self.logger.info(f"Adding '{self.display_name}' to jsqp 📦 storage...")

        # Zip it if it's not already a zip.
        if self.type == FileTypes.FOLDER:
            self.zip(self.name + ".zip")

        # Move the package to JSQPCore install location directory.

        if not os.path.exists(self.package_install_path):
            Paths().repair_app_data_dir([self.package_install_path])

        try:
            self.move(
                self.package_install_path, overwrite, config.no_copy
            )
        except FileExistsError:
            raise errors.PackageAlreadyExist(self)

    def link_to(self, location: str, file_name: str = None, overwrite: bool = False) -> None:
        """Method that creates a symbolic link of the package in that location."""
        self.logger.debug("Creating symbolic link...")

        if file_name is None:
            file_name = self.display_name + self.path.suffix

        target_location = location + f"/{file_name}"

        if os.path.exists(target_location) and overwrite:
            os.remove(target_location)

        try:
            os.link(self.path.absolute(), target_location)
            self.logger.debug(f"Created symbolic link '{self.name}' at '{location}'.")
        except FileExistsError:
            # TODO: We probably would want to overwrite it instead of causing an exception.
            self.logger.warning("Didn't create symbolic link as it already exists.")

    def move(self, path: str, overwrite: bool = False, no_copy: bool = True) -> None:
        """
        Allows you to move this file package to another location. 
        Raises ``FileNotFoundError`` if path does not exist and ``FileExistsError`` if a file already exists there.
        """
        new_path = f"{path}/{self.path.name}"
        self.logger.info(f"Moving '{self.display_name}' to '{os.path.split(new_path)[0]:.60}'...")

        if os.path.exists(new_path):

            if overwrite or config.overwrite:
                self.logger.info("Overwriting as it already exists...")
                shutil.rmtree(new_path, True) if os.path.isdir(new_path) else os.remove(new_path)

            else:
                raise FileExistsError("The file already exists.")

        shutil.copy2(self.path.absolute(), new_path)

        # Delete if the user only wants to copy the file.
        if no_copy is False:
            self.delete()

        # Update path
        self.path = Path(new_path)

        self.logger.info(f"Moved to '{new_path:.60}'!")

    def zip(self, zip_name: str = None) -> bool:
        """Turn file package into a zip if it is a folder."""
        if zip_name is None:
            zip_name = self.name + ".zip"

        if self.type == FileTypes.FOLDER:
            zip_name = (lambda x: x if x[-4:] == ".zip" else x + ".zip")(zip_name)
            path_to_zip = Path(str(self.path.parent) + f"/{zip_name}")

            self.logger.info(f"Zipping {self.display_name} to '{str(path_to_zip):.60}...'")

            with ZipFile(path_to_zip.absolute(), mode = "w") as archive:
                for file_path in self.path.rglob("*"):
                    archive.write(file_path, arcname = file_path.__str__().partition(self.path.name + os.path.sep)[2])

            self.logger.debug(f"Done zipping to '{path_to_zip.absolute()}'!")

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
        self.logger.info(f"Deleting '{self.display_name}' at '{os.path.split(absolute_path)[0]:.60}...'")

        if self.path.is_dir():
            shutil.rmtree(absolute_path, True)
        else:
            os.remove(absolute_path)

        self.logger.debug(f"'{absolute_path}' deleted!")
        return True