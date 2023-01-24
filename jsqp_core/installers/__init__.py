from abc import ABC, abstractmethod

from ..objects.package import Package

class Installer(ABC):
    """Base class for installers. More like an interface actually."""
    def __init__(self, display_name) -> None:
        self.display_name = display_name
        super().__init__()

    def install(self, package:Package):
        """Method to install a package that should be overridden."""
        ...

from .minecraft_java import MinecraftJava