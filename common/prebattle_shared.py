# Source Generated with Decompyle++
# File: prebattle_shared.pyc (Python 2.6)

import items
from account_shared import AmmoIterator
from constants import PREBATTLE_ACCOUNT_STATE, VEHICLE_CLASSES
from items import vehicles
_VEHICLE = items.ITEM_TYPE_INDICES['vehicle']
_CHASSIS = items.ITEM_TYPE_INDICES['vehicleChassis']
_TURRET = items.ITEM_TYPE_INDICES['vehicleTurret']
_GUN = items.ITEM_TYPE_INDICES['vehicleGun']
_ENGINE = items.ITEM_TYPE_INDICES['vehicleEngine']
_FUEL_TANK = items.ITEM_TYPE_INDICES['vehicleFuelTank']
_RADIO = items.ITEM_TYPE_INDICES['vehicleRadio']
_TANKMAN = items.ITEM_TYPE_INDICES['tankman']
_OPTIONALDEVICE = items.ITEM_TYPE_INDICES['optionalDevice']
_SHELL = items.ITEM_TYPE_INDICES['shell']
_EQUIPMENT = items.ITEM_TYPE_INDICES['equipment']

def trimLocalizedData(localized_data, languages, key = None):
    if key:
        pass
    1
    d = localized_data
    if d is None:
        return localized_data
    continue
    d = [](_[1])
    if not d:
        return localized_data
    if key:
        localized_data[key] = d
        return localized_data
    return d


def isVehicleValid(vehDescr, vehAmmo, settings):
    s = settings
    (minLevel, maxLevel) = s.get('limit_level', (0, 65535))
    limit_class_level = s.get('limit_class_level', { })
    for classTag in VEHICLE_CLASSES:
        if classTag not in vehDescr.type.tags:
            continue
        
        if classTag in limit_class_level:
            (classMinLevel, classMaxLevel) = limit_class_level[classTag]
            if classMinLevel <= vehDescr.level:
                pass
            vehDescr.level <= classMaxLevel
            if not 1:
                return (False, 'wrong_class_level')
            continue
        1
        if minLevel <= vehDescr.level:
            pass
        vehDescr.level <= maxLevel
        if not 1:
            return (False, 'wrong_level')
    
    vehTypeCompDescr = vehDescr.type.compactDescr
    limit_vehicles = s.get('limit_vehicles', None)
    if limit_vehicles is not None and vehTypeCompDescr not in limit_vehicles:
        return (False, 'limit_vehicles')
    limit_components = s.get('limit_components', { }).get(vehTypeCompDescr, None)
    if limit_components is not None:
        (isValid, components) = limit_components
        for compDescr in _collectCurrentReplaceableVehicleComponents(vehDescr):
            if isValid and compDescr not in components:
                return (False, 'limit_components')
            if not isValid and compDescr in components:
                return (False, 'limit_components')
        
    
    limit_ammo = s.get('limit_ammo', None)
    if limit_ammo is not None:
        (isValid, ammoSet) = limit_ammo
        for (compDescr, count) in AmmoIterator(vehAmmo):
            if compDescr == 0 or count == 0:
                continue
            
            if isValid and compDescr not in ammoSet:
                return (False, 'limit_ammo')
            if not isValid and compDescr in ammoSet:
                return (False, 'limit_ammo')
        
    
    limit_shells = s.get('limit_shells', { })
    if limit_shells:
        for (compDescr, count) in AmmoIterator(vehAmmo):
            if compDescr == 0 or count == 0:
                continue
            
            itemTypeIdx = vehicles.parseIntCompactDescr(compDescr)[0]
            if itemTypeIdx != _SHELL:
                continue
            
            if count > limit_shells.get(compDescr, 65535):
                return (False, 'limit_shells')
        
    
    return (True, None)


def isTeamValid(accountsInfo, team, settings):
    s = settings
    (minLevel, maxLevel) = s.get('limit_level', (0, 65535))
    count = 0
    totalLevel = 0
    vehs = { }
    for accInfo in accountsInfo.itervalues():
        if not accInfo['state'] & PREBATTLE_ACCOUNT_STATE.READY:
            continue
        
        if 'vehTypeCompDescr' not in accInfo or 'vehLevel' not in accInfo:
            vehDescr = vehicles.VehicleDescr(compactDescr = accInfo['vehCompDescr'])
            vehLevel = vehDescr.level
            vehTypeCompDescr = vehDescr.type.compactDescr
        else:
            vehLevel = accInfo['vehLevel']
            vehTypeCompDescr = accInfo['vehTypeCompDescr']
        if minLevel <= vehLevel:
            pass
        vehLevel <= maxLevel
        if not 1:
            return (False, 'limit_level')
        count += 1
        totalLevel += vehLevel
        vehs[vehTypeCompDescr] = vehs.get(vehTypeCompDescr, 0) + 1
    
    if count < s['limit_min_count'][team]:
        return (False, 'limit_min_count')
    (minTotalLevel, maxTotalLevel) = s.get('limit_total_level', (0, 65535))
    if minTotalLevel <= totalLevel:
        pass
    totalLevel <= maxTotalLevel
    if not 1:
        return (False, 'limit_total_level')
    limit_vehicles = s.get('limit_vehicles', None)
    if limit_vehicles is not None:
        for (minCount, maxCount) in limit_vehicles.iteritems():
            count = vehs.get(vehTypeCompDescr, 0)
            if minCount <= count:
                pass
            count <= maxCount
            if not 1:
                return (False, 'limit_vehicles')
        
    
    return (True, '')


def _collectCurrentReplaceableVehicleComponents(vehicleDescr):
    res = []
    vehicleType = vehicleDescr.type
    if len(vehicleType.chassis) > 1:
        res.append(vehicleDescr.chassis['compactDescr'])
    
    if len(vehicleType.engines) > 1:
        res.append(vehicleDescr.engine['compactDescr'])
    
    if len(vehicleType.radios) > 1:
        res.append(vehicleDescr.radio['compactDescr'])
    
    for (turretDescr, gunDescr) in enumerate(vehicleDescr.turrets):
        if len(vehicleType.turrets[posIdx]) > 1:
            res.append(turretDescr['compactDescr'])
        
        if len(turretDescr['guns']) > 1:
            res.append(gunDescr['compactDescr'])
            continue
    
    return res


