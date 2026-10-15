# Source Generated with Decompyle++
# File: HornInterface.pyc (Python 2.6)

import BigWorld
from debug_utils import LOG_DEBUG
from gui import SystemMessages
from gui.Scaleform.customization.HornSoundPlayer import HornSoundPlayer
from gui.Scaleform.customization.CustomizationInterface import CustomizationInterface
from gui.Scaleform.customization.data_providers import HornsDataProvider
from helpers import i18n
import Event

class HornInterface(CustomizationInterface):
    
    def __init__(self, name, nationID, position):
        super(HornInterface, self).__init__(name, nationID, position)
        self._currentHornID = None
        self._newHornID = None
        self._player = HornSoundPlayer()
        self._player.onStartSoundEvent += self._HornInterface__onStartHornSoundEvent
        self._player.onStopSoundEvent += self._HornInterface__onStopHornSoundEvent

    
    def __del__(self):
        LOG_DEBUG('HornInterface deleted')

    
    def populateUI(self, proxy):
        super(HornInterface, self).populateUI(proxy)
        self._hornsDP = HornsDataProvider()
        self._hornsDP.populateUI(proxy)

    
    def dispossessUI(self):
        self.uiHolder.removeExternalCallbacks('Customization.Vehicle.Horn.RequestCurrent', 'Customization.Vehicle.Horn.SetHornID')
        self._hornsDP.dispossessUI()
        self._hornsDP = None
        self._player.fini()
        self._eventManager.clear()
        super(HornInterface, self).dispossessUI()

    
    def fetchCurrentItem(self, vehDescr):
        self._currentHornID = vehDescr.hornID

    
    def invalidateData(self, vehType, refresh = False):
        if vehType is not None:
            self._hornsDP.setVehicleTypeParams(vehType.tags, vehType.hornPriceFactor)
        
        (None, BigWorld.player().shop.getHornCost)((lambda resultID, costs, rev: self._HornInterface__onGetHornCost(resultID, costs, rev, refresh)))

    
    def isNewItemSelected(self):
        return self._newHornID is not None

    
    def getSelectedItemCost(self):
        return (self._hornsDP.getCost(self._newHornID), 1)

    
    def isCurrentItemRemove(self):
        return self._currentHornID is not None

    
    def change(self, vehInvID, section):
        if self._newHornID is None:
            message = i18n.makeString('#system_messages:customization/horn_not_selected')
            self.onCustomizationChangeFailed(message)
            return None
        gold = self._hornsDP.getCost(self._newHornID)
        if gold < 0:
            message = i18n.makeString('#system_messages:customization/horn_cost_not_found')
            self.onCustomizationChangeFailed(message)
            return None
        gold < 0(BigWorld.player().inventory.changeVehicleHorn, (vehInvID, self._newHornID), (lambda resultID: self._HornInterface__onChangeVehicleHorn(resultID, gold)))

    
    def drop(self, vehInvID, kind):
        if self._currentHornID is None:
            message = i18n.makeString('#system_messages:customization/horn_not_found_to_drop')
            self.onCustomizationDropFailed(message)
            return None
        BigWorld.player().inventory.changeVehicleHorn(vehInvID, 0, self._HornInterface__onDropVehicleHorn)

    
    def update(self, vehicleDescr):
        hornID = vehicleDescr.hornID
        if hornID != self._currentHornID:
            self._currentHornID = hornID
            self._hornsDP.buildList(self._currentHornID)
            self.onCurrentItemChange(self._name)
        

    
    def _HornInterface__onGetHornCost(self, resultID, costs, _, refresh):
        if resultID < 0:
            SystemMessages.pushI18nMessage('#system_messages:customization/horn_get_cost_server_error', type = SystemMessages.SM_TYPE.Error)
        else:
            self._hornsDP.setHornDefCosts(costs)
            self._hornsDP.buildList(self._currentHornID)
        if refresh:
            self._newHornID = None
            self._hornsDP.refresh()
        
        LOG_DEBUG('HornInterface data inited.')
        self.onDataInited(self._name)

    
    def _HornInterface__onChangeVehicleHorn(self, resultID, gold):
        if resultID < 0:
            message = i18n.makeString('#system_messages:customization/horn_change_server_error')
            self.onCustomizationChangeFailed(message)
            return None
        self._currentHornID = self._newHornID
        self._newHornID = None
        self._hornsDP.buildList(self._currentHornID)
        message = i18n.makeString('#system_messages:customization/horn_change_success', BigWorld.wg_getGoldFormat(gold))
        self.onCustomizationChangeSuccess(message, SystemMessages.SM_TYPE.CustomizationForGold)

    
    def _HornInterface__onDropVehicleHorn(self, resultID):
        if resultID < 0:
            message = i18n.makeString('#system_messages:customization/horn_drop_server_error')
            self.onCustomizationDropFailed(message)
            return None
        self._currentHornID = None
        self._hornsDP.buildList(None)
        message = i18n.makeString('#system_messages:customization/horn_drop_success')
        self.onCustomizationDropSuccess(message)

    
    def _HornInterface__playHornSound(self, hornID, button):
        if hornID is not None:
            self._player.play(hornID, button)
        

    
    def _HornInterface__onStartHornSoundEvent(self, button):
        if button is not None:
            button.soundPlaying = True
        

    
    def _HornInterface__onStopHornSoundEvent(self, button):
        if button is not None:
            button.soundPlaying = False
        

    
    def getCurrentItem(self):
        return self._hornsDP.makeItem(self._currentHornID, False)

    
    def onSetID(self, hornID, kind, packageIdx):
        if self._currentHornID == hornID:
            self._newHornID = None
        else:
            self._newHornID = hornID

    
    def onSoundButtonPress(self, hornID, button):
        self._HornInterface__playHornSound(hornID, button)

    
    def onSoundButtonRelease(self):
        self._player.stopWithDelay()



