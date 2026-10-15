# Source Generated with Decompyle++
# File: EdgeDetectColorController.pyc (Python 2.6)

import BigWorld
import ResMgr
import Math
from account_helpers.AccountSettings import AccountSettings
g_instance = None

class EdgeDetectColorController:
    
    def __init__(self, dataSec):
        self._EdgeDetectColorController__colors = {
            'common': dict(),
            'colorBlind': dict() }
        self._EdgeDetectColorController__readColors(self._EdgeDetectColorController__colors['common'], 'common', dataSec)
        self._EdgeDetectColorController__readColors(self._EdgeDetectColorController__colors['colorBlind'], 'colorBlind', dataSec)
        AccountSettings.onSettingsChanging += self._EdgeDetectColorController__changeColor

    
    def updateColors(self):
        self._EdgeDetectColorController__changeColor('isColorBlind')

    
    def destroy(self):
        AccountSettings.onSettingsChanging -= self._EdgeDetectColorController__changeColor

    
    def _EdgeDetectColorController__readColors(self, out, type, section):
        cName = '%s/' % type
        out['self'] = section.readVector4(cName + 'self', Math.Vector4(0.2, 0.2, 0.2, 0.5))
        out['enemy'] = section.readVector4(cName + 'enemy', Math.Vector4(1, 0, 0, 0.5))
        out['friend'] = section.readVector4(cName + 'friend', Math.Vector4(0, 1, 0, 0.5))

    
    def _EdgeDetectColorController__changeColor(self, args):
        if args != 'isColorBlind':
            return None
        if AccountSettings.getSettings('isColorBlind') is True:
            pass
        1
        cType = 'common'
        colors = self._EdgeDetectColorController__colors[cType]
        BigWorld.wgSetEdgeDetectColors((colors['self'], colors['enemy'], colors['friend']))



