from ..objects import package as pk, texture_pack
from ..errors import PackageNotSupported, PackageAlreadyExist
from ..paths import Paths

from .default_paths import DefaultPaths

class Minecraft():
    """Class that handles installation of minecraft java edition packs."""
    def __init__(self, dot_minecraft_dir:str=DefaultPaths.DOT_MINECRAFT):
        self.__dot_minecraft_dir = dot_minecraft_dir

        if isinstance(dot_minecraft_dir, DefaultPaths): 
            self.__dot_minecraft_dir = dot_minecraft_dir.value

    def install(self, package:pk.Package, overwrite_if_exist:bool=False) -> bool:
        """Method to install a package into minecraft."""
        
        if isinstance(package, texture_pack.TexturePack):
            # Zip the package if it is a folder.
            if package.file_type == pk.FileTypes.FOLDER:
                package.zip()

            # Move the package to JSQPCore install location directory.
            try:
                package.move(package.install_location, overwrite_if_exist)
            except FileNotFoundError:
                # Repair and try again if file is not found.
                # -------------------------------------------
                Paths().repair_app_data_dir([
                    package.install_location
                ])

                package.move(package.install_location, overwrite_if_exist)

            return True
            
        raise PackageNotSupported(package, self)