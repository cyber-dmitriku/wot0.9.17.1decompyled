# Source Generated with Decompyle++
# File: CurrentVehicle.pyc (Python 2.6)

import BigWorld
from items import vehicles
from AccountCommands import LOCK_REASON
from account_helpers.AccountSettings import AccountSettings
from account_helpers.AccountPrebattle import AccountPrebattle
from adisp import process, async
from Event import Event, EventManager
from gui.Scaleform.Waiting import Waiting
from debug_utils import LOG_DEBUG

class _CurrentVehicle(object):
    
    def __init__(self):
        self.firstTimeInitialized = False
        self._CurrentVehicle__eventManager = EventManager()
        self.onChanged = Event(self._CurrentVehicle__eventManager)
        self.onChanging = Event(self._CurrentVehicle__eventManager)
        self._CurrentVehicle__vehicle = None
        self._CurrentVehicle__changeCallbackID = None
        self._CurrentVehicle__clanLock = None

    
    def _CurrentVehicle__reset(self):
        self.firstTimeInitialized = False
        self._CurrentVehicle__vehicle = None

    
    def isVehicleTypeLocked(self):
        return self._CurrentVehicle__clanLock is not None

    
    def cleanup(self):
        self.reset(True)
        self._CurrentVehicle__eventManager.clear()

    
    def _CurrentVehicle__setVehicleToServer(self, id):
        AccountSettings.setFavorites('current', id)

    
    def __repr__(self):
        return 'CurrentVehicle(%s)' % str(self._CurrentVehicle__vehicle)

    
    def _CurrentVehicle__getVehicle(self):
        return self._CurrentVehicle__vehicle

    
    def _CurrentVehicle__setVehicle(self, newVehicle):
        self._CurrentVehicle__request(newVehicle.inventoryId)
        g_currentVehicle.onChanging()

    
    def setVehicleById(self, id):
        self._CurrentVehicle__request(id)

    vehicle = property(_CurrentVehicle__getVehicle, _CurrentVehicle__setVehicle)
    
    def _CurrentVehicle__getRepairCost(self):
        return self._CurrentVehicle__vehicle.repairCost

    
    def _CurrentVehicle__setRepairCost(self, newValue):
        if self._CurrentVehicle__vehicle.repairCost != newValue:
            self._CurrentVehicle__vehicle.repairCost = newValue
            self.onChanged()
        

    repairCost = property(_CurrentVehicle__getRepairCost, _CurrentVehicle__setRepairCost)
    
    def isBroken(self):
        return self._CurrentVehicle__vehicle.repairCost > 0

    
    def setLocked(self, newValue):
        if self._CurrentVehicle__vehicle.lock != newValue:
            self._CurrentVehicle__vehicle.lock = newValue
            self.onChanged()
        

    
    def isCrewFull(self):
        if self.isPresent() and None not in self._CurrentVehicle__vehicle.crew:
            pass
        return self._CurrentVehicle__vehicle.crew != []

    
    def isInBattle(self):
        return self._CurrentVehicle__vehicle.lock == LOCK_REASON.ON_ARENA

    
    def isInHangar(self):
        if self.isPresent():
            pass
        return not self.isInBattle()

    
    def isAwaitingBattle(self):
        return self._CurrentVehicle__vehicle.lock == LOCK_REASON.IN_QUEUE

    
    def isLocked(self):
        return self._CurrentVehicle__vehicle.lock != LOCK_REASON.NONE

    
    def isAlive(self):
        if self.isPresent() and not self.isBroken():
            pass
        return not self.isLocked()

    
    def isReadyToFight(self):
        isBS = AccountPrebattle.isBattleSession()
        isBSVehicleLockMode = AccountPrebattle.getSettings().get('vehicleLockMode', False)
        isCurrentVehicleTypeLocked = self.isVehicleTypeLocked()
        if self.isAlive() and self.isCrewFull():
            if not isBS and isBSVehicleLockMode or not isCurrentVehicleTypeLocked:
                if not isBS or not isBSVehicleLockMode:
                    pass
        return not isBS

    
    def isPresent(self):
        return self._CurrentVehicle__vehicle is not None

    
    def getState(self):
        if not self.isInHangar():
            return None
        return self.vehicle.getState()

    
    def getHangarMessage(self):
        InventoryVehicle = InventoryVehicle
        import gui.Scaleform.utils.gui_items
        if self.vehicle is None:
            return ('#menu:currentVehicleStatus/notpresent', InventoryVehicle.STATE_LEVEL.CRITICAL)
        return ('#menu:currentVehicleStatus/' + self._CurrentVehicle__vehicle.getState(), self._CurrentVehicle__vehicle.getStateLevel())

    
    def getReadyMessage(self):
        return self.getHangarMessage()

    
    def reset(self, silent = False):
        self._CurrentVehicle__reset()
        if not silent:
            self.onChanged()
        

    
    def __request(self, inventoryId):
        Waiting.show('updateCurrentVehicle', True)
        Requester = Requester
        StatsRequester = StatsRequester
        import gui.Scaleform.utils.requesters
        yield Requester('vehicle').getFromInventory()
        vehicles = None
        yield StatsRequester().getVehicleTypeLocks()
        vehicleTypeLocks = None
        yield StatsRequester().getGlobalVehicleLocks()
        globalVehicleLocks = None
        old = self._CurrentVehicle__vehicle
        self._CurrentVehicle__vehicle = self._CurrentVehicle__findCurrent(inventoryId, vehicles)
        if self._CurrentVehicle__vehicle and self._CurrentVehicle__vehicle != old:
            self._CurrentVehicle__setVehicleToServer(self._CurrentVehicle__vehicle.inventoryId)
        
        self._CurrentVehicle__clanLock = None
        if g_currentVehicle.isPresent():
            clanDamageLock = vehicleTypeLocks.get(self._CurrentVehicle__vehicle.descriptor.type.compactDescr, { }).get(1, None)
            clanNewbeLock = globalVehicleLocks.get(1, None)
            if not clanDamageLock:
                pass
            self._CurrentVehicle__clanLock = clanNewbeLock
        
        if not self._CurrentVehicle__changeCallbackID:
            self._CurrentVehicle__changeCallbackID = BigWorld.callback(0.1, self._CurrentVehicle__changeDone)
        

    _CurrentVehicle__request = process(__request)
    
    def _CurrentVehicle__changeDone(self):
        self._CurrentVehicle__changeCallbackID = None
        player = BigWorld.player()
        if player and hasattr(player, 'isPlayer') and player.isPlayer:
            self.onChanged()
        
        Waiting.hide('updateCurrentVehicle')

    
    def _CurrentVehicle__findCurrent(self, inventoryId, vehicles):
        for vehicle in vehicles:
            if vehicle.inventoryId == inventoryId:
                return vehicle
        
        vehicles.sort()
        if len(vehicles):
            return vehicles[0]

    
    def update(self):
        if self.firstTimeInitialized:
            if self._CurrentVehicle__vehicle:
                pass
            1
            self._CurrentVehicle__vehicle.inventoryId(None)
        

    
    def getFromServer(self, callback):
        currentId = AccountSettings.getFavorites('current')
        Requester = Requester
        import gui.Scaleform.utils.requesters
        yield Requester('vehicle').getFromInventory()
        vehiclesList = None
        prebattle = AccountPrebattle.get()
        if prebattle is not None:
            for (rId, roster) in prebattle.rosters.iteritems():
                if BigWorld.player().id in roster:
                    vehCompDescr = roster[BigWorld.player().id].get('vehCompDescr')
                    if len(vehCompDescr):
                        vehDescr = vehicles.VehicleDescr(compactDescr = vehCompDescr)
                        for v in vehiclesList:
                            if v.descriptor.type.id == vehDescr.type.id:
                                currentId = v.inventoryId
                                break
                                continue
                        
                    
                len(vehCompDescr)
            
        
        self._CurrentVehicle__vehicle = self._CurrentVehicle__findCurrent(currentId, vehiclesList)
        self.onChanged()
        self.firstTimeInitialized = True
        callback(True)

    getFromServer = async(process(getFromServer))
    
    def getParams(self):
        ItemsParameters = ItemsParameters
        import gui.Scaleform.utils
        data = list()
        if self.isPresent():
            params = ItemsParameters.g_instance.getParameters(g_currentVehicle.vehicle)
            if params is not None:
                for p in params:
                    data.append(p[0])
                    data.append(p[1])
                
            
        
        return data


g_currentVehicle = _CurrentVehicle()

