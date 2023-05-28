from ... import TexturePackParser, TexturePack, MCVersions, core_logger, logging

core_logger.setLevel(logging.DEBUG)

texture_pack_1 = TexturePack("./packages/texture_pack/.parser_files/test_texture_pack_1.zip")
texture_pack_2 = TexturePack("./packages/texture_pack/.parser_files/damn.zip")
texture_pack_3 = TexturePack("./packages/texture_pack/.parser_files/mc_1.10_pack")

def test_actual_name():
    assert TexturePackParser(texture_pack_1).actual_name == "test_texture_pack_1"
    assert TexturePackParser(texture_pack_2).actual_name == "uwu_pack_v2.0"
    assert TexturePackParser(texture_pack_3).actual_name == "goldy_pack"

def test_version_detection():
    assert TexturePackParser(texture_pack_1).version == MCVersions.JAVA_1_12
    assert TexturePackParser(texture_pack_2).version == MCVersions.JAVA_1_10
    assert TexturePackParser(texture_pack_3).version == MCVersions.JAVA_1_10