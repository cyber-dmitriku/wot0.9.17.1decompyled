# Source Generated with Decompyle++
# File: VehicleAppearance.pyc (Python 2.6)

import BigWorld
import ResMgr
import Math
import Pixie
import weakref
from constants import IS_DEVELOPMENT
from debug_utils import *
import vehicle_extras
from helpers import bound_effects
from helpers import DecalMap
from helpers.EffectsList import EffectsListPlayer
import items.vehicles as items
import random
import math
import time
from itertools import chain
from Event import Event
from functools import partial
import material_kinds
import Avatar
import VehicleStickers
import AuxiliaryFx
from constants import ARENA_PERIOD
from gui.WindowsManager import g_windowsManager
from Vibroeffects.ControllersManager import ControllersManager as VibrationControllersManager
from LightFx.LightControllersManager import LightControllersManager as LightFxControllersManager
import LightFx.LightManager as LightFx
_ENABLE_VEHICLE_VALIDATION = False
_VEHICLE_DISAPPEAR_TIME = 0.2
_VEHICLE_APPEAR_TIME = 0.2
_ROOT_NODE_NAME = 'V'
_GUN_RECOIL_NODE_NAME = 'G'
_PERIODIC_TIME = 0.25
_LOD_DISTANCE_SOUNDS = 80
_LOD_DISTANCE_EXHAUST = 200
_LOD_DISTANCE_TRAIL_PARTICLES = 100
_MOVE_THROUGH_WATER_SOUND = '/vehicles/tanks/water'
_TURRET_ROTATION_SOUND = '/vehicles/tanks/turrets/turret_mid'
_ENABLE_TURRET_ROTATION_SOUND = False
_TURRET_SOUND_MIN_YAW_SPEED = 0.01
_TURRET_SOUND_PREDICT_STOP_TIME = 0.2
_CAMOUFLAGE_MIN_INTENSITY = 1
_PITCH_SWINGING_MODIFIERS = (0.9, 1.88, 0.3, 4, 1, 1)
_ROUGHNESS_DECREASE_SPEEDS = (12, 18)
_ROUGHNESS_DECREASE_FACTOR = 0.4
_ROUGHNESS_DECREASE_FACTOR2 = 0.6
_FRICTION_ANG_FACTOR = 0.8
_FRICTION_ANG_BOUND = 0.5
_FRICTION_STRAFE_FACTOR = 0.4
_FRICTION_STRAFE_BOUND = 1
_MIN_DEPTH_FOR_HEAVY_SPLASH = 0.5

class SoundMaxPlaybacksChecker:
    
    def __init__(self, maxPaybacks, period = 0.25):
        self._SoundMaxPlaybacksChecker__maxPlaybacks = maxPaybacks
        self._SoundMaxPlaybacksChecker__period = period
        self._SoundMaxPlaybacksChecker__queue = []
        self._SoundMaxPlaybacksChecker__distRecalcId = None

    
    def __isSoundPlaying(sound):
        if sound.state.find('playing') != -1 and sound.state.find('error') == -1:
            pass
        return sound.state.find('stopped') == -1

    _SoundMaxPlaybacksChecker__isSoundPlaying = staticmethod(__isSoundPlaying)
    
    def _SoundMaxPlaybacksChecker__distRecalc(self):
        if not isinstance(BigWorld.player(), Avatar.PlayerAvatar):
            self._SoundMaxPlaybacksChecker__distRecalcId = None
            self.cleanup()
            return None
        self._SoundMaxPlaybacksChecker__distRecalcId = BigWorld.callback(self._SoundMaxPlaybacksChecker__period, self._SoundMaxPlaybacksChecker__distRecalc)
        cameraPos = BigWorld.camera().position
        for soundDistSq in self._SoundMaxPlaybacksChecker__queue:
            if not self._SoundMaxPlaybacksChecker__isSoundPlaying(soundDistSq[0]):
                soundDistSq[0] = None
                soundDistSq[1] = 0
                continue
            isinstance(BigWorld.player(), Avatar.PlayerAvatar)
            soundDistSq[1] = (cameraPos - soundDistSq[0].position).lengthSquared
        
        self._SoundMaxPlaybacksChecker__queue = filter((lambda x: x[0] is not None), self._SoundMaxPlaybacksChecker__queue)
        self._SoundMaxPlaybacksChecker__queue.sort(key = (lambda soundDistSq: soundDistSq[1]))

    
    def cleanup(self):
        self._SoundMaxPlaybacksChecker__queue = []
        if self._SoundMaxPlaybacksChecker__distRecalcId is not None:
            BigWorld.cancelCallback(self._SoundMaxPlaybacksChecker__distRecalcId)
            self._SoundMaxPlaybacksChecker__distRecalcId = None
        

    
    def checkAndPlay(self, newSound):
        if self._SoundMaxPlaybacksChecker__distRecalcId is None:
            self._SoundMaxPlaybacksChecker__distRecalc()
        
        cameraPos = BigWorld.camera().position
        newSoundDistSq = (cameraPos - newSound.position).lengthSquared
        for (sound, distSq) in self._SoundMaxPlaybacksChecker__queue:
            if sound is newSound:
                return None
        
        fullQueue = len(self._SoundMaxPlaybacksChecker__queue) == self._SoundMaxPlaybacksChecker__maxPlaybacks
        insertBeforeIdx = len(self._SoundMaxPlaybacksChecker__queue)
        while insertBeforeIdx >= 1:
            (sound, distSq) = self._SoundMaxPlaybacksChecker__queue[insertBeforeIdx - 1]
            if distSq < newSoundDistSq:
                break
            
            insertBeforeIdx -= 1
            continue
            sound is newSound
        if insertBeforeIdx < len(self._SoundMaxPlaybacksChecker__queue) or not fullQueue:
            toInsert = [
                newSound,
                newSoundDistSq]
            self._SoundMaxPlaybacksChecker__queue.insert(insertBeforeIdx, toInsert)
            if fullQueue:
                excessSound = self._SoundMaxPlaybacksChecker__queue.pop()[0]
                if excessSound is not None:
                    excessSound.stop()
                
            
            if not self._SoundMaxPlaybacksChecker__isSoundPlaying(newSound):
                newSound.play()
            
        

    
    def removeSound(self, sound):
        if sound is None:
            return None
        for (snd, _) in enumerate(self._SoundMaxPlaybacksChecker__queue):
            if snd == sound:
                del self._SoundMaxPlaybacksChecker__queue[idx]
                return None
        



