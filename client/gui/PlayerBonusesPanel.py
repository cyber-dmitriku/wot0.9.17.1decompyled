# Source Generated with Decompyle++
# File: PlayerBonusesPanel.pyc (Python 2.6)

import BigWorld
from gui import DebugMonitorView
from gui import DEPTH_OF_PlayerBonusesPanel
import constants
from debug_utils import *

class PlayerBonusesPanel(object):
    
    def __init__(self):
        self._PlayerBonusesPanel__monitor = None

    
    def prerequisites(self):
        return []

    
    def start(self):
        self._PlayerBonusesPanel__monitor = self._PlayerBonusesPanel__createDebugMonitorView()

    
    def destroy(self):
        self._PlayerBonusesPanel__monitor.destroy()
        self._PlayerBonusesPanel__monitor = None

    
    def setVisible(self, bValue):
        if self._PlayerBonusesPanel__monitor is not None:
            self._PlayerBonusesPanel__monitor.setVisible(bValue)
        

    
    def getVisible(self):
        if self._PlayerBonusesPanel__monitor is not None:
            return self._PlayerBonusesPanel__monitor.getVisible()
        return False

    
    def setContent(self, content):
        self._PlayerBonusesPanel__monitor.setContent(content)

    
    def _PlayerBonusesPanel__createDebugMonitorView(self):
        result = DebugMonitorView.DebugMonitorView()
        result.setPosition((-0.99, 0.15, DEPTH_OF_PlayerBonusesPanel))
        result.setAlign((True, True, True, True))
        result.setMargin((0.04, 0.04, 0.04, 0.04))
        result.setVisible(True)
        return result



