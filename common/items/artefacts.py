# Source Generated with Decompyle++
# File: artefacts.pyc (Python 2.6)

from types import IntType
import items
import nations
from items import _xml, vehicles
from debug_utils import *
from constants import IS_CLIENT, IS_BASEAPP, IS_CELLAPP, IS_WEB, IS_DEVELOPMENT
if IS_CLIENT:
    from helpers import i18n
elif IS_WEB:
    from web_stubs import *


class OptionalDevice(object):
    
    def get(self, key, defVal = None):
        return self.__dict__.get(key, defVal)

    
    def __getitem__(self, key):
        return self.__dict__[key]

    
    def init(self, xmlCtx, section):
        self._OptionalDevice__readBasicConfig(xmlCtx, section)
        xmlCtx = (xmlCtx, 'script')
        section = section['script']
        (self._vehWeightFraction, self._weight) = _readWeight(xmlCtx, section)
        self._maxWeightChange = 0
        self._readConfig(xmlCtx, section)

    
    def weightOnVehicle(self, vehicleDescr):
        return (self._vehWeightFraction, self._weight, 0)

    
    def checkCompatibilityWithVehicle(self, vehicleDescr):
        if self._OptionalDevice__filter is None:
            return (True, None)
        return self._OptionalDevice__filter.checkCompatibility(vehicleDescr)

    
    def updateVehicleDescrAttrs(self, vehicleDescr):
        pass

    
    def updatePrice(self, newPrice, showInShop):
        self.price = newPrice
        self.showInShop = showInShop

    
    def extraName(self):
        pass

    
    def _readConfig(self, xmlCtx, scriptSection):
        pass

    
    def _OptionalDevice__readBasicConfig(self, xmlCtx, section):
        self.itemTypeName = 'optionalDevice'
        self.name = section.name
        self.id = (nations.NONE_INDEX, _xml.readInt(xmlCtx, section, 'id', 0, 65535))
        self.compactDescr = vehicles.makeIntCompactDescrByID('optionalDevice', *self.id)
        if IS_CLIENT or IS_WEB:
            self.userString = i18n.makeString(section.readString('userString'))
            self.description = i18n.makeString(section.readString('description'))
            self.icon = _xml.readIcon(xmlCtx, section, 'icon')
        
        price = _xml.readPrice(xmlCtx, section, 'price')
        if IS_BASEAPP or IS_WEB:
            self.price = price
            self.showInShop = not section.readBool('notInShop', False)
        
        if IS_CELLAPP or not section.has_key('vehicleFilter'):
            self._OptionalDevice__filter = None
        else:
            self._OptionalDevice__filter = _VehicleFilter((xmlCtx, 'vehicleFilter'), section['vehicleFilter'])
        self.removable = section.readBool('removable', False)



class StaticFactorDevice(OptionalDevice):
    
    def updateVehicleDescrAttrs(self, vehicleDescr):
        if len(self._StaticFactorDevice__attr) == 1:
            attrDict = vehicleDescr.__dict__
            attrName = self._StaticFactorDevice__attr[0]
        else:
            attrDict = getattr(vehicleDescr, self._StaticFactorDevice__attr[0])
            attrName = self._StaticFactorDevice__attr[1]
        val = attrDict[attrName]
        if type(val) is IntType:
            attrDict[attrName] = int(val * self._StaticFactorDevice__factor)
        else:
            attrDict[attrName] = val * self._StaticFactorDevice__factor

    
    def _readConfig(self, xmlCtx, section):
        self._StaticFactorDevice__factor = _xml.readPositiveFloat(xmlCtx, section, 'factor')
        self._StaticFactorDevice__attr = _xml.readNonEmptyString(xmlCtx, section, 'attribute').split('/', 1)



class StaticAdditiveDevice(OptionalDevice):
    
    def updateVehicleDescrAttrs(self, vehicleDescr):
        if len(self._StaticAdditiveDevice__attr) == 1:
            attrDict = vehicleDescr.__dict__
            attrName = self._StaticAdditiveDevice__attr[0]
        else:
            attrDict = getattr(vehicleDescr, self._StaticAdditiveDevice__attr[0])
            attrName = self._StaticAdditiveDevice__attr[1]
        val = attrDict[attrName]
        if type(val) is IntType:
            attrDict[attrName] = int(val + self._StaticAdditiveDevice__value)
        else:
            attrDict[attrName] = val + self._StaticAdditiveDevice__value

    
    def _readConfig(self, xmlCtx, section):
        self._StaticAdditiveDevice__value = _xml.readFloat(xmlCtx, section, 'value')
        self._StaticAdditiveDevice__attr = _xml.readNonEmptyString(xmlCtx, section, 'attribute').split('/', 1)



