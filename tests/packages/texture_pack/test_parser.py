from ... import TexturePack, MCVersions, core_logger, logging

core_logger.setLevel(logging.DEBUG)

texture_pack_1 = TexturePack("./packages/texture_pack/.parser_files/test_texture_pack_1.zip")
texture_pack_2 = TexturePack("./packages/texture_pack/.parser_files/goldish_pack.zip")
texture_pack_3 = TexturePack("./packages/texture_pack/.parser_files/mc_1.10_pack.zip")

def test_actual_name():
    assert texture_pack_1.parser.actual_name == "test_texture_pack_1"
    assert texture_pack_2.parser.actual_name == "!        §eGold§6ish §bPack §7(§f350 SUBS§7) §7[§416x§7]"
    assert texture_pack_3.parser.actual_name == "goldy_pack"

def test_version_detection():
    assert texture_pack_1.parser.version == MCVersions.JAVA_1_12
    assert texture_pack_2.parser.version == MCVersions.JAVA_1_8
    assert texture_pack_3.parser.version == MCVersions.JAVA_1_12