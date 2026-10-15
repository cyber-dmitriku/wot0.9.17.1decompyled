# Source Generated with Decompyle++
# File: MemoryCriticalController.pyc (Python 2.6)

import BigWorld
from debug_utils import LOG_NOTE
import Event

class MemoryCriticalController:
    QUALITY_MAP = [
        'high',
        'medium',
        'low']
    messages = property((lambda self: self._MemoryCriticalController__messages))
    onMemCrit = property((lambda self: self._MemoryCriticalController__event))
    originQuality = property((lambda self: self._MemoryCriticalController__originQuality))
    
    def __init__(self):
        self._MemoryCriticalController__messages = []
        self._MemoryCriticalController__originQuality = -1
        self._MemoryCriticalController__needReboot = False
        self._MemoryCriticalController__event = Event.Event()

    
    def destroy(self):
        if self._MemoryCriticalController__event is not None:
            self._MemoryCriticalController__event.clear()
            self._MemoryCriticalController__event = None
        

    
    def __call__(self):
        if self._MemoryCriticalController__needReboot:
            return None
        texQuality = BigWorld.getGraphicsSetting('TEXTURE_QUALITY')
        if texQuality < 2:
            texQuality += 1
            if self._MemoryCriticalController__originQuality == -1:
                self._MemoryCriticalController__originQuality = texQuality - 1
            
            LOG_NOTE('To save the memory the texture quality setting was force lowered to <%s>.' % self.QUALITY_MAP[texQuality])
        else:
            message = (1, 'insufficient_memory_please_reboot')
            self._MemoryCriticalController__messages.append(message)
            self._MemoryCriticalController__event(message)
            LOG_NOTE("The free memory is too low, We can't do anything. Please, reboot the game.")
            self._MemoryCriticalController__needReboot = True
            return None
        message = (texQuality < 2, 'tex_was_lowered_to_' + self.QUALITY_MAP[texQuality])
        self._MemoryCriticalController__messages.append(message)
        self._MemoryCriticalController__event(message)
        BigWorld.setGraphicsSetting('TEXTURE_QUALITY', texQuality)
        BigWorld.commitPendingGraphicsSettings()

    
    def restore(self):
        if self._MemoryCriticalController__originQuality != -1:
            BigWorld.setGraphicsSetting('TEXTURE_QUALITY', self._MemoryCriticalController__originQuality)
            BigWorld.commitPendingGraphicsSettings()
            LOG_NOTE('The texture quality setting was restored to the original value <%s>.' % self.QUALITY_MAP[self._MemoryCriticalController__originQuality])
            self._MemoryCriticalController__originQuality = -1
            self._MemoryCriticalController__needReboot = False
            self._MemoryCriticalController__messages = []
        


g_critMemHandler = MemoryCriticalController()

