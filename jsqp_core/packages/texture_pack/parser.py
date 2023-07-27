from __future__ import annotations

import os
import json
#from deepdiff import DeepDiff
from typing import TYPE_CHECKING, Dict, Tuple, final, TypedDict, Literal, Iterable, List, Generator, Any
from devgoldyutils import LoggerAdapter, Colours, pprint, short_str
from io import StringIO

from ...logger import core_logger
from ...mc_versions import MCVersions
from ...errors import JSQPCoreError
from . import maps, pack_formats

if TYPE_CHECKING:
    from ...packages.texture_pack import TexturePack

__all__ = ("AssetsFolderNotFound", "TexturePackParser")

PACK_FORMAT_TYPES = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9]

@final
class PackMeta(TypedDict):
    pack_format: PACK_FORMAT_TYPES
    description: str

@final
class MCMeta(TypedDict):
    pack: PackMeta

class AssetsFolderNotFound(JSQPCoreError):
    """Raises when the texture pack's assets folder is not found for some reason."""
    def __init__(self, texture_pack: TexturePack, map: dict):
        pprint(map, depth=8, max_seq_len=3)
        texture_pack.logger.info(Colours.ORANGE.apply("^ The texture pack's map has been printed above ^"))

        super().__init__(
            f"The assets folder for the texture pack at '{texture_pack.path}' can't be found therefore this texture pack can't be phrased correctly!" \
                f"{Colours.BLUE} Make sure your pack is structured correctly and has an assets folder.{Colours.RESET}"
        )

class UnsupportedPackFormat(JSQPCoreError):
    """Raises when the texture pack's assets folder is not found for some reason."""
    def __init__(self, texture_pack: TexturePack, key_error: KeyError):
        stream = StringIO()
        pprint(pack_formats.pack_format_versions, stream)
        stream.seek(0)

        super().__init__(
            f"This texture pack format seems to not be supported yet. This usually means your pack is too new for quick pack to phrase correctly.\n" \
                "Make sure to update quick pack core: pip install jsqp-core -U\n\n" \
                f"{Colours.RESET}{texture_pack.display_name}'s Format: {Colours.CLAY.apply(str(key_error))}\n" \
                f"{Colours.BLUE.apply('Formats we currently support:')}\n{stream.read()}" \
        )

