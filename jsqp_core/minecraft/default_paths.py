from enum import Enum
from ..paths import Paths

paths = Paths()

class DefaultPaths(Enum):
    DOT_MINECRAFT = (paths.appdata_dir + "./minecraft")

    DOT_MINECRAFT_RPS = (DOT_MINECRAFT + "/resourcepacks")
    """Default .minecraft resource packs folder."""