from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING
from devgoldyutils import LoggerAdapter

from ... import core_logger
from ...errors import JSQPCoreError

if TYPE_CHECKING:
    from ...packages.texture_pack import TexturePack
    from ...mc_versions import MCVersions

class AssetsFolderNotFound(JSQPCoreError):
    def __init__(self, texture_pack: TexturePack):
        super().__init__(
            f"The assets folder for the texture pack at '{texture_pack.path}' can't be found therefore this texture pack can't be phrased correctly!"
        )

class TexturePackParser():
    """Class used to detect the version and actual path of a minecraft java texture pack via the file structure."""
    def __init__(self, texture_pack: TexturePack) -> None:
        self.texture_pack = texture_pack

        self.logger = LoggerAdapter(core_logger, "TexturePackParser")

        self.__path_to_assets = ""
        """The path to the assets folder, this is automatically assigned by ``.__find_assets_folder()``."""

        assets_exist = next(self.__find_assets_folder(self.__get_folder_structure()), (False, None))[0]

        if not assets_exist:
            raise AssetsFolderNotFound(texture_pack)

        self.logger.info(f"Parsed the texture pack '{self.actual_name}'!")
    
    @property
    def actual_name(self) -> str | None:
        """Returns the actual name of the texture pack."""
        if self.root_path is None:
            return None
    
        return os.path.split(self.root_path)[1]

    @property
    def root_path(self) -> str:
        """Returns the real root path of this texture pack. E.g. where the ``assets``, ``pack.mcmeta`` and ``pack.png`` is stored."""
        return self.texture_pack.path + (lambda x: "" if x == "/" else x)(os.path.split(self.__path_to_assets)[0])

    @property
    def assets_path(self) -> str:
        return f"{self.texture_pack.path}/{os.path.split(self.__path_to_assets)[1]}"
    
    @property
    def version(self) -> MCVersions:
        """Returns the minecraft version this pack belongs to."""
        return self.detect_version()
    
    def detect_version() -> MCVersions:
        """Tries to detect the game version this pack was made for."""
        # TODO: the funny code.
        ...

    def __get_folder_structure(self) -> dict:
        """Returns the folder structure of this texture pack."""
        folder_structure = {}

        for foldername, sub_folders, filenames in os.walk(self.texture_pack.path):
            current_folder = folder_structure
            subfolder_list = foldername.split(os.path.sep)

            for subfolder in subfolder_list[1:]:
                if subfolder not in current_folder:
                    current_folder[subfolder] = {}
                current_folder = current_folder[subfolder]

            current_folder["files"] = filenames

        return folder_structure

    
    # Partly stolen from: https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-dictionaries-and-lists
    # ----------------------------------------------------------------------------------------------------------------------------
    def __find_assets_folder(self, folder_structure: dict):
        """
        Function that will walk into directory after directory to find the assets folder.
        """

        if hasattr(folder_structure, 'items'):

            for k, v in folder_structure.items():
                if not k == "files":
                    self.__path_to_assets += f"/{k}"

                if k == "assets":
                    yield True, self.__path_to_assets

                if isinstance(v, dict):
                    for result in self.__find_assets_folder(v):
                        yield result

                elif isinstance(v, list):
                    for d in v:
                        for result in self.__find_assets_folder(d):
                            yield result