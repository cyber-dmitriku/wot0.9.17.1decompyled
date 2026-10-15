# Source Generated with Decompyle++
# File: Hangar.pyc (Python 2.6)

import BigWorld
import MusicController
import account_helpers
import FMOD
import SoundGroups
from account_helpers.AccountPrebattle import AccountPrebattle
from account_helpers.AccountSettings import AccountSettings, CAROUSEL_FILTER
from adisp import process
from PlayerEvents import g_playerEvents
from CurrentVehicle import g_currentVehicle
from debug_utils import *
from gui.BattleContext import g_battleContext
from items.tankmen import getSkillsConfig, COMMANDER_ADDITION_RATIO, PERKS, compareMastery, ACTIVE_SKILLS
from items import ITEM_TYPE_NAMES, getTypeInfoByName
from helpers.i18n import convert, makeString
from gui import SystemMessages, AOGAS, GUI_SETTINGS
from gui.ClientUpdateManager import g_clientUpdateManager
from gui.Scaleform import VoiceChatInterface, ColorSchemeManager
from gui.Scaleform.Waiting import Waiting
from gui.Scaleform.windows import UIInterface
from gui.Scaleform.TankmenInterface import TankmenInterface
from gui.Scaleform.TechnicalMaintenance import TechnicalMaintenance
from gui.Scaleform.utils.requesters import Requester, AvailableItemsRequester, StatsRequester, VehicleItemsRequester
from gui.Scaleform.utils import gui_items
from gui.Scaleform.utils.gui_items import formatPrice, getItemByCompact, VehicleItem
from gui.Scaleform.utils.functions import isModuleFitVehicle, findConflictedEquipmentForModule, async_showConfirmDialog, showConfirmDialog
from gui.Scaleform.utils.HangarSpace import g_hangarSpace
INVENTORY_ITEM_TANKMEN_IDX = 3

