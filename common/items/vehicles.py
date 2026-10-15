# Source Generated with Decompyle++
# File: vehicles.pyc (Python 2.6)

from collections import namedtuple
from math import radians, cos, pi
from functools import partial
from types import IntType
import struct
import ResMgr
from Math import Vector2, Vector3
import nations
import items
from items import _xml
from debug_utils import *
from constants import IS_DEVELOPMENT, IS_CLIENT, IS_CELLAPP, IS_BASEAPP, IS_WEB, ITEM_DEFS_PATH
from constants import DEFAULT_GUN_PITCH_LIMITS_TRANSITION
if IS_CELLAPP or IS_CLIENT:
    from ModelHitTester import ModelHitTester, VehicleHitTester

if IS_CELLAPP and IS_CLIENT or IS_WEB:
    import material_kinds
    from material_kinds import EFFECT_MATERIALS

if IS_CLIENT:
    from helpers import i18n
    from helpers import EffectsList
elif IS_WEB:
    from web_stubs import *

VEHICLE_CLASS_TAGS = frozenset(('lightTank', 'mediumTank', 'heavyTank', 'SPG', 'AT-SPG'))
VEHICLE_MODULE_TAGS = frozenset(('vehicle', 'gun', 'turret', 'engine', 'chassis', 'radio'))
NUM_OPTIONAL_DEVICE_SLOTS = 3
NUM_EQUIPMENT_SLOTS = 3
CAMOUFLAGE_KINDS = {
    'winter': 0,
    'summer': 1,
    'desert': 2 }

class HORN_COOLDOWN:
    WINDOW = 25
    CLIENT_WINDOW_EXPANSION = 5
    MAX_SIGNALS = 3

NUM_INSCRIPTION_COLORS = 16
KMH_TO_MS = 0.27778
HP_TO_WATTS = 735.5
g_list = None
g_cache = None
_VEHICLE_TYPE_XML_PATH = ITEM_DEFS_PATH + 'vehicles/'
_DEFAULT_SPECIFIC_FRICTION = 0.07 * 9.81
_DEFAULT_HEALTH_BURN_PER_SEC_LOSS_FRACTION = 0.0875
_CUSTOMIZATION_EPOCH = 1306886400
MaterialInfo = namedtuple('MaterialInfo', [
    'kind',
    'armor',
    'extra',
    'vehicleDamageFactor',
    'useArmorHomogenization',
    'useHitAngle',
    'useAntifragmentationLining',
    'mayRicochet',
    'collideOnceOnly',
    'damageKind',
    'chanceToHitByProjectile',
    'chanceToHitByExplosion',
    'continueTraceIfNoHit'])
_defMaterialInfo = MaterialInfo(0, 0, None, 0, False, False, False, False, False, 0, 0, 0, False)

def init(preloadEverything):
    global g_list, g_cache
    if IS_CLIENT or IS_CELLAPP:
        import vehicle_extras as vehicle_extras
    
    g_list = VehicleList()
    g_cache = Cache()
    preloadEverything = True
    if preloadEverything:
        g_cache.optionalDevices()
        g_cache.equipments()
        g_cache.horns()
        g_cache.playerEmblems()
        for nationID in xrange(len(nations.NAMES)):
            g_cache.customization(nationID)
            for vehicleTypeID in g_list.getList(nationID).iterkeys():
                g_cache.vehicle(nationID, vehicleTypeID)
            
        
    


def reload():
    import vehicle_extras
    vehicle_extras.reload()
    modules = modules
    import sys
    import __builtin__ as __builtin__
    __builtin__.reload(modules[reload.__module__])
    init(False)


