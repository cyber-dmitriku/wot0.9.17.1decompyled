# Source Generated with Decompyle++
# File: EngineController.pyc (Python 2.6)

import BigWorld
import Vibroeffects.VibroManager as VibroManager
from debug_utils import *
from OnceController import OnceController
from Vibroeffects.EffectsSettings import EffectsSettings
import time

class EngineController:
    _EngineController__SWAMP = 0
    _EngineController__SAND = 1
    _EngineController__OTHER_TERRAIN = 2
    
    def __init__(self):
        self._EngineController__lastVehicleSpeed = 0
        self._EngineController__lastTime = None
        self._EngineController__accelerationStartTime = None
        self._EngineController__prevEnginePower = 0
        self._EngineController__movingEffect = VibroManager.g_instance.getEffect('move_low_veff')
        self._EngineController__turnLeftEffect = None
        self._EngineController__turnRightEffect = None
        self._EngineController__idleEffect = VibroManager.g_instance.getEffect('move_idle_veff')
        self._EngineController__accelerationEffect = VibroManager.g_instance.getEffect('move_acceleration_veff')
        self._EngineController__brakingEffect = VibroManager.g_instance.getEffect('move_braking_veff')
        getEffect = VibroManager.g_instance.getEffect
        self._EngineController__engineEffects = {
            EngineController._EngineController__SWAMP: {
                2: getEffect('move_swamp_low_veff'),
                3: getEffect('move_swamp_high_veff') },
            EngineController._EngineController__SAND: {
                2: getEffect('move_sand_low_veff'),
                3: getEffect('move_sand_high_veff') },
            EngineController._EngineController__OTHER_TERRAIN: {
                2: getEffect('move_low_veff'),
                3: getEffect('move_high_veff') } }
        self._EngineController__turn = ''
        self._EngineController__lastTurn = ''
        self._EngineController__startupApply()

    
    def destroy(self):
        self._EngineController__turnOffVibrations()

    
    def setTurn(self, value):
        self._EngineController__turn = value

    
    def _EngineController__checkAcceleration(self, vehicle):
        if self._EngineController__accelerationStartTime is None:
            pass
        1
        totalAccelerationTime = time.time() - self._EngineController__accelerationStartTime
        ACC_ENGINE_MODE = 3
        if vehicle.engineMode[0] == ACC_ENGINE_MODE and self._EngineController__prevEnginePower != ACC_ENGINE_MODE:
            VibroManager.g_instance.startEffect(self._EngineController__accelerationEffect)
            self._EngineController__accelerationStartTime = time.time()
        elif vehicle.engineMode[0] != ACC_ENGINE_MODE or self._EngineController__prevEnginePower == ACC_ENGINE_MODE or totalAccelerationTime > self._EngineController__accelerationEffect.getDuration():
            if self._EngineController__accelerationEffect.isRunning():
                VibroManager.g_instance.stopEffect(self._EngineController__accelerationEffect)
            
            if vehicle.engineMode[0] != ACC_ENGINE_MODE:
                self._EngineController__accelerationStartTime = None
            
        
        curSpeed = vehicle.getSpeed()
        curTime = BigWorld.time()
        deltaT = curTime - self._EngineController__lastTime
        acc = (curSpeed - self._EngineController__lastVehicleSpeed) / deltaT
        if acc <= EffectsSettings.DecelerationThreshold:
            VibroManager.g_instance.startEffect(self._EngineController__brakingEffect)
        else:
            VibroManager.g_instance.stopEffect(self._EngineController__brakingEffect)
        self._EngineController__lastVehicleSpeed = curSpeed
        self._EngineController__lastTime = curTime
        self._EngineController__prevEnginePower = vehicle.engineMode[0]

    
    def update(self, vehicle):
        if self._EngineController__lastTime is not None:
            self._EngineController__checkAcceleration(vehicle)
        else:
            self._EngineController__lastTime = BigWorld.time()
        enginePower = vehicle.engineMode[0]
        if enginePower == 0:
            self._EngineController__turnOffVibrations()
        elif enginePower == 1:
            self._EngineController__doApplyIdlePower()
        else:
            self._EngineController__doApplyNormalPower(vehicle)
        if self._EngineController__turn != self._EngineController__lastTurn:
            if self._EngineController__turn != 'left' and self._EngineController__turn != 'right':
                self._EngineController__turn = ''
            
            self._EngineController__lastTurn = self._EngineController__turn
            self._EngineController__doApplyTurn()
        

    
    def _EngineController__turnOffVibrations(self):
        VibroManager.g_instance.stopEffect(self._EngineController__movingEffect)
        VibroManager.g_instance.stopEffect(self._EngineController__idleEffect)
        VibroManager.g_instance.stopEffect(self._EngineController__accelerationEffect)
        VibroManager.g_instance.stopEffect(self._EngineController__brakingEffect)

    
    def _EngineController__startupApply(self):
        self._EngineController__turn = ''
        self._EngineController__lastTurn = ''
        self._EngineController__turnOffVibrations()

    
    def _EngineController__doApplyIdlePower(self):
        VibroManager.g_instance.startEffect(self._EngineController__idleEffect)
        VibroManager.g_instance.stopEffect(self._EngineController__movingEffect)

    
    def getMoveEffect(self, vehicle):
        terrainMaterialType = vehicle.appearance.getTerrainMatKind()[0]
        terrainType = EngineController._EngineController__OTHER_TERRAIN
        if vehicle.appearance.isInWater() or terrainMaterialType in (102,):
            terrainType = EngineController._EngineController__SWAMP
        elif terrainMaterialType in (103, 110):
            terrainType = EngineController._EngineController__SAND
        
        return self._EngineController__engineEffects[terrainType][vehicle.engineMode[0]]

    
    def _EngineController__doApplyNormalPower(self, vehicle):
        oldMoveEffect = self._EngineController__movingEffect
        self._EngineController__movingEffect = self.getMoveEffect(vehicle)
        if self._EngineController__movingEffect != oldMoveEffect:
            VibroManager.g_instance.stopEffect(oldMoveEffect)
        
        VibroManager.g_instance.startEffect(self._EngineController__movingEffect)
        VibroManager.g_instance.stopEffect(self._EngineController__idleEffect)

    
    def _EngineController__doApplyTurn(self):
        return None
        if self._EngineController__turn == 'left':
            VibroManager.g_instance.startEffect(self._EngineController__turnLeftEffect)
            VibroManager.g_instance.stopEffect(self._EngineController__turnRightEffect)
        elif self._EngineController__turn == 'right':
            VibroManager.g_instance.startEffect(self._EngineController__turnRightEffect)
            VibroManager.g_instance.stopEffect(self._EngineController__turnLeftEffect)
        else:
            VibroManager.g_instance.stopEffect(self._EngineController__turnLeftEffect)
            VibroManager.g_instance.stopEffect(self._EngineController__turnRightEffect)



