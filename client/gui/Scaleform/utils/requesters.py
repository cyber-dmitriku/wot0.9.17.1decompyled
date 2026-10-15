# Source Generated with Decompyle++
# File: requesters.pyc (Python 2.6)

import BigWorld
import nations
import constants
import AccountCommands
import time
import dossiers
from functools import partial
from adisp import async, process
from debug_utils import *
from gui_items import InventoryItem, ShopItem, InventoryVehicle, InventoryTankman, VehicleItem
from items import tankmen, vehicles, ITEM_TYPE_NAMES, ITEM_TYPE_INDICES
from Account import PlayerAccount
g_suitableModules = None
g_suitableVehicles = None
_ARTEFACTS_ITEMS = (ITEM_TYPE_INDICES['optionalDevice'], ITEM_TYPE_INDICES['equipment'])
_TANKMAN = ITEM_TYPE_INDICES['tankman']

def code2str(code):
    if code == AccountCommands.RES_SUCCESS:
        return 'Request succedded'
    if code == AccountCommands.RES_STREAM:
        return 'Stream is sent to the client'
    if code == AccountCommands.RES_CACHE:
        return 'Data is taken from cache'
    if code == AccountCommands.RES_FAILURE:
        return 'Unknown reason'
    if code == AccountCommands.RES_WRONG_ARGS:
        return 'Wrong arguments'
    if code == AccountCommands.RES_NON_PLAYER:
        return 'Account become non player'
    if code == AccountCommands.RES_SHOP_DESYNC:
        return 'Shop cache is desynchronized'
    if code == AccountCommands.RES_COOLDOWN:
        return 'Identical requests cooldown'
    if code == AccountCommands.RES_HIDDEN_DOSSIER:
        return 'Player dossier is hidden'
    if code == AccountCommands.RES_CENTER_DISCONNECTED:
        return 'Dossiers are unavailable'
    return 'Unknown error code'


class RequestProcessor(object):
    
    def __init__(self, delay, callback):
        self._RequestProcessor__callback = callback
        self._RequestProcessor__fired = False
        self._RequestProcessor__bwCallbackID = BigWorld.callback(delay, self._RequestProcessor__cooldownCallback)

    
    def isFired(self):
        return self._RequestProcessor__fired

    isFired = property(isFired)
    
    def cancel(self):
        if self._RequestProcessor__bwCallbackID is not None:
            BigWorld.cancelCallback(self._RequestProcessor__bwCallbackID)
            self._RequestProcessor__bwCallbackID = None
        

    
    def _RequestProcessor__cooldownCallback(self):
        self.cancel()
        self._RequestProcessor__fired = True
        self._RequestProcessor__callback()



class DossierRequester(object):
    _DossierRequester__queue = []
    _DossierRequester__lastResponseTime = 0
    _DossierRequester__request = None
    
    def __init__(self, userName):
        self.userName = userName
        self._DossierRequester__cache = {
            'account': None,
            'vehicles': { },
            'clan': None,
            'hidden': False,
            'available': True }

    
    def _DossierRequester__setLastResponseTime(self):
        DossierRequester._DossierRequester__lastResponseTime = time.time()

    
    def _DossierRequester__nextRequestTime(self):
        t = constants.REQUEST_COOLDOWN.PLAYER_DOSSIER - time.time() - DossierRequester._DossierRequester__lastResponseTime
        if t > 0:
            return t
        return 0

    
    def _DossierRequester__processQueue(self):
        if DossierRequester._DossierRequester__request is not None:
            return None
        if DossierRequester._DossierRequester__queue:
            DossierRequester._DossierRequester__request = RequestProcessor(self._DossierRequester__nextRequestTime(), DossierRequester._DossierRequester__queue.pop())
            return None

    
    def _DossierRequester__requestPlayerInfo(self, callback):
        
        def proxyCallback(value):
            if value is not None and len(value) > 1:
                self._DossierRequester__cache['account'] = dossiers.getAccountDossierDescr(value[0])
                self._DossierRequester__cache['clan'] = value[1]
            
            callback(self._DossierRequester__cache['account'])

        ((None, None), DossierRequester._DossierRequester__queue.append)((lambda : BigWorld.player().requestPlayerInfo(self.userName, (partial,)((lambda c, code, dossier, clanID, clanInfo: self._DossierRequester__processValueResponse(c, code, (dossier, (clanID, clanInfo)))), proxyCallback))
))
        self._DossierRequester__processQueue()

    
    def _DossierRequester__requestAccountDossier(self, callback):
        
        def proxyCallback(dossier):
            self._DossierRequester__cache['account'] = dossiers.getAccountDossierDescr(dossier)
            callback(self._DossierRequester__cache['account'])

        ((None, None), DossierRequester._DossierRequester__queue.append)((lambda : BigWorld.player().requestAccountDossier(self.userName, (partial,)((lambda c, code, dossier: self._DossierRequester__processValueResponse(c, code, dossier)), proxyCallback))
))
        self._DossierRequester__processQueue()

    
    def _DossierRequester__requestVehicleDossier(self, vehCompDescr, callback):
        
        def proxyCallback(dossier):
            self._DossierRequester__cache['vehicles'][vehCompDescr] = dossiers.getVehicleDossierDescr(dossier)
            callback(self._DossierRequester__cache['vehicles'][vehCompDescr])

        (None, (None, None, None), DossierRequester._DossierRequester__queue.append)((lambda : BigWorld.player().requestVehicleDossier(self.userName, vehCompDescr, (partial,)((lambda c, code, dossier: self._DossierRequester__processValueResponse(c, code, dossier)), proxyCallback))
))
        self._DossierRequester__processQueue()

    
    def _DossierRequester__requestClanInfo(self, callback):
        
        def proxyCallback(value):
            self._DossierRequester__cache['clan'] = value
            callback(self._DossierRequester__cache['clan'])

        ((None, None), DossierRequester._DossierRequester__queue.append)((lambda : BigWorld.player().requestPlayerClanInfo(self.userName, (partial,)((lambda c, code, str, clanDBID, clanInfo: self._DossierRequester__processValueResponse(c, code, (clanDBID, clanInfo))), callback))
))
        self._DossierRequester__processQueue()

    
    def _DossierRequester__processValueResponse(self, callback, code, value):
        self._DossierRequester__setLastResponseTime()
        DossierRequester._DossierRequester__request = None
        if code < 0:
            LOG_ERROR('Error while server request (code=%s): %s' % (code, code2str(code)))
            if code == AccountCommands.RES_HIDDEN_DOSSIER:
                self._DossierRequester__cache['hidden'] = True
            elif code == AccountCommands.RES_CENTER_DISCONNECTED:
                self._DossierRequester__cache['available'] = False
            
            callback('')
        else:
            callback(value)
        self._DossierRequester__processQueue()

    
    def getAccountDossier(self, callback):
        if not self.isValid:
            callback(None)
        
        if self._DossierRequester__cache.get('account') is None:
            if self._DossierRequester__cache.get('clan') is None:
                self._DossierRequester__requestPlayerInfo(callback)
            else:
                self._DossierRequester__requestAccountDossier(callback)
            return None
        callback(self._DossierRequester__cache['account'])

    getAccountDossier = async(getAccountDossier)
    
    def getClanInfo(self, callback):
        if not self.isValid:
            callback(None)
        
        if self._DossierRequester__cache.get('clan') is None:
            self._DossierRequester__requestClanInfo(callback)
            return None
        callback(self._DossierRequester__cache['clan'])

    getClanInfo = async(getClanInfo)
    
    def getVehicleDossier(self, vehCompDescr, callback):
        if not self.isValid:
            callback(None)
        
        if self._DossierRequester__cache.get('vehicles', { }).get(vehCompDescr, None) is None:
            self._DossierRequester__requestVehicleDossier(vehCompDescr, callback)
            return None
        callback(self._DossierRequester__cache['vehicles'][vehCompDescr])

    getVehicleDossier = async(getVehicleDossier)
    
    def isHidden(self):
        return self._DossierRequester__cache.get('hidden', False)

    isHidden = property(isHidden)
    
    def isAvailable(self):
        return self._DossierRequester__cache.get('available', False)

    isAvailable = property(isAvailable)
    
    def isValid(self):
        if not (self.isHidden):
            pass
        return self.isAvailable

    isValid = property(isValid)


