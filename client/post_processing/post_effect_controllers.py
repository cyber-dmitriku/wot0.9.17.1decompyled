# Source Generated with Decompyle++
# File: post_effect_controllers.pyc (Python 2.6)

import BigWorld
import Math
import Event
from PostProcessing.Effects import *
from debug_utils import *

class _PostProcessingEvents(object):
    
    def __init__(self):
        self.onFocalPlaneChanged = Event.Event()


g_postProcessingEvents = _PostProcessingEvents()

class IEffectController(object):
    
    def __init__(self):
        pass

    
    def enable(self):
        pass

    
    def disable(self):
        pass

    
    def create(self):
        pass

    
    def destroy(self):
        pass



class DofEffectCtrl(IEffectController):
    
    def __init__(self):
        IEffectController.__init__(self)
        self._DofEffectCtrl__relaxTime = 0.1

    
    def enable(self):
        g_postProcessingEvents.onFocalPlaneChanged += self._DofEffectCtrl__update

    
    def disable(self):
        g_postProcessingEvents.onFocalPlaneChanged -= self._DofEffectCtrl__update

    
    def _DofEffectCtrl__update(self):
        getFocalPoint = getFocalPoint
        import AvatarInputHandler.control_modes
        pos = getFocalPoint()
        if pos is None:
            pos = 0
        else:
            pos = (BigWorld.camera().position - pos).length
        farPlane = 1 / BigWorld.projection().farPlane
        offset = 2.5
        zNear = (pos - offset) * farPlane
        zFar = (pos + offset) * farPlane
        DepthOfField.zNear.set(zNear, self._DofEffectCtrl__relaxTime, True)
        DepthOfField.zFar.set(zFar, self._DofEffectCtrl__relaxTime, True)



class DofEffectManualDistanceCtrl(IEffectController):
    onDistanceChanged = Event.Event()
    
    def enable(self):
        DofEffectManualDistanceCtrl.onDistanceChanged += self._DofEffectManualDistanceCtrl__onDistanceChanged

    
    def disable(self):
        DofEffectManualDistanceCtrl.onDistanceChanged -= self._DofEffectManualDistanceCtrl__onDistanceChanged

    
    def _DofEffectManualDistanceCtrl__onDistanceChanged(self, distance):
        farPlane = 1 / BigWorld.projection().farPlane
        offset = 2.5
        zNear = (distance - offset) * farPlane
        zFar = (distance + offset) * farPlane
        DepthOfFieldUnit.zNear.set(zNear, 0.1, True)
        DepthOfFieldUnit.zFar.set(zFar, 0.1, True)



