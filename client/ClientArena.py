# Source Generated with Decompyle++
# File: ClientArena.pyc (Python 2.6)

import Math
import BigWorld
import ResMgr
import ArenaType
from items import vehicles
import constants
import cPickle
import Event
from constants import ARENA_PERIOD, ARENA_UPDATE
from PlayerEvents import g_playerEvents
from debug_utils import *

class ClientArena(object):
    _ClientArena__onUpdate = {
        ARENA_UPDATE.VEHICLE_LIST: '_ClientArena__onVehicleListUpdate',
        ARENA_UPDATE.VEHICLE_ADDED: '_ClientArena__onVehicleAddedUpdate',
        ARENA_UPDATE.PERIOD: '_ClientArena__onPeriodInfoUpdate',
        ARENA_UPDATE.STATISTICS: '_ClientArena__onStatisticsUpdate',
        ARENA_UPDATE.VEHICLE_STATISTICS: '_ClientArena__onVehicleStatisticsUpdate',
        ARENA_UPDATE.VEHICLE_KILLED: '_ClientArena__onVehicleKilled',
        ARENA_UPDATE.AVATAR_READY: '_ClientArena__onAvatarReady',
        ARENA_UPDATE.BASE_POINTS: '_ClientArena__onBasePointsUpdate',
        ARENA_UPDATE.BASE_CAPTURED: '_ClientArena__onBaseCaptured',
        ARENA_UPDATE.TEAM_KILLER: '_ClientArena__onTeamKiller',
        ARENA_UPDATE.VEHICLE_UPDATED: '_ClientArena__onVehicleUpdatedUpdate' }
    
    def __init__(self, arenaUniqueID, arenaTypeID, arenaGuiType, arenaExtraData, weatherPresetID):
        self._ClientArena__vehicles = { }
        self._ClientArena__vehicleIndexToId = { }
        self._ClientArena__positions = { }
        self._ClientArena__statistics = { }
        self._ClientArena__periodInfo = (ARENA_PERIOD.WAITING, 0, 0, None)
        self._ClientArena__eventManager = Event.EventManager()
        em = self._ClientArena__eventManager
        self.onNewVehicleListReceived = Event.Event(em)
        self.onVehicleAdded = Event.Event(em)
        self.onVehicleUpdated = Event.Event(em)
        self.onPositionsUpdated = Event.Event(em)
        self.onPeriodChange = Event.Event(em)
        self.onNewStatisticsReceived = Event.Event(em)
        self.onVehicleStatisticsUpdate = Event.Event(em)
        self.onVehicleKilled = Event.Event(em)
        self.onAvatarReady = Event.Event(em)
        self.onTeamBasePointsUpdate = Event.Event(em)
        self.onTeamBaseCaptured = Event.Event(em)
        self.onTeamKiller = Event.Event(em)
        self.arenaUniqueID = arenaUniqueID
        self.arenaType = ArenaType.g_cache[arenaTypeID]
        self.guiType = arenaGuiType
        self.extraData = arenaExtraData
        self._ClientArena__arenaBBCollider = None
        self._ClientArena__spaceBBCollider = None

    vehicles = property((lambda self: self._ClientArena__vehicles))
    positions = property((lambda self: self._ClientArena__positions))
    statistics = property((lambda self: self._ClientArena__statistics))
    period = property((lambda self: self._ClientArena__periodInfo[0]))
    periodEndTime = property((lambda self: self._ClientArena__periodInfo[1]))
    periodLength = property((lambda self: self._ClientArena__periodInfo[2]))
    periodAdditionalInfo = property((lambda self: self._ClientArena__periodInfo[3]))
    
    def destroy(self):
        self._ClientArena__eventManager.clear()

    
    def update(self, updateType, argStr):
        delegateName = self._ClientArena__onUpdate.get(updateType, None)
        if delegateName is not None:
            getattr(self, delegateName)(argStr)
        

    
    def updatePositions(self, indices, positions):
        self._ClientArena__positions.clear()
        if indices:
            lenPos = len(positions)
            lenInd = len(indices)
            if not lenPos == 2 * lenInd:
                raise AssertionError
            indexToId = self._ClientArena__vehicleIndexToId
            for i in xrange(0, lenInd):
                if indices[i] in indexToId:
                    positionTuple = (positions[2 * i], 0, positions[2 * i + 1])
                    self._ClientArena__positions[indexToId[indices[i]]] = positionTuple
                    continue
                lenPos == 2 * lenInd
            
        
        self.onPositionsUpdated()

    
    def collideWithArenaBB(self, start, end):
        if self._ClientArena__arenaBBCollider is None:
            if not self._ClientArena__setupBBColliders():
                return None
        
        return self._ClientArena__arenaBBCollider.collide(start, end)

    
    def collideWithSpaceBB(self, start, end):
        if self._ClientArena__spaceBBCollider is None:
            if not self._ClientArena__setupBBColliders():
                return None
        
        return self._ClientArena__spaceBBCollider.collide(start, end)

    
    def _ClientArena__setupBBColliders(self):
        if BigWorld.wg_getSpaceBounds().length == 0:
            return False
        arenaBB = self.arenaType.boundingBox
        spaceBB = _convertToList(BigWorld.wg_getSpaceBounds())
        self._ClientArena__arenaBBCollider = _BBCollider(arenaBB, (-500, 500))
        self._ClientArena__spaceBBCollider = _BBCollider(spaceBB, (-500, 500))
        return True

    
    def _ClientArena__onVehicleListUpdate(self, argStr):
        list = cPickle.loads(argStr)
        vehicles = self._ClientArena__vehicles
        vehicles.clear()
        for infoAsTuple in list:
            (id, info) = self._ClientArena__vehicleInfoAsDict(infoAsTuple)
            vehicles[id] = info
        
        self._ClientArena__rebuildIndexToId()
        self.onNewVehicleListReceived()

    
    def _ClientArena__onVehicleAddedUpdate(self, argStr):
        infoAsTuple = cPickle.loads(argStr)
        (id, info) = self._ClientArena__vehicleInfoAsDict(infoAsTuple)
        self._ClientArena__vehicles[id] = info
        self._ClientArena__rebuildIndexToId()
        self.onVehicleAdded(id)

    
    def _ClientArena__onVehicleUpdatedUpdate(self, argStr):
        infoAsTuple = cPickle.loads(argStr)
        (id, info) = self._ClientArena__vehicleInfoAsDict(infoAsTuple)
        self._ClientArena__vehicles[id] = info
        self.onVehicleUpdated(id)

    
    def _ClientArena__onPeriodInfoUpdate(self, argStr):
        self._ClientArena__periodInfo = cPickle.loads(argStr)
        self.onPeriodChange(*self._ClientArena__periodInfo)
        g_playerEvents.onArenaPeriodChange(*self._ClientArena__periodInfo)

    
    def _ClientArena__onStatisticsUpdate(self, argStr):
        self._ClientArena__statistics = { }
        statList = cPickle.loads(argStr)
        for s in statList:
            (vehicleID, stats) = self._ClientArena__vehicleStatisticsAsDict(s)
            self._ClientArena__statistics[vehicleID] = stats
        
        self.onNewStatisticsReceived()

    
    def _ClientArena__onVehicleStatisticsUpdate(self, argStr):
        (vehicleID, stats) = self._ClientArena__vehicleStatisticsAsDict(cPickle.loads(argStr))
        self._ClientArena__statistics[vehicleID] = stats
        self.onVehicleStatisticsUpdate(vehicleID)

    
    def _ClientArena__onVehicleKilled(self, argStr):
        (victimID, killerID, reason) = cPickle.loads(argStr)
        vehInfo = self._ClientArena__vehicles.get(victimID, None)
        if vehInfo is not None:
            vehInfo['isAlive'] = False
            self.onVehicleKilled(victimID, killerID, reason)
        

    
    def _ClientArena__onAvatarReady(self, argStr):
        vehicleID = cPickle.loads(argStr)
        vehInfo = self._ClientArena__vehicles.get(vehicleID, None)
        if vehInfo is not None:
            vehInfo['isAvatarReady'] = True
            self.onAvatarReady(vehicleID)
        

    
    def _ClientArena__onBasePointsUpdate(self, argStr):
        (team, baseID, points, capturingStopped) = cPickle.loads(argStr)
        self.onTeamBasePointsUpdate(team, baseID, points, capturingStopped)

    
    def _ClientArena__onBaseCaptured(self, argStr):
        (team, baseID) = cPickle.loads(argStr)
        self.onTeamBaseCaptured(team, baseID)

    
    def _ClientArena__onTeamKiller(self, argStr):
        vehicleID = cPickle.loads(argStr)
        vehInfo = self._ClientArena__vehicles.get(vehicleID, None)
        if vehInfo is not None:
            vehInfo['isTeamKiller'] = True
            self.onTeamKiller(vehicleID)
        

    
    def _ClientArena__rebuildIndexToId(self):
        vehicles = self._ClientArena__vehicles
        self._ClientArena__vehicleIndexToId = dict(zip(range(len(vehicles)), sorted(vehicles.keys())))

    
    def _ClientArena__vehicleInfoAsDict(self, info):
        
        getVehicleType = lambda cd: if cd is None:
