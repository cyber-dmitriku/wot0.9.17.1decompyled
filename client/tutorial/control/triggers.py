# Source Generated with Decompyle++
# File: triggers.pyc (Python 2.6)

import BigWorld
from account_helpers.Inventory import _VEHICLE, _TANKMAN
from AccountCommands import RES_SUCCESS
from CurrentVehicle import g_currentVehicle
from PlayerEvents import g_playerEvents
import dossiers
from items import vehicles, ITEM_TYPE_NAMES, tankmen
from tutorial.control import TutorialProxyHolder
from tutorial.control.functional import factory
from tutorial.data import HasID
from tutorial.logger import LOG_ERROR
from gui.ClientUpdateManager import g_clientUpdateManager
__all__ = [
    'BonusTrigger',
    'BattleCountRequester',
    'ItemUnlockedTrigger',
    'ItemInstalledTrigger',
    'VehicleSettingTrigger',
    'EliteVehicleTrigger',
    'AccountCreditsTrigger',
    'ItemPriceTrigger',
    'ItemExperienceTrigger',
    'EquipmentInstalledTrigger',
    'InventoryItemTrigger',
    'CurVehicleCrewTrigger',
    'CurVehicleLockedTrigger',
    'CurrentVehicleTriggerTankmanLevelTrigger',
    'TankmanSkillTrigger',
    'FreeVehicleSlotTrigger']

class _Trigger(TutorialProxyHolder, HasID):
    
    def __init__(self, triggerID):
        super(_Trigger, self).__init__()
        self._Trigger__triggerID = triggerID
        self._Trigger__onEffects = []
        self._Trigger__offEffects = []
        self._Trigger__excludeTriggerIDs = []
        self.isRunning = False
        self.isSubscribed = False

    
    def getID(self):
        return self._Trigger__triggerID

    
    def setID(self, id):
        self._Trigger__triggerID = id

    
    def addOnEffect(self, effect):
        self._Trigger__onEffects.append(effect)

    
    def addOffEffect(self, effect):
        self._Trigger__offEffects.append(effect)

    
    def addExcludeTriggerID(self, triggerID):
        self._Trigger__excludeTriggerIDs.append(triggerID)

    
    def run(self):
        self.isRunning = True
        self.toggle(isOn = self.isOn())

    
    def clear(self):
        self.isRunning = False

    
    def isOn(self, *args):
        return True

    
    def toggle(self, isOn = True):
        effects = self._Trigger__offEffects
        if isOn:
            effects = self._Trigger__onEffects
            getter = self._tutorial._data.getTrigger
            for triggerID in self._Trigger__excludeTriggerIDs:
                trigger = getter(triggerID)
                if trigger is not None:
                    trigger.clear()
                    continue
                LOG_ERROR('Trigger not found', triggerID)
            
        
        if len(effects):
            self._tutorial.storeEffectsInQueue(factory(effects), benefit = True)
        
        self.isRunning = False

    
    def _setFlagValue(self, flagID, value):
        if flagID is None:
            return None
        flags = self._tutorial.getFlags()
        isActive = flags.isActiveFlag(flagID)
        if value:
            if not isActive:
                flags.activateFlag(flagID)
                self._tutorial.invalidateFlags()
            
        elif isActive:
            flags.deactivateFlag(flagID)
            self._tutorial.invalidateFlags()
        



class _TriggerWithValidateVar(_Trigger):
    
    def __init__(self, triggerID, validateVarID, setVarID = None):
        super(_TriggerWithValidateVar, self).__init__(triggerID)
        self._validateVarID = validateVarID
        self._setVarID = setVarID

    
    def vars(self):
        return self._tutorial.getVars()

    
    def getVar(self):
        return self._tutorial.getVars().get(self._validateVarID)

    
    def getIterVar(self):
        var = self._tutorial.getVars().get(self._validateVarID)
        if hasattr(var, '__iter__'):
            var = set(var)
        else:
            var = set([
                var])
        return var

    
    def setVar(self, value):
        if self._setVarID is not None:
            self._tutorial.getVars().set(self._setVarID, value)
        



