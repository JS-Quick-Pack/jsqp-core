from jsqp_core import TexturePack
from ... import TexturePackParser

texture_pack_1 = TexturePack("./utils/texture_packs/.parser_files/test_texture_pack_1.zip")
texture_pack_2 = TexturePack("./utils/texture_packs/.parser_files/damn.zip")
texture_pack_3 = TexturePack("./utils/texture_packs/.parser_files/goldy_pack")

def test_parser_actual_name():
    assert TexturePackParser(texture_pack_1).actual_name == "test_texture_pack_1"
    assert TexturePackParser(texture_pack_2).actual_name == "uwu_pack_v2.0"
    assert TexturePackParser(texture_pack_3).actual_name == "goldy_pack"