import os
from decouple import config as env

class Config():
    """A wrapper for the jsqp-core config environment variables."""

    @property
    def performance_mode(self) -> bool:
        """
        When enabled some fancy stuff and extra debugging features are disabled like zip extraction logs in order to speed up performance.
        """
        return env("jsqp_performance", default = False)

    @performance_mode.setter
    def performance_mode(self, x: bool):
        os.environ["jsqp_performance"] = str(x).lower()

    @property
    def no_copy(self) -> bool:
        """When enabled files will be deleted after being moved instead of just copied."""
        return env("jsqp_no_copy", default = False)

    @no_copy.setter
    def no_copy(self, x: bool):
        os.environ["jsqp_no_copy"] = str(x).lower()