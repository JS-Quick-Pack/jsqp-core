from __future__ import annotations

import os
import json
from deepdiff import DeepDiff
from typing import TYPE_CHECKING, Dict, Tuple, final, TypedDict, Literal
from devgoldyutils import LoggerAdapter, Colours, pprint

from ... import core_logger
from ...mc_versions import MCVersions
from ...errors import JSQPCoreError
from . import maps, pack_formats

if TYPE_CHECKING:
    from ...packages.texture_pack import TexturePack

PACK_FORMAT_TYPES = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9]

@final
class PackMeta(TypedDict):
    pack_format: PACK_FORMAT_TYPES
    description: str

@final
class MCMeta(TypedDict):
    pack: PackMeta

class AssetsFolderNotFound(JSQPCoreError):
    def __init__(self, texture_pack: TexturePack, map: dict):
        pprint(map, depth=8, max_seq_len=3)
        texture_pack.logger.info(Colours.ORANGE.apply("^ The texture pack's map has been printed above ^"))

        super().__init__(
            f"The assets folder for the texture pack at '{texture_pack.path}' can't be found therefore this texture pack can't be phrased correctly!" \
            f"{Colours.BLUE} Make sure your pack is structured correctly and has an assets folder.{Colours.RESET}"
        )

class TexturePackParser():
    """Class used to detect the version and actual path of a minecraft java texture pack via the file structure."""
    def __init__(self, texture_pack: TexturePack) -> None:
        self.texture_pack = texture_pack

        self.logger = LoggerAdapter(core_logger, "TexturePackParser")

        self.__path_to_assets = ""
        """The path to the assets folder, this is automatically assigned by ``.__find_assets_folder()``."""

        self.map = self.__get_folder_structure()
        """Folder structure of this texture pack."""

        assets_exist = next(self.__find_assets_folder(self.map), False)

        if not assets_exist:
            raise AssetsFolderNotFound(texture_pack, self.map)

        self.logger.info(f"Parsed the texture pack '{self.actual_name}'!")
    
    @property
    def actual_name(self) -> str | None:
        """Returns the actual name of the texture pack."""
        return os.path.split(self.root_path)[1]

    @property
    def root_path(self) -> str:
        """Returns the real root path of this texture pack. E.g. where the ``assets``, ``pack.mcmeta`` and ``pack.png`` is stored."""
        # TODO: Fix this, it breaks with zips.
        return str(self.texture_pack.path) + (lambda x: "" if x == "/" else x)(os.path.split(self.__path_to_assets)[0])

    @property
    def assets_path(self) -> str:
        return f"{self.texture_pack.path}/{os.path.split(self.__path_to_assets)[1]}"
    
    @property
    def mc_meta(self) -> MCMeta:
        file = open(self.root_path + "/pack.mcmeta", mode="r")
        json_dict = json.load(file)
        file.close()
        return json_dict

    @property
    def pack_format(self) -> Tuple[PACK_FORMAT_TYPES, Tuple[MCVersions]]:
        """Returns the pack format of this pack and the versions that pack format corresponds to."""
        return self.mc_meta["pack"]["pack_format"], pack_formats.pack_format_versions[self.mc_meta["pack"]["pack_format"]]
    
    @property
    def version(self) -> MCVersions:
        """Returns the minecraft version this pack belongs to."""
        return self.detect_version()
    
    def detect_version(self) -> MCVersions:
        """Tries to detect the game version this pack was made for."""
        version_diff: Dict[int, MCVersions] = {}
        self.logger.debug("Detecting minecraft version of this texture pack...")
        self.logger.warning(
            "If the detected pack version is false PLEASE report an issue at https://github.com/JS-Quick-Pack/jsqp-core/issues."
        )

        targeted_versions = self.pack_format[1]

        for version in targeted_versions:
            json_file = open(f"{os.path.split(maps.__file__)[0]}/{version.value}.json", mode="r")
            json_file = json.load(json_file)

            difference = DeepDiff(json_file, self.map)

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
        main_folder_name = os.path.split(self.texture_pack.path)[1]

        # type 3 is a zip so we should use the zip walker I made instead.
        for foldername, _, filenames in os.walk(self.texture_pack.path):
            current_folder = folder_structure
            subfolder_list = foldername.split(main_folder_name)[1].split(os.path.sep)

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
                    yield True

                if isinstance(v, dict):
                    for result in self.__find_assets_folder(v):
                        yield result

                elif isinstance(v, list):
                    for d in v:
                        for result in self.__find_assets_folder(d):
                            yield result