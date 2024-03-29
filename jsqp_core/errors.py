from __future__ import annotations

from devgoldyutils import Colours
from .logger import core_logger

import pathlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .packages.package import Package
    from .launchers import Launcher

class JSQPCoreError(Exception):
    """Raises whenever there's a known error in jsqp core."""
    def __init__(self, message: str):
        core_logger.critical(message)
        super().__init__(Colours.RED.apply(message))

class PackageAlreadyExist(JSQPCoreError):
    def __init__(self, package: Package):
        super().__init__(
            f"The package '{package.name}' already exists! " \
            "Although you can ask me to overwrite it by setting the correct flags/parameters."
        )

class FilePackageDoesNotExist(JSQPCoreError):
    def __init__(self, path: pathlib.Path):
        super().__init__(
            f"'{str(path)}' does not exist. Are you sure you typed the path correctly."
        )

class PackageNotSupported(JSQPCoreError):
    """Raises whenever a package is not supported by an installer."""
    def __init__(self, package: Package, launcher: Launcher):
        super().__init__(
            f"'{package.__class__.__name__}()' is not supported in the '{launcher.__class__.__name__}()' installer. " \
            "Hence '{package.name}' can't be installed."
        )

class OSNotSupported(JSQPCoreError):
    """Raises when the OS is not supported."""
    def __init__(self):
        super().__init__(
            "Only Linux and Windows are supported right now. " \
            "If you would like for your OS to be supported contribute to the project: https://github.com/JS-Quick-Pack/jsqp-core"
        )