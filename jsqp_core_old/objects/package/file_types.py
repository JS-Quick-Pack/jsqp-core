from enum import Enum

class FileTypes(Enum):
    """Enum of all the supported file types."""
    FILE = 0
    FOLDER = 1
    SYMBOLIC_LINK = 2
    ZIP = 3