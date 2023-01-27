import os
from pathlib import Path
from ...packages.texture_pack import TexturePack

class VersionDetector():
    """Class used to detect the version of a minecraft java texture pack via file structure."""
    def __init__(self, texture_pack:TexturePack) -> None:
        self.texture_pack = texture_pack

    def get_folder_structure(self) -> dict:
        """Creates a nested dictionary that represents the folder structure of rootdir."""

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