class VehicleAppearance(object):
    VehicleSoundsChecker = SoundMaxPlaybacksChecker(6)
    gunRecoil = property((lambda self: self._VehicleAppearance__gunRecoil))
    fashion = property((lambda self: self._VehicleAppearance__fashion))
    
    def __init__(self):
        self.modelsDesc = {
            'chassis': {
                'model': None,
                'boundEffects': None,
                '_visibility': (True, True),
                '_fetchedModel': None,
                '_stateFunc': (lambda vehicle, state: vehicle.typeDescriptor.chassis['models'][state]),
                '_callbackFunc': '_VehicleAppearance__onChassisModelLoaded' },
            'hull': {
                'model': None,
                'boundEffects': None,
                '_visibility': (True, True),
                '_node': None,
                '_fetchedModel': None,
                '_stateFunc': (lambda vehicle, state: vehicle.typeDescriptor.hull['models'][state]),
                '_callbackFunc': '_VehicleAppearance__onHullModelLoaded' },
            'turret': {
                'model': None,
                'boundEffects': None,
                '_visibility': (True, True),
                '_node': None,
                '_fetchedModel': None,
                '_stateFunc': (lambda vehicle, state: vehicle.typeDescriptor.turret['models'][state]),
                '_callbackFunc': '_VehicleAppearance__onTurretModelLoaded' },
            'gun': {
                'model': None,
                'boundEffects': None,
                '_visibility': (True, True),
                '_fetchedModel': None,
                '_node': None,
                '_stateFunc': (lambda vehicle, state: vehicle.typeDescriptor.gun['models'][state]),
                '_callbackFunc': '_VehicleAppearance__onGunModelLoaded' } }
        self.turretMatrix = Math.WGAdaptiveMatrixProvider()
        self.gunMatrix = Math.WGAdaptiveMatrixProvider()
        self._VehicleAppearance__vehicle = None
        self._VehicleAppearance__skeletonCollider = None
        self._VehicleAppearance__engineSound = None
        self._VehicleAppearance__movementSound = None
        self._VehicleAppearance__waterHeight = -1
        self._VehicleAppearance__isInWater = False
        self._VehicleAppearance__isUnderWater = False
        self._VehicleAppearance__splashedWater = False
        self._VehicleAppearance__vibrationsCtrl = None
        self._VehicleAppearance__lightFxCtrl = None
        self._VehicleAppearance__auxiliaryFxCtrl = None
        self._VehicleAppearance__fashion = None
        self._VehicleAppearance__crashedTracksCtrl = None
        self._VehicleAppearance__gunRecoil = None
        self._VehicleAppearance__firstInit = True
        self._VehicleAppearance__curDamageState = None
        self._VehicleAppearance__loadingProgress = len(self.modelsDesc)
        self._VehicleAppearance__actualDamageState = None
        self._VehicleAppearance__invalidateLoading = False
        self._VehicleAppearance__exhaust = []
        self._VehicleAppearance__showStickers = True
        self._VehicleAppearance__effectsPlayer = None
        self._VehicleAppearance__engineMode = (0, 0)
        self._VehicleAppearance__swingMoveFlags = 0
        self._VehicleAppearance__engineSndVariation = [
            0,
            0]
        self._VehicleAppearance__exhaustDisabledByLOD = False
        self._VehicleAppearance__trailParticlesDisabled = False
        self._VehicleAppearance__trailParticles = { }
        self._VehicleAppearance__trackSounds = [
            None,
            None]
        self._VehicleAppearance__currTerrainMatKind = [
            -1,
            -1]
        self._VehicleAppearance__turretSound = None
        self._VehicleAppearance__prevTurretYaw = None
        self._VehicleAppearance__periodicTimerID = None
        self._VehicleAppearance__stickers = { }
        self.onModelChanged = Event()

    
    def getTerrainMatKind(self):
        return self._VehicleAppearance__currTerrainMatKind

    
    def isInWater(self):
        return self._VehicleAppearance__isInWater

    
    def isUnderwater(self):
        return self._VehicleAppearance__isUnderWater

    
    def _VehicleAppearance__calcIsUnderwater(self):
        if not self._VehicleAppearance__isInWater:
            return False
        chassisModel = self.modelsDesc['chassis']['model']
        turretOffs = self._VehicleAppearance__vehicle.typeDescriptor.chassis['hullPosition'] + self._VehicleAppearance__vehicle.typeDescriptor.hull['turretPositions'][0]
        turretOffsetMat = Math.Matrix()
        turretOffsetMat.setTranslate(turretOffs)
        turretJointMat = Math.Matrix(chassisModel.matrix)
        turretJointMat.preMultiply(turretOffsetMat)
        turretHeight = turretJointMat.translation.y - self._VehicleAppearance__vehicle.position.y
        return turretHeight < self._VehicleAppearance__waterHeight

    
    def prerequisites(self, vehicle):
        self._VehicleAppearance__curDamageState = self._VehicleAppearance__getDamageModelsState(vehicle.health)
        out = []
        for desc in self.modelsDesc.itervalues():
            out.append(desc['_stateFunc'](vehicle, self._VehicleAppearance__curDamageState))
        
        vDesc = vehicle.typeDescriptor
        out.append(vDesc.type.camouflageExclusionMask)
        customization = items.vehicles.g_cache.customization(vDesc.type.id[0])
        camouflageParams = self._VehicleAppearance__getCamouflageParams(vehicle)
        if camouflageParams is not None and customization is not None:
            camouflageId = camouflageParams[0]
            camouflageDesc = customization['camouflages'].get(camouflageId)
            if camouflageDesc is not None and camouflageDesc['texture'] != '':
                out.append(camouflageDesc['texture'])
                for tgDesc in (vDesc.turret, vDesc.gun):
                    exclMask = tgDesc.get('camouflageExclusionMask')
                    if exclMask is not None and exclMask != '':
                        out.append(exclMask)
                        continue
                
            
        
        return out

    
    def destroy(self):
        vehicle = self._VehicleAppearance__vehicle
        self._VehicleAppearance__vehicle = None
        if IS_DEVELOPMENT and _ENABLE_VEHICLE_VALIDATION and self._VehicleAppearance__validateCallbackId is not None:
            BigWorld.cancelCallback(self._VehicleAppearance__validateCallbackId)
            self._VehicleAppearance__validateCallbackId = None
        
        self._VehicleAppearance__skeletonCollider.destroy()
        if self._VehicleAppearance__engineSound is not None:
            VehicleAppearance.VehicleSoundsChecker.removeSound(self._VehicleAppearance__engineSound)
            self._VehicleAppearance__engineSound.stop()
            self._VehicleAppearance__engineSound = None
        
        if self._VehicleAppearance__movementSound is not None:
            VehicleAppearance.VehicleSoundsChecker.removeSound(self._VehicleAppearance__movementSound)
            self._VehicleAppearance__movementSound.stop()
            self._VehicleAppearance__movementSound = None
        
        if self._VehicleAppearance__turretSound is not None:
            self._VehicleAppearance__turretSound.stop()
            self._VehicleAppearance__turretSound = None
        
        if self._VehicleAppearance__vibrationsCtrl is not None:
            self._VehicleAppearance__vibrationsCtrl.destroy()
            self._VehicleAppearance__vibrationsCtrl = None
        
        if self._VehicleAppearance__lightFxCtrl is not None:
            self._VehicleAppearance__lightFxCtrl.destroy()
            self._VehicleAppearance__lightFxCtrl = None
        
        if self._VehicleAppearance__auxiliaryFxCtrl is not None:
            self._VehicleAppearance__auxiliaryFxCtrl.destroy()
            self._VehicleAppearance__auxiliaryFxCtrl = None
        
        self._VehicleAppearance__stopEffects()
        self._VehicleAppearance__detachTrailParticles()
        self._VehicleAppearance__destroyTrackDamageSounds()
        vehicle.stopHornSound(True)
        for desc in self.modelsDesc.iteritems():
            boundEffects = desc[1].get('boundEffects', None)
            if boundEffects is not None:
                boundEffects.destroy()
                continue
        
        if vehicle.isPlayer:
            player = BigWorld.player()
            if player.inputHandler is not None:
                arcadeCamera = player.inputHandler.ctrls['arcade'].camera
                if arcadeCamera is not None:
                    hull = self.modelsDesc['hull']['model']
                    turret = self.modelsDesc['turret']['model']
                    arcadeCamera.removeModelsToCollideWith((hull, turret))
                
            
        
        vehicle.model.delMotor(vehicle.model.motors[0])
        vehicle.filter.vehicleCollisionCallback = None
        vehicle.filter.isLaggingStateChangedCallback = None
        self._VehicleAppearance__stickers = None
        self.modelsDesc = None
        self.onModelChanged = None
        id = getattr(self, '_VehicleAppearance__stippleCallbackID', None)
        if id is not None:
            BigWorld.cancelCallback(id)
            self._VehicleAppearance__stippleCallbackID = None
        
        if self._VehicleAppearance__periodicTimerID is not None:
            BigWorld.cancelCallback(self._VehicleAppearance__periodicTimerID)
            self._VehicleAppearance__periodicTimerID = None
        
        self._VehicleAppearance__crashedTracksCtrl.destroy()
        self._VehicleAppearance__crashedTracksCtrl = None

    
    def start(self, vehicle, prereqs = None):
        self._VehicleAppearance__vehicle = vehicle
        descr = vehicle.typeDescriptor
        player = BigWorld.player()
        if prereqs is None:
            descr.chassis['hitTester'].loadBspModel()
            descr.hull['hitTester'].loadBspModel()
            descr.turret['hitTester'].loadBspModel()
        
        if vehicle.useAdvancedPhysics:
            filter = BigWorld.WGVehicleFilter2()
        else:
            filter = BigWorld.WGVehicleFilter()
        vehicle.filter = filter
        filter.vehicleWidth = descr.chassis['topRightCarryingPoint'][0] * 2
        filter.vehicleCollisionCallback = player.handleVehicleCollidedVehicle
        filter.isLaggingStateChangedCallback = self._VehicleAppearance__onIsLaggingStateChanged
        filter.vehicleMaxMove = descr.physics['speedLimits'][0] * 2
        filter.vehicleMinNormalY = descr.physics['minPlaneNormalY']
        for (p1, p2, p3) in descr.physics['carryingTriangles']:
            filter.addTriangle((p1[0], 0, p1[1]), (p2[0], 0, p2[1]), (p3[0], 0, p3[1]))
        
        self.turretMatrix.target = filter.turretMatrix
        self.gunMatrix.target = filter.gunMatrix
        self._VehicleAppearance__createGunRecoil()
        self._VehicleAppearance__createStickers(prereqs)
        self._VehicleAppearance__createExhaust()
        self._VehicleAppearance__skeletonCollider = _SkeletonCollider(vehicle, self)
        self._VehicleAppearance__crashedTracksCtrl = _CrashedTrackController(vehicle, self)
        self._VehicleAppearance__fashion = BigWorld.WGVehicleFashion()
        _setupVehicleFashion(self._VehicleAppearance__fashion, self._VehicleAppearance__vehicle)
        for desc in self.modelsDesc.itervalues():
            modelName = desc['_stateFunc'](vehicle, self._VehicleAppearance__curDamageState)
            if prereqs is not None:
                
                try:
                    desc['model'] = prereqs[modelName]
                except Exception:
                    LOG_ERROR("can't load model <%s> from prerequisites." % modelName)

                if desc['model'] is None:
                    desc['model'] = BigWorld.Model(desc['_stateFunc'](vehicle, 'undamaged'))
                
            else:
                desc['model'] = BigWorld.Model(modelName)
            desc['model'].outsideOnly = 1
            if desc.has_key('boundEffects'):
                desc['boundEffects'] = bound_effects.ModelBoundEffects(desc['model'])
                continue
        
        self._VehicleAppearance__setupModels()
        state = self._VehicleAppearance__curDamageState
        if state == 'destroyed':
            self._VehicleAppearance__playEffect('destruction', 'static')
        elif state == 'exploded':
            self._VehicleAppearance__playEffect('explosion', 'static')
        
        self._VehicleAppearance__firstInit = False
        if self._VehicleAppearance__invalidateLoading:
            self._VehicleAppearance__invalidateLoading = True
            self._VehicleAppearance__fetchModels(self._VehicleAppearance__actualDamageState)
        
        if vehicle.isAlive():
            turretModel = self.modelsDesc['turret']['model']
            self._VehicleAppearance__engineSound = _getSound(turretModel, descr.engine['sound'])
            self._VehicleAppearance__movementSound = _getSound(turretModel, descr.chassis['sound'])
            self._VehicleAppearance__isEngineSoundMutedByLOD = False
        
        if vehicle.isAlive() and self._VehicleAppearance__vehicle.isPlayer:
            self._VehicleAppearance__vibrationsCtrl = VibrationControllersManager()
            if LightFx.LightManager.g_instance is not None and LightFx.LightManager.g_instance.isEnabled():
                self._VehicleAppearance__lightFxCtrl = LightFxControllersManager(self._VehicleAppearance__vehicle)
            
            if AuxiliaryFx.g_instance is not None:
                self._VehicleAppearance__auxiliaryFxCtrl = AuxiliaryFx.g_instance.createFxController(self._VehicleAppearance__vehicle)
            
        
        vehicle.model.stipple = True
        self._VehicleAppearance__stippleCallbackID = BigWorld.callback(_VEHICLE_APPEAR_TIME, self._VehicleAppearance__disableStipple)
        self._VehicleAppearance__setupTrailParticles()
        self._VehicleAppearance__setupTrackDamageSounds()
        self._VehicleAppearance__periodicTimerID = BigWorld.callback(_PERIODIC_TIME * random.uniform(0.01, 1), self._VehicleAppearance__onPeriodicTimer)

    
    def showStickers(self, bool):
        self._VehicleAppearance__showStickers = bool
        for (compName, stickerDesc) in self._VehicleAppearance__stickers.iteritems():
            if bool:
                pass
            1
            alpha = 0
            stickerDesc['stickers'].setAlphas(alpha, alpha)
        

    
    def changeVisibility(self, modelName, modelVisible, attachmentsVisible):
        desc = self.modelsDesc.get(modelName, None)
        if desc is None:
            LOG_ERROR("invalid model's description name <%s>." % modelName)
        
        desc['model'].visible = modelVisible
        desc['model'].visibleAttachments = attachmentsVisible
        desc['_visibility'] = (modelVisible, attachmentsVisible)
        if modelName == 'chassis':
            self._VehicleAppearance__crashedTracksCtrl.setVisible(modelVisible)
        

    
    def onVehicleHealthChanged(self):
        vehicle = self._VehicleAppearance__vehicle
        if not vehicle.isAlive():
            BigWorld.wgDelEdgeDetectEntity(vehicle)
            if vehicle.health > 0:
                self.changeEngineMode((0, 0))
            elif self._VehicleAppearance__engineSound is not None:
                VehicleAppearance.VehicleSoundsChecker.removeSound(self._VehicleAppearance__engineSound)
                self._VehicleAppearance__engineSound.stop()
                self._VehicleAppearance__engineSound = None
            
            if self._VehicleAppearance__movementSound is not None:
                VehicleAppearance.VehicleSoundsChecker.removeSound(self._VehicleAppearance__movementSound)
                self._VehicleAppearance__movementSound.stop()
                self._VehicleAppearance__movementSound = None
            
            if self._VehicleAppearance__turretSound is not None:
                self._VehicleAppearance__turretSound.stop()
                self._VehicleAppearance__turretSound = None
            
        
        state = self._VehicleAppearance__getDamageModelsState(vehicle.health)
        if state != self._VehicleAppearance__curDamageState:
            if self._VehicleAppearance__loadingProgress == len(self.modelsDesc) and not (self._VehicleAppearance__firstInit):
                if state == 'undamaged':
                    self._VehicleAppearance__stopEffects()
                elif state == 'destroyed':
                    self._VehicleAppearance__playEffect('destruction')
                elif state == 'exploded':
                    self._VehicleAppearance__playEffect('explosion')
                
                self._VehicleAppearance__fetchModels(state)
            else:
                self._VehicleAppearance__actualDamageState = state
                self._VehicleAppearance__invalidateLoading = True
        

    
    def changeEngineMode(self, mode, forceSwinging = False):
        self._VehicleAppearance__engineMode = mode
        powerMode = mode[0]
        dirFlags = mode[1]
        self._VehicleAppearance__changeExhaust(powerMode)
        self._VehicleAppearance__updateBlockedMovement()
        sound = self._VehicleAppearance__engineSound
        if sound is not None:
            param = sound.param('load')
            if param is not None:
                if param.value != powerMode:
                    pass
                1
                param.value = 0 + 0.001
                self._VehicleAppearance__engineSndVariation = [
                    BigWorld.time() + 1,
                    False]
            
        
        if forceSwinging:
            flags = mode[1]
            prevFlags = self._VehicleAppearance__swingMoveFlags
            fashion = self.fashion
            moveMask = 3
            rotMask = 12
            if flags & moveMask ^ prevFlags & moveMask:
                swingPeriod = 2
                if flags & 1:
                    fashion.accelSwingingDirection = -1
                elif flags & 2:
                    fashion.accelSwingingDirection = 1
                else:
                    fashion.accelSwingingDirection = 0
            elif not (flags & moveMask) and flags & rotMask ^ prevFlags & rotMask:
                swingPeriod = 1
                fashion.accelSwingingDirection = 0
            else:
                swingPeriod = 0
            if swingPeriod > fashion.accelSwingingPeriod:
                fashion.accelSwingingPeriod = swingPeriod
            
            self._VehicleAppearance__swingMoveFlags = flags
        

    
    def stopSwinging(self):
        self.fashion.accelSwingingPeriod = 0

    
    def removeDamageSticker(self, code):
        for stickerDesc in self._VehicleAppearance__stickers.itervalues():
            dmgSticker = stickerDesc['damageStickers'].get(code)
            if dmgSticker is not None:
                if dmgSticker['handle'] is not None:
                    stickerDesc['stickers'].delDamageSticker(dmgSticker['handle'])
                
                del stickerDesc['damageStickers'][code]
                continue
        

    
    def addDamageSticker(self, code, componentName, stickerID, segStart, segEnd):
        stickerDesc = self._VehicleAppearance__stickers[componentName]
        if stickerDesc['damageStickers'].has_key(code):
            return None
        desc = items.vehicles.g_cache.damageStickers['descrs'][stickerID]
        texName = desc['texName']
        bumpTexName = desc['bumpTexName']
        segment = segEnd - segStart
        segLen = segment.lengthSquared
        if segLen != 0:
            segStart -= 0.25 * segment / math.sqrt(segLen)
        
        angle = random.random() * math.pi * 2
        rotAxis = 0
        for i in xrange(1, 3):
            if abs(segment[i]) > abs(segment[rotAxis]):
                rotAxis = i
                continue
            stickerDesc['damageStickers'].has_key(code)
        
        up = Math.Vector3()
        up[(rotAxis + 1) % 3] = math.sin(angle)
        up[(rotAxis + 2) % 3] = math.cos(angle)
        stickerDesc = self._VehicleAppearance__stickers[componentName]
        model = self.modelsDesc[componentName]['model']
        handle = stickerDesc['stickers'].addDamageSticker(texName, bumpTexName, segStart, segEnd, desc['modelSizes'], up)
        stickerDesc['damageStickers'][code] = {
            'rayStart': segStart,
            'rayEnd': segEnd,
            'up': up,
            'sizes': desc['modelSizes'],
            'handle': handle }

    
    def receiveShotImpulse(self, dir, impulse):
        if self._VehicleAppearance__curDamageState == 'undamaged':
            self._VehicleAppearance__fashion.receiveShotImpulse(dir, impulse)
            self._VehicleAppearance__crashedTracksCtrl.receiveShotImpulse(dir, impulse)
        

    
    def addCrashedTrack(self, isLeft):
        self._VehicleAppearance__crashedTracksCtrl.addTrack(isLeft)
        if not self._VehicleAppearance__vehicle.isEnteringWorld:
            if isLeft:
                pass
            1
            sound = 0[1]
            if sound is not None and sound[1] is not None:
                sound[1].play()
            
        

    
    def delCrashedTrack(self, isLeft):
        self._VehicleAppearance__crashedTracksCtrl.delTrack(isLeft)

    
    def _VehicleAppearance__fetchModels(self, modelState):
        self._VehicleAppearance__curDamageState = modelState
        self._VehicleAppearance__loadingProgress = 0
        for desc in self.modelsDesc.itervalues():
            BigWorld.fetchModel(desc['_stateFunc'](self._VehicleAppearance__vehicle, modelState), getattr(self, desc['_callbackFunc']))
        

    
    def _VehicleAppearance__attemptToSetupModels(self):
        self._VehicleAppearance__loadingProgress += 1
        if self._VehicleAppearance__loadingProgress == len(self.modelsDesc):
            if self._VehicleAppearance__invalidateLoading:
                self._VehicleAppearance__invalidateLoading = False
                self._VehicleAppearance__fetchModels(self._VehicleAppearance__actualDamageState)
            else:
                self._VehicleAppearance__setupModels()
        

    
    def _VehicleAppearance__setupModels(self):
        vehicle = self._VehicleAppearance__vehicle
        chassis = self.modelsDesc['chassis']
        hull = self.modelsDesc['hull']
        turret = self.modelsDesc['turret']
        gun = self.modelsDesc['gun']
        if not self._VehicleAppearance__firstInit:
            self._VehicleAppearance__detachStickers()
            delattr(gun['model'], 'wg_gunRecoil')
            self._VehicleAppearance__gunFireNode = None
            self._VehicleAppearance__attachExhaust(False)
            self._VehicleAppearance__detachTrailParticles()
            self._VehicleAppearance__destroyTrackDamageSounds()
            self._VehicleAppearance__skeletonCollider.detach()
            self._VehicleAppearance__crashedTracksCtrl.reset()
            chassis['model'].stopSoundsOnDestroy = False
            hull['model'].stopSoundsOnDestroy = False
            turret['model'].stopSoundsOnDestroy = False
            hull['_node'].detach(hull['model'])
            turret['_node'].detach(turret['model'])
            gun['_node'].detach(gun['model'])
            chassis['model'] = chassis['_fetchedModel']
            hull['model'] = hull['_fetchedModel']
            turret['model'] = turret['_fetchedModel']
            gun['model'] = gun['_fetchedModel']
            delattr(vehicle.model, 'wg_fashion')
            self._VehicleAppearance__reattachEffects()
        
        vehicle.model = None
        vehicle.model = chassis['model']
        vehicle.model.delMotor(vehicle.model.motors[0])
        matrix = vehicle.matrix
        matrix.notModel = True
        vehicle.model.addMotor(BigWorld.Servo(matrix))
        self._VehicleAppearance__assembleModels()
        self._VehicleAppearance__skeletonCollider.attach()
        if not self._VehicleAppearance__firstInit:
            chassis['boundEffects'].reattachTo(chassis['model'])
            hull['boundEffects'].reattachTo(hull['model'])
            turret['boundEffects'].reattachTo(turret['model'])
            gun['boundEffects'].reattachTo(gun['model'])
        
        modelsState = self._VehicleAppearance__curDamageState
        if modelsState == 'undamaged':
            self._VehicleAppearance__attachStickers()
            
            try:
                vehicle.model.wg_fashion = self._VehicleAppearance__fashion
            except:
                LOG_CURRENT_EXCEPTION()

            self._VehicleAppearance__attachExhaust(True)
            gun['model'].wg_gunRecoil = self._VehicleAppearance__gunRecoil
            self._VehicleAppearance__gunFireNode = gun['model'].node('HP_gunFire')
        elif modelsState == 'destroyed' or modelsState == 'exploded':
            self._VehicleAppearance__attachStickers(0.3, True)
        elif not False:
            raise AssertionError
        self._VehicleAppearance__updateCamouflage()
        self._VehicleAppearance__applyVisibility()
        self.onModelChanged()
        if 'observer' in vehicle.typeDescriptor.type.tags:
            vehicle.model.visible = False
            vehicle.model.visibleAttachments = False
        

    
    def _VehicleAppearance__reattachEffects(self):
        if self._VehicleAppearance__effectsPlayer is not None:
            self._VehicleAppearance__effectsPlayer.reattachTo(self.modelsDesc['hull']['model'])
        

    
    def _VehicleAppearance__playEffect(self, kind, *modifs):
        if self._VehicleAppearance__effectsPlayer is not None:
            self._VehicleAppearance__effectsPlayer.stop()
        
        if kind in ('explosion', 'destruction') and self.isUnderwater():
            return None
        vehicle = self._VehicleAppearance__vehicle
        effects = vehicle.typeDescriptor.type.effects[kind]
        if not effects:
            return None
        effects = random.choice(effects)
        self._VehicleAppearance__effectsPlayer = EffectsListPlayer(effects[1], effects[0], showShockWave = vehicle.isPlayer, showFlashBang = vehicle.isPlayer, start = vehicle.position + Math.Vector3(0, -1, 0), end = vehicle.position + Math.Vector3(0, 1, 0))
        self._VehicleAppearance__effectsPlayer.play(self.modelsDesc['hull']['model'], *modifs)

    
    def _VehicleAppearance__updateCamouflage(self):
        texture = ''
        colors = [
            0,
            0,
            0,
            0]
        weights = Math.Vector4(1, 0, 0, 0)
        camouflagePresent = False
        vDesc = self._VehicleAppearance__vehicle.typeDescriptor
        camouflageParams = self._VehicleAppearance__getCamouflageParams(self._VehicleAppearance__vehicle)
        customization = items.vehicles.g_cache.customization(vDesc.type.id[0])
        defaultTiling = None
        if camouflageParams is not None and customization is not None:
            camouflage = customization['camouflages'].get(camouflageParams[0])
            if camouflage is not None:
                camouflagePresent = True
                texture = camouflage['texture']
                colors = camouflage['colors']
                weights = Math.Vector4((colors[0] >> 24) / 255, (colors[1] >> 24) / 255, (colors[2] >> 24) / 255, (colors[3] >> 24) / 255)
                defaultTiling = camouflage['tiling'].get(vDesc.type.compactDescr)
            
        
        if self._VehicleAppearance__curDamageState != 'undamaged':
            weights *= 0.1
        
        if camouflageParams is not None:
            (_, camStartTime, camNumDays) = camouflageParams
            if camNumDays > 0:
                timeAmount = (time.time() - camStartTime) / camNumDays * 86400
                if timeAmount > 1:
                    weights *= _CAMOUFLAGE_MIN_INTENSITY
                elif timeAmount > 0:
                    weights *= (1 - timeAmount) * (1 - _CAMOUFLAGE_MIN_INTENSITY) + _CAMOUFLAGE_MIN_INTENSITY
                
            
        
        for descId in ('chassis', 'hull', 'turret', 'gun'):
            exclusionMap = vDesc.type.camouflageExclusionMask
            tiling = defaultTiling
            if tiling is None:
                tiling = vDesc.type.camouflageTiling
            
            model = self.modelsDesc[descId]['model']
            tgDesc = None
            if descId == 'turret':
                tgDesc = vDesc.turret
            elif descId == 'gun':
                tgDesc = vDesc.gun
            
            if tgDesc is not None:
                coeff = tgDesc.get('camouflageTiling')
                if coeff is not None:
                    if tiling is not None:
                        tiling = (tiling[0] * coeff[0], tiling[1] * coeff[1], tiling[2] * coeff[2], tiling[3] * coeff[3])
                    else:
                        tiling = coeff
                
                if tgDesc.has_key('camouflageExclusionMask'):
                    exclusionMap = tgDesc['camouflageExclusionMask']
                
            
            if camouflagePresent and exclusionMap != '':
                pass
            useCamouflage = texture != ''
            fashion = None
            if hasattr(model, 'wg_fashion'):
                fashion = model.wg_fashion
            elif hasattr(model, 'wg_gunRecoil'):
                fashion = model.wg_gunRecoil
            elif useCamouflage:
                fashion = BigWorld.WGBaseFashion()
                model.wg_baseFashion = BigWorld.WGBaseFashion()
            elif hasattr(model, 'wg_baseFashion'):
                delattr(model, 'wg_baseFashion')
            
            if fashion is not None:
                if useCamouflage:
                    fashion.setCamouflage(texture, exclusionMap, tiling, colors[0], colors[1], colors[2], colors[3], weights)
                else:
                    fashion.removeCamouflage()
        

    
    def _VehicleAppearance__getCamouflageParams(self, vehicle):
        vDesc = vehicle.typeDescriptor
        vehicleInfo = BigWorld.player().arena.vehicles.get(vehicle.id)
        if vehicleInfo is not None:
            camouflagePseudoname = vehicleInfo['events'].get('hunting', None)
            if camouflagePseudoname is not None:
                camouflIdsByNation = {
                    0: {
                        'black': 29,
                        'gold': 30,
                        'red': 31,
                        'silver': 32 },
                    1: {
                        'black': 25,
                        'gold': 26,
                        'red': 27,
                        'silver': 28 } }
                camouflIds = camouflIdsByNation.get(vDesc.type.id[0])
                if camouflIds is not None:
                    ret = camouflIds.get(camouflagePseudoname)
                    if ret is not None:
                        return (ret, time.time(), 100)
                
            
        
        arenaType = BigWorld.player().arena.arenaType
        camouflageKind = arenaType.vehicleCamouflageKind
        return vDesc.camouflages[camouflageKind]

    
    def _VehicleAppearance__stopEffects(self):
        if self._VehicleAppearance__effectsPlayer is not None:
            self._VehicleAppearance__effectsPlayer.stop()
        
        self._VehicleAppearance__effectsPlayer = None

    
    def _VehicleAppearance__updateWaterStatus(self):
        self._VehicleAppearance__waterHeight = BigWorld.wg_collideWater(self._VehicleAppearance__vehicle.position, self._VehicleAppearance__vehicle.position + Math.Vector3(0, 1, 0))
        self._VehicleAppearance__isInWater = self._VehicleAppearance__waterHeight != -1
        self._VehicleAppearance__isUnderWater = self._VehicleAppearance__calcIsUnderwater()
        wasSplashed = self._VehicleAppearance__splashedWater
        self._VehicleAppearance__splashedWater = False
        waterHitPoint = None
        if self._VehicleAppearance__isInWater:
            self._VehicleAppearance__splashedWater = True
            waterHitPoint = self._VehicleAppearance__vehicle.position + Math.Vector3(0, self._VehicleAppearance__waterHeight, 0)
        else:
            trPoint = self._VehicleAppearance__vehicle.typeDescriptor.chassis['topRightCarryingPoint']
            cornerPoints = [
                Math.Vector3(trPoint.x, 0, trPoint.y),
                Math.Vector3(trPoint.x, 0, -(trPoint.y)),
                Math.Vector3(-(trPoint.x), 0, -(trPoint.y)),
                Math.Vector3(-(trPoint.x), 0, trPoint.y)]
            vehMat = Math.Matrix(self._VehicleAppearance__vehicle.model.matrix)
            for cornerPoint in cornerPoints:
                pointToTest = vehMat.applyPoint(cornerPoint)
                dist = BigWorld.wg_collideWater(pointToTest, pointToTest + Math.Vector3(0, 1, 0))
                if dist != -1:
                    self._VehicleAppearance__splashedWater = True
                    waterHitPoint = pointToTest + Math.Vector3(0, dist, 0)
                    break
                    continue
            
        if self._VehicleAppearance__splashedWater and not wasSplashed:
            lightVelocityThreshold = self._VehicleAppearance__vehicle.typeDescriptor.type.collisionEffectVelocities['waterContact']
            heavyVelocityThreshold = self._VehicleAppearance__vehicle.typeDescriptor.type.heavyCollisionEffectVelocities['waterContact']
            vehicleVelocity = abs(self._VehicleAppearance__vehicle.filter.speedInfo.value[0])
            if vehicleVelocity >= lightVelocityThreshold:
                collRes = BigWorld.wg_collideSegment(self._VehicleAppearance__vehicle.spaceID, waterHitPoint, waterHitPoint + (0, -_MIN_DEPTH_FOR_HEAVY_SPLASH, 0), 18, (lambda matKind, collFlags, itemId, chunkId: collFlags & 8))
                deepEnough = collRes is None
                if vehicleVelocity < heavyVelocityThreshold or not deepEnough:
                    pass
                1
                effectName = 'waterCollisionHeavy'
                self._VehicleAppearance__vehicle.showCollisionEffect(waterHitPoint, effectName, Math.Vector3(0, 1, 0))
            
        
        if self.isUnderwater() and self._VehicleAppearance__effectsPlayer is not None:
            self._VehicleAppearance__effectsPlayer.stop()
        

    
    def _VehicleAppearance__onPeriodicTimer(self):
        self._VehicleAppearance__periodicTimerID = None
        
        try:
            self._VehicleAppearance__updateVibrations()
        except Exception:
            LOG_CURRENT_EXCEPTION()

        
        try:
            if self._VehicleAppearance__lightFxCtrl is not None:
                self._VehicleAppearance__lightFxCtrl.update(self._VehicleAppearance__vehicle)
            
            if self._VehicleAppearance__auxiliaryFxCtrl is not None:
                self._VehicleAppearance__auxiliaryFxCtrl.update(self._VehicleAppearance__vehicle)
            
            self._VehicleAppearance__updateWaterStatus()
        except:
            LOG_CURRENT_EXCEPTION()

        if not self._VehicleAppearance__vehicle.isAlive():
            self._VehicleAppearance__periodicTimerID = BigWorld.callback(_PERIODIC_TIME, self._VehicleAppearance__onPeriodicTimer)
            return None
        
        try:
            self._VehicleAppearance__distanceFromPlayer = (BigWorld.camera().position - self._VehicleAppearance__vehicle.position).length
            for extraData in self._VehicleAppearance__vehicle.extras.values():
                extra = extraData.get('extra', None)
                if isinstance(extra, vehicle_extras.Fire):
                    extra.checkUnderwater(extraData, self._VehicleAppearance__vehicle, self.isUnderwater())
                    break
                    continue
                self._VehicleAppearance__vehicle.isAlive()
            
            self._VehicleAppearance__updateCurrTerrainMatKinds()
            self._VehicleAppearance__updateMovementSounds()
            self._VehicleAppearance__updateTurretSound()
            self._VehicleAppearance__updateBlockedMovement()
            self._VehicleAppearance__updateEffectsLOD()
            self._VehicleAppearance__updateTrailParticles()
        except Exception:
            self._VehicleAppearance__vehicle.isAlive()
            LOG_CURRENT_EXCEPTION()
        except:
            self._VehicleAppearance__vehicle.isAlive()

        self._VehicleAppearance__periodicTimerID = BigWorld.callback(_PERIODIC_TIME, self._VehicleAppearance__onPeriodicTimer)

    
    def _VehicleAppearance__updateMovementSounds(self):
        vehicle = self._VehicleAppearance__vehicle
        isTooFar = self._VehicleAppearance__distanceFromPlayer > _LOD_DISTANCE_SOUNDS
        if isTooFar != self._VehicleAppearance__isEngineSoundMutedByLOD:
            self._VehicleAppearance__isEngineSoundMutedByLOD = isTooFar
            if isTooFar:
                if self._VehicleAppearance__engineSound is not None:
                    self._VehicleAppearance__engineSound.stop()
                
                if self._VehicleAppearance__movementSound is not None:
                    self._VehicleAppearance__movementSound.stop()
                
            else:
                self.changeEngineMode(self._VehicleAppearance__engineMode)
        
        if not isTooFar:
            if self._VehicleAppearance__engineSound is not None:
                VehicleAppearance.VehicleSoundsChecker.checkAndPlay(self._VehicleAppearance__engineSound)
            
            if self._VehicleAppearance__movementSound is not None:
                VehicleAppearance.VehicleSoundsChecker.checkAndPlay(self._VehicleAppearance__movementSound)
            
        
        time = BigWorld.time()
        sound = self._VehicleAppearance__engineSound
        powerMode = self._VehicleAppearance__engineMode[0]
        if sound is not None:
            param = sound.param('load')
            if param is not None:
                if param.value == 0 and param.value != powerMode:
                    seekSpeed = param.seekSpeed
                    param.seekSpeed = 0
                    param.value = powerMode
                    param.seekSpeed = seekSpeed
                    self._VehicleAppearance__engineSndVariation = [
                        time + 1,
                        False]
                
                if time >= self._VehicleAppearance__engineSndVariation[0]:
                    if powerMode >= 3:
                        if self._VehicleAppearance__engineSndVariation[1]:
                            self._VehicleAppearance__engineSndVariation[1] = False
                            param.value = powerMode + (random.random() * 0.1 - 0.05)
                        elif random.random() < 0.35:
                            peak = random.random() * 0.35 + 0.1
                            self._VehicleAppearance__engineSndVariation[0] = time + peak * 0.9
                            self._VehicleAppearance__engineSndVariation[1] = True
                            param.value = powerMode + peak
                        
                    elif powerMode >= 2:
                        self._VehicleAppearance__engineSndVariation[0] = time + random.choice((0.5, 0.25, 0.75, 0.25))
                        value = param.value + (random.random() * 0.17 - 0.085)
                        value = min(value, powerMode + 0.25)
                        value = max(value, powerMode - 0.1)
                        param.value = value
                    
                
            
        
        self._VehicleAppearance__updateTrackSounds()

    EFFECT_MATERIALS_HARDNESS = {
        'ground': 0.1,
        'stone': 1,
        'wood': 0.5,
        'snow': 0.3,
        'sand': 0,
        'water': 0.2 }
    
    def _VehicleAppearance__updateTrackSounds(self):
        sound = self._VehicleAppearance__movementSound
        if sound is None:
            return None
        filter = self._VehicleAppearance__vehicle.filter
        if self._VehicleAppearance__vehicle.useAdvancedPhysics:
            isFlyingParam = sound.param('flying')
            if isFlyingParam is not None:
                contactsWithGround = filter.numLeftTrackContacts + filter.numRightTrackContacts
                if contactsWithGround > 0:
                    pass
                1
                isFlyingParam.value = 1
            
        
        speedFraction = filter.speedInfo.value[0]
        speedFraction = abs(speedFraction / self._VehicleAppearance__vehicle.typeDescriptor.physics['speedLimits'][0])
        param = sound.param('speed')
        if param is not None:
            param.value = min(1, speedFraction)
        
        if not self._VehicleAppearance__vehicle.isPlayer:
            toZeroParams = VehicleAppearance.EFFECT_MATERIALS_HARDNESS.keys()
            toZeroParams += [
                'hardness',
                'friction',
                'roughness']
            for paramName in toZeroParams:
                param = sound.param(paramName)
                if param is not None:
                    param.value = 0
                    continue
                sound is None
            
            return None
        matEffectsUnderTracks = dict((lambda .0: for effectMaterial in .0:
(effectMaterial, 0))(VehicleAppearance.EFFECT_MATERIALS_HARDNESS))
        powerMode = self._VehicleAppearance__engineMode[0]
        if self._VehicleAppearance__isInWater and powerMode > 1 and speedFraction > 0.01:
            matEffectsUnderTracks['water'] = len(self._VehicleAppearance__currTerrainMatKind)
        else:
            for matKind in self._VehicleAppearance__currTerrainMatKind:
                effectIndex = VehicleAppearance.calcEffectMaterialIndex(matKind)
                if effectIndex is not None:
                    effectMaterial = material_kinds.EFFECT_MATERIALS[effectIndex]
                    matEffectsUnderTracks[effectMaterial] = matEffectsUnderTracks.get(effectMaterial, 0) + 1
                    continue
            
        hardness = 0
        for (effectMaterial, amount) in matEffectsUnderTracks.iteritems():
            param = sound.param(effectMaterial)
            if param is not None:
                param.value = amount / len(self._VehicleAppearance__currTerrainMatKind)
            
            hardness += VehicleAppearance.EFFECT_MATERIALS_HARDNESS.get(effectMaterial, 0) * amount
        
        hardnessParam = sound.param('hardness')
        if hardnessParam is not None:
            hardnessParam.value = hardness / len(self._VehicleAppearance__currTerrainMatKind)
        
        if self._VehicleAppearance__vehicle.useAdvancedPhysics:
            strafeParam = sound.param('friction')
            if strafeParam is not None:
                angPart = min(abs(filter.angularSpeed) * _FRICTION_ANG_FACTOR, _FRICTION_ANG_BOUND)
                strafePart = min(abs(filter.strafeSpeed) * _FRICTION_STRAFE_FACTOR, _FRICTION_STRAFE_BOUND)
                frictionValue = max(angPart, strafePart)
                strafeParam.value = frictionValue
            
            roughnessParam = sound.param('roughness')
            if roughnessParam is not None:
                speed = filter.speedInfo.value[2]
                rds = _ROUGHNESS_DECREASE_SPEEDS
                decFactor = (speed - rds[0]) / (rds[1] - rds[0])
                if decFactor <= 0:
                    pass
                1
                if decFactor <= 1:
                    pass
                1
                decFactor = 1
                subs = _ROUGHNESS_DECREASE_FACTOR2 * decFactor
                decFactor = 1 - (1 - _ROUGHNESS_DECREASE_FACTOR) * decFactor
                surfaceCurvature = filter.suspCompressionRate
                roughness = max(0, min((surfaceCurvature * 2 * speedFraction - subs) * decFactor, 1))
                roughnessParam.value = roughness
            
        

    
    def _VehicleAppearance__updateTurretSound(self):
        if not _ENABLE_TURRET_ROTATION_SOUND:
            return None
        gunRotator = BigWorld.player().gunRotator
        currYaw = Math.Matrix(gunRotator.turretMatrix).yaw
        if self._VehicleAppearance__prevTurretYaw is None:
            self._VehicleAppearance__prevTurretYaw = currYaw
            return None
        prevParamValue = 0
        if self._VehicleAppearance__turretSound is not None:
            param = self._VehicleAppearance__turretSound.param('speed')
            if param is not None:
                prevParamValue = param.value
            
        
        yawSpeed = abs(currYaw - self._VehicleAppearance__prevTurretYaw) / _PERIODIC_TIME
        if yawSpeed >= _TURRET_SOUND_MIN_YAW_SPEED and gunRotator.estimatedTurretRotationTime > _TURRET_SOUND_PREDICT_STOP_TIME:
            if self._VehicleAppearance__turretSound is None:
                self._VehicleAppearance__turretSound = _getSound(self.modelsDesc['turret']['model'], _TURRET_ROTATION_SOUND)
                self._VehicleAppearance__turretSound.play()
            elif prevParamValue > 1:
                _seekSoundParam(self._VehicleAppearance__turretSound, 'speed', 0)
            
        elif self._VehicleAppearance__turretSound is not None:
            if prevParamValue < 2:
                _seekSoundParam(self._VehicleAppearance__turretSound, 'speed', 2)
            
        
        self._VehicleAppearance__prevTurretYaw = currYaw

    
    def _VehicleAppearance__updateBlockedMovement(self):
        blockingForce = 0
        (powerMode, dirFlags) = self._VehicleAppearance__engineMode
        vehSpeed = self._VehicleAppearance__vehicle.filter.speedInfo.value[0]
        if abs(vehSpeed) < 0.25 and powerMode > 1:
            if dirFlags & 1:
                blockingForce = -0.5
            elif dirFlags & 2:
                blockingForce = 0.5
            
        

    
    def _VehicleAppearance__updateEffectsLOD(self):
        disableExhaust = self._VehicleAppearance__distanceFromPlayer > _LOD_DISTANCE_EXHAUST
        if disableExhaust != self._VehicleAppearance__exhaustDisabledByLOD:
            self._VehicleAppearance__exhaustDisabledByLOD = disableExhaust
            self._VehicleAppearance__changeExhaust(self._VehicleAppearance__engineMode[0])
        
        if not self._VehicleAppearance__distanceFromPlayer > _LOD_DISTANCE_TRAIL_PARTICLES:
            pass
        disableTrails = not BigWorld.wg_isVehicleDustEnabled()
        if disableTrails != self._VehicleAppearance__trailParticlesDisabled:
            self._VehicleAppearance__trailParticlesDisabled = disableTrails
            if disableTrails:
                self._VehicleAppearance__detachTrailParticles()
            
        

    
    def _VehicleAppearance__setupTrailParticles(self):
        model = self.modelsDesc['chassis']['model']
        trPoint = self._VehicleAppearance__vehicle.typeDescriptor.chassis['topRightCarryingPoint']
        mMidLeft = Math.Matrix()
        mMidLeft.setTranslate((-trPoint[0], 0, 0))
        mMidRight = Math.Matrix()
        mMidRight.setTranslate((trPoint[0], 0, 0))
        self._VehicleAppearance__trailParticleNodes = [
            model.node('', mMidLeft),
            model.node('', mMidRight)]
        i = 0
        for nodeName in ('HP_Track_LFront', 'HP_Track_RFront', 'HP_Track_LRear', 'HP_Track_RRear'):
            node = None
            
            try:
                identity = Math.Matrix()
                identity.setIdentity()
                node = model.node(nodeName, identity)
            except:
                if i % 2 == 0:
                    pass
                1
                matr = mMidRight
                node = model.node('', Math.Matrix(matr))

            self._VehicleAppearance__trailParticleNodes.append(node)
        
        self._VehicleAppearance__trailParticlesDelayBeforeShow = BigWorld.time() + 4

    
    def _VehicleAppearance__detachTrailParticles(self):
        for node in self._VehicleAppearance__trailParticles.iterkeys():
            for trail in self._VehicleAppearance__trailParticles[node]:
                node.detach(trail[0])
            
        
        self._VehicleAppearance__trailParticles = { }

    
    def _VehicleAppearance__setupTrackDamageSounds(self):
        for i in xrange(2):
            
            try:
                fakeModel = BigWorld.player().newFakeModel()
                self._VehicleAppearance__trailParticleNodes[i].attach(fakeModel)
                self._VehicleAppearance__trackSounds[i] = (fakeModel, fakeModel.getSound('/hits/hits/hit_treads'))
            continue
            self._VehicleAppearance__trackSounds[i] = None
            LOG_CURRENT_EXCEPTION()
            continue

        

    
    def _VehicleAppearance__destroyTrackDamageSounds(self):
        for i in xrange(2):
            if self._VehicleAppearance__trackSounds[i] is not None:
                self._VehicleAppearance__trailParticleNodes[i].detach(self._VehicleAppearance__trackSounds[i][0])
                continue
        
        self._VehicleAppearance__trackSounds = [
            None,
            None]

    
    def _VehicleAppearance__updateCurrTerrainMatKinds(self):
        for iTrack in xrange(2):
            centerNode = self._VehicleAppearance__trailParticleNodes[iTrack]
            mMidNode = Math.Matrix(centerNode)
            testPoint = mMidNode.translation
            res = BigWorld.wg_collideSegment(self._VehicleAppearance__vehicle.spaceID, testPoint + (0, 2, 0), testPoint + (0, -2, 0), 18)
            if res is not None:
                pass
            1
            self._VehicleAppearance__currTerrainMatKind[iTrack] = 0
        
        self._VehicleAppearance__fashion.setCurrTerrainMatKinds(self._VehicleAppearance__currTerrainMatKind[0], self._VehicleAppearance__currTerrainMatKind[1])

    
    def _VehicleAppearance__updateTrailParticles(self):
        if self._VehicleAppearance__trailParticlesDisabled:
            return None
        if self._VehicleAppearance__vehicle.typeDescriptor.chassis['effects'] is None:
            self._VehicleAppearance__trailParticlesDisabled = True
            return None
        time = BigWorld.time()
        if time < self._VehicleAppearance__trailParticlesDelayBeforeShow:
            return None
        movementInfo = Math.Vector4(self._VehicleAppearance__fashion.movementInfo.value)
        maxMovement = self._VehicleAppearance__fashion.maxMovement
        for iTrack in xrange(2):
            trackSpeedRel = movementInfo[iTrack + 1] / maxMovement
            tooSlow = abs(self._VehicleAppearance__vehicle.filter.speedInfo.value[2]) < 0.1
            centerNode = self._VehicleAppearance__trailParticleNodes[iTrack]
            if trackSpeedRel <= 0:
                pass
            1
            activeCornerNode = 2 + iTrack[0 + 2]
            if trackSpeedRel > 0:
                pass
            1
            inactiveCornerNode = 2 + iTrack[0 + 2]
            if self._VehicleAppearance__isInWater:
                pass
            1
            currMatKind = self._VehicleAppearance__currTerrainMatKind[iTrack]
            if not self._VehicleAppearance__isInWater:
                pass
            1
            waterHeight = self._VehicleAppearance__waterHeight
            prevCenterNodeTranslation = centerNode.local.translation
            centerNode.local.translation = Math.Vector3(prevCenterNodeTranslation.x, waterHeight, prevCenterNodeTranslation.z)
            if self._VehicleAppearance__isInWater:
                activeToCenterShift = self._VehicleAppearance__vehicle.position.y - Math.Matrix(activeCornerNode).translation.y - activeCornerNode.local.translation.y
                activeCornerNode.local.translation = Math.Vector3(0, waterHeight + activeToCenterShift, 0)
                inactiveToCenterShift = self._VehicleAppearance__vehicle.position.y - Math.Matrix(inactiveCornerNode).translation.y - inactiveCornerNode.local.translation.y
                inactiveCornerNode.local.translation = Math.Vector3(0, waterHeight + inactiveToCenterShift, 0)
            else:
                activeCornerNode.local.translation = Math.Vector3(0, 0, 0)
                inactiveCornerNode.local.translation = Math.Vector3(0, 0, 0)
            currEffectIndex = VehicleAppearance.calcEffectMaterialIndex(currMatKind)
            if not tooSlow and not self.isUnderwater():
                self._VehicleAppearance__createTrailParticlesIfNeeded(centerNode, iTrack, 'dust', currEffectIndex, 100 + iTrack, True)
                self._VehicleAppearance__createTrailParticlesIfNeeded(activeCornerNode, iTrack, 'mud', currEffectIndex, 102 + iTrack, True)
                self._VehicleAppearance__createTrailParticlesIfNeeded(inactiveCornerNode, iTrack, 'mud', currEffectIndex, 102 + iTrack, False)
            
            for node in (centerNode, activeCornerNode, inactiveCornerNode):
                nodeEffects = self._VehicleAppearance__trailParticles.get(node)
                if nodeEffects is not None:
                    for nodeEffect in nodeEffects:
                        createdForActiveNode = nodeEffect[5]
                        if (node == activeCornerNode or not createdForActiveNode) and node == inactiveCornerNode:
                            pass
                        stopParticlesOnDirChange = createdForActiveNode
                        if not nodeEffect[1] != currEffectIndex and stopParticlesOnDirChange and self.isUnderwater():
                            pass
                        stopParticles = tooSlow
                        if stopParticles:
                            pass
                        1
                        relEmissionRate = -0.25 + 0.25
                        relEmissionRate = min(relEmissionRate, 1)
                        relEmissionRate = max(relEmissionRate, 0)
                        nodeEffect[2] = relEmissionRate
                        pixie = nodeEffect[0]
                        emissionRate = 150 * relEmissionRate * abs(trackSpeedRel)
                        emissionRate = min(emissionRate, 1)
                        basicEmissionRates = nodeEffect[4]
                        for i in xrange(pixie.nSystems()):
                            if basicEmissionRates[i] < 0:
                                source = pixie.system(i).action(16)
                                source.MultRate(emissionRate)
                                continue
                            nodeEffect[2]
                            source = pixie.system(i).action(1)
                            source.rate = emissionRate * basicEmissionRates[i]
                        
                    
                0
            
            for (node, nodeEffects) in self._VehicleAppearance__trailParticles.iteritems():
                for nodeEffect in nodeEffects:
                    effectInactive = abs(nodeEffect[2] * trackSpeedRel) < 0.0001
                    if effectInactive:
                        timeOfStop = nodeEffect[3]
                        if timeOfStop == 0:
                            nodeEffect[3] = time
                        elif time - timeOfStop > 5:
                            pixie = nodeEffect[0]
                            node.detach(pixie)
                            nodeEffects.remove(nodeEffect)
                        
                    timeOfStop == 0
                    nodeEffect[3] = 0
                
            
        

    
    def switchFireVibrations(self, bStart):
        if self._VehicleAppearance__vibrationsCtrl is not None:
            self._VehicleAppearance__vibrationsCtrl.switchFireVibrations(bStart)
        

    
    def executeHitVibrations(self, shotResult):
        if self._VehicleAppearance__vibrationsCtrl is not None:
            self._VehicleAppearance__vibrationsCtrl.executeHitVibrations(shotResult)
        

    
    def executeRammingVibrations(self, matKind = None):
        if self._VehicleAppearance__vibrationsCtrl is not None:
            self._VehicleAppearance__vibrationsCtrl.executeRammingVibrations(self._VehicleAppearance__vehicle.getSpeed(), matKind)
        

    
    def executeShootingVibrations(self, caliber):
        if self._VehicleAppearance__vibrationsCtrl is not None:
            self._VehicleAppearance__vibrationsCtrl.executeShootingVibrations(caliber)
        

    
    def executeCriticalHitVibrations(self, vehicle, extrasName):
        if self._VehicleAppearance__vibrationsCtrl is not None:
            self._VehicleAppearance__vibrationsCtrl.executeCriticalHitVibrations(vehicle, extrasName)
        

    
    def _VehicleAppearance__updateVibrations(self):
        if self._VehicleAppearance__vibrationsCtrl is None:
            return None
        vehicle = self._VehicleAppearance__vehicle
        crashedTrackCtrl = self._VehicleAppearance__crashedTracksCtrl
        self._VehicleAppearance__vibrationsCtrl.update(vehicle, crashedTrackCtrl.isLeftTrackBroken(), crashedTrackCtrl.isRightTrackBroken())

    
    def calcEffectMaterialIndex(matKind):
        if matKind != 0:
            return material_kinds.EFFECT_MATERIAL_INDEXES_BY_IDS.get(matKind)
        effectIndex = -1
        player = BigWorld.player()
        if isinstance(player, Avatar.PlayerAvatar):
            arenaSpecificEffect = player.arena.arenaType.defaultGroundEffect
            if arenaSpecificEffect is not None:
                if arenaSpecificEffect == 'None':
                    return None
                if not isinstance(arenaSpecificEffect, int):
                    effectIndex = material_kinds.EFFECT_MATERIAL_INDEXES_BY_NAMES.get(arenaSpecificEffect)
                    if effectIndex is None:
                        pass
                    1
                    effectIndex = effectIndex
                    player.arena.arenaType.defaultGroundEffect = effectIndex
                else:
                    effectIndex = arenaSpecificEffect
            
        
        return effectIndex

    calcEffectMaterialIndex = staticmethod(calcEffectMaterialIndex)
    
    def _VehicleAppearance__createTrailParticlesIfNeeded(self, node, iTrack, effectGroup, effectIndex, drawOrder, isActiveNode):
        if effectIndex is None:
            return None
        effectDesc = self._VehicleAppearance__vehicle.typeDescriptor.chassis['effects'].get(effectGroup)
        if effectDesc is None:
            return None
        effectName = effectDesc[0].get(effectIndex)
        if effectName is None and effectName == 'none' or effectName == 'None':
            return None
        if isinstance(effectName, list):
            effectIdx = iTrack
            if isActiveNode:
                pass
            1
            0 += 2
            effectName = effectName[effectIdx]
        
        nodeEffects = self._VehicleAppearance__trailParticles.get(node)
        if nodeEffects is None:
            nodeEffects = []
            self._VehicleAppearance__trailParticles[node] = nodeEffects
        else:
            for nodeEffect in nodeEffects:
                createdForActiveNode = nodeEffect[5]
                if nodeEffect[1] == effectIndex and createdForActiveNode == isActiveNode:
                    return None
            
        pixie = Pixie.create(effectName)
        pixie.drawOrder = drawOrder
        node.attach(pixie)
        basicRates = []
        for i in xrange(pixie.nSystems()):
            
            try:
                source = pixie.system(i).action(1)
                basicRates.append(source.rate)
            continue
            effectName == 'None'
            effectDesc is None
            basicRates.append(-1)
            continue

        
        nodeEffects.append([
            pixie,
            effectIndex,
            0,
            0,
            basicRates,
            isActiveNode])

    
    def _VehicleAppearance__getDamageModelsState(self, vehicleHealth):
        if vehicleHealth > 0:
            return 'undamaged'
        if vehicleHealth == 0:
            return 'destroyed'
        return 'exploded'

    
    def _VehicleAppearance__onChassisModelLoaded(self, model):
        self._VehicleAppearance__onModelLoaded('chassis', model)

    
    def _VehicleAppearance__onHullModelLoaded(self, model):
        self._VehicleAppearance__onModelLoaded('hull', model)

    
    def _VehicleAppearance__onTurretModelLoaded(self, model):
        self._VehicleAppearance__onModelLoaded('turret', model)

    
    def _VehicleAppearance__onGunModelLoaded(self, model):
        self._VehicleAppearance__onModelLoaded('gun', model)

    
    def _VehicleAppearance__onModelLoaded(self, name, model):
        if self.modelsDesc is None:
            return None
        desc = self.modelsDesc[name]
        if model is not None:
            desc['_fetchedModel'] = model
        else:
            desc['_fetchedModel'] = desc['model']
            modelState = desc['_stateFunc'](self._VehicleAppearance__vehicle, self._VehicleAppearance__curDamageState)
            LOG_ERROR('Model %s not loaded.' % modelState)
        self._VehicleAppearance__attemptToSetupModels()

    
    def _VehicleAppearance__assembleModels(self):
        vehicle = self._VehicleAppearance__vehicle
        hull = self.modelsDesc['hull']
        turret = self.modelsDesc['turret']
        gun = self.modelsDesc['gun']
        
        try:
            hull['_node'] = vehicle.model.node(_ROOT_NODE_NAME)
            hull['_node'].attach(hull['model'])
            turret['_node'] = hull['model'].node('HP_turretJoint', self.turretMatrix)
            turret['_node'].attach(turret['model'])
            gun['_node'] = turret['model'].node('HP_gunJoint', self.gunMatrix)
            gun['_node'].attach(gun['model'])
            if vehicle.isPlayer:
                player = BigWorld.player()
                if player.inputHandler is not None:
                    arcadeCamera = player.inputHandler.ctrls['arcade'].camera
                    if arcadeCamera is not None:
                        arcadeCamera.addModelsToCollideWith([
                            hull['model'],
                            turret['model']])
                    
                
        except Exception:
            LOG_ERROR('Can not assemble models for %s.' % vehicle.typeDescriptor.name)
            raise 

        if IS_DEVELOPMENT and _ENABLE_VEHICLE_VALIDATION:
            self._VehicleAppearance__validateCallbackId = BigWorld.callback(0.01, self._VehicleAppearance__validateAssembledModel)
        

    
    def _VehicleAppearance__applyVisibility(self):
        vehicle = self._VehicleAppearance__vehicle
        chassis = self.modelsDesc['chassis']
        hull = self.modelsDesc['hull']
        turret = self.modelsDesc['turret']
        gun = self.modelsDesc['gun']
        chassis['model'].visible = chassis['_visibility'][0]
        chassis['model'].visibleAttachments = chassis['_visibility'][1]
        hull['model'].visible = hull['_visibility'][0]
        hull['model'].visibleAttachments = hull['_visibility'][1]
        turret['model'].visible = turret['_visibility'][0]
        turret['model'].visibleAttachments = turret['_visibility'][1]
        gun['model'].visible = gun['_visibility'][0]
        gun['model'].visibleAttachments = gun['_visibility'][1]

    
    def _VehicleAppearance__validateAssembledModel(self):
        self._VehicleAppearance__validateCallbackId = None
        vehicle = self._VehicleAppearance__vehicle
        vDesc = vehicle.typeDescriptor
        state = self._VehicleAppearance__curDamageState
        chassis = self.modelsDesc['chassis']
        hull = self.modelsDesc['hull']
        turret = self.modelsDesc['turret']
        gun = self.modelsDesc['gun']
        _validateCfgPos(chassis, hull, vDesc.chassis['hullPosition'], 'hullPosition', vehicle, state)
        _validateCfgPos(hull, turret, vDesc.hull['turretPositions'][0], 'turretPosition', vehicle, state)
        _validateCfgPos(turret, gun, vDesc.turret['gunPosition'], 'gunPosition', vehicle, state)

    
    def _VehicleAppearance__createExhaust(self):
        exhaust = self._VehicleAppearance__vehicle.typeDescriptor.hull['exhaust']
        pixieName = exhaust['pixie']
        rates = exhaust['rates']
        for i in xrange(len(exhaust['nodes'])):
            pixie = Pixie.create(pixieName)
            pixie.drawOrder = 50 + i
            self._VehicleAppearance__exhaust.append([
                None,
                pixie])
            for i in xrange(pixie.nSystems()):
                source = pixie.system(i).action(1)
                source.rate = rates[0]
            
        

    
    def _VehicleAppearance__attachExhaust(self, attach):
        nodes = self._VehicleAppearance__vehicle.typeDescriptor.hull['exhaust']['nodes']
        hullModel = self.modelsDesc['hull']['model']
        if attach:
            for i in xrange(len(nodes)):
                pair = self._VehicleAppearance__exhaust[i]
                pair[0] = hullModel.node(nodes[i])
                pair[0].attach(pair[1])
            
        else:
            for pair in self._VehicleAppearance__exhaust:
                if pair[0] is not None:
                    pair[0].detach(pair[1])
                    continue
            

    
    def _VehicleAppearance__changeExhaust(self, engineMode):
        rates = self._VehicleAppearance__vehicle.typeDescriptor.hull['exhaust']['rates']
        for pair in self._VehicleAppearance__exhaust:
            pixie = pair[1]
            for i in xrange(pixie.nSystems()):
                source = pixie.system(i).action(1)
                if not self._VehicleAppearance__exhaustDisabledByLOD:
                    pass
                1
                source.rate = 0
            
        

    
    def _VehicleAppearance__createGunRecoil(self):
        recoilDescr = self._VehicleAppearance__vehicle.typeDescriptor.gun['recoil']
        recoil = BigWorld.WGGunRecoil(_GUN_RECOIL_NODE_NAME)
        recoil.setLod(recoilDescr['lodDist'])
        recoil.setDuration(recoilDescr['backoffTime'], recoilDescr['returnTime'])
        recoil.setDepth(recoilDescr['amplitude'])
        self._VehicleAppearance__gunRecoil = recoil

    
    def _VehicleAppearance__createStickers(self, prereqs):
        vDesc = self._VehicleAppearance__vehicle.typeDescriptor
        g_cache = items.vehicles.g_cache
        if vDesc.turret['showEmblemsOnGun']:
            pass
        1
        if vDesc.turret['showEmblemsOnGun']:
            pass
        1
        emblemPositions = (('turret', vDesc.turret['emblemSlots']), 'turret', ('gun', []))
        clanID = BigWorld.player().arena.vehicles[self._VehicleAppearance__vehicle.id]['clanDBID']
        for (componentName, slots) in emblemPositions:
            stickers = VehicleStickers.VehicleStickers(vDesc, slots, componentName == 'hull', prereqs)
            stickers.setClanID(clanID)
            self._VehicleAppearance__stickers[componentName] = {
                'stickers': stickers,
                'damageStickers': { },
                'alpha': 1 }
        

    
    def _VehicleAppearance__attachStickers(self, alpha = 1, emblemsOnly = False):
        actualAlpha = alpha * self._VehicleAppearance__vehicle.typeDescriptor.type.emblemsAlpha
        if self._VehicleAppearance__showStickers:
            pass
        1
        actualAlpha = 0
        isDamaged = self._VehicleAppearance__curDamageState != 'undamaged'
        for (componentName, stickerDesc) in self._VehicleAppearance__stickers.iteritems():
            stickers = stickerDesc['stickers']
            stickers.setAlphas(actualAlpha, actualAlpha)
            stickerDesc['alpha'] = actualAlpha
            model = self.modelsDesc[componentName]['model']
            node = self.modelsDesc[componentName]['_node']
            stickers.attachStickers(model, node, isDamaged)
            if emblemsOnly:
                continue
            
            for dmgSticker in stickerDesc['damageStickers'].itervalues():
                if dmgSticker['handle'] is not None:
                    stickers.delDamageSticker(dmgSticker['handle'])
                    dmgSticker['handle'] = None
                    LOG_WARNING('Adding %s damage sticker to occupied slot' % componentName)
                
                dmgSticker['handle'] = stickers.addDamageSticker(dmgSticker['texName'], dmgSticker['bumpTexName'], dmgSticker['rayStart'], dmgSticker['rayEnd'], dmgSticker['sizes'], dmgSticker['rayUp'])
            
        

    
    def _VehicleAppearance__detachStickers(self):
        for (componentName, stickerDesc) in self._VehicleAppearance__stickers.iteritems():
            stickerDesc['stickers'].detachStickers()
            for dmgSticker in stickerDesc['damageStickers'].itervalues():
                dmgSticker['handle'] = None
            
        

    
    def _VehicleAppearance__disableStipple(self):
        self._VehicleAppearance__vehicle.model.stipple = False
        self._VehicleAppearance__stippleCallbackID = None

    
    def _VehicleAppearance__onIsLaggingStateChanged(self, isLaggingNow):
        if self._VehicleAppearance__fashion is None:
            return None
        if not isLaggingNow:
            self._VehicleAppearance__fashion.disableAccelSwinging = True
            BigWorld.callback(1, self._VehicleAppearance__reEnableAccelSwinging)
        

    
    def _VehicleAppearance__reEnableAccelSwinging(self):
        if self._VehicleAppearance__fashion is not None:
            self._VehicleAppearance__fashion.disableAccelSwinging = False
        



