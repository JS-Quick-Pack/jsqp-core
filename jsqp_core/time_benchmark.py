from __future__ import annotations
from typing import TYPE_CHECKING

import time

if TYPE_CHECKING:
    import logging

__all__ = ("TimeBenchmark",)

class TimeBenchmark():
    def __init__(self, msg: str, logger: logging.Logger) -> None:
        self.msg = msg
        self.logger = logger

        self.__start_time = None

    def start(self):
        """Starts a benchmark counter."""
        self.__start_time = time.perf_counter()

    def end(self, arg_1: str):
        """Ends the benchmark counter and displays the results."""
        self.logger.info(
            self.msg.format(arg_1, time.perf_counter() - self.__start_time)
        )

        self.__start_time = None