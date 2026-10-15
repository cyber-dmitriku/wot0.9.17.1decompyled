# Source Generated with Decompyle++
# File: CamouflageInterface.pyc (Python 2.6)

import BigWorld
import functools
from datetime import timedelta
from math import ceil
import time
from CurrentVehicle import g_currentVehicle
from debug_utils import LOG_DEBUG
from gui import SystemMessages, g_tankActiveCamouflage
from gui.Scaleform.customization.BaseTimedCustomizationInterface import BaseTimedCustomizationInterface
from gui.Scaleform.customization.data_providers import CamouflageGroupsDataProvider, CamouflagesDataProvider, CamouflageRentalPackageDataProvider
from gui.Scaleform.utils.HangarSpace import g_hangarSpace
from helpers import i18n, time_utils
from items.vehicles import CAMOUFLAGE_KINDS

class CamouflageInterface(BaseTimedCustomizationInterface):
    
    def __init__(self, name, nationId, position):
        super(CamouflageInterface, self).__init__(name, nationId, position)
        self.currentItemsByKind = { }
        self.indexToKind = { }
        self.resetCurrentItems()

    
    def resetCurrentItems(self):
        for (k, v) in CAMOUFLAGE_KINDS.iteritems():
            self.setCurrentItem(v, None, None, None, None)
            self.indexToKind[v] = k
        

    
    def setCurrentItem(self, kindIdx, ID, lifeCycle, newItemID, packageIdx):
        self.currentItemsByKind[kindIdx] = {
            'id': ID,
            'lifeCycle': lifeCycle,
            'newItemID': newItemID,
            'packageIdx': packageIdx }

    
    def __del__(self):
        LOG_DEBUG('CamouflageInterface deleted')

    
    def getRentalPackagesDP(self):
        return CamouflageRentalPackageDataProvider(self._nationID)

    
    def getGroupsDP(self):
        return CamouflageGroupsDataProvider(self._nationID)

    
    def getItemsDP(self):
        return CamouflagesDataProvider(self._nationID)

    
    def getItemPriceFactor(self, vehType):
        return vehType.camouflagePriceFactor

    
    def invalidateData(self, vehType, refresh = False):
        if vehType is not None:
            self._groupsDP.buildList()
            self._itemsDP.setVehicleTypeParams(self.getItemPriceFactor(vehType), self.currentItemsByKind.get(0, {
                'id': None }).get('id'))
        
        self._rentalPackageDP.getRentalPackages(refresh)

    
    def isNewItemSelected(self):
        return self.getSelectedItemsCount() > 0

    
    def getSelectedItemCost(self):
        continue
        newItemsCosts = _[1]
        return newItemsCosts

    
    def getSelectedItemsCount(self):
        continue
        newItems = _[1]
        return len(newItems)

    
    def isCurrentItemRemove(self):
        continue
        currentItems = _[1]
        return len(currentItems) > 0

    
    def getCurrentItem(self):
        space = g_hangarSpace.space
        if space is not None:
            space.locateCameraToPreview()
            space.clearSelectedEmblemInfo()
        
        items = []
        for (key, item) in self.currentItemsByKind.iteritems():
            items.append(self._itemsDP.makeItem(item.get('id'), True, item.get('lifeCycle'), self._CamouflageInterface__makeTimeLeftString(item = item), key))
        
        return items

    
    def onSetID(self, itemID, kind, packageIdx):
        item = self.currentItemsByKind.get(kind)
        if item.get('id') == itemID:
            item['newItemID'] = None
        else:
            item['newItemID'] = itemID
        item['packageIdx'] = packageIdx
        self.updateVehicleCustomization(itemID)

    
    def _CamouflageInterface__onRentalPackagesDataInited(self, selectedPackage, refresh):
        if selectedPackage:
            self._itemsDP.setDefaultCost(selectedPackage.get('cost'), selectedPackage.get('isGold'))
        
        if refresh:
            for (kind, item) in self.currentItemsByKind.iteritems():
                item['newItemID'] = None
            
            self._rentalPackageDP.refresh()
            self._itemsDP.refresh()
        
        LOG_DEBUG('CamouflageInterface data inited', self._name)
        self.onDataInited(self._name)

    
    def _CamouflageInterface__makeTimeLeftString(self, **kwargs):
        result = ''
        item = kwargs.get('item')
        if item.get('lifeCycle') is not None:
            (startTime, days) = item.get('lifeCycle')
            if days > 0:
                timeLeft = startTime + days * 86400 - time.time()
                if timeLeft > 0:
                    delta = timedelta(0, timeLeft)
                    if delta.days > 0:
                        if delta.seconds > 0:
                            pass
                        1
                        result = '#menu:customization/labels/camouflage/timeLeft/days'(delta.days + 1, delta.days)
                    else:
                        result = i18n.makeString('#menu:customization/labels/camouflage/timeLeft/hours', ceil(delta.seconds / 3600))
                
            
        
        return result

    
    def updateVehicleCustomization(self, itemID = None):
        space = g_hangarSpace.space
        if space is not None and g_currentVehicle.isInHangar():
            space.updateVehicleCamouflage(camouflageID = itemID)
        

    
    def fetchCurrentItem(self, vehDescr):
        if vehDescr is not None:
            camouflages = vehDescr.camouflages
            if camouflages is not None:
                for camouflage in camouflages:
                    (itemId, startTime, days) = camouflage
                    if itemId is not None:
                        if itemId is None:
                            pass
                        1
                        lifeCycle = (time_utils.makeLocalServerTime(startTime), days)
                        camouflageObject = self._itemsDP.getCamouflageDescr(itemId)
                        self.setCurrentItem(camouflageObject.get('kind'), itemId, lifeCycle, None, self._rentalPackageDP.getIndexByDays(days))
                        continue
                
            
        

    
    def change(self, vehInvID, section):
        if self._rentalPackageDP.selectedPackage is None:
            message = i18n.makeString('#system_messages:customization/camouflage_days_not_selected')
            self.onCustomizationChangeFailed(message)
            return None
        isNewItemFound = False
        for (kind, item) in self.currentItemsByKind.iteritems():
            if item.get('newItemID', None) is None:
                continue
            elif not isNewItemFound:
                isNewItemFound = True
            
            price = self.getItemCost(item.get('newItemID'), item.get('packageIdx'))
            if price.get('cost') < 0:
                message = i18n.makeString('#system_messages:customization/camouflage_cost_not_found')
                self.onCustomizationChangeFailed(message)
                return None
            localKind = kind
            pricePackage = self._rentalPackageDP.requestItemAt(item.get('packageIdx'))
            BigWorld.player().inventory.changeVehicleCamouflage(vehInvID, localKind, item.get('newItemID'), pricePackage.get('periodDays'), functools.partial(self._CamouflageInterface__onChangeVehicleCamouflage, (price.get('cost'), price.get('isGold')), localKind))
        
        if not isNewItemFound:
            message = i18n.makeString('#system_messages:customization/camouflage_not_selected')
            self.onCustomizationChangeFailed(message)
        

    
    def drop(self, vehInvID, kind):
        if self.currentItemsByKind.get(kind) is None:
            message = i18n.makeString('#system_messages:customization/camouflage_not_found_to_drop')
            self.onCustomizationDropFailed(message)
            return None
        self.currentItemsByKind.get(kind) is None(BigWorld.player().inventory.changeVehicleCamouflage, vehInvID, kind, (0, 0), (lambda resultID: self._CamouflageInterface__onDropVehicleCamouflage(resultID, kind)))

    
    def update(self, vehicleDescr):
        camouflages = vehicleDescr.camouflages
        isUpdated = False
        for (index, camouflage) in enumerate(camouflages):
            if camouflage is not None:
                pass
            1
            camouflageID = None
            item = self.currentItemsByKind[index]
            if camouflageID != item.get('id'):
                isUpdated = True
                item['id'] = camouflageID
                if camouflage is not None:
                    (_, startTime, days) = camouflage
                    startTime = time_utils.makeLocalServerTime(startTime)
                    item['lifeCycle'] = (startTime, days)
                else:
                    item['lifeCycle'] = None
                if CAMOUFLAGE_KINDS.get(self._itemsDP.currentGroup) == index:
                    self._itemsDP.currentItemID = item['id']
                
            CAMOUFLAGE_KINDS.get(self._itemsDP.currentGroup) == index
        
        if isUpdated:
            self.onCurrentItemChange(self._name)
        

    
    def populateUI(self, proxy):
        super(CamouflageInterface, self).populateUI(proxy)

    
    def dispossessUI(self):
        self.resetCurrentItems()
        super(CamouflageInterface, self).dispossessUI()

    
    def _CamouflageInterface__onChangeVehicleCamouflage(self, price, kind, resultID):
        if resultID < 0:
            message = i18n.makeString('#system_messages:customization/camouflage_change_server_error')
            self.onCustomizationChangeFailed(message)
            return None
        item = self.currentItemsByKind.get(kind)
        g_tankActiveCamouflage[g_currentVehicle.vehicle.descriptor.type.compactDescr] = kind
        item['id'] = item.get('newItemID')
        item['lifeCycle'] = None
        item['newItemID'] = None
        if CAMOUFLAGE_KINDS.get(self._itemsDP.currentGroup) == kind:
            self._itemsDP.currentItemID = item['id']
        
        (cost, isGold) = price
        if isGold:
            key = '#system_messages:customization/camouflage_change_success/gold'
            fCost = BigWorld.wg_getGoldFormat(cost)
            type = SystemMessages.SM_TYPE.CustomizationForGold
        else:
            key = '#system_messages:customization/camouflage_change_success/credits'
            fCost = BigWorld.wg_getIntegralFormat(cost)
            type = SystemMessages.SM_TYPE.CustomizationForCredits
        self.onCustomizationChangeSuccess(i18n.makeString(key, fCost), type)

    
    def _CamouflageInterface__onDropVehicleCamouflage(self, resultID, kind):
        if resultID < 0:
            message = i18n.makeString('#system_messages:customization/camouflage_drop_server_error')
            self.onCustomizationDropFailed(message)
            return None
        item = self.currentItemsByKind.get(kind)
        if g_tankActiveCamouflage.has_key(g_currentVehicle.vehicle.descriptor.type.compactDescr):
            del g_tankActiveCamouflage[g_currentVehicle.vehicle.descriptor.type.compactDescr]
        
        item['id'] = None
        item['lifeCycle'] = None
        if CAMOUFLAGE_KINDS.get(self._itemsDP.currentGroup) == kind:
            self._itemsDP.currentItemID = None
        
        if item.get('newItemID') is None:
            g_currentVehicle.update()
        
        message = i18n.makeString('#system_messages:customization/camouflage_drop_success')
        self.onCustomizationDropSuccess(message)



