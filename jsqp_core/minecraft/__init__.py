from ..objects import package as pk, texture_pack
from ..errors import PackageNotSupported
from ..paths import Paths

from .default_paths import DefaultPaths

class Minecraft():
    """Class that handles installation of minecraft java edition packs."""
    def __init__(self, dot_minecraft_dir:str=DefaultPaths.DOT_MINECRAFT):
        self.__dot_minecraft_dir = dot_minecraft_dir

        if isinstance(dot_minecraft_dir, DefaultPaths): 
            self.__dot_minecraft_dir = dot_minecraft_dir.value

    def install(self, package:pk.Package) -> bool:
        """Method to install a package into minecraft."""
        install_path:str = DefaultPaths.JSQP_INSTALL_PATH.value
        
        if isinstance(package, texture_pack.TexturePack):
            if package.file_type == pk.FileTypes.FOLDER:
                package.zip()

            try:
                package.move(install_path + "/resource_packs")
            except FileNotFoundError:
                # Repair and try again if file is not found.
                # -------------------------------------------
                Paths().repair_app_data_dir([
                    install_path + "/resource_packs"
                ])

                package.move(install_path + "/resource_packs")

            return True
            
        raise PackageNotSupported(package, self)