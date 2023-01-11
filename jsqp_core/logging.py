import os
import sys

import logging as log

# Logging module stuff
# -----------------------
class JSQPCustomFormatter(log.Formatter):
    if sys.platform == "win32": os.system("color")

    pink_grey = "\u001b[38;5;139m"
    clay = "\u001b[38;5;51m"
    grey = "\u001b[38;20m"
    yellow = "\u001b[33;20m"
    red = "\u001b[31;20m"
    bold_red = "\u001b[31;1m"
    reset = "\u001b[0m"
    
    format = "[%(levelname)s]\u001b[0m (%(name)s) - %(message)s"

    FORMATS = {
        log.DEBUG: pink_grey + format,
        log.INFO: clay + format,
        log.WARNING: yellow + format,
        log.ERROR: red + format,
        log.CRITICAL: bold_red + format
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = log.Formatter(log_fmt)
        return formatter.format(record)

class LoggerAdapter(log.LoggerAdapter):
    def __init__(self, logger:log.Logger, prefix:str):
        super().__init__(logger, {})
        self.prefix = prefix

    def process(self, msg, kwargs):
        return f"\u001b[92m[{self.prefix}]\u001b[0m {msg}", kwargs

# Method for adding custom handler to any logger object.
# -------------------------------------
def add_custom_handler(logger:log.Logger) -> log.Logger:
    stream_handler = log.StreamHandler()
    stream_handler.setLevel(log.DEBUG)
    stream_handler.setFormatter(JSQPCustomFormatter())

    logger.propagate = False
    logger.addHandler(stream_handler)

    return logger