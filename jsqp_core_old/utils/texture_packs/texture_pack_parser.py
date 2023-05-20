from __future__ import annotations

import os
from pathlib import Path
from devgoldyutils import LoggerAdapter

from ... import jsqp_core_logger
from ...objects.package import FilePackage
from ...errors import JSQPCoreError

class AssetsFolderNotFound(JSQPCoreError):
    def __init__(self, texture_pack:FilePackage):
        super().__init__(f"The assets folder for the texture pack at '{texture_pack.path}' can't be found therefore this texture pack can't be phrased correctly!")

class TexturePackParser():
    """Class used to detect the version and actual path of a minecraft java texture pack via the file structure."""
    def __init__(self, texture_pack:FilePackage) -> None:
        self.texture_pack = texture_pack

        self.parser_logger = LoggerAdapter(jsqp_core_logger, "TexturePackParser")

        self.__path_to_assets = ""

        assets_exist, assets_path = next(
            self.assets_folder_exist(self.get_folder_structure()),
            (False, None)
        )

        if not assets_exist:
            raise AssetsFolderNotFound(texture_pack)

        self.parser_logger.info(f"Parsed the texture pack '{self.actual_name}'!")
    
    @property
    def root_path(self) -> str|None:
        """Returns the real root path of this texture pack. E.g. where the ``assets``, ``pack.mcmeta`` and ``pack.png`` is stored."""
        if self.__path_to_assets == "":
            return None
        else:
            return self.texture_pack.path + (lambda x: "" if x == "/" else x)(os.path.split(self.__path_to_assets)[0])

    @property
    def assets_path(self) -> str|None:
        if self.__path_to_assets == "":
            return None
        else:
            return f"{self.texture_pack.path}/{os.path.split(self.__path_to_assets)[1]}"

    @property
    def actual_name(self) -> str|None:
        """Returns the actual name of the texture pack."""
        if self.root_path is None:
            return None
    
        return os.path.split(self.root_path)[1]

    def get_folder_structure(self) -> dict:
        """Returns the folder structure of this texture pack."""
        folder_structure = {}
        for foldername, subfolders, filenames in os.walk(self.texture_pack.path):
            current_folder = folder_structure
            subfolder_list = foldername.split(os.path.sep)
            for subfolder in subfolder_list[1:]:
                if subfolder not in current_folder:
                    current_folder[subfolder] = {}
                current_folder = current_folder[subfolder]
            current_folder['files'] = filenames
        return folder_structure

    
    # Partly stolen from: https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-dictionaries-and-lists
    # ----------------------------------------------------------------------------------------------------------------------------
    def assets_folder_exist(self, folder_stucure:dict):
        if hasattr(folder_stucure, 'items'):
            for k, v in folder_stucure.items():
                if not k == "files":
                    self.__path_to_assets += f"/{k}"
                
                if k == "assets":
                    yield True, self.__path_to_assets
                if isinstance(v, dict):
                    for result in self.assets_folder_exist(v):
                        yield result
                elif isinstance(v, list):
                    for d in v:
                        for result in self.assets_folder_exist(d):
                            yield result