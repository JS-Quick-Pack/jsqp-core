from __future__ import annotations

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from ..packages import Package

@dataclass
class LauncherInfo:
    display_name: str
    homepage: str
    """Where you can download the Launcher."""
    developer: str
    """The company/individual/group behind the creation of this Launcher."""

class Launcher(ABC):
    """Base class for all launchers. More like an interface actually."""
    def __init__(self, info: LauncherInfo) -> None:
        self.info = info

        super().__init__()

    @property
    def display_name(self) -> str:
        """Display name of the Launcher."""
        return f"({self.info.developer}) {self.info.display_name}"

    @abstractmethod
    def install(self, package: Package, overwrite_if_exist: bool = False, performance_mode: bool = False) -> bool:
        """Method to install a package."""
        ...

    @abstractmethod
    def uninstall(self, package: Package, overwrite_if_exist: bool = False, performance_mode: bool = False) -> bool:
        """Method to uninstall a package."""
        ...