# Source Generated with Decompyle++
# File: SwitchController.pyc (Python 2.6)

import BigWorld
from Vibroeffects import VibroManager
from debug_utils import *

class SwitchController:
    
    def __init__(self, effectName):
        self._SwitchController__effect = VibroManager.g_instance.getEffect(effectName)

    
    def destroy(self):
        VibroManager.g_instance.stopEffect(self._SwitchController__effect)
        self._SwitchController__effect = None

    
    def switch(self, turnOn):
        if turnOn:
            VibroManager.g_instance.startEffect(self._SwitchController__effect)
        else:
            VibroManager.g_instance.stopEffect(self._SwitchController__effect)



