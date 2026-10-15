# Source Generated with Decompyle++
# File: Stats.pyc (Python 2.6)

import AccountCommands
import time
import constants
import items
import dossiers
from functools import partial
from AccountSyncData import synchronizeDicts
from PlayerEvents import g_playerEvents as events
from itertools import izip
from items import vehicles
from constants import DOSSIER_TYPE, ACCOUNT_ATTR
from AccountCommands import VEHICLE_SETTINGS_FLAG
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
_SIMPLE_VALUE_STATS = ('credits', 'gold', 'slots', 'berths', 'freeXP', 'dossier', 'clanInfo', 'accOnline', 'accOffline', 'freeTMenLeft', 'freeVehiclesLeft', 'vehicleSellsLeft', 'captchaTriesLeft', 'hasFinPassword', 'finPswdAttemptsLeft', 'tkillIsSuspected', 'denunciationsLeft', 'tutorialsCompleted', 'battlesTillCaptcha', 'dailyPlayHours', 'playLimits')
_DICT_STATS = ('vehTypeXP', 'vehTypeLocks', 'restrictions', 'globalVehicleLocks')
_GROWING_SET_STATS = ('unlocks', 'eliteVehicles', 'multipliedXPVehs')
_ACCOUNT_STATS = ('clanDBID', 'attrs', 'premiumExpiryTime', 'autoBanTime')