class VehicleDescr(object):
    
    def __init__(self, compactDescr = None, typeID = None, typeName = None):
        if compactDescr is None:
            if typeID is not None:
                (nationID, vehicleTypeID) = typeID
            elif not typeName is not None:
                raise AssertionError
            (nationID, vehicleTypeID) = g_list.getIDsByName(typeName)
            type = g_cache.vehicle(nationID, vehicleTypeID)
            turretDescr = type.turrets[0][0]
            header = items.ITEM_TYPE_INDICES['vehicle'] + (nationID << 4)
            compactDescr = struct.pack('<2B6HB', header, vehicleTypeID, type.chassis[0]['id'][1], type.engines[0]['id'][1], type.fuelTanks[0]['id'][1], type.radios[0]['id'][1], turretDescr['id'][1], turretDescr['guns'][0]['id'][1], 0)
        
        self._VehicleDescr__initFromCompactDescr(compactDescr)

    
    def _VehicleDescr__set_activeTurretPos(self, turretPosition):
        (self.turret, self.gun) = self.turrets[turretPosition]
        self._VehicleDescr__activeTurretPos = turretPosition
        self.activeGunShotIndex = 0

    activeTurretPosition = property((lambda self: self._VehicleDescr__activeTurretPos), _VehicleDescr__set_activeTurretPos)
    
    def _VehicleDescr__set_activeGunShotIndex(self, shotIndex):
        self.shot = self.gun['shots'][shotIndex]
        self._VehicleDescr__activeGunShotIdx = shotIndex

    activeGunShotIndex = property((lambda self: self._VehicleDescr__activeGunShotIdx), _VehicleDescr__set_activeGunShotIndex)
    
    def _VehicleDescr__get_camouflage(self):
        for v in self.camouflages:
            if v[0] is not None:
                return v
        

    
    def _VehicleDescr__set_camouflage(self, c):
        p = _EMPTY_CAMOUFLAGES
        if c is None:
            self.camouflages = p
            return None
        (id, startTime, durationDays) = c
        startTime = int(startTime / 60) * 60
        durationDays = int(durationDays)
        descr = g_cache.customization(self.type.id[0])['camouflages'][id]
        cd = self.type.compactDescr
        if cd in descr['deny']:
            raise Exception, 'camouflage is incompatible with vehicle'
        cd in descr['deny']
        if descr['allow'] and cd not in descr['allow']:
            raise Exception, 'camouflage is incompatible with vehicle'
        cd not in descr['allow']
        if startTime < _CUSTOMIZATION_EPOCH:
            raise Exception, 'wrong camouflage start time'
        startTime < _CUSTOMIZATION_EPOCH
        if 0 <= durationDays:
            pass
        durationDays <= 255
        if not 1:
            raise Exception, 'wrong camouflage duration'
        1
        position = descr['kind']
        self.camouflages = p[:position] + ((id, startTime, durationDays),) + p[position + 1:]

    camouflage = property(_VehicleDescr__get_camouflage, _VehicleDescr__set_camouflage)
    
    def _VehicleDescr__set_hornID(self, id):
        if id is not None:
            descr = g_cache.horns()[id]
            if not self.type.tags.intersection(descr['vehicleTags']):
                raise Exception, 'horn is incompatible with vehicle'
            self.type.tags.intersection(descr['vehicleTags'])
        
        self._VehicleDescr__hornID = id

    hornID = property((lambda self: self._VehicleDescr__hornID), _VehicleDescr__set_hornID)
    
    def setCamouflage(self, position, camouflageID, startTime, durationDays):
        p = self.camouflages
        if camouflageID is None:
            startTime = _CUSTOMIZATION_EPOCH
            durationDays = 0
            p[position]
        else:
            descr = g_cache.customization(self.type.id[0])['camouflages'][camouflageID]
            if position is None:
                position = descr['kind']
            elif position != descr['kind']:
                raise Exception, 'wrong camouflage kind'
            
            cd = self.type.compactDescr
            if cd in descr['deny']:
                raise Exception, 'camouflage is incompatible with vehicle'
            cd in descr['deny']
            if descr['allow'] and cd not in descr['allow']:
                raise Exception, 'camouflage is incompatible with vehicle'
            cd not in descr['allow']
            startTime = int(startTime / 60) * 60
            if startTime < _CUSTOMIZATION_EPOCH:
                raise Exception, 'wrong camouflage start time'
            startTime < _CUSTOMIZATION_EPOCH
            durationDays = int(durationDays)
            if 0 <= durationDays:
                pass
            durationDays <= 255
            if not 1:
                raise Exception, 'wrong camouflage duration'
            1
        self.camouflages = p[:position] + ((camouflageID, startTime, durationDays),) + p[position + 1:]

    
    def setPlayerEmblem(self, position, emblemID, startTime, durationDays):
        p = self.playerEmblems
        p[position]
        defEmblemID = self.type.defaultPlayerEmblemID
        if emblemID is None or emblemID == defEmblemID:
            emblemID = defEmblemID
            startTime = _CUSTOMIZATION_EPOCH
            durationDays = 0
        else:
            g_cache.playerEmblems()[1][emblemID]
            startTime = int(startTime / 60) * 60
            if startTime < _CUSTOMIZATION_EPOCH:
                raise Exception, 'wrong emblem start time'
            startTime < _CUSTOMIZATION_EPOCH
            durationDays = int(durationDays)
            if 0 <= durationDays:
                pass
            durationDays <= 255
            if not 1:
                raise Exception, 'wrong emblem duration'
            1
        self.playerEmblems = p[:position] + ((emblemID, startTime, durationDays),) + p[position + 1:]

    
    def setPlayerInscription(self, position, inscriptionID, startTime, durationDays, color):
        p = self.playerInscriptions
        p[position]
        if inscriptionID is None:
            startTime = _CUSTOMIZATION_EPOCH
            durationDays = 0
            color = 0
        elif inscriptionID is not None:
            customization = g_cache.customization(self.type.id[0])
            customization['inscriptions'][inscriptionID]
            customization['inscriptionColors'][color]
        
        startTime = int(startTime / 60) * 60
        if startTime < _CUSTOMIZATION_EPOCH:
            raise Exception, 'wrong inscription start time'
        startTime < _CUSTOMIZATION_EPOCH
        durationDays = int(durationDays)
        if 0 <= durationDays:
            pass
        durationDays <= 255
        if not 1:
            raise Exception, 'wrong inscription duration'
        1
        self.playerInscriptions = p[:position] + ((inscriptionID, startTime, durationDays, color),) + p[position + 1:]

    
    def getComponentsByType(self, itemTypeName, positionIndex = 0):
        if itemTypeName == 'vehicleChassis':
            return (self.chassis, self.type.chassis)
        if itemTypeName == 'vehicleEngine':
            return (self.engine, self.type.engines)
        if itemTypeName == 'vehicleRadio':
            return (self.radio, self.type.radios)
        if itemTypeName == 'vehicleFuelTank':
            return (self.fuelTank, self.type.fuelTanks)
        if itemTypeName == 'vehicleTurret':
            return (self.turrets[positionIndex][0], self.type.turrets[positionIndex])
        if itemTypeName == 'vehicleGun':
            (turretDescr, gunDescr) = self.turrets[positionIndex]
            return (gunDescr, turretDescr['guns'])
        if not False:
            raise AssertionError

    
    def mayInstallTurret(self, turretCompactDescr, gunCompactDescr, positionIndex = 0):
        (itemTypeID, nationID, turretID) = parseIntCompactDescr(turretCompactDescr)
        if items.ITEM_TYPE_NAMES[itemTypeID] != 'vehicleTurret':
            return (False, 'wrong item type')
        if nationID != self.type.id[0]:
            return (False, 'wrong nation')
        if gunCompactDescr == 0:
            gunID = self.turrets[positionIndex][1]['id'][1]
        else:
            (itemTypeID, nationID, gunID) = parseIntCompactDescr(gunCompactDescr)
            if items.ITEM_TYPE_NAMES[itemTypeID] != 'vehicleGun':
                return (False, 'wrong item type')
            if nationID != self.type.id[0]:
                return (False, 'wrong nation')
        newTurretDescr = _findDescrByID(self.type.turrets[positionIndex], turretID)
        if newTurretDescr is None:
            return (False, 'not for this vehicle type')
        newGunDescr = _findDescrByID(newTurretDescr['guns'], gunID)
        if newGunDescr is None:
            if gunCompactDescr not in self.type.installableComponents:
                return (False, 'not for this vehicle type')
            return (False, 'not for current vehicle')
        setter = partial(self.turrets.__setitem__, positionIndex, (newTurretDescr, newGunDescr))
        restorer = partial(self.turrets.__setitem__, positionIndex, self.turrets[positionIndex])
        
        try:
            setter()
            if self._VehicleDescr__haveIncompatibleOptionalDevices():
                return (False, 'not for current vehicle')
            (weight, maxWeight) = self._VehicleDescr__computeWeight()
            if weight > maxWeight:
                return (False, 'too heavy')
        finally:
            restorer()

        return (True, None)

    
    def installTurret(self, turretCompactDescr, gunCompactDescr, positionIndex = 0):
        turretID = parseIntCompactDescr(turretCompactDescr)[2]
        if gunCompactDescr == 0:
            gunID = self.turrets[positionIndex][1]['id'][1]
        else:
            gunID = parseIntCompactDescr(gunCompactDescr)[2]
        (prevTurretDescr, prevGunDescr) = self.turrets[positionIndex]
        newTurretDescr = _descrByID(self.type.turrets[positionIndex], turretID)
        newGunDescr = _descrByID(newTurretDescr['guns'], gunID)
        self.turrets[positionIndex] = (newTurretDescr, newGunDescr)
        self._VehicleDescr__updateAttributes()
        if self._VehicleDescr__activeTurretPos == positionIndex:
            self.activeTurretPosition = positionIndex
        
        removed = [
            prevTurretDescr['compactDescr']]
        if gunCompactDescr != 0:
            removed.append(prevGunDescr['compactDescr'])
        
        return removed

    
    def mayInstallComponent(self, compactDescr, positionIndex = 0):
        (itemTypeID, nationID, compID) = parseIntCompactDescr(compactDescr)
        itemTypeName = items.ITEM_TYPE_NAMES[itemTypeID]
        if nationID != self.type.id[0]:
            return (False, 'wrong nation')
        if itemTypeName == 'vehicleGun':
            turretDescr = self.turrets[positionIndex][0]
            newDescr = _findDescrByID(turretDescr['guns'], compID)
            setter = partial(self.turrets.__setitem__, positionIndex, (turretDescr, newDescr))
            restorer = partial(self.turrets.__setitem__, positionIndex, self.turrets[positionIndex])
        elif itemTypeName == 'vehicleChassis':
            newDescr = _findDescrByID(self.type.chassis, compID)
            setter = partial(setattr, self, 'chassis', newDescr)
            restorer = partial(setattr, self, 'chassis', self.chassis)
        elif itemTypeName == 'vehicleEngine':
            newDescr = _findDescrByID(self.type.engines, compID)
            setter = partial(setattr, self, 'engine', newDescr)
            restorer = partial(setattr, self, 'engine', self.engine)
        elif itemTypeName == 'vehicleRadio':
            newDescr = _findDescrByID(self.type.radios, compID)
            setter = partial(setattr, self, 'radio', newDescr)
            restorer = partial(setattr, self, 'radio', self.radio)
        elif itemTypeName == 'vehicleFuelTank':
            newDescr = _findDescrByID(self.type.fuelTanks, compID)
            setter = partial(setattr, self, 'fuelTank', newDescr)
            restorer = partial(setattr, self, 'fuelTank', self.fuelTank)
        else:
            return (False, 'wrong item type')
        if itemTypeName == 'vehicleGun' is None:
            if compactDescr not in self.type.installableComponents:
                return (False, 'not for this vehicle type')
            return (False, 'not for current vehicle')
        
        try:
            setter()
            if self._VehicleDescr__haveIncompatibleOptionalDevices():
                return (False, 'not for current vehicle')
            (weight, maxWeight) = self._VehicleDescr__computeWeight()
            if weight > maxWeight:
                return (False, 'too heavy')
        finally:
            restorer()

        return (True, None)

    
    def installComponent(self, compactDescr, positionIndex = 0):
        (itemTypeID, nationID, compID) = parseIntCompactDescr(compactDescr)
        itemTypeName = items.ITEM_TYPE_NAMES[itemTypeID]
        if nationID != self.type.id[0]:
            raise Exception, 'incompatible nation of component'
        nationID != self.type.id[0]
        if itemTypeName == 'vehicleGun':
            return self._VehicleDescr__installGun(compID, positionIndex)
        if itemTypeName == 'vehicleChassis':
            attrName = 'chassis'
            compList = self.type.chassis
        elif itemTypeName == 'vehicleEngine':
            attrName = 'engine'
            compList = self.type.engines
        elif itemTypeName == 'vehicleRadio':
            attrName = 'radio'
            compList = self.type.radios
        elif itemTypeName == 'vehicleFuelTank':
            attrName = 'fuelTank'
            compList = self.type.fuelTanks
        elif not False:
            raise AssertionError
        itemTypeName == 'vehicleGun'
        prevDescr = getattr(self, attrName)
        newDescr = _descrByID(compList, compID)
        setattr(self, attrName, newDescr)
        self._VehicleDescr__updateAttributes()
        return (prevDescr['compactDescr'],)

    
    def mayInstallOptionalDevice(self, compactDescr, slotIdx):
        (itemTypeID, _, deviceID) = parseIntCompactDescr(compactDescr)
        if items.ITEM_TYPE_NAMES[itemTypeID] != 'optionalDevice':
            return (False, 'wrong item type')
        device = g_cache.optionalDevices()[deviceID]
        prevDevices = self.optionalDevices
        if device in prevDevices:
            return (False, 'already installed')
        devices = list(prevDevices)
        self.optionalDevices = devices
        
        try:
            devices[slotIdx] = None
            res = device.checkCompatibilityWithVehicle(self)
            if not res[0]:
                return res
            devices[slotIdx] = device
            if self._VehicleDescr__haveIncompatibleOptionalDevices():
                return (False, 'not for current vehicle')
            (weight, maxWeight) = self._VehicleDescr__computeWeight()
            if weight > maxWeight:
                return (False, 'too heavy')
        finally:
            self.optionalDevices = prevDevices

        return (True, None)

    
    def installOptionalDevice(self, compactDescr, slotIdx):
        device = g_cache.optionalDevices()[parseIntCompactDescr(compactDescr)[2]]
        devices = self.optionalDevices
        prevDevice = devices[slotIdx]
        devices[slotIdx] = device
        self._VehicleDescr__updateAttributes()
        if prevDevice is None:
            return ((), ())
        if prevDevice['removable']:
            return ((prevDevice.compactDescr,), ())
        return ((), (prevDevice.compactDescr,))

    
    def mayRemoveOptionalDevice(self, slotIdx):
        prevDevices = self.optionalDevices
        devices = list(prevDevices)
        self.optionalDevices = devices
        
        try:
            devices[slotIdx] = None
            if self._VehicleDescr__haveIncompatibleOptionalDevices():
                return (False, 'not for current vehicle')
            (weight, maxWeight) = self._VehicleDescr__computeWeight()
            if weight > maxWeight:
                return (False, 'too heavy')
        finally:
            self.optionalDevices = prevDevices

        return (True, None)

    
    def removeOptionalDevice(self, slotIdx):
        device = self.optionalDevices[slotIdx]
        self.optionalDevices[slotIdx] = None
        self._VehicleDescr__updateAttributes()
        if device is None:
            return ((), ())
        if device['removable']:
            return ((device.compactDescr,), ())
        return ((), (device.compactDescr,))

    
    def makeCompactDescr(self):
        type = self.type
        pack = struct.pack
        header = items.ITEM_TYPE_INDICES['vehicle'] + (type.id[0] << 4)
        vehicleTypeID = type.id[1]
        chassisID = self.chassis['id'][1]
        engineID = self.engine['id'][1]
        fuelTankID = self.fuelTank['id'][1]
        radioID = self.radio['id'][1]
        cd = pack('<2B4H', header, vehicleTypeID, chassisID, engineID, fuelTankID, radioID)
        for n in xrange(len(type.turrets)):
            (turretDescr, gunDescr) = self.turrets[n]
            cd += pack('<2H', turretDescr['id'][1], gunDescr['id'][1])
        
        optionalDevices = ''
        optionalDevicesMask = 0
        if not len(self.optionalDevices) == NUM_OPTIONAL_DEVICE_SLOTS:
            raise AssertionError
        for device in self.optionalDevices:
            optionalDevicesMask <<= 1
            if device is not None:
                optionalDevices = pack('<H', device.id[1]) + optionalDevices
                optionalDevicesMask |= 1
                continue
            len(self.optionalDevices) == NUM_OPTIONAL_DEVICE_SLOTS
        
        emblemPositions = 0
        emblems = ''
        for (idx, item) in enumerate(self.playerEmblems):
            if item[0] is not None and item[0] != type.defaultPlayerEmblemID:
                emblemPositions |= 1 << idx
                emblems += _packIDAndDuration(*item)
                continue
        
        for (idx, item) in enumerate(self.playerInscriptions):
            if item[0] is not None:
                emblemPositions |= 1 << idx + 4
                emblems += _packIDAndDuration(item[0], item[1], item[2]) + chr(item[3])
                continue
        
        camouflages = ''
        for item in self.camouflages:
            if item[0] is not None:
                camouflages += _packIDAndDuration(*item)
                continue
        
        flags = 0
        flags |= optionalDevicesMask
        if emblemPositions:
            flags |= 32
        
        if self._VehicleDescr__hornID is not None:
            flags |= 64
        
        if camouflages:
            flags |= 128
        
        cd += chr(flags) + optionalDevices
        if emblemPositions:
            cd += chr(emblemPositions) + emblems
        
        if self._VehicleDescr__hornID is not None:
            cd += chr(self._VehicleDescr__hornID)
        
        if camouflages:
            cd += camouflages
        
        return cd

    
    def getCost(self):
        type = self.type
        cost = type.price
        for idx in xrange(len(self.turrets)):
            (turretDescr, gunDescr) = self.turrets[idx]
            cost = _summPriceDiff(cost, turretDescr['price'], type.turrets[idx][0]['price'])
            cost = _summPriceDiff(cost, gunDescr['price'], turretDescr['guns'][0]['price'])
        
        cost = _summPriceDiff(cost, self.chassis['price'], type.chassis[0]['price'])
        cost = _summPriceDiff(cost, self.engine['price'], type.engines[0]['price'])
        cost = _summPriceDiff(cost, self.fuelTank['price'], type.fuelTanks[0]['price'])
        cost = _summPriceDiff(cost, self.radio['price'], type.radios[0]['price'])
        for device in self.optionalDevices:
            if device is not None:
                cost = _summPriceDiff(cost, device.price, (0, 0))
                continue
        
        return cost

    
    def getMaxRepairCost(self):
        type = self.type
        cost = self.maxHealth * type.repairCost
        for (turretDescr, gunDescr) in self.turrets:
            cost += _getMaxCompRepairCost(gunDescr) + _getMaxCompRepairCost(turretDescr['turretRotatorHealth']) + _getMaxCompRepairCost(turretDescr['surveyingDeviceHealth'])
        
        cost += _getMaxCompRepairCost(self.hull['ammoBayHealth']) + _getMaxCompRepairCost(self.chassis) * 2 + _getMaxCompRepairCost(self.engine) + _getMaxCompRepairCost(self.fuelTank) + _getMaxCompRepairCost(self.radio)
        return cost

    
    def getDevices(self):
        defComps = []
        instComps = []
        type = self.type
        instComps.append(self.chassis['compactDescr'])
        defComps.append(type.chassis[0]['compactDescr'])
        instComps.append(self.engine['compactDescr'])
        defComps.append(type.engines[0]['compactDescr'])
        instComps.append(self.fuelTank['compactDescr'])
        defComps.append(type.fuelTanks[0]['compactDescr'])
        instComps.append(self.radio['compactDescr'])
        defComps.append(type.radios[0]['compactDescr'])
        for (turretDescr, gunDescr) in zip(self.turrets, type.turrets):
            turrets = None
            instComps.append(turretDescr['compactDescr'])
            defComps.append(turrets[0]['compactDescr'])
            instComps.append(gunDescr['compactDescr'])
            defComps.append(turretDescr['guns'][0]['compactDescr'])
        
        optDevices = []
        for device in self.optionalDevices:
            if device is not None:
                optDevices.append(device.compactDescr)
                continue
        
        return (defComps, instComps, optDevices)

    
    def getHitTesters(self):
        hitTesters = [
            self.chassis['hitTester'],
            self.hull['hitTester']]
        for (turretDescr, gunDescr) in self.turrets:
            hitTesters.append(turretDescr['hitTester'])
            hitTesters.append(gunDescr['hitTester'])
        
        return hitTesters

    
    def prerequisites(self):
        prereqs = set()
        for effGroup in self.type.effects.values():
            for (stages, effects, readyPrereqs) in effGroup:
                if not readyPrereqs:
                    prereqs.update(effects.prerequisites())
                    continue
            
        
        if self.chassis['effects'] is not None:
            if self.chassis['effects']['dust'] is not None:
                (effGroup, readyPrereqs) = self.chassis['effects']['dust']
                if not readyPrereqs:
                    prereqs.update(self._VehicleDescr__getChassisEffectNames(effGroup))
                
            
            if self.chassis['effects']['mud'] is not None:
                (effGroup, readyPrereqs) = self.chassis['effects']['mud']
                if not readyPrereqs:
                    prereqs.update(self._VehicleDescr__getChassisEffectNames(effGroup))
                
            
        
        for (_, gunDescr) in self.turrets:
            for tagName in ('effects', 'groundWave'):
                if gunDescr[tagName] is not None:
                    (stages, effects, readyPrereqs) = gunDescr[tagName]
                    if not readyPrereqs:
                        prereqs.update(effects.prerequisites())
                    
            
            for shotDescr in gunDescr['shots']:
                effectsDescr = g_cache.shotEffects[shotDescr['shell']['effectsIndex']]
                if not effectsDescr['prereqs']:
                    (projectileModel, effects) = effectsDescr['projectile']
                    prereqs.add(projectileModel)
                    prereqs.update(effects.prerequisites())
                    for materialName in EFFECT_MATERIALS:
                        prereqs.update(effectsDescr[materialName + 'Hit'][1].prerequisites())
                    
                    prereqs.update(effectsDescr['shallowWaterHit'][1].prerequisites())
                    prereqs.update(effectsDescr['deepWaterHit'][1].prerequisites())
                    prereqs.update(effectsDescr['armorResisted'][1].prerequisites())
                    prereqs.update(effectsDescr['armorRicochet'][1].prerequisites())
                    prereqs.update(effectsDescr['armorHit'][1].prerequisites())
                    prereqs.update(effectsDescr['armorCriticalHit'][1].prerequisites())
                    continue
            
        
        if self.type._prereqs is None:
            prereqs.add(self.hull['exhaust']['pixie'])
            for extra in self.extras:
                prereqs.update(extra.prerequisites())
            
        
        return list(prereqs)

    
    def keepPrereqs(self, prereqs):
        if not prereqs:
            return None
        for effGroup in self.type.effects.values():
            for (stages, effects, readyPrereqs) in effGroup:
                if not readyPrereqs:
                    readyPrereqs.update(_extractNeededPrereqs(prereqs, effects.prerequisites()))
                    continue
            
        
        if self.chassis['effects'] is not None:
            if self.chassis['effects']['dust'] is not None:
                (effGroup, readyPrereqs) = self.chassis['effects']['dust']
                if not readyPrereqs:
                    readyPrereqs.update(_extractNeededPrereqs(prereqs, self._VehicleDescr__getChassisEffectNames(effGroup)))
                
            
            if self.chassis['effects']['mud'] is not None:
                (effGroup, readyPrereqs) = self.chassis['effects']['mud']
                if not readyPrereqs:
                    readyPrereqs.update(_extractNeededPrereqs(prereqs, self._VehicleDescr__getChassisEffectNames(effGroup)))
                
            
        
        for (_, gunDescr) in self.turrets:
            (stages, effects, readyPrereqs) = gunDescr['effects']
            if not readyPrereqs:
                readyPrereqs.update(_extractNeededPrereqs(prereqs, effects.prerequisites()))
            
            for shotDescr in gunDescr['shots']:
                effectsDescr = g_cache.shotEffects[shotDescr['shell']['effectsIndex']]
                readyPrereqs = effectsDescr['prereqs']
                if not readyPrereqs:
                    (projectileModel, effects) = effectsDescr['projectile']
                    readyPrereqs.update(_extractNeededPrereqs(prereqs, (projectileModel,)))
                    readyPrereqs.update(_extractNeededPrereqs(prereqs, effects.prerequisites()))
                    for materialName in EFFECT_MATERIALS:
                        readyPrereqs.update(_extractNeededPrereqs(prereqs, effectsDescr[materialName + 'Hit'][1].prerequisites()))
                    
                    readyPrereqs.update(_extractNeededPrereqs(prereqs, effectsDescr['shallowWaterHit'][1].prerequisites()))
                    readyPrereqs.update(_extractNeededPrereqs(prereqs, effectsDescr['deepWaterHit'][1].prerequisites()))
                    readyPrereqs.update(_extractNeededPrereqs(prereqs, effectsDescr['armorResisted'][1].prerequisites()))
                    readyPrereqs.update(_extractNeededPrereqs(prereqs, effectsDescr['armorRicochet'][1].prerequisites()))
                    readyPrereqs.update(_extractNeededPrereqs(prereqs, effectsDescr['armorHit'][1].prerequisites()))
                    readyPrereqs.update(_extractNeededPrereqs(prereqs, effectsDescr['armorCriticalHit'][1].prerequisites()))
                    continue
            
        
        if self.type._prereqs is None:
            resourceNames = [
                self.hull['exhaust']['pixie']]
            for extra in self.extras:
                resourceNames += extra.prerequisites()
            
            self.type._prereqs = _extractNeededPrereqs(prereqs, resourceNames)
        

    
    def _VehicleDescr__getChassisEffectNames(self, effectGroup):
        ret = []
        for v in effectGroup.values():
            if isinstance(v, list):
                for s in v:
                    ret.append(s)
                
            ret.append(v)
        
        return ret

    
    def _VehicleDescr__installGun(self, gunID, turretPosition):
        (turretDescr, prevGunDescr) = self.turrets[turretPosition]
        newGunDescr = _descrByID(turretDescr['guns'], gunID)
        self.turrets[turretPosition] = (turretDescr, newGunDescr)
        self._VehicleDescr__updateAttributes()
        if self._VehicleDescr__activeTurretPos == turretPosition:
            self.activeTurretPosition = turretPosition
        
        return (prevGunDescr['compactDescr'],)

    
    def _VehicleDescr__initFromCompactDescr(self, compactDescr):
        cd = compactDescr
        unpack = struct.unpack
        
        try:
            (header, vehicleTypeID, chassisID, engineID, fuelTankID, radioID) = unpack('<2B4H', cd[:10])
            if not header & 15 == items.ITEM_TYPE_INDICES['vehicle']:
                raise AssertionError
            cd = cd[10:]
            nationID = header >> 4 & 15
            type = g_cache.vehicle(nationID, vehicleTypeID)
            customization = g_cache.customization(nationID)
            self.type = type
            self.name = type.name
            self.level = type.level
            if IS_CLIENT or IS_CELLAPP:
                self.extras = type.extras
                self.extrasDict = type.extrasDict
            
            self.hull = type.hull
            self.chassis = _descrByID(type.chassis, chassisID)
            self.engine = _descrByID(type.engines, engineID)
            self.fuelTank = _descrByID(type.fuelTanks, fuelTankID)
            self.radio = _descrByID(type.radios, radioID)
            turrets = []
            for idx in xrange(len(type.turrets)):
                (turretID, gunID) = unpack('<2H', cd[:4])
                cd = cd[4:]
                turret = _descrByID(type.turrets[idx], turretID)
                turrets.append((turret, _descrByID(turret['guns'], gunID)))
            
            self.turrets = turrets
            self.activeTurretPosition = 0
            flags = ord(cd[0])
            cd = cd[1:]
            optionalDevicesMask = flags & 15
            continue
            self.optionalDevices = [ None for idx in xrange(NUM_OPTIONAL_DEVICE_SLOTS) ]
            idx = NUM_OPTIONAL_DEVICE_SLOTS - 1
            while optionalDevicesMask:
                if optionalDevicesMask & 1:
                    self.optionalDevices[idx] = g_cache.optionalDevices()[unpack('<H', cd[:2])[0]]
                    cd = cd[2:]
                
                optionalDevicesMask >>= 1
                idx -= 1
            if not flags & 32:
                self.playerEmblems = type._defEmblems
                self.playerInscriptions = _EMPTY_INSCRIPTIONS
            else:
                positions = ord(cd[0])
                cd = cd[1:]
                if not positions & 15:
                    self.playerEmblems = type._defEmblems
                else:
                    slots = [
                        None,
                        None,
                        None,
                        None]
                    for idx in range(4):
                        if positions & 1 << idx:
                            slots[idx] = _unpackIDAndDuration(cd[:6])
                            g_cache.playerEmblems()[1][slots[idx][0]]
                            cd = cd[6:]
                            continue
                        []
                        slots[idx] = type._defEmblem
                    
                    self.playerEmblems = tuple(slots)
                if not positions & 240:
                    self.playerInscriptions = _EMPTY_INSCRIPTIONS
                else:
                    slots = [
                        None,
                        None,
                        None,
                        None]
                    for idx in range(4):
                        if positions & 1 << idx + 4:
                            slots[idx] = _unpackIDAndDuration(cd[:6]) + (ord(cd[6]),)
                            customization['inscriptions'][slots[idx][0]]
                            customization['inscriptionColors'][slots[idx][3]]
                            cd = cd[7:]
                            continue
                        header & 15 == items.ITEM_TYPE_INDICES['vehicle']
                        slots[idx] = _EMPTY_INSCRIPTION
                    
                    self.playerInscriptions = tuple(slots)
            if not flags & 64:
                self._VehicleDescr__hornID = None
            else:
                self._VehicleDescr__hornID = ord(cd[0])
                cd = cd[1:]
                g_cache.horns()[self._VehicleDescr__hornID]
            if not flags & 128:
                self.camouflages = _EMPTY_CAMOUFLAGES
                if not not cd:
                    raise AssertionError
            else:
                slots = list(_EMPTY_CAMOUFLAGES)
                while cd:
                    item = _unpackIDAndDuration(cd[:6])
                    cd = cd[6:]
                    idx = customization['camouflages'][item[0]]['kind']
                    if slots[idx][0] is not None:
                        LOG_WARNING('Second camouflage of same kind', nationID, item[0], slots[idx][0])
                    
                    slots[idx] = item
                self.camouflages = tuple(slots)
            self._VehicleDescr__updateAttributes()
        except Exception:
            LOG_ERROR('(compact descriptor to XML mismatch?)', compactDescr)
            raise 


    
    def _VehicleDescr__computeWeight(self):
        maxWeight = self.chassis['maxLoad']
        weight = self.hull['weight'] + self.chassis['weight'] + self.engine['weight'] + self.fuelTank['weight'] + self.radio['weight']
        for (turretDescr, gunDescr) in self.turrets:
            weight += turretDescr['weight'] + gunDescr['weight']
        
        vehWeightFraction = 0
        vehWeightAddition = 0
        for device in self.optionalDevices:
            if device is not None:
                (fraction, addition, maxWeightChange) = device.weightOnVehicle(self)
                vehWeightFraction += fraction
                vehWeightAddition += addition
                maxWeight += maxWeightChange
                continue
        
        return (weight * (1 + vehWeightFraction) + vehWeightAddition, maxWeight)

    
    def _VehicleDescr__haveIncompatibleOptionalDevices(self):
        for device in self.optionalDevices:
            if device is not None and not device.checkCompatibilityWithVehicle(self)[0]:
                return True
        
        return False

    
    def _VehicleDescr__updateAttributes(self):
        self.miscAttrs = None
        self.physics = None
        type = self.type
        chassis = self.chassis
        self.maxHealth = self.hull['maxHealth']
        for (turretDescr, gunDescr) in self.turrets:
            self.maxHealth += turretDescr['maxHealth']
        
        if IS_CLIENT and IS_BASEAPP or IS_WEB:
            bpl = type.balanceByComponentLevels
            modMul = g_cache.commonConfig['balanceModulesWeightMultipliers']
            vmw = g_cache.commonConfig['balanceByVehicleModule'].get(self.type.name, None)
            if vmw:
                pass
            1
            vehicleBalance = bpl[self.level] * modMul['vehicle']
            self.balanceWeight = (vehicleBalance + bpl[self.gun['level']] * modMul['gun'] + bpl[self.turret['level']] * modMul['turret'] + bpl[self.engine['level']] * modMul['engine'] + bpl[chassis['level']] * modMul['chassis'] + bpl[self.radio['level']] * modMul['radio']) * type.balanceByClass
        
        if IS_CLIENT or IS_CELLAPP:
            self.hitTester = VehicleHitTester(chassis['hitTester'], self.hull['hitTester'], chassis['hullPosition'])
        
        if IS_CLIENT and IS_CELLAPP or IS_WEB:
            (weight, maxWeight) = self._VehicleDescr__computeWeight()
            trackCenterOffset = chassis['topRightCarryingPoint'][0]
            self.physics = {
                'weight': weight,
                'enginePower': self.engine['power'],
                'specificFriction': chassis['specificFriction'],
                'minPlaneNormalY': chassis['minPlaneNormalY'],
                'trackCenterOffset': trackCenterOffset,
                'rotationIsAroundCenter': chassis['rotationIsAroundCenter'],
                'speedLimits': self.type.speedLimits,
                'navmeshGirth': chassis['navmeshGirth'],
                'carryingTriangles': chassis['carryingTriangles'],
                'brakeForce': chassis['brakeForce'],
                'terrainResistance': chassis['terrainResistance'] }
            self.miscAttrs = {
                'maxWeight': maxWeight,
                'repairSpeedFactor': 1,
                'additiveShotDispersionFactor': 1,
                'antifragmentationLiningFactor': 1,
                'circularVisionRadiusFactor': 1,
                'gunReloadTimeFactor': 1,
                'gunAimingTimeFactor': 1,
                'ammoBayHealthFactor': 1,
                'engineHealthFactor': 1,
                'chassisHealthFactor': 1,
                'fuelTankHealthFactor': 1,
                'crewLevelIncrease': 0 }
            for device in self.optionalDevices:
                if device is not None:
                    device.updateVehicleDescrAttrs(self)
                    continue
            
            physics = self.physics
            defWeight = type.hull['weight'] + chassis['weight'] + type.engines[0]['weight'] + type.fuelTanks[0]['weight'] + type.radios[0]['weight']
            for turretList in type.turrets:
                defWeight += turretList[0]['weight'] + turretList[0]['guns'][0]['weight']
            
            defResistance = chassis['terrainResistance'][0]
            rotationEnergy = type.engines[0]['power'] * (weight / defWeight) / chassis['rotationSpeed'] * defResistance
            rotationSpeedLimit = physics['enginePower'] / rotationEnergy * physics['terrainResistance'][0]
            if not chassis['rotationIsAroundCenter']:
                rotationEnergy -= trackCenterOffset * weight * chassis['specificFriction'] / defResistance
                if rotationEnergy <= 0:
                    raise Exception, 'wrong parameters of rotation of ' + type.name
                rotationEnergy <= 0
            
            if chassis['rotationSpeedLimit'] is not None:
                rotationSpeedLimit = min(rotationSpeedLimit, chassis['rotationSpeedLimit'])
            
            physics['rotationSpeedLimit'] = rotationSpeedLimit
            physics['rotationEnergy'] = rotationEnergy
            if not IS_CLIENT or IS_DEVELOPMENT:
                (invisibility1, invisibility2) = type.invisibility
                for (turretDescr, gunDescr) in self.turrets:
                    factor = turretDescr['invisibilityFactor']
                    invisibility1 *= factor
                    invisibility2 *= factor
                
                self.invisibility = (min(invisibility1, 1), min(invisibility2, 1))
            
        
        if IS_CELLAPP:
            hullPos = self.chassis['hullPosition']
            (hullBboxMin, hullBboxMax, _) = self.hull['hitTester'].bbox
            turretPosOnHull = self.hull['turretPositions'][0]
            turretLocalTopY = max(hullBboxMax.y, turretPosOnHull.y + self.turret['hitTester'].bbox[1].y)
            gunPosOnHull = turretPosOnHull + self.turret['gunPosition']
            hullLocalCenterY = (hullBboxMin.y + hullBboxMax.y) / 2
            hullLocalPt1 = Vector3(0, hullLocalCenterY, hullBboxMax.z)
            hullLocalPt2 = Vector3(0, hullLocalCenterY, hullBboxMin.z)
            hullLocalCenterZ = (hullBboxMin.z + hullBboxMax.z) / 2
            hullLocalPt3 = Vector3(hullBboxMax.x, gunPosOnHull.y, hullLocalCenterZ)
            hullLocalPt4 = Vector3(hullBboxMin.x, gunPosOnHull.y, hullLocalCenterZ)
            self.visibilityCheckPoints = (Vector3(0, hullPos.y + turretLocalTopY, 0), hullPos + gunPosOnHull, hullPos + hullLocalPt1, hullPos + hullLocalPt2, hullPos + hullLocalPt3, hullPos + hullLocalPt4)
            self.observerPosOnChassis = Vector3(0, hullPos.y + turretLocalTopY, 0)
            self.observerPosOnTurret = self.turret['gunPosition']
        



