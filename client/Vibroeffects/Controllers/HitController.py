# Source Generated with Decompyle++
# File: HitController.pyc (Python 2.6)

import BigWorld
import Math
from constants import SHOT_RESULT
from debug_utils import *
from OnceController import OnceController
import math

class HitController:
    
    def __init__(self, shotResult):
        if shotResult in (SHOT_RESULT.ARMOR_NOT_PIERCED, SHOT_RESULT.ARMOR_PIERCED_NO_DAMAGE):
            OnceController('hit_nonpenetration_veff')
            return None
        if shotResult == SHOT_RESULT.RICOCHET:
            OnceController('hit_ricochet_veff')
            return None
        if shotResult == SHOT_RESULT.MAX_HIT + 1:
            OnceController('hit_splash_veff')
            return None
        OnceController('hit_veff')



