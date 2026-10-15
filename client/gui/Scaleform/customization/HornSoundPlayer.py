# Source Generated with Decompyle++
# File: HornSoundPlayer.pyc (Python 2.6)

import BigWorld
import FMOD
import Event
from debug_utils import LOG_DEBUG
from gui import ClientHangarSpace
from items import vehicles

class HornSoundPlayer(object):
    
    def __init__(self):
        super(HornSoundPlayer, self).__init__()
        self._HornSoundPlayer__hornID = None
        self._HornSoundPlayer__hornSoundIdx = 0
        self._HornSoundPlayer__hornSounds = []
        self._HornSoundPlayer__hornMode = ''
        self._HornSoundPlayer__playing = False
        self._HornSoundPlayer__flashButton = None
        self._HornSoundPlayer__stopCallback = None
        self.onStartSoundEvent = Event.Event()
        self.onStopSoundEvent = Event.Event()

    
    def clear(self):
        while len(self._HornSoundPlayer__hornSounds):
            sound = self._HornSoundPlayer__hornSounds.pop()
            sound.setCallback('SOUNDDEF_START', None)
            sound.setCallback('SOUNDDEF_END', None)
            sound.stop()
        self._HornSoundPlayer__hornID = None
        self._HornSoundPlayer__hornSoundIdx = 0
        self._HornSoundPlayer__hornMode = ''
        self._HornSoundPlayer__playing = False
        self._HornSoundPlayer__flashButton = None

    
    def fini(self):
        self.clear()
        self.onStartSoundEvent.clear()
        self.onStopSoundEvent.clear()
        if self._HornSoundPlayer__stopCallback is not None:
            BigWorld.cancelCallback(self._HornSoundPlayer__stopCallback)
            self._HornSoundPlayer__stopCallback = None
        

    
    def play(self, hornID, button):
        hornDesc = vehicles.g_cache.horns().get(hornID)
        if hornDesc is None:
            return None
        LOG_DEBUG('Start playing sound by user')
        self.stop(forceSilence = True)
        self._HornSoundPlayer__hornID = hornID
        self._HornSoundPlayer__flashButton = button
        self._HornSoundPlayer__hornSounds = []
        self._HornSoundPlayer__hornSoundIdx = 0
        self._HornSoundPlayer__hornMode = hornDesc['mode']
        self._HornSoundPlayer__stopCallback = None
        for sndEventId in hornDesc['sounds']:
            sound = FMOD.getSound(sndEventId)
            sound.position = ClientHangarSpace._V_START_POS
            sound.setCallback('SOUNDDEF_START', self._HornSoundPlayer__soundDefStart)
            sound.setCallback('SOUNDDEF_END', self._HornSoundPlayer__soundDefStop)
            self._HornSoundPlayer__hornSounds.append(sound)
        
        if len(self._HornSoundPlayer__hornSounds) > 0:
            self._HornSoundPlayer__hornSounds[0].play()
            self._HornSoundPlayer__playing = True
            if self._HornSoundPlayer__hornMode == 'continuous' and hornDesc['maxDuration'] > 0:
                self._HornSoundPlayer__stopCallback = BigWorld.callback(hornDesc['maxDuration'], self.stop)
            
        

    
    def stop(self, forceSilence = False):
        if not self._HornSoundPlayer__playing:
            if self._HornSoundPlayer__stopCallback is not None:
                BigWorld.cancelCallback(self._HornSoundPlayer__stopCallback)
                self._HornSoundPlayer__stopCallback = None
            
            return None
        LOG_DEBUG('Stop playing sound by user')
        if not forceSilence and self._HornSoundPlayer__hornMode == 'twoSounds':
            if self._HornSoundPlayer__hornSounds[1] is not None:
                self._HornSoundPlayer__hornSounds[1].play()
            
        else:
            self.onStopSoundEvent(self._HornSoundPlayer__flashButton)
            self.clear()
        if self._HornSoundPlayer__stopCallback is not None:
            BigWorld.cancelCallback(self._HornSoundPlayer__stopCallback)
            self._HornSoundPlayer__stopCallback = None
        

    
    def stopWithDelay(self, delay = 2):
        if self._HornSoundPlayer__hornMode == 'twoSounds' or delay <= 0:
            self.stop()
            return None
        if self._HornSoundPlayer__stopCallback is not None:
            BigWorld.cancelCallback(self._HornSoundPlayer__stopCallback)
            self._HornSoundPlayer__stopCallback = None
        
        self._HornSoundPlayer__stopCallback = BigWorld.callback(delay, self.stop)

    
    def _HornSoundPlayer__soundDefStart(self, sound):
        LOG_DEBUG('Start playing sound by event', sound)
        self.onStartSoundEvent(self._HornSoundPlayer__flashButton)

    
    def _HornSoundPlayer__soundDefStop(self, sound):
        LOG_DEBUG('Stop playing sound by event', sound)
        if self._HornSoundPlayer__playing:
            self.onStopSoundEvent(self._HornSoundPlayer__flashButton)
            self._HornSoundPlayer__hornSoundIdx += 1
            if self._HornSoundPlayer__hornSoundIdx >= len(self._HornSoundPlayer__hornSounds):
                self.clear()
                if self._HornSoundPlayer__stopCallback is not None:
                    BigWorld.cancelCallback(self._HornSoundPlayer__stopCallback)
                    self._HornSoundPlayer__stopCallback = None
                
            
        