Nonevehicles.VehicleDescr(compactDescr = cd)
        infoAsDict = {
            'vehicleType': getVehicleType(info[1]),
            'name': info[2],
            'team': info[3],
            'isAlive': info[4],
            'isAvatarReady': info[5],
            'isTeamKiller': info[6],
            'accountDBID': info[7],
            'clanAbbrev': info[8],
            'clanDBID': info[9],
            'prebattleID': info[10],
            'isPrebattleCreator': bool(info[11]),
            'events': info[12] }
        return (info[0], infoAsDict)

    
    def _ClientArena__vehicleStatisticsAsDict(self, stats):
        return (stats[0], {
            'frags': stats[1] })



def _convertToList(vec4):
    return ((vec4.x, vec4.y), (vec4.z, vec4.w))


def _pointInBB(bottomLeft2D, upperRight2D, point3D, minMaxHeight):
    if bottomLeft2D[0] < point3D[0]:
        pass
    point3D[0] < upperRight2D[0]
    if 1:
        if bottomLeft2D[1] < point3D[2]:
            pass
        point3D[2] < upperRight2D[1]
        if 1:
            if minMaxHeight[0] < point3D[1]:
                pass
            point3D[1] < minMaxHeight[1]
            if 1:
                return True
            return False
        return 1


