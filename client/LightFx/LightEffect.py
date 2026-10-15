# Source Generated with Decompyle++
# File: LightEffect.pyc (Python 2.6)

import BigWorld
import weakref
import Event
ACTION_MORPH = 1
ACTION_PULSE = 2
ACTION_COLOR = 3

class OneLightAction:
    
    def __init__(self, lightDescription, color, action):
        self.lightDescription = lightDescription
        self.color = color
        self.action = action



class LightEffect:
    
    def __init__(self, name, lightActions, duration = None):
        self.name = name
        self.lightActions = lightActions
        self._LightEffect__duration = duration
        self._LightEffect__eventManager = Event.EventManager()
        self.onStop = Event.Event(self._LightEffect__eventManager)
        self._LightEffect__onStopCallbackId = None
        self._LightEffect__isRunning = False

    
    def isRunning(self):
        return self._LightEffect__isRunning

    
    def destroy(self):
        if self._LightEffect__onStopCallbackId is not None:
            BigWorld.cancelCallback(self._LightEffect__onStopCallbackId)
            self._LightEffect__onStopCallbackId = None
        
        self._LightEffect__eventManager.clear()

    
    def start(self):
        if self._LightEffect__onStopCallbackId is not None:
            BigWorld.cancelCallback(self._LightEffect__onStopCallbackId)
            self._LightEffect__onStopCallbackId = None
        
        if self._LightEffect__duration is not None:
            self._LightEffect__onStopCallbackId = BigWorld.callback(self._LightEffect__duration, self.stop)
        
        self._LightEffect__isRunning = True

    
    def stop(self):
        if self._LightEffect__onStopCallbackId is not None:
            BigWorld.cancelCallback(self._LightEffect__onStopCallbackId)
            self._LightEffect__onStopCallbackId = None
        
        self.onStop(self)
        self._LightEffect__isRunning = False



