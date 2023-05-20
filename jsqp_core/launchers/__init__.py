from abc import ABC, abstractmethod

class Launcher(ABC):
    """Base class for all launchers. More like an interface actually."""
    def __init__(self) -> None:
        super().__init__()

    @property
    @abstractmethod
    def display_name(self):
        """Display name of Launcher."""
        ...

    @abstractmethod
    def install(self, package: Package, overwrite_if_exist: bool = False, performance_mode: bool = False) -> bool:
        """Method to install a package."""
        ...

    @abstractmethod
    def uninstall(self, package: Package, overwrite_if_exist: bool = False, performance_mode: bool = False) -> bool:
        """Method to uninstall a package."""
        ...