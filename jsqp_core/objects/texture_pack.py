import time

from .package import FilePackage
from ..installers import Installer, Minecraft
from .. import LoggerAdapter, jsqp_core_logger

class TexturePack(FilePackage):
    """Class that represents a minecraft texture pack file."""
    def __init__(self, path_to_file: str):
        self.tp_logger = LoggerAdapter(jsqp_core_logger, "TexturePack")

        #TODO: Change path_to_file to actual texture pack folder. (The detected directory/folder of the pack.)
        #TODO: Detect if file is actually a texture pack.

        super().__init__(path_to_file)

    @property
    def install_location(self) -> str:
        return super().install_location + "/resource_packs"

    def install(self, installer:Installer=None, overwrite=False):
        """Method that allows you to install this pack into your Minecraft Game."""
        if installer is None: # Default installer.
            installer = Minecraft()

        start_time = time.perf_counter()

        installer.install(self, overwrite_if_exist=overwrite) #TODO: Add argument to change installer and add installer base class.

        end_time = time.perf_counter()

        self.tp_logger.info(f"⌛ Installed '{self.name}' in {end_time - start_time:0.4f} seconds!")

    def remove(self):
        """Method that allows you to remove this pack from your game."""
        ...