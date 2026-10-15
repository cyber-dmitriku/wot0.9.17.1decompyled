# Source Generated with Decompyle++
# File: InscriptionInterface.pyc (Python 2.6)

import BigWorld
from abc import abstractmethod, ABCMeta
from CurrentVehicle import g_currentVehicle
from debug_utils import LOG_DEBUG
from gui import SystemMessages
from gui.Scaleform.customization.BaseTimedCustomizationInterface import BaseTimedCustomizationInterface
from gui.Scaleform.customization.VehicleCustonizationModel import VehicleCustomizationModel
from gui.Scaleform.customization.data_providers import InscriptionLeftDataProvider, InscriptionRightDataProvider, InscriptionLeftRentalPackageDataProvider, InscriptionLeftGroupsDataProvider, InscriptionRightRentalPackageDataProvider, InscriptionRightGroupsDataProvider
from gui.Scaleform.utils.HangarSpace import g_hangarSpace
from helpers import time_utils, i18n

class InscriptionInterface(BaseTimedCustomizationInterface):
    __metaclass__ = ABCMeta
    
    def __init__(self, name, nationId, position):
        super(InscriptionInterface, self).__init__(name, nationId, position)
        self.isTurret = False
        self._isEnabled = False
        self._vehicleLevel = 1
        self._positionShift = 0

    
    def __del__(self):
        LOG_DEBUG('InscriptionInterface deleted')

    
    def getCurrentItem(self):
        self.locateCameraOnSlot()
        return super(InscriptionInterface, self).getCurrentItem()

    
    def isEnabled(self):
        return self._isEnabled

    
    def locateCameraOnSlot(self):
        res = g_hangarSpace.space.locateCameraOnEmblem(not (self.isTurret), 'inscription', self._position - self._positionShift, self.ZOOM_FACTOR)

    
    def getRealPosition(self):
        if not self.isTurret:
            return self._position - self._positionShift
        return 2 + self._position

    
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
            VehicleCustomizationModel.updateVehicleSticker('inscription', itemID, self.getRealPosition(), self._rentalPackageDP.selectedPackage.get('periodDays'))
            space.updateVehicleSticker(VehicleCustomizationModel.getVehicleModel())
        

    
    def fetchCurrentItem(self, vehDescr):
        if vehDescr is not None:
            self._vehicleLevel = vehDescr.type.level
            slotsCount = self.getSlotsCount(vehDescr.turret, 'inscription')
            self.isTurret = slotsCount > self._position
            if self._position == 1 and slotsCount == 1:
                self._positionShift = 1
            
            if not self.isTurret:
                slotsCount += self.getSlotsCount(vehDescr.hull, 'inscription')
            
            self._isEnabled = slotsCount > self._position
            inscription = vehDescr.playerInscriptions[self.getRealPosition()]
            if inscription is not None and inscription[0] is not None:
                (self._currentItemID, startTime, days, _) = inscription
                startTime = time_utils.makeLocalServerTime(startTime)
                self._currentLifeCycle = (startTime, days)
            
        

    
    def change(self, vehInvID, section):
        if self._newItemID is None:
            message = i18n.makeString('#system_messages:customization/inscription_not_selected')
            self.onCustomizationChangeFailed(message)
            return None
        if self._rentalPackageDP.selectedPackage is None:
            message = i18n.makeString('#system_messages:customization/inscription_days_not_selected')
            self.onCustomizationChangeFailed(message)
            return None
        (cost, isGold) = self._itemsDP.getCost(self._newItemID)
        if cost < 0:
            message = i18n.makeString('#system_messages:customization/inscription_cost_not_found')
            self.onCustomizationChangeFailed(message)
            return None
        self._rentalPackageDP.selectedPackage is None(cost < 0, BigWorld.player().inventory.changeVehicleInscription, vehInvID, self.getRealPosition(), (self._newItemID, self._rentalPackageDP.selectedPackage.get('periodDays'), 1), (lambda resultID: self._InscriptionInterface__onChangeVehicleInscription(resultID, (cost, isGold))))

    
    def drop(self, vehInvID, kind):
        if self._currentItemID is None:
            message = i18n.makeString('#system_messages:customization/inscription_not_found_to_drop')
            self.onCustomizationDropFailed(message)
            return None
        BigWorld.player().inventory.changeVehicleInscription(vehInvID, self.getRealPosition(), 0, 0, 1, self._InscriptionInterface__onDropVehicleInscription)

    
    def update(self, vehicleDescr):
        inscription = vehicleDescr.playerInscriptions[self.getRealPosition()]
        if inscription is not None:
            pass
        1
        inscriptionID = None
        if inscriptionID != self._currentItemID:
            self._currentItemID = inscriptionID
            self._itemsDP.currentItemID = self._currentItemID
            if inscription is not None:
                (_, startTime, days, colorId) = inscription
                startTime = time_utils.makeLocalServerTime(startTime)
                self._currentLifeCycle = (startTime, days)
            else:
                self._currentLifeCycle = None
            self.onCurrentItemChange(self._name)
        

    
    def populateUI(self, proxy):
        super(InscriptionInterface, self).populateUI(proxy)

    
    def dispossessUI(self):
        super(InscriptionInterface, self).dispossessUI()

    
    def _InscriptionInterface__onChangeVehicleInscription(self, resultID, price):
        if resultID < 0:
            message = i18n.makeString('#system_messages:customization/inscription_change_server_error')
            self.onCustomizationChangeFailed(message)
            return None
        self._currentItemID = self._newItemID
        self._currentLifeCycle = None
        self._newItemID = None
        self._itemsDP.currentItemID = self._currentItemID
        (cost, isGold) = price
        if isGold:
            key = '#system_messages:customization/inscription_change_success/gold'
            fCost = BigWorld.wg_getGoldFormat(cost)
            type = SystemMessages.SM_TYPE.CustomizationForGold
        else:
            key = '#system_messages:customization/inscription_change_success/credits'
            fCost = BigWorld.wg_getIntegralFormat(cost)
            type = SystemMessages.SM_TYPE.CustomizationForCredits
        self.onCustomizationChangeSuccess(i18n.makeString(key, fCost), type)

    
    def _InscriptionInterface__onDropVehicleInscription(self, resultID):
        if resultID < 0:
            message = i18n.makeString('#system_messages:customization/inscription_drop_server_error')
            self.onCustomizationDropFailed(message)
            return None
        self._currentItemID = None
        self._currentLifeCycle = None
        self._itemsDP.currentItemID = None
        if self._newItemID is None:
            g_currentVehicle.update()
        
        message = i18n.makeString('#system_messages:customization/inscription_drop_success')
        self.onCustomizationDropSuccess(message)



class InscriptionLeftInterface(InscriptionInterface):
    
    def getItemsDP(self):
        return InscriptionLeftDataProvider(self._nationID)

    
    def getRentalPackagesDP(self):
        return InscriptionLeftRentalPackageDataProvider(self._nationID)

    
    def getGroupsDP(self):
        return InscriptionLeftGroupsDataProvider(self._nationID)



class InscriptionRightInterface(InscriptionInterface):
    
    def getItemsDP(self):
        return InscriptionRightDataProvider(self._nationID)

    
    def getRentalPackagesDP(self):
        return InscriptionRightRentalPackageDataProvider(self._nationID)

    
    def getGroupsDP(self):
        return InscriptionRightGroupsDataProvider(self._nationID)



