from __future__ import annotations
from typing import TYPE_CHECKING

from PIL import Image
from dataclasses import dataclass, field
from devgoldyutils import LoggerAdapter, Colours, short_str

if TYPE_CHECKING:
    from .texture_pack import TexturePack

from ...logger import core_logger

__all__ = ("TexturePackAssets",)

@dataclass()
class TexturePackAsset:
    image_path: str
    model_path: str

    image: Image.Image = field(init=False)
    """The image of this asset."""
    model: dict = field(init=False)
    """The 3D model of this asset."""

    def __post_init__(self):
        self.image = Image.open(self.image_path)

class TexturePackAssets():
    """Class used to allow all the assets in a texture pack to be programmatically accessible."""
    def __init__(self, texture_pack: TexturePack) -> None:
        self.texture_pack = texture_pack

        self.logger = LoggerAdapter(
            LoggerAdapter(core_logger, self.__class__.__name__), prefix = Colours.PINK_GREY.apply(short_str(texture_pack.name))
        )

    @property
    def iron_door_bottom(self) -> TexturePackAsset:
        ...