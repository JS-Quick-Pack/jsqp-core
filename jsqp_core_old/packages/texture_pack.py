from __future__ import annotations

import time
from devgoldyutils import LoggerAdapter

from .. import jsqp_core_logger

from ..utils.texture_packs.texture_pack_parser import TexturePackParser
from ..objects.mc_versions import MCVersions
from ..objects.package import FilePackage
from ..installers import Installer
from .. import MinecraftJava

class TexturePack(FilePackage):
    """
    Class that allows you to represent a file as a texture pack and install it to your minecraft game.
    """
    def __init__(self, path_to_texture_pack: str, mc_version:MCVersions|int=None):
        self.tp_logger = LoggerAdapter(jsqp_core_logger, "TexturePack")

        super().__init__(
            path_to_texture_pack, package_name = "Nameless Texture Pack"
        )

        self.pack_parser = TexturePackParser(self)

        # Set/Detect minecraft version.
        # --------------------------------
        self.__mc_version = None
        if not mc_version is None:
            if isinstance(mc_version, MCVersions):
                self.__mc_version = mc_version.value
            else:
                self.__mc_version = mc_version
        else:
            #TODO: Detect the minecraft version!
            pass

        # Change path_to_file to actual texture pack root directory.
        self.update_path(self.pack_parser.root_path)

        # Name package to actual texture pack name.
        self.update_name(self.pack_parser.actual_name)

    @property
    def install_location(self) -> str:
        return super().install_location + "/resource_packs"

    @property
    def mc_version(self) -> int|None:
        """Returns the minecraft version this pack was made for."""
        return self.__mc_version

    def install(self, installer:Installer = None, overwrite:bool = False, performance_mode:bool = False, copy_it:bool = False):
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

        installer.install(self, overwrite_if_exist=overwrite, performance_mode=performance_mode, copy_it=copy_it)

        end_time = time.perf_counter()

        self.tp_logger.info(f"⌛ Installed '{self.name}' in {end_time - start_time:0.4f} seconds!")

    def remove(self):
        """Method that allows you to remove this pack from your game."""
        ...