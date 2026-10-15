# Source Generated with Decompyle++
# File: RoccatFxManager.pyc (Python 2.6)

import BigWorld
from AuxiliaryFx.FxController import IAuxiliaryVehicleFx

class ColorState:
    
    def __init__(self, zone, effect, speed, color):
        self.zone = zone
        self.effect = effect
        self.speed = speed
        self.color = color



class RoccatFxManager:
    ZONE_EVENT = 1
    ZONE_AMBIENT = 2
    EFFECT_OFF = 0
    EFFECT_ON = 1
    EFFECT_BLINKING = 2
    EFFECT_BREATHING = 3
    EFFECT_HEARTBEAT = 4
    SPEED_NOCHANGE = 0
    SPEED_SLOW = 1
    SPEED_NORMAL = 2
    SPEED_FAST = 3
    
    def __init__(self):
        self._RoccatFxManager__roccatFx = BigWorld.WGRoccatFx
        self._RoccatFxManager__isEnabled = False
        self._RoccatFxManager__roccatFx.setOnReadyCallback(self._RoccatFxManager__onRoccatReady)
        self._RoccatFxManager__roccatFx.initialize()
        self._RoccatFxManager__tempColorCallbackId = None
        self._RoccatFxManager__mainColorState = ColorState(0, 0, 0, (0, 0, 0))

    
    def destroy(self):
        if self._RoccatFxManager__isEnabled:
            self.resetBackground()
        
        self._RoccatFxManager__roccatFx.clearOnReadyCallback()
        self._RoccatFxManager__roccatFx = None
        if self._RoccatFxManager__tempColorCallbackId is not None:
            BigWorld.cancelCallback(self._RoccatFxManager__tempColorCallbackId)
        

    
    def _RoccatFxManager__onRoccatReady(self):
        self._RoccatFxManager__isEnabled = True
        self.resetBackground()

    
    def start(self):
        self.resetBackground()

    
    def isEnabled(self):
        return self._RoccatFxManager__isEnabled

    
    def setMainColors(self, zone, effect, speed, color):
        if not self.isEnabled():
            return None
        self._RoccatFxManager__mainColorState = ColorState(zone, effect, speed, color)
        self._RoccatFxManager__roccatFx.setColors(zone, effect, speed, color)

    
    def launchTempColors(self, zone, effect, speed, color, time):
        if not self.isEnabled():
            return None
        if self._RoccatFxManager__tempColorCallbackId is not None:
            BigWorld.cancelCallback(self._RoccatFxManager__tempColorCallbackId)
        
        self._RoccatFxManager__roccatFx.setColors(zone, effect, speed, color)
        self._RoccatFxManager__tempColorCallbackId = BigWorld.callback(time, self._RoccatFxManager__onTempColorStops)

    
    def _RoccatFxManager__onTempColorStops(self):
        self._RoccatFxManager__tempColorCallbackId = None
        self._RoccatFxManager__roccatFx.setColors(self._RoccatFxManager__mainColorState.zone, self._RoccatFxManager__mainColorState.effect, self._RoccatFxManager__mainColorState.speed, self._RoccatFxManager__mainColorState.color)

    
    def resetBackground(self):
        self.setMainColors(RoccatFxManager.ZONE_AMBIENT, RoccatFxManager.EFFECT_ON, RoccatFxManager.SPEED_SLOW, (255, 240, 0))

    
    def startInvitationEffect(self):
        self.setMainColors(RoccatFxManager.ZONE_EVENT, RoccatFxManager.EFFECT_BLINKING, RoccatFxManager.SPEED_FAST, (255, 255, 255))

    
    def stopInvitationEffect(self):
        self.resetBackground()

    
    def systemMessageEffect(self):
        self.launchTempColors(RoccatFxManager.ZONE_EVENT, RoccatFxManager.EFFECT_BREATHING, RoccatFxManager.SPEED_SLOW, (0, 0, 255), 3.5)

    
    def channelOpenedEffect(self):
        self.launchTempColors(RoccatFxManager.ZONE_EVENT, RoccatFxManager.EFFECT_HEARTBEAT, RoccatFxManager.SPEED_SLOW, (0, 255, 255), 5)

    
    def startTicksEffect(self):
        self.launchTempColors(RoccatFxManager.ZONE_EVENT, RoccatFxManager.EFFECT_BREATHING, RoccatFxManager.SPEED_FAST, (255, 255, 255), 30)

    
    def roundStartedEffect(self):
        self.launchTempColors(RoccatFxManager.ZONE_EVENT, RoccatFxManager.EFFECT_HEARTBEAT, RoccatFxManager.SPEED_SLOW, (0, 255, 0), 2)



class RoccatVehicleFx(IAuxiliaryVehicleFx):
    HEALTH_EFFECTS = [
        (9000, (RoccatFxManager.ZONE_AMBIENT, RoccatFxManager.EFFECT_ON, RoccatFxManager.SPEED_NORMAL, (0, 255, 0))),
        (0.6, (RoccatFxManager.ZONE_AMBIENT, RoccatFxManager.EFFECT_ON, RoccatFxManager.SPEED_NORMAL, (255, 255, 0))),
        (0.3, (RoccatFxManager.ZONE_AMBIENT, RoccatFxManager.EFFECT_ON, RoccatFxManager.SPEED_NORMAL, (255, 0, 0))),
        (0, (RoccatFxManager.ZONE_AMBIENT, RoccatFxManager.EFFECT_ON, RoccatFxManager.SPEED_NORMAL, (255, 255, 255)))]
    DEATH_EFFECT = (RoccatFxManager.ZONE_EVENT, RoccatFxManager.EFFECT_BLINKING, RoccatFxManager.SPEED_FAST, (255, 0, 0), 5)
    
    def __init__(self, vehicle, fxManager):
        IAuxiliaryVehicleFx.__init__(self, vehicle, fxManager)
        self._RoccatVehicleFx__prevHealth = vehicle.health
        effect = self._RoccatVehicleFx__getHealthEffect(vehicle.health, vehicle.typeDescriptor.maxHealth)
        self._fxManager.setMainColors(*effect)

    
    def destroy(self):
        self._fxManager.resetBackground()

    
    def _RoccatVehicleFx__getHealthEffect(self, health, maxHealth):
        durability = health * 1 / maxHealth
        healthEffect = RoccatVehicleFx.HEALTH_EFFECTS[0][1]
        for durabilityEffect in RoccatVehicleFx.HEALTH_EFFECTS:
            if durabilityEffect[0] < durability:
                break
            
            healthEffect = durabilityEffect[1]
        
        return healthEffect

    
    def update(self, vehicle):
        health = vehicle.health
        if health != self._RoccatVehicleFx__prevHealth:
            effect = self._RoccatVehicleFx__getHealthEffect(health, vehicle.typeDescriptor.maxHealth)
            self._fxManager.setMainColors(*effect)
        
        if health <= 0:
            self._fxManager.launchTempColors(*RoccatVehicleFx.DEATH_EFFECT)
        
        self._RoccatVehicleFx__prevHealth = health



