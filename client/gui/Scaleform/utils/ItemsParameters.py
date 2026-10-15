# Source Generated with Decompyle++
# File: ItemsParameters.pyc (Python 2.6)

__author__ = 'i_maliavko'
import BigWorld
from gui.Scaleform.utils import ParametersCache
from debug_utils import *
from gui import GUI_SETTINGS
from items import ITEM_TYPE_INDICES, vehicles, getTypeInfoByIndex

class _ItemsParameters(object):
    
    def __init__(self):
        self._ItemsParameters__itemTypeHandlers = {
            vehicles._RADIO: self.getRadio,
            vehicles._ENGINE: self.getEngine,
            vehicles._CHASSIS: self.getChassis,
            vehicles._TURRET: self.getTurret,
            vehicles._VEHICLE: self.getVehicle,
            vehicles._EQUIPMENT: self.getEquipment,
            vehicles._OPTIONALDEVICE: self.getOptionalDevice,
            vehicles._GUN: self.getGun,
            vehicles._SHELL: self.getShell }
        self._ItemsParameters__itemCommonParamsList = {
            vehicles._RADIO: ('radioDistance', 'weight'),
            vehicles._CHASSIS: ('maxLoad', 'rotationSpeed', 'weight'),
            vehicles._ENGINE: ('enginePower', ('fireStartingChance', (lambda v: '%d%%' % v)), 'weight'),
            vehicles._TURRET: (('armor', (lambda v: '%d/%d/%d' % v)), ('rotationSpeed', (lambda v: BigWorld.wg_getIntegralFormat(v))), ('circularVisionRadius', (lambda v: BigWorld.wg_getIntegralFormat(v))), 'weight'),
            vehicles._VEHICLE: (('maxHealth', (lambda v: BigWorld.wg_getIntegralFormat(v))), ('weight', (lambda v: '%s/%s' % (BigWorld.wg_getNiceNumberFormat(v[0]), BigWorld.wg_getNiceNumberFormat(v[1])))), ('enginePower', (lambda v: BigWorld.wg_getIntegralFormat(v))), ('speedLimits', (lambda v: BigWorld.wg_getNiceNumberFormat(v))), ('chassisRotationSpeed', (lambda v: BigWorld.wg_getNiceNumberFormat(v))), ('hullArmor', (lambda v: '%d/%d/%d' % v)), ('turretArmor', (lambda v: '%d/%d/%d' % v)), ('damage', (lambda v: '%s-%s' % v)), ('piercingPower', (lambda v: '%s-%s' % v)), ('reloadTime', (lambda v: BigWorld.wg_getNiceNumberFormat(v))), ('turretRotationSpeed', (lambda v: BigWorld.wg_getIntegralFormat(v))), ('gunRotationSpeed', (lambda v: BigWorld.wg_getIntegralFormat(v))), ('circularVisionRadius', (lambda v: BigWorld.wg_getIntegralFormat(v))), ('radioDistance', (lambda v: BigWorld.wg_getIntegralFormat(v)))),
            vehicles._EQUIPMENT: tuple(),
            vehicles._OPTIONALDEVICE: ((('weight',), (lambda v: if v[1] > 0:
self._ItemsParameters__formatRange(*v))),),
            vehicles._GUN: ('caliber', (('reloadTime',), (lambda v: self._ItemsParameters__formatRange(*v))), ('avgPiercingPower', (lambda v: '/'.join(v))), ('avgDamage', (lambda v: '/'.join(v))), (('dispertionRadius',), (lambda v: self._ItemsParameters__formatRange(*v))), (('aimingTime',), (lambda v: self._ItemsParameters__formatRange(*v))), 'weight'),
            vehicles._SHELL: ('caliber', (('piercingPower',), (lambda v: self._ItemsParameters__formatRange(*v))), (('damage',), (lambda v: self._ItemsParameters__formatRange(*v))), ('explosionRadius', (lambda v: if v > 0:
'%.2f' % v))) }

    
    def _ItemsParameters__getCommonParameters(self, itemTypeName, paramsDict, excluded = tuple()):
        result = list()
        if GUI_SETTINGS.technicalInfo:
            for param in self._ItemsParameters__itemCommonParamsList.get(ITEM_TYPE_INDICES[itemTypeName], tuple()):
                if type(param) == str:
                    if param not in excluded:
                        result.append([
                            param,
                            paramsDict.get(param)])
                    
                param not in excluded
                paramName = param[0]
                paramValue = paramsDict.get(param[0])
                formatFunc = param[1]
                formattedValue = formatFunc(paramValue)
                if formattedValue is not None and paramName not in excluded:
                    result.append([
                        paramName,
                        formattedValue])
                    continue
            
        
        return result

    
    def _ItemsParameters__formatAsCurrent(self, item):
        return '<font color="#658c4c"><b>%s</b></font>' % item

    
    def _ItemsParameters__formatRange(self, minVal, maxVal):
        if minVal == maxVal:
            return BigWorld.wg_getNiceNumberFormat(minVal)
        
        def smartRound(value):
            if value > 99:
                return round(value)
            if value > 9:
                return round(value, 1)
            return round(value, 2)

        return '%s-%s' % (BigWorld.wg_getNiceNumberFormat(smartRound(minVal)), BigWorld.wg_getNiceNumberFormat(smartRound(maxVal)))

    
    def _ItemsParameters__getCompatibles(self, item, collection):
        continue
        return self._ItemsParameters__formatAsCurrent(c)([ c for c in collection ])

    
    def _ItemsParameters__getItemFullName(self, itemTypeIdx, itemDescr):
        return getTypeInfoByIndex(itemTypeIdx)['userString'] + ' ' + itemDescr['userString']

    
    def getParameters(self, item, vehicle = None):
        return self._ItemsParameters__get(item, vehicle, isCompatibles = False).get('parameters')

    
    def getCompatibles(self, item, vehicle = None):
        return self._ItemsParameters__get(item, vehicle, isParameters = False).get('compatible')

    
    def get(self, item, vehicle = None):
        return self._ItemsParameters__get(item, vehicle)

    
    def _ItemsParameters__get(self, item, vehicle = None, isParameters = True, isCompatibles = True):
        
        try:
            handler = self._ItemsParameters__itemTypeHandlers.get(ITEM_TYPE_INDICES[item.itemTypeName], (lambda : pass))
            return handler(item, vehicle, isParameters, isCompatibles)
        except Exception:
            LOG_CURRENT_EXCEPTION()
            return dict()


    
    def getRadio(self, item, vehicle = None, isParameters = True, isCompatibles = True):
        result = {
            'parameters': tuple(),
            'compatible': tuple() }
        if isParameters:
            result['parameters'] = self._ItemsParameters__getCommonParameters(item.itemTypeName, ParametersCache.g_instance.getRadioParameters(item, vehicle))
        
        if isCompatibles:
            curVehicle = None
            if vehicle and vehicle.descriptor.radio['id'][1] == item.descriptor['id'][1]:
                curVehicle = vehicle.name
            
            compatibles = ParametersCache.g_instance.getRadioCompatibles(item, vehicle)
            result['compatible'] = (('vehicles', self._ItemsParameters__getCompatibles(curVehicle, compatibles['vehicles'])),)
        
        return result

    
    def getChassis(self, item, vehicle = None, isParameters = True, isCompatibles = True):
        result = {
            'parameters': tuple(),
            'compatible': tuple() }
        if isParameters:
            result['parameters'] = self._ItemsParameters__getCommonParameters(item.itemTypeName, ParametersCache.g_instance.getChassisParameters(item, vehicle))
        
        if isCompatibles:
            curVehicle = None
            if vehicle and vehicle.descriptor.chassis['id'][1] == item.descriptor['id'][1]:
                curVehicle = vehicle.name
            
            compatibles = ParametersCache.g_instance.getChassisCompatibles(item, vehicle)
            result['compatible'] = (('vehicles', self._ItemsParameters__getCompatibles(curVehicle, compatibles['vehicles'])),)
        
        return result

    
    def getEngine(self, item, vehicle = None, isParameters = True, isCompatibles = True):
        result = {
            'parameters': tuple(),
            'compatible': tuple() }
        if isParameters:
            result['parameters'] = self._ItemsParameters__getCommonParameters(item.itemTypeName, ParametersCache.g_instance.getEngineParameters(item, vehicle))
        
        if isCompatibles:
            curVehicle = None
            if vehicle and vehicle.descriptor.engine['id'][1] == item.descriptor['id'][1]:
                curVehicle = vehicle.name
            
            compatibles = ParametersCache.g_instance.getEngineCompatibles(item, vehicle)
            result['compatible'] = (('vehicles', self._ItemsParameters__getCompatibles(curVehicle, compatibles['vehicles'])),)
        
        return result

    
    def getTurret(self, item, vehicle = None, isParameters = True, isCompatibles = True):
        result = {
            'parameters': tuple(),
            'compatible': tuple() }
        if isParameters:
            result['parameters'] = self._ItemsParameters__getCommonParameters(item.itemTypeName, ParametersCache.g_instance.getTurretParameters(item, vehicle))
        
        if isCompatibles:
            curVehicle = None
            curGun = None
            if vehicle and vehicle.descriptor.turret['id'][1] == item.descriptor['id'][1]:
                curGun = vehicle.descriptor.gun['userString']
                curVehicle = vehicle.name
            
            compatibles = ParametersCache.g_instance.getTurretCompatibles(item, vehicle)
            result['compatible'] = (('vehicles', self._ItemsParameters__getCompatibles(curVehicle, compatibles['vehicles'])), ('guns', self._ItemsParameters__getCompatibles(curGun, compatibles['guns'])))
        
        return result

    
    def getVehicle(self, vehicle, stubParameter = None, isParameters = True, isCompatibles = True):
        result = {
            'parameters': tuple(),
            'compatible': tuple(),
            'stats': list(),
            'base': list() }
        if isParameters:
            excluded = list()
            if not vehicle.hasTurrets:
                excluded.append('turretArmor')
            
            if vehicle.type != 'AT-SPG':
                excluded.append('gunRotationSpeed')
            else:
                excluded.append('turretRotationSpeed')
            result['parameters'] = self._ItemsParameters__getCommonParameters(vehicle.itemTypeName, ParametersCache.g_instance.getVehicleParameters(vehicle), excluded)
        
        if True:
            result['base'] = [
                self._ItemsParameters__getItemFullName(vehicles._GUN, vehicle.descriptor.gun),
                self._ItemsParameters__getItemFullName(vehicles._ENGINE, vehicle.descriptor.engine),
                self._ItemsParameters__getItemFullName(vehicles._CHASSIS, vehicle.descriptor.chassis),
                self._ItemsParameters__getItemFullName(vehicles._RADIO, vehicle.descriptor.radio)]
            if vehicle.hasTurrets:
                result['base'].insert(1, self._ItemsParameters__getItemFullName(vehicles._TURRET, vehicle.descriptor.turret))
            
        
        return result

    
    def getEquipment(self, item, vehicle = None, isParameters = True, isCompatibles = True):
        result = {
            'parameters': tuple(),
            'compatible': tuple() }
        if isParameters:
            result['parameters'] = self._ItemsParameters__getCommonParameters(item.itemTypeName, ParametersCache.g_instance.getEquipmentParameters(item, vehicle))
        
        if isCompatibles:
            pass
        1
        return result

    
    def getOptionalDevice(self, item, vehicle = None, isParameters = True, isCompatibles = True):
        result = {
            'parameters': tuple(),
            'compatible': tuple() }
        if isParameters:
            result['parameters'] = self._ItemsParameters__getCommonParameters(item.itemTypeName, ParametersCache.g_instance.getOptionalDeviceParameters(item, vehicle))
        
        if isCompatibles:
            pass
        1
        return result

    
    def getGun(self, item, vehicle = None, isParameters = True, isCompatibles = True):
        result = {
            'parameters': tuple(),
            'compatible': tuple() }
        if isParameters:
            result['parameters'] = self._ItemsParameters__getCommonParameters(item.itemTypeName, ParametersCache.g_instance.getGunParameters(item, vehicle))
        
        if isCompatibles:
            curVehicle = None
            curTurret = None
            if vehicle and vehicle.descriptor.gun['id'][1] == item.descriptor['id'][1]:
                curVehicle = vehicle.name
                curTurret = vehicle.descriptor.turret['userString']
            
            compatibles = ParametersCache.g_instance.getGunCompatibles(item, vehicle)
            result['compatible'] = [
                ('vehicles', self._ItemsParameters__getCompatibles(curVehicle, compatibles['vehicles'])),
                ('shells', ', '.join(compatibles['shells']))]
            if 'turrets' in result['compatible']:
                result['compatible'].insert(1, self._ItemsParameters__getCompatibles(curTurret, compatibles['turrets']))
            
        
        return result

    
    def getShell(self, item, vehicle = None, isParameters = True, isCompatibles = True):
        result = {
            'parameters': tuple(),
            'compatible': tuple() }
        if isParameters:
            result['parameters'] = self._ItemsParameters__getCommonParameters(item.itemTypeName, ParametersCache.g_instance.getShellParameters(item, vehicle))
        
        if isCompatibles:
            compatibles = ParametersCache.g_instance.getShellCompatibles(item, vehicle)
            result['compatible'] = (('shellGuns', ', '.join(compatibles['shellGuns'])),)
        
        return result


g_instance = _ItemsParameters()

