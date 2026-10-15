# Source Generated with Decompyle++
# File: research_page.pyc (Python 2.6)

import weakref
from AccountCommands import RES_SUCCESS
from PlayerEvents import g_playerEvents
from adisp import process
import BigWorld
from CurrentVehicle import g_currentVehicle
from constants import IS_DEVELOPMENT
from debug_utils import LOG_ERROR, LOG_DEBUG, LOG_CURRENT_EXCEPTION
from gui import SystemMessages
from gui.Scaleform.Waiting import Waiting
from gui.Scaleform.techtree import _TURRET, _GUN
from gui.Scaleform.techtree.custom_items import _makeShopItem, _convert4ToolTip
from gui.Scaleform.techtree.listeners import StatsListener, InventoryListener, INV_ITEM_VCDESC_KEY
from gui.Scaleform.utils import functions
from gui.Scaleform.utils.functions import async_showConfirmDialog
from items import ITEM_TYPE_NAMES, vehicles
from gui.Scaleform.techtree import custom_items, _VEHICLE_TYPE_NAME, _VEHICLE, _RESEARCH_ITEMS, USE_XML_DUMPING, SelectedNation, RequestState
from gui.Scaleform.techtree.data import ResearchItemsData
from gui.Scaleform.techtree import dumpers
from gui.Scaleform.techtree.interfaces import ItemsInterface, _AS_DisplayRoot, _Py_BaseScriptHandler
from gui.Scaleform.utils.requesters import StatsRequester, Requester
from functools import partial

class _Py_ScriptHandler(_Py_BaseScriptHandler):
    
    def requestNationData(self, selected):
        pass

    
    def getResearchItemsData(self, vehCD, rootChanged):
        pass

    
    def onResearchItemsDrawn(self):
        pass

    
    def request4Install(self, itemCD):
        pass



class _AS_ResearchDO(_AS_DisplayRoot):
    
    def drawResearchItems(self, vehCD):
        pass

    
    def setInstalledItems(self, data):
        pass