class Parser(object):
    
    def parseVehicles(data):
        return data

    parseVehicles = staticmethod(parseVehicles)
    
    def parseModules(data, type):
        return data

    parseModules = staticmethod(parseModules)
    
    def getParser(itemTypeID):
        if itemTypeID == 1:
            return Parser.parseVehicles
        return (lambda data: Parser.parseModules(data, itemTypeID))

    getParser = staticmethod(getParser)


class InventoryParser(Parser):
    
    def parseVehicles(data):
        if data is None:
            return []
        vehicles = []
        for (id, vehCompDescr) in data.get('compDescr', { }).items():
            descriptor = vehCompDescr
            ammoLayout = dict(data['shellsLayout'].get(id, { }))
            shells = list(data['shells'].get(id, []))
            crew = list(data['crew'].get(id, []))
            (repairCost, health) = data['repair'].get(id, (0, 0))
            equipmentsLayout = data['eqsLayout'].get(id, [
                0,
                0,
                0])
            equipments = data['eqs'].get(id, [
                0,
                0,
                0])
            if not equipments:
                equipments = [
                    0,
                    0,
                    0]
            
            settings = data['settings'].get(id, 0)
            lock = data['lock'].get(id, 0)
            vehicles.append(InventoryVehicle(compactDescr = descriptor, id = id, crew = crew, shells = shells, ammoLayout = ammoLayout, repairCost = repairCost, health = health, lock = lock, equipments = equipments, equipmentsLayout = equipmentsLayout, settings = settings))
        
        return vehicles

    parseVehicles = staticmethod(parseVehicles)
    
    def parseTankmen(data):
        if data is None:
            return []
        tankmen = []
        for (id, compDescr) in data.get('compDescr', { }).items():
            descriptor = compDescr
            vehicleID = data['vehicle'].get(id, -1)
            tankmen.append(InventoryTankman(compactDescr = descriptor, id = id, vehicleID = vehicleID))
        
        return tankmen

    parseTankmen = staticmethod(parseTankmen)
    
    def parseModules(data, itemTypeID):
        if data is None:
            return []
        modules = []
        for (descriptor, count) in data.items():
            modules.append(InventoryItem(itemTypeName = ITEM_TYPE_NAMES[itemTypeID], compactDescr = descriptor, count = count))
        
        return modules

    parseModules = staticmethod(parseModules)
    
    def getParser(itemTypeID):
        if itemTypeID == 1:
            return InventoryParser.parseVehicles
        if itemTypeID == 8:
            return InventoryParser.parseTankmen
        return (lambda data: InventoryParser.parseModules(data, itemTypeID))

    getParser = staticmethod(getParser)