class VehicleType(object):
    
    def __init__(self, nationID, basicInfo, xmlPath):
        self.name = basicInfo['name']
        self.id = (nationID, basicInfo['id'])
        self.compactDescr = basicInfo['compactDescr']
        nation = nations.NAMES[nationID]
        section = ResMgr.openSection(xmlPath)
        if section is None:
            _xml.raiseWrongXml(None, xmlPath, 'can not open or read')
        
        xmlCtx = (None, xmlPath)
        self.tags = basicInfo['tags']
        self.level = basicInfo['level']
        self.speedLimits = (KMH_TO_MS * _xml.readPositiveFloat(xmlCtx, section, 'speedLimits/forward'), KMH_TO_MS * _xml.readPositiveFloat(xmlCtx, section, 'speedLimits/backward'))
        self.repairCost = _xml.readNonNegativeFloat(xmlCtx, section, 'repairCost')
        if not IS_CLIENT or IS_DEVELOPMENT:
            self.xpFactor = _xml.readNonNegativeFloat(xmlCtx, section, 'xpFactor')
            self.freeXpFactor = _xml.readNonNegativeFloat(xmlCtx, section, 'freeXpFactor')
            self.crewXpFactor = _xml.readNonNegativeFloat(xmlCtx, section, 'crewXpFactor')
            self.creditsFactor = _xml.readNonNegativeFloat(xmlCtx, section, 'creditsFactor')
            self.healthBurnPerSec = _xml.readNonNegativeFloat(xmlCtx, section, 'healthBurnPerSec')
            self.healthBurnPerSecLossFraction = _DEFAULT_HEALTH_BURN_PER_SEC_LOSS_FRACTION
            self.invisibility = (_xml.readFraction(xmlCtx, section, 'invisibility/moving'), _xml.readFraction(xmlCtx, section, 'invisibility/still'))
        
        self.crewRoles = _readCrew(xmlCtx, section, 'crew')
        if IS_BASEAPP or IS_WEB:
            self.price = basicInfo['price']
            self.showInShop = basicInfo['showInShop']
        
        commonConfig = g_cache.commonConfig
        if IS_CLIENT or IS_CELLAPP:
            self.extras = commonConfig['extras']
            self.extrasDict = commonConfig['extrasDict']
            self.devices = commonConfig['devices']
            self.tankmen = _selectCrewExtras(self.crewRoles, self.extrasDict)
        
        if IS_CLIENT and IS_BASEAPP or IS_WEB:
            classTag = tuple(VEHICLE_CLASS_TAGS & self.tags)[0]
            self.balanceByClass = commonConfig['balanceByVehicleClasses'][classTag]
            self.balanceByComponentLevels = commonConfig['balanceByComponentLevels']
        
        if IS_CLIENT or IS_WEB:
            self.userString = basicInfo['userString']
            self.shortUserString = basicInfo['shortUserString']
            self.description = basicInfo['description']
        
        if IS_CLIENT:
            self.damageStickersLodDist = commonConfig['miscParams']['damageStickersLodDist']
            collisionVelCfg = commonConfig['miscParams']['collisionEffectVelocities']
            self.heavyCollisionEffectVelocities = {
                'hull': collisionVelCfg['hull'][1],
                'track': collisionVelCfg['track'][1],
                'waterContact': collisionVelCfg['waterContact'][1] }
            self.effects = _readVehicleEffects(xmlCtx, section, 'effects', commonConfig['defaultVehicleEffects'])
            (self.camouflageTiling, self.camouflageExclusionMask) = _readCamouflageTilingAndMask(xmlCtx, section, 'camouflage', True)
            self.emblemsLodDist = _readLodDist(xmlCtx, section, 'emblems/lodDist')
            self.emblemsAlpha = _xml.readFraction(xmlCtx, section, 'emblems/alpha')
            self._prereqs = None
        
        if IS_CELLAPP or IS_CLIENT:
            collisionVelCfg = commonConfig['miscParams']['collisionEffectVelocities']
            self.collisionEffectVelocities = {
                'hull': collisionVelCfg['hull'][0],
                'track': collisionVelCfg['track'][0],
                'waterContact': collisionVelCfg['waterContact'][0] }
        
        defEmblemName = _xml.readNonEmptyString(xmlCtx, section, 'emblems/default')
        self.defaultPlayerEmblemID = g_cache.playerEmblems()[2].get(defEmblemName)
        if self.defaultPlayerEmblemID is None:
            _xml.raiseWrongXml(xmlCtx, 'emblems/default', "unknown emblem '%s'" % defEmblemName)
        
        self._defEmblem = (self.defaultPlayerEmblemID, _CUSTOMIZATION_EPOCH, 0)
        self._defEmblems = (self._defEmblem, self._defEmblem, self._defEmblem, self._defEmblem)
        self.camouflagePriceFactor = _xml.readNonNegativeFloat(xmlCtx, section, 'camouflage/priceFactor')
        (self.hornPriceFactor, self.hornDistanceFactor, self.hornVolumeFactor) = _readVehicleHorns(xmlCtx, section, 'horns')
        unlocksDescrs = []
        self.unlocks = _readUnlocks(xmlCtx, section, 'unlocks', unlocksDescrs)
        self.hull = _readHull((xmlCtx, 'hull'), _xml.getSubsection(xmlCtx, section, 'hull'))
        self.chassis = _readInstallableComponents(xmlCtx, section, 'chassis', nationID, _readChassis, _defaultLocalReader, g_cache.chassis(nationID), g_cache.chassisIDs(nationID), unlocksDescrs)
        self.engines = _readInstallableComponents(xmlCtx, section, 'engines', nationID, _readEngine, _defaultLocalReader, g_cache.engines(nationID), g_cache.engineIDs(nationID), unlocksDescrs)
        self.fuelTanks = _readInstallableComponents(xmlCtx, section, 'fuelTanks', nationID, _readFuelTank, _defaultLocalReader, g_cache.fuelTanks(nationID), g_cache.fuelTankIDs(nationID), unlocksDescrs)
        self.radios = _readInstallableComponents(xmlCtx, section, 'radios', nationID, _readRadio, _defaultLocalReader, g_cache.radios(nationID), g_cache.radioIDs(nationID), unlocksDescrs)
        turretsList = []
        for n in xrange(len(self.hull['turretPositions'])):
            turrets = _readInstallableComponents(xmlCtx, section, 'turrets' + repr(n), nationID, _readTurret, _readTurretLocals, g_cache.turrets(nationID), g_cache.turretIDs(nationID), unlocksDescrs)
            turretsList.append(turrets)
        
        self.turrets = tuple(turretsList)
        compactDescrs = set()
        _collectComponents(compactDescrs, self.chassis)
        _collectComponents(compactDescrs, self.engines)
        _collectComponents(compactDescrs, self.fuelTanks)
        _collectComponents(compactDescrs, self.radios)
        for turrets in self.turrets:
            _collectComponents(compactDescrs, turrets)
            for turret in turrets:
                _collectComponents(compactDescrs, turret['guns'])
            
        
        self.installableComponents = compactDescrs
        self.unlocksDescrs = self._VehicleType__convertAndValidateUnlocksDescrs(unlocksDescrs)
        self.autounlockedItems = self._VehicleType__collectDefaultUnlocks()
        section = None
        ResMgr.purge(xmlPath, True)

    
    def _VehicleType__convertAndValidateUnlocksDescrs(self, srcList):
        nationID = self.id[0]
        destList = []
        reqItems = { }
        for descr in srcList:
            itemTypeName = descr[1]
            itemName = descr[2]
            itemID = None
            
            try:
                if itemTypeName == 'vehicle':
                    itemID = g_list.getIDsByName(nations.NAMES[nationID] + ':' + itemName)[1]
                
                if itemTypeName == 'vehicleChassis':
                    itemID = g_cache.chassisIDs(nationID)[itemName]
                
                if itemTypeName == 'vehicleTurret':
                    itemID = g_cache.turretIDs(nationID)[itemName]
                
                if itemTypeName == 'vehicleGun':
                    itemID = g_cache.gunIDs(nationID)[itemName]
                
                if itemTypeName == 'vehicleEngine':
                    itemID = g_cache.engineIDs(nationID)[itemName]
                
                if itemTypeName == 'vehicleFuelTank':
                    itemID = g_cache.fuelTankIDs(nationID)[itemName]
                
                if itemTypeName == 'vehicleRadio':
                    itemID = g_cache.radioIDs(nationID)[itemName]
            except Exception:
                LOG_CURRENT_EXCEPTION()
                raise Exception, "wrong name '%s' in <unlocks> of '%s'" % (itemName, self.name)

            compactDescr = makeIntCompactDescrByID(itemTypeName, nationID, itemID)
            if itemTypeName != 'vehicle' and compactDescr not in self.installableComponents:
                raise Exception, "component '%s' in <unlocks> is not for '%s'" % (itemName, self.name)
            compactDescr not in self.installableComponents
            reqItems.setdefault(compactDescr, set()).update(descr[3:])
            destList.append((descr[0], compactDescr))
        
        for descr in reqItems.itervalues():
            for compactDescr in tuple(descr):
                _collectReqItemsRecursively(descr, tuple(reqItems.get(compactDescr, ())), reqItems)
            
        
        for idx in xrange(len(destList)):
            descr = destList[idx]
            destList[idx] = descr + tuple(reqItems[descr[1]])
        
        return destList

    
    def _VehicleType__collectDefaultUnlocks(self):
        autounlocks = []
        autounlocks.append(self.chassis[0]['compactDescr'])
        autounlocks.append(self.engines[0]['compactDescr'])
        autounlocks.append(self.fuelTanks[0]['compactDescr'])
        autounlocks.append(self.radios[0]['compactDescr'])
        for turrets in self.turrets:
            turret = turrets[0]
            autounlocks.append(turret['compactDescr'])
            autounlocks.append(turret['guns'][0]['compactDescr'])
        
        return autounlocks