class TexturePackParser():
    """Class used to detect the version and actual path of a minecraft java texture pack via the file structure."""
    def __init__(self, texture_pack: TexturePack) -> None:
        self.texture_pack = texture_pack

        self.logger = LoggerAdapter(LoggerAdapter(core_logger, "TexturePackParser"), prefix = Colours.PINK_GREY.apply(short_str(texture_pack.name)))

        self.__path_to_assets = ""
        """The path to the assets folder, this is automatically assigned by ``.__find_assets_folder()``."""

        self.original_pack_path = texture_pack.path
        """A copy of the path object for the texture pack when this parser was initialized."""
        
        self.map = self.__get_folder_structure()
        """Folder structure of this texture pack."""

        assets_exist = next(self.__find_assets_folder(self.map), False)

        if not assets_exist:
            raise AssetsFolderNotFound(texture_pack, self.map)

        self.logger.info(f"Parsed the texture pack '{self.actual_name}'!")

    @property
    def actual_name(self) -> str:
        """Returns the actual name of the texture pack."""
        return os.path.basename(os.path.normpath(self.root_path))

    @property
    def root_path(self) -> str:
        """Returns the real root path of this texture pack. E.g. where the ``assets``, ``pack.mcmeta`` and ``pack.png`` is stored."""
        return os.path.join(str(self.original_pack_path.absolute()), *os.path.split(self.__path_to_assets)[0].split(os.path.sep))

    @property
    def assets_path(self) -> str:
        return os.path.join(self.root_path, "assets")
    
    @property
    def mc_meta(self) -> MCMeta:
        self.logger.debug("Opening pack.mcmeta...")
        file = open(self.root_path + "/pack.mcmeta", mode="r")
        self.logger.debug("Parsing pack.mcmeta...")
        json_dict = json.load(file)
        file.close()
        return json_dict

    @property
    def pack_format(self) -> Tuple[PACK_FORMAT_TYPES, Tuple[MCVersions]]:
        """Returns the pack format of this pack and the versions that pack format corresponds to."""
        try:
            return self.mc_meta["pack"]["pack_format"], pack_formats.pack_format_versions[self.mc_meta["pack"]["pack_format"]]
        except KeyError as e:
            raise UnsupportedPackFormat(self.texture_pack, e)

    @property
    def description(self) -> str | None:
        """Returns the pack's description from the .mcmeta file."""
        return self.mc_meta["pack"].get("description", None)
    
    @property
    def version(self) -> MCVersions:
        """Returns the minecraft version this pack belongs to."""
        version, version_diff = self.detect_version(self.pack_format[1])
        
        if version_diff > 100: # If the version difference is too big target all versions.
            self.logger.warning(
                "We are detecting a large version difference, " \
                "If the detected pack version is false PLEASE report an issue at https://github.com/JS-Quick-Pack/jsqp-core/issues."
            )
            self.logger.debug("Trying again but with all minecraft versions instead...")
            version = self.detect_version(MCVersions)[0]

        return version
    
    def detect_version(self, targeted_versions: Iterable[MCVersions] = None) -> Tuple[MCVersions, int]:
        """
        This is an internal method, use `TexturePackParser.version` instead. 
        This method tries to detect the game version this pack was made for. Returns version and the detected map difference of that version.
        """
        version_diff: Dict[MCVersions, int] = {}
        self.logger.debug(f"Detecting minecraft version of '{self.actual_name}'...")

        if targeted_versions is None or len(targeted_versions) == 0:
            targeted_versions = MCVersions

        for version in targeted_versions:
            self.logger.debug(f"Testing against '{version.name}' map...")
            json_file = open(f"{os.path.split(maps.__file__)[0]}/{version.value}.json", mode="r")
            json_file = json.load(json_file)

            #difference = DeepDiff(self.map, json_file)
            #version_diff[version] = len(difference.affected_paths)

            mc_map_files = next(self.__get_map_files(json_file))
            texture_pack_map_files = next(self.__get_map_files(self.map))

            difference = list(set(mc_map_files).symmetric_difference(set(texture_pack_map_files)))
            #print(">", difference)
            version_diff[version] = len(difference)

        sorted_versions = sorted(version_diff, key=lambda x: version_diff[x])
        detected_version = sorted_versions[0]

        self.logger.info(f"Detected Version -> {Colours.GREEN.apply(detected_version.name)}")
        self.logger.debug(
            f"Version difference = {Colours.PINK_GREY.apply(str([f'{x.name} ({version_diff[x]})' for x in sorted_versions]))}"
        )

        return detected_version, version_diff[detected_version]

    def __get_folder_structure(self) -> dict:
        """Returns the folder structure of this texture pack."""
        folder_structure = {}
        main_folder_name = os.path.split(self.texture_pack.path)[1]

        for foldername, _, filenames in os.walk(self.texture_pack.path):
            current_folder = folder_structure
            subfolder_list = foldername.split(main_folder_name, maxsplit = 1)[1].split(os.path.sep)

            for subfolder in subfolder_list[1:]:
                if subfolder not in current_folder:
                    current_folder[subfolder] = {}
                current_folder = current_folder[subfolder]

            current_folder["files"] = filenames

        return folder_structure

    def __find_assets_folder(self, map: Dict[str, List[str] | dict]):
        """
        Function that will walk into directory after directory to find the assets folder.
        """

        for k, v in map.items():
            if k == "files":
                continue

            self.__path_to_assets += f"/{k}"

            if k == "assets":
                self.logger.debug("Assets folder found!")
                yield True

            if len(v.items()) == 1:
                yield False # There's no assets folder.

            yield next(self.__find_assets_folder(v))

    def __get_map_files(self, map: dict) -> Generator[List[str], Any, Any]:
        """Function returns all files from a texture pack map as a list."""
        list = []

        for key, value in map.items():
            if key == "files":
                list.extend(value)
                continue

            yield next(self.__get_map_files(value))

        yield list