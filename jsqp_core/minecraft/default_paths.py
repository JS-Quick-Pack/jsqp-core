from enum import Enum
from ..paths import Paths

paths = Paths()

class DefaultPaths(Enum):
    DOT_MINECRAFT = (paths.appdata_dir + "./minecraft")

    JSQP_INSTALL_PATH = (paths.jsqp_core_appdata_dir + "/packages")