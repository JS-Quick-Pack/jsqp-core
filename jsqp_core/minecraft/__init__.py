from ..objects import package, texture_pack

from .default_paths import DefaultPaths

class Minecraft():
    """Class that handles installation of minecraft java edition packs."""
    def __init__(self, dot_minecraft_dir:str=DefaultPaths.DOT_MINECRAFT):
        self.__dot_minecraft_dir = dot_minecraft_dir

        if isinstance(dot_minecraft_dir, DefaultPaths): 
            self.__dot_minecraft_dir = dot_minecraft_dir.value

    def install(self, package:package.Package):
        """Method to install a package into minecraft."""
        install_path:str = DefaultPaths.JSQP_INSTALL_PATH.value
        
        if isinstance(package, texture_pack.TexturePack):
            package.move(install_path + "/resource_packs")