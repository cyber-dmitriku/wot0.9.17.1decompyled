# Source Generated with Decompyle++
# File: MapActivities.pyc (Python 2.6)

import BigWorld
import Math
import ResMgr
import Pixie
import PlayerEvents
import random
import copy
from constants import ARENA_PERIOD
from debug_utils import *

class IMapActivity:
    
    def create(self, settings):
        pass

    
    def destroy(self):
        self.stop()

    
    def start(self):
        pass

    
    def stop(self):
        pass

    
    def canStart(self):
        return False

    
    def isActive(self):
        return False



class MapActivities(object):
    
    def __init__(self):
        self._MapActivities__cbID = BigWorld.callback(0.1, self._MapActivities__onPeriodicTimer)
        self._MapActivities__isOnArena = False
        self._MapActivities__pendingActivities = []
        self._MapActivities__currActivities = []
        PlayerEvents.g_playerEvents.onArenaPeriodChange += self._MapActivities__onArenaPeriodChange

    
    def destroy(self):
        BigWorld.cancelCallback(self._MapActivities__cbID)
        self._MapActivities__cbID = None
        PlayerEvents.g_playerEvents.onArenaPeriodChange -= self._MapActivities__onArenaPeriodChange

    
    def _MapActivities__generateActivities(self):
        self._MapActivities__pendingActivities = []
        arenaType = BigWorld.player().arena.arenaType
        vehicles = BigWorld.player().arena.vehicles
        if arenaType.mapActivities is None:
            return None
        randHash = 0
        for v in vehicles.values():
            vehicle = copy.copy(v)
            vehicle['vehicleType'] = v['vehicleType'].name
            randHash = randHash ^ hash(str(vehicle))
        
        random.seed(randHash)
        for (activityType, activityXML) in arenaType.mapActivities.items():
            activity = _createActivity(activityType)
            if activity is not None:
                activity.create(activityXML)
                self._MapActivities__pendingActivities.append(activity)
                continue
            arenaType.mapActivities is None
        

    
    def _MapActivities__stopActivities(self):
        for activity in self._MapActivities__currActivities:
            activity.stop()
        
        self._MapActivities__currActivities = []
        self._MapActivities__pendingActivities = []

    
    def _MapActivities__onPeriodicTimer(self):
        for activity in self._MapActivities__pendingActivities:
            if activity.canStart():
                activity.start()
                self._MapActivities__currActivities.append(activity)
                self._MapActivities__pendingActivities.remove(activity)
                continue
        
        self._MapActivities__cbID = BigWorld.callback(0.1, self._MapActivities__onPeriodicTimer)

    
    def _MapActivities__onArenaPeriodChange(self, period, periodEndTime, periodLength, periodAdditionalInfo):
        isOnArena = period == ARENA_PERIOD.BATTLE
        if isOnArena and not (self._MapActivities__isOnArena):
            self._MapActivities__generateActivities()
        elif not isOnArena and self._MapActivities__isOnArena:
            self._MapActivities__stopActivities()
        
        self._MapActivities__isOnArena = isOnArena



