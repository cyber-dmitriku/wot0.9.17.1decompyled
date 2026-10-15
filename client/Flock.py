# Source Generated with Decompyle++
# File: Flock.pyc (Python 2.6)

import BigWorld
import Math
import ResMgr
import math
import random
import BattleReplay
from debug_utils import LOG_CURRENT_EXCEPTION
ENVIRONMENT_EFFECTS_CONFIG_FILE = 'scripts/environment_effects.xml'

class DebugGizmo:
    
    def __init__(self):
        self.model = BigWorld.Model('helpers/models/position_gizmo.model')
        BigWorld.addModel(self.model)
        self.motor = BigWorld.Servo(Math.Matrix())
        self.model.addMotor(self.motor)

    
    def visible(self, show):
        self.model.visible = show

    
    def attachTo(self, model):
        self.motor.signal = model.matrix

    
    def attachToPosition(self, pos):
        self.model.motors = ()
        self.model.position = pos



class _FlockSound:
    
    def __init__(self, soundName, parent):
        self.soundModel = BigWorld.player().newFakeModel()
        self.soundModel.addMotor(BigWorld.Servo(parent.root))
        BigWorld.addModel(self.soundModel)
        self.sound = self.soundModel.playSound(soundName)
        self.parent = parent

    
    def attachTo(self, model):
        self.soundModel.motors[0].signal = model.matrix
        self.parent = model

    
    def destroy(self):
        BigWorld.delModel(self.soundModel)



class FlockLike:
    _FlockLike__SoundNames = None
    MAX_SOUNDS = 2
    SOUND_RECALC_TIME = 0.6
    MAX_DIST_SQ = 10000
    
    def __init__(self):
        self._FlockLike__recalcSoundsCallback = None
        if FlockLike._FlockLike__SoundNames is None:
            FlockLike._FlockLike__SoundNames = { }
            flockDataSect = ResMgr.openSection(ENVIRONMENT_EFFECTS_CONFIG_FILE + '/birds')
            for value in flockDataSect.values():
                modelName = value.readString('modelName', '')
                soundName = value.readString('sound', '')
                if modelName != '' and soundName != '':
                    FlockLike._FlockLike__SoundNames[modelName] = soundName
                    continue
            
        
        self._FlockLike__sounds = { }

    
    def _FlockLike__getAllSounds(self):
        for modelSounds in self._FlockLike__sounds.values():
            for flockSound in modelSounds:
                yield flockSound
            
        

    
    def destroy(self):
        if self._FlockLike__recalcSoundsCallback is not None:
            BigWorld.cancelCallback(self._FlockLike__recalcSoundsCallback)
        
        allSounds = self._FlockLike__getAllSounds()
        for flockSound in allSounds:
            flockSound.destroy()
        

    
    def _getModelsToLoad(self):
        list = []
        modelNames = [
            self.modelName]
        if self.modelName2 != '':
            modelNames.append(self.modelName2)
        
        for i in xrange(0, self.modelCount):
            list.append(random.choice(modelNames))
        
        return list

    
    def _loadModels(self, prereqs):
        boidModels = prereqs.values()
        
        try:
            for model in boidModels:
                model.outsideOnly = 1
                model.moveAttachments = True
                self.addModel(model)
                model.FlockAnimAction(random.uniform(self.animSpeedMin, self.animSpeedMax))
                self._FlockLike__addSound(model)
            
            self._FlockLike__recalcSounds()
        except Exception:
            LOG_CURRENT_EXCEPTION()


    
    def _FlockLike__addSound(self, model):
        if not model.sources:
            return None
        modelName = model.sources[0]
        if modelName not in self._FlockLike__sounds:
            self._FlockLike__sounds[modelName] = []
        
        soundsForModel = self._FlockLike__sounds[modelName]
        if len(soundsForModel) >= FlockLike.MAX_SOUNDS:
            return None
        correctModelName = modelName.replace('\\', '/')
        soundName = FlockLike._FlockLike__SoundNames.get(correctModelName, None)
        if soundName is None or soundName == '':
            return None
        flockSound = None
        
        try:
            flockSound = _FlockSound(soundName, model)
        except Exception:
            soundName == ''
            len(soundsForModel) >= FlockLike.MAX_SOUNDS
            LOG_CURRENT_EXCEPTION()
            return None

        if flockSound is not None:
            if flockSound.sound is not None:
                soundsForModel.append(flockSound)
            else:
                flockSound.destroy()
        

    
    def _FlockLike__recalcSounds(self):
        self._FlockLike__recalcSoundsCallback = None
        camera = BigWorld.camera()
        
        def closest(x1, x2):
            dist1 = (camera.position - x1.position).lengthSquared
            dist2 = (camera.position - x2.position).lengthSquared
            return cmp(dist1, dist2)

        modelsByDist = sorted(self.models, closest)
        soundsToTalkIdx = { }
        for flockModel in modelsByDist:
            if not flockModel.sources:
                continue
            
            modelName = flockModel.sources[0]
            soundsToTalkIdx[modelName] = soundsToTalkIdx.get(modelName, -1) + 1
            idx = soundsToTalkIdx[modelName]
            soundsForModel = self._FlockLike__sounds[modelName]
            if idx < len(soundsForModel):
                soundsForModel[idx].attachTo(flockModel)
                continue
            (None,)
        
        self._FlockLike__recalcSoundsCallback = BigWorld.callback(FlockLike.SOUND_RECALC_TIME, self._FlockLike__recalcSounds)

    
    def _switchSounds(self, enable):
        allSounds = self._FlockLike__getAllSounds()
        for flockSound in allSounds:
            if enable:
                flockSound.sound.play()
                continue
            flockSound.sound.stop()
        
        if enable:
            if self._FlockLike__recalcSoundsCallback is None:
                self._FlockLike__recalcSounds()
            
        elif self._FlockLike__recalcSoundsCallback is not None:
            BigWorld.cancelCallback(self._FlockLike__recalcSoundsCallback)
            self._FlockLike__recalcSoundsCallback = None
        



