from typing import Dict, Tuple
from ...mc_versions import MCVersions

__all__ = ("pack_format_versions",)

pack_format_versions: Dict[int, Tuple[MCVersions]] = {
    1: (MCVersions.JAVA_1_6, MCVersions.JAVA_1_7, MCVersions.JAVA_1_8),
    2: (MCVersions.JAVA_1_9, MCVersions.JAVA_1_10),
    3: (MCVersions.JAVA_1_11, MCVersions.JAVA_1_12,),
    4: (MCVersions.JAVA_1_13, MCVersions.JAVA_1_14),
    5: (MCVersions.JAVA_1_15, MCVersions.JAVA_1_16),
    6: (MCVersions.JAVA_1_16,),
    7: (MCVersions.JAVA_1_17,),
    8: (MCVersions.JAVA_1_18,),
    9: (MCVersions.JAVA_1_19,),
    # idk who would create a pack in a snapshot version so I'm skipping them.
    12: (MCVersions.JAVA_1_19,),
    13: (MCVersions.JAVA_1_19,),
    15: (MCVersions.JAVA_1_20,)
}
"""The minecraft versions corresponding to each pack format version."""