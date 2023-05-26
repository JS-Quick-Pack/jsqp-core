import shutil
from ..paths import Paths

from .. import core_logger

def clear_temp():
    """Function that clears the temp folder JSQPCore creates to temporary store stuff."""
    shutil.rmtree(Paths().temp_dir, True)
    core_logger.debug("Cleared temp dir.")