class Cache(object):
    
    def __init__(self):
        self._Cache__vehicles = { }
        self._Cache__commonConfig = None
        continue
        self._Cache__chassis = [ None for i in nations.NAMES ]
        continue
        self._Cache__engines = [ None for i in nations.NAMES ]
        continue
        self._Cache__fuelTanks = [ None for i in nations.NAMES ]
        continue
        self._Cache__radios = [ None for i in nations.NAMES ]
        continue
        self._Cache__turrets = [ None for i in nations.NAMES ]
        continue
        self._Cache__guns = [ None for i in nations.NAMES ]
        continue
        self._Cache__shells = [ None for i in nations.NAMES ]
        self._Cache__optionalDevices = None
        self._Cache__optionalDeviceIDs = None
        self._Cache__equipments = None
        self._Cache__equipmentIDs = None
        continue
        self._Cache__chassisIDs = [ None for i in nations.NAMES ]
        continue
        self._Cache__engineIDs = [ None for i in nations.NAMES ]
        continue
        self._Cache__fuelTankIDs = [ None for i in nations.NAMES ]
        continue
        self._Cache__radioIDs = [ None for i in nations.NAMES ]
        continue
        self._Cache__turretIDs = [ None for i in nations.NAMES ]
        continue
        self._Cache__gunIDs = [ None for i in nations.NAMES ]
        continue
        self._Cache__shellIDs = [ None for i in nations.NAMES ]
        continue
        self._Cache__customization = [ None for i in nations.NAMES ]
        self._Cache__horns = None
        self._Cache__playerEmblems = None
        self._Cache__playerIscriptions = None
        self._Cache__shotEffects = None
        self._Cache__shotEffectsIndexes = None
        self._Cache__damageStickers = None
        if IS_CLIENT:
            self._Cache__vehicleEffects = None
            self._Cache__gunEffects = None
            self._Cache__chassisEffects = None
        

    
    def clearPrereqs(self):
        pass

    
    def getPriceCache(self):
        cache = { }
        horns = cache.setdefault('hornCost', { })
        for (hornID, descr) in self._Cache__horns.items():
            horns[hornID] = descr['gold']
        
        shop = cache.setdefault('items', { })
        for nationIdx in xrange(len(nations.NAMES)):
            nationShop = shop.setdefault(nationIdx, { })
            (vehPrices, vehNotShown) = nationShop.setdefault(_VEHICLE, ({ }, set()))
            for (innationIdx, vehDescr) in g_list.getList(nationIdx).iteritems():
                vehType = getVehicleType(vehDescr['compactDescr'])
                vehPrices[innationIdx] = (vehDescr['price'][0], vehDescr['price'][1], vehType.camouflagePriceFactor, vehType.hornPriceFactor)
                if not vehDescr['showInShop']:
                    vehNotShown.add(innationIdx)
                    continue
            
            itemLists = {
                _CHASSIS: self.chassis(nationIdx),
                _TURRET: self.turrets(nationIdx),
                _GUN: self.guns(nationIdx),
                _ENGINE: self.engines(nationIdx),
                _FUEL_TANK: self.fuelTanks(nationIdx),
                _RADIO: self.radios(nationIdx),
                _SHELL: self.shells(nationIdx) }
            self._Cache__addItemListsToNationShop(itemLists, nationShop)
        
        nationShop = shop.setdefault(nations.NONE_INDEX, { })
        itemLists = {
            _EQUIPMENT: self.equipments(),
            _OPTIONALDEVICE: self.optionalDevices() }
        self._Cache__addItemListsToNationShop(itemLists, nationShop)
        customization = cache.setdefault('customization', { })
        for nationIdx in xrange(len(nations.NAMES)):
            nationCustomization = customization.setdefault(nationIdx, { })
            camouflages = nationCustomization.setdefault('camouflages', { })
            if self._Cache__customization[nationIdx].has_key('camouflages'):
                for (id, camouflage) in self._Cache__customization[nationIdx]['camouflages'].iteritems():
                    camouflages[id] = camouflage['priceFactor']
                
        
        return cache

    
    def _Cache__addItemListsToNationShop(self, itemLists, nationShop):
        for (itemTypeIdx, descriptions) in itemLists.iteritems():
            (itemPrices, itemNotShown) = nationShop.setdefault(itemTypeIdx, ({ }, set()))
            for descr in descriptions.itervalues():
                if descr.get('status', '') == 'empty':
                    continue
                
                itemPrices[descr['compactDescr']] = descr['price']
                if not descr['showInShop']:
                    itemNotShown.add(descr['compactDescr'])
                    continue
            
        

    
    def setPriceCache(self, cache):
        horns = cache['hornCost']
        for (hornID, price) in horns.items():
            self._Cache__horns[hornID]['gold'] = price
        
        shop = cache['items']
        for (nationIdx, nationShop) in shop.items():
            LOG_DZ('Updating nation ', nationIdx)
            if nationIdx == nations.NONE_INDEX:
                itemLists = {
                    _EQUIPMENT: self._Cache__equipments,
                    _OPTIONALDEVICE: self._Cache__optionalDevices }
                self._Cache__updateItemListsFromNationShop(nationShop, itemLists)
                continue
            
            LOG_DZ('Start updating vehicles, count=', len(nationShop[_VEHICLE][0]))
            vehList = g_list._VehicleList__nations[nationIdx]
            (vehPrices, vehNotShown) = nationShop[_VEHICLE]
            for (inNationIdx, price) in vehPrices.items():
                vehInfo = vehList[inNationIdx]
                vehType = getVehicleType(vehInfo['compactDescr'])
                if inNationIdx in vehNotShown:
                    pass
                1
                showInShop = True
                if vehInfo['price'] != (price[0], price[1]) and vehInfo['showInShop'] != showInShop and vehType.camouflagePriceFactor != price[2] or vehType.hornPriceFactor != price[3]:
                    LOG_DZ('Vehicle updated, name=%s, price:%s->%s, showInShop:%s->%s, camouflagePriceFactor:%s->%s, hornPriceFactor:%s->%s' % (vehInfo['name'], vehInfo['price'], (price[0], price[1]), vehInfo['showInShop'], showInShop, vehType.camouflagePriceFactor, price[2], vehType.hornPriceFactor, price[3]))
                    vehInfo['price'] = (price[0], price[1])
                    vehType.price = (price[0], price[1])
                    vehInfo['showInShop'] = showInShop
                    vehType.showInShop = showInShop
                    vehType.camouflagePriceFactor = price[2]
                    vehType.hornPriceFactor = price[3]
                    continue
            
            count = 0
            for (itemType, items) in nationShop.items():
                if itemType != _VEHICLE:
                    pass
                1
                len(items[0]) += 0
            
            LOG_DZ('Start updating items, count=', count)
            itemLists = {
                _CHASSIS: self._Cache__chassis[nationIdx],
                _TURRET: self._Cache__turrets[nationIdx],
                _GUN: self._Cache__guns[nationIdx],
                _ENGINE: self._Cache__engines[nationIdx],
                _FUEL_TANK: self._Cache__fuelTanks[nationIdx],
                _RADIO: self._Cache__radios[nationIdx],
                _SHELL: self._Cache__shells[nationIdx] }
            self._Cache__updateItemListsFromNationShop(nationShop, itemLists)
        
        customization = cache.setdefault('customization', { })
        for (nationIdx, nationCustomization) in cache['customization'].iteritems():
            camouflages = self._Cache__customization[nationIdx].get('camouflages', None)
            if camouflages is None:
                continue
            
            for (id, priceFactor) in nationCustomization['camouflages'].iteritems():
                camouflage = camouflages[id]
                if camouflage['priceFactor'] != priceFactor:
                    LOG_DZ('Camouflage updated: id=%s, priceFactor:%s->%s' % (id, camouflage['priceFactor'], priceFactor))
                    camouflage['priceFactor'] = priceFactor
                    continue
            
        

    
    def _Cache__updateItemListsFromNationShop(self, nationShop, itemLists):
        for (itemTypeIdx, items) in itemLists.iteritems():
            if items is None:
                continue
            
            (itemPrices, itemNotShown) = nationShop[itemTypeIdx]
            for (inNationIdx, item) in items.items():
                compDescr = item['compactDescr']
                price = itemPrices.get(compDescr, None)
                if price is None:
                    continue
                
                if compDescr in itemNotShown:
                    pass
                1
                showInShop = True
                if item['price'] != price or item['showInShop'] != showInShop:
                    LOG_DZ('Item updated, name=%s, price:%s->%s, showInShop:%s->%s' % (item['name'], item['price'], price, item['showInShop'], showInShop))
                    if itemTypeIdx == _EQUIPMENT or itemTypeIdx == _OPTIONALDEVICE:
                        item.updatePrice(price, showInShop)
                    else:
                        item['price'] = price
                        item['showInShop'] = showInShop
                itemTypeIdx == _OPTIONALDEVICE
            
        

    
    def vehicle(self, nationID, vehicleTypeID):
        id = (nationID, vehicleTypeID)
        vt = self._Cache__vehicles.get(id)
        if vt:
            return vt
        nation = nations.NAMES[nationID]
        basicInfo = g_list.getList(nationID)[vehicleTypeID]
        xmlName = basicInfo['name'].split(':')[1]
        xmlPath = _VEHICLE_TYPE_XML_PATH + nation + '/' + xmlName + '.xml'
        vt = VehicleType(nationID, basicInfo, xmlPath)
        self._Cache__vehicles[id] = vt
        return vt

    
    def chassis(self, nationID):
        return self._Cache__getList(nationID, 'chassis')

    
    def chassisIDs(self, nationID):
        return self._Cache__getList(nationID, 'chassisIDs')

    
    def engines(self, nationID):
        return self._Cache__getList(nationID, 'engines')

    
    def engineIDs(self, nationID):
        return self._Cache__getList(nationID, 'engineIDs')

    
    def fuelTanks(self, nationID):
        return self._Cache__getList(nationID, 'fuelTanks')

    
    def fuelTankIDs(self, nationID):
        return self._Cache__getList(nationID, 'fuelTankIDs')

    
    def radios(self, nationID):
        return self._Cache__getList(nationID, 'radios')

    
    def radioIDs(self, nationID):
        return self._Cache__getList(nationID, 'radioIDs')

    
    def turrets(self, nationID):
        return self._Cache__getList(nationID, 'turrets')

    
    def turretIDs(self, nationID):
        return self._Cache__getList(nationID, 'turretIDs')

    
    def guns(self, nationID):
        return self._Cache__getList(nationID, 'guns')

    
    def gunIDs(self, nationID):
        return self._Cache__getList(nationID, 'gunIDs')

    
    def shells(self, nationID):
        return self._Cache__getList(nationID, 'shells')

    
    def shellIDs(self, nationID):
        return self._Cache__getList(nationID, 'shellIDs')

    
    def customization(self, nationID):
        descr = self._Cache__customization[nationID]
        if descr is None:
            nationName = nations.NAMES[nationID]
            if nationName not in nations.AVAILABLE_NAMES:
                descr = { }
            else:
                descr = _readCustomization(_VEHICLE_TYPE_XML_PATH + nationName + '/customization.xml', nationID)
            self._Cache__customization[nationID] = descr
        
        return descr

    
    def horns(self):
        if self._Cache__horns is None:
            self._Cache__horns = _readHorns(_VEHICLE_TYPE_XML_PATH + 'common/horns.xml')
        
        return self._Cache__horns

    
    def playerEmblems(self):
        if self._Cache__playerEmblems is None:
            self._Cache__playerEmblems = _readPlayerEmblems(_VEHICLE_TYPE_XML_PATH + 'common/player_emblems.xml')
        
        return self._Cache__playerEmblems

    
    def optionalDevices(self):
        if self._Cache__optionalDevices is None:
            artefacts = artefacts
            import items
            (self._Cache__optionalDevices, self._Cache__optionalDeviceIDs) = _readArtefacts(_VEHICLE_TYPE_XML_PATH + 'common/optional_devices.xml')
        
        return self._Cache__optionalDevices

    
    def optionalDeviceIDs(self):
        if self._Cache__optionalDeviceIDs is None:
            artefacts = artefacts
            import items
            (self._Cache__optionalDevices, self._Cache__optionalDeviceIDs) = _readArtefacts(_VEHICLE_TYPE_XML_PATH + 'common/optional_devices.xml')
        
        return self._Cache__optionalDeviceIDs

    
    def equipments(self):
        if self._Cache__equipments is None:
            artefacts = artefacts
            import items
            (self._Cache__equipments, self._Cache__equipmentIDs) = _readArtefacts(_VEHICLE_TYPE_XML_PATH + 'common/equipments.xml')
        
        return self._Cache__equipments

    
    def equipmentIDs(self):
        if self._Cache__equipmentIDs is None:
            artefacts = artefacts
            import items
            (self._Cache__equipments, self._Cache__equipmentIDs) = _readArtefacts(_VEHICLE_TYPE_XML_PATH + 'common/equipments.xml')
        
        return self._Cache__equipmentIDs

    
    def shotEffects(self):
        if self._Cache__shotEffects is None:
            (self._Cache__shotEffectsIndexes, self._Cache__shotEffects) = _readShotEffectGroups(_VEHICLE_TYPE_XML_PATH + 'common/shot_effects.xml')
        
        return self._Cache__shotEffects

    shotEffects = property(shotEffects)
    
    def shotEffectsIndexes(self):
        if self._Cache__shotEffects is None:
            (self._Cache__shotEffectsIndexes, self._Cache__shotEffects) = _readShotEffectGroups(_VEHICLE_TYPE_XML_PATH + 'common/shot_effects.xml')
        
        return self._Cache__shotEffectsIndexes

    shotEffectsIndexes = property(shotEffectsIndexes)
    
    def damageStickers(self):
        if self._Cache__damageStickers is None:
            self._Cache__damageStickers = _readDamageStickers(_VEHICLE_TYPE_XML_PATH + 'common/damage_stickers.xml')
        
        return self._Cache__damageStickers

    damageStickers = property(damageStickers)
    
    def commonConfig(self):
        if self._Cache__commonConfig is None:
            commonXmlPath = _VEHICLE_TYPE_XML_PATH + 'common/vehicle.xml'
            commonXml = ResMgr.openSection(commonXmlPath)
            if commonXml is None:
                _xml.raiseWrongXml(None, commonXmlPath, 'can not open or read')
            
            self._Cache__commonConfig = _readCommonConfig((None, commonXmlPath), commonXml)
            hornCooldownParams = self._Cache__commonConfig['miscParams']['hornCooldown']
            HORN_COOLDOWN.WINDOW = hornCooldownParams['window']
            HORN_COOLDOWN.CLIENT_WINDOW_EXPANSION = hornCooldownParams['clientWindowExpansion']
            HORN_COOLDOWN.MAX_SIGNALS = hornCooldownParams['maxSignals']
            commonXml = None
            ResMgr.purge(commonXmlPath, True)
        
        return self._Cache__commonConfig

    commonConfig = property(commonConfig)
    
    def _vehicleEffects(self):
        if self._Cache__vehicleEffects is None:
            self._Cache__vehicleEffects = _readEffectGroups(_VEHICLE_TYPE_XML_PATH + 'common/vehicle_effects.xml', True)
        
        return self._Cache__vehicleEffects

    _vehicleEffects = property(_vehicleEffects)
    
    def _gunEffects(self):
        if self._Cache__gunEffects is None:
            self._Cache__gunEffects = _readEffectGroups(_VEHICLE_TYPE_XML_PATH + 'common/gun_effects.xml')
        
        return self._Cache__gunEffects

    _gunEffects = property(_gunEffects)
    
    def _chassisEffects(self):
        if self._Cache__chassisEffects is None:
            self._Cache__chassisEffects = _readChassisEffectGroups(_VEHICLE_TYPE_XML_PATH + 'common/chassis_effects.xml')
        
        return self._Cache__chassisEffects

    _chassisEffects = property(_chassisEffects)
    
    def _Cache__getList(self, nationID, listName):
        nations = getattr(self, '_Cache__' + listName)
        if nations[nationID] is None:
            self._Cache__readNation(nationID)
        
        return nations[nationID]

    
    def _Cache__readNation(self, nationID):
        nationName = nations.NAMES[nationID]
        if nationName not in nations.AVAILABLE_NAMES:
            emptyDict = { }
            self._Cache__chassis[nationID] = emptyDict
            self._Cache__chassisIDs[nationID] = emptyDict
            self._Cache__engines[nationID] = emptyDict
            self._Cache__engineIDs[nationID] = emptyDict
            self._Cache__fuelTanks[nationID] = emptyDict
            self._Cache__fuelTankIDs[nationID] = emptyDict
            self._Cache__radios[nationID] = emptyDict
            self._Cache__radioIDs[nationID] = emptyDict
            self._Cache__turrets[nationID] = emptyDict
            self._Cache__turretIDs[nationID] = emptyDict
            self._Cache__guns[nationID] = emptyDict
            self._Cache__gunIDs[nationID] = emptyDict
            self._Cache__shells[nationID] = emptyDict
            self._Cache__shellIDs[nationID] = emptyDict
            return None
        compsXmlPath = _VEHICLE_TYPE_XML_PATH + nationName + '/components/'
        (self._Cache__chassis[nationID], self._Cache__chassisIDs[nationID]) = _readComponents(compsXmlPath + 'chassis.xml', _readChassis, nationID, 'vehicleChassis')
        (self._Cache__engines[nationID], self._Cache__engineIDs[nationID]) = _readComponents(compsXmlPath + 'engines.xml', _readEngine, nationID, 'vehicleEngine')
        (self._Cache__fuelTanks[nationID], self._Cache__fuelTankIDs[nationID]) = _readComponents(compsXmlPath + 'fuelTanks.xml', _readFuelTank, nationID, 'vehicleFuelTank')
        (self._Cache__radios[nationID], self._Cache__radioIDs[nationID]) = _readComponents(compsXmlPath + 'radios.xml', _readRadio, nationID, 'vehicleRadio')
        (self._Cache__shells[nationID], self._Cache__shellIDs[nationID]) = _readShells(compsXmlPath + 'shells.xml', nationID)
        (self._Cache__guns[nationID], self._Cache__gunIDs[nationID]) = _readComponents(compsXmlPath + 'guns.xml', _readGun, nationID, 'vehicleGun')
        (self._Cache__turrets[nationID], self._Cache__turretIDs[nationID]) = _readComponents(compsXmlPath + 'turrets.xml', _readTurret, nationID, 'vehicleTurret')

    
    def _Cache__idsFromNames(self, descrs):
        return dict((lambda .0: for d in .0:
(d['name'], d['id']))(descrs.itervalues()))



