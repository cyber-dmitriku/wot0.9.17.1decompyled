# Source Generated with Decompyle++
# File: Disconnect.pyc (Python 2.6)

import BigWorld
import GUI
from gui.Scaleform.CursorDelegator import g_cursorDelegator
from helpers.i18n import makeString
from gui import DEPTH_OF_Disconnect
from gui.Scaleform.Waiting import Waiting
from gui.Scaleform.windows import ModalWindow
from debug_utils import LOG_DEBUG

class _Disconnect(ModalWindow):
    
    def __init__(self):
        ModalWindow.__init__(self, 'disconnect.swf')
        self.movie.backgroundAlpha = 0
        self.component.position.z = DEPTH_OF_Disconnect
        if hasattr(BigWorld.player(), 'setForcedGuiControlMode'):
            BigWorld.player().setForcedGuiControlMode(True)
        

    
    def show(self, reason = None, isBan = None, expiryTime = None):
        Waiting.close()
        g_cursorDelegator.syncMousePosition(self, None, None)
        params = {
            'reason': '',
            'expiryTime': '' }
        if reason:
            params['reason'] = makeString('#dialogs:disconnected/reason', makeString(reason))
        
        if expiryTime:
            makeLocalServerTime = makeLocalServerTime
            import helpers.time_utils
            expiryTime = makeLocalServerTime(int(expiryTime))
            params['expiryTime'] = BigWorld.wg_getLongDateFormat(expiryTime) + ' ' + BigWorld.wg_getLongTimeFormat(expiryTime)
        
        if not isBan:
            pass
        1
        if expiryTime:
            pass
        1
        message = 'messageBan'
        message = makeString('#dialogs:disconnected/' + message) % params
        self.setMovieVariable('_root._level0.setMessage', [
            message])

    
    def handleMouseEvent(self, event):
        return self.movie.handleMouseEvent(event)


__waiting = None

class Disconnect:
    _Disconnect__window = None
    
    def show():
        if Disconnect._Disconnect__window is None:
            Disconnect._Disconnect__showParentCursor(False)
            Disconnect._Disconnect__window = _Disconnect()
            Disconnect._Disconnect__window.active(True)
            Waiting.close()
        

    show = staticmethod(show)
    
    def showKick(reason, isBan, expiryTime):
        if Disconnect._Disconnect__window is None:
            Disconnect._Disconnect__showParentCursor(False)
            Disconnect._Disconnect__window = _Disconnect()
            Disconnect._Disconnect__window.show(reason, isBan, expiryTime)
            Disconnect._Disconnect__window.active(True)
            Waiting.close()
        

    showKick = staticmethod(showKick)
    
    def __showParentCursor(isShow):
        g_windowsManager = g_windowsManager
        import gui.WindowsManager
        if g_windowsManager.window is not None:
            g_windowsManager.window.showCursor(isShow)
        

    _Disconnect__showParentCursor = staticmethod(__showParentCursor)
    
    def hide():
        Disconnect._Disconnect__showParentCursor(True)
        if Disconnect._Disconnect__window is not None:
            Disconnect._Disconnect__window.close()
            Disconnect._Disconnect__window = None
        

    hide = staticmethod(hide)
    
    def getWindow():
        return Disconnect._Disconnect__window

    getWindow = staticmethod(getWindow)


