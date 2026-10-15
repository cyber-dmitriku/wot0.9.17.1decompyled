# Source Generated with Decompyle++
# File: CursorDelegator.pyc (Python 2.6)

import BigWorld
import GUI
from debug_utils import LOG_DEBUG

class CursorDelegator(object):
    
    def __init__(self):
        super(CursorDelegator, self).__init__()
        self._CursorDelegator__activated = False
        self._CursorDelegator__savedMCursorPos = None

    
    def activateCursor(self):
        if not self._CursorDelegator__activated:
            mcursor = GUI.mcursor()
            mcursor.visible = False
            LOG_DEBUG('Cursor activate', mcursor.position)
            BigWorld.setCursor(mcursor)
            self._CursorDelegator__activated = True
        

    
    def detachCursor(self):
        if self._CursorDelegator__activated:
            LOG_DEBUG('Cursor detach')
            BigWorld.setCursor(None)
            self._CursorDelegator__activated = False
        

    
    def syncMousePosition(self, flash, flashX = None, flashY = None, customCall = False):
        (screenWidth, screenHeight) = GUI.screenResolution()
        (mouseLeft, mouseTop) = GUI.mcursor().position
        if not customCall:
            self._CursorDelegator__savedMCursorPos = (mouseLeft, mouseTop)
        
        if flashX is None:
            pass
        1
        x = flashX
        if flashY is None:
            pass
        1
        y = flashY
        if flashX is not None and flashY is not None:
            GUI.mcursor().position = (x * 2 / screenWidth - 1, -y * 2 / screenHeight + 1)
        
        flash.call('Cursor.SetPosition', [
            x,
            y])

    
    def restoreMousePosition(self):
        if self._CursorDelegator__savedMCursorPos is not None:
            GUI.mcursor().position = self._CursorDelegator__savedMCursorPos
            self._CursorDelegator__savedMCursorPos = None
        

    
    def setForcedGuiControlMode(self, flash, hold):
        flash.call('Cursor.Hold', [
            hold])
        if hasattr(BigWorld.player(), 'setForcedGuiControlMode'):
            BigWorld.player().setForcedGuiControlMode(hold)
        


g_cursorDelegator = CursorDelegator()