class VehicleList(object):
    
    def __init__(self):
        self._VehicleList__ids = { }
        list = []
        for nation in nations.NAMES:
            if nation not in nations.AVAILABLE_NAMES:
                list.append({ })
                continue
            
            xmlPath = _VEHICLE_TYPE_XML_PATH + nation + '/list.xml'
            section = ResMgr.openSection(xmlPath)
            if section is None:
                _xml.raiseWrongXml(None, xmlPath, 'can not open or read')
            
            descrs = self._VehicleList__readVehicleList(nation, section, xmlPath)
            list.append(descrs)
            nationID = nations.INDICES[nation]
            self._VehicleList__ids.update((dict,)((lambda .0: for d in .0:
(d['name'], (nationID, d['id'])))(descrs.itervalues())))
            ResMgr.purge(xmlPath, True)
        
        self._VehicleList__nations = tuple(list)

    
    def getList(self, nationID):
        return self._VehicleList__nations[nationID]

    
    def getIDsByName(self, name):
        ids = self._VehicleList__ids.get(name)
        if ids is None:
            raise Exception, "unknown vehicle type name '%s'" % name
        ids is None
        return ids

    
    def _VehicleList__readVehicleList(self, nation, section, xmlPath):
        res = { }
        ids = { }
        for (vname, vsection) in section.items():
            ctx = (None, xmlPath + '/' + vname)
            if vname in ids:
                _xml.raiseWrongXml(ctx, '', 'vehicle type name is not unique')
            
            id = _xml.readInt(ctx, vsection, 'id', 0, 255)
            if id in res:
                _xml.raiseWrongXml(ctx, 'id', 'is not unique')
            
            ids[vname] = id
            res[id] = {
                'name': nation + ':' + vname,
                'id': id,
                'compactDescr': makeIntCompactDescrByID('vehicle', nations.INDICES[nation], id),
                'level': _readLevel(ctx, vsection) }
            tags = _readTags(ctx, vsection, 'tags', 'vehicle')
            if 1 != len(tags & VEHICLE_CLASS_TAGS):
                _xml.raiseWrongXml(ctx, 'tags', 'vehicle class tag is missing or is multiple')
            
            res[id]['tags'] = tags
            if IS_CLIENT or IS_WEB:
                res[id]['userString'] = i18n.makeString(vsection.readString('userString'))
                res[id]['description'] = i18n.makeString(vsection.readString('description'))
                res[id]['shortUserString'] = i18n.makeString(vsection.readString('shortUserString'))
                if not res[id]['shortUserString']:
                    res[id]['shortUserString'] = res[id]['userString']
                
            
            price = _xml.readPrice(ctx, vsection, 'price')
            if price[1]:
                res[id]['tags'] |= frozenset(('premium',))
            
            if IS_BASEAPP or IS_WEB:
                res[id]['price'] = price
                res[id]['showInShop'] = not vsection.readBool('notInShop', False)
                continue
        
        return res