class BonusTrigger(_Trigger):
    
    def __init__(self, triggerID, bonusID):
        super(BonusTrigger, self).__init__(triggerID)
        self.bonusID = bonusID

    
    def run(self):
        self.isRunning = True
        if not self.isSubscribed:
            self.isSubscribed = True
            g_clientUpdateManager.addCallbacks({
                'stats.tutorialsCompleted': self.onTutorialCompleted })
        
        self.toggle(isOn = self.isOn(self._tutorial._bonusCompleted))

    
    def isOn(self, tutorialsCompleted):
        return tutorialsCompleted & 1 << self.bonusID != 0

    
    def clear(self):
        g_clientUpdateManager.removeObjectCallbacks(self)
        self.isSubscribed = False
        self.isRunning = False

    
    def onTutorialCompleted(self, completed):
        if completed is not None:
            self.toggle(isOn = self.isOn(completed))
        



class BattleCountRequester(_TriggerWithValidateVar):
    
    def __init__(self, triggerID, validateVarID, setVarID = None):
        super(BattleCountRequester, self).__init__(triggerID, validateVarID, setVarID = setVarID)

    
    def run(self):
        self.isRunning = True
        self._gui.showWaiting('request-battle-count')
        BigWorld.player().stats.get('dossier', self._BattleCountRequester__cb_onGetDossier)

    
    def isOn(self, battlesCount):
        return battlesCount >= self.getVar()

    
    def _BattleCountRequester__cb_onGetDossier(self, resultID, dossierCompDescr):
        self._gui.hideWaiting('request-battle-count')
        if resultID < RES_SUCCESS:
            LOG_ERROR('Server return error on request dossier', resultID, dossierCompDescr)
            self.isRunning = False
            return None
        dossierDescr = dossiers.getAccountDossierDescr(dossierCompDescr)
        self.toggle(isOn = self.isOn(dossierDescr['battlesCount']))



class ItemUnlockedTrigger(_TriggerWithValidateVar):
    
    def __init__(self, triggerID, validateVarID, setVarID, validateUpdateOnly = False):
        super(ItemUnlockedTrigger, self).__init__(triggerID, validateVarID, setVarID = setVarID)
        self._validateUpdateOnly = validateUpdateOnly

    
    def run(self):
        if not self.isSubscribed:
            self.isSubscribed = True
            g_clientUpdateManager.addCallbacks({
                'stats.unlocks': self.onUnlocksUpdate })
        
        if self._validateUpdateOnly:
            return None
        self.isRunning = True
        self._gui.showWaiting('request-unlocks')
        BigWorld.player().stats.get('unlocks', self._ItemUnlockedTrigger__cb_onGetUnlocks)

    
    def isOn(self, unlocks):
        var = self.getIterVar()
        result = var & unlocks
        isOn = len(result) > 0
        if isOn:
            self.setVar(result.pop())
        
        return isOn

    
    def clear(self):
        g_clientUpdateManager.removeObjectCallbacks(self)
        self.isSubscribed = False
        self.isRunning = False

    
    def _ItemUnlockedTrigger__cb_onGetUnlocks(self, resultID, unlocks):
        self._gui.hideWaiting('request-unlocks')
        if resultID < 0:
            LOG_ERROR('Server return error unlocks request:', resultID)
            self.isRunning = False
            return None
        self.toggle(isOn = self.isOn(unlocks))

    
    def onUnlocksUpdate(self, unlocks):
        if unlocks is not None:
            self.toggle(isOn = self.isOn(unlocks))
        



class ItemInstalledTrigger(_TriggerWithValidateVar):
    
    def __init__(self, triggerID, validateVarID, setVarID = None):
        super(ItemInstalledTrigger, self).__init__(triggerID, validateVarID, setVarID = setVarID)

    
    def run(self):
        self.isRunning = True
        if not self.isSubscribed:
            g_clientUpdateManager.addCallbacks({
                'inventory.1.compDescr': self.onVehiclesUpdate })
            self.isSubscribed = True
        
        if g_currentVehicle.isPresent():
            pass
        1
        descriptor = None
        self.toggle(isOn = self.isOn(descriptor))

    
    def isOn(self, vehDescr):
        if vehDescr is None:
            return False
        (_, installed, _) = vehDescr.getDevices()
        itemCompactDescr = self.getVar()
        return itemCompactDescr in installed

    
    def clear(self):
        g_clientUpdateManager.removeObjectCallbacks(self)
        self.isSubscribed = False
        self.isRunning = False

    
    def onVehiclesUpdate(self, vehiclesDescr):
        if vehiclesDescr is not None and g_currentVehicle.isPresent():
            vCompDescr = vehiclesDescr.get(g_currentVehicle.vehicle.inventoryId)
            if vCompDescr is not None:
                self.toggle(isOn = self.isOn(vehicles.VehicleDescr(compactDescr = vCompDescr)))
            
        



