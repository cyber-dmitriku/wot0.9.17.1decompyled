# Source Generated with Decompyle++
# File: ParametersCache.pyc (Python 2.6)

__author__ = 'i_maliavko'
import BigWorld
import nations
import math
import sys
from debug_utils import *
from helpers import i18n
from items import ITEM_TYPE_INDICES, vehicles

class _ParametersCache(object):
    
    def __init__(self):
        self._ParametersCache__xmlItems = { }
        self._ParametersCache__cache = { }
        self._ParametersCache__init = False
        self._ParametersCache__precachHandlers = {
            vehicles._OPTIONALDEVICE: self._ParametersCache__precachOptionalDevices,
            vehicles._GUN: self._ParametersCache__precachGuns,
            vehicles._SHELL: self._ParametersCache__precachShells }
        self._ParametersCache__itemTypeHandlers = {
            vehicles._RADIO: self.getRadioParameters,
            vehicles._ENGINE: self.getEngineParameters,
            vehicles._CHASSIS: self.getChassisParameters,
            vehicles._TURRET: self.getTurretParameters,
            vehicles._VEHICLE: self.getVehicleParameters,
            vehicles._EQUIPMENT: self.getEquipmentParameters,
            vehicles._OPTIONALDEVICE: self.getOptionalDeviceParameters,
            vehicles._GUN: self.getGunParameters,
            vehicles._SHELL: self.getShellParameters }

    
    def initialized(self):
        return self._ParametersCache__init

    initialized = property(initialized)
    
    def _ParametersCache__readXMLItems(self):
        import items as items
        result = dict()
        for (_, idx) in nations.INDICES.iteritems():
            section = result.setdefault(idx, dict())
            section[items.vehicles._VEHICLE] = items.vehicles.g_list.getList(idx).keys()
            continue
            section[items.vehicles._RADIO] = [ data['compactDescr'] for data in items.vehicles.g_cache.radios(idx).values() ]
            continue
            section[items.vehicles._ENGINE] = [ data['compactDescr'] for data in items.vehicles.g_cache.engines(idx).values() ]
            continue
            section[items.vehicles._CHASSIS] = [ data['compactDescr'] for data in items.vehicles.g_cache.chassis(idx).values() ]
            continue
            section[items.vehicles._TURRET] = [ data['compactDescr'] for data in items.vehicles.g_cache.turrets(idx).values() ]
            continue
            section[items.vehicles._GUN] = [ data['compactDescr'] for data in items.vehicles.g_cache.guns(idx).values() ]
            continue
            section[items.vehicles._SHELL] = [ data['compactDescr'] for data in items.vehicles.g_cache.shells(idx).values() ]
        
        section = result.setdefault(nations.NONE_INDEX, dict())
        continue
        section[items.vehicles._EQUIPMENT] = [ data['compactDescr'] for data in items.vehicles.g_cache.equipments().values() ]
        continue
        section[items.vehicles._OPTIONALDEVICE] = [ data['compactDescr'] for data in items.vehicles.g_cache.optionalDevices().values() ]
        return result

    
    def _ParametersCache__getItemDescriptor(self, typeIdx, nationIdx, compactDescr):
        if typeIdx == vehicles._VEHICLE:
            return vehicles.VehicleDescr(typeID = (nationIdx, compactDescr))
        return vehicles.getDictDescr(compactDescr)

    
    def _ParametersCache__getItems(self, typeIdx, nationIdx = None):
        if nationIdx is None:
            result = list()
            for (_, idx) in nations.INDICES.iteritems():
                vDescrs = self._ParametersCache__getItems(typeIdx, idx)
                if vDescrs is not None:
                    result.extend(vDescrs)
                    continue
            
            return result
        items = self._ParametersCache__xmlItems.get(nationIdx, { }).get(typeIdx)
        if items is None:
            return list()
        continue
        return [ self._ParametersCache__getItemDescriptor(typeIdx, nationIdx, cd) for cd in items ]

    
    def _getShotsPerMinute(self, descriptor):
        return descriptor['burst'][0] * descriptor['clip'][0] * 60 / (descriptor['reloadTime'] + descriptor['burst'][0] * descriptor['burst'][1] + descriptor['clip'][0] * descriptor['clip'][1])

    
    def _ParametersCache__getParamFromCache(self, itemOrDescr, paramName, typeIdx = None, nationIdx = nations.NONE_INDEX, default = None):
        compactDescr = itemOrDescr
        itemTypeIdx = typeIdx
        itemNationIdx = nationIdx
        
        try:
            if not isinstance(itemOrDescr, int):
                compactDescr = itemOrDescr.compactDescr
                itemTypeIdx = ITEM_TYPE_INDICES[itemOrDescr.itemTypeName]
                itemNationIdx = itemOrDescr.nation
            
            cachedParams = self._ParametersCache__cache.get(itemNationIdx, { }).get(itemTypeIdx, { }).get(compactDescr, { })
            return cachedParams.get(paramName, default)
        except Exception:
            return default


    
    def _ParametersCache__precachOptionalDevices(self):
        self._ParametersCache__cache.setdefault(nations.NONE_INDEX, { })[vehicles._OPTIONALDEVICE] = { }
        optDevs = self._ParametersCache__getItems(vehicles._OPTIONALDEVICE, nations.NONE_INDEX)
        for deviceDescr in optDevs:
            wmin = sys.maxint
            wmax = -1
            for vDescr in self._ParametersCache__getItems(vehicles._VEHICLE):
                if not deviceDescr.checkCompatibilityWithVehicle(vDescr)[0]:
                    continue
                
                mods = deviceDescr.weightOnVehicle(vDescr)
                weightOnVehicle = math.ceil(vDescr.physics['weight'] * mods[0] + mods[1])
                wmin = min(wmin, weightOnVehicle)
                wmax = max(wmax, weightOnVehicle)
            
            self._ParametersCache__cache[nations.NONE_INDEX][vehicles._OPTIONALDEVICE][deviceDescr.compactDescr] = {
                'weight': (wmin, wmax) }
        

    
    def _ParametersCache__precachGuns(self):
        for (nationName, nationIdx) in nations.INDICES.iteritems():
            self._ParametersCache__cache.setdefault(nationIdx, { })[vehicles._GUN] = { }
            vcls = self._ParametersCache__getItems(vehicles._VEHICLE, nationIdx)
            guns = self._ParametersCache__getItems(vehicles._GUN, nationIdx)
            for g in guns:
                descriptors = list()
                self._ParametersCache__cache[nationIdx][vehicles._GUN][g['compactDescr']] = {
                    'turrets': list(),
                    'avgParams': dict() }
                for vDescr in vcls:
                    for vTurrets in vDescr.type.turrets:
                        for turret in vTurrets:
                            for gun in turret['guns']:
                                if gun['id'][1] == g['id'][1]:
                                    descriptors.append(gun)
                                    if len(vDescr.type.hull.get('fakeTurrets', { }).get('lobby', ())) != len(vDescr.type.turrets):
                                        self._ParametersCache__cache[nationIdx][vehicles._GUN][g['compactDescr']]['turrets'].append(turret['userString'])
                                    
                                len(vDescr.type.hull.get('fakeTurrets', { }).get('lobby', ())) != len(vDescr.type.turrets)
                            
                        
                    
                
                self._ParametersCache__cache[nationIdx][vehicles._GUN][g['compactDescr']]['avgParams'] = self._ParametersCache__calcGunParams(g, descriptors)
            
        

    
    def _ParametersCache__precachShells(self):
        for (nationName, nationIdx) in nations.INDICES.iteritems():
            self._ParametersCache__cache.setdefault(nationIdx, { })[vehicles._SHELL] = { }
            guns = self._ParametersCache__getItems(vehicles._GUN, nationIdx)
            shells = self._ParametersCache__getItems(vehicles._SHELL, nationIdx)
            for sDescr in shells:
                descriptors = list()
                gNames = list()
                self._ParametersCache__cache[nationIdx][vehicles._SHELL][sDescr['compactDescr']] = {
                    'guns': list(),
                    'avgParams': dict() }
                for gDescr in guns:
                    if 'shots' in gDescr:
                        for shot in gDescr['shots']:
                            if shot['shell']['id'][1] == sDescr['id'][1]:
                                if gDescr['userString'] not in gNames:
                                    gNames.append(gDescr['userString'])
                                    descriptors.append(shot)
                                
                            gDescr['userString'] not in gNames
                        
                
                self._ParametersCache__cache[nationIdx][vehicles._SHELL][sDescr['compactDescr']]['guns'] = gNames
                self._ParametersCache__cache[nationIdx][vehicles._SHELL][sDescr['compactDescr']]['avgParams'] = self._ParametersCache__calcShellParams(sDescr, descriptors)
            
        

    
    def _ParametersCache__getComponentVehiclesNames(self, item):
        ShopItem = ShopItem
        import gui.Scaleform.utils.gui_items
        _getComponentsByType = _getComponentsByType
        import gui.Scaleform.utils.requesters
        result = list()
        for vDescr in self._ParametersCache__getItems(vehicles._VEHICLE, item.nation):
            shopVehicle = ShopItem('vehicle', vDescr.type.id[1], vDescr.type.id[0])
            components = _getComponentsByType(shopVehicle, ITEM_TYPE_INDICES[item.itemTypeName])
            if item.compactDescr in components.keys():
                result.append(shopVehicle.name)
                continue
        
        return result

    
    def init(self):
        import time as time
        startTime = time.time()
        self._ParametersCache__init = False
        
        try:
            self._ParametersCache__xmlItems = self._ParametersCache__readXMLItems()
            for (itemTypeIdx, handler) in self._ParametersCache__precachHandlers.iteritems():
                handler()
        except Exception:
            LOG_CURRENT_EXCEPTION()
            return False

        elapsed = time.time() - startTime
        LOG_DEBUG("Parameters' cache initialization has been completed. Time elapsed: %.5fs" % elapsed)
        self._ParametersCache__init = True
        return True

    
    def _ParametersCache__calcGunParams(self, gunDescr, descriptors):
        result = {
            'reloadTime': (sys.maxint, -1),
            'dispRadius': (sys.maxint, -1),
            'aimingTime': (sys.maxint, -1),
            'piercingPower': list(),
            'damage': list(),
            'shells': list() }
        for d in descriptors:
            curReloadTime = self._getShotsPerMinute(d)
            curDispRadius = round(d['shotDispersionAngle'] * 100, 2)
            curAimingTime = round(d['aimingTime'], 1)
            result['reloadTime'] = (min(result['reloadTime'][0], curReloadTime), max(result['reloadTime'][1], curReloadTime))
            result['dispRadius'] = (min(result['dispRadius'][0], curDispRadius), max(result['dispRadius'][1], curDispRadius))
            result['aimingTime'] = (min(result['aimingTime'][0], curAimingTime), max(result['aimingTime'][1], curAimingTime))
        
        if 'shots' in gunDescr:
            for shot in gunDescr['shots']:
                result['piercingPower'].append('%d' % shot['piercingPower'][0])
                result['damage'].append('%d' % shot['shell']['damage'][0])
                result['shells'].append(i18n.makeString('#item_types:shell/kinds/' + shot['shell']['kind']))
            
        
        return result

    
    def _ParametersCache__calcShellParams(self, shellDescr, descriptors):
        result = {
            'piercingPower': (sys.maxint, -1),
            'damage': (sys.maxint, -1) }
        for d in descriptors:
            curPiercingPower = (round(d['piercingPower'][0] - d['piercingPower'][0] * d['shell']['piercingPowerRandomization']), round(d['piercingPower'][0] + d['piercingPower'][0] * d['shell']['piercingPowerRandomization']))
            curDamage = (round(d['shell']['damage'][0] - d['shell']['damage'][0] * d['shell']['damageRandomization']), round(d['shell']['damage'][0] + d['shell']['damage