class ShopParser(Parser):
    
    def parseVehicles(data, nationId):
        if data is None or not len(data):
            return []
        vehicles = []
        for (compactDescr, price) in data[0].items():
            vehicles.append(ShopItem(itemTypeName = ITEM_TYPE_NAMES[1], compactDescr = compactDescr, priceOrder = price, nation = nationId, hidden = compactDescr in data[1]))
        
        return vehicles

    parseVehicles = staticmethod(parseVehicles)
    
    def parseModules(data, itemTypeID, nationId):
        if data is None or not len(data):
            return []
        modules = []
        for (compactDescr, price) in data[0].items():
            modules.append(ShopItem(itemTypeName = ITEM_TYPE_NAMES[itemTypeID], compactDescr = compactDescr, priceOrder = price, nation = nationId, hidden = compactDescr in data[1]))
        
        return modules

    parseModules = staticmethod(parseModules)
    
    def getParser(itemTypeID):
        if itemTypeID == 1:
            return ShopParser.parseVehicles
        return (lambda data, nationId: ShopParser.parseModules(data, itemTypeID, nationId))

    getParser = staticmethod(getParser)


class Requester(object):
    """
\tAsync requester of items @see: helpers.Scaleform.utils.items
\t@param itemTypeName: item type to request @see: items.ITEM_TYPE_NAMES

\tExample of usage:
\t#Dont forget annotate function @process
\t@process
\tdef updateGuns():
\t\t#make request to inventory
\t\tinventoryGuns = yield Requester('vehicleGun').getFromInventory()
\t\t#continue after request complete
\t\t#do somthing with guns list [InventoryItem, InventoryItem, ...]

\t\t#make request to shop
\t\tguns = yield Requester('vehicleGun').getFromShop()
\t\t#continue after request complete
\t\t#do somthing with guns list [ShopItem, ShopItem, ...]
\t"""
    PARSERS = {
        'inventory': InventoryParser,
        'shop': ShopParser }
    
    def __init__(self, itemTypeName):
        self._itemTypeId = ITEM_TYPE_INDICES[itemTypeName]
        self._callback = None
        self._requestsCount = 0
        self._responsesCount = 0
        self._response = []

    
    def getAllPossible(self, callback):
        """
\t\tMake request to inventory and shop
\t\treturn InventoryItems and ShopItems

\t\tExample of usage:
\t\t@process
\t\tdef updateGuns():
\t\t\tguns = yield Requester('vehicleGun').getAllPossible()
\t\t\t#continue after request complete
\t\t\t#do somthing with guns list [InventoryItem, InventoryItem, ShopItem, ...]
\t\t"""
        self._callback = callback
        self._requestsCount = count(nations.INDICES) + 1
        self._requestInventory()
        for nationId in nations.INDICES.values():
            self._requestShop(nationId)
        

    getAllPossible = async(getAllPossible)
    
    def getFromInventory(self, callback):
        """
\t\tMake request to inventory

\t\tExample of usage:
\t\t@process
\t\tdef updateGuns():
\t\t\tguns = yield Requester('vehicleGun').getFromInventory()
\t\t\t#continue after request complete
\t\t\t#do somthing with guns list [InventoryItem, InventoryItem, ...]
\t\t"""
        self._callback = callback
        self._requestsCount = 1
        self._requestInventory()

    getFromInventory = async(getFromInventory)
    
    def getFromShop(self, callback, nation = None):
        """
\t\tMake request to shop

\t\tExample of usage:
\t\t@process
\t\tdef updateGuns():
\t\t\tguns = yield Requester('vehicleGun').getFromShop()
\t\t\t#continue after request complete
\t\t\t#do somthing with guns list [ShopItem, ShopItem, ...]
\t\t"""
        self._callback = callback
        if self._itemTypeId in _ARTEFACTS_ITEMS:
            self._requestsCount = 1
            self._requestShop(nations.NONE_INDEX)
        elif nation is not None:
            self._requestsCount = 1
            self._requestShop(nation)
        else:
            self._requestsCount = len(nations.INDICES)
            for nationId in nations.INDICES.values():
                self._requestShop(nationId)
            

    getFromShop = async(getFromShop)
    
    def _requestInventory(self):
        if not hasattr(BigWorld.player(), 'inventory'):
            raise AssertionError, 'Request from inventory is not possible'
        BigWorld.player().inventory.getItems(self._itemTypeId, self._Requester__parseInventoryResponse)

    
    def _Requester__parseInventoryResponse(self, responseCode, data):
        listData = []
        if responseCode >= 0:
            listData = Requester.PARSERS['inventory'].getParser(self._itemTypeId)(data)
        else:
            LOG_ERROR('Server return error for inventory getItems request: responseCode=%s, itemTypeId=%s.' % (responseCode, self._itemTypeId))
        self._collectResponse(listData, 'inventory')

    
    def _requestShop(self, nationId):
        if not hasattr(BigWorld.player(), 'shop'):
            raise AssertionError, 'Request from shop is not possible'
        hasattr(BigWorld.player(), 'shop')(BigWorld.player().shop.getItems, (self._itemTypeId, nationId), (lambda responseCode, data, shopRev: self._Requester__parseShopResponse(responseCode, data, nationId)))

    
    def _Requester__parseShopResponse(self, responseCode, data, nationId):
        listData = []
        if responseCode >= 0:
            listData = Requester.PARSERS['shop'].getParser(self._itemTypeId)(data, nationId)
        else:
            LOG_ERROR('Server return error for shop getItems request: responseCode=%s, itemTypeId=%s, nationId=%s, data=%s.' % (responseCode, self._itemTypeId, nationId, data))
        self._collectResponse(listData, 'shop')

    
    def _collectResponse(self, response, requestType):
        self._responsesCount += 1
        self._response.extend(response)
        if self._responsesCount == self._requestsCount:
            if self._callback is not None:
                self._callback(self._response)
            
        