class VehicleSettingTrigger(_TriggerWithValidateVar):
    
    def __init__(self, triggerID, validateVarID, setVarID = None):
        super(VehicleSettingTrigger, self).__init__(triggerID, validateVarID, setVarID = setVarID)

    
    def run(self):
        self.isRunning = True
        if not self.isSubscribed:
            g_clientUpdateManager.addCallbacks({
                'inventory.1.settings': self.onVehiclesSettingsUpdate })
            g_currentVehicle.onChanged += self._VehicleSettingTrigger__cv_onChanged
            self.isSubscribed = True
        
        if not g_currentVehicle.isPresent():
            self.toggle(isOn = False)
            return None
        self._gui.showWaiting('request-vehicle-settings')
        BigWorld.player().inventory.getItems(_VEHICLE, self._VehicleSettingTrigger__cb_onGetVehicles)

    
    def isOn(self, settings):
        return settings & self.getVar() != 0

    
    def clear(self):
        g_clientUpdateManager.removeObjectCallbacks(self)
        g_currentVehicle.onChanged -= self._VehicleSettingTrigger__cv_onChanged
        self.isSubscribed = False
        self.isRunning = False

    
    def _VehicleSettingTrigger__cb_onGetVehicles(self, resultID, data):
        self._gui.hideWaiting('request-vehicle-settings')
        if resultID < 0:
            LOG_ERROR('Server return error to request inventory vehicles:', resultID)
            self.isRunning = False
            return None
        invID = g_currentVehicle.vehicle.inventoryId
        vSettings = data.get('settings', { }).get(invID, 0)
        self.toggle(isOn = self.isOn(vSettings))

    
    def onVehiclesSettingsUpdate(self, vSettings):
        if vSettings is not None and g_currentVehicle.isPresent():
            curVehSet = vSettings.get(g_currentVehicle.vehicle.inventoryId)
            if curVehSet is not None:
                self.toggle(isOn = self.isOn(curVehSet))
            
        

    
    def _VehicleSettingTrigger__cv_onChanged(self):
        self.run()



class EliteVehicleTrigger(_TriggerWithValidateVar):
    
    def __init__(self, triggerID, validateVarID, setVarID = None):
        super(EliteVehicleTrigger, self).__init__(triggerID, validateVarID, setVarID = setVarID)

    
    def run(self):
        self.isRunning = True
        if not self.isSubscribed:
            guiRoot = self._gui.getGuiRoot()
            if guiRoot is not None and hasattr(guiRoot, 'onVehicleBecomeElite'):
                g_playerEvents.onVehicleBecomeElite -= guiRoot.onVehicleBecomeElite
            
            g_playerEvents.onVehicleBecomeElite += self._EliteVehicleTrigger__pe_onVehicleBecomeElite
            self.isSubscribed = True
        
        self._gui.showWaiting('request-elite-vehicles')
        BigWorld.player().stats.get('eliteVehicles', self._EliteVehicleTrigger__cb_onGetEliteVehicles)

    
    def isOn(self, eliteVehicles):
        return self.getVar() in eliteVehicles

    
    def clear(self):
        guiRoot = self._gui.getGuiRoot()
        if guiRoot is not None and hasattr(guiRoot, 'onVehicleBecomeElite'):
            g_playerEvents.onVehicleBecomeElite += guiRoot.onVehicleBecomeElite
        
        g_playerEvents.onVehicleBecomeElite -= self._EliteVehicleTrigger__pe_onVehicleBecomeElite
        self.isSubscribed = False
        self.isRunning = False

    
    def _EliteVehicleTrigger__cb_onGetEliteVehicles(self, resultID, eliteVehicles):
        self._gui.hideWaiting('request-elite-vehicles')
        if resultID < 0:
            LOG_ERROR('Server return error eliteVehicles request:', resultID)
            self.isRunning = False
            return None
        self.toggle(isOn = self.isOn(eliteVehicles))

    
    def _EliteVehicleTrigger__pe_onVehicleBecomeElite(self, vehTypeCompDescr):
        isOn = self.isOn(set([
            vehTypeCompDescr]))
        if isOn:
            self.toggle()
        else:
            guiRoot = self._gui.getGuiRoot()
            if guiRoot is not None and hasattr(guiRoot, 'onVehicleBecomeElite'):
                guiRoot.onVehicleBecomeElite(vehTypeCompDescr)
            