class Flock(BigWorld.Entity, FlockLike):
    HEIGHT_CHANGE_DECISION_COUNT = 3
    HEIGHT_CHANGE_SPEED_MULTIPLIER = 1.1
    HEIGHT_DISPERSION_CORRIDOR = 0.05
    CIRCLE_FLIGHT_ABOVE = 0.5
    CIRCLE_FLIGHT_PROBABILITY = 0.25
    _Flock__SoundNames = None
    
    def __init__(self):
        BigWorld.Entity.__init__(self)
        FlockLike.__init__(self)
        self._Flock__decisionCallbackId = None
        self._Flock__decisionCount = 0

    
    def prerequisites(self):
        return self._getModelsToLoad()

    
    def onEnterWorld(self, prereqs):
        if BattleReplay.g_replayCtrl.isPlaying:
            return None
        self._loadModels(prereqs)
        self._Flock__decisionStrategy = self._Flock__doUsualFly
        if self.flyAroundCenter:
            self._Flock__decisionStrategy = self._Flock__doAroundCenterFly
            self.deadZoneRadius = self.radius
        
        self.filter = BigWorld.BoidsFilter()
        self.filter.speed = self.speedAtBottom
        self.filter.yawSpeed = self.yawSpeed
        self.filter.deadZonePosition = self.position
        self.filter.deadZoneRadius = self.deadZoneRadius
        self.middlePosition = Math.Vector3()
        self.minHeight = self.position.y
        self.maxHeight = self.minHeight + self.height
        for boid in self.models:
            boid.visible = True
        
        self.middlePosition = Math.Vector3(self.position)
        self.physics = 0
        newPosition = Math.Vector3(self.position)
        newPosition.y = (self.minHeight + self.maxHeight) / 2
        self.physics.teleport(newPosition)
        self._Flock__makeDecision()

    
    def onLeaveWorld(self):
        self.models = []
        if self._Flock__decisionCallbackId is not None:
            BigWorld.cancelCallback(self._Flock__decisionCallbackId)
        
        FlockLike.destroy(self)

    
    def set_state(self, oldState):
        pass

    
    def boidsLanded(self):
        pass

    
    def name(self):
        return 'Flock'

    
    def _Flock__doUsualFly(self):
        randY = self.position.y
        flightZoneHeight = self.maxHeight - self.minHeight
        if self._Flock__decisionCount >= Flock.HEIGHT_CHANGE_DECISION_COUNT:
            randY = random.uniform(self.minHeight, self.maxHeight)
            heightFraction = (randY - self.minHeight) / flightZoneHeight
            self.filter.speed = self.speedAtBottom + (self.speedAtTop - self.speedAtBottom) * heightFraction
            self._Flock__decisionCount = 0
        else:
            heightFraction = (self.position.y - self.minHeight) / flightZoneHeight
            if heightFraction >= Flock.CIRCLE_FLIGHT_ABOVE and random.random() <= Flock.CIRCLE_FLIGHT_PROBABILITY:
                return None
            self.filter.speed = self.speedAtBottom + (self.speedAtTop - self.speedAtBottom) * heightFraction
            randY = self.position.y + random.uniform(-flightZoneHeight * Flock.HEIGHT_DISPERSION_CORRIDOR, flightZoneHeight * Flock.HEIGHT_DISPERSION_CORRIDOR)
            if randY < self.minHeight:
                randY = self.minHeight
            elif randY > self.maxHeight:
                randY = self.maxHeight
            
        randRadius = random.uniform(self.deadZoneRadius, self.radius)
        randAngle = random.uniform(0, 2 * math.pi)
        newPosition = Math.Vector3(self.middlePosition.x + randRadius * math.cos(randAngle), randY, self.middlePosition.z + randRadius * math.sin(randAngle))
        self.physics.teleport(newPosition)

    
    def _Flock__doAroundCenterFly(self):
        randY = random.uniform(self.minHeight, self.maxHeight)
        self.physics.teleport(Math.Vector3(self.middlePosition.x, randY, self.middlePosition.z))

    
    def _Flock__makeDecision(self):
        self._Flock__decisionCallbackId = BigWorld.callback(self.decisionTime, self._Flock__makeDecision)
        self._Flock__decisionCount += 1
        self._Flock__decisionStrategy()



