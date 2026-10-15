# Source Generated with Decompyle++
# File: techtree_page.pyc (Python 2.6)

import weakref
from AccountCommands import RES_SUCCESS
from adisp import process
import BigWorld
import Keys
from constants import IS_DEVELOPMENT
from debug_utils import LOG_DEBUG, LOG_ERROR, LOG_CURRENT_EXCEPTION
from gui.Scaleform.techtree.custom_items import _convert4ToolTip
from gui.Scaleform.techtree.listeners import StatsListener, InventoryListener, INV_ITEM_VCDESC_KEY
from items import ITEM_TYPE_NAMES, vehicles
from gui.Scaleform.techtree import custom_items, _VEHICLE, _VEHICLE_TYPE_NAME, USE_XML_DUMPING, SelectedNation
from gui.Scaleform.techtree import dumpers
from gui.Scaleform.techtree.data import NationTreeData
from gui.Scaleform.techtree.techtree_dp import g_techTreeDP
from gui.Scaleform.techtree.interfaces import ItemsInterface, _AS_DisplayRoot, _Py_BaseScriptHandler
from gui.Scaleform.Waiting import Waiting
from gui.Scaleform.utils.requesters import StatsRequester
from functools import partial
import nations
from PlayerEvents import g_playerEvents

class _Py_ScriptHandler(_Py_BaseScriptHandler):
    
    def requestNationTreeData(self):
        pass

    
    def getNationTreeData(self, nationName):
        pass



class _AS_TechTreeDO(_AS_DisplayRoot):
    
    def setAvailableNations(self, nations):
        pass

    
    def setSelectedNation(self, nationName):
        pass

    
    def refreshNationTreeData(self):
        pass



