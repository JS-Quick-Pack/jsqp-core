from abc import ABC, abstractmethod

from ..objects.package import Package

class Installer(ABC):
    """Base class for installers. More like an interface actually."""
    def __init__(self, display_name) -> None:
        self.display_name = display_name
        super().__init__()

    @abstractmethod
    def install(self, package:Package, overwrite_if_exist:bool = False, performance_mode:bool = False, copy_it:bool = False) -> bool:
        """Method to install a package that should be overridden."""
        ...


from .minecraft_java import MinecraftJava