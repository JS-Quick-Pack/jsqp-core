from ...objects import package as pk
from ...errors import PackageNotSupported, PackageAlreadyExist
from ...paths import Paths

from .. import Installer

from .default_paths import DefaultPaths

class MinecraftJava(Installer):
    """Class that handles installation of minecraft java edition packs."""
    def __init__(self, dot_minecraft_dir:str=DefaultPaths.DOT_MINECRAFT):
        self.__dot_minecraft_dir = dot_minecraft_dir

        if isinstance(dot_minecraft_dir, DefaultPaths):
            self.__dot_minecraft_dir = dot_minecraft_dir.value

        super().__init__(
            display_name="Minecraft Java Edition"
        )

    def install(self, package:pk.Package, overwrite_if_exist:bool=False, performance_mode:bool=False) -> bool:
        """Method to install a package into minecraft."""
        from ...packages.texture_pack import TexturePack

        if isinstance(package, TexturePack):
            # Zip the package if it is a folder.
            if package.file_type == pk.FileTypes.FOLDER:
                package.zip(package.name + ".zip", performance_mode)

            package.file_rename(f"{package.name}.zip")

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