class StillVehicleFactorDevice(OptionalDevice):
    
    def extraName(self):
        return self.name

    
    def _readConfig(self, xmlCtx, section):
        self.activateWhenStillSec = _xml.readNonNegativeFloat(xmlCtx, section, 'activateWhenStillSec')
        self.attributeName = _xml.readNonEmptyString(xmlCtx, section, 'attribute')
        self.factor = _xml.readPositiveFloat(xmlCtx, section, 'factor')



class EnhancedSuspension(OptionalDevice):
    
    def weightOnVehicle(self, vehicleDescr):
        chassis = vehicleDescr.chassis
        return (self._vehWeightFraction, self._weight, chassis['maxLoad'] * (self._EnhancedSuspension__chassisMaxLoadFactor - 1))

    
    def _readConfig(self, xmlCtx, section):
        self._EnhancedSuspension__chassisMaxLoadFactor = _xml.readPositiveFloat(xmlCtx, section, 'chassisMaxLoadFactor')
        self._EnhancedSuspension__chassisHealthFactor = _xml.readPositiveFloat(xmlCtx, section, 'chassisHealthFactor')

    
    def updateVehicleDescrAttrs(self, vehicleDescr):
        vehicleDescr.miscAttrs['chassisHealthFactor'] *= self._EnhancedSuspension__chassisHealthFactor



class Grousers(OptionalDevice):
    if not IS_CLIENT or IS_DEVELOPMENT:
        
        def updateVehicleDescrAttrs(self, vehicleDescr):
            r = vehicleDescr.physics['terrainResistance']
            vehicleDescr.physics['terrainResistance'] = (r[0], r[1] * self._Grousers__factorMedium, r[2] * self._Grousers__factorSoft)

    else:
        
        def updateVehicleDescrAttrs(self, vehicleDescr):
            pass

    
    def _readConfig(self, xmlCtx, section):
        self._Grousers__factorSoft = _xml.readPositiveFloat(xmlCtx, section, 'softGroundResistanceFactor')
        self._Grousers__factorMedium = _xml.readPositiveFloat(xmlCtx, section, 'mediumGroundResistanceFactor')



class Equipment(object):
    
    def get(self, key, defVal = None):
        return self.__dict__.get(key, defVal)

    
    def __getitem__(self, key):
        return self.__dict__[key]

    
    def init(self, xmlCtx, section):
        self._Equipment__readBasicConfig(xmlCtx, section)
        self._readConfig((xmlCtx, 'script'), section['script'])

    
    def checkCompatibilityWithVehicle(self, vehicleDescr):
        if self._Equipment__vehicleFilter is None:
            return (True, None)
        return self._Equipment__vehicleFilter.checkCompatibility(vehicleDescr)

    
    def checkCompatibilityWithEquipment(self, other):
        if self is other:
            return False
        filter = self._Equipment__equipmentFilter
        if filter is None:
            return True
        return not filter.inInstalled(other.tags)

    
    def checkCompatibilityWithActiveEquipment(self, other):
        if self is other:
            return False
        filter = self._Equipment__equipmentFilter
        if filter is None:
            return True
        return not filter.inActive(other.tags)

    
    def updatePrice(self, newPrice, showInShop):
        self.price = newPrice
        self.showInShop = showInShop

    
    def extraName(self):
        return self.name

    
    def _readConfig(self, xmlCtx, scriptSection):
        pass

    
    def _Equipment__readBasicConfig(self, xmlCtx, section):
        self.itemTypeName = 'equipment'
        self.name = section.name
        self.id = (nations.NONE_INDEX, _xml.readInt(xmlCtx, section, 'id', 0, 65535))
        self.compactDescr = vehicles.makeIntCompactDescrByID('equipment', *self.id)
        if not section.has_key('tags'):
            self.tags = frozenset()
        else:
            self.tags = _readTags(xmlCtx, section, 'tags', 'equipment')
        if IS_CLIENT or IS_WEB:
            self.userString = i18n.makeString(section.readString('userString'))
            self.description = i18n.makeString(section.readString('description'))
            self.icon = _xml.readIcon(xmlCtx, section, 'icon')
        
        price = _xml.readPrice(xmlCtx, section, 'price')
        if IS_BASEAPP or IS_WEB:
            self.price = price
            self.showInShop = not section.readBool('notInShop', False)
        
        if IS_CELLAPP or not section.has_key('vehicleFilter'):
            self._Equipment__vehicleFilter = None
        else:
            self._Equipment__vehicleFilter = _VehicleFilter((xmlCtx, 'vehicleFilter'), section['vehicleFilter'])
        if not section.has_key('incompatibleTags'):
            self._Equipment__equipmentFilter = None
        else:
            self._Equipment__equipmentFilter = _EquipmentFilter((xmlCtx, 'incompatibleTags'), section['incompatibleTags'])



