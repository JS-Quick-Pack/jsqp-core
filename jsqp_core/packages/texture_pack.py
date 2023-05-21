from __future__ import annotations

import time
from devgoldyutils import LoggerAdapter
from typing import TYPE_CHECKING
from pathlib import Path

from .. import core_logger, utils
from ..mc_versions import MCVersions
from .file_package import FilePackage
#from ..launchers.minecraft import Minecraft

if TYPE_CHECKING:
    from ..launchers import Launcher

# TODO: Do this next! 20/05/2023

class TexturePack(FilePackage):
    """
    Class that allows you to represent a file as a texture pack and install it to your minecraft game.
    """
    def __init__(self, path_to_texture_pack: str, mc_version: MCVersions | int = None):
        self.logger = LoggerAdapter(core_logger, "TexturePack")

        super().__init__(
            path_to_texture_pack
        )

        self.pack_parser = utils.TexturePackParser(self)

        # Set/Detect minecraft version.
        # --------------------------------
        if mc_version is not None:
            self.__mc_version = mc_version.value if isinstance(mc_version, MCVersions) else mc_version
        else:
            self.__mc_version = self.pack_parser.version

        # Change path_to_file to actual texture pack root directory.
        self.path = Path(self.pack_parser.root_path)

        # Name package to actual texture pack name.
        self.name = self.pack_parser.actual_name

        self.logger.debug("Initialized!")

    @property
    def install_location(self) -> str:
        return super().install_location + "/resource_packs"

    @property
    def mc_version(self) -> int | None:
        """Returns the minecraft version this pack was made for."""
        return self.__mc_version

    def install(self, launcher: Launcher = None, overwrite: bool = False, performance_mode: bool = False, copy_it: bool = False):
        """
        Method that allows you to install this pack into your minecraft game.

        Defaults to Minecraft Java Edition.
        """
        if launcher is None: # Default launcher is the official minecraft launcher.
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