class TechTreePage(ItemsInterface, _Py_ScriptHandler):
    
    def __init__(self):
        data = NationTreeData()
        if USE_XML_DUMPING and IS_DEVELOPMENT:
            dumper = dumpers.NationXMLDumper()
        else:
            dumper = dumpers.NationObjDumper()
        data.setDumper(dumper)
        super(TechTreePage, self).__init__(data)
        self._statsListener = StatsListener()
        self._invListener = InventoryListener()
        SelectedNation.byDefault()

    
    def __del__(self):
        LOG_DEBUG('TechTreePage deleted')

    
    def populateUI(self, proxy):
        super(TechTreePage, self).populateUI(proxy)
        self._displayRoot = self.uiHolder.getMember('contentHolder.main')
        if self._displayRoot is not None:
            self._displayRoot.resync()
            self._displayRoot.script = self
        else:
            self._displayRoot = _AS_TechTreeDO()
            LOG_ERROR('Display object of tech tree not found')
        selfProxy = weakref.proxy(self)
        self._statsListener.startListen(selfProxy)
        self._invListener.startListen(selfProxy)
        g_playerEvents.onShopResync += self._TechTreePage__shop_onResync
        if IS_DEVELOPMENT:
            self.uiHolder.bindExCallbackToKey(Keys.KEY_R, 'NationTree.ReloadData', self._TechTreePage__handleReloadData)
        
        if not Waiting.isVisible():
            Waiting.show('loadPage')
        

    
    def dispossessUI(self):
        if self._displayRoot is not None:
            self._displayRoot.script = None
            self._displayRoot = None
        
        self._statsListener.stopListen()
        self._invListener.stopListen()
        g_playerEvents.onShopResync -= self._TechTreePage__shop_onResync
        if IS_DEVELOPMENT:
            self.uiHolder.clearExCallbackToKey(Keys.KEY_R, 'NationTree.ReloadData')
        
        super(TechTreePage, self).dispossessUI()

    
    def requestNationTreeData(self):
        if USE_XML_DUMPING and IS_DEVELOPMENT:
            self._displayRoot.useXMLDumping()
        
        self._TechTreePage__startDataCollect()
        return True

    
    def getNationTreeData(self, nationName):
        if nationName not in nations.INDICES:
            LOG_ERROR('Nation not found', nationName)
            return { }
        nationIdx = nations.INDICES[nationName]
        SelectedNation.select(nationIdx)
        self._data.load(nationIdx)
        return self._data.dump()

    
    def requestToolTip(self, pickleDump, node):
        text = ''
        
        try:
            manager = self.uiHolder.tooltipManager
            item = _convert4ToolTip(pickleDump, node.shopPrice)
            if item.itemTypeName == _VEHICLE_TYPE_NAME:
                text = manager.getTechTreeVehicleData(item, node = node)
            else:
                text = manager.getTechTreeModuleData(item, node = node)
        except Exception:
            LOG_ERROR('There is error while getting tooltip in tech tree: ', str(pickleDump))
            LOG_CURRENT_EXCEPTION()

        return text

    
    def request4Unlock(self, unlockCD, vehCD, unlockIdx, xpCost):
        self.unlockItem(int(unlockCD), int(vehCD), int(unlockIdx), int(xpCost))

    
    def request4Buy(self, itemCD):
        self.buyVehicle(int(itemCD))

    
    def showSystemMessage(self, typeString, message):
        self.pushSystemMessage(typeString, message)

    
    def setInvVehicles(self, data):
        vCDs = data.get(INV_ITEM_VCDESC_KEY, { })
        vTypeName = ITEM_TYPE_NAMES[_VEHICLE]
        result = set()
        for (invID, vStrCD) in vCDs.iteritems():
            vType = vehicles.getVehicleType(vStrCD)
            vIntCD = vehicles.makeIntCompactDescrByID(vTypeName, vType.id[0], vType.id[1])
            self._data.setInvItem(vIntCD, custom_items._makeInventoryVehicle(invID, vStrCD, data))
            result.add(vIntCD)
        
        return (result, False)

    
    def setInvItems(self, data):
        return set()

    
    def invalidateVehLocks(self, locks):
        pass

    
    def __startDataCollect(self):
        yield StatsRequester().getVehicleTypeExperiences()
        self._data._xps = None
        yield StatsRequester().getUnlocks()
        self._data._unlocks = None
        yield StatsRequester().getEliteVehicles()
        self._data._elite = None
        yield StatsRequester().getFreeExperience()
        self._data._accFreeXP = None
        yield StatsRequester().getCredits()
        self._data._accCredits = None
        yield StatsRequester().getGold()
        self._data._accGold = None
        yield StatsRequester().getAccountDossier()
        accDossier = None
        if accDossier and accDossier['vehDossiersCut']:
            self._data._wereInBattle = set(accDossier['vehDossiersCut'].keys())
        
        self._TechTreePage__requestVehiclesFromInv()

    _TechTreePage__startDataCollect = process(__startDataCollect)
    
    def _TechTreePage__requestVehiclesFromInv(self):
        BigWorld.player().inventory.getItems(_VEHICLE, self._TechTreePage__onGetVehiclesFromInventory)

    
    def _TechTreePage__onGetVehiclesFromInventory(self, resultID, data):
        if resultID < RES_SUCCESS:
            LOG_ERROR('Server return error inventory vehicle items request: responseCode=', resultID)
            data = {
                INV_ITEM_VCDESC_KEY: { } }
        
        self.setInvVehicles(data)
        self._TechTreePage__requestVehiclesFromShop(nations.INDICES.values())

    
    def _TechTreePage__requestVehiclesFromShop(self, nationIDs):
        if len(nationIDs) > 0:
            next = nationIDs.pop()
            BigWorld.player().shop.getItems(_VEHICLE, next, partial(self._TechTreePage__onGetVehiclesFromShop, next, nationIDs))
        else:
            self._TechTreePage__stopDataCollect()

    
    def _TechTreePage__onGetVehiclesFromShop(self, nationID, nationIDs, resultID, data, _):
        if resultID < RES_SUCCESS:
            LOG_ERROR('Server return error shop vehicles request: responseCode=' % resultID)
            data = { }
        
        dataLen = len(data)
        if dataLen:
            pass
        1
        prices = []
        if dataLen > 1:
            pass
        1
        nationID(data[1], set())
        for (innationID, price) in prices:
            intCD = vehicles.makeIntCompactDescrByID(ITEM_TYPE_NAMES[_VEHICLE], nationID, innationID)
            self._data.setShopPrice(intCD, price)
        
        self._TechTreePage__requestVehiclesFromShop(nationIDs)

    
    def _TechTreePage__stopDataCollect(self):
        self._displayRoot.setAvailableNations(g_techTreeDP.getAvailableNations())
        self._displayRoot.setSelectedNation(SelectedNation.getName())
        Waiting.hide('loadPage')

    
    def _TechTreePage__shop_onResync(self):
        self._TechTreePage__requestVehiclesFromShop(nations.INDICES.values())
        self._displayRoot.refreshNationTreeData()

    
    def _TechTreePage__handleReloadData(self, _, isDown):
        if not isDown:
            g_techTreeDP.load(reload = True)
            self._displayRoot.refreshNationTreeData()
        



