# Source Generated with Decompyle++
# File: Shop.pyc (Python 2.6)

import AccountCommands
import items
import nations
from functools import partial
from math import ceil
from itertools import izip
from items import vehicles, tankmen
from AccountCommands import BUY_VEHICLE_FLAG
from account_shared import AmmoIterator
from SyncController import SyncController
from PlayerEvents import g_playerEvents as events
from debug_utils import *
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

class Shop(object):
    
    def __init__(self):
        self._Shop__account = None
        self._Shop__syncController = None
        self._Shop__cache = { }
        self._Shop__ignore = True
        self._Shop__isSynchronizing = False
        self._Shop__syncID = 0
        self._Shop__isFirstSync = True

    
    def onAccountBecomePlayer(self):
        self._Shop__ignore = False
        self._Shop__isFirstSync = True
        self.synchronize()

    
    def onAccountBecomeNonPlayer(self):
        self._Shop__ignore = True
        self._Shop__isSynchronizing = False

    
    def setAccount(self, account):
        self._Shop__account = account
        if self._Shop__syncController is not None:
            self._Shop__syncController.destroy()
            self._Shop__syncController = None
        
        if account is not None:
            self._Shop__syncController = SyncController(account, self._Shop__sendSyncRequest, self._Shop__onSyncResponse, self._Shop__onSyncComplete)
        

    
    def synchronize(self, serverCacheRev = None):
        LOG_MX('Shop.synchronize: cli_rev=%s, serv_rev=%s' % (self._Shop__getCacheRevision(), serverCacheRev))
        if self._Shop__ignore:
            return None
        if self._Shop__getCacheRevision() == serverCacheRev:
            return None
        if self._Shop__isSynchronizing:
            return None
        self._Shop__isSynchronizing = True
        if not self._Shop__isFirstSync:
            events.onShopResyncStarted()
        
        self._Shop__syncController.request(self._Shop__getNextSyncID(), None)

    
    def resynchronize(self):
        LOG_MX('resynchronize')
        if self._Shop__ignore:
            return None
        self._Shop__cache.clear()
        self._Shop__isSynchronizing = True
        events.onShopResyncStarted()
        self._Shop__syncController.request(self._Shop__getNextSyncID(), None)

    
    def waitForSync(self, callback):
        if self._Shop__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, None)
            
            return None
        if not self._Shop__isSynchronizing:
            callback(AccountCommands.RES_CACHE, self._Shop__getCacheRevision())
            return None
        
        proxy = lambda resultID, data: callback(resultID, self._Shop__getCacheRevision())
        self._Shop__syncController.request(self._Shop__syncID, proxy)

    
    def getCache(self, callback):
        self._Shop__getValue(None, callback)

    
    def getItems(self, itemTypeIdx, nationIdx, callback):
        
        proxy = lambda resultID, items, rev: self._Shop__onGetItemsResponse(resultID, itemTypeIdx, nationIdx, callback)
        self._Shop__getValue('items', proxy)

    
    def getAllItems(self, callback):
        self._Shop__getValue('items', callback)

    
    def getSellPriceModifiers(self, callback):
        
        proxy = lambda resultID, data, rev: callback(resultID, self._Shop__getSellPriceModifiersFromCache())
        self._Shop__getValue('sellPriceModif', proxy)

    
    def getSellPrice(self, buyPrice, sellPriceModifiers):
        (shopRev, exchangeRate, sellPriceModif) = sellPriceModifiers
        if not shopRev == self._Shop__getCacheRevision():
            raise AssertionError
        return int(ceil(sellPriceModif * (buyPrice[0] + buyPrice[1] * exchangeRate)))

    
    def getPrice(self, itemTypeIdx, nationIdx, itemShopID, callback):
        
        proxy = lambda resultID, items, rev: self._Shop__onGetPriceResponse(resultID, itemTypeIdx, nationIdx, itemShopID, callback)
        self._Shop__getValue('items', proxy)

    
    def getVehiclePrice(self, vehCompDescr, callback):
        
        proxy = lambda resultID, items, rev: self._Shop__onGetVehiclePriceResponse(resultID, vehCompDescr, False, callback)
        self._Shop__getValue('items', proxy)

    
    def getVehicleSellPrice(self, vehCompDescr, callback):
        
        proxy = lambda resultID, items, rev: self._Shop__onGetVehiclePriceResponse(resultID, vehCompDescr, True, callback)
        self._Shop__getValue('items', proxy)

    
    def getVehiclesSellPrices(self, vehCompDescrs, callback):
        
        proxy = lambda resultID, items, rev: self._Shop__onGetVehiclesSellPriceResponse(resultID, vehCompDescrs, callback)
        self._Shop__getValue('items', proxy)

    
    def getComponentPrice(self, compDescr, callback):
        
        proxy = lambda resultID, items, rev: self._Shop__onGetComponentPriceResponse(resultID, compDescr, False, callback)
        self._Shop__getValue('items', proxy)

    
    def getComponentSellPrice(self, compDescr, callback):
        
        proxy = lambda resultID, items, rev: self._Shop__onGetComponentPriceResponse(resultID, compDescr, True, callback)
        self._Shop__getValue('items', proxy)

    
    def getAmmoSellPrice(self, ammo, callback):
        
        proxy = lambda resultID, items, rev: self._Shop__onGetAmmoSellPriceResponse(resultID, ammo, callback)
        self._Shop__getValue('items', proxy)

    
    def getDailyXPFactor(self, callback):
        self._Shop__getValue('dailyXPFactor', callback)

    
    def getSlotsPrices(self, callback):
        self._Shop__getValue('slotsPrices', callback)

    
    def getNextSlotPrice(self, slots, slotsPrices):
        addSlotNumber = slots - slotsPrices[0]
        if addSlotNumber < 0:
            return 0
        if addSlotNumber < len(slotsPrices[1]):
            return slotsPrices[1][addSlotNumber]
        return slotsPrices[1][-1]

    
    def getBerthsPrices(self, callback):
        self._Shop__getValue('berthsPrices', callback)

    
    def getNextBerthPackPrice(self, berths, berthsPrices):
        addPackNumber = (berths - berthsPrices[0]) / berthsPrices[1]
        if addPackNumber < 0:
            return 0
        if addPackNumber < len(berthsPrices[2]):
            return berthsPrices[2][addPackNumber]
        return berthsPrices[2][-1]

    
    def getExchangeRate(self, callback):
        self._Shop__getValue('exchangeRate', callback)

    
    def getFreeXPToTManXPRate(self, callback):
        self._Shop__getValue('freeXPToTManXPRate', callback)

    
    def ebankVCoinExchangeRate(self, callback):
        self._Shop__getValue('ebank/vcoinExchangeRate', callback)

    
    def ebankMinTransactionValue(self, callback):
        self._Shop__getValue('ebank/vcoinMinTransactionValue', callback)

    
    def ebankMaxTransactionValue(self, callback):
        self._Shop__getValue('ebank/vcoinMaxTransactionValue', callback)

    
    def getFreeXPConversion(self, callback):
        self._Shop__getValue('freeXPConversion', callback)

    
    def getPremiumCost(self, callback):
        self._Shop__getValue('premiumCost', callback)

    
    def getTradeFees(self, callback):
        self._Shop__getValue('tradeFees', callback)

    
    def getTankmanCost(self, callback):
        self._Shop__getValue('tankmanCost', callback)

    
    def getDropSkillsCost(self, callback):
        self._Shop__getValue('dropSkillsCost', callback)

    
    def getPassportChangeCost(self, callback):
        self._Shop__getValue('passportChangeCost', callback)

    
    def getPaidRemovalCost(self, callback):
        self._Shop__getValue('paidRemovalCost', callback)

    
    def getCamouflageCost(self, callback):
        self._Shop__getValue('camouflageCost', callback)

    
    def getPlayerEmblemCost(self, callback):
        self._Shop__getValue('playerEmblemCost', callback)

    
    def getPlayerInscriptionCost(self, callback):
        self._Shop__getValue('playerInscriptionCost', callback)

    
    def getHornCost(self, callback):
        self._Shop__getValue('hornCost', callback)

    
    def getGoldPackets(self, callback):
        return self._Shop__getValue('goldPackets', callback)

    
    def buy(self, itemTypeIdx, nationIdx, itemShopID, count, callback):
        if self._Shop__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, { })
            
            return None
        if itemTypeIdx == _VEHICLE:
            self.buyVehicle(nationIdx, itemShopID, False, True, 0, callback)
            return None
        count = int(round(count))
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Shop__account._doCmdInt3(AccountCommands.CMD_BUY_ITEM, self._Shop__getCacheRevision(), itemShopID, count, proxy)

    
    def buyAndEquipItem(self, vehInvID, compDescr, slotIdx, isPaidRemoval, gunCompDescr, callback):
        if self._Shop__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, '', { })
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID, errorStr, ext)
        else:
            proxy = None
        arr = [
            self._Shop__getCacheRevision(),
            compDescr,
            vehInvID,
            slotIdx,
            isPaidRemoval,
            gunCompDescr]
        self._Shop__account._doCmdIntArr(AccountCommands.CMD_BUY_AND_EQUIP_ITEM, arr, proxy)

    
    def buyVehicle(self, nationIdx, innationIdx, buyShells, recruitCrew, tmanCostTypeIdx, callback):
        if self._Shop__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, { })
            
            return None
        typeCompDescr = vehicles.makeIntCompactDescrByID('vehicle', nationIdx, innationIdx)
        flags = BUY_VEHICLE_FLAG.NONE
        if buyShells:
            flags |= BUY_VEHICLE_FLAG.SHELLS
        
        if recruitCrew:
            flags |= BUY_VEHICLE_FLAG.CREW
        
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Shop__account._doCmdInt4(AccountCommands.CMD_BUY_VEHICLE, self._Shop__getCacheRevision(), typeCompDescr, flags, tmanCostTypeIdx, proxy)

    
    def buyTankman(self, nationIdx, innationIdx, role, tmanCostTypeIdx, callback):
        vehTypeCompDescr = vehicles.makeIntCompactDescrByID('vehicle', nationIdx, innationIdx)
        roleIdx = tankmen.SKILL_INDICES[role]
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID, ext.get('tmanInvID', None), ext.get('tmanCompDescr', None))
        else:
            proxy = None
        self._Shop__account._doCmdInt4(AccountCommands.CMD_BUY_TMAN, self._Shop__getCacheRevision(), vehTypeCompDescr, roleIdx, tmanCostTypeIdx, proxy)

    
    def _Shop__onSyncResponse(self, syncID, resultID, ext = { }):
        if resultID == AccountCommands.RES_NON_PLAYER:
            return None
        if syncID != self._Shop__syncID:
            return None
        if resultID < 0:
            LOG_ERROR('Shop synchronization failed. Repeating')
            self.resynchronize()
            return None
        self._Shop__isSynchronizing = False

    
    def _Shop__onSyncComplete(self, syncID, data):
        if syncID != self._Shop__syncID:
            return None
        if data is None:
            return None
        for (nationIdx, nationShop) in data['items'].iteritems():
            if nationIdx == nations.NONE_INDEX:
                continue
            
            camouflages = vehicles.g_cache.customization(nationIdx).get('camouflages', None)
            if camouflages is None:
                continue
            
            vehList = vehicles.g_list.getList(nationIdx)
            vehPrices = nationShop[_VEHICLE][0]
            for (inNationIdx, price) in vehPrices.iteritems():
                vehInfo = vehList[inNationIdx]
                vehType = vehicles.getVehicleType(vehInfo['compactDescr'])
                if vehType.camouflagePriceFactor != price[2] or vehType.hornPriceFactor != price[3]:
                    vehType.camouflagePriceFactor = price[2]
                    vehType.hornPriceFactor = price[3]
                
                vehPrices[inNationIdx] = (price[0], price[1])
            
            for (id, priceFactor) in data['customization'][nationIdx]['camouflages'].iteritems():
                camouflage = camouflages[id]
                if camouflage['priceFactor'] != priceFactor:
                    LOG_DZ('Camouflage updated: id=%s, priceFactor:%s->%s' % (id, camouflage['priceFactor'], priceFactor))
                    camouflage['priceFactor'] = priceFactor
                    continue
                data is None
            
        
        self._Shop__cache = data
        self._Shop__isSynchronizing = False
        if self._Shop__isFirstSync:
            self._Shop__isFirstSync = False
        else:
            events.onShopResync()

    
    def _Shop__onGetItemsResponse(self, resultID, itemTypeIdx, nationIdx, callback):
        if resultID < 0:
            items = None
        else:
            items = self._Shop__cache.get('items', { }).get(nationIdx, { }).get(itemTypeIdx, None)
        if callback is not None:
            callback(resultID, items, self._Shop__getCacheRevision())
        

    
    def _Shop__onGetValueResponse(self, resultID, key, callback):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None, self._Shop__getCacheRevision())
            
            return None
        if self._Shop__isSynchronizing:
            self._Shop__getValue(key, callback)
            return None
        if key is None:
            pass
        1
        value = self._Shop__cache.get(key, None)
        if callback is not None:
            callback(resultID, value, self._Shop__getCacheRevision())
        

    
    def _Shop__onGetPriceResponse(self, resultID, itemTypeIdx, nationIdx, itemShopID, callback):
        if resultID < 0:
            price = None
        else:
            price = self._Shop__getPriceFromCache(itemTypeIdx, nationIdx, itemShopID)
        if callback is not None:
            callback(resultID, price, self._Shop__getCacheRevision())
        

    
    def _Shop__onGetVehiclePriceResponse(self, resultID, vehCompDescr, isSellPrice, callback):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None, self._Shop__getCacheRevision())
            
            return None
        price = self._Shop__getVehiclePriceFromCache(vehCompDescr, None)
        if isSellPrice and price is not None:
            price = self.getSellPrice(price, self._Shop__getSellPriceModifiersFromCache())
        
        if callback is not None:
            callback(resultID, price, self._Shop__getCacheRevision())
        

    
    def _Shop__onGetVehiclesSellPriceResponse(self, resultID, vehCompDescrs, callback):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None, self._Shop__getCacheRevision())
            
            return None
        prices = []
        for vehCompDescr in vehCompDescrs:
            price = self._Shop__getVehiclePriceFromCache(vehCompDescr, None)
            if price is None:
                prices = None
                break
            
            prices.append(self.getSellPrice(price, self._Shop__getSellPriceModifiersFromCache()))
        
        if callback is not None:
            callback(resultID, prices, self._Shop__getCacheRevision())
        

    
    def _Shop__onGetComponentPriceResponse(self, resultID, compDescr, isSellPrice, callback):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None, self._Shop__getCacheRevision())
            
            return None
        (itemTypeIdx, nationIdx, innationIdx) = vehicles.parseIntCompactDescr(compDescr)
        price = self._Shop__getPriceFromCache(itemTypeIdx, nationIdx, compDescr)
        if isSellPrice:
            price = self.getSellPrice(price, self._Shop__getSellPriceModifiersFromCache())
        
        if callback is not None:
            callback(resultID, price, self._Shop__getCacheRevision())
        

    
    def _Shop__onGetAmmoSellPriceResponse(self, resultID, ammo, callback):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None, self._Shop__getCacheRevision())
            
            return None
        price = 0
        for (shellCompDescr, count) in AmmoIterator(ammo):
            if count == 0:
                continue
            
            (_, nationIdx, innationIdx) = vehicles.parseIntCompactDescr(shellCompDescr)
            shellPrice = self._Shop__getPriceFromCache(_SHELL, nationIdx, shellCompDescr)
            shellSellPrice = self.getSellPrice(shellPrice, self._Shop__getSellPriceModifiersFromCache())
            price += shellSellPrice * count
        
        if callback is not None:
            callback(resultID, price, self._Shop__getCacheRevision())
        

    
    def _Shop__getNextSyncID(self):
        self._Shop__syncID += 1
        if self._Shop__syncID > 30000:
            self._Shop__syncID = 1
        
        return self._Shop__syncID

    
    def _Shop__sendSyncRequest(self, id, proxy):
        if self._Shop__ignore:
            return None
        clientRev = self._Shop__getCacheRevision()
        self._Shop__account._doCmdInt3(AccountCommands.CMD_SYNC_SHOP, clientRev, 0, 0, proxy)

    
    def _Shop__getCacheRevision(self):
        return self._Shop__cache.get('rev', 0)

    
    def _Shop__getPriceFromCache(self, itemTypeIdx, nationIdx, itemShopID, default = (0, 0)):
        return self._Shop__cache.get('items', { }).get(nationIdx, { }).get(itemTypeIdx, ({ }, set()))[0].get(itemShopID, default)

    
    def _Shop__getVehiclePriceFromCache(self, vehCompDescr, default = (0, 0)):
        (nationIdx, innationIdx) = vehicles.parseVehicleCompactDescr(vehCompDescr)
        price = self._Shop__getPriceFromCache(_VEHICLE, nationIdx, innationIdx, None)
        if price is None:
            return default
        vehDescr = vehicles.VehicleDescr(compactDescr = vehCompDescr)
        devices = vehDescr.getDevices()
        for (defCompDescr, instCompDescr) in izip(devices[0], devices[1]):
            if defCompDescr == instCompDescr:
                continue
            
            (itemTypeIdx, nationIdx, innationIdx) = vehicles.parseIntCompactDescr(defCompDescr)
            compPrice = self._Shop__getPriceFromCache(itemTypeIdx, nationIdx, defCompDescr, None)
            if compPrice is None:
                return default
            price = _subtractPrices(price, compPrice)
            (itemTypeIdx, nationIdx, innationIdx) = vehicles.parseIntCompactDescr(instCompDescr)
            compPrice = self._Shop__getPriceFromCache(itemTypeIdx, nationIdx, instCompDescr, None)
            if compPrice is None:
                return default
            price = _summPrices(price, compPrice)
        
        for optDevCompDescr in devices[2]:
            (itemTypeIdx, nationIdx, innationIdx) = vehicles.parseIntCompactDescr(optDevCompDescr)
            compPrice = self._Shop__getPriceFromCache(itemTypeIdx, nationIdx, optDevCompDescr, None)
            if compPrice is None:
                return default
            price = _summPrices(price, compPrice)
        
        return price

    
    def _Shop__getSellPriceModifiersFromCache(self):
        return (self._Shop__getCacheRevision(), self._Shop__cache.get('exchangeRate', 0), self._Shop__cache.get('sellPriceModif', 0))

    
    def _Shop__getValue(self, key, callback):
        if self._Shop__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, None, self._Shop__getCacheRevision())
            
            return None
        if not self._Shop__isSynchronizing:
            self._Shop__onGetValueResponse(AccountCommands.RES_CACHE, key, callback)
            return None
        
        proxy = lambda resultID, data: self._Shop__onGetValueResponse(resultID, key, callback)
        self._Shop__syncController.request(self._Shop__syncID, proxy)



def _summPrices(price1, price2):
    return (price1[0] + price2[0], price1[1] + price2[1])


def _subtractPrices(price1, price2):
    return (price1[0] - price2[0], price1[1] - price2[1])


