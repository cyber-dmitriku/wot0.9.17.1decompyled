# Source Generated with Decompyle++
# File: listeners.pyc (Python 2.6)

from CurrentVehicle import g_currentVehicle
from debug_utils import LOG_DEBUG
from gui.ClientUpdateManager import g_clientUpdateManager
from gui.Scaleform.techtree import _VEHICLE, _TURRET, _GUN, _RESEARCH_ITEMS
INV_ITEM_VCDESC_KEY = 'compDescr'
CACHE_VEHS_LOCK_KEY = 'vehsLock'
STAT_DIFF_KEY = 'stats'
INVENTORY_DIFF_KEY = 'inventory'
CACHE_DIFF_KEY = 'cache'
_STAT_DIFF_FORMAT = STAT_DIFF_KEY + '.{0:>s}'
_INV_DIFF_FORMAT = INVENTORY_DIFF_KEY + '.{0:d}'
CREDITS_DIFF_KEY = _STAT_DIFF_FORMAT.format('credits')
GOLD_DIFF_KEY = _STAT_DIFF_FORMAT.format('gold')
FREE_XP_DIFF_KEY = _STAT_DIFF_FORMAT.format('freeXP')
UNLOCKS_DIFF_KEY = _STAT_DIFF_FORMAT.format('unlocks')
VEH_XP_DIFF_KEY = _STAT_DIFF_FORMAT.format('vehTypeXP')
ELITE_DIFF_KEY = _STAT_DIFF_FORMAT.format('eliteVehicles')
INV_VEHS_DIFF_KEY = _INV_DIFF_FORMAT.format(_VEHICLE)
INV_TURRET_DIFF_KEY = _INV_DIFF_FORMAT.format(_TURRET)
INV_GUN_DIFF_KEY = _INV_DIFF_FORMAT.format(_GUN)

class StatsListener(object):
    
    def __init__(self):
        super(StatsListener, self).__init__()
        self._StatsListener__page = None

    
    def __del__(self):
        LOG_DEBUG('StatsListener deleted')

    
    def startListen(self, page):
        self._StatsListener__page = page
        g_clientUpdateManager.addCallbacks({
            CREDITS_DIFF_KEY: self._onCreditsUpdate,
            GOLD_DIFF_KEY: self._onGoldUpdate,
            FREE_XP_DIFF_KEY: self._onFreeXPUpdate,
            UNLOCKS_DIFF_KEY: self._onUnlocksUpdate,
            VEH_XP_DIFF_KEY: self._onVehiclesXPUpdate,
            ELITE_DIFF_KEY: self._onEliteVehiclesUpdate })

    
    def stopListen(self):
        g_clientUpdateManager.removeObjectCallbacks(self)
        self._StatsListener__page = None

    
    def _onCreditsUpdate(self, credits):
        self._StatsListener__page.invalidateCredits(credits)

    
    def _onGoldUpdate(self, gold):
        self._StatsListener__page.invalidateGold(gold)

    
    def _onFreeXPUpdate(self, freeXP):
        self._StatsListener__page.invalidateFreeXP(freeXP)

    
    def _onEliteVehiclesUpdate(self, elites):
        self._StatsListener__page.invalidateElites(elites)

    
    def _onVehiclesXPUpdate(self, xps):
        self._StatsListener__page.invalidateVTypeXP(xps)

    
    def _onUnlocksUpdate(self, unlocks):
        self._StatsListener__page.invalidateUnlocks(unlocks)



class InventoryListener(object):
    
    def __init__(self):
        super(InventoryListener, self).__init__()
        self._InventoryListener__page = None

    
    def __del__(self):
        LOG_DEBUG('InventoryListener deleted')

    
    def startListen(self, page):
        self._InventoryListener__page = page
        g_clientUpdateManager.addCallbacks({
            INVENTORY_DIFF_KEY: self._onInventoryUpdate,
            CACHE_DIFF_KEY: self._onCacheUpdate,
            INV_VEHS_DIFF_KEY: self._onVehiclesUpdate,
            INV_TURRET_DIFF_KEY: self._onVehicleModelUpdate,
            INV_GUN_DIFF_KEY: self._onVehicleModelUpdate })

    
    def stopListen(self):
        g_clientUpdateManager.removeObjectCallbacks(self)
        self._InventoryListener__page = None

    
    def _onInventoryUpdate(self, data):
        self._InventoryListener__page.invalidateInventory(data)

    
    def _onCacheUpdate(self, cache):
        if CACHE_VEHS_LOCK_KEY in cache:
            vehLocks = cache.get(CACHE_VEHS_LOCK_KEY)
            if vehLocks and len(vehLocks):
                self._InventoryListener__page.invalidateVehLocks(vehLocks)
            
        

    
    def _onVehiclesUpdate(self, vehicles):
        if vehicles is not None:
            vehInvID = -1
            if g_currentVehicle.isPresent():
                vehInvID = g_currentVehicle.vehicle.inventoryId
            
            if vehicles.get(INV_ITEM_VCDESC_KEY, { }).get(vehInvID) is not None:
                g_currentVehicle.update()
            
        

    
    def _onVehicleModelUpdate(self, *args):
        g_hangarSpace = g_hangarSpace
        import gui.Scaleform.utils.HangarSpace
        g_hangarSpace.refreshVehicle()



