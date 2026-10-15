# Source Generated with Decompyle++
# File: VibroEffect.pyc (Python 2.6)

import BigWorld
from Vibroeffects.EffectsSettings import EffectsSettings

class VibroEffect:
    
    def __init__(self, name, handle, priority, vibrationObject, group):
        self.name = name
        self.group = group
        self._VibroEffect__priority = priority
        self._VibroEffect__vibrationObject = vibrationObject
        self._VibroEffect__isRunning = False
        self.handle = handle
        self._VibroEffect__relativeGain = 100
        self._VibroEffect__requiresGainChange = False
        durationInMs = None
        if self.handle is not None:
            durationInMs = self._VibroEffect__vibrationObject.getEffectLength(self.handle)
        
        if durationInMs is not None:
            self._VibroEffect__duration = durationInMs / 1000
        else:
            self._VibroEffect__duration = None
        self._VibroEffect__count = 0
        self._VibroEffect__startDelayId = None
        self._VibroEffect__stopDelayId = None

    
    def reInit(self, vibroEffect):
        self.name = vibroEffect.name
        self.handle = vibroEffect.handle
        self.group = vibroEffect.group
        self._VibroEffect__vibrationObject = vibroEffect._VibroEffect__vibrationObject
        self._VibroEffect__isRunning = vibroEffect._VibroEffect__isRunning
        self._VibroEffect__duration = vibroEffect._VibroEffect__duration
        self._VibroEffect__startDelayId = None
        self._VibroEffect__stopDelayId = None
        self._VibroEffect__relativeGain = 100
        self._VibroEffect__requiresGainChange = False

    
    def destroy(self):
        if self._VibroEffect__startDelayId is not None:
            BigWorld.cancelCallback(self._VibroEffect__startDelayId)
            self._VibroEffect__startDelayId = None
        
        if self._VibroEffect__stopDelayId is not None:
            BigWorld.cancelCallback(self._VibroEffect__stopDelayId)
            self._VibroEffect__stopDelayId = None
        
        if self.handle is not None:
            self._VibroEffect__vibrationObject.deleteEffect(self.handle)
        

    
    def onStart(self, count = None):
        if self.handle is None:
            return None
        self._VibroEffect__count = count
        if self._VibroEffect__startDelayId is not None:
            BigWorld.cancelCallback(self._VibroEffect__startDelayId)
        
        self._VibroEffect__startDelayId = BigWorld.callback(EffectsSettings.DELAY_BETWEEN_EFFECTS, self._VibroEffect__delayedStart)
        self._VibroEffect__isRunning = True

    
    def _VibroEffect__delayedStart(self):
        self._VibroEffect__startDelayId = None
        if self._VibroEffect__count is None:
            self._VibroEffect__vibrationObject.startEffect(self.handle, EffectsSettings.COUNT_INFINITY)
        else:
            self._VibroEffect__vibrationObject.startEffect(self.handle, self._VibroEffect__count)
        duration = self.getDuration()
        if duration is not None and self._VibroEffect__count is not None:
            self._VibroEffect__stopDelayId = BigWorld.callback(duration * self._VibroEffect__count, self.onStop)
        

    
    def onStop(self):
        if self._VibroEffect__startDelayId is not None:
            BigWorld.cancelCallback(self._VibroEffect__startDelayId)
            self._VibroEffect__startDelayId = None
        
        self._VibroEffect__stopDelayId = None
        self._VibroEffect__vibrationObject.stopEffect(self.handle)
        self._VibroEffect__stopDelayId = BigWorld.callback(EffectsSettings.DELAY_BETWEEN_EFFECTS, self._VibroEffect__delayedStop)

    
    def _VibroEffect__delayedStop(self):
        self._VibroEffect__stopDelayId = None
        self._VibroEffect__isRunning = False

    
    def setRelativeGain(self, gain):
        self._VibroEffect__relativeGain = gain
        self._VibroEffect__requiresGainChange = True

    
    def getRelativeGain(self):
        return self._VibroEffect__relativeGain

    
    def isRunning(self):
        return self._VibroEffect__isRunning

    
    def requiresGainChange(self):
        return self._VibroEffect__requiresGainChange

    
    def getPriority(self):
        return self._VibroEffect__priority

    
    def getDuration(self):
        return self._VibroEffect__duration



