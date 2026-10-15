# Source Generated with Decompyle++
# File: Postmortem.pyc (Python 2.6)

import BigWorld
from gui import DEPTH_OF_Postmortem
from gui.Scaleform.windows import ModalWindow
from debug_utils import LOG_DEBUG

class _Postmortem(ModalWindow):
    
    def __init__(self, continueCallback):
        ModalWindow.__init__(self, 'postmortem.swf')
        self.movie.backgroundAlpha = 0
        self.component.position.z = DEPTH_OF_Postmortem
        if hasattr(BigWorld.player(), 'setForcedGuiControlMode'):
            BigWorld.player().setForcedGuiControlMode(True)
        
        self._Postmortem__continueCallback = continueCallback
        self.addFsCallbacks({
            'postmortem.Exit': self.onExit,
            'postmortem.Continue': self.onContinue })

    
    def close(self):
        self._Postmortem__continueCallback = None
        ModalWindow.close(self)

    
    def onExit(self, arg):
        LOG_DEBUG('onExitBattle')
        arena = getattr(BigWorld.player(), 'arena', None)
        if arena:
            BigWorld.player().leaveArena()
        
        Postmortem.hide()

    
    def onContinue(self, arg):
        if hasattr(BigWorld.player(), 'setForcedGuiControlMode'):
            BigWorld.player().setForcedGuiControlMode(False)
        
        self._Postmortem__continueCallback()
        Postmortem.hide()


__waiting = None

class Postmortem:
    _Postmortem__window = None
    
    def show(continueCallback):
        if Postmortem._Postmortem__window is None:
            Postmortem._Postmortem__window = _Postmortem(continueCallback)
            Postmortem._Postmortem__window.active(True)
        

    show = staticmethod(show)
    
    def hide():
        if Postmortem._Postmortem__window is not None:
            Postmortem._Postmortem__window.close()
            Postmortem._Postmortem__window = None
        

    hide = staticmethod(hide)


