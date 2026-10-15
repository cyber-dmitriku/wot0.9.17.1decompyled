# Source Generated with Decompyle++
# File: GameLoading.pyc (Python 2.6)

import GUI
from debug_utils import LOG_DEBUG
from gui.Scaleform.Flash import Flash
from helpers import getClientVersion

class GameLoading(Flash):
    
    def __init__(self, component = None):
        Flash.__init__(self, 'GameLoading.swf')
        self.call('Stage.Update', list(GUI.screenResolution()))
        self._GameLoading__loadVersion()

    
    def onLoad(self, dataSection):
        self.active(True)

    
    def onBound(self):
        pass

    
    def setProgress(self, value):
        self.call('setProgress', [
            value])

    
    def addMessage(self, message):
        LOG_DEBUG(message)

    
    def reset(self):
        self.call('setProgress', [
            0])

    
    def _GameLoading__loadVersion(self):
        self.call('Login.SetVersion', [
            getClientVersion()])



