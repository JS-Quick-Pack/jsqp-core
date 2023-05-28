"""
This is the module that handles the Official Microsoft Minecraft Launcher at https://www.minecraft.net/en-us/download.

Adds support to the Launcher on Windows and Linux (only tested on Fedora 38 KDE via flatpak).
ONLY java edition is currently supported.

WIKI: https://minecraft.fandom.com/wiki/Minecraft_Launcher
"""

import os
import sys
from typing import Tuple

from .. import errors
from ..packages import Package
from ..paths import Paths
from . import Launcher, LauncherInfo, LauncherNotFound

paths = Paths()

class Minecraft(Launcher):
    """The official microsoft minecraft launcher."""
    def __init__(self, dot_minecraft_dir: Tuple[str, str] = None) -> None:
        super().__init__(
            LauncherInfo(
                id = "minecraft",
                display_name = "Minecraft Launcher",
                homepage_link = "https://www.minecraft.net/en-us/download",
                developer = "Microsoft"
            )
        )

        # Find the goddam minecraft launcher.
        # -------------------------------------
        if dot_minecraft_dir is None:
            dot_minecraft_dir = self.find_launcher()

        self.info.display_name += f" [{dot_minecraft_dir[1]}]" # Append to display name.

        self.dot_minecraft_dir = dot_minecraft_dir[0]
        """The directory where the launcher files are. (e.g profiles, etc)"""

    def install(self, package: Package, overwrite: bool = False) -> None:
        """Install the texture pack into """
        from ..packages.texture_pack import TexturePack

        if isinstance(package, TexturePack):
            package.add()

            return


        raise errors.PackageNotSupported(package, self)

    def uninstall(self, package: Package, performance_mode: bool = False) -> bool:
        ...

    def find_launcher(self) -> Tuple[str, str]:
        """Method that tries to find the minecraft launcher on your os and returns the path and type of installation."""
        if sys.platform == "win32": # For the windows normies. You know literally 90% of players.
            return paths.appdata_dir + "/.minecraft", "official"

        elif sys.platform == "linux": # For the Linux nerds like me. 🤓
            normal_install = paths.appdata_dir + "/.minecraft"
            flatpak_install = paths.appdata_dir + "/.var/app/com.mojang.Minecraft/.minecraft"

            if os.path.exists(normal_install):
                return normal_install, "normal"
            elif os.path.exists(flatpak_install):
                return flatpak_install, "flatpak"

        raise LauncherNotFound(self)