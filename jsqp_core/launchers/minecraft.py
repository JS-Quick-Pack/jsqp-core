"""
This is the module that handles the Official Microsoft Minecraft Launcher at https://www.xbox.com/en-GB/games/store/minecraft-launcher/9PGW18NPBZV5.

Adds support to the Launcher on Windows and Linux (only tested on Fedora 38 KDE via flatpak).
ONLY java edition is currently supported.

WIKI: https://minecraft.fandom.com/wiki/Minecraft_Launcher
"""

from . import Launcher, LauncherInfo

class Minecraft(Launcher):
    """The official microsoft minecraft launcher."""
    def __init__(self) -> None:
        super().__init__(
            LauncherInfo(
                display_name = "Minecraft Launcher",
                homepage = "https://www.xbox.com/en-GB/games/store/minecraft-launcher/9PGW18NPBZV5",
                developer = "Microsoft"
            )
        )