def makeIntCompactDescrByID(itemTypeName, nationID, itemID):
    header = items.ITEM_TYPE_INDICES[itemTypeName] + (nationID << 4)
    return (itemID << 8) + header


def parseIntCompactDescr(compactDescr):
    return (compactDescr & 15, compactDescr >> 4 & 15, compactDescr >> 8 & 65535)


def parseVehicleCompactDescr(compactDescr):
    (header, vehicleTypeID) = struct.unpack('2B', compactDescr[0:2])
    return (header >> 4 & 15, vehicleTypeID)


def getDictDescr(compactDescr):
    
    try:
        itemTypeID = compactDescr & 15
        nationID = compactDescr >> 4 & 15
        compTypeID = compactDescr >> 8 & 65535
        itemTypeName = items.ITEM_TYPE_NAMES[itemTypeID]
        return _dictDescrGetters[itemTypeName](nationID, compTypeID)
    except Exception:
        LOG_CURRENT_EXCEPTION()
        LOG_ERROR('(compact description to XML mismatch?)', compactDescr)
        raise 


_dictDescrGetters = {
    'shell': (lambda nationID, compTypeID: g_cache.shells(nationID)[compTypeID]),
    'equipment': (lambda nationID, compTypeID: g_cache.equipments()[compTypeID]),
    'optionalDevice': (lambda nationID, compTypeID: g_cache.optionalDevices()[compTypeID]),
    'vehicleGun': (lambda nationID, compTypeID: g_cache.guns(nationID)[compTypeID]),
    'vehicleTurret': (lambda nationID, compTypeID: g_cache.turrets(nationID)[compTypeID]),
    'vehicleEngine': (lambda nationID, compTypeID: g_cache.engines(nationID)[compTypeID]),
    'vehicleRadio': (lambda nationID, compTypeID: g_cache.radios(nationID)[compTypeID]),
    'vehicleChassis': (lambda nationID, compTypeID: g_cache.chassis(nationID)[compTypeID]),
    'vehicleFuelTank': (lambda nationID, compTypeID: g_cache.fuelTanks(nationID)[compTypeID]) }

def getVehicleType(compactDescr):
    if type(compactDescr) is IntType:
        nationID = compactDescr >> 4 & 15
        vehicleTypeID = compactDescr >> 8 & 65535
    else:
        (header, vehicleTypeID) = struct.unpack('2B', compactDescr[0:2])
        nationID = header >> 4 & 15
    return g_cache.vehicle(nationID, vehicleTypeID)


def isShellSuitableForGun(shellCompactDescr, gunDescr):
    (itemTypeID, nationID, shellTypeID) = parseIntCompactDescr(shellCompactDescr)
    if not itemTypeID == items.ITEM_TYPE_INDICES['shell']:
        raise AssertionError
    shellID = (nationID, shellTypeID)
    for shotDescr in gunDescr['shots']:
        if shotDescr['shell']['id'] == shellID:
            return True
    
    return False


def getEmptyAmmoForGun(gunDescr):
    ammo = []
    for shot in gunDescr['shots']:
        ammo.append(shot['shell']['compactDescr'])
        ammo.append(0)
    
    if not ammo:
        ammo.append(gunDescr['shots'][0]['shell']['compactDescr'])
        ammo.append(0)
    
    return ammo


def getDefaultAmmoForGun(gunDescr):
    return _getAmmoForGun(gunDescr, None)


def getUniformAmmoForGun(gunDescr):
    shots = len(gunDescr['shots'])
    if shots:
        pass
    1
    defaultPortion = 1
    return _getAmmoForGun(gunDescr, defaultPortion)


def _getAmmoForGun(gunDescr, defaultPortion = None):
    ammo = []
    maxCount = gunDescr['maxAmmo']
    clipSize = gunDescr['clip'][0]
    currCount = 0
    for shot in gunDescr['shots']:
        if defaultPortion is None:
            portion = shot['defaultPortion']
        else:
            portion = defaultPortion
        shotCount = int(portion * maxCount / clipSize + 0.5) * clipSize
        if currCount + shotCount > maxCount:
            shotCount = maxCount - currCount
        
        currCount += shotCount
        ammo.append(shot['shell']['compactDescr'])
        ammo.append(shotCount)
    
    if not ammo:
        ammo.append(gunDescr['shots'][0]['shell']['compactDescr'])
        ammo.append(maxCount)
    
    return ammo


def getUnlocksSources():
    res = { }
    for nationID in xrange(len(nations.NAMES)):
        for vehicleTypeID in g_list.getList(nationID).iterkeys():
            vehicleType = g_cache.vehicle(nationID, vehicleTypeID)
            for descr in vehicleType.unlocksDescrs:
                cd = descr[1]
                res.setdefault(cd, set()).add(vehicleType)
            
        
    
    return res


def _readComponents(xmlPath, reader, nationID, itemTypeName):
    section = ResMgr.openSection(xmlPath)
    if section is None:
        _xml.raiseWrongXml(None, xmlPath, 'can not open or read')
    
    xmlCtx = (None, xmlPath)
    descrs = { }
    ids = { }
    for name in _xml.getSubsection(xmlCtx, section, 'ids').keys():
        name = intern(name)
        id = _xml.readInt(xmlCtx, section, 'ids/' + name, 0, 65535)
        if descrs.has_key(id):
            _xml.raiseWrongXml(xmlCtx, 'ids/' + name, 'name or ID is not unique')
        
        ids[name] = id
        descrs[id] = {
            'itemTypeName': itemTypeName,
            'name': name,
            'id': (nationID, id),
            'compactDescr': makeIntCompactDescrByID(itemTypeName, nationID, id),
            'status': 'empty' }
    
    for (name, subsection) in _xml.getChildren(xmlCtx, section, 'shared'):
        ctx = (xmlCtx, 'shared')
        id = ids.get(name)
        if id is None:
            _xml.raiseWrongXml(ctx, name, 'unknown name')
        
        descr = descrs[id]
        if descr['status'] != 'empty':
            _xml.raiseWrongXml(ctx, name, 'already defined')
        
        descr.update(reader((ctx, name), subsection, descr['compactDescr']))
        descr['status'] = 'shared'
    
    section = None
    subsection = None
    ResMgr.purge(xmlPath, True)
    return (descrs, ids)


def _readInstallableComponents(xmlCtx, section, subsectionName, nationID, reader, localReader, cachedDescrs, cachedIDs, unlocksDescrs, parentItem = None):
    res = []
    for (sname, subsection) in _xml.getChildren(xmlCtx, section, subsectionName):
        ctx = (xmlCtx, subsectionName + '/' + sname)
        id = cachedIDs.get(sname)
        if id is None:
            _xml.raiseWrongXml(ctx, '', 'unknown name')
        
        descr = cachedDescrs[id]
        if subsection.asString == 'shared':
            if descr['status'] != 'shared':
                _xml.raiseWrongXml(ctx, sname, 'the component is not shared')
            
            res.append(localReader(ctx, subsection, descr, unlocksDescrs, parentItem))
            continue
        if descr['status'] != 'empty':
            _xml.raiseWrongXml(ctx, '', 'the component is already defined somewhere')
        
        descr.update(reader(ctx, subsection, descr['compactDescr'], unlocksDescrs, parentItem))
        descr['status'] = 'local'
        res.append(descr)
    
    if not res:
        _xml.raiseWrongXml(xmlCtx, subsectionName, 'should be at least one subsection')
    
    return tuple(res)


def _readTags(xmlCtx, section, subsectionName, itemTypeName):
    tagNames = _xml.readString(xmlCtx, section, subsectionName).split()
    res = set()
    allowedTagNames = items.getTypeInfoByName(itemTypeName)['tags']
    for tagName in tagNames:
        if tagName not in allowedTagNames:
            _xml.raiseWrongXml(xmlCtx, subsectionName, "unknown tag '%s'" % tagName)
        
        res.add(intern(tagName))
    
    return frozenset(res)


def _readLevel(xmlCtx, section):
    level = section.readInt('level', 1)
    if 1 <= level:
        pass
    level <= 10
    if not 1:
        _xml.raiseWrongSection(xmlCtx, 'level')
    
    return level


def _readHull(xmlCtx, section):
    res = {
        'hitTester': _readHitTester(xmlCtx, section, 'hitTester'),
        'materials': _readArmor(xmlCtx, section, 'armor'),
        'weight': _xml.readNonNegativeFloat(xmlCtx, section, 'weight'),
        'maxHealth': _xml.readInt(xmlCtx, section, 'maxHealth', 1),
        'ammoBayHealth': _readDeviceHealthParams(xmlCtx, section, 'ammoBayHealth', False) }
    if not IS_CLIENT or IS_DEVELOPMENT:
        res['armorHomogenization'] = _xml.readPositiveFloat(xmlCtx, section, 'armorHomogenization')
    
    v = []
    for s in _xml.getSubsection(xmlCtx, section, 'turretPositions').values():
        v.append(_xml.readVector3((xmlCtx, 'turretPositions'), s, ''))
    
    if not v:
        _xml.raiseWrongSection(xmlCtx, 'turretPositions')
    
    res['turretPositions'] = tuple(v)
    if not section.has_key('fakeTurrets'):
        res['fakeTurrets'] = _defFakeTurrets
    else:
        numTurrets = len(res['turretPositions'])
        res['fakeTurrets'] = {
            'lobby': _readFakeTurretIndices(xmlCtx, section, 'fakeTurrets/lobby', numTurrets),
            'battle': _readFakeTurretIndices(xmlCtx, section, 'fakeTurrets/battle', numTurrets) }
    if IS_CLIENT:
        res['emblemSlots'] = _readEmblemSlots(xmlCtx, section, 'emblemSlots')
        res['models'] = _readModels(xmlCtx, section, 'models')
        res['swinging'] = {
            'lodDist': _readLodDist(xmlCtx, section, 'swinging/lodDist'),
            'sensitivityToImpulse': _xml.readNonNegativeFloat(xmlCtx, section, 'swinging/sensitivityToImpulse'),
            'pitchParams': _xml.readTupleOfFloats(xmlCtx, section, 'swinging/pitchParams', 6),
            'rollParams': _xml.readTupleOfFloats(xmlCtx, section, 'swinging/rollParams', 7) }
        res['exhaust'] = {
            'pixie': _xml.readNonEmptyString(xmlCtx, section, 'exhaust/pixie'),
            'rates': (0,) + _xml.readTupleOfFloats(xmlCtx, section, 'exhaust/rates', 3),
            'nodes': _xml.readNonEmptyString(xmlCtx, section, 'exhaust/nodes').split() }
    
    if IS_CLIENT or IS_WEB:
        res['primaryArmor'] = _readPrimaryArmor(xmlCtx, section, 'primaryArmor', res['materials'])
    
    return res

_defFakeTurrets = {
    'lobby': (),
    'battle': () }