class Hangar(UIInterface):
    UPDATE_LOCKS_PERIOD = 60
    gprahicsSettingsResetDialogShown = False
    
    def __init__(self):
        self._Hangar__inited = 0
        UIInterface.__init__(self)
        self.tankmenInterface = TankmenInterface(self)
        self._Hangar__techMaintenance = TechnicalMaintenance()
        self._Hangar__fitting = Fitting()
        self._Hangar__updateVehiclesTimerId = None
        self.vehiclesFilter = dict(AccountSettings.getFilter(CAROUSEL_FILTER))

    
    def __del__(self):
        LOG_DEBUG('HangarHandler deleted')

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self.tankmenInterface.populateUI(proxy)
        g_playerEvents.onVehicleBecomeElite += self._Hangar__onVehicleBecomeElite
        self._Hangar__fitting.populateUI(proxy)
        self.uiHolder.movie.backgroundAlpha = 0
        self.uiHolder.movie.wg_inputKeyMode = 1
        self.uiHolder.addExternalCallbacks({
            'hangar.vehicleChange': self.onVehicleSelectChange,
            'hangar.ammoRequest': self.onAmmoRequest,
            'hangar.checkMoney': self.onCheckMoney,
            'hangar.buySlot': self.onBuySlot,
            'hangar.setVehiclesFilter': self.onSetVehiclesFilter,
            'hangar.sellVehicle': self.onSellVehicle,
            'hangar.getVehicleSellParams': self.onGetSellVehicleParams,
            'hangar.favoriteVehicle': self.onFavoriteVehicle,
            'hangar.getUnlockVehicles': self.onGetUnlockVehicles,
            'hangar.buyTankClick': self.onBuyTank })
        self.colorManager = ColorSchemeManager._ColorSchemeManager()
        self.colorManager.populateUI(proxy)
        VoiceChatInterface.g_instance.onVoiceChatInitFailed += self.onVoiceChatInitFailed
        VoiceChatInterface.g_instance.onVoiceChatInitSucceded += self.onVoiceChatInitSucceded
        g_currentVehicle.onChanged += self._Hangar__onCurrentVehicleChanged
        g_playerEvents.onShopResync += self.update
        g_playerEvents.onPrebattleLeft += self._Hangar__onPrebattleLeft
        g_playerEvents.onKickedFromPrebattle += self._Hangar__onKickedFromPrebattle
        g_playerEvents.onBattleResultsReceived += self.onFittingUpdate
        self._Hangar__techMaintenance.populateUI(proxy)
        g_currentVehicle.update()
        self.call('hangar.setCarouselFilter', [
            self.vehiclesFilter['nation'],
            self.vehiclesFilter['tankType'],
            self.vehiclesFilter['ready']])
        BigWorld.player().stats.get('attrs', self._Hangar__startSoundEventsCallback)
        AOGAS.g_controller.enableNotifyAccount()
        g_clientUpdateManager.addCallbacks({
            'inventory.1': self.onVehiclesUpdate,
            'inventory.1.compDescr': self.onCurrentVehicleUpdate,
            'inventory.1.repair': self.onCurrentVehicleUpdate,
            'inventory.1.shells': self.onCurrentVehicleUpdate,
            'inventory.1.shellsLayout': self.onCurrentVehicleUpdate,
            'inventory.1.eqs': self.onCurrentVehicleUpdate,
            'inventory.1.eqsLayout': self.onCurrentVehicleUpdate,
            'inventory.8': self.onPersonalCasesUpdate,
            'stats.multipliedXPVehs_r': self.onVehiclesUpdate,
            'stats.slots': self.onVehiclesUpdate,
            'stats.vehTypeXP': self.onVehiclesUpdate,
            'stats.unlocks': self.onVehiclesUpdate,
            'stats.eliteVehicles': self.onVehiclesUpdate,
            'stats.credits': self.onFittingUpdate,
            'stats.gold': self.onFittingUpdate,
            'stats.vehicleSellsLeft': self.onFittingUpdate,
            'stats.vehTypeLocks': self.onVehiclesUpdate })
        if not self.uiHolder.commandsBinded:
            self.uiHolder.bindCommands()
        
        self._Hangar__checkGraphicsSettingsRest()
        Waiting.hide('loadPage')
        self._Hangar__showBattleResults()

    
    def _Hangar__showBattleResults(self):
        if GUI_SETTINGS.battleStatsInHangar and g_battleContext.lastArenaUniqueID:
            self.uiHolder.battleResults.onBattleResultsShow(None, g_battleContext.lastArenaUniqueID)
            g_battleContext.lastArenaUniqueID = None
        

    
    def _Hangar__checkGraphicsSettingsRest(self):
        isResetted = BigWorld.graphicsSettingsWereForcedToReset()
        if isResetted and not (Hangar.gprahicsSettingsResetDialogShown):
            
            def callback(isConfirm):
                if isConfirm:
                    self.call('common.showSettings', [
                        1])
                

            showConfirmDialog('resetGraphics', callback)
            Hangar.gprahicsSettingsResetDialogShown = True
        

    
    def onVoiceChatInitFailed(self):
        self.call('VoiceChat.initFailed', [])

    
    def onVoiceChatInitSucceded(self):
        self.call('VoiceChat.initSucceded', [])

    
    def _Hangar__startSoundEventsCallback(self, resultId, attrs):
        isPremium = account_helpers.isPremiumAccount(attrs)
        MusicController.g_musicController.setAccountAttrs(attrs)
        MusicController.g_musicController.play(MusicController.MUSIC_EVENT_LOBBY)
        MusicController.g_musicController.play(MusicController.AMBIENT_EVENT_LOBBY)
        self._Hangar__premiumHangarSndFan = None
        if isPremium:
            self._Hangar__premiumHangarSndFan = FMOD.getSound('/ambient/hangar/hangar_prem_fen')
        
        if self._Hangar__premiumHangarSndFan is not None:
            self._Hangar__premiumHangarSndFan.position = (50, 2, 64)
            self._Hangar__premiumHangarSndFan.play()
        
        SoundGroups.g_instance.enableLobbySounds(True)

    
    def dispossessUI(self):
        if self._Hangar__updateVehiclesTimerId is not None:
            BigWorld.cancelCallback(self._Hangar__updateVehiclesTimerId)
            self._Hangar__updateVehiclesTimerId = None
        
        g_clientUpdateManager.removeObjectCallbacks(self)
        if self.colorManager:
            self.colorManager.dispossessUI()
        
        if self._Hangar__premiumHangarSndFan is not None:
            self._Hangar__premiumHangarSndFan.stop()
            self._Hangar__premiumHangarSndFan = None
        
        self._Hangar__techMaintenance.dispossessUI()
        g_playerEvents.onVehicleBecomeElite -= self._Hangar__onVehicleBecomeElite
        self._Hangar__fitting.dispossessUI()
        g_currentVehicle.onChanged -= self._Hangar__onCurrentVehicleChanged
        g_playerEvents.onShopResync -= self.update
        g_playerEvents.onBattleResultsReceived -= self.onFittingUpdate
        g_playerEvents.onPrebattleLeft -= self._Hangar__onPrebattleLeft
        g_playerEvents.onKi
