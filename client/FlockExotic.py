# Source Generated with Decompyle++
# File: FlockExotic.pyc (Python 2.6)

import BigWorld
import math
from Vehicle import Vehicle
import random
import Math
from debug_utils import LOG_CURRENT_EXCEPTION
from Flock import FlockLike

class FlockExotic(BigWorld.Entity, FlockLike):
    _FlockExotic__TRIGGER_CHECK_PERIOD = 1
    
    def __init__(self):
        BigWorld.Entity.__init__(self)
        FlockLike.__init__(self)
        self._FlockExotic__checkTriggerCallbackId = None
        self._FlockExotic__respawnCallbackId = None
        self._FlockExotic__motors = []
        self.flightAngleMin = math.radians(self.flightAngleMin)
        self.flightAngleMax = math.radians(self.flightAngleMax)
        if self.flightAngleMin < 0:
            self.flightAngleMin += math.ceil(abs(self.flightAngleMin) / math.pi * 2) * math.pi * 2
        elif self.flightAngleMin > math.pi * 2:
            self.flightAngleMin -= math.floor(self.flightAngleMin / math.pi * 2) * math.pi * 2
        

    
    def prerequisites(self):
        return self._getModelsToLoad()

    
    def _FlockExotic__createMotors(self):
        del self._FlockExotic__motors[:]
        for i in xrange(self.modelCount):
            motor = BigWorld.LinearHomer()
            self._FlockExotic__motors.append(motor)
            motorMatrix = Math.Matrix()
            motorMatrix.setIdentity()
            motor.target = motorMatrix
            motor.acceleration = 0
            motor.proximity = 0.5
        

    
    def onEnterWorld(self, prereqs):
        self._loadModels(prereqs)
        for model in self.models:
            model.visible = False
        
        self._FlockExotic__createMotors()
        self._FlockExotic__respawnCallbackId = BigWorld.callback(self.respawnTime, self._FlockExotic__respawnTrigger)
        self._switchSounds(False)

    
    def onLeaveWorld(self):
        self.models = []
        if self._FlockExotic__checkTriggerCallbackId is not None:
            BigWorld.cancelCallback(self._FlockExotic__checkTriggerCallbackId)
            self._FlockExotic__checkTriggerCallbackId = None
        
        if self._FlockExotic__respawnCallbackId is not None:
            BigWorld.cancelCallback(self._FlockExotic__respawnCallbackId)
            self._FlockExotic__respawnCallbackId = None
        
        FlockLike.destroy(self)

    
    def name(self):
        return 'FlockExotic'

    
    def _FlockExotic__checkTrigger(self):
        self._FlockExotic__checkTriggerCallbackId = None
        isTriggered = False
        for (id, entity) in BigWorld.entities.items():
            if isinstance(entity, Vehicle):
                distanceVec = self.position - entity.position
                distanceVec.y = 0
                if distanceVec.lengthSquared <= self.triggerRadius * self.triggerRadius:
                    self._FlockExotic__onTrigger()
                    isTriggered = True
                    break
                
            distanceVec.lengthSquared <= self.triggerRadius * self.triggerRadius
        
        if not isTriggered:
            self._FlockExotic__checkTriggerCallbackId = BigWorld.callback(FlockExotic._FlockExotic__TRIGGER_CHECK_PERIOD, self._FlockExotic__checkTrigger)
        

    
    def _FlockExotic__respawnTrigger(self):
        self._FlockExotic__respawnCallbackId = None
        self._FlockExotic__checkTriggerCallbackId = BigWorld.callback(FlockExotic._FlockExotic__TRIGGER_CHECK_PERIOD, self._FlockExotic__checkTrigger)

    
    def _FlockExotic__getRandomSpawnPos(self):
        randHeight = random.uniform(0, self.spawnHeight)
        randAngle = random.uniform(0, 2 * math.pi)
        randRadius = random.uniform(0, self.spawnRadius)
        return Math.Vector3(randRadius * math.cos(randAngle), randHeight, randRadius * math.sin(randAngle)) + self.position

    
    def _FlockExotic__getRandomTargetPos(self, startPos):
        randHeight = random.uniform(0, self.flightHeight)
        arc = 0
        arc = self.flightAngleMax - self.flightAngleMin
        if self.flightAngleMax < self.flightAngleMin:
            arc = 2 * math.pi - abs(arc)
        
        randAngle = random.uniform(self.flightAngleMin, self.flightAngleMin + arc)
        dir = Math.Vector3(self.flightRadius * math.cos(randAngle), self.flightOffsetFromOrigin + randHeight, self.flightRadius * math.sin(randAngle)) + self.position
        dir = dir - startPos
        dir.normalise()
        dir *= self.speed * self.lifeTime
        return startPos + dir

    
    def _FlockExotic__onTrigger(self):
        for (model, motor) in zip(self.models, self._FlockExotic__motors):
            model.visible = True
            model.position = self._FlockExotic__getRandomSpawnPos()
            model.addMotor(motor)
            targetPos = self._FlockExotic__getRandomTargetPos(model.position)
            motor.target.setTranslate(targetPos)
            dir = targetPos - model.position
            dirLength = dir.length
            if dirLength > 0:
                dir *= self.speed / dirLength
                motor.velocity = dir
                continue
            motor.velocity = Math.Vector3(0, self.speed, 0)
        
        if len(self._FlockExotic__motors) > 0:
            self._FlockExotic__motors[0].proximityCallback = self._FlockExotic__onFlightEnd
        
        self._switchSounds(True)

    
    def _FlockExotic__onFlightEnd(self):
        self._switchSounds(False)
        for model in self.models:
            model.motors = ()
            model.position = self.position
            model.visible = False
        
        self._FlockExotic__respawnCallbackId = BigWorld.callback(self.respawnTime, self._FlockExotic__respawnTrigger)



