from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

from abc import ABC, abstractmethod
from dataclasses import dataclass
from devgoldyutils import LoggerAdapter
from ..logger import core_logger

if TYPE_CHECKING:
    from ..packages.package import Package

from ..errors import JSQPCoreError

__all__ = ("LauncherInfo", "LauncherNotFound", "Launcher")

@dataclass
class LauncherInfo:
    id: str
    """The id of this launcher."""
    display_name: str
    "The display name of the launcher."
    homepage_link: str
    """Url link to where you can download the Launcher."""
    developer: str
    """The company/individual/group behind the creation of this Launcher."""

class LauncherNotFound(JSQPCoreError):
    def __init__(self, launcher: Launcher):
        super().__init__(
            f"Could not find the launcher '{launcher.display_name}'." \
            f"\nCheck if we support your installation over here: https://github.com/JS-Quick-Pack/jsqp-core/blob/main/jsqp_core/launchers/{launcher.id}.md"
        )

class Launcher(ABC):
    """Base class for all launchers. More like an interface actually."""
    def __init__(self, info: LauncherInfo) -> None:
        self.info = info
        self.logger = LoggerAdapter(core_logger, prefix = info.display_name)

        super().__init__()

    @property
    def id(self) -> str:
        """Returns the launcher's ID."""
        return self.info.id

    @property
    def display_name(self) -> str:
        """Display name of the Launcher."""
        return f"({self.info.developer}) {self.info.display_name}"

    @abstractmethod
    def find_launcher(self) -> Tuple[str, str]:
        """
        Method that tries to locate the launcher on your OS and returns the path and installation type.
        Raises LauncherNotFound() exception if the launcher is not found.
        """
        ...

    @abstractmethod
    def install(self, package: Package, overwrite: bool = False) -> bool:
        """Method to install a package."""
        ...

    @abstractmethod
    def uninstall(self, package: Package) -> bool:
        """Method to uninstall a package."""
        ...