class WarplaneActivity(IMapActivity):
    
    def create(self, settings):
        self._WarplaneActivity__settings = settings
        self._WarplaneActivity__curve = None
        self._WarplaneActivity__model = None
        self._WarplaneActivity__motor = None
        self._WarplaneActivity__sound = None
        self._WarplaneActivity__particles = None
        self._WarplaneActivity__particlesAdded = False
        self._WarplaneActivity__particlesNode = None
        self._WarplaneActivity__cbID = None
        startTimeRange = settings.readVector2('startTime')
        self._WarplaneActivity__startTime = BigWorld.time() + random.uniform(startTimeRange[0], startTimeRange[1])
        if settings.readFloat('possibility', 1) < random.uniform(0, 1):
            self._WarplaneActivity__startTime += 1e+06
        
        self._WarplaneActivity__curve = BigWorld.WGActionCurve(self._WarplaneActivity__settings)
        self._WarplaneActivity__modelName = self._WarplaneActivity__curve.getChannelProperty(0, 'modelName').asString
        BigWorld.loadResourceListBG((self._WarplaneActivity__modelName,), self._WarplaneActivity__onModelLoaded)

    
    def isActive(self):
        return self._WarplaneActivity__model is not None

    
    def canStart(self):
        if BigWorld.time() >= self._WarplaneActivity__startTime:
            pass
        return self._WarplaneActivity__model is not None

    
    def start(self):
        self._WarplaneActivity__model = BigWorld.Model(self._WarplaneActivity__curve.getChannelProperty(0, 'modelName').asString)
        BigWorld.addModel(self._WarplaneActivity__model)
        self._WarplaneActivity__model.wg_fashion = BigWorld.WGBaseFashion()
        self._WarplaneActivity__model.wg_fashion.initAlphaMaterials()
        self._WarplaneActivity__motor = BigWorld.WGWarplaneMotor(self._WarplaneActivity__curve, 0)
        self._WarplaneActivity__model.addMotor(self._WarplaneActivity__motor)
        ds = self._WarplaneActivity__curve.getChannelProperty(0, 'soundName')
        if ds is not None:
            pass
        1
        soundName = ''
        if soundName != '':
            self._WarplaneActivity__sound = self._WarplaneActivity__model.playSound(soundName)
            self._WarplaneActivity__sound.volume = 0
        
        self._WarplaneActivity__updateAlpha()

    
    def stop(self):
        if self._WarplaneActivity__cbID is not None:
            BigWorld.cancelCallback(self._WarplaneActivity__cbID)
            self._WarplaneActivity__cbID = None
        
        if self._WarplaneActivity__model is not None:
            delattr(self._WarplaneActivity__model, 'wg_fashion')
            self._WarplaneActivity__model.delMotor(self._WarplaneActivity__motor)
            BigWorld.delModel(self._WarplaneActivity__model)
            self._WarplaneActivity__model = None
            self._WarplaneActivity__motor = None
            self._WarplaneActivity__curve = None
        
        if self._WarplaneActivity__sound is not None:
            self._WarplaneActivity__sound.stop()
            self._WarplaneActivity__sound = None
        
        if self._WarplaneActivity__particles is not None:
            self._WarplaneActivity__particlesNode.detach(self._WarplaneActivity__particles)
            self._WarplaneActivity__particlesNode = None
            self._WarplaneActivity__particles = None
        

    
    def _WarplaneActivity__updateAlpha(self):
        alpha = self._WarplaneActivity__motor.warplaneAlpha
        self._WarplaneActivity__cbID = None
        self._WarplaneActivity__model.wg_fashion.setAlpha(alpha)
        if self._WarplaneActivity__sound is not None:
            self._WarplaneActivity__sound.volume = alpha
        
        if alpha == 1 and self._WarplaneActivity__particles is None and not (self._WarplaneActivity__particlesAdded):
            self._WarplaneActivity__particlesAdded = True
            ds = self._WarplaneActivity__curve.getChannelProperty(0, 'effectName')
            if ds is not None:
                pass
            1
            effectName = ''
            if effectName != '':
                Pixie.createBG(effectName, self._WarplaneActivity__onParticlesLoaded)
            
        elif alpha == 0 and self._WarplaneActivity__particles is not None and self._WarplaneActivity__particlesAdded:
            self.stop()
            return None
        self._WarplaneActivity__cbID = BigWorld.callback(0, self._WarplaneActivity__updateAlpha)

    
    def _WarplaneActivity__onModelLoaded(self, resourceRefs):
        if self._WarplaneActivity__modelName not in resourceRefs.failedIDs:
            self._WarplaneActivity__model = resourceRefs[self._WarplaneActivity__modelName]
        else:
            LOG_ERROR('Could not load model %s' % self._WarplaneActivity__modelName)

    
    def _WarplaneActivity__onParticlesLoaded(self, particles):
        if self._WarplaneActivity__curve is None:
            return None
        hardPointName = self._WarplaneActivity__curve.getChannelProperty(0, 'effectHardpoint').asString
        if hardPointName != '':
            self._WarplaneActivity__particles = particles
            self._WarplaneActivity__particlesNode = self._WarplaneActivity__model.node(hardPointName)
            self._WarplaneActivity__particlesNode.attach(self._WarplaneActivity__particles)
        



def _createActivity(typeName):
    if typeName == 'warplane':
        return WarplaneActivity()

g_mapActivities = MapActivities()