class StippleManager:
    
    def __init__(self):
        self._StippleManager__stippleDescs = { }
        self._StippleManager__stippleToAddDescs = { }

    
    def showFor(self, vehicle, model):
        if not model.stipple:
            model.stipple = True
            callbackID = BigWorld.callback(0, partial(self._StippleManager__addStippleModel, vehicle.id))
            self._StippleManager__stippleToAddDescs[vehicle.id] = (model, callbackID)
        

    
    def hideIfExistFor(self, vehicle):
        desc = self._StippleManager__stippleDescs.get(vehicle.id)
        if desc is not None:
            BigWorld.cancelCallback(desc[1])
            BigWorld.player().delModel(desc[0])
            del self._StippleManager__stippleDescs[vehicle.id]
        
        desc = self._StippleManager__stippleToAddDescs.get(vehicle.id)
        if desc is not None:
            BigWorld.cancelCallback(desc[1])
            del self._StippleManager__stippleToAddDescs[vehicle.id]
        

    
    def destroy(self):
        for (model, callbackID) in self._StippleManager__stippleDescs.itervalues():
            BigWorld.cancelCallback(callbackID)
            BigWorld.player().delModel(model)
        
        for (model, callbackID) in self._StippleManager__stippleToAddDescs.itervalues():
            BigWorld.cancelCallback(callbackID)
        
        self._StippleManager__stippleDescs = None
        self._StippleManager__stippleToAddDescs = None

    
    def _StippleManager__addStippleModel(self, vehID):
        model = self._StippleManager__stippleToAddDescs[vehID][0]
        if model.attached:
            callbackID = BigWorld.callback(0, partial(self._StippleManager__addStippleModel, vehID))
            self._StippleManager__stippleToAddDescs[vehID] = (model, callbackID)
            return None
        del self._StippleManager__stippleToAddDescs[vehID]
        BigWorld.player().addModel(model)
        callbackID = BigWorld.callback(_VEHICLE_DISAPPEAR_TIME, partial(self._StippleManager__removeStippleModel, vehID))
        self._StippleManager__stippleDescs[vehID] = (model, callbackID)

    
    def _StippleManager__removeStippleModel(self, vehID):
        BigWorld.player().delModel(self._StippleManager__stippleDescs[vehID][0])
        del self._StippleManager__stippleDescs[vehID]



class _CrashedTrackController:
    
    def __init__(self, vehicle, va):
        self._CrashedTrackController__vehicle = vehicle.proxy
        self._CrashedTrackController__va = weakref.ref(va)
        self._CrashedTrackController__flags = 0
        self._CrashedTrackController__model = None
        self._CrashedTrackController__fashion = None
        self._CrashedTrackController__inited = True
        self._CrashedTrackController__forceHide = False
        self._CrashedTrackController__loadInfo = [
            False,
