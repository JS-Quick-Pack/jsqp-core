import os
import shutil
from ..paths import Paths

from .. import core_logger

paths = Paths()

def clear_temp():
    """Function that clears the temp folder JSQPCore creates to temporary store stuff."""
    if os.path.exists(paths.temp_dir):
        shutil.rmtree(paths.temp_dir, True)
        core_logger.debug("Cleared temp dir.")