class AccountCreditsTrigger(_TriggerWithValidateVar):
    
    def __init__(self, triggerID, validateVarID, setVarID = None):
        super(AccountCreditsTrigger, self).__init__(triggerID, validateVarID, setVarID = setVarID)

    
    def run(self):
        self.isRunning = True
        if not self.isSubscribed:
            g_clientUpdateManager.addCallbacks({
                'stats.credits': self.onCreditsChanged })
            self.isSubscribed = True
        
        self._gui.showWaiting('request-credits')
        BigWorld.player().stats.get('credits', self._AccountCreditsTrigger__cb_onCreditsReceived)

    
    def isOn(self, credits):
        return self.getVar() <= credits

    
    def clear(self):
        g_clientUpdateManager.removeObjectCallbacks(self)
        self.isSubscribed = False
        self.isRunning = False

    
    def _AccountCreditsTrigger__cb_onCreditsReceived(self, resultID, credits):
        self._gui.hideWaiting('request-credits')
        if resultID < 0:
            LOG_ERROR('Server return error credits request: ', resultID)
            self.isRunning = False
            return None
        self.toggle(isOn = self.isOn(credits))

    
    def onCreditsChanged(self, credits):
        if credits is not None:
            self.toggle(isOn = self.isOn(credits))
        



class ItemPriceTrigger(_TriggerWithValidateVar):
    
    def __init__(self, triggerID, validateVarID, setVarID = None):
        super(ItemPriceTrigger, self).__init__(triggerID, validateVarID, setVarID = setVarID)
        self._accCredits = 0
        self._itemPrice = None

    
    def run(self):
        self.isRunning = True
        if not self.isSubscribed:
            g_clientUpdateManager.addCallbacks({
                'stats.credits': self.onCreditsChanged })
            g_playerEvents.onShopResync += self._ItemPriceTrigger__pe_onShopResync
            self.isSubscribed = True
        
        self._gui.showWaiting('request-credits')
        BigWorld.player().stats.get('credits', self._ItemPriceTrigger__cb_onCreditsReceived)

    
    def isOn(self):
        if self._itemPrice is not None:
            pass
        return self._itemPrice[0] <= self._accCredits

    
    def clear(self):
        g_clientUpdateManager.removeObjectCallbacks(self)
        g_playerEvents.onShopResync -= self._ItemPriceTrigger__pe_onShopResync
        self._accCredits = 0
        self._itemPrice = None
        self.isSubscribed = False
        self.isRunning = False

    
    def _ItemPriceTrigger__cb_onCreditsReceived(self, resultID, credits):
        self._gui.hideWaiting('request-credits')
        if resultID < 0:
            LOG_ERROR('Server return error credits request: ', resultID)
            self.isRunning = False
            return None
        self._accCredits = credits
        self._gui.showWaiting('request-shop')
        (itemTypeID, nationID, _) = vehicles.parseIntCompactDescr(self.getVar())
        BigWorld.player().shop.getItems(itemTypeID, nationID, self._ItemPriceTrigger__cb_onShopItemsReceived)

    
    def _ItemPriceTrigger__cb_onShopItemsReceived(self, resultID, data, _):
        self._gui.hideWaiting('request-shop')
        if resultID < 0:
            LOG_ERROR('Server return error shop %s items request:', resultID, data)
            data = ({ }, set([]))
        
        self._itemPrice = data[0].get(self.getVar())
        self.toggle(isOn = self.isOn())

    
    def onCreditsChanged(self, credits):
        if credits is not None:
            self._accCredits = credits
            self.toggle(isOn = self.isOn())
        

    
    def _ItemPriceTrigger__pe_onShopResync(self):
        self.run()