def getComponentsByType(vehDescr, itemTypeId, turretPID = 0):
    '''
\tReturn list suitable modules for vehicle foloving structure:
\t{
\t\tcompactDescriptor: (isCurrent, isDefault),
\t\t...
\t}
\t'''
    descriptorsList = []
    current = []
    if itemTypeId == vehicles._CHASSIS:
        current = [
            vehDescr.chassis['compactDescr']]
        descriptorsList = vehDescr.type.chassis
    elif itemTypeId == vehicles._ENGINE:
        current = [
            vehDescr.engine['compactDescr']]
        descriptorsList = vehDescr.type.engines
    elif itemTypeId == vehicles._RADIO:
        current = [
            vehDescr.radio['compactDescr']]
        descriptorsList = vehDescr.type.radios
    elif itemTypeId == vehicles._FUEL_TANK:
        current = [
            vehDescr.fuelTank['compactDescr']]
        descriptorsList = vehDescr.type.fuelTanks
    elif itemTypeId == vehicles._TURRET:
        current = [
            vehDescr.turret['compactDescr']]
        descriptorsList = vehDescr.type.turrets[turretPID]
    elif itemTypeId == vehicles._OPTIONALDEVICE:
        descriptorsList = vehDescr.optionalDevices
    elif itemTypeId == vehicles._GUN:
        current = [
            vehDescr.gun['compactDescr']]
        for gun in vehDescr.turret['guns']:
            descriptorsList.append(gun)
        
        for turret in vehDescr.type.turrets[turretPID]:
            if turret is not vehDescr.turret:
                for gun in turret['guns']:
                    descriptorsList.append(gun)
                
        
    elif itemTypeId == vehicles._SHELL:
        for shot in vehDescr.gun['shots']:
            current.append(shot['shell']['compactDescr'])
        
        for gun in vehDescr.turret['guns']:
            for shot in gun['shots']:
                descriptorsList.append(shot['shell'])
            
        
        for turret in vehDescr.type.turrets[turretPID]:
            if turret is not vehDescr.turret:
                for gun in turret['guns']:
                    for shot in gun['shots']:
                        descriptorsList.append(shot['shell'])
                    
                
        
    
    return (descriptorsList, current)


def _getComponentsByType(vehicle, itemTypeId, turretPID = 0):
    components = dict()
    (descriptorsList, current) = getComponentsByType(vehicle.descriptor, itemTypeId, turretPID)
    if itemTypeId == vehicles._EQUIPMENT:
        descriptorsList = vehicle.equipments
    
    if itemTypeId == vehicles._OPTIONALDEVICE:
        for (index, item) in enumerate(descriptorsList):
            if item:
                components[item['compactDescr']] = index
                continue
        
    elif itemTypeId == vehicles._EQUIPMENT:
        for (index, item) in enumerate(descriptorsList):
            if item:
                components[item] = index
                continue
        
    else:
        for item in descriptorsList:
            key = item['compactDescr']
            if not components.has_key(key):
                components[key] = item['compactDescr'] in current
                continue
        
    return components


class AvailableItemsRequester(Requester):
    
    def __init__(self, vehicle, itemTypeName):
        if not vehicle is not None:
            raise AssertionError
        Requester.__init__(self, itemTypeName)
        self._vehicle = vehicle

    
    def request(self, callback):
        self._callback = callback
        self._requestsCount = 2
        self._requestInventory()
        if self._itemTypeId in _ARTEFACTS_ITEMS:
            self._requestShop(nations.NONE_INDEX)
        else:
            (nationId, vehicleTypeId) = self._vehicle.descriptor.type.id
            self._requestShop(nationId)

    request = async(request)
    
    def _collectResponse(self, response, requestType):
        self._responsesCount += 1
        if requestType == 'shop':
            for item1 in response:
                isIn = False
                for item2 in self._response:
                    if item1 == item2:
                        item2.priceOrder = item1.priceOrder
                        isIn = True
                        break
                        continue
                
                if not isIn:
                    self._response.append(item1)
                    continue
            
        else:
            for item1 in response:
                for item2 in self._response:
                    if item1 == item2:
                        item1.priceOrder = item2.priceOrder
                        self._response.remove(item2)
                        break
                        continue
                
                self._response.append(item1)
            
        if self._responsesCount == self._requestsCount:
            values = []
            components = _getComponentsByType(self._vehicle, self._itemTypeId)
            descriptors = components.keys()
            for item in self._response:
                if self._itemTypeId not in _ARTEFACTS_ITEMS:
                    if item.compactDescr not in descriptors:
                        continue
                    
                elif not item.descriptor.checkCompatibilityWithVehicle(self._vehicle.descriptor)[0]:
                    continue
                
                isCurrentOrIndex = components.get(item.compactDescr, False)
                if isinstance(isCurrentOrIndex, bool):
                    pass
                1
                isCurrent = True
                if isCurrent and isinstance(item, ShopItem):
                    item = InventoryItem(itemTypeName = item.itemTypeName, compactDescr = item.compactDescr, priceOrder = item.priceOrder, count = 1)
                
                item.isCurrent = isCurrent
                if not isinstance(isCurrentOrIndex, bool):
                    item.index = isCurrentOrIndex
                
                values.append(item)
            
            if self._callback is not None:
                self._callback(values)
            
        



