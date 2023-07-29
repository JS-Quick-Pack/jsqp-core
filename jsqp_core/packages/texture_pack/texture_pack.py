from __future__ import annotations

import time
from devgoldyutils import LoggerAdapter, Colours
from typing import TYPE_CHECKING, Tuple
from pathlib import Path

from ... import config
from ...logger import core_logger
from ...mc_versions import MCVersions
from ..file_package import FilePackage
from ...launchers.minecraft import Minecraft
from .parser import TexturePackParser

if TYPE_CHECKING:
    from .parser import MCMeta
    from ...launchers import Launcher

__all__ = ("TexturePack",)

class TexturePack(FilePackage):
    """
    Class that allows you to represent a file as a texture pack and install it to your minecraft game.
    """
    def __init__(self, path_to_texture_pack: str, minecraft_version: MCVersions | int = None):
        self.logger = LoggerAdapter(core_logger, "TexturePack")

        super().__init__(
            path_to_texture_pack
        )

        self.__mc_ver = minecraft_version

        self.parser = TexturePackParser(self)
        """The pack's parser class."""

        # Change path_to_file to actual texture pack root directory.
        self.path = Path(self.parser.root_path)

        # Name package to actual texture pack name.
        self.name = self.parser.actual_name

        self.logger.debug("Texture Pack Initialized!")

    @property
    def display_name(self) -> str:
        return "".join([x[1:] if not x[0] == self.name[0] else x for x in self.name.replace("  ", "").split("§")])

    @property
    def package_install_path(self) -> str:
        return super().package_install_path + "/texture_packs"

    @property
    def minecraft_version(self) -> int:
        """Returns the minecraft version this pack was made for."""
        if self.__mc_ver is not None:
            return self.__mc_ver.value if isinstance(self.__mc_ver, MCVersions) else self.__mc_ver # Might change this in the future. (make it valid versions only)

        return self.parser.version.value

    @property
    def mc_meta(self) -> MCMeta:
        """Returns a dictatory of the pack's .mcmeta file."""
        return self.parser.mc_meta
    
    @property
    def description(self) -> str | None:
        """Returns the pack's description from the .mcmeta file."""
        return self.parser.description

    @property
    def ___package_repr___(self) -> Tuple[str, dict]:
        return f"🖌️  {Colours.GREEN.apply('TexturePack')} = ", {
            "display_name": self.display_name, "mc_meta": self.mc_meta, "minecraft_version": self.minecraft_version
        }

    def install(self, launcher: Launcher = None, overwrite: bool = False, copy_it: bool = False):
        """
        Method that allows you to install this pack into your minecraft game.

        Defaults to Minecraft Java Edition.
        """
        if launcher is None: # Default launcher is the official minecraft launcher.
            launcher = Minecraft()
            self.logger.info(f"Launcher was not specified so I'm defaulting to '{launcher.display_name}'.")
            if not config.performance_mode: time.sleep(1.5) # Will probably remove this.

        start_time = time.perf_counter()

        launcher.install(self, overwrite)

        end_time = time.perf_counter()

        # TODO: We should probably move this to the launchers's base functions.
        self.logger.info(f"⌛ Installed '{self.name}' in {end_time - start_time:0.4f} seconds!")

    def remove(self):
        """Method that allows you to remove this pack from your minecraft game."""
        ...