class ItemExperienceTrigger(_TriggerWithValidateVar):
    
    def __init__(self, triggerID, validateVarID, setVarID = None, vehicleVarID = None):
        super(ItemExperienceTrigger, self).__init__(triggerID, validateVarID, setVarID = setVarID)
        self._vehicleVarID = vehicleVarID
        self._vehTypeXPs = { }
        self._freeXP = 0

    
    def run(self):
        self.isRunning = True
        if not self.isSubscribed:
            g_clientUpdateManager.addCallbacks({
                'stats': self.onXpChanged })
            self.isSubscribed = True
        
        self._gui.showWaiting('request-xp')
        BigWorld.player().stats.get('vehTypeXP', self._ItemExperienceTrigger__cb_onGetVehTypeXP)

    
    def isOn(self):
        itemCompDescr = self.getVar()
        vehCompDescr = self.vars().get(self._vehicleVarID)
        (itemTypeID, nationID, compTypeID) = vehicles.parseIntCompactDescr(vehCompDescr)
        if not itemTypeID == _VEHICLE:
            raise AssertionError
        vehType = vehicles.g_cache.vehicle(nationID, compTypeID)
        unlocksDescrs = vehType.unlocksDescrs
        filtered = (filter,)((lambda info: info[1] == itemCompDescr), unlocksDescrs)
        vehTypeXP = self._vehTypeXPs.get(vehCompDescr, 0)
        result = False
        if len(filtered):
            result = vehTypeXP + self._freeXP >= filtered[0][0]
        
        return result

    
    def clear(self):
        g_clientUpdateManager.removeObjectCallbacks(self)
        self.isSubscribed = False
        self.isRunning = False
        self._vehTypeXP = 0
        self._freeXP = 0

    
    def _ItemExperienceTrigger__cb_onGetVehTypeXP(self, resultID, data):
        if resultID < 0:
            LOG_ERROR('Server return error vehTypeXP request: ', resultID)
            self.isRunning = False
            self._gui.hideWaiting('request-xp')
            return None
        self._vehTypeXPs = data
        BigWorld.player().stats.get('freeXP', self._ItemExperienceTrigger__cb_onGetFreeXP)

    
    def _ItemExperienceTrigger__cb_onGetFreeXP(self, resultID, data):
        self._gui.hideWaiting('request-xp')
        if resultID < 0:
            LOG_ERROR('Server return error vehTypeXP request: ', resultID)
            self.isRunning = False
            return None
        self._freeXP = data
        self.toggle(isOn = self.isOn())

    
    def onXpChanged(self, stats):
        if 'vehTypeXP' in stats or 'freeXP' in stats:
            vehTypeXPs = stats.get('vehTypeXP')
            freeXP = stats.get('freeXP')
            updated = False
            if vehTypeXPs is not None:
                self._vehTypeXPs = vehTypeXPs
                updated = True
            
            if freeXP is not None:
                self._freeXP = freeXP
                updated = True
            
            if updated:
                self.toggle(isOn = self.isOn())
            
        



class EquipmentInstalledTrigger(_TriggerWithValidateVar):
    
    def __init__(self, triggerID, validateVarID, setVarID = None):
        super(EquipmentInstalledTrigger, self).__init__(triggerID, validateVarID, setVarID = setVarID)

    
    def run(self):
        self.isRunning = True
        if not self.isSubscribed:
            g_clientUpdateManager.addCallbacks({
                'inventory.1.eqs': self.onEquipmentsChanged })
            g_currentVehicle.onChanged += self._EquipmentInstalledTrigger__cv_onChanged
            self.isSubscribed = True
        
        if not g_currentVehicle.isPresent():
            self.toggle(isOn = False)
            return None
        self._gui.showWaiting('request-vehicle-equipments')
        BigWorld.player().inventory.getItems(_VEHICLE, self._EquipmentInstalledTrigger__cb_onGetVehicles)

    
    def isOn(self, eqs):
        return self.getVar() in eqs

    
    def clear(self):
        g_clientUpdateManager.removeObjectCallbacks(self)
        g_currentVehicle.onChanged -= self._EquipmentInstalledTrigger__cv_onChanged
        self.isSubscribed = False
        self.isRunning = False

    
    def _EquipmentInstalledTrigger__cb_onGetVehicles(self, resultID, data):
        self._gui.hideWaiting('request-vehicle-equipments')
        if resultID < 0:
            LOG_ERROR('Server return error to request inventory vehicles:', resultID)
            self.isRunning = False
            return None
        invID = g_currentVehicle.vehicle.inventoryId
        eqs = data.get('eqs', { }).get(invID, 0)
        self.toggle(isOn = self.isOn(eqs))

    
    def onEquipmentsChanged(self, eqs):
        if eqs is not None and g_currentVehicle.isPresent():
            e = eqs.get(g_currentVehicle.vehicle.inventoryId)
            if e is not None:
                self.toggle(isOn = self.isOn(e))
            
        

    
    def _EquipmentInstalledTrigger__cv_onChanged(self):
        self.run()