def _readChassis(xmlCtx, section, compactDescr, unlocksDescrs = None, parentItem = None):
    res = {
        'tags': _readTags(xmlCtx, section, 'tags', 'vehicleChassis'),
        'level': _readLevel(xmlCtx, section),
        'hullPosition': _xml.readVector3(xmlCtx, section, 'hullPosition'),
        'hitTester': _readHitTester(xmlCtx, section, 'hitTester'),
        'topRightCarryingPoint': _xml.readPositiveVector2(xmlCtx, section, 'topRightCarryingPoint'),
        'navmeshGirth': _xml.readPositiveFloat(xmlCtx, section, 'navmeshGirth'),
        'minPlaneNormalY': cos(radians(_xml.readPositiveFloat(xmlCtx, section, 'maxClimbAngle'))),
        'materials': _readArmor(xmlCtx, section, 'armor'),
        'weight': _xml.readPositiveFloat(xmlCtx, section, 'weight'),
        'maxLoad': _xml.readPositiveFloat(xmlCtx, section, 'maxLoad'),
        'specificFriction': _DEFAULT_SPECIFIC_FRICTION,
        'rotationSpeed': radians(_xml.readPositiveFloat(xmlCtx, section, 'rotationSpeed')),
        'rotationIsAroundCenter': _xml.readBool(xmlCtx, section, 'rotationIsAroundCenter') }
    if section.has_key('rotationSpeedLimit'):
        res['rotationSpeedLimit'] = radians(_xml.readPositiveFloat(xmlCtx, section, 'rotationSpeedLimit'))
    else:
        res['rotationSpeedLimit'] = None
    res['shotDispersionFactors'] = (_xml.readNonNegativeFloat(xmlCtx, section, 'shotDispersionFactors/vehicleMovement') / KMH_TO_MS, _xml.readNonNegativeFloat(xmlCtx, section, 'shotDispersionFactors/vehicleRotation') / radians(1))
    res['brakeForce'] = _xml.readPositiveFloat(xmlCtx, section, 'brakeForce') * 9.81
    v = _xml.readVector3(xmlCtx, section, 'terrainResistance').tuple()
    if 0 < v[0] and v[0] <= v[1]:
        pass
    v[1] <= v[2]
    if not 1:
        _xml.raiseWrongSection(xmlCtx, 'terrainResistance')
    
    res['terrainResistance'] = v
    if not IS_CLIENT or IS_DEVELOPMENT:
        res['armorHomogenization'] = 1
        res['bulkHealthFactor'] = _xml.readPositiveFloat(xmlCtx, section, 'bulkHealthFactor')
    
    res.update(_readDeviceHealthParams(xmlCtx, section))
    if IS_CLIENT and IS_CELLAPP or IS_WEB:
        v = res['topRightCarryingPoint']
        topLeft = Vector2(-(v.x), v.y)
        bottomLeft = Vector2(-(v.x), -(v.y))
        topRight = Vector2(v.x, v.y)
        bottomRight = Vector2(v.x, -(v.y))
        res['carryingTriangles'] = (((topLeft + bottomLeft) / 2, topRight, bottomRight), ((topRight + bottomRight) / 2, bottomLeft, topLeft))
    
    if IS_CLIENT or IS_CELLAPP:
        wheelGroups = []
        wheels = []
        for (sname, subsection) in _xml.getChildren(xmlCtx, section, 'wheels'):
            if sname == 'group':
                ctx = (xmlCtx, 'wheels/group')
                v = (_xml.readBool(ctx, subsection, 'isLeft'), _xml.readNonEmptyString(ctx, subsection, 'template'), _xml.readInt(ctx, subsection, 'count', 1), subsection.readInt('startIndex', 0), _xml.readPositiveFloat(ctx, subsection, 'radius'))
                wheelGroups.append(v)
                continue
            if sname == 'wheel':
                ctx = (xmlCtx, 'wheels/wheel')
                v = (_xml.readBool(ctx, subsection, 'isLeft'), _xml.readNonEmptyString(ctx, subsection, 'name'), _xml.readPositiveFloat(ctx, subsection, 'radius'))
                wheels.append(v)
                continue
        
        drivingWheelNames = section.readString('drivingWheels').split()
        if len(drivingWheelNames) != 2:
            _xml.raiseWrongSection(xmlCtx, 'drivingWheels')
        
        frontWheelSize = None
        rearWheelSize = None
        for (_, wheelName, wheelRadius) in wheels:
            if wheelName == drivingWheelNames[0]:
                frontWheelSize = wheelRadius * 2.2
            elif wheelName == drivingWheelNames[1]:
                rearWheelSize = wheelRadius * 2.2
            
            if frontWheelSize is not None and rearWheelSize is not None:
                break
                continue
        
        res['drivingWheelsSizes'] = (frontWheelSize, rearWheelSize)
    
    v = _xml.readPrice(xmlCtx, section, 'price')
    if IS_BASEAPP or IS_WEB:
        res['price'] = v
        res['showInShop'] = not section.readBool('notInShop', False)
    
    if IS_CLIENT or IS_WEB:
        _readUserText(res, section)
    
    if IS_CLIENT:
        res['models'] = _readModels(xmlCtx, section, 'models')
        res['traces'] = {
            'lodDist': _readLodDist(xmlCtx, section, 'traces/lodDist'),
            'bufferPrefs': _xml.readNonEmptyString(xmlCtx, section, 'traces/bufferPrefs'),
            'textureSet': _xml.readNonEmptyString(xmlCtx, section, 'traces/textureSet'),
            'centerOffset': res['topRightCarryingPoint'][0],
            'size': _xml.readPositiveVector2(xmlCtx, section, 'traces/size') }
        res['tracks'] = {
            'lodDist': _readLodDist(xmlCtx, section, 'tracks/lodDist'),
            'leftMaterial': _xml.readNonEmptyString(xmlCtx, section, 'tracks/leftMaterial'),
            'rightMaterial': _xml.readNonEmptyString(xmlCtx, section, 'tracks/rightMaterial'),
            'textureScale': _xml.readFloat(xmlCtx, section, 'tracks/textureScale') }
        res['wheels'] = {
            'lodDist': _readLodDist(xmlCtx, section, 'wheels/lodDist') }
        res['effects'] = {
            'lodDist': _readLodDist(xmlCtx, section, 'effects/lodDist'),
            'dust': _readChassisEffects(xmlCtx, section, 'effects/dust'),
            'mud': _readChassisEffects(xmlCtx, section, 'effects/mud') }
        res['sound'] = _xml.readNonEmptyString(xmlCtx, section, 'sound')
        res['wheels']['groups'] = wheelGroups
        res['wheels']['wheels'] = wheels
    
    res['unlocks'] = _readUnlocks(xmlCtx, section, 'unlocks', unlocksDescrs, compactDescr)
    return res


def _readEngine(xmlCtx, section, compactDescr, unlocksDescrs = None, parentItem = None):
    res = {
        'tags': _readTags(xmlCtx, section, 'tags', 'vehicleEngine'),
        'level': _readLevel(xmlCtx, section),
        'power': _xml.readPositiveFloat(xmlCtx, section, 'power') * HP_TO_WATTS,
        'weight': _xml.readPositiveFloat(xmlCtx, section, 'weight'),
        'fireStartingChance': _xml.readFraction(xmlCtx, section, 'fireStartingChance'),
        'minFireStartingDamage': g_cache.commonConfig['miscParams']['minFireStartingDamage'] }
    v = _xml.readPrice(xmlCtx, section, 'price')
    if IS_BASEAPP or IS_WEB:
        res['price'] = v
        res['showInShop'] = not section.readBool('notInShop', False)
    
    if IS_CLIENT or IS_WEB:
        _readUserText(res, section)
    
    if IS_CLIENT:
        res['sound'] = _xml.readNonEmptyString(xmlCtx, section, 'sound')
    
    res.update(_readDeviceHealthParams(xmlCtx, section))
    res['unlocks'] = _readUnlocks(xmlCtx, section, 'unlocks', unlocksDescrs, compactDescr)
    return res


def _readFuelTank(xmlCtx, section, compactDescr, unlocksDescrs = None, parentItem = None):
    res = {
        'tags': _readTags(xmlCtx, section, 'tags', 'vehicleEngine'),
        'level': _readLevel(xmlCtx, section),
        'weight': _xml.readPositiveFloat(xmlCtx, section, 'weight') }
    v = _xml.readPrice(xmlCtx, section, 'price')
    if IS_BASEAPP or IS_WEB:
        res['price'] = v
        res['showInShop'] = not section.readBool('notInShop', False)
    
    if IS_CLIENT or IS_WEB:
        _readUserText(res, section)
    
    res.update(_readDeviceHealthParams(xmlCtx, section, '', False))
    res['unlocks'] = _readUnlocks(xmlCtx, section, 'unlocks', unlocksDescrs, compactDescr)
    return res


def _readRadio(xmlCtx, section, compactDescr, unlocksDescrs = None, parentItem = None):
    res = {
        'tags': _readTags(xmlCtx, section, 'tags', 'vehicleEngine'),
        'level': _readLevel(xmlCtx, section),
        'weight': _xml.readNonNegativeFloat(xmlCtx, section, 'weight'),
        'distance': _xml.readNonNegativeFloat(xmlCtx, section, 'distance') }
    v = _xml.readPrice(xmlCtx, section, 'price')
    if IS_BASEAPP or IS_WEB:
        res['price'] = v
        res['showInShop'] = not section.readBool('notInShop', False)
    
    if IS_CLIENT or IS_WEB:
        _readUserText(res, section)
    
    res.update(_readDeviceHealthParams(xmlCtx, section))
    res['unlocks'] = _readUnlocks(xmlCtx, section, 'unlocks', unlocksDescrs, compactDescr)
    return res


def _readTurret(xmlCtx, section, compactDescr, unlocksDescrs = None, parentItem = None):
    res = {
        'tags': _readTags(xmlCtx, section, 'tags', 'vehicleTurret'),
        'level': _readLevel(xmlCtx, section),
        'hitTester': _readHitTester(xmlCtx, section, 'hitTester'),
        'gunPosition': _xml.readVector3(xmlCtx, section, 'gunPosition'),
        'materials': _readArmor(xmlCtx, section, 'armor'),
        'weight': _xml.readNonNegativeFloat(xmlCtx, section, 'weight'),
        'maxHealth': _xml.readInt(xmlCtx, section, 'maxHealth', 1),
        'rotationSpeed': radians(_xml.readPositiveFloat(xmlCtx, section, 'rotationSpeed')),
        'turretRotatorHealth': _readDeviceHealthParams(xmlCtx, section, 'turretRotatorHealth'),
        'surveyingDeviceHealth': _readDeviceHealthParams(xmlCtx, section, 'surveyingDeviceHealth') }
    if not IS_CLIENT or IS_DEVELOPMENT:
        res['armorHomogenization'] = _xml.readPositiveFloat(xmlCtx, section, 'armorHomogenization')
        if section.has_key('invisibilityFactor'):
            res['invisibilityFactor'] = _xml.readNonNegativeFloat(xmlCtx, section, 'invisibilityFactor')
        else:
            res['invisibilityFactor'] = 1
    
    v = _xml.readPrice(xmlCtx, section, 'price')
    if IS_BASEAPP or IS_WEB:
        res['price'] = v
        res['showInShop'] = not section.readBool('notInShop', False)
    
    if IS_CLIENT or IS_WEB:
        _readUserText(res, section)
        res['primaryArmor'] = _readPrimaryArmor(xmlCtx, section, 'primaryArmor', res['materials'])
    
    if IS_CLIENT:
        res['models'] = _readModels(xmlCtx, section, 'models')
        res['showEmblemsOnGun'] = section.readBool('showEmblemsOnGun', False)
        res['emblemSlots'] = _readEmblemSlots(xmlCtx, section, 'emblemSlots')
        if section.has_key('camouflage'):
            (res['camouflageTiling'], res['camouflageExclusionMask']) = _readCamouflageTilingAndMask(xmlCtx, section, 'camouflage', False)
        
    
    v = _xml.readNonNegativeFloat(xmlCtx, section, 'circularVisionRadius')
    res['circularVisionRadius'] = v
    v = _xml.readVector2(xmlCtx, section, 'yawLimits')
    if v[0] > v[1]:
        _xml.raiseWrongSection(xmlCtx, 'yawLimits')
    
    if v[0] > -179 or v[1] < 179:
        pass
    1
    v = None
    res['yawLimits'] = v
    nationID = parseIntCompactDescr(compactDescr)[1]
    res['guns'] = _readInstallableComponents(xmlCtx, section, 'guns', nationID, _readGun, _readGunLocals, g_cache.guns(nationID), g_cache.gunIDs(nationID), unlocksDescrs, compactDescr)
    res['unlocks'] = _readUnlocks(xmlCtx, section, 'unlocks', unlocksDescrs, compactDescr)
    return res


def _readTurretLocals(xmlCtx, section, sharedDescr, unlocksDescrs, parentItem = None):
    hasOverride = False
    nationID = sharedDescr['id'][0]
    if not section.has_key('yawLimits'):
        yawLimits = sharedDescr['yawLimits']
    else:
        hasOverride = True
        v = _xml.readVector2(xmlCtx, section, 'yawLimits')
        if v[0] > v[1]:
            _xml.raiseWrongSection(xmlCtx, 'yawLimits')
        
        if v[0] > -179 or v[1] < 179:
            pass
        1
        yawLimits = None
    if not section.has_key('guns'):
        guns = sharedDescr['guns']
    else:
        hasOverride = True
        guns = _readInstallableComponents(xmlCtx, section, 'guns', nationID, _readGun, _readGunLocals, g_cache.guns(nationID), g_cache.gunIDs(nationID), unlocksDescrs, sharedDescr['compactDescr'])
    if not section.has_key('unlocks'):
        unlocks = sharedDescr['unlocks']
    else:
        hasOverride = True
        unlocks = _readUnlocks(xmlCtx, section, 'unlocks', unlocksDescrs, sharedDescr['compactDescr'])
    if not hasOverride:
        return sharedDescr
    descr = sharedDescr.copy()
    descr['yawLimits'] = yawLimits
    descr['guns'] = guns
    descr['unlocks'] = unlocks
    return descr