class ResearchPage(ItemsInterface, _Py_ScriptHandler):
    
    def __init__(self):
        data = ResearchItemsData()
        if USE_XML_DUMPING and IS_DEVELOPMENT:
            dumper = dumpers.ResearchItemsXMLDumper()
        else:
            dumper = dumpers.ResearchItemsObjDumper()
        data.setDumper(dumper)
        super(ResearchPage, self).__init__(data)
        self._statsListener = StatsListener()
        self._invListener = InventoryListener()
        SelectedNation.byDefault()

    
    def __del__(self):
        LOG_DEBUG('ResearchPage deleted')

    
    def populateUI(self, proxy):
        super(ResearchPage, self).populateUI(proxy)
        self._displayRoot = self.uiHolder.getMember('contentHolder.main')
        if self._displayRoot is not None:
            self._displayRoot.resync()
            self._displayRoot.script = self
        else:
            self._displayRoot = _AS_ResearchDO()
            LOG_ERROR('Display object of research items not found')
        selfProxy = weakref.proxy(self)
        self._statsListener.startListen(selfProxy)
        self._invListener.startListen(selfProxy)
        g_playerEvents.onShopResync += self._ResearchPage__shop_onResync

    
    def dispossessUI(self):
        if self._displayRoot is not None:
            self._displayRoot.script = None
            self._displayRoot = None
        
        self._statsListener.stopListen()
        self._invListener.stopListen()
        g_playerEvents.onShopResync -= self._ResearchPage__shop_onResync
        super(ResearchPage, self).dispossessUI()

    
    def requestNationData(self, selected):
        if selected is not None:
            self._data.setRootCD(selected)
        elif g_currentVehicle.isPresent():
            selected = g_currentVehicle.vehicle.descriptor.type.compactDescr
            self._data.setRootCD(selected)
        
        self._ResearchPage__startDataCollect()
        return True

    
    def getResearchItemsData(self, vehCD, rootChanged):
        Waiting.show('draw_research_items', isSingle = True)
        if rootChanged:
            self._data.setRootCD(vehCD)
        
        self._data.load()
        return self._data.dump()

    
    def redrawResearchItems(self):
        self._displayRoot.drawResearchItems(self._data.getRootCD())

    
    def onResearchItemsDrawn(self):
        Waiting.hide('draw_research_items')

    
    def requestToolTip(self, pickleDump, node):
        text = ''
        
        try:
            manager = self.uiHolder.tooltipManager
            item = _convert4ToolTip(pickleDump, node.shopPrice)
            rootVehicle = self._data.getItem(self._data.getRootCD())
            if item.itemTypeName == _VEHICLE_TYPE_NAME:
                g_techTreeDP = g_techTreeDP
                import gui.Scaleform.techtree.techtree_dp
                parents = g_techTreeDP.getTopLevel(self._data.getRootCD())
                if item.descriptor.type.compactDescr == rootVehicle.descriptor.type.compactDescr or item.descriptor.type.compactDescr in parents:
                    rootVehicle = None
                
                text = manager.getTechTreeVehicleData(item, rootVehicle, node)
            else:
                text = manager.getTechTreeModuleData(item, rootVehicle, node)
        except Exception:
            LOG_ERROR('There is error while getting tooltip in research page: ', str(pickleDump))
            LOG_CURRENT_EXCEPTION()

        return text

    
    def request4Unlock(self, itemCD, parentID, unlockIdx, xpCost):
        self.unlockItem(int(itemCD), int(parentID), int(unlockIdx), int(xpCost))

    
    def request4Buy(self, itemCD):
        itemCD = int(itemCD)
        (itemTypeID, _, _) = vehicles.parseIntCompactDescr(itemCD)
        if itemTypeID == _VEHICLE:
            self.buyVehicle(itemCD)
        elif RequestState.inProcess('buyAndInstall'):
            SystemMessages.pushI18nMessage('#system_messages:shop/item/buy_and_equip_in_processing', type = SystemMessages.SM_TYPE.Warning)
        
        self.buyAndInstallItem(itemCD, 'buyAndInstall')

    
    def request4Install(self, itemCD):
        if RequestState.inProcess('install'):
            SystemMessages.pushI18nMessage('#system_messages:inventory/item/equip_in_processing', type = SystemMessages.SM_TYPE.Warning)
        
        itemCD = int(itemCD)
        self.buyAndInstallItem(itemCD, 'install', inInventory = True)

    
    def showSystemMessage(self, typeString, message):
        self.pushSystemMessage(typeString, message)

    
    def buyAndInstallItem(self, itemCD, state, inInventory = False):
        (itemTypeID, nationID, itemID) = vehicles.parseIntCompactDescr(itemCD)
        if not itemTypeID in _RESEARCH_ITEMS:
            raise AssertionError
        price = self._data.getShopPrice(itemCD)
        item = _makeShopItem(itemCD, itemTypeID, nationID, price)
        invVehItem = self._data.getInvItem(self._data.getRootCD())
        if not invVehItem is not None:
            raise AssertionError
        eqs = functions.findConflictedEquipments(itemCD, itemTypeID, invVehItem)
        if not inInventory:
            message = self._getBuyConfirmMsg(itemCD, price, eqs)
            yield async_showConfirmDialog('buyInstallConfirmation', customMessage = message)
            isConfirmed = invVehItem is not None
            if not isConfirmed:
                return None
            RequestState.sent(state)
            Waiting.show('buyItem')
            yield item.buy()
            response = isConfirmed
            success = response[0]
            message = response[1]
            length = len(response)
            if length > 2:
                pass
            1
            smType = SystemMessages.SM_TYPE.Error
            if length > 3:
                pass
            1
            item = None
            SystemMessages.pushMessage(message, smType)
            Waiting.hide('buyItem')
        else:
            RequestState.sent(state)
            item = self._data.getInvItem(itemCD)
            success = item is not None
        if success and item is not None:
            if inInventory and len(eqs):
                message = self._getConflictedEqsMsg(eqs)
                yield async_showConfirmDialog('removeIncompatibleEqs', customMessage = message)
                isConfirmed = invVehItem is not None
                if not isConfirmed:
                    return None
            
            Waiting.show('applyModule')
            y
