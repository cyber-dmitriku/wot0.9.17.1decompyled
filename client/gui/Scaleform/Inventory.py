# Source Generated with Decompyle++
# File: Inventory.pyc (Python 2.6)

import BigWorld
from account_helpers.AccountSettings import AccountSettings
from adisp import process
from CurrentVehicle import g_currentVehicle
from debug_utils import LOG_DEBUG, LOG_ERROR
from helpers.i18n import makeString
from gui import SystemMessages, GUI_NATIONS, GUI_NATIONS_ORDER_INDEX, getNationIndex
from gui.Scaleform.Waiting import Waiting
from gui.Scaleform.utils.gui_items import InventoryVehicle, VehicleItem, compactItem, getItemByCompact
from gui.Scaleform.utils.functions import makeTooltip, stripShortDescrTags
from gui.Scaleform.utils.requesters import Requester, VehicleItemsRequester, StatsRequester, _getComponentsByType, ITEM_TYPE_INDICES
from gui.Scaleform.windows import UIInterface
from PlayerEvents import g_playerEvents
import constants
import MusicController
import nations
from gui.ClientUpdateManager import g_clientUpdateManager

class Inventory(UIInterface):
    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self.uiHolder.movie.backgroundAlpha = 0
        self.uiHolder.addExternalCallbacks({
            'inventory.populateTable': self._Inventory__onDataRequest,
            'inventory.populateMenuFilter': self.populateMenuFilter,
            'inventory.sellItem': self._Inventory__onSellItem,
            'inventory.sellVehicle': self._Inventory__onSellVehicle,
            'inventory.getVehicleSellParams': self._Inventory__onGetSellVehicleParams })
        g_clientUpdateManager.addCallbacks({
            '': self.onTableUpdate,
            'inventory': self.onFiltersUpdate })
        g_playerEvents.onShopResync += self.update
        MusicController.g_musicController.play(MusicController.MUSIC_EVENT_LOBBY)
        MusicController.g_musicController.play(MusicController.AMBIENT_EVENT_SHOP)
        self.populateFilters(True)
        Waiting.hide('loadPage')

    
    def dispossessUI(self):
        g_playerEvents.onShopResync -= self.update
        g_clientUpdateManager.removeObjectCallbacks(self)
        self.uiHolder.removeExternalCallbacks('inventory.populateTable', 'inventory.populateMenuFilter', 'inventory.sellItem', 'inventory.getVehicleSellParams', 'inventory.sellVehicle')
        UIInterface.dispossessUI(self)

    
    def __del__(self):
        LOG_DEBUG('InventoryHandler deleted')

    
    def onFiltersUpdate(self, *args):
        self.populateFilters()

    
    def onTableUpdate(self, *args):
        params = self._Inventory__getCurrentFilter()
        params.extend(AccountSettings.getFilter('inventory_' + params[1]))
        self._Inventory__onDataRequest(0, *params)

    
    def _Inventory__getCurrentFilter(self):
        filter = list(AccountSettings.getFilter('inventory_current'))
        if filter[0] < len(GUI_NATIONS):
            pass
        1
        return [
            -1,
            filter[1]]

    
    def update(self, diff = { }):
        pass

    
    def populateFilters(self, init = False):
        self.uiHolder.updateAccountInfo()
        yield Requester('vehicle').getFromInventory()
        vehicles = None
        filterVehicle = None
        if g_currentVehicle.isPresent():
            filterVehicle = compactItem(g_currentVehicle.vehicle)
        
        filter = self._Inventory__getCurrentFilter()
        if filter[1] == 'module':
            filter = list(AccountSettings.getFilter('inventory_module'))
            typeSize = int(filter.pop(0))
            filterVehicle = filter[typeSize + 1]
        
        vehFilter = [
            filterVehicle]
        vehicles.sort(reverse = True)
        for v in vehicles:
            vehFilter.append(compactItem(v))
            vehFilter.append(GUI_NATIONS_ORDER_INDEX[nations.NAMES[v.nation]])
            vehFilter.append(v.name)
        
        if init:
            self.call('inventory.setFilter', self._Inventory__getCurrentFilter())
        
        self.call('inventory.setVehicleFilter', vehFilter)

    populateFilters = process(populateFilters)
    
    def populateMenuFilter(self, callbackId, type):
        res
