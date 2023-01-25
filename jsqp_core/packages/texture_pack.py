import time

from .. import LoggerAdapter, jsqp_core_logger

from ..objects.package import FilePackage
from ..installers import Installer
from .. import MinecraftJava
from devgoldyutils.console import ConsoleColours

class TexturePack(FilePackage):
    """
    Class that allows you to represent a file as a texture pack and install it to a minecraft game.
    """
    def __init__(self, path_to_file: str):
        self.tp_logger = LoggerAdapter(jsqp_core_logger, "TexturePack")

        #TODO: Change path_to_file to actual texture pack directory.
        #TODO: Name package to actual texture pack name.

        super().__init__(path_to_file)

    @property
    def install_location(self) -> str:
        return super().install_location + "/resource_packs"

    def install(self, installer:Installer=None, overwrite:bool=False, performance_mode:bool=False):
        """
        Method that allows you to install this pack into your Minecraft Game.
        
        Defaults to Minecraft Java Edition.
        """
        if installer is None: # Default installer.
            installer = MinecraftJava()
            self.tp_logger.info(f"Installer was never specified so I'm defaulting to '{installer.display_name}'.")

        if (jsqp_core_logger.level == 10) and (performance_mode is False):
            self.tp_logger.warn(
                "\u001b[33;20mTexture packs will take longer to install because logging level is set to DEBUG! Please set logging level to info unless you know what you are doing.\u001b[0m"
            )

        start_time = time.perf_counter()

        installer.install(self, overwrite_if_exist=overwrite, performance_mode=performance_mode) #TODO: Add argument to change installer and add installer base class.

        end_time = time.perf_counter()

        self.tp_logger.info(f"⌛ Installed '{self.name}' in {end_time - start_time:0.4f} seconds!")

    def remove(self):
        """Method that allows you to remove this pack from your game."""
        ...