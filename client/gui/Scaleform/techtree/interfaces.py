# Source Generated with Decompyle++
# File: interfaces.pyc (Python 2.6)

import BigWorld
from AccountCommands import RES_SUCCESS
from debug_utils import LOG_ERROR, LOG_DEBUG
from functools import partial
import enumerations
from gui import SystemMessages, makeHtmlString
from gui.Scaleform.techtree import _VEHICLE, _RESEARCH_ITEMS, NODE_STATE, RequestState
from gui.Scaleform.techtree.custom_items import _makeShopVehicle
from gui.Scaleform.utils import functions, gui_items
from gui.Scaleform.windows import UIInterface
from gui.Scaleform.Waiting import Waiting
from items import getTypeInfoByIndex, vehicles
from helpers import i18n

class _Py_BaseScriptHandler(object):
    
    def request4Unlock(self, itemCD, parentID, unlockIdx, xpCost):
        pass

    
    def request4Buy(self, itemCD):
        pass

    
    def requestToolTip(self, pickleDump, price):
        pass

    
    def showSystemMessage(self, typeString, message):
        pass



class _AS_DisplayRoot(object):
    
    def setNodesStates(self, primary, data):
        pass

    
    def setNext2Unlock(self, data):
        pass

    
    def setVehicleTypeXP(self, xps):
        pass

    
    def setInventoryItems(self, data):
        pass

    
    def useXMLDumping(self):
        pass



class ItemsInterface(UIInterface):
    MSG_SCOPE = enumerations.Enumeration('Message scope', [
        ('Unlocks', (lambda entity, msg: '#system_messages:unlocks/{0:>s}/{1:>s}'.format(entity, msg))),
        ('Shop', (lambda entity, msg: '#system_messages:shop/{0:>s}/{1:>s}'.format(entity, msg))),
        ('Inventory', (lambda entity, msg: '#system_messages:inventory/{0:>s}/{1:>s}'.format(entity, msg))),
        ('Dialog', (lambda entity, msg: '#dialogs:techtree/{0:>s}/{1:>s}'.format(entity, msg)))], instance = enumerations.CallabbleEnumItem)
    
    def __init__(self, data):
        super(ItemsInterface, self).__init__()
        self._data = data
        self._displayRoot = None

    
    def unlockItem(self, unlockCD, vehCD, unlockIdx, xpCost):
        if self._validateItem2Unlock(unlockCD, vehCD, unlockIdx, xpCost):
            message = self._getUnlockConfirmMsg(unlockCD, xpCost)
            functions.showConfirmDialog('confirmUnlock', partial(self._doUnlockItem, unlockCD, vehCD, unlockIdx, xpCost), customMessage = message)
        

    
    def buyVehicle(self, vehCD):
        if not self._data.hasInvItem(vehCD):
            price = self._data.getShopPrice(vehCD)
            if price is None:
                self._showMessage4Vehicle(self.MSG_SCOPE.Shop, 'not_found', vehCD)
                return None
            credits = self._data._accCredits
            gold = self._data._accGold
            if (credits, gold) >= price:
                (_, nationID, itemID) = vehicles.parseIntCompactDescr(vehCD)
                self.call('common.showVehicleBuyDialog', [
                    _makeShopVehicle(itemID, nationID, price).pack()])
            elif price[0] > 0:
                pass
            
            _credits = 0
            if price[1] > 0:
                pass
            1
            _gold = 0
            self._showMessage4Vehicle(self.MSG_SCOPE.Shop, 'not_enough_money', vehCD, price = gui_items.formatPrice([
                _credits,
                _gold]))
        else:
            self._showMessage4Vehicle(self.MSG_SCOPE.Inventory, 'already_exists', vehCD, type = SystemMessages.SM_TYPE.Warning)

    
    def pushSystemMessage(self, typeString, message):
        type = SystemMessages.SM_TYPE.lookup(typeString)
        if type is None:
            type = SystemMessages.SM_TYPE.Error
        
        SystemMessages.pushMessage(message, type)

    
    def invalidateCredits(self, credits):
        result = self._data.invalidateCredits(credits)
        if len(result):
            self._displayRoot.setNodesStates(NODE_STATE.ENOUGH_MONEY, result)
        

    
    def invalidateGold(self, gold):
        result = self._data.invalidateGold(gold)
        if len(result):
            self._displayRoot.setNodesStates(NODE_STATE.ENOUGH_MONEY, result)
        

    
    d
