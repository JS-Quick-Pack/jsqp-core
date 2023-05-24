from __future__ import annotations

import os
import json
from deepdiff import DeepDiff
from pathlib import Path
from typing import TYPE_CHECKING, Dict
from devgoldyutils import LoggerAdapter, Colours

from ... import core_logger
from ...mc_versions import MCVersions
from ...errors import JSQPCoreError
from . import maps

if TYPE_CHECKING:
    from ...packages.texture_pack import TexturePack

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

        self.folder_structure = self.__get_folder_structure()
        """Folder structure of this texture pack."""

        assets_exist = next(self.__find_assets_folder(self.folder_structure), False)

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
        return str(self.texture_pack.path) + (lambda x: "" if x == "/" else x)(os.path.split(self.__path_to_assets)[0])

    @property
    def assets_path(self) -> str:
        return f"{self.texture_pack.path}/{os.path.split(self.__path_to_assets)[1]}"
    
    @property
    def version(self) -> MCVersions:
        """Returns the minecraft version this pack belongs to."""
        return self.detect_version()
    
    def detect_version(self) -> MCVersions:
        """Tries to detect the game version this pack was made for."""
        # TODO: the funny code.
        version_diff: Dict[int, MCVersions] = {}

        for version in MCVersions:
            json_file = open(f"{os.path.split(maps.__file__)[0]}/{version.value}.json", mode="r")
            json_file = json.load(json_file)

            difference = DeepDiff(json_file, self.folder_structure)

            version_diff[len(difference.affected_paths)] = version

        detected_version = version_diff[sorted(version_diff)[0]]
        self.logger.info(f"Detected Version -> {Colours.GREEN.apply(detected_version.name)}")
        self.logger.debug(
            f"Version difference = {Colours.PINK_GREY.apply(str([f'{version_diff[x].name} ({x})' for x in sorted(version_diff)]))}"
        )

        return detected_version

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
                    self.folder_structure = folder_structure

                if k == "assets":
                    yield True

                if isinstance(v, dict):
                    for result in self.__find_assets_folder(v):
                        yield result

                elif isinstance(v, list):
                    for d in v:
                        for result in self.__find_assets_folder(d):
                            yield result