class InventoryItemTrigger(_TriggerWithValidateVar):
    
    def __init__(self, triggerID, validateVarID, setVarID = None, itemTypeID = _VEHICLE):
        super(InventoryItemTrigger, self).__init__(triggerID, validateVarID, setVarID = setVarID)
        self._itemTypeID = itemTypeID
        self._itemTypeName = ITEM_TYPE_NAMES[self._itemTypeID]

    
    def run(self):
        self.isRunning = True
        if not self.isSubscribed:
            g_clientUpdateManager.addCallbacks({
                'inventory': self.onInventoryChanged })
            self.isSubscribed = True
        
        self._gui.showWaiting('request-inventory-items')
        BigWorld.player().inventory.getItems(self._itemTypeID, self._InventoryItemTrigger__cb_onGetItemsFromInventory)

    
    def isOn(self, items):
        return len(self.getIterVar() & set(items)) > 0

    
    def clear(self):
        g_clientUpdateManager.removeObjectCallbacks(self)
        self.isSubscribed = False
        self.isRunning = False

    
    def _InventoryItemTrigger__makeIntVehCompactDescr(self, vCompDescr):
        (nationID, compTypeID) = vehicles.parseVehicleCompactDescr(vCompDescr)
        return vehicles.makeIntCompactDescrByID(self._itemTypeName, nationID, compTypeID)

    
    def _InventoryItemTrigger__cb_onGetItemsFromInventory(self, resultID, data):
        self._gui.hideWaiting('request-inventory-items')
        if resultID < RES_SUCCESS:
            LOG_ERROR('Server return error inventory {0:d} items request, responseCode = {1:d}'.format(self._itemTypeID, resultID))
            self.isRunning = False
            return None
        if self._itemTypeID == _VEHICLE:
            items = map(self._InventoryItemTrigger__makeIntVehCompactDescr, data.get('compDescr', { }).itervalues())
        else:
            items = dict(filter((lambda item: item[1] > 0), data.iteritems()))
            items = items.keys()
        self.toggle(isOn = self.isOn(items))

    
    def onInventoryChanged(self, inventory):
        invItems = inventory.get(self._itemTypeID)
        if invItems is not None:
            if self._itemTypeID == _VEHICLE:
                if not self.isRunning:
                    self.run()
                
            else:
                var = self.getIterVar()
                removeItems = dict((filter,)((lambda item: if item[1] is None:
passitem[0] in var), invItems.iteritems()))
                addItems = dict((filter,)((lambda item: if item[1] > 0:
passitem[0] in var), invItems.iteritems()))
                if len(addItems) or len(removeItems):
                    self.toggle(isOn = len(addItems))
                
        



class _CurVehiclePropTrigger(_Trigger):
    
    def run(self):
        self.isRunning = True
        if not self.isSubscribed:
            g_currentVehicle.onChanged += self._CurVehiclePropTrigger__cv_onChanged
            self.isSubscribed = True
        
        self.toggle(isOn = self.isOn())

    
    def clear(self):
        self.isRunning = False
        g_currentVehicle.onChanged -= self._CurVehiclePropTrigger__cv_onChanged
        self.isSubscribed = False

    
    def _CurVehiclePropTrigger__cv_onChanged(self):
        self.run()



class CurVehicleCrewTrigger(_CurVehiclePropTrigger):
    
    def isOn(self):
        return g_currentVehicle.isCrewFull()



class CurVehicleLockedTrigger(_CurVehiclePropTrigger):
    
    def isOn(self):
        isOn = False
        if g_currentVehicle.isPresent():
            isOn = g_currentVehicle.isLocked()
        
        return isOn



