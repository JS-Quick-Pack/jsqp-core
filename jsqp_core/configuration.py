import os
from decouple import AutoConfig

class Config():
    """A wrapper for the jsqp-core config environment variables."""
    def __init__(self) -> None:
        self.env = AutoConfig(".")

    @property
    def no_copy(self) -> bool:
        """When enabled files will be deleted after being moved instead of just copied."""
        return self.env("JSQP_NO_COPY", default = False)

    @no_copy.setter
    def no_copy(self, x: bool):
        os.environ["JSQP_NO_COPY"] = str(x).lower()

    @property
    def overwrite(self) -> bool:
        """When enabled file that already exist will be overwritten while moving or copying."""
        return self.env("JSQP_OVERWRITE", default = False)

    @overwrite.setter
    def overwrite(self, x: bool):
        os.environ["JSQP_OVERWRITE"] = str(x).lower()

    @property
    def test_all_versions(self) -> bool:
        """When enabled texture packs will be tested against all minecraft versions during version detection."""
        return self.env("JSQP_TEST_ALL_VERSIONS", default = False)

    @test_all_versions.setter
    def test_all_versions(self, x: bool):
        os.environ["JSQP_TEST_ALL_VERSIONS"] = str(x).lower()