# Source Generated with Decompyle++
# File: Waiting.pyc (Python 2.6)

from gui.Scaleform.windows import ModalWindow
from gui import InputHandler
from debug_utils import *
import inspect
import BigWorld
import Keys

class _Waiting(ModalWindow):
    
    def __init__(self, interruptCallback = (lambda : pass)):
        ModalWindow.__init__(self, 'waiting.swf')
        self.component.position.z = 0.1
        self.callback = interruptCallback
        InputHandler.g_instance.onKeyUp += self.handleKeyUpEvent

    
    def close(self):
        InputHandler.g_instance.onKeyUp -= self.handleKeyUpEvent
        ModalWindow.close(self)

    
    def setMessage(self, message):
        self.setMovieVariable('_root._level0.setMessage', [
            '#waiting:%s' % message])

    
    def handleKeyUpEvent(self, event):
        if event.key == Keys.KEY_ESCAPE:
            self.callback()
        


__waiting = None

class Waiting:
    _Waiting__window = None
    _Waiting__waitingStack = []
    
    def isVisible(cls):
        return cls._Waiting__window is not None

    isVisible = classmethod(isVisible)
    
    def show(message, isSingle = False, interruptCallback = (lambda : pass)):
        BigWorld.Screener.setEnabled(False)
        if not isSingle and message in Waiting._Waiting__waitingStack:
            Waiting._Waiting__waitingStack.append(message)
        
        if Waiting._Waiting__window is None:
            Waiting._Waiting__window = _Waiting(interruptCallback)
            Waiting._Waiting__window.setMessage(message)
            Waiting._Waiting__window.active(True)
        else:
            Waiting._Waiting__window.setMessage(message)
            Waiting._Waiting__window.callback = interruptCallback

    show = staticmethod(show)
    
    def hide(message):
        if Waiting._Waiting__window is None:
            LOG_DEBUG('Waitin.hide without show: in %s line %d func %s' % inspect.stack()[1][1:4])
            return None
        
        try:
            Waiting._Waiting__waitingStack.remove(message)
        except:
            Waiting._Waiting__window is None
            LOG_DEBUG('Waitin.hide without show: ', message, inspect.stack()[1][1:4])

        if len(Waiting._Waiting__waitingStack) == 0:
            Waiting.close()
        

    hide = staticmethod(hide)
    
    def close():
        BigWorld.Screener.setEnabled(True)
        if Waiting._Waiting__window:
            Waiting._Waiting__window.close()
            Waiting._Waiting__window = None
            Waiting._Waiting__waitingStack = []
        

    close = staticmethod(close)