class CurrentVehicleTrigger(_TriggerWithValidateVar):
    
    def __init__(self, triggerID, validateVarID, setVarID = None, isLockedFlagID = None, isCrewFullFlagID = None):
        super(CurrentVehicleTrigger, self).__init__(triggerID, validateVarID, setVarID = setVarID)
        self._CurrentVehicleTrigger__isLockedFlagID = isLockedFlagID
        self._CurrentVehicleTrigger__isCrewFullFlagID = isCrewFullFlagID

    
    def run(self):
        self.isRunning = True
        if not self.isSubscribed:
            g_currentVehicle.onChanged += self._CurrentVehicleTrigger__cv_onChanged
            self.isSubscribed = True
        
        self._CurrentVehicleTrigger__checkCurrent()

    
    def isOn(self):
        (nationID, compTypeID) = g_currentVehicle.vehicle.descriptor.type.id
        vehIntCompDescr = vehicles.makeIntCompactDescrByID(ITEM_TYPE_NAMES[_VEHICLE], nationID, compTypeID)
        result = vehIntCompDescr in self.getIterVar()
        if result:
            pass
        1
        vehIntCompDescr(None)
        return result

    
    def clear(self):
        g_currentVehicle.onChanged -= self._CurrentVehicleTrigger__cv_onChanged
        self.isSubscribed = False
        self.isRunning = False

    
    def _CurrentVehicleTrigger__checkCurrent(self):
        isOn = False
        isLocked = False
        isCrewFull = False
        if g_currentVehicle.isPresent():
            isOn = self.isOn()
            isLocked = g_currentVehicle.isLocked()
            isCrewFull = g_currentVehicle.isCrewFull()
        
        self._setFlagValue(self._CurrentVehicleTrigger__isLockedFlagID, isLocked)
        self._setFlagValue(self._CurrentVehicleTrigger__isCrewFullFlagID, isCrewFull)
        self.toggle(isOn = isOn)

    
    def _CurrentVehicleTrigger__cv_onChanged(self):
        self._CurrentVehicleTrigger__checkCurrent()



class TankmanLevelTrigger(_Trigger):
    
    def __init__(self, triggerID, role, roleLevel, setVarID, inVehicleFlagID, specVehicleFlagID):
        super(TankmanLevelTrigger, self).__init__(triggerID)
        self._role = role
        self._roleLevel = roleLevel
        self._setVarID = setVarID
        self._inVehicleFlagID = inVehicleFlagID
        self._specVehicleFlagID = specVehicleFlagID

    
    def run(self):
        self.isRunning = True
        if not self.isSubscribed:
            g_clientUpdateManager.addCallbacks({
                'inventory.8': self.onTankmanChanged })
            g_currentVehicle.onChanged += self._TankmanLevelTrigger__cv_onChanged
            self.isSubscribed = True
        
        if not g_currentVehicle.isPresent():
            self.toggle(isOn = False)
            return None
        self._gui.showWaiting('request-tankman')
        BigWorld.player().inventory.getItems(_TANKMAN, self._TankmanLevelTrigger__cb_onGetItemsFromInventory)

    
    def isOn(self, tankman):
        if self._role == tankman.role:
            pass
        return self._roleLevel <= tankman.roleLevel

    
    def clear(self):
        g_clientUpdateManager.removeObjectCallbacks(self)
        g_currentVehicle.onChanged -= self._TankmanLevelTrigger__cv_onChanged
        self.isSubscribed = False
        self.isRunning = False

    
    def _TankmanLevelTrigger__cb_onGetItemsFromInventory(self, resultID, data):
        self._gui.hideWaiting('request-tankman')
        if resultID < RES_SUCCESS:
            LOG_ERROR('Server return error inventory {0:d} items request, responseCode='.format(_TANKMAN, resultID))
            self.isRunning = False
            return None
        current = g_currentVehicle.vehicle
        invID = current.inventoryId
        (nationID, compTypeID) = current.descriptor.type.id
        compDescrs = data.get('compDescr', { })
        vehs = data.get('vehicle', { })
        descrs = map((lambda item: (item[0], tankmen.TankmanDescr(item[1]))), compDescrs.iteritems())
        descrs = (None, resultID < RES_SUCCESS, filter)((lambda item: if not item[1].nationID == nationID and item[1].vehicleTypeID == compTypeID:
passself._specVehicleFlagID is not None), descrs)
        isOn = False
        inVehicle = False
        specVehicle = False
        for (idx, tankman) in descrs:
            if self.isOn(tankman) and not inVehicle:
                inVehicle = vehs.get(idx, -1) == invID
                if (tankman.vehicleTypeID != compTypeID or not inVehicle) and idx in vehs:
                    continue
                
                isOn = True
                specVehicle = True
                if self._setVarID is not None:
                    self._tutorial.getVars().set(self._setVarID, idx)
                
                if inVehicle:
                    break
                
        
        self._setFlagValue(self._inVehicleFlagID, inVehicle)
        self._setFlagValue(self._specVehicleFlagID, specVehicle)
        self.toggle(isOn = isOn)

    
    def onTankmanChanged(self, tankmen):
        if tankmen is not None:
            self.run()
        

    
    def _TankmanLevelTrigger__cv_onChanged(self):
        self.run()



