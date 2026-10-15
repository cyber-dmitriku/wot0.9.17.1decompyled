# Source Generated with Decompyle++
# File: VehicleCustomization.pyc (Python 2.6)

from adisp import process
from CurrentVehicle import g_currentVehicle
from debug_utils import LOG_ERROR, LOG_DEBUG
import gui
from gui.Scaleform.customization.VehicleCustonizationModel import VehicleCustomizationModel
from items import vehicles
from items.vehicles import VehicleDescr
from gui import SystemMessages
from gui.Scaleform.CommandArgsParser import CommandArgsParser
from gui.Scaleform.Waiting import Waiting
from gui.Scaleform.customization import _VEHICLE_CUSTOMIZATIONS
from gui.Scaleform.utils.requesters import StatsRequester
from gui.Scaleform.windows import UIInterface
from gui.Scaleform.utils.HangarSpace import g_hangarSpace
from helpers import i18n
from PlayerEvents import g_playerEvents
from gui.ClientUpdateManager import g_clientUpdateManager

class VehicleCustomization(UIInterface):
    
    def __init__(self):
        super(VehicleCustomization, self).__init__()
        self._VehicleCustomization__interfaces = { }
        self._VehicleCustomization__prevCameraLocation = None
        self._VehicleCustomization__steps = 0
        self._VehicleCustomization__messages = []
        self._VehicleCustomization__credits = 0
        self._VehicleCustomization__gold = 0
        self._VehicleCustomization__returnHangar = False
        self._VehicleCustomization__lockUpdate = False
        self._VehicleCustomization__onceDataInited = False
        self._VehicleCustomization__flashForm = None

    
    def __del__(self):
        LOG_DEBUG('VehicleCustomization deleted')

    
    def _VehicleCustomization__onServerResponsesReceived(self):
        self._VehicleCustomization__flashForm.onServerResponsesReceived()
        self._VehicleCustomization__lockUpdate = False
        Waiting.hide('customizationApply')
        for (type, message) in self._VehicleCustomization__messages:
            SystemMessages.pushMessage(message, type = type)
        
        self._VehicleCustomization__messages = []
        if self._VehicleCustomization__returnHangar:
            self.uiHolder.movie.invoke(('loadHangar',))
        

    
    def _VehicleCustomization__setPreviewMode(self):
        space = g_hangarSpace.space
        if space is not None:
            self._VehicleCustomization__prevCameraLocation = space.getCameraLocation()
            space.locateCameraToPreview()
        else:
            LOG_ERROR("ClientHangarSpace isn't initialized")

    
    def _VehicleCustomization__resetPreviewMode(self):
        space = g_hangarSpace.space
        if space is not None and self._VehicleCustomization__prevCameraLocation is not None:
            space.setCameraLocation(**None)
        

    
    def __requestMoney(self):
        yield StatsRequester().getCredits()
        self._VehicleCustomization__credits = None
        yield StatsRequester().getGold()
        self._VehicleCustomization__gold = None

    _VehicleCustomization__requestMoney = process(__requestMoney)
    
    def _VehicleCustomization__finishInitData(self):
        if not self._VehicleCustomization__onceDataInited:
            self._VehicleCustomization__requestMoney()
            self._VehicleCustomization__flashForm.onInit(self._getSections())
            if g_currentVehicle.isLocked() or g_currentVehicle.isBroken():
                self._VehicleCustomization__flashForm.setActionsLocked(True)
            
            self._VehicleCustomization__setPreviewMode()
            self._VehicleCustomization__onceDataInited = True
        
        Waiting.hide('loadPage')

    
    def populateUI(self, proxy):
        super(VehicleCustomization, self).populateUI(proxy)
        self._VehicleCustomization__flashForm = proxy.movie.contentHolder.main.window.form
        self._VehicleCustomization__flashForm.resync()
        self._VehicleCustomization__flashForm.script = self
        self.uiHolder.movie.backgroundAlpha = 0
        self.uiHolder.addExternalCallbacks({
            'Customization.Vehicle.DoApply': self.onConfirmApply,
            'Customization.Vehicle.DoDrop': self.onConfirmDrop })
        g_clientUpdateManager.addCallbacks({
            'stats.gold': self.onGoldUpdate,
            'stats.credits': self.onCreditsUpdate,
            'account.attrs': self.onCameraUpdate,
            'inventory.1.compDescr': self.onVehiclesUpdate })
        g_playerEvents.onShopResync += self._VehicleCustomization__pe_onShopResync
        g_currentVehicle.onChanged += self._VehicleCustomization__cv_onChanged
        vehDescr = None
        vehType = None
        if g_currentVehicle.isPresent():
            vehDescr = g_currentVehicle.vehicle.descriptor
            vehType = vehDescr.type
            VehicleCustomizationModel.setVehicleDescriptor(vehDescr)
        
        self._VehicleCustomization__steps = len(_VEHICLE_CUSTOMIZATIONS)
        for customization in _VEHICLE_CUSTOMIZATIONS:
            sectionName = customization['sectionName']
            interface = customization['interface'](customization['sectionName'], vehDescr.type.id[0], customization['position'])
            interface.onDataInited += self._VehicleCustomization__ci_onDataInited
            interface.onCustomizationChangeSuccess += self._VehicleCustomization__ci_onCustomizationChangeSuccess
            interface.onCustomizationChangeFailed += self._VehicleCustomization__ci_onCustomizationChangeFailed
            interface.onCustomizationDropSuccess += self._VehicleCustomization__ci_onCustomizationDropSuccess
            interface.onCustomizationDropFailed += self._VehicleCustomization__ci_onCustomizationDropFailed
            interface.onCurrentItemChange += self._VehicleCustomization__ci_onCurrentItemChanged
            self._VehicleCustomization__interfaces[sectionName] = interface
            interface.populateUI(proxy)
            interface.fetchCurrentItem(vehDescr)
            interface.invalidateData(vehType)
        
        if not self._VehicleCustomization__steps:
            self._VehicleCustomization__finishInitData()
        

    
    def dispossessUI(self):
        self._VehicleCustomization__flashForm.script = None
        self._VehicleCustomization__flashForm = None
        self._VehicleCustomization__resetPreviewMode()
        for interface in self._VehicleCustomization__interfaces.itervalues():
            interface.dispossessUI()
            interface.onDataInited -= self._VehicleCustomization__ci_onDataInited
            interface.onCustomizationChangeSuccess -= self._VehicleCustomization__ci_onCustomizationChangeSuccess
            interface.onCustomizationChangeFailed -= self._VehicleCustomization__ci_onCustomizationChangeFailed
            interface.onCustomizationDropSuccess -= self._VehicleCustomization__ci_onCustomizationDropSuccess
            interface.onCustomizationDropFailed -= self._VehicleCustomization__ci_onCustomizationDropFailed
        
        self._VehicleCustomization__interfaces.clear()
        self._VehicleCustomization__onceDataInited = False
        g_playerEvents.onShopResync -= self._VehicleCustomization__pe_onShopResync
        g_currentVehicle.onChanged -= self._VehicleCustomization__cv_onChanged
        g_clientUpdateManager.removeObjectCallbacks(self)
        self.uiHolder.removeExternalCallbacks('Customization.Vehicle.RequestSections', 'Customization.Vehicle.Apply', 'Customization.Vehicle.DoApply', 'Customization.Vehicle.Drop', 'Customization.Vehicle.DoDrop')
        super(VehicleCustomization, self).dispossessUI()

    
    def _getSections(self):
        res = []
        for customization in _VEHICLE_CUSTOMIZATIONS:
            res.append({
                'sectionName': customization['sectionName'],
                'sectionLabel': customization['sectionUserString'],
                'priceLabel': customization['priceUserString'],
                'disabled': not self.getInterface(customization['sectionName']).isEnabled() })
        
        return res

    
    def onClickApplyButton(self, event):
        if g_currentVehicle.isLocked():
            SystemMessages.pushI18nMessage('#system_messages:customization/vehicle_locked', type = SystemMessages.SM_TYPE.Error)
            return None
        if g_currentVehicle.isBroken():
            SystemMessages.pushI18nMessage('#system_messages:customization/vehicle_{0:>s}'.format(g_currentVehicle.getState()), type = SystemMessages.SM_TYPE.Error)
            return None
        notSelected = []
        selected = []
        remove = []
        totalGold = 0
        totalCredits = 0
        self._VehicleCustomization__flashForm.resync()
        sections = self._VehicleCustomization__flashForm.selectedSections[:]
        for section in sections:
            interface = self._VehicleCustomization__interfaces.get(section.sectionName)
            if interface is not None:
                if interface.isNewItemSelected():
                    costValue = interface.getSelectedItemCost()
                    if type(costValue) is list:
                        for price in costValue:
                            cost = price.get('cost')
                            isGold = price.get('isGold')
                            if cost > 0:
                                if isGold and section.isGold:
                                    totalGold += cost
                                elif not isGold and not (section.isGold):
                                    totalCredits += cost
                                
                            not (section.isGold)
                        
                    else:
                        (cost, isGold) = costValue
                        if cost > 0:
                            if isGold:
                                totalGold += cost
                            else:
                                totalCredits += cost
                        
                    selected.append(i18n.makeString('#menu:customization/change/{0:>s}'.format(section.sectionName)))
                    if interface.isCurrentItemRemove():
                        remove.append(gui.makeHtmlString('html_templates:lobby/customization', 'remove-{0:>s}'.format(section.sectionName)))
                    
                else:
                    notSelected.append(i18n.makeString('#menu:customization/items/{0:>s}'.format(section.sectionName)))
            interface.isNewItemSelected()
            LOG_ERROR('Section not found', section.sectionName)
        
        if len(notSelected) > 0:
            messageEx = i18n.makeString('#dialogs:customization/selectNewItems/message', ', '.join(notSelected))
            self.call('common.showMessageDialog', [
                'customization/selectNewItems',
                True,
                False,
                messageEx,
                None])
            return None
        creditsNotEnough = totalCredits > self._VehicleCustomization__credits
        goldNotEnough = totalGold > self._VehicleCustomization__gold
        if creditsNotEnough or goldNotEnough:
            if creditsNotEnough and goldNotEnough:
                key = '#system_messages:customization/credits_and_gold_not_enough'
            elif goldNotEnough:
                key = '#system_messages:customization/gold_not_enough'
            else:
                key = '#system_messages:customization/credits_not_enough'
            SystemMessages.pushI18nMessage(key, type = SystemMessages.SM_TYPE.Error)
            return None
        messageEx = i18n.makeString('#dialogs:customization/changeConfirmation/message', selected = ', '.join(selected), remove = '\n'.join(remove))
        args = [
            'customization/changeConfirmation',
            True,
            True,
            messageEx,
            'Customization.Vehicle.DoApply']
        self.call('common.showMessageDialog', args)

    
    def onConfirmApply(self, _):
        self._VehicleCustomization__returnHangar = True
        vehInvID = g_currentVehicle.vehicle.inventoryId
        sections = self._VehicleCustomization__flashForm.selectedSections[:]
        continue
        sections = _[1]([ (s.sectionName, s) for s in sections ]).values()
        self._VehicleCustomization__steps = 0
        self._VehicleCustomization__messages = []
        self._VehicleCustomization__flashForm.applyButton.disabled = True
        if len(sections) > 0:
            Waiting.show('customizationApply')
            self._VehicleCustomization__lockUpdate = True
        
        for section in sections:
            interface = self._VehicleCustomization__interfaces.get(section.sectionName)
            if interface is not None:
                self._VehicleCustomization__steps += interface.getSelectedItemsCount()
                interface.change(vehInvID, section)
                continue
            []
            LOG_ERROR('Change operation, section not found', section)
            self._VehicleCustomization__steps -= 1
        
        if not self._VehicleCustomization__steps:
            self._VehicleCustomization__onServerResponsesReceived()
        

    
    def dropCurrentItemInSection(self, section, kind):
        if g_currentVehicle.isLocked():
            SystemMessages.pushI18nMessage('#system_messages:customization/vehicle_locked', type = SystemMessages.SM_TYPE.Error)
            return None
        if g_currentVehicle.isBroken():
            SystemMessages.pushI18nMessage('#system_messages:customization/vehicle_{0:>s}'.format(g_currentVehicle.getState()), type = SystemMessages.SM_TYPE.Error)
            return None
        dialog = 'customization/{0:>s}Drop'.format(section)
        self.call('common.showMessageDialog', [
            dialog,
            True,
            True,
            None,
            'Customization.Vehicle.DoDrop',
            section,
            kind])

    
    def onConfirmDrop(self, *args):
        parser = CommandArgsParser(self.onConfirmDrop.__name__, 2, [
            str,
            int])
        (section, kind) = parser.parse(*args)
        interface = self._VehicleCustomization__interfaces.get(section)
        if interface is not None:
            self._VehicleCustomization__returnHangar = False
            self._VehicleCustomization__lockUpdate = True
            Waiting.show('customizationDrop')
            interface.drop(g_currentVehicle.vehicle.inventoryId, kind)
        else:
            LOG_ERROR('Drop operation, section not found', section)

    
    def _VehicleCustomization__ci_onDataInited(self, _):
        self._VehicleCustomization__steps -= 1
        if not self._VehicleCustomization__steps:
            self._VehicleCustomization__finishInitData()
        

    
    def _VehicleCustomization__ci_onCustomizationChangeFailed(self, message):
        self._VehicleCustomization__returnHangar = False
        self._VehicleCustomization__messages.append((SystemMessages.SM_TYPE.Error, message))
        self._VehicleCustomization__steps -= 1
        if not self._VehicleCustomization__steps:
            self._VehicleCustomization__onServerResponsesReceived()
        

    
    def _VehicleCustomization__ci_onCustomizationChangeSuccess(self, message, type):
        self._VehicleCustomization__flashForm.onChangeSuccess()
        self._VehicleCustomization__messages.append((type, message))
        self._VehicleCustomization__steps -= 1
        if not self._VehicleCustomization__steps:
            self._VehicleCustomization__onServerResponsesReceived()
        

    
    def _VehicleCustomization__ci_onCustomizationDropFailed(self, message):
        Waiting.hide('customizationDrop')
        self._VehicleCustomization__lockUpdate = False
        SystemMessages.pushMessage(message, type = SystemMessages.SM_TYPE.Error)

    
    def _VehicleCustomization__ci_onCurrentItemChanged(self, section):
        self._VehicleCustomization__flashForm.onCurrentChanged(section)

    
    def _VehicleCustomization__ci_onCustomizationDropSuccess(self, message):
        self._VehicleCustomization__flashForm.onDropSuccess()
        Waiting.hide('customizationDrop')
        self._VehicleCustomization__lockUpdate = False
        SystemMessages.pushMessage(message, type = SystemMessages.SM_TYPE.Information)

    
    def _VehicleCustomization__cv_onChanged(self):
        if not g_currentVehicle.isReadyToFight():
            self.uiHolder.movie.invoke(('loadHangar',))
            return None

    
    def onGoldUpdate(self, value):
        self._VehicleCustomization__gold = value

    
    def onCreditsUpdate(self, value):
        self._VehicleCustomization__credits = value

    
    def onCameraUpdate(self, *args):
        self._VehicleCustomization__prevCameraLocation.update({
            'yaw': None,
            'pitch': None })

    
    def onVehiclesUpdate(self, vehicles):
        if vehicles is None:
            return None
        vehCompDescr = vehicles.get(g_currentVehicle.vehicle.inventoryId)
        if vehCompDescr is not None:
            vehDescr = VehicleDescr(compactDescr = vehCompDescr)
            for interface in self._VehicleCustomization__interfaces.itervalues():
                interface.update(vehDescr)
            
        

    
    def _VehicleCustomization__pe_onShopResync(self):
        if not g_currentVehicle.isPresent():
            return None
        Waiting.show('loadPage')
        self._VehicleCustomization__steps = len(_VEHICLE_CUSTOMIZATIONS)
        vehType = vehicles.g_cache.vehicle(*g_currentVehicle.vehicle.descriptor.type.id)
        self._VehicleCustomization__flashForm.onResetNewItem()
        for interface in self._VehicleCustomization__interfaces.itervalues():
            interface.invalidateData(vehType, refresh = True)
        

    
    def onSoundButtonPress(self, hornId, button):
        interface = self._VehicleCustomization__interfaces.get('horn')
        if interface is not None:
            interface.onSoundButtonPress(hornId, button)
        

    
    def onSoundButtonUp(self):
        interface = self._VehicleCustomization__interfaces.get('horn')
        if interface is not None:
            interface.onSoundButtonRelease()
        

    
    def setNewItemId(self, section, itemId, kind, packageIdx):
        interface = self._VehicleCustomization__interfaces.get(section)
        if interface is not None:
            interface.onSetID(int(itemId), int(kind), int(packageIdx))
        

    
    def getCurrentItem(self, section):
        interface = self._VehicleCustomization__interfaces.get(section)
        if interface is not None:
            return interface.getCurrentItem()
        return None

    
    def getItemCost(self, section, itemId, priceIndex):
        interface = self._VehicleCustomization__interfaces.get(section)
        if interface is not None:
            return interface.getItemCost(itemId, priceIndex)
        return None

    
    def getInterface(self, section):
        return self._VehicleCustomization__interfaces.get(section)



