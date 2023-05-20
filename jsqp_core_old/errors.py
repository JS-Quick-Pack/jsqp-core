from __future__ import annotations

from devgoldyutils import Colours
from . import jsqp_core_logger

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .installers import Installer
    from .objects.package import Package

class JSQPCoreError(Exception):
    """Raises whenever there's a known error in jsqp core."""
    def __init__(self, message: str):
        jsqp_core_logger.error(message)
        super().__init__(Colours.RED(message))

class PackageAlreadyExist(JSQPCoreError):
    def __init__(self, package: Package, location_where_it_exists: str):
        super().__init__(
            f"The package '{package.name}' already exists under '{location_where_it_exists}'! Although you can ask me to rename or overwrite it by setting the correct flags/parameters."
        )

class PackageNotSupported(JSQPCoreError):
    """Raises whenever a package is not supported by an installer."""
    def __init__(self, package: Package, installer: Installer):
        super().__init__(
            f"'{package.__class__.__name__}()' is not supported in the '{installer.__class__.__name__}()' installer. Hence '{package.name}' can't be installed."
        )

class OSNotSupported(JSQPCoreError):
    """Raises when the OS is not supported."""
    def __init__(self):
        super().__init__(
            "Only Linux and Windows are supported right now. If you would like for your OS to be supported contribute to the project here: https://github.com/JS-Quick-Pack/jsqp-core"
        )