# Source Generated with Decompyle++
# File: Inventory.pyc (Python 2.6)

import AccountCommands
import items
import dossiers
import collections
from functools import partial
from AccountSyncData import synchronizeDicts
from PlayerEvents import g_playerEvents as events
from items import vehicles, tankmen
from constants import DOSSIER_TYPE
from AccountCommands import LOCK_REASON, SELL_VEHICLE_FLAG, VEHICLE_SETTINGS_FLAG
from debug_utils import *
from account_shared import AmmoIterator, getAmmoDiff
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

def getAmmoAsDict(ammo):
    ammoAsDict = collections.defaultdict(int)
    for i in xrange(len(ammo) / 2):
        ammoAsDict[ammo[2 * i]] += ammo[2 * i + 1]
    
    return ammoAsDict


class Inventory(object):
    
    def __init__(self, syncData):
        self._Inventory__account = None
        self._Inventory__syncData = syncData
        self._Inventory__cache = { }
        self._Inventory__ignore = True

    
    def onAccountBecomePlayer(self):
        self._Inventory__ignore = False

    
    def onAccountBecomeNonPlayer(self):
        self._Inventory__ignore = True

    
    def setAccount(self, account):
        self._Inventory__account = account

    
    def synchronize(self, isFullSync, diff):
        if isFullSync:
            self._Inventory__cache.clear()
        
        invDiff = diff.get('inventory', None)
        if invDiff is not None:
            for (itemTypeIdx, itemInvDiff) in invDiff.iteritems():
                synchronizeDicts(itemInvDiff, self._Inventory__cache.setdefault(itemTypeIdx, { }))
            
        
        cacheDiff = diff.get('cache', None)
        if cacheDiff is not None:
            vehsLockDiff = cacheDiff.get('vehsLock', None)
            if vehsLockDiff is not None:
                itemInvCache = self._Inventory__cache.setdefault(_VEHICLE, { })
                synchronizeDicts(vehsLockDiff, itemInvCache.setdefault('lock', { }))
            
        

    
    def getCache(self, callback):
        self._Inventory__syncData.waitForSync(partial(self._Inventory__onGetItemsResponse, None, callback))

    
    def getItems(self, itemTypeIdx, callback):
        self._Inventory__syncData.waitForSync(partial(self._Inventory__onGetItemsResponse, itemTypeIdx, callback))

    
    def sell(self, itemTypeIdx, itemInvID, count, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        if itemTypeIdx == _VEHICLE:
            self.sellVehicle(itemInvID, False, False, False, False, False, True, [], callback)
            return None
        if itemTypeIdx == _TANKMAN:
            if callback is not None:
                callback(AccountCommands.RES_WRONG_ARGS)
            
            return None
        self._Inventory__account.shop.waitForSync(partial(self._Inventory__sellItem_onShopSynced, itemTypeIdx, itemInvID, count, callback))

    
    def sellVehicle(self, vehInvID, sellShells, sellEquipments, sellModules, sellRmOptDevs, dismantleNonRmOptDevs, dismissCrew, componentCompDescrs, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        flags = SELL_VEHICLE_FLAG.NONE
        if dismissCrew:
            flags |= SELL_VEHICLE_FLAG.CREW
        
        if sellShells:
            flags |= SELL_VEHICLE_FLAG.SHELLS
        
        if sellEquipments:
            flags |= SELL_VEHICLE_FLAG.EQS
        
        if sellRmOptDevs:
            flags |= SELL_VEHICLE_FLAG.RM_OPTIONAL_DEVICES
        
        if dismantleNonRmOptDevs:
            flags |= SELL_VEHICLE_FLAG.NONRM_OPTIONAL_DEVICES
        
        if sellModules:
            flags |= SELL_VEHICLE_FLAG.MODULES
        
        self._Inventory__account.shop.waitForSync(partial(self._Inventory__sellVehicle_onShopSynced, vehInvID, flags, componentCompDescrs, callback))

    
    def dismissTankman(self, tmanInvID, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Inventory__account._doCmdInt3(AccountCommands.CMD_DISMISS_TMAN, tmanInvID, 0, 0, proxy)

    
    def equip(self, vehInvID, itemCompDescr, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, 0, [])
            
            return None
        itemTypeIdx = vehicles.parseIntCompactDescr(itemCompDescr)[0]
        if not itemTypeIdx in (_CHASSIS, _GUN, _ENGINE, _FUEL_TANK, _RADIO):
            raise AssertionError
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID, ext)
        else:
            proxy = None
        self._Inventory__account._doCmdInt3(AccountCommands.CMD_EQUIP, vehInvID, itemCompDescr, 0, proxy)

    
    def equipTurret(self, vehInvID, turretCompDescr, gunCompDescr, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, 0, [])
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID, ext)
        else:
            proxy = None
        self._Inventory__account._doCmdInt3(AccountCommands.CMD_EQUIP, vehInvID, turretCompDescr, gunCompDescr, proxy)

    
    def equipOptionalDevice(self, vehInvID, deviceCompDescr, slotIdx, isPaidRemoval, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, 0, [])
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Inventory__account._doCmdInt4(AccountCommands.CMD_EQUIP_OPTDEV, vehInvID, deviceCompDescr, slotIdx, int(isPaidRemoval), proxy)

    
    def equipShells(self, vehInvID, shells, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, [])
            
            return None
        continue
        arr = _[1] + [ int(s) for s in shells ]
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Inventory__account._doCmdIntArr(AccountCommands.CMD_EQUIP_SHELLS, arr, proxy)

    
    def equipEquipments(self, vehInvID, eqs, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, [])
            
            return None
        continue
        arr = _[1] + [ int(e) for e in eqs ]
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Inventory__account._doCmdIntArr(AccountCommands.CMD_EQUIP_EQS, arr, proxy)

    
    def setAndFillLayouts(self, vehInvID, shellsLayout, eqsLayout, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, '', { })
            
            return None
        self._Inventory__account.shop.waitForSync(partial(self._Inventory__setAndFillLayouts_onShopSynced, vehInvID, shellsLayout, eqsLayout, callback))

    
    def equipTankman(self, vehInvID, slot, tmanInvID, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, [])
            
            return None
        if tmanInvID is None:
            tmanInvID = -1
        
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Inventory__account._doCmdInt3(AccountCommands.CMD_EQUIP_TMAN, vehInvID, slot, tmanInvID, proxy)

    
    def repair(self, vehInvID, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Inventory__account._doCmdInt3(AccountCommands.CMD_REPAIR, vehInvID, 0, 0, proxy)

    
    def addTankmanSkill(self, tmanInvID, skillName, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        skillIdx = tankmen.SKILL_INDICES[skillName]
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Inventory__account._doCmdInt3(AccountCommands.CMD_TMAN_ADD_SKILL, tmanInvID, skillIdx, 0, proxy)

    
    def dropTankmanSkills(self, tmanInvID, dropSkillsCostIdx, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        self._Inventory__account.shop.waitForSync(partial(self._Inventory__dropSkillsTman_onShopSynced, tmanInvID, dropSkillsCostIdx, callback))

    
    def respecTankman(self, tmanInvID, vehTypeCompDescr, tmanCostTypeIdx, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        if vehTypeCompDescr is None:
            vehTypeCompDescr = 0
        
        self._Inventory__account.shop.waitForSync(partial(self._Inventory__respecTman_onShopSynced, tmanInvID, vehTypeCompDescr, tmanCostTypeIdx, callback))

    
    def replacePassport(self, tmanInvID, isFemale, firstNameID, lastNameID, iconID, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        self._Inventory__account.shop.waitForSync(partial(self._Inventory__replacePassport_onShopSynced, tmanInvID, isFemale, firstNameID, lastNameID, iconID, callback))

    
    def freeXPToTankman(self, tmanInvID, freeXP, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback('', AccountCommands.RES_NON_PLAYER)
            
            return None
        self._Inventory__account.shop.waitForSync(partial(self._Inventory__freeXPToTankman_onShopSynced, tmanInvID, freeXP, callback))

    
    def changeVehicleSetting(self, vehInvID, setting, isOn, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        if isOn:
            pass
        1
        isOn = 0
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Inventory__account._doCmdInt3(AccountCommands.CMD_VEH_SETTINGS, vehInvID, setting, isOn, proxy)

    
    def changeVehicleCamouflage(self, vehInvID, camouflageKind, camouflageID, periodDays, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        self._Inventory__account.shop.waitForSync(partial(self._Inventory__changeVehCamouflage_onShopSynced, vehInvID, camouflageKind, camouflageID, periodDays, callback))

    
    def changeVehicleEmblem(self, vehInvID, position, emblemID, periodDays, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        self._Inventory__account.shop.waitForSync(partial(self._Inventory__changeVehEmblem_onShopSynced, vehInvID, position, emblemID, periodDays, callback))

    
    def changeVehicleInscription(self, vehInvID, position, inscriptionID, periodDays, colorID, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        self._Inventory__account.shop.waitForSync(partial(self._Inventory__changeVehInscription_onShopSynced, vehInvID, position, inscriptionID, periodDays, colorID, callback))

    
    def changeVehicleHorn(self, vehInvID, hornID, callback):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        self._Inventory__account.shop.waitForSync(partial(self._Inventory__changeVehHorn_onShopSynced, vehInvID, hornID, callback))

    
    def addTankmanExperience(self, tmanInvID, xp, callback = None):
        if self._Inventory__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Inventory__account._doCmdInt3(AccountCommands.CMD_ADD_TMAN_XP, tmanInvID, xp, 0, proxy)

    
    def _Inventory__onGetItemsResponse(self, itemTypeIdx, callback, resultID):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None)
            
            return None
        if itemTypeIdx is None:
            pass
        1
        items = self._Inventory__cache.get(itemTypeIdx, None)
        if callback is not None:
            callback(resultID, items)
        

    
    def _Inventory__sellItem_onShopSynced(self, itemTypeIdx, itemInvID, count, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Inventory__account._doCmdInt4(AccountCommands.CMD_SELL_ITEM, shopRev, itemTypeIdx, itemInvID, count, proxy)

    
    def _Inventory__sellVehicle_onShopSynced(self, vehInvID, flags, componentCompDescrs, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        arr = [
            shopRev,
            vehInvID,
            flags] + componentCompDescrs
        self._Inventory__account._doCmdIntArr(AccountCommands.CMD_SELL_VEHICLE, arr, proxy)

    
    def _Inventory__dropSkillsTman_onShopSynced(self, tmanInvID, dropSkillsCostIdx, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Inventory__account._doCmdInt3(AccountCommands.CMD_TMAN_DROP_SKILLS, shopRev, tmanInvID, dropSkillsCostIdx, proxy)

    
    def _Inventory__respecTman_onShopSynced(self, tmanInvID, vehTypeCompDescr, tmanCostTypeIdx, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Inventory__account._doCmdInt4(AccountCommands.CMD_TMAN_RESPEC, shopRev, tmanInvID, tmanCostTypeIdx, vehTypeCompDescr, proxy)

    
    def _Inventory__replacePassport_onShopSynced(self, tmanInvID, isFemale, firstNameID, lastNameID, iconID, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            
            return None
        arr = [
            shopRev,
            tmanInvID]
        if isFemale is None:
            arr.append(-1)
        elif isFemale:
            arr.append(1)
        else:
            arr.append(0)
        if firstNameID is not None:
            pass
        1
        firstNameID(-1)
        if lastNameID is not None:
            pass
        1
        lastNameID(-1)
        if iconID is not None:
            pass
        1
        iconID(-1)
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Inventory__account._doCmdIntArr(AccountCommands.CMD_TMAN_PASSPORT, arr, proxy)

    
    def _Inventory__freeXPToTankman_onShopSynced(self, tmanInvID, freeXP, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback('', resultID)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(errorStr, resultID)
        else:
            proxy = None
        self._Inventory__account._doCmdInt3(AccountCommands.CMD_TRAINING_TMAN, shopRev, tmanInvID, freeXP, proxy)

    
    def _Inventory__changeVehCamouflage_onShopSynced(self, vehInvID, camouflageKind, camouflageID, periodDays, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        arr = [
            shopRev,
            vehInvID,
            camouflageKind,
            camouflageID,
            periodDays]
        self._Inventory__account._doCmdIntArr(AccountCommands.CMD_VEH_CAMOUFLAGE, arr, proxy)

    
    def _Inventory__setAndFillLayouts_onShopSynced(self, vehInvID, shellsLayout, eqsLayout, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID, '', { })
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID, errorStr, ext)
        else:
            proxy = None
        arr = [
            shopRev,
            vehInvID]
        if shellsLayout is not None:
            arr += shellsLayout
        
        arr += (-1, -1)
        if eqsLayout is not None:
            arr += eqsLayout
        
        self._Inventory__account._doCmdIntArr(AccountCommands.CMD_SET_AND_FILL_LAYOUTS, arr, proxy)

    
    def _Inventory__changeVehEmblem_onShopSynced(self, vehInvID, position, emblemID, periodDays, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        arr = [
            shopRev,
            vehInvID,
            position,
            emblemID,
            periodDays]
        self._Inventory__account._doCmdIntArr(AccountCommands.CMD_VEH_EMBLEM, arr, proxy)

    
    def _Inventory__changeVehInscription_onShopSynced(self, vehInvID, position, inscriptionID, periodDays, colorID, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        arr = [
            shopRev,
            vehInvID,
            position,
            inscriptionID,
            periodDays,
            colorID]
        self._Inventory__account._doCmdIntArr(AccountCommands.CMD_VEH_INSCRIPTION, arr, proxy)

    
    def _Inventory__changeVehHorn_onShopSynced(self, vehInvID, hornID, callback, resultID, shopRev):
        if resultID < 0:
            if callback is not None:
                callback(resultID)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Inventory__account._doCmdInt3(AccountCommands.CMD_VEH_HORN, shopRev, vehInvID, hornID, proxy)