class CurrentVehicleRequester(object):
    
    def __init__(self):
        self._CurrentVehicleRequester__callback = None

    
    def get(self, callback):
        if not hasattr(BigWorld.player(), 'stats'):
            raise AssertionError, 'Request from stats is not possible'
        self._CurrentVehicleRequester__callback = callback
        BigWorld.player().stats.get('currentVehInvID', self._CurrentVehicleRequester__getResponse)

    get = async(get)
    
    def set(self, vehicleId, callback):
        if not hasattr(BigWorld.player(), 'stats'):
            raise AssertionError, 'Request from stats is not possible'
        self._CurrentVehicleRequester__callback = callback
        hasattr(BigWorld.player(), 'stats')((BigWorld.player().stats.setCurrentVehicle, vehicleId), (lambda code: self._CurrentVehicleRequester__setResponse(code, vehicleId)))

    set = async(set)
    
    def getMyVehicleInfo(self, vehicleId, callback):
        if not hasattr(BigWorld.player(), 'inventory'):
            raise AssertionError, 'Request from inventory is not possible'
        self._CurrentVehicleRequester__callback = callback
        hasattr(BigWorld.player(), 'inventory')((BigWorld.player().inventory.getVehicleInfo, vehicleId), (lambda code, data: self._CurrentVehicleRequester__parseVehicleResponse(code, data, vehicleId)))

    getMyVehicleInfo = async(getMyVehicleInfo)
    
    def _CurrentVehicleRequester__parseVehicleResponse(self, responseCode, data, id):
        vehicleData = None
        if responseCode >= 0:
            vehicleData = InventoryVehicle(data[0], id, (0, 0), data[1], data[2], data[4], data[5])
        else:
            LOG_ERROR('Server return error for inventory getVehicleInfo request: responseCode=%s, itemTypeId=%s.' % (responseCode, self._itemTypeId))
        if self._CurrentVehicleRequester__callback:
            self._CurrentVehicleRequester__callback(vehicleData)
        

    
    def _CurrentVehicleRequester__getResponse(self, responseCode, vehicleId):
        if responseCode < 0:
            LOG_ERROR('Server return error for statr get currentVehicleInvID request: responseCode=%s, vehicleId=%s.' % (responseCode, vehicleId))
        
        if self._CurrentVehicleRequester__callback:
            self._CurrentVehicleRequester__callback(vehicleId)
        

    
    def _CurrentVehicleRequester__setResponse(self, responseCode, vehicleId):
        if responseCode < 0:
            LOG_ERROR('Server return error for statr get currentVehicleInvID request: responseCode=%s, vehicleId=%s.' % (responseCode, vehicleId))
        
        if self._CurrentVehicleRequester__callback:
            self._CurrentVehicleRequester__callback(responseCode)
        



def responseIfNotAccount(*dargs, **dkwargs):
    
    def decorate(fn):
        
        def checkAccount(*fargs, **fkwargs):
            if not isinstance(BigWorld.player(), PlayerAccount):
                LOG_NOTE('Server call "StatsRequester.%s" canceled: player is not account.' % fn.func_name)
                returnFurnc = dkwargs.get('func', None)
                if returnFurnc:
                    returnArgs = dkwargs.get('args', None)
                    if returnArgs:
                        return fkwargs['callback'](returnFurnc(returnArgs))
                    return fkwargs['callback'](returnFurnc())
                return fkwargs['callback'](*dargs, **dargs)
            fargs[0].setCallback(fkwargs['callback'])
            return fn(*fargs, **fargs)

        return checkAccount

    return decorate


