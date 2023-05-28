from __future__ import annotations

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from dataclasses import dataclass

if TYPE_CHECKING:
    from ..packages import Package

from ..errors import JSQPCoreError

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
            f"\nCheck if we support your installation over here: https://github.com/JS-Quick-Pack/jsqp-core/blob/feat/main/launchers/{launcher.info.id}.md"
        )

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