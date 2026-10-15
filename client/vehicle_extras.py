# Source Generated with Decompyle++
# File: vehicle_extras.pyc (Python 2.6)

import BigWorld
import random
import items
import constants
from Vibroeffects.Controllers.ShootingController import ShootingController
from debug_utils import *
from helpers import i18n
from helpers.EntityExtra import EntityExtra
import BattleReplay

def reload():
    modNames = (reload.__module__,)
    modules = modules
    import sys
    import __builtin__ as __builtin__
    for m in modNames:
        __builtin__.reload(modules[m])
    
    print 'vehicle_extras reloaded'


def _isAllowedToStart():
    replayCtrl = BattleReplay.g_replayCtrl
    if replayCtrl.isPlaying:
        pass
    return not (replayCtrl.isTimeWarpInProgress)


class NoneExtra(EntityExtra):
    
    def _start(self, data, args):
        debug_utils.LOG_CODEPOINT_WARNING()
        self.stop(data)


import Math
from functools import partial
from helpers.EffectsList import EffectsListPlayer

class ShowShooting(EntityExtra):
    
    def _start(self, data, burstCount):
        if not _isAllowedToStart():
            return None
        vehicle = data['entity']
        gunDescr = vehicle.typeDescriptor.gun
        (stages, effects, _) = gunDescr['effects']
        data['_effectsListPlayer'] = EffectsListPlayer(effects, stages)
        data['_burst'] = (burstCount, gunDescr['burst'][1])
        data['_gunModel'] = vehicle.appearance.modelsDesc['gun']['model']
        if vehicle.isPlayer:
            BigWorld.addAlwaysUpdateModel(data['_gunModel'])
        
        self._ShowShooting__doShot(data)

    
    def _cleanup(self, data):
        if data.get('_effectsListPlayer') is not None:
            data['_effectsListPlayer'].stop()
        
        timerID = data.get('_timerID')
        if timerID is not None:
            BigWorld.cancelCallback(timerID)
            data['_timerID'] = None
        
        if data['entity'].isPlayer and data.has_key('_gunModel'):
            BigWorld.delAlwaysUpdateModel(data['_gunModel'])
        

    
    def _ShowShooting__doShot(self, data):
        data['_timerID'] = None
        
        try:
            vehicle = data['entity']
            if not vehicle.isAlive():
                self.stop(data)
                return None
            (burstCount, burstInterval) = data['_burst']
            gunModel = data['_gunModel']
            effPlayer = data['_effectsListPlayer']
            effPlayer.stop()
            if burstCount == 1:
                effPlayer.play(gunModel, None, partial(self.stop, data))
                if data['entity'].isPlayer and burstInterval > 0:
                    data['_timerID'] = BigWorld.callback(0.5, partial(self._ShowShooting__notifyOnCompletionOfBurst, data))
                
            else:
                data['_burst'] = (burstCount - 1, burstInterval)
                data['_timerID'] = BigWorld.callback(burstInterval, partial(self._ShowShooting__doShot, data))
                effPlayer.play(gunModel)
                if data['entity'].isPlayer:
                    avatar = BigWorld.player()
                    avatar.getOwnVehicleShotDispersionAngle(avatar.gunRotator.turretRotationSpeed, 2)
                
            self._ShowShooting__doGroundWaveEffect(data, gunModel)
            appearance = vehicle.appearance
            appearance.gunRecoil.recoil()
            appearance.receiveShotImpulse(Math.Matrix(gunModel.matrix).applyVector(Math.Vector3(0, 0, -1)), vehicle.typeDescriptor.gun['impulse'])
            appearance.executeShootingVibrations(vehicle.typeDescriptor.shot['shell']['caliber'])
        except Exception:
            LOG_CURRENT_EXCEPTION()
            self.stop(data)


    
    def _ShowShooting__doGroundWaveEffect(self, data, gunModel):
        vehicle = data['entity']
        gunDescr = vehicle.typeDescriptor.gun
        if gunDescr['groundWave'] is None:
            return None
        node = gunModel.node('HP_gunFire')
        gunPos = Math.Matrix(node).translation
        upVec = Math.Matrix(vehicle.matrix).applyVector(Math.Vector3(0, 1, 0))
        if upVec.y != 0:
            centerToGun = gunPos - vehicle.position
            centerToGunDist = centerToGun.length
            centerToGun.normalise()
            gunHeight = centerToGunDist * centerToGun.dot(upVec) / upVec.y
            gunPos.y -= gunHeight
        
        testRes = BigWorld.wg_collideSegment(BigWorld.player().spaceID, gunPos + Math.Vector3(0, 0.5, 0), gunPos - Math.Vector3(0, 1.5, 0), 128)
        if testRes is None:
            return None
        position = testRes[0]
        (stages, effects, _) = gunDescr['groundWave']
        BigWorld.player().terrainEffects.addNew(position, effects, stages, None, dir = testRes[1], start = position + Math.Vector3(0, 0.5, 0), end = position - Math.Vector3(0, 0.5, 0))

    
    def _ShowShooting__notifyOnCompletionOfBurst(self, data):
        data['_timerID'] = None
        BigWorld.player().playShotResultNotification(None, None)



