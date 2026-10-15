# Source Generated with Decompyle++
# File: EmblemInterface.pyc (Python 2.6)

import BigWorld
from abc import abstractmethod, ABCMeta
import time
from CurrentVehicle import g_currentVehicle
from debug_utils import LOG_DEBUG
from gui import SystemMessages
from gui.Scaleform.customization.BaseTimedCustomizationInterface import BaseTimedCustomizationInterface
from gui.Scaleform.customization.VehicleCustonizationModel import VehicleCustomizationModel
from gui.Scaleform.customization.data_providers import EmblemsLeftDataProvider, EmblemsRightDataProvider, EmblemLeftGroupsDataProvider, EmblemLeftRentalPackageDataProvider, EmblemRightRentalPackageDataProvider, EmblemRightGroupsDataProvider
from gui.Scaleform.utils.HangarSpace import g_hangarSpace
from helpers import time_utils, i18n

class EmblemInterface(BaseTimedCustomizationInterface):
    __metaclass__ = ABCMeta
    
    def __init__(self, name, nationId, position):
        super(EmblemInterface, self).__init__(name, nationId, position)
        self.defaultPlayerEmblemID = None
        self.isTurret = False
        self._isEnabled = False
        self._vehicleLevel = 1
        self._positionShift = 0

    
    def __del__(self):
        LOG_DEBUG('EmblemInterface deleted')

    
    def getCurrentItem(self):
        self.locateCameraOnSlot()
        item = super(EmblemInterface, self).getCurrentItem()
        if self.defaultPlayerEmblemID == item.get('id'):
            item['canDrop'] = False
        
        return item

    
    def isEnabled(self):
        return self._isEnabled

    
    def locateCameraOnSlot(self):
        res = g_hangarSpace.space.locateCameraOnEmblem(not (self.isTurret), 'player', self._position - self._positionShift, self.ZOOM_FACTOR)
        LOG_DEBUG('EmblemLeftInterface g_hangarSpace.space.locateCameraOnEmblem', self._position, res)

    
    def getRealPosition(self):
        if not self.isTurret:
            return self._position - self._positionShift
        return self._position + 2

    
    def getRentalPackagesDP(self):
        pass

    getRentalPackagesDP = abstractmethod(getRentalPackagesDP)
    
    def getGroupsDP(self):
        pass

    getGroupsDP = abstractmethod(getGroupsDP)
    
    def getItemsDP(self):
        pass

    getItemsDP = abstractmethod(getItemsDP)
    
    def getItemPriceFactor(self, vehType):
        return self._vehicleLevel

    
    def updateVehicleCustomization(self, itemID = None):
        space = g_hangarSpace.space
        if space is not None and g_currentVehicle.isInHangar():
            VehicleCustomizationModel.updateVehicleSticker('player', itemID, self.getRealPosition(), self._rentalPackageDP.selectedPackage.get('periodDays'))
            space.updateVehicleSticker(VehicleCustomizationModel.getVehicleModel())
        

    
    def fetchCurrentItem(self, vehDescr):
        if vehDescr is not None:
            self._vehicleLevel = vehDescr.type.level
            slotsCount = self.getSlotsCount(vehDescr.turret, 'player')
            self.isTurret = slotsCount > self._position
            if self._position == 1 and slotsCount == 1:
                self._positionShift = 1
            
            if not self.isTurret:
                slotsCount += self.getSlotsCount(vehDescr.hull, 'player')
            
            self._isEnabled = slotsCount > self._position
            self.defaultPlayerEmblemID = vehDescr.type.defaultPlayerEmblemID
            emblem = vehDescr.playerEmblems[self.getRealPosition()]
            if emblem is not None:
                (self._currentItemID, startTime, days) = emblem
                startTime = time_utils.makeLocalServerTime(startTime)
                self._currentLifeCycle = (startTime, days)
            
        

    
    def change(self, vehInvID, section):
        if self._newItemID is None:
            message = i18n.makeString('#system_messages:customization/emblem_not_selected')
            self.onCustomizationChangeFailed(message)
            return None
        if self._rentalPackageDP.selectedPackage is None:
            message = i18n.makeString('#system_messages:customization/emblem_days_not_selected')
            self.onCustomizationChangeFailed(message)
            return None
        (cost, isGold) = self._itemsDP.getCost(self._newItemID)
        if cost < 0:
            message = i18n.makeString('#system_messages:customization/emblem_cost_not_found')
            self.onCustomizationChangeFailed(message)
            return None
        self._rentalPackageDP.selectedPackage is None(cost < 0, BigWorld.player().inventory.changeVehicleEmblem, vehInvID, (self.getRealPosition(), self._newItemID, self._rentalPackageDP.selectedPackage.get('periodDays')), (lambda resultID: self._EmblemInterface__onChangeVehicleEmblem(resultID, (cost, isGold))))

    
    def drop(self, vehInvID, kind):
        if self._currentItemID is None:
            message = i18n.makeString('#system_messages:customization/emblem_not_found_to_drop')
            self.onCustomizationDropFailed(message)
            return None
        BigWorld.player().inventory.changeVehicleEmblem(vehInvID, self.getRealPosition(), 0, 0, self._EmblemInterface__onDropVehicleEmblem)

    
    def update(self, vehicleDescr):
        emblem = vehicleDescr.playerEmblems[self.getRealPosition()]
        if emblem is not None:
            pass
        1
        emblemID = None
        if emblemID != self._currentItemID:
            self._currentItemID = emblemID
            self._itemsDP.currentItemID = self._currentItemID
            if emblem is not None:
                (_, startTime, days) = emblem
                startTime = time_utils.makeLocalServerTime(startTime)
                self._currentLifeCycle = (startTime, days)
            else:
                self._currentLifeCycle = None
            self.onCurrentItemChange(self._name)
        

    
    def populateUI(self, proxy):
        super(EmblemInterface, self).populateUI(proxy)

    
    def dispossessUI(self):
        super(EmblemInterface, self).dispossessUI()

    
    def _EmblemInterface__onChangeVehicleEmblem(self, resultID, price):
        if resultID < 0:
            message = i18n.makeString('#system_messages:customization/emblem_change_server_error')
            self.onCustomizationChangeFailed(message)
            return None
        self._currentItemID = self._newItemID
        self._currentLifeCycle = (round(time.time()), 0)
        self._newItemID = None
        self._itemsDP.currentItemID = self._currentItemID
        (cost, isGold) = price
        if isGold:
            key = '#system_messages:customization/emblem_change_success/gold'
            fCost = BigWorld.wg_getGoldFormat(cost)
            type = SystemMessages.SM_TYPE.CustomizationForGold
        else:
            key = '#system_messages:customization/emblem_change_success/credits'
            fCost = BigWorld.wg_getIntegralFormat(cost)
            type = SystemMessages.SM_TYPE.CustomizationForCredits
        self.onCustomizationChangeSuccess(i18n.makeString(key, fCost), type)

    
    def _EmblemInterface__onDropVehicleEmblem(self, resultID):
        if resultID < 0:
            message = i18n.makeString('#system_messages:customization/emblem_drop_server_error')
            self.onCustomizationDropFailed(message)
            return None
        self._currentItemID = self.defaultPlayerEmblemID
        self._currentLifeCycle = None
        self._itemsDP.currentItemID = self.defaultPlayerEmblemID
        if self._newItemID is None:
            g_currentVehicle.update()
        
        message = i18n.makeString('#system_messages:customization/emblem_drop_success')
        self.onCustomizationDropSuccess(message)
        self.onCurrentItemChange(self._name)



class EmblemLeftInterface(EmblemInterface):
    
    def getItemsDP(self):
        return EmblemsLeftDataProvider()

    
    def getRentalPackagesDP(self):
        return EmblemLeftRentalPackageDataProvider(self._nationID)

    
    def getGroupsDP(self):
        return EmblemLeftGroupsDataProvider()



class EmblemRightInterface(EmblemInterface):
    
    def getItemsDP(self):
        return EmblemsRightDataProvider()

    
    def getRentalPackagesDP(self):
        return EmblemRightRentalPackageDataProvider(self._nationID)

    
    def getGroupsDP(self):
        return EmblemRightGroupsDataProvider()



