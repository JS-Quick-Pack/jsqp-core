from typing import Dict, Tuple
from ...mc_versions import MCVersions

pack_format_versions: Dict[int, Tuple[MCVersions]] = {
    1: (MCVersions.JAVA_1_8,),
    2: (MCVersions.JAVA_1_10,),
    3: (MCVersions.JAVA_1_12,),
    4: (),
    5: (),
    6: (),
    7: (MCVersions.JAVA_1_17,),
    8: (MCVersions.JAVA_1_18,),
    9: (MCVersions.JAVA_1_19,),
    12: (MCVersions.JAVA_1_19,),
    13: (MCVersions.JAVA_1_19,),
}
"""The minecraft versions corresponding to each pack format version."""