# Source Generated with Decompyle++
# File: __init__.pyc (Python 2.6)

from collections import namedtuple
from items import ITEM_TYPE_NAMES
from items.vehicles import _VEHICLE, _TURRET, _GUN, _CHASSIS, _RADIO, _ENGINE
import nations
SMALL_ICONS_PATH = '../maps/icons/%(type)s/small/%(unicName)s.png'
TREE_SHARED_REL_FILE_PATH = 'gui/flash/techtree/tree-shared.xml'
NATION_TREE_REL_FILE_PATH = 'gui/flash/techtree/%s-tree.xml'
USE_XML_DUMPING = False
_VEHICLE_TYPE_NAME = ITEM_TYPE_NAMES[_VEHICLE]
_GUN_TYPE_NAME = ITEM_TYPE_NAMES[_GUN]
_TURRET_TYPE_NAME = ITEM_TYPE_NAMES[_TURRET]
_PREMIUM_TAGS = frozenset([
    'premium'])
_RESEARCH_ITEMS = (_GUN, _TURRET, _RADIO, _ENGINE, _CHASSIS)
MAX_PATH_LIMIT = 5

class NODE_STATE:
    LOCKED = 1
    NEXT_2_UNLOCK = 2
    UNLOCKED = 4
    ENOUGH_XP = 8
    ENOUGH_MONEY = 16
    IN_INVENTORY = 32
    WAS_IN_BATTLE = 64
    ELITE = 128
    PREMIUM = 256
    SELECTED = 512
    AUTO_UNLOCKED = 1024
    INSTALLED = 2048
    SHOP_ACTION = 4096
    
    def add(cls, state, flag):
        if not state & flag:
            state |= flag
            return state
        return -1

    add = classmethod(add)
    
    def addIfNot(cls, state, flag):
        if not state & flag:
            state |= flag
        
        return state

    addIfNot = classmethod(addIfNot)
    
    def remove(cls, state, flag):
        if state & flag > 0:
            state ^= flag
            return state
        return -1

    remove = classmethod(remove)
    
    def removeIfHas(cls, state, flag):
        if state & flag > 0:
            state ^= flag
        
        return state

    removeIfHas = classmethod(removeIfHas)
    
    def isAvailable2Unlock(cls, state):
        if not (state & cls.UNLOCKED) and state & cls.NEXT_2_UNLOCK:
            pass
        return state & cls.ENOUGH_XP

    isAvailable2Unlock = classmethod(isAvailable2Unlock)
    
    def isAvailable2Buy(cls, state):
        if not (state & cls.IN_INVENTORY) and state & cls.UNLOCKED:
            pass
        return state & cls.ENOUGH_MONEY

    isAvailable2Buy = classmethod(isAvailable2Buy)
    
    def isBuyForCredits(cls, state):
        if state & cls.UNLOCKED and not (state & cls.IN_INVENTORY):
            pass
        return not (state & cls.PREMIUM)

    isBuyForCredits = classmethod(isBuyForCredits)
    
    def isBuyForGold(cls, state):
        if state & cls.UNLOCKED and not (state & cls.IN_INVENTORY):
            pass
        return state & cls.PREMIUM

    isBuyForGold = classmethod(isBuyForGold)
    
    def change2Unlocked(cls, state):
        if state & NODE_STATE.UNLOCKED > 0:
            return -1
        if state & cls.LOCKED > 0:
            state ^= cls.LOCKED
        
        if state & cls.NEXT_2_UNLOCK > 0:
            state ^= cls.NEXT_2_UNLOCK
            if state & cls.ENOUGH_XP > 0:
                state ^= cls.ENOUGH_XP
            
        
        state |= cls.UNLOCKED
        return state

    change2Unlocked = classmethod(change2Unlocked)

UnlockProps = namedtuple('UnlockProps', 'parentID unlockIdx xpCost required')

def makeDefUnlockProps():
    return UnlockProps(0, -1, 0, set())


class SelectedNation(object):
    _SelectedNation__index = None
    
    def byDefault(cls):
        if cls._SelectedNation__index is None:
            g_currentVehicle = g_currentVehicle
            import CurrentVehicle
            if g_currentVehicle.isPresent():
                pass
            1
            cls._SelectedNation__index = 0
        

    byDefault = classmethod(byDefault)
    
    def select(cls, index):
        cls._SelectedNation__index = index

    select = classmethod(select)
    
    def getIndex(cls):
        return cls._SelectedNation__index

    getIndex = classmethod(getIndex)
    
    def getName(cls):
        return nations.NAMES[cls._SelectedNation__index]

    getName = classmethod(getName)


class RequestState(object):
    _RequestState__states = set()
    
    def sent(cls, name):
        cls._RequestState__states.add(name)

    sent = classmethod(sent)
    
    def received(cls, name):
        if name in cls._RequestState__states:
            cls._RequestState__states.remove(name)
        

    received = classmethod(received)
    
    def inProcess(cls, name):
        return name in cls._RequestState__states

    inProcess = classmethod(inProcess)

__all__ = [
    'USE_XML_DUMPING',
    'NODE_STATE',
    'RequestState',
    'SelectedNation',
    'UnlockProps',
    'makeDefUnlockProps',
    'listeners',
    'tech_tree_dp',
    'customs_items',
    'dumpers',
    'data',
    'MAX_PATH_LIMIT',
    '_VEHICLE',
    '_VEHICLE_TYPE_NAME',
    '_PREMIUM_TAGS',
    '_RESEARCH_ITEMS',
    '_TURRET',
    '_TURRET_TYPE_NAME',
    '_GUN',
    '_GUN_TYPE_NAME',
    'SMALL_ICONS_PATH',
    'TREE_SHARED_REL_FILE_PATH',
    'NATION_TREE_REL_FILE_PATH']

