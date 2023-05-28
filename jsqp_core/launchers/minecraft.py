"""
This is the module that handles the Official Microsoft Minecraft Launcher at https://www.minecraft.net/en-us/download.

Adds support to the Launcher on Windows and Linux (only tested on Fedora 38 KDE via flatpak).
ONLY java edition is currently supported.

WIKI: https://minecraft.fandom.com/wiki/Minecraft_Launcher
"""

import os
import sys
from typing import Tuple

from jsqp_core.packages import Package
from ..paths import Paths
from . import Launcher, LauncherInfo, LauncherNotFound

paths = Paths()

class Minecraft(Launcher):
    """The official microsoft minecraft launcher."""
    def __init__(self, launcher_directory: Tuple[str, str] = None) -> None:
        self.game_directory = None
        """The directory where the actual game files are. (e.g. logs, resourcepacks, saves)"""
        
        # Find the goddam minecraft launcher.
        # -------------------------------------
        if launcher_directory is None:
            launcher_directory = self.find_launcher()

        self.launcher_directory = launcher_directory
        """The directory where the launcher files are. (e.g profiles, etc)"""

        super().__init__(
            LauncherInfo(
                id = "minecraft",
                display_name = f"Minecraft Launcher [{launcher_directory[1]}]",
                homepage_link = "https://www.minecraft.net/en-us/download",
                developer = "Microsoft"
            )
        )

    def install(self, package: Package, overwrite_if_exist: bool = False, performance_mode: bool = False) -> bool:
        ...

    def uninstall(self, package: Package, overwrite_if_exist: bool = False, performance_mode: bool = False) -> bool:
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

        raise LauncherNotFound("Check out", self)