class _BBCollider:
    
    def __init__(self, bb, heightLimits):
        self._BBCollider__planes = list()
        self._BBCollider__bb = bb
        self._BBCollider__heightLimits = heightLimits
        self._BBCollider__planes.append(Plane(Math.Vector3(0, 0, 1), bb[0][1]))
        self._BBCollider__planes.append(Plane(Math.Vector3(0, 0, -1), -bb[1][1]))
        self._BBCollider__planes.append(Plane(Math.Vector3(1, 0, 0), bb[0][0]))
        self._BBCollider__planes.append(Plane(Math.Vector3(-1, 0, 0), -bb[1][0]))
        self._BBCollider__planes.append(Plane(Math.Vector3(0, 1, 0), heightLimits[0]))
        self._BBCollider__planes.append(Plane(Math.Vector3(0, -1, 0), heightLimits[1]))

    
    def collide(self, start, end):
        if not _pointInBB(self._BBCollider__bb[0], self._BBCollider__bb[1], end, self._BBCollider__heightLimits):
            finalPoint = None
            dist = 0
            for plane in self._BBCollider__planes:
                intersecPoint = plane.intersectSegment(start, end)
                if intersecPoint:
                    tmpDist = (intersecPoint - start).length
                    if tmpDist < dist or dist == 0:
                        dist = tmpDist
                        finalPoint = intersecPoint
                    
                dist == 0
            
            if finalPoint is not None:
                return finalPoint
            return start
        _pointInBB(self._BBCollider__bb[0], self._BBCollider__bb[1], end, self._BBCollider__heightLimits)



class Plane:
    
    def __init__(self, n, d):
        self.n = n
        self.d = d

    
    def intersectSegment(self, a, b):
        ab = b - a
        normalDotDir = self.n.dot(ab)
        if normalDotDir == 0:
            return None
        t = (self.d - self.n.dot(a)) / normalDotDir
        if t >= 0 and t <= 1:
            return a + ab.scale(t)

    
    def testPoint(self, point):
        if self.n.dot(point) - self.d >= 0:
            return True
        return False