def _readGun(xmlCtx, section, compactDescr, unlocksDescrs = None, turretCompactDescr = None):
    res = {
        'tags': _readTags(xmlCtx, section, 'tags', 'vehicleGun'),
        'level': _readLevel(xmlCtx, section),
        'rotationSpeed': radians(_xml.readPositiveFloat(xmlCtx, section, 'rotationSpeed')),
        'weight': _xml.readPositiveFloat(xmlCtx, section, 'weight'),
        'reloadTime': _xml.readPositiveFloat(xmlCtx, section, 'reloadTime'),
        'aimingTime': _xml.readPositiveFloat(xmlCtx, section, 'aimingTime'),
        'maxAmmo': _xml.readInt(xmlCtx, section, 'maxAmmo', 1) }
    if not IS_CLIENT or IS_DEVELOPMENT:
        res['invisibilityFactorAtShot'] = _xml.readNonNegativeFloat(xmlCtx, section, 'invisibilityFactorAtShot')
        res['armorHomogenization'] = 1
    
    v = _xml.readPrice(xmlCtx, section, 'price')
    if IS_BASEAPP or IS_WEB:
        res['price'] = v
        res['showInShop'] = not section.readBool('notInShop', False)
    
    if IS_CLIENT or IS_WEB:
        _readUserText(res, section)
    
    if IS_CLIENT:
        if section.has_key('models'):
            res['models'] = _readModels(xmlCtx, section, 'models')
        else:
            res['models'] = None
        effName = _xml.readNonEmptyString(xmlCtx, section, 'effects')
        eff = g_cache._gunEffects.get(effName)
        if eff is None:
            _xml.raiseWrongXml(xmlCtx, 'effects', "unknown effect '%s'" % effName)
        
        res['effects'] = eff
        groundWaveEffName = section.readString('groundWave', '')
        if groundWaveEffName == '':
            res['groundWave'] = None
        else:
            eff = g_cache._gunEffects.get(groundWaveEffName)
            if eff is None:
                _xml.raiseWrongXml(xmlCtx, 'groundWave', "unknown effect '%s'" % groundWaveEffName)
            else:
                res['groundWave'] = eff
        res['impulse'] = _xml.readNonNegativeFloat(xmlCtx, section, 'impulse')
        res['recoil'] = {
            'lodDist': _readLodDist(xmlCtx, section, 'recoil/lodDist'),
            'amplitude': _xml.readNonNegativeFloat(xmlCtx, section, 'recoil/amplitude'),
            'backoffTime': _xml.readNonNegativeFloat(xmlCtx, section, 'recoil/backoffTime'),
            'returnTime': _xml.readNonNegativeFloat(xmlCtx, section, 'recoil/returnTime') }
        if section.has_key('camouflage'):
            (res['camouflageTiling'], res['camouflageExclusionMask']) = _readCamouflageTilingAndMask(xmlCtx, section, 'camouflage', False)
        
    
    if section.has_key('hitTester'):
        res['hitTester'] = _readHitTester(xmlCtx, section, 'hitTester')
    else:
        res['hitTester'] = None
    if section.has_key('armor'):
        res['materials'] = _readArmor(xmlCtx, section, 'armor')
    else:
        res['materials'] = None
    if not section.has_key('pitchLimits'):
        _xml.raiseWrongSection(xmlCtx, 'pitchLimits')
    else:
        v = _xml.readVector2(xmlCtx, section, 'pitchLimits')
        if v[0] > v[1]:
            _xml.raiseWrongSection(xmlCtx, 'pitchLimits')
        
        basicLimits = (radians(v[0]), radians(v[1]))
        plimsSec = {
            'basic': basicLimits,
            'absolute': basicLimits }
        if section.has_key('extraPitchLimits'):
            _readGunPitchExtraLimits((xmlCtx, 'extraPitchLimits'), section['extraPitchLimits'], pitchLimits)
        
        res['pitchLimits'] = plimsSec
    res.update(_readDeviceHealthParams(xmlCtx, section))
    res['shotDispersionAngle'] = _xml.readNonNegativeFloat(xmlCtx, section, 'shotDispersionRadius') / 100
    res['shotDispersionFactors'] = _readGunShotDispersionFactors(xmlCtx, section, 'shotDispersionFactors')
    if not section.has_key('burst'):
        res['burst'] = (1, 0)
    else:
        res['burst'] = _readGunClipBurst(xmlCtx, section, 'burst')
    if not section.has_key('clip'):
        res['clip'] = (1, 0)
    else:
        res['clip'] = _readGunClipBurst(xmlCtx, section, 'clip')
    if res['burst'][0] > res['clip'][0]:
        pass
    res['clip'][0] > 1
    if 1:
        _xml.raiseWrongXml(xmlCtx, 'burst', 'burst/count is larger than clip/count')
    
    nationID = parseIntCompactDescr(compactDescr)[1]
    v = []
    projSpeedFactor = g_cache.commonConfig['miscParams']['projectileSpeedFactor']
    for (sname, subsection) in _xml.getChildren(xmlCtx, section, 'shots'):
        v.append(_readShot((xmlCtx, 'shots/' + sname), subsection, nationID, projSpeedFactor))
    
    if not v:
        _xml.raiseWrongXml(xmlCtx, 'shots', 'no shots are specified')
    
    if IS_DEVELOPMENT and res['burst'][0] > 1:
        for shot in v:
            if shot['maxDistance'] > 400:
                _xml.raiseWrongXml(xmlCtx, 'shots/' + shot['shell']['name'], 'maxDistance > 400m is not allowed for autocannons')
                continue
        
    
    res['shots'] = tuple(v)
    res['unlocks'] = _readUnlocks(xmlCtx, section, 'unlocks', unlocksDescrs, compactDescr)
    return res


def _readGunLocals(xmlCtx, section, sharedDescr, unlocksDescrs, turretCompactDescr):
    hasOverride = False
    if section.has_key('pitchLimits'):
        hasOverride = True
        v = _xml.readVector2(xmlCtx, section, 'pitchLimits')
        if v[0] > v[1]:
            _xml.raiseWrongSection(xmlCtx, 'pitchLimits')
        
        basicLimits = (radians(v[0]), radians(v[1]))
        pitchLimits = {
            'basic': basicLimits,
            'absolute': basicLimits }
    else:
        pitchLimits = dict(sharedDescr['pitchLimits'])
    if section.has_key('extraPitchLimits'):
        hasOverride = True
        _readGunPitchExtraLimits((xmlCtx, 'extraPitchLimits'), section['extraPitchLimits'], pitchLimits)
    
    if not section.has_key('rotationSpeed'):
        rotationSpeed = sharedDescr['rotationSpeed']
    else:
        hasOverride = True
        rotationSpeed = radians(_xml.readPositiveFloat(xmlCtx, section, 'rotationSpeed'))
    if not section.has_key('reloadTime'):
        reloadTime = sharedDescr['reloadTime']
    else:
        hasOverride = True
        reloadTime = _xml.readPositiveFloat(xmlCtx, section, 'reloadTime')
    if not section.has_key('aimingTime'):
        aimingTime = sharedDescr['aimingTime']
    else:
        hasOverride = True
        aimingTime = _xml.readPositiveFloat(xmlCtx, section, 'aimingTime')
    if not section.has_key('maxAmmo'):
        ammo = sharedDescr['maxAmmo']
    else:
        hasOverride = True
        ammo = _xml.readInt(xmlCtx, section, 'maxAmmo', 1)
    if not section.has_key('shotDispersionRadius'):
        shotDispAngle = sharedDescr['shotDispersionAngle']
    else:
        hasOverride = True
        shotDispAngle = _xml.readNonNegativeFloat(xmlCtx, section, 'shotDispersionRadius') / 100
    if not section.has_key('shotDispersionFactors'):
        shotDispFactors = sharedDescr['shotDispersionFactors']
    else:
        hasOverride = True
        shotDispFactors = _readGunShotDispersionFactors(xmlCtx, section, 'shotDispersionFactors')
    if not section.has_key('burst'):
        burst = sharedDescr['burst']
    else:
        hasOverride = True
        burst = _readGunClipBurst(xmlCtx, section, 'burst')
    if not section.has_key('clip'):
        clip = sharedDescr['clip']
    else:
        hasOverride = True
        clip = _readGunClipBurst(xmlCtx, section, 'clip')
    if burst[0] > clip[0]:
        pass
    clip[0] > 1
    if 1:
        _xml.raiseWrongXml(xmlCtx, 'burst', 'burst/count is larger than clip/count')
    
    if not IS_CLIENT or IS_DEVELOPMENT:
        if not section.has_key('invisibilityFactorAtShot'):
            invisibilityFactorAtShot = sharedDescr['invisibilityFactorAtShot']
        else:
            hasOverride = True
            invisibilityFactorAtShot = _xml.readNonNegativeFloat(xmlCtx, section, 'invisibilityFactorAtShot')
    
    if IS_CLIENT:
        if not section.has_key('models'):
            models = sharedDescr['models']
            if models is None:
                _xml.raiseWrongSection(xmlCtx, 'models')
            
        else:
            hasOverride = True
            models = _readModels(xmlCtx, section, 'models')
        if not section.has_key('effects'):
            effects = sharedDescr['effects']
        else:
            hasOverride = True
            effName = _xml.readNonEmptyString(xmlCtx, section, 'effects')
            effects = g_cache._gunEffects.get(effName)
            if effects is None:
                _xml.raiseWrongXml(xmlCtx, 'effects', "unknown effect '%s'" % effName)
            
        if not section.has_key('camouflage'):
            camTiling = sharedDescr.get('camouflageTiling')
            camExclMask = sharedDescr.get('camouflageExclusionMask')
        else:
            hasOverride = True
            (camTiling, camExclMask) = _readCamouflageTilingAndMask(xmlCtx, section, 'camouflage', False)
    
    if IS_BASEAPP:
        hitTester = None
        materials = None
    elif not section.has_key('hitTester'):
        hitTester = sharedDescr['hitTester']
        if hitTester is None:
            _xml.raiseWrongSection(xmlCtx, 'hitTester')
        
    else:
        hasOverride = True
        hitTester = _readHitTester(xmlCtx, section, 'hitTester')
    if not section.has_key('armor'):
        materials = sharedDescr['materials']
        if materials is None:
            _xml.raiseWrongSection(xmlCtx, 'armor')
        
    else:
        hasOverride = True
        materials = _readArmor(xmlCtx, section, 'armor')
    if not section.has_key('unlocks'):
        unlocks = sharedDescr['unlocks']
    else:
        hasOverride = True
        unlocks = _readUnlocks(xmlCtx, section, 'unlocks', unlocksDescrs, sharedDescr['compactDescr'], turretCompactDescr)
    if not hasOverride:
        return sharedDescr
    descr = sharedDescr.copy()
    descr['pitchLimits'] = pitchLimits
    descr['rotationSpeed'] = rotationSpeed
    descr['reloadTime'] = reloadTime
    descr['aimingTime'] = aimingTime
    descr['maxAmmo'] = ammo
    descr['shotDispersionAngle'] = shotDispAngle
    descr['shotDispersionFactors'] = shotDispFactors
    descr['burst'] = burst
    descr['clip'] = clip
    descr['unlocks'] = unlocks
    descr['hitTester'] = hitTester
    descr['materials'] = materials
    if IS_CLIENT:
        descr['models'] = models
        descr['effects'] = effects
        if camTiling is not None:
            descr['camouflageTiling'] = camTiling
            descr['camouflageExclusionMask'] = camExclMask
        
    
    if not IS_CLIENT or IS_DEVELOPMENT:
        descr['invisibilityFactorAtShot'] = invisibilityFactorAtShot
    
    return descr


def _readGunClipBurst(xmlCtx, section, type):
    count = _xml.readInt(xmlCtx, section, type + '/count', 1)
    interval = 60 / _xml.readPositiveFloat(xmlCtx, section, type + '/rate')
    if count > 1:
        pass
    1
    return (interval, 0)


def _readGunPitchExtraLimits(xmlCtx, section, descToUpdate):
    readSomething = False
    extraAngle = 0
    if section.has_key('front'):
        v = _xml.readVector3(xmlCtx, section, 'front')
        if v[0] > v[1]:
            _xml.raiseWrongSection(xmlCtx, 'front')
        
        descToUpdate['front'] = tuple((lambda .0: for ang in .0:
radians(ang))(v))
        descToUpdate['absolute'] = (min(descToUpdate['absolute'][0], descToUpdate['front'][0]), max(descToUpdate['absolute'][1], descToUpdate['front'][1]))
        extraAngle += descToUpdate['front'][2]
        readSomething = True
    
    if section.has_key('back'):
        v = _xml.readVector3(xmlCtx, section, 'back')
        if v[0] > v[1]:
            _xml.raiseWrongSection(xmlCtx, 'back')
        
        descToUpdate['back'] = tuple((lambda .0: for ang in .0:
radians(ang))(v))
        descToUpdate['absolute'] = (min(descToUpdate['absolute'][0], descToUpdate['back'][0]), max(descToUpdate['absolute'][1], descToUpdate['back'][1]))
        extraAngle += descToUpdate['back'][2]
        readSomething = True
    
    if section.has_key('transition'):
        v = _xml.readFloat(xmlCtx, section, 'transition')
        descToUpdate['transition'] = radians(v)
        extraAngle += descToUpdate['transition'] * 4
        readSomething = True
    else:
        extraAngle += DEFAULT_GUN_PITCH_LIMITS_TRANSITION * 4
    if extraAngle > pi * 2:
        _xml.raiseWrongXml(xmlCtx[0], xmlCtx[1], 'overlapping sectors')
    
    return readSomething


def _readShells(xmlPath, nationID):
    section = ResMgr.openSection(xmlPath)
    if section is None:
        _xml.raiseWrongXml(None, xmlPath, 'can not open or read')
    
    icons = { }
    if IS_CLIENT or IS_WEB:
        for (name, subsection) in _xml.getChildren((None, xmlPath), section, 'icons'):
            name = intern(name)
            if icons.has_key(name):
                _xml.raiseWrongXml((None, xmlPath + '/icons'), name, 'name is not unique')
            
            icons[name] = _xml.readIcon((None, xmlPath + '/icons'), subsection, '')
        
    
    descrs = { }
    ids = { }
    for (name, subsection) in section.items():
        if name == 'icons':
            continue
        
        xmlCtx = (None, xmlPath + '/' + name)
        name = intern(name)
        if ids.has_key(name):
            _xml.raiseWrongXml(xmlCtx, '', 'shell type name is not unique')
        
        id = _xml.readInt(xmlCtx, subsection, 'id', 0, 65535)
        if descrs.has_key(id):
            _xml.raiseWrongXml(xmlCtx, 'id', 'shell type ID is not unique')
        
        descrs[id] = _readShell(xmlCtx, subsection, name, nationID, id, icons)
        ids[name] = id
    
    section = None
    subsection = None
    ResMgr.purge(xmlPath, True)
    return (descrs, ids)


def _readShell(xmlCtx, section, name, nationID, shellTypeID, icons):
    res = {
        'itemTypeName': 'shell',
        'name': name,
        'id': (nationID, shellTypeID),
        'compactDescr': makeIntCompactDescrByID('shell', nationID, shellTypeID),
        'caliber': _xml.readInt(xmlCtx, section, 'caliber', 1),
        'isTracer': section.readBool('isTracer', False),
        'damage': (_xml.readPositiveFloat(xmlCtx, section, 'damage/armor'), _xml.readPositiveFloat(xmlCtx, section, 'damage/devices')),
        'damageRandomization': 0.25,
        'piercingPowerRandomization': 0.25 }
    if IS_CLIENT or IS_WEB:
        res['userStrin