class Extinguisher(Equipment):
    
    def _readConfig(self, xmlCtx, section):
        if not section.has_key('fireStartingChanceFactor'):
            self.fireStartingChanceFactor = 1
        else:
            self.fireStartingChanceFactor = _xml.readPositiveFloat(xmlCtx, section, 'fireStartingChanceFactor')
        self.autoactivate = section.readBool('autoactivate', False)



class Fuel(Equipment):
    
    def _readConfig(self, xmlCtx, section):
        self.enginePowerFactor = _xml.readPositiveFloat(xmlCtx, section, 'enginePowerFactor')
        self.turretRotationSpeedFactor = _xml.readPositiveFloat(xmlCtx, section, 'turretRotationSpeedFactor')



class Stimulator(Equipment):
    
    def _readConfig(self, xmlCtx, section):
        self.crewLevelIncrease = _xml.readInt(xmlCtx, section, 'crewLevelIncrease', 1)



class Repairkit(Equipment):
    
    def _readConfig(self, xmlCtx, section):
        self.repairAll = section.readBool('repairAll', False)
        self.bonusValue = _xml.readFraction(xmlCtx, section, 'bonusValue')



class RemovedRpmLimiter(Equipment):
    
    def _readConfig(self, xmlCtx, section):
        self.enginePowerFactor = _xml.readPositiveFloat(xmlCtx, section, 'enginePowerFactor')
        self.engineHpLossPerSecond = _xml.readPositiveFloat(xmlCtx, section, 'engineHpLossPerSecond')



class Afterburning(Equipment):
    
    def _readConfig(self, xmlCtx, section):
        self.enginePowerFactor = _xml.readPositiveFloat(xmlCtx, section, 'enginePowerFactor')
        self.durationSeconds = _xml.readInt(xmlCtx, section, 'durationSeconds', 1)



class _VehicleFilter(object):
    
    def __init__(self, xmlCtx, section):
        self._VehicleFilter__include = []
        self._VehicleFilter__exclude = []
        for subsection in section.values():
            if subsection.name == 'include':
                self._VehicleFilter__include.append(_readVehicleFilterPattern((xmlCtx, 'include'), subsection))
                continue
            if subsection.name == 'exclude':
                self._VehicleFilter__exclude.append(_readVehicleFilterPattern((xmlCtx, 'exclude'), subsection))
                continue
            _xml.raiseWrongXml(xmlCtx, subsection.name, 'should be <include> or <exclude>')
        

    
    def checkCompatibility(self, vehicleDescr):
        if self._VehicleFilter__exclude:
            (isVehicleTypeMatched, isVehicleMatched) = _matchSubfilter(vehicleDescr, self._VehicleFilter__exclude)
            if isVehicleMatched:
                return (False, 'not for current vehicle')
            if isVehicleTypeMatched:
                return (False, 'not for this vehicle type')
        
        if self._VehicleFilter__include:
            (isVehicleTypeMatched, isVehicleMatched) = _matchSubfilter(vehicleDescr, self._VehicleFilter__include)
            if not isVehicleMatched:
                if not isVehicleTypeMatched:
                    return (False, 'not for this vehicle type')
                return (False, 'not for current vehicle')
        
        return (True, None)



