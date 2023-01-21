import time

from .package import FilePackage
from .. import minecraft
from .. import LoggerAdapter, jsqp_core_logger
from ..paths import Paths

class TexturePack(FilePackage):
    """Class that represents a minecraft texture pack file."""
    def __init__(self, path_to_file: str):
        self.tp_logger = LoggerAdapter(jsqp_core_logger, "TexturePack")

        super().__init__(path_to_file)

        #TODO: Detect if file is actually a texture pack.

    @property
    def install_location(self) -> str:
        return super().install_location + "/resource_packs"

    def install(self, overwrite=False):
        """Method that allows you to install this pack into your Minecraft Game."""
        #TODO: Change path dir to actual texture pack. (The detected directory/folder of the pack.)
        start_time = time.perf_counter()
        minecraft.Minecraft().install(self, overwrite_if_exist=overwrite) #TODO: Add argument to change installer and add installer base class.
        end_time = time.perf_counter()

        #TODO: I might change all of this later. (Might not have a pack install method anymore.)

        self.tp_logger.info(f"⌛ Installed '{self.name}' in {end_time - start_time:0.4f} seconds!")

    def remove(self):
        """Method that allows you to remove this pack from your game."""
        ...