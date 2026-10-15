# Source Generated with Decompyle++
# File: TechnicalMaintenance.pyc (Python 2.6)

__author__ = 'i_maliavko'
from windows import UIInterface
from adisp import process
from helpers.i18n import makeString
from AccountCommands import LOCK_REASON
from CurrentVehicle import g_currentVehicle
from debug_utils import *
from gui import SystemMessages
from gui.Scaleform.Waiting import Waiting
from gui.Scaleform.utils.functions import getShortDescr, isModuleFitVehicle
from gui.Scaleform.utils.gui_items import VehicleItem, InventoryItem, getVehicleFullName, compactItem, getItemByCompact
from gui.Scaleform.utils.requesters import StatsRequester, Requester, VehicleItemsRequester, AvailableItemsRequester

class TechnicalMaintenance(UIInterface):
    
    def __init__(self):
        UIInterface.__init__(self)

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self.uiHolder.addExternalCallbacks({
            'techMaintenance.repair': self.onRepair,
            'techMaintenance.setRefillSettings': self.onSetRefillSettings,
            'techMaintenance.populateEqs': self.onPopulateTechnicalMaintenanceEquipments,
            'techMaintenance.populate': self.onPopulateTechnicalMaintenance,
            'techMaintenance.fillVehicle': self.onFillTechnicalMaintenance })

    
    def dispossessUI(self):
        self.uiHolder.removeExternalCallbacks('techMaintenance.populate', 'techMaintenance.populateEqs', 'techMaintenance.setRefillSettings', 'techMaintenance.repair', 'techMaintenance.fillVehicle')
        UIInterface.dispossessUI(self)

    
    def onPopulateTechnicalMaintenance(self, callbackId):
        Waiting.show('techMaintenance')
        yield StatsRequester().getGold()
        gold = None
        yield StatsRequester().getCredits()
        credits = None
        params = [
            gold,
            credits]
        if g_currentVehicle.isPresent():
            yield Requester('vehicle').getFromInventory()
            iVehicles = None
            for v in iVehicles:
                if v.inventoryId == g_currentVehicle.vehicle.inventoryId:
                    vehicle = v
                    continue
            
            params.append(vehicle.pack())
            params.append(getVehicleFullName())
            params.append(vehicle.repairCost)
            params.append(vehicle.descriptor.getMaxRepairCost())
            params.append(vehicle.isAutoRepair)
            gun = VehicleItem(vehicle.descriptor.gun)
            yield Requester('shell').getFromInventory()
            iAmmo = None
            yield Requester('shell').getFromShop()
            sAmmo = None
            totalPrice = {
                'credits': 0,
                'gold': 0 }
            params.append(gun.descriptor['maxAmmo'])
            params.append(vehicle.lock != LOCK_REASON.NONE)
            params.append(vehicle.repairCost > 0)
            casseteCount = vehicle.descriptor.gun['clip'][0]
            params.append(casseteCount)
            if casseteCount == 1:
                pass
            1
            ''(makeString('#menu:technicalMaintenance/ammoTitleEx') % casseteCount)
            params.append(len(vehicle.shells))
            for shell in vehicle.shells:
                if shell in sAmmo:
                    pass
                1
                shopShell = None
                if shopShell:
                    if shell in iAmmo:
                        pass
                    1
                    iCount = 0
                    if shell is not shopShell:
                        yield shopShell.getPrice()
                    
                    sPrice = (0, 0)
                    shellParams = shopShell.getParams(vehicle)
                    buyCount = max(shell.default - iCount - shell.count, 0)
                    params.append(compactItem(shopShell))
                    params.append(shell.type)
                    params.append('../maps/icons/ammopanel/ammo/%s' % shell.descriptor['icon'][0])
                    params.append(shell.count)
                    params.append(shell.default)
               