class Stats(object):
    
    def __init__(self, syncData):
        self._Stats__account = None
        self._Stats__syncData = syncData
        self._Stats__cache = { }
        self._Stats__ignore = True

    
    def onAccountBecomePlayer(self):
        self._Stats__ignore = False

    
    def onAccountBecomeNonPlayer(self):
        self._Stats__ignore = True

    
    def setAccount(self, account):
        self._Stats__account = account

    
    def synchronize(self, isFullSync, diff):
        if isFullSync:
            self._Stats__cache.clear()
        
        cache = self._Stats__cache
        statsDiff = diff.get('stats', None)
        if statsDiff is not None:
            for stat in _SIMPLE_VALUE_STATS:
                if stat in statsDiff:
                    cache[stat] = statsDiff[stat]
                    continue
            
            for stat in _DICT_STATS:
                stat_r = stat + '_r'
                if stat_r in statsDiff:
                    cache[stat] = statsDiff[stat_r]
                
                if stat in statsDiff:
                    synchronizeDicts(statsDiff[stat], cache.setdefault(stat, dict()))
                    continue
            
            for stat in _GROWING_SET_STATS:
                stat_r = stat + '_r'
                if stat_r in statsDiff:
                    cache[stat] = statsDiff[stat_r]
                
                if stat in statsDiff:
                    cache.setdefault(stat, set()).update(statsDiff[stat])
                    continue
            
        
        accountDiff = diff.get('account', None)
        if accountDiff is not None:
            for stat in _ACCOUNT_STATS:
                if stat in accountDiff:
                    cache[stat] = accountDiff[stat]
                    continue
            
        
        economicsDiff = diff.get('economics', None)
        if economicsDiff is not None:
            for stat in ('unlocks', 'eliteVehicles'):
                if stat in economicsDiff:
                    cache.setdefault(stat, set()).update(economicsDiff[stat])
                    continue
            
        
        cacheDiff = diff.get('cache', None)
        if cacheDiff is not None:
            for stat in ('isFinPswdVerified',):
                if stat in cacheDiff:
                    cache[stat] = cacheDiff[stat]
                    continue
            
        

    
    def getCache(self, callback = None):
        if self._Stats__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, None)
            
            return None
        self._Stats__syncData.waitForSync(partial(self._Stats__onGetResponse, None, callback))

    
    def get(self, statName, callback = None):
        if self._Stats__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, None)
            
            return None
        self._Stats__syncData.waitForSync(partial(self._Stats__onGetResponse, statName, callback))

    
    def unlock(self, vehTypeCompDescr, unlockIdx, callback = None):
        if self._Stats__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Stats__account._doCmdInt3(AccountCommands.CMD_UNLOCK, vehTypeCompDescr, unlockIdx, 0, proxy)

    
    def setCurrentVehicle(self, vehInvID, callback = None):
        LOG_WARNING('Deprecated. setCurrentVehicle')

    
    def exchange(self, gold, callback = None):
        if self._Stats__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        self._Stats__account.shop.getExchangeRate(partial(self._Stats__exchange_onGetRate, gold, callback))

    
    def convertToFreeXP(self, vehTypeCompDescrs, xp, callback = None):
        if self._Stats__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        self._Stats__account.shop.getFreeXPConversion(partial(self._Stats__convertToFreeXP_onGetParameters, vehTypeCompDescrs, xp, callback))

    
    def upgradeToPremium(self, days, callback = None):
        if self._Stats__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, 0)
            
            return None
        self._Stats__account.shop.getPremiumCost(partial(self._Stats__premium_onGetPremCost, days, callback))

    
    def buySlot(self, callback = None):
        if self._Stats__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, 0)
            
            return None
        self._Stats__account.shop.waitForSync(partial(self._Stats__slot_onShopSynced, callback))

    
    def buyBerths(self, callback = None):
        if self._Stats__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, 0)
            
            return None
        self._Stats__account.shop.waitForSync(partial(self._Stats__berths_onShopSynced, callback))

    
    def setMoney(self, credits, gold = 0, callback = None):
        if self._Stats__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Stats__account._doCmdInt3(AccountCommands.CMD_SET_MONEY, credits, gold, 0, proxy)

    
    def addExperience(self, vehTypeName, xp, callback = None):
        if self._Stats__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        vehTypeCompDescr = vehicles.makeIntCompactDescrByID('vehicle', *vehicles.g_list.getIDsByName(vehTypeName))
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Stats__account._doCmdInt3(AccountCommands.CMD_ADD_XP, vehTypeCompDescr, xp, 0, proxy)

    
    def unlockAll(self, callback):
        if self._Stats__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Stats__account._doCmdInt3(AccountCommands.CMD_UNLOCK_ALL, 0, 0, 0, proxy)

    
    def _Stats__onGetResponse(self, statName, callback, resultID):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None)
            
            return None
        if statName is None:
            pass
        1
        statValue = self._Stats__cache.get(statName, None)
        if callback is not None:
            callback(resultID, statValue)
        

    
    def _Stats__exchange_onGetRate(self, gold, callback, resultID, exchRate, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None)
            
            return None
        if exchRate is None:
            LOG_ERROR('Result of the getExchangeRate request is None')
            if callback is not None:
                callback(AccountCommands.RES_FAILURE)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Stats__account._doCmdInt3(AccountCommands.CMD_EXCHANGE, shopRev, gold, 0, proxy)

    
    def _Stats__convertToFreeXP_onGetParameters(self, vehTypeCompDescrs, xp, callback, resultID, freeXPConversion, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None)
            
            return None
        if freeXPConversion is None:
            LOG_ERROR('Result of the getFreeXPConversion request is None')
            if callback is not None:
                callback(AccountCommands.RES_FAILURE)
            
            return None
        arr = [
            shopRev,
            xp] + list(vehTypeCompDescrs)
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Stats__account._doCmdIntArr(AccountCommands.CMD_FREE_XP_CONV, arr, proxy)

    
    def _Stats__premium_onGetPremCost(self, days, callback, resultID, premCost, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None)
            
            return None
        if premCost is None:
            LOG_ERROR('Result of the getPremiumCost request is None')
            if callback is not None:
                callback(AccountCommands.RES_FAILURE)
            
            return None
        gold = premCost.get(days, None)
        if gold is None:
            LOG_ERROR('Wrong days number')
            if callback is not None:
                callback(AccountCommands.RES_WRONG_ARGS)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Stats__account._doCmdInt3(AccountCommands.CMD_PREMIUM, shopRev, days, 0, proxy)

    
    def _Stats__slot_onShopSynced(self, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Stats__account._doCmdInt3(AccountCommands.CMD_BUY_SLOT, shopRev, 0, 0, proxy)

    
    def _Stats__berths_onShopSynced(self, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Stats__account._doCmdInt3(AccountCommands.CMD_BUY_BERTHS, shopRev, 0, 0, proxy)



