from __future__ import annotations

import os
import sys

from .. import jsqp_core_logger, LoggerAdapter

class Paths():
    """Class containing methods for finding required paths."""

    def __init__(self):
        self.__platform = sys.platform

        self.logger = LoggerAdapter(jsqp_core_logger, "Paths")

        self.__create_dev_goldy_dir()

    @property
    def appdata_dir(self):
        if self.__platform == "win32":
            return os.getenv('APPDATA')
        elif self.__platform == "linux":
            return os.getenv("HOME")
        else:
            return None
            
    @property
    def dev_goldy_dir(self):
        """Returns path to DevGoldy appdata folder."""

        return (lambda x: x + "/.devgoldy" if not x is None else None)(self.appdata_dir)

    @property
    def jsqp_core_appdata_dir(self) -> str|None:
        """Returns path to jsqp core appdata folder."""

        return (lambda x: x + "/.devgoldy/JsqpCore" if not x is None else None)(self.appdata_dir)


    def __create_dev_goldy_dir(self):
        try:
            os.mkdir(self.dev_goldy_dir)
            self.logger.info(f"Created devgoldy directory at '{self.dev_goldy_dir}'.")
        except FileExistsError:
            self.logger.debug(f"Devgoldy directory already exist at '{self.dev_goldy_dir}'.")

        try:
            os.mkdir(self.jsqp_core_appdata_dir)
            self.logger.info(f"Created jsqp core directory at '{self.jsqp_core_appdata_dir}'.")
        except FileExistsError:
            self.logger.debug(f"Jsqp core directory already exist at '{self.jsqp_core_appdata_dir}'.")