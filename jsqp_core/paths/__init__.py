from __future__ import annotations

import os
import sys
from typing import List

from .. import jsqp_core_logger, LoggerAdapter
from ..errors import OSNotSupported

class Paths():
    """Class containing methods for finding required paths."""

    def __init__(self):
        self.__platform = sys.platform

        self.logger = LoggerAdapter(jsqp_core_logger, "Paths")

        # Creates APPDATA directory if it doesn't exist.
        # ----------------------------------------------
        if not os.path.exists(self.jsqp_core_appdata_dir):
            self.repair_app_data_dir()

    @property
    def appdata_dir(self):
        if self.__platform == "win32":
            return os.getenv('APPDATA')
        elif self.__platform == "linux":
            return os.getenv("HOME")
        else:
            raise OSNotSupported()
            
    @property
    def dev_goldy_dir(self) -> str:
        """Returns path to DevGoldy appdata folder."""
        return f"{self.appdata_dir}/.devgoldy"

    @property
    def jsqp_core_appdata_dir(self) -> str:
        """Returns path to jsqp core appdata folder."""
        return f"{self.dev_goldy_dir}/JSQPCore"

    def repair_app_data_dir(self, more_paths_to_repair:List[str]=[]):
        self.logger.info(f"Creating/repairing appdata dir at '{self.jsqp_core_appdata_dir}'...")

        os.makedirs(self.jsqp_core_appdata_dir, exist_ok=True)

        for path in more_paths_to_repair:
            self.logger.debug(f"Repairing '{path}'...")
            os.makedirs(path, exist_ok=True)

        self.logger.info(f"Done creating/repairing appdata dir!")