class TankmanSkillTrigger(_TriggerWithValidateVar):
    
    def __init__(self, triggerID, validateVarID, setVarID = None):
        super(TankmanSkillTrigger, self).__init__(triggerID, validateVarID, setVarID = setVarID)

    
    def run(self):
        self.isRunning = True
        if not self.isSubscribed:
            g_clientUpdateManager.addCallbacks({
                'inventory.8': self.onTankmanChanged })
            g_currentVehicle.onChanged += self._TankmanSkillTrigger__cv_onChanged
            self.isSubscribed = True
        
        if not g_currentVehicle.isPresent():
            self.toggle(isOn = False)
            return None
        self._gui.showWaiting('request-tankman')
        BigWorld.player().inventory.getItems(_TANKMAN, self._TankmanSkillTrigger__cb_onGetItemsFromInventory)

    
    def isOn(self, tankmanDescr):
        if tankmanDescr is None:
            return False
        tankman = tankmen.TankmanDescr(tankmanDescr)
        result = len(tankman.skills) > 0
        if result:
            self.setVar(tankman.skills[0])
        
        return result

    
    def clear(self):
        g_clientUpdateManager.removeObjectCallbacks(self)
        g_currentVehicle.onChanged -= self._TankmanSkillTrigger__cv_onChanged
        self.isSubscribed = True
        self.isRunning = False

    
    def _TankmanSkillTrigger__cb_onGetItemsFromInventory(self, resultID, data):
        self._gui.hideWaiting('request-tankman')
        if resultID < RES_SUCCESS:
            LOG_ERROR('Server return error inventory {0:d} items request, responseCode='.format(_TANKMAN, resultID))
            self.isRunning = False
            return None
        self.toggle(isOn = self.isOn(data.get('compDescr', { }).get(self.getVar())))

    
    def onTankmanChanged(self, tankmen):
        if tankmen is not None:
            self.run()
        

    
    def _TankmanSkillTrigger__cv_onChanged(self):
        self.run()



class FreeVehicleSlotTrigger(_Trigger):
    
    def __init__(self, triggerID):
        super(FreeVehicleSlotTrigger, self).__init__(triggerID)
        self._slots = 0
        self._vehicles = 0

    
    def isOn(self):
        return self._slots > self._vehicles

    
    def clear(self):
        g_clientUpdateManager.removeObjectCallbacks(self)
        self.isSubscribed = False
        self.isRunning = False

    
    def run(self):
        self.isRunning = True
        if not self.isSubscribed:
            g_clientUpdateManager.addCallbacks({
                '': self.onClientUpdate })
            self.isSubscribed = True
        
        self._gui.showWaiting('request-slots')
        BigWorld.player().stats.get('slots', self._FreeVehicleSlotTrigger__cb_onSlotsReceived)

    
    def _FreeVehicleSlotTrigger__cb_onSlotsReceived(self, resultID, slots):
        self._gui.hideWaiting('request-slots')
        if resultID < 0:
            LOG_ERROR('Server return error credits request: ', resultID)
            self.isRunning = False
            return None
        self._slots = slots
        self._gui.showWaiting('request-inventory-items')
        BigWorld.player().inventory.getItems(_VEHICLE, self._FreeVehicleSlotTrigger__cb_onGetItemsFromInventory)

    
    def _FreeVehicleSlotTrigger__cb_onGetItemsFromInventory(self, resultID, data):
        self._gui.hideWaiting('request-inventory-items')
        if resultID < RES_SUCCESS:
            LOG_ERROR('Server return error inventory vehicles request, responseCode = {0:d}'.format(resultID))
            self.isRunning = False
            return None
        self._vehicles = len(data.get('compDescr', { }))
        self.toggle(isOn = self.isOn())

    
    def onClientUpdate(self, diff):
        slots = diff.get('stats', { }).get('slots')
        if slots is not None:
            self._slots = slots
        
        vehDiff = diff.get('inventory', { }).get(_VEHICLE, { }).get('compDescr')
        if vehDiff is not None:
            self._gui.showWaiting('request-inventory-items')
            BigWorld.player().inventory.getItems(_VEHICLE, self._FreeVehicleSlotTrigger__cb_onGetItemsFromInventory)
        else:
            self.toggle(isOn = self.isOn())



