from .package import FilePackage
from .. import minecraft

class TexturePack(FilePackage):
    """Class that represents a minecraft texture pack file."""
    def __init__(self, path_to_file: str):
        super().__init__(path_to_file)

    def install(self):
        """Method that allows you to install this pack into your Minecraft Game."""
        minecraft.Minecraft().install(self)

    def remove(self):
        """Method that allows you to remove this pack from your game."""
        ...