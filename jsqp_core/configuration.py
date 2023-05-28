import os
from decouple import config

class Config():
    """A wrapper for the jsqp-core config environment variables."""

    @property
    def performance_mode(self) -> bool:
        """
        When enabled some fancy stuff and extra debugging features are disabled like zip extraction logs in order to speed up performance.
        """
        return config("jsqp_performance", default = False)

    @performance_mode.setter
    def performance_mode(self, x: bool):
        os.environ["jsqp_performance"] = str(x).lower()


    @property
    def debug_mode(self) -> bool:
        """When enabled more things are logged to console."""
        return config("jsqp_debug", default = False)

    @performance_mode.setter
    def debug_mode(self, x: bool):
        os.environ["jsqp_debug"] = str(x).lower()


    @property
    def no_copy(self) -> bool:
        """When enabled files will be deleted instead of copied appropriately when moving."""
        return config("jsqp_no_copy", default = False)

    @no_copy.setter
    def debug_mode(self, x: bool):
        os.environ["jsqp_no_copy"] = str(x).lower()