class StatsRequester(object):
    
    def __init__(self):
        self._StatsRequester__callback = None

    
    def setCallback(self, callback):
        self._StatsRequester__callback = callback

    
    def getMultipliedXPVehicles(self, callback):
        BigWorld.player().stats.get('multipliedXPVehs', self._StatsRequester__valueResponse)

    getMultipliedXPVehicles = async(responseIfNotAccount(set())(getMultipliedXPVehicles))
    
    def getAccountDossier(self, callback):
        BigWorld.player().stats.get('dossier', self._StatsRequester__accountDossierResponse)

    getAccountDossier = async(responseIfNotAccount(func = dossiers.getAccountDossierDescr, args = ('',))(getAccountDossier))
    
    def getVehicleDossier(self, vehTypeCompDescr, callback):
        BigWorld.player().dossierCache.get(constants.DOSSIER_TYPE.VEHICLE, vehTypeCompDescr, self._StatsRequester__vehicleDossierResponse)

    getVehicleDossier = async(responseIfNotAccount(func = dossiers.getVehicleDossierDescr, args = ('',))(getVehicleDossier))
    
    def getTankmanDossier(self, tankmanID, callback):
        BigWorld.player().inventory.getItems(_TANKMAN, partial(self._StatsRequester__tankmanDossierResponse, tankmanID))

    getTankmanDossier = async(responseIfNotAccount(func = dossiers.getTankmanDossierDescr, args = ('',))(getTankmanDossier))
    
    def getCredits(self, callback):
        BigWorld.player().stats.get('credits', self._StatsRequester__valueResponse)

    getCredits = async(responseIfNotAccount(0)(getCredits))
    
    def getFreeXPToTManXPRate(self, callback):
        BigWorld.player().shop.getFreeXPToTManXPRate(self._StatsRequester__valueResponse)

    getFreeXPToTManXPRate = async(responseIfNotAccount(1)(getFreeXPToTManXPRate))
    
    def freeXPToTankman(self, tankmanId, freeXp, callback):
        BigWorld.player().inventory.freeXPToTankman(tankmanId, (freeXp,), (lambda eStr, code: self._StatsRequester__callback((code >= 0, eStr))))

    freeXPToTankman = async(responseIfNotAccount(1)(freeXPToTankman))
    
    def isTeamKiller(self, callback):
        BigWorld.player().stats.get('tkillIsSuspected', self._StatsRequester__valueResponse)

    isTeamKiller = async(responseIfNotAccount(False)(isTeamKiller))
    
    def getRestrictions(self, callback):
        BigWorld.player().stats.get('restrictions', self._StatsRequester__valueResponse)

    getRestrictions = async(responseIfNotAccount(0)(getRestrictions))
    
    def getDenunciations(self, callback):
        BigWorld.player().stats.get('denunciationsLeft', self._StatsRequester__valueResponse)

    getDenunciations = async(responseIfNotAccount(0)(getDenunciations))
    
    def getGold(self, callback):
        BigWorld.player().stats.get('gold', self._StatsRequester__valueResponse)

    getGold = async(responseIfNotAccount(0)(getGold))
    
    def getVehicleTypeExperiences(self, callback):
        BigWorld.player().stats.get('vehTypeXP', self._StatsRequester__valueResponse)

    getVehicleTypeExperiences = async(responseIfNotAccount({ })(getVehicleTypeExperiences))
    
    def getFreeExperience(self, callback):
        BigWorld.player().stats.get('freeXP', self._StatsRequester__valueResponse)

    getFreeExperience = async(responseIfNotAccount(0)(getFreeExperience))
    
    def getVehicleTypeLocks(self, callback):
        BigWorld.player().stats.get('vehTypeLocks', self._StatsRequester__valueResponse)

    getVehicleTypeLocks = async(responseIfNotAccount({ })(getVehicleTypeLocks))
    
    def getGlobalVehicleLocks(self, callback):
        BigWorld.player().stats.get('globalVehicleLocks', self._StatsRequester__valueResponse)

    getGlobalVehicleLocks = async(responseIfNotAccount({ })(getGlobalVehicleLocks))
    
    def exchange(self, gold, callback):
        BigWorld.player().stats.exchange(gold, self._StatsRequester__response)

    exchange = async(responseIfNotAccount(False)(exchange))
    
    def getAmmoSellPrice(self, ammo, callback):
        BigWorld.player().shop.getAmmoSellPrice(ammo, self._StatsRequester__valueResponse)

    getAmmoSellPrice = async(responseIfNotAccount(0)(getAmmoSellPrice))
    
    def getDailyXPFactor(self, callback):
        BigWorld.player().shop.getDailyXPFactor(self._StatsRequester__valueResponse)

    getDailyXPFactor = async(responseIfNotAccount(1)(getDailyXPFactor))
    
    def convertVehiclesXP(self, xp, vehTypeDescrs, callback):
        BigWorld.player().stats.convertToFreeXP(vehTypeDescrs, xp, self._StatsRequester__response)

    convertVehiclesXP = async(responseIfNotAccount(False)(convertVehiclesXP))
    
    def getUnlocks(self, callback):
        BigWorld.player().stats.get('unlocks', self._StatsRequester__valueResponse)

    getUnlocks = async(responseIfNotAccount(set())(getUnlocks))
    
    def getEliteVehicles(self, callback):
        BigWorld.player().stats.get('eliteVehicles', self._StatsRequester__valueResponse)

    getEliteVehicles = async(responseIfNotAccount(set())(getEliteVehicles))
    
    def upgradeToPremium(self, days, callback):
        BigWorld.player().stats.upgradeToPremium(days, self._StatsRequester__response)

    upgradeToPremium = async(responseIfNotAccount(False)(upgradeToPremium))
    
    def buySlot(self, callback):
        BigWorld.player().stats.buySlot(self._StatsRequester__response)

    buySlot = async(responseIfNotAccount(False)(buySlot))
    
    def getSlotsCount(self, callback):
        BigWorld.player().stats.get('slots', self._StatsRequester__valueResponse)

    getSlotsCount = async(responseIfNotAccount(0)(getSlotsCount))
    
    def getTankmenBerthsCount(self, callback):
        BigWorld.player().stats.get('berths', self._StatsRequester__valueResponse)

    getTankmenBerthsCount = async(responseIfNotAccount(0)(getTankmenBerthsCount))
    
    def getSlotsPrices(self, callback):
        BigWorld.player().shop.getSlotsPrices(self._StatsRequester__valueResponse)

    getSlotsPrices = async(responseIfNotAccount([
        0,
        [
            0]])(getSlotsPrices))
    
    def getSteamGoldPackets(self, callback):
        BigWorld.player().shop.getGoldPackets(self._StatsRequester__valueResponse)

    getSteamGoldPackets = async(responseIfNotAccount(dict())(getSteamGoldPackets))
    
    def getPaidRemovalCost(self, callback):
        BigWorld.player().shop.getPaidRemovalCost(self._StatsRequester__valueResponse)

    getPaidRemovalCost = async(responseIfNotAccount(0)(getPaidRemovalCost))
    
    def getBerthsPrices(self, callback):
        BigWorld.player().shop.getBerthsPrices(self._StatsRequester__valueResponse)

    getBerthsPrices = async(responseIfNotAccount([
        0,
        1,
        [
            0]])(getBerthsPrices))
    
    def buyBerths(self, callback):
        BigWorld.player().stats.buyBerths(self._StatsRequester__response)

    buyBerths = async(responseIfNotAccount(False)(buyBerths))
    
    def getTankmanCost(self, callback):
        BigWorld.player().shop.getTankmanCost(self._StatsRequester__valueResponse)

    getTankmanCost = async(responseIfNotAccount(tuple())(getTankmanCost))
    
    def getDropSkillsCost(self, callback):
        BigWorld.player().shop.getDropSkillsCost(self._StatsRequester__valueResponse)

    getDropSkillsCost = async(responseIfNotAccount(tuple())(getDropSkillsCost))
    
    def getPassportChangeCost(self, callback):
        BigWorld.player().shop.getPassportChangeCost(self._StatsRequester__valueResponse)

    getPassportChangeCost = async(responseIfNotAccount(0)(getPassportChangeCost))
    
    def getShellPrice(self, nationIdx, shellCompactDescr, callback):
        BigWorld.player().shop.getPrice(ITEM_TYPE_INDICES['shell'], nationIdx, shellCompactDescr, self._StatsRequester__valueResponse)

    getShellPrice = async(responseIfNotAccount((0, 0))(getShellPrice))
    
    def getSellPriceModifiers(self, callback):
        BigWorld.player().shop.getSellPriceModifiers(self._StatsRequester__valueResponse)

    getSellPriceModifiers = async(responseIfNotAccount(False)(getSellPriceModifiers))
    
    def getExchangeRate(self, callback):
        BigWorld.player().shop.getExchangeRate(self._StatsRequester__valueResponse)

    getExchangeRate = async(responseIfNotAccount(1)(getExchangeRate))
    
    def getFreeXPConversion(self, callback):
        BigWorld.player().shop.getFreeXPConversion(self._StatsRequester__valueResponse)

    getFreeXPConversion = async(responseIfNotAccount(None)(getFreeXPConversion))
    
    def getPremiumCost(self, callback):
        BigWorld.player().shop.getPremiumCost(self._StatsRequester__valueResponse)

    getPremiumCost = async(responseIfNotAccount({ })(getPremiumCost))
    
    def getAccountAttrs(self, callback):
        BigWorld.player().stats.get('attrs', self._StatsRequester__valueResponse)

    getAccountAttrs = async(responseIfNotAccount(0)(getAccountAttrs))
    
    def getPremiumExpiryTime(self, callback):
        BigWorld.player().stats.get('premiumExpiryTime', self._StatsRequester__valueResponse)

    getPremiumExpiryTime = async(responseIfNotAccount(0)(getPremiumExpiryTime))
    
    def getClanInfo(self, callback):
        BigWorld.player().stats.get('clanInfo', self._StatsRequester__valueResponse)

    getClanInfo = async(responseIfNotAccount(None)(getClanInfo))
    
    def getClanDBID(self, callback):
        BigWorld.player().stats.get('clanDBID', self._StatsRequester__valueResponse)

    getClanDBID = async(responseIfNotAccount(None)(getClanDBID))
    
    def ebankGetBalance(self, callback):
        (BigWorld.player().ebankGetBalance,)((lambda code, errStr, props: self._StatsRequester__callback((props.get('vcoinBalance', 0), errStr))))

    ebankGetBalance = async(responseIfNotAccount((0, ''))(ebankGetBalance))
    
    def ebankBuyGold(self, vcoin, callback):
        BigWorld.player().ebankBuyGold((vcoin,), (lambda code, errStr, props: self._StatsRequester__callback((code >= 0, errStr))))

    ebankBuyGold = async(responseIfNotAccount((0, ''))(ebankBuyGold))
    
    def ebankGetExchangeRate(self, callback):
        BigWorld.player().shop.ebankVCoinExchangeRate(self._StatsRequester__valueResponse)

    ebankGetExchangeRate = async(responseIfNotAccount(1)(ebankGetExchangeRate))
    
    def setAndFillLayouts(self, vehInvID, shellsLayout, eqsLayout, callback):
        BigWorld.player().inventory.setAndFillLayouts(vehInvID, shellsLayout, (eqsLayout,), (lambda resID, errStr, value: self._StatsRequester__callback((resID, errStr, value))))

    setAndFillLayouts = async(responseIfNotAccount(dict())(setAndFillLayouts))
    
    def ebankGetMinTransactionValue(self, callback):
        BigWorld.player().shop.ebankMinTransactionValue(self._StatsRequester__valueResponse)

    ebankGetMinTransactionValue = async(responseIfNotAccount(50)(ebankGetMinTransactionValue))
    
    def ebankGetMaxTransactionValue(self, callback):
        BigWorld.player().shop.ebankMaxTransactionValue(self._StatsRequester__valueResponse)

    ebankGetMaxTransactionValue = async(responseIfNotAccount(500000)(ebankGetMaxTransactionValue))
    
    def getBattleResults(self, arenaUniqueID, callback):
        BigWorld.player().battleResultsCache.get(arenaUniqueID, self._StatsRequester__valueResponse)

    getBattleResults = async(responseIfNotAccount(dict())(getBattleResults))
    
    def getFileFromServer(self, clanId, fileType, callback):
        if not BigWorld.player().serverSettings['file_server'].has_key(fileType):
            LOG_ERROR("Invalid server's file type: %s" % fileType)
            self._StatsRequester__valueResponse(0, (None, None))
            return None
        clan_emblems = BigWorld.player().serverSettings['file_server'][fileType]
        BigWorld.player().customFilesCache.get((clan_emblems['url_template'] % clanId,), (lambda url, file: self._StatsRequester__valueResponse(0, (url, file))), True)

    getFileFromServer = async(responseIfNotAccount((None, None))(getFileFromServer))
    
    def getUserClanInfo(self, userName, callback):
        BigWorld.player().requestPlayerClanInfo((userName,), (lambda resultID, str, clanDBID, clanInfo: self._StatsRequester__valueResponse(resultID, (clanDBID, clanInfo))))

    getUserClanInfo = async(responseIfNotAccount(None)(getUserClanInfo))
    
    def hasFinPassword(self, callback):
        BigWorld.player().stats.get('hasFinPassword', self._StatsRequester__valueResponse)

    hasFinPassword = async(responseIfNotAccount(False)(hasFinPassword))
    
    def getVehiclesPrices(self, vehicles, callback):
        BigWorld.player().shop.getVehiclesSellPrices(vehicles, self._StatsRequester__valueResponse)

    getVehiclesPrices = async(responseIfNotAccount({ })(getVehiclesPrices))
    
    def getFreeVehicleLeft(self, callback):
        BigWorld.player().stats.get('freeVehiclesLeft', self._StatsRequester__valueResponse)

    getFreeVehicleLeft = async(responseIfNotAccount(None)(getFreeVehicleLeft))
    
    def getVehicleSellsLeft(self, callback):
        BigWorld.player().stats.get('vehicleSellsLeft', self._StatsRequester__valueResponse)

    getVehicleSellsLeft = async(responseIfNotAccount(None)(getVehicleSellsLeft))
    
    def getFreeTankmanLeft(self, callback):
        BigWorld.player().stats.get('freeTMenLeft', self._StatsRequester__valueResponse)

    getFreeTankmanLeft = async(responseIfNotAccount(None)(getFreeTankmanLeft))
    
    def setEquipments(self, vehInvId, equipments, callback):
        BigWorld.player().inventory.equipEquipments(vehInvId, equipments, self._StatsRequester__response)

    setEquipments = async(responseIfNotAccount(False)(setEquipments))
    
    def getTradeFees(self, callback):
        if not hasattr(BigWorld.player(), 'shop'):
            raise AssertionError, 'Request from shop is not possible'
        self._StatsRequester__callback = callback
        BigWorld.player().shop.getTradeFees(self._StatsRequester__valueResponse)

    getTradeFees = async(responseIfNotAccount({ })(getTradeFees))
    
    def _StatsRequester__accountDossierResponse(self, responseCode, dossierCompDescr = ''):
        if responseCode < 0:
            LOG_ERROR('Server return error for stat account dossier request: responseCode=%s' % responseCode)
            return None
        if self._StatsRequester__callback:
            import dossiers
            dossierDescr = dossiers.getAccountDossierDescr(dossierCompDescr)
            self._StatsRequester__callback(dossierDescr)
        

    
    def _StatsRequester__vehicleDossierResponse(self, responseCode, vehTypeDossiers = ''):
        if responseCode < 0:
            LOG_ERROR('Server return error for stat account dossier request: responseCode=%s' % responseCode)
            return None
        if self._StatsRequester__callback:
            import dossiers
            if vehTypeDossiers is not None:
                self._StatsRequester__callback(dossiers.getVehicleDossierDescr(vehTypeDossiers))
            
            self._StatsRequester__callback(dossiers.getVehicleDossierDescr(''))
        

    
    def _StatsRequester__tankmanDossierResponse(self, tankmanID, resultID, data):
        if resultID < 0:
            LOG_ERROR('Server return error for inventory tankman dossier request: responseCode=%s' % resultID)
            return None
        if self._StatsRequester__callback and data is not None:
            dossier = ''
            tankman = data.get('compDescr', None)
            if tankman is not None:
                tmenCompDescr = tankman.get(tankmanID, None)
                if tmenCompDescr is not None:
                    dossier = tankmen.TankmanDescr(tmenCompDescr).dossierCompactDescr
                
            
            self._StatsRequester__callback(dossiers.getTankmanDossierDescr(dossier))
        

    
    def _valueResponse(self, responseCode, value = None, revision = 0):
        if responseCode < 0:
            LOG_ERROR('Server return error for stat request: responseCode=%s' % responseCode)
            self._StatsRequester__dumpStack()
        elif self._StatsRequester__callback:
            self._StatsRequester__callback(value)
        

    
    def _StatsRequester__valueResponse(self, responseCode, value = None, revision = 0):
        if responseCode < 0:
            LOG_ERROR('Server return error for stat request: responseCode=%s' % responseCode)
            self._StatsRequester__dumpStack()
        
        if self._StatsRequester__callback:
            self._StatsRequester__callback(value)
        

    
    def _StatsRequester__response(self, responseCode):
        if responseCode < 0:
            LOG_ERROR('Server return error for stat request: responseCode=%s.' % responseCode)
            self._StatsRequester__dumpStack()
        
        if self._StatsRequester__callback:
            self._StatsRequester__callback(responseCode >= 0)
        

    
    def _StatsRequester__dumpStack(self):
        import inspect as inspect
        dump = 'frames stack dumping --------------'
        for (frame, file, line, method, _, _) in inspect.stack():
            dump = '%s\n (%s, %d): %s' % (dump, str(file), line, str(method))
        
        LOG_ERROR(dump)



class VehicleItemsRequester(object):
    
    def __init__(self, vehicles):
        self._VehicleItemsRequester__vehicles = vehicles

    
    def getItems(self, types):
        items = { }
        for v in self._VehicleItemsRequester__vehicles:
            for type in types:
                currents = self._VehicleItemsRequester__getItemsByType(v, type)
                for current in currents:
                    if current:
                        current = items.setdefault(current, VehicleItem(compactDescr = current))
                        current.count += 1
                        current.vehicles.append(v)
                        continue
                
            
        
        return items.values()

    
    def _VehicleItemsRequester__getItemsByType(self, v, itemTypeName):
        vd = v.descriptor
        if itemTypeName == 'vehicleChassis':
            return [
                vd.chassis['compactDescr']]
        if itemTypeName == 'vehicleEngine':
            return [
                vd.engine['compactDescr']]
        if itemTypeName == 'vehicleRadio':
            return [
                vd.radio['compactDescr']]
        if itemTypeName == 'vehicleFuelTank':
            return [
                vd.fuelTank['compactDescr']]
        if itemTypeName == 'vehicleTurret':
            if v.hasTurrets:
                return [
                    vd.turret['compactDescr']]
        
        if itemTypeName == 'vehicleGun':
            return [
                vd.gun['compactDescr']]
        if itemTypeName == 'optionalDevice':
            continue
            return _[1]
        if itemTypeName == 'equipment':
            return v.equipments
        return []



