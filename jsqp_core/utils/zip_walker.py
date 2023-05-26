"""
My implementation os.walk but for zip files.
"""
import os
from zipfile import ZipFile
from typing import Dict, List, Generator, Tuple

def zip_walk(path_to_zip: str) -> Generator[Tuple[str, None, List[str]], None, None]:
    """Directory tree generator for zip files."""
    zip = ZipFile(path_to_zip)

    dict: Dict[str, List[str]] = {}

    for file in [x for x in zip.filelist]:
        folder_path, filename = os.path.split(file.filename)

        if folder_path not in dict:
            dict[folder_path] = []
            if not filename == "": dict[folder_path].append(filename)
        else:
            dict[folder_path].append(filename)

    for folder in [x for x in zip.filelist if x.is_dir()]:
        folder_path = os.path.split(folder.filename)[0]
        yield folder_path, None, dict[folder_path]