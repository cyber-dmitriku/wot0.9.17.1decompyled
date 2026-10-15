# Source Generated with Decompyle++
# File: BaseTimedCustomizationInterface.pyc (Python 2.6)

import time
from abc import abstractmethod, ABCMeta
from datetime import timedelta
from math import ceil
from debug_utils import LOG_DEBUG
from helpers import i18n
from gui.Scaleform.customization.CustomizationInterface import CustomizationInterface
from gui.Scaleform.utils.HangarSpace import g_hangarSpace

class BaseTimedCustomizationInterface(CustomizationInterface):
    ZOOM_FACTOR = 0.2
    __metaclass__ = ABCMeta
    
    def __init__(self, name, nationId, position = -1):
        super(BaseTimedCustomizationInterface, self).__init__(name, nationId, position)
        self._currentItemID = None
        self._currentLifeCycle = None
        self._newItemID = None
        self._rentalPackageDP = None
        self._groupsDP = None
        self._itemsDP = None

    
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
        pass

    getItemPriceFactor = abstractmethod(getItemPriceFactor)
    
    def updateVehicleCustomization(self, itemID = None):
        pass

    updateVehicleCustomization = abstractmethod(updateVehicleCustomization)
    
    def fetchCurrentItem(self, vehDescr):
        pass

    fetchCurrentItem = abstractmethod(fetchCurrentItem)
    
    def change(self, vehInvID, section):
        pass

    change = abstractmethod(change)
    
    def drop(self, vehInvID, kind):
        pass

    drop = abstractmethod(drop)
    
    def update(self, vehDescr):
        pass

    update = abstractmethod(update)
    
    def getSlotsCount(self, descriptor, slotType):
        slots = descriptor.get('emblemSlots', [])
        continue
        resultingSlots = _[1]
        return len(resultingSlots)

    
    def populateUI(self, proxy):
        super(BaseTimedCustomizationInterface, self).populateUI(proxy)
        self._rentalPackageDP = self.getRentalPackagesDP()
        self._groupsDP = self.getGroupsDP()
        self._itemsDP = self.getItemsDP()
        self._rentalPackageDP.onDataInited += self._BaseTimedCustomizationInterface__onRentalPackagesDataInited
        self._rentalPackageDP.onRentalPackageChange += self._BaseTimedCustomizationInterface__handleRentalPackageChange
        self._rentalPackageDP.populateUI(proxy)
        self._groupsDP.populateUI(proxy)
        self._itemsDP.populateUI(proxy)

    
    def dispossessUI(self):
        if self._newItemID is not None:
            self.updateVehicleCustomization()
        
        self._rentalPackageDP.onDataInited -= self._BaseTimedCustomizationInterface__onRentalPackagesDataInited
        self._rentalPackageDP.onRentalPackageChange -= self._BaseTimedCustomizationInterface__handleRentalPackageChange
        self._rentalPackageDP.dispossessUI()
        self._groupsDP.dispossessUI()
        self._itemsDP.dispossessUI()
        self._rentalPackageDP = None
        self._groupsDP = None
        self._itemsDP = None
        self._eventManager.clear()
        LOG_DEBUG('BaseTimedCustomizationInterface dispossessUI', self._name)
        if g_hangarSpace.space is not None:
            g_hangarSpace.space.clearSelectedEmblemInfo()
        
        super(BaseTimedCustomizationInterface, self).dispossessUI()

    
    def invalidateData(self, vehType, refresh = False):
        if vehType is not None:
            self._groupsDP.buildList()
            self._itemsDP.setVehicleTypeParams(self.getItemPriceFactor(vehType), self._currentItemID)
        
        self._rentalPackageDP.getRentalPackages(refresh)

    
    def isNewItemSelected(self):
        return self._newItemID is not None

    
    def getSelectedItemCost(self):
        return self._itemsDP.getCost(self._newItemID)

    
    def getItemCost(self, itemId, priceIndex):
        packageCost = self._rentalPackageDP.requestItemAt(priceIndex)
        (cost, isGold) = self._itemsDP.getCostForPackagePrice(itemId, packageCost.get('cost', -1), packageCost.get('isGold', False))
        return {
            'cost': cost,
            'isGold': isGold }

    
    def isCurrentItemRemove(self):
        return self._currentItemID is not None

    
    def getCurrentItem(self):
        return self._itemsDP.makeItem(self._currentItemID, True, self._currentLifeCycle, self._BaseTimedCustomizationInterface__makeTimeLeftString())

    
    def onSetID(self, itemID, kind, packageIdx):
        if self._currentItemID == itemID:
            self._newItemID = None
        else:
            self._newItemID = itemID
        self.updateVehicleCustomization(itemID)

    
    def _BaseTimedCustomizationInterface__onRentalPackagesDataInited(self, selectedPackage, refresh):
        if selectedPackage:
            self._itemsDP.setDefaultCost(selectedPackage.get('cost'), selectedPackage.get('isGold'))
        
        if refresh:
            self._newItemID = None
            self._rentalPackageDP.refresh()
            self._itemsDP.refresh()
        
        LOG_DEBUG('BaseTimedCustomizationInterface data inited', self._name)
        self.onDataInited(self._name)

    
    def _BaseTimedCustomizationInterface__handleRentalPackageChange(self, index):
        item = self._rentalPackageDP.selectedPackage
        if not item is not None or item.get('cost') > -1:
            raise AssertionError
        self._itemsDP.setDefaultCost(item.get('cost'), item.get('isGold'))
        self._itemsDP.refresh()

    
    def _BaseTimedCustomizationInterface__makeTimeLeftString(self, **kwargs):
        if self._currentLifeCycle is None:
            return ''
        (startTime, days) = self._currentLifeCycle
        result = ''
        if days > 0:
            timeLeft = startTime + days * 86400 - time.time()
            if timeLeft > 0:
                delta = timedelta(0, timeLeft)
                if delta.days > 0:
                    if delta.seconds > 0:
                        pass
                    1
                    result = '#menu:customization/labels/timeLeft/days'(delta.days + 1, delta.days)
                else:
                    result = i18n.makeString('#menu:customization/labels/timeLeft/hours', ceil(delta.seconds / 3600))
            
        
        return result