class DamageMarker(EntityExtra):
    
    def _readConfig(self, dataSection, containerName):
        self.deviceUserString = dataSection.readString('deviceUserString')
        if not self.deviceUserString:
            self._raiseWrongConfig('deviceUserString', containerName)
        
        self.deviceUserString = i18n.makeString(self.deviceUserString)
        soundSection = dataSection['sounds']
        self.sounds = { }
        for state in ('critical', 'destroyed', 'functional', 'fixed'):
            sound = soundSection.readString(state)
            if sound:
                self.sounds[state] = sound
                continue
        



class TrackHealth(DamageMarker):
    
    def _readConfig(self, dataSection, containerName):
        DamageMarker._readConfig(self, dataSection, containerName)
        self._TrackHealth__isLeft = dataSection.readBool('isLeft')
        functionalCanMoveState = 'functionalCanMove'
        self.sounds[functionalCanMoveState] = dataSection.readString('sounds/' + functionalCanMoveState)

    
    def _start(self, data, args):
        data['entity'].appearance.addCrashedTrack(self._TrackHealth__isLeft)

    
    def _cleanup(self, data):
        data['entity'].appearance.delCrashedTrack(self._TrackHealth__isLeft)



class Fire(EntityExtra):
    _SIRENE_SOUND_NAME = '/ingame_voice/notifications_VO/fire_started_FX'
    
    def _readConfig(self, dataSection, containerName):
        self.sounds = { }
        startSound = dataSection.readString('sounds/fireStarted')
        if startSound:
            self.sounds['critical'] = startSound
            self.sounds['destroyed'] = startSound
        else:
            self._raiseWrongConfig('sounds/fireStarted', containerName)
        stopSound = dataSection.readString('sounds/fireStopped')
        if stopSound:
            self.sounds['fixed'] = stopSound
        else:
            self._raiseWrongConfig('sounds/fireStopped', containerName)
        self.sireneSound = None

    
    def _start(self, data, args):
        data['_isStarted'] = False
        if not _isAllowedToStart():
            return None
        vehicle = data['entity']
        isUnderwater = vehicle.appearance.isUnderwater()
        data['wasUnderwater'] = isUnderwater
        if not isUnderwater:
            (stages, effects, _) = random.choice(vehicle.typeDescriptor.type.effects['flaming'])
            if len(stages) != 2 and stages[0][0] != 'fire' or stages[1][0] != 'noEmission':
                LOG_ERROR("Wrong stages in vehicle flaming effect. Should be 'fire' and 'noEmission'.", vehicle.typeDescriptor.name)
                self.stop(data)
                return None
            data['_noEmissionTime'] = stages[1][1]
            data['_effects'] = effects
            effects.attachTo(vehicle.appearance.modelsDesc['hull']['model'], data, 'fire')
        
        data['_isStarted'] = True
        self.sireneSound = vehicle.appearance.modelsDesc['hull']['model'].playSound(Fire._SIRENE_SOUND_NAME)
        vehicle.appearance.switchFireVibrations(True)

    
    def _cleanup(self, data):
        if not data['_isStarted']:
            return None
        vehicle = data['entity']
        vehicle.appearance.switchFireVibrations(False)
        if '_effects' in data:
            effects = data['_effects']
            if vehicle.health <= 0:
                effects.detachAllFrom(data)
                return None
            effects.detachFrom(data, 'fire')
            effects.attachTo(vehicle.appearance.modelsDesc['hull']['model'], data, 'noEmission')
            BigWorld.callback(data['_noEmissionTime'], partial(self._Fire__stop, data))
        
        if self.sireneSound is not None:
            self.sireneSound.stop()
            self.sireneSound = None
        

    
    def _Fire__stop(self, data):
        if '_effects' in data:
            data['_effects'].detachAllFrom(data)
        

    
    def checkUnderwater(self, data, vehicle, isVehicleUnderwater):
        wasUnderwater = data['wasUnderwater']
        if isVehicleUnderwater and not wasUnderwater:
            if '_effects' in data:
                effects = data['_effects']
                effects.detachAllFrom(data)
                del data['_effects']
            
        
        if not isVehicleUnderwater and wasUnderwater:
            (stages, effects, _) = random.choice(vehicle.typeDescriptor.type.effects['flaming'])
            data['_noEmissionTime'] = stages[1][1]
            data['_effects'] = effects
            effects.attachTo(vehicle.appearance.modelsDesc['hull']['model'], data, 'fire')
        
        data['wasUnderwater'] = isVehicleUnderwater