class _EquipmentFilter(object):
    
    def __init__(self, xmlCtx, section):
        self._EquipmentFilter__installed = set()
        self._EquipmentFilter__active = set()
        for subsection in section.values():
            if subsection.name == 'installed':
                self._EquipmentFilter__installed.update(_readTags((xmlCtx, subsection.name), subsection, '', 'equipment'))
                continue
            if subsection.name == 'active':
                self._EquipmentFilter__active.update(_readTags((xmlCtx, subsection.name), subsection, '', 'equipment'))
                continue
            _xml.raiseWrongXml(xmlCtx, subsection.name, 'should be <installed> or <active>')
        

    
    def inInstalled(self, tags):
        return len(self._EquipmentFilter__installed.intersection(tags))

    
    def inActive(self, tags):
        return len(self._EquipmentFilter__active.intersection(tags))



def _readVehicleFilterPattern(xmlCtx, section):
    res = { }
    for (sname, section) in section.items():
        ctx = (xmlCtx, sname)
        if sname == 'nations':
            names = section.asString
            res['nations'] = []
            for name in names.split():
                id = nations.INDICES.get(name)
                if id is None:
                    _xml.raiseWrongXml(xmlCtx, 'nations', "unknown nation '%s'" % name)
                
                res['nations'].append(id)
            
        if sname in _vehicleFilterItemTypes:
            sname = intern(sname)
            res[sname] = { }
            if section.has_key('tags'):
                tags = _readTags(ctx, section, 'tags', _vehicleFilterItemTypes[sname])
                res[sname]['tags'] = tags
            
            minLevel = section.readInt('minLevel', 1)
            if 1 <= minLevel:
                pass
            minLevel <= 10
            if not 1:
                _xml.raiseWrongSection(ctx, 'minLevel')
            
            if minLevel != 1:
                res[sname]['minLevel'] = minLevel
            
            maxLevel = section.readInt('maxLevel', 10)
            if 1 <= maxLevel:
                pass
            maxLevel <= 10
            if not 1:
                _xml.raiseWrongSection(ctx, 'maxLevel')
            
            if maxLevel != 10:
                res[sname]['maxLevel'] = maxLevel
            
        maxLevel != 10
        _xml.raiseWrongXml(ctx, '', 'unknown section name')
    
    return res


def _matchSubfilter(vehicleDescr, subfilter):
    vehicleType = vehicleDescr.type
    nationID = vehicleType.id[0]
    hasVehicleTypeOk = False
    for entry in subfilter:
        item = entry.get('nations')
        if item is not None and nationID not in item:
            continue
        
        item = entry.get('vehicle')
        if item is None:
            hasVehicleTypeOk = True
        else:
            tags = item.get('tags')
            if tags is not None and not vehicleType.tags.intersection(tags):
                continue
            
            minLevel = item.get('minLevel')
            if minLevel is not None and minLevel > vehicleDescr.level:
                continue
            
            maxLevel = item.get('maxLevel')
            if maxLevel is not None and maxLevel < vehicleDescr.level:
                continue
            
            hasVehicleTypeOk = True
        isVehicleOk = True
        for (name, item) in entry.iteritems():
            if name in ('nations', 'vehicle'):
                continue
            
            descr = getattr(vehicleDescr, name)
            tags = item.get('tags')
            if tags is not None and not descr['tags'].intersection(tags):
                isVehicleOk = False
                break
            
            minLevel = item.get('minLevel')
            if minLevel is not None and minLevel > descr['level']:
                isVehicleOk = False
                break
            
            maxLevel = item.get('maxLevel')
            if maxLevel is not None and maxLevel < descr['level']:
                isVehicleOk = False
                break
                continue
        
        if isVehicleOk:
            return (True, True)
    
    return (hasVehicleTypeOk, False)

_vehicleFilterItemTypes = {
    'vehicle': 'vehicle',
    'chassis': 'vehicleChassis',
    'engine': 'vehicleEngine',
    'fuelTank': 'vehicleFuelTank',
    'radio': 'vehicleRadio' }

def _readWeight(xmlCtx, section):
    fraction = 0
    if section.has_key('vehicleWeightFraction'):
        fraction = _xml.readNonNegativeFloat(xmlCtx, section, 'vehicleWeightFraction')
    
    weight = 0
    if section.has_key('weight'):
        weight = _xml.readNonNegativeFloat(xmlCtx, section, 'weight')
    
    return (fraction, weight)

_readTags = vehicles._readTags

