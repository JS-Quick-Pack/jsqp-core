"""
This is the module that handles the Official Microsoft Minecraft Launcher at https://www.minecraft.net/en-us/download.

Adds support to the Launcher on Windows and Linux (only tested on Fedora 38 KDE via flatpak).
ONLY java edition is currently supported.

WIKI: https://minecraft.fandom.com/wiki/Minecraft_Launcher
"""
from __future__ import annotations

import os
import sys
import json
from typing import Tuple, final, TypedDict, Dict, TYPE_CHECKING, List
from devgoldyutils import Colours

from .. import errors
from ..paths import Paths
from ..packages import Package
from . import Launcher, LauncherInfo, LauncherNotFound

if TYPE_CHECKING:
    from ..packages.file_package import FilePackage

paths = Paths()

@final
class LauncherProfile(TypedDict):
    """Minecraft launcher profile dictatory."""
    created: str
    gameDir: str
    icon: str
    lastUsed: str
    lastVersionId: str
    name: str
    type: str

@final
class LauncherProfilesDict(TypedDict):
    profiles: Dict[str, LauncherProfile]
    settings: dict
    version: int

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

        self.info.display_name += f" [{dot_minecraft_dir[1]}]" # Append type to display name.

        self.dot_minecraft_dir = dot_minecraft_dir[0]
        """The directory where the launcher files are. (e.g profiles, etc)"""

    @property
    def launcher_profiles(self) -> LauncherProfilesDict:
        """Returns the dictionary from the launcher_profiles.json file."""
        file = open(self.dot_minecraft_dir + "/launcher_profiles.json", mode="r")
        json_dict = json.load(file)
        file.close()
        return json_dict

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
    
    def add_to_profiles(self, package: FilePackage, folder_name: str, profiles: List[LauncherProfile] = None, overwrite: bool = False) -> List[LauncherProfile]:
        """
        Method that adds a file package to the game profiles in the Minecraft Launcher.
        Returns the profiles that the package was added to.
        """
        if profiles is None:
            profiles = [self.launcher_profiles["profiles"][profile] for profile in self.launcher_profiles["profiles"]]

        for profile in profiles:
            name = profile.get("name") if not profile.get("name") == "" else profile.get("type").replace("-", " ").title()

            if profile["lastUsed"] == "1970-01-01T00:00:00.000Z": # Don't include profiles that have never been ran.
                self.logger.warning(f"Skipped '{name}' because that profile was never used/launched.")
                continue

            game_dir = profile.get("gameDir", self.dot_minecraft_dir)

            try:
                package.link_to(os.path.join(game_dir, folder_name), overwrite = overwrite)
                self.logger.info(f"Linked '{Colours.BLUE.apply(package.display_name)}' to game profile '{Colours.GREEN.apply(name)}' ✅")

            except FileNotFoundError:
                self.logger.error(
                    f"I can't find the '{folder_name}' folder for the profile '{name}', " \
                    "make sure you have set the correct game directory in profile settings."
                )


    def install(self, package: FilePackage, overwrite: bool = False) -> None:
        """Install the texture pack into """
        from ..packages.texture_pack import TexturePack

        if isinstance(package, TexturePack):
            package.add(overwrite) # TODO: idk about doing this here, also we will definitely have to keep track of the repo with some type of database or json files.

            # Link the texture pack to each minecraft launcher profile.
            self.add_to_profiles(
                package, 
                folder_name = "resourcepacks",
                overwrite = overwrite
            )

            return None

        raise errors.PackageNotSupported(package, self)

    def uninstall(self, package: Package, performance_mode: bool = False) -> bool:
        ...