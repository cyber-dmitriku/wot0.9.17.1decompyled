# Source Generated with Decompyle++
# File: ToolTipManager.pyc (Python 2.6)

from helpers import i18n
__author__ = 'i_maliavko'
import ResMgr
import BigWorld
import json
import dossiers
import gui
import pickle
import constants
import nations
from debug_utils import *
from helpers.i18n import makeString
from adisp import process, async
from CurrentVehicle import g_currentVehicle
from gui.Scaleform.techtree import NODE_STATE
from gui.Scaleform.techtree.techtree_dp import g_techTreeDP
from gui.Scaleform.utils import ParametersCache, ItemsParameters, dossiers_utils
from gui.Scaleform.windows import UIInterface
from gui.Scaleform.utils.requesters import StatsRequester, Requester
from gui.Scaleform.utils.gui_items import ShopItem, InventoryVehicle, VehicleItem, _ICONS_MASK, getItemByCompact
from gui.Scaleform.utils.functions import stripShortDescrTags, getShortDescr, isModuleFitVehicle, makeTooltip
from gui.Scaleform.utils.dossiers_utils import getAchievementType, MEDALS_SERIES, getAchievementSection, ACHIEVEMENTS_NEXT_LEVEL_VALUES
from gui.Scaleform.utils.RareAchievementsCache import g_rareAchievesCache
from items import ITEM_TYPE_NAMES, vehicles, artefacts
from items.tankmen import getSkillsConfig, MAX_SKILL_LEVEL, PERKS, SKILLS_BY_ROLES, COMMANDER_ADDITION_RATIO
from gui.ClientUpdateManager import g_clientUpdateManager

class ToolTipManager(UIInterface):
    VEHICLE_PARAMS = {
        'lightTank': ('speedLimits', 'enginePowerPerTon', 'chassisRotationSpeed', 'circularVisionRadius'),
        'mediumTank': ('speedLimits', 'enginePowerPerTon', 'chassisRotationSpeed', 'damageAvgPerMinute'),
        'heavyTank': ('hullArmor', 'turretArmor', 'damageAvg', 'piercingPower'),
        'SPG': ('damageAvg', 'explosionRadius', 'shotDispersionAngle', 'aimingTime', 'reloadTimeSecs'),
        'AT-SPG': ('speedLimits', 'chassisRotationSpeed', 'damageAvgPerMinute', 'shotDispersionAngle', 'piercingPower'),
        'default': ('speedLimits', 'enginePower', 'chassisRotationSpeed') }
    MODULE_PARAMS = {
        'vehicleChassis': ('maxLoad', 'rotationSpeed', 'weight'),
        'vehicleTurret': ('armor', 'rotationSpeed', 'circularVisionRadius', 'weight'),
        'vehicleGun': ('reloadTime', 'avgPiercingPower', 'avgDamage', 'dispertionRadius', 'aimingTime', 'weight'),
        'vehicleEngine': ('enginePower', 'fireStartingChance', 'weight'),
        'vehicleRadio': ('radioDistance', 'weight'),
        'optionalDevice': ('weight',) }
    
    class TOOLTIP_TYPE:
        VEHICLE = 'vehicle'
        TANKMAN = 'tankman'
        SKILL = 'skill'
        ACHIEVEMENT = 'achievement'
        MODULE = 'module'
        SHELL = 'shell'

    
    class TOOLTIP_COMPONENT:
        TECH_MAIN = 'technical_maintenance'
        HANGAR = 'hangar'
        SHOP = 'shop'
        INVENTORY = 'inventory'
        PERSONAL_CASE = 'personal_case'
        CAROUSEL = 'carousel'
        RESEARCH = 'research'
        PROFILE = 'profile'

    DEFAUL_DAILY_XP_FACTOR = 2
    
    def __init__(self):
        UIInterface.__init__(self)
        self.initialized = False
        self._ToolTipManager__eliteVehicles = set()
        self._ToolTipManager__unlocks = set()
        self._ToolTipManager__unlockPrices = dict()
        self._ToolTipManager__xpVehicles = dict()
        self._ToolTipManager__priceVehicles = dict()
        self._ToolTipManager__inventoryVehicles = dict()
        self._ToolTipManager__inventoryVehiclesDescrs = dict()
        self._ToolTipManager__vehicleTypeLock = dict()
        self._ToolTipManager__multipliedXPVehicles = list()
        self._ToolTipManager__dailyXPFactor = self.DEFAUL_DAILY_XP_FACTOR
        self._ToolTipManager__priceModifiers = 0.5
        self._ToolTipManager__dismantlingPrice = 10
        self._ToolTipManager__tankmen = dict()
        g_clientUpdateManager.addCallbacks({
            'inventory': self.onInventoryUpdate,
            'stats.unlocks': self.onUnlocksUpdate,
            'stats.vehTypeXP': self.onVehicleXPUpdate,
            'stats.eliteVehicles': self.onEliteVehiclesUpdate,
            'cache.vehsLock': self.onInventoryUpdate })

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self.flashMgr = proxy.getMember('tooltipManager')
        if self.flashMgr is not None:
            self.flashMgr.resync()
            self.flashMgr.script = self
        else:
            LOG_ERROR('Can not getting tooltip manager flash representation')

    
    def dispossessUI(self):
        if self.flashMgr is not None:
            self.flashMgr.script = None
            self.flashMgr = None
        
        UIInterface.dispossessUI(self)

    
    def clear(self):
        g_clientUpdateManager.removeObjectCallbacks(self)
        self.initialized = False

    
    def request(self, callback):
        import time as time
        startTime = time.time()
        self.initialized = False
        yield self._ToolTipManager__getAccountInfo()
        yield self._ToolTipManager__getVehiclesInfo()
        self._ToolTipManager__readVehiclesData()
        elapsed = time.time() - startTime
        LOG_DEBUG("ToolTipManager's cache initialization has been completed. Time elapsed: %.5fs" % elapsed)
        self.initialized = True
        callback(True)

    request = async(process(request))
    
    def __getAccountInfo(self, callback):
        yield StatsRequester().getSellPriceModifiers()
        self._ToolTipManager__priceModifiers = None
        yield StatsRequester().getPaidRemovalCost()
        self._ToolTipManager__dismantlingPrice = None
        callback(True)

    _ToolTipManager__getAccountInfo = async(process(__getAccountInfo))
    
    def __getVehiclesInfo(self, callback):
        yield Requester('vehicle').getFromInventory()
        inventoryVehicles = None
        continue
        self._ToolTipManager__inventoryVehicles = _[1]([ (v.inventoryId, v) for v in inventoryVehicles ])
        continue
        self._ToolTipManager__inventoryVehiclesDescrs = _[2]([ (v.inventoryId, v.compactDescr) for v in inventoryVehicles ])
        yield StatsRequester().getVehiclesPrices(self._ToolTipManager__inventoryVehiclesDescrs.values())
        vehPrices = []
        self._ToolTipManager__priceVehicles = dict(zip(self._ToolTipManager__inventoryVehiclesDescrs.values(), vehPrices))
        yield StatsRequester().getVehicleTypeExperiences()
        self._ToolTipManager__xpVehicles = dict
        yield StatsRequester().getUnlocks()
        self._ToolTipManager__unlocks = []
        yield StatsRequester().getEliteVehicles()
        self._ToolTipManager__eliteVehicles = dict
        yield StatsRequester().getMultipliedXPVehicles()
        self._ToolTipManager__multipliedXPVehicles = None
        yield StatsRequester().getVehicleTypeLocks()
        self._ToolTipManager__vehicleTypeLock = None
        yield StatsRequester().getGlobalVehicleLocks()
        self._ToolTipManager__globalVehicleLocks = None
        yield StatsRequester().getDailyXPFactor()
        self._ToolTipManager__dailyXPFactor = None
        if not self._ToolTipManager__dailyXPFactor:
            pass
        self._ToolTipManager__dailyXPFactor = self.DEFAUL_DAILY_XP_FACTOR
        yield Requester('tankman').getFromInventory()
        tankmen = None
        continue
        self._ToolTipManager__tankmen = _[3]([ (t.inventoryId, t) for t in tankmen ])
        callback(True)

    _ToolTipManager__getVehiclesInfo = async(process(__getVehiclesInfo))
    
    def _ToolTipManager__readVehiclesData(self):
        for nation in nations.AVAILABLE_NAMES:
            for item in vehicles.g_list.getList(nations.INDICES[nation]).itervalues():
                vehicleDescr = vehicles.VehicleDescr(typeName = item['name'])
                for unlockDescr in vehicleDescr.type.unlocksDescrs:
                    prices = self._ToolTipManager__unlockPrices.setdefault(unlockDescr[1], dict())
                    prices[vehicleDescr.type.compactDescr] = unlockDescr[0]
                
            
        

    
    def _ToolTipManager__getUnlockPrice(self, compactDescr, parentVehicle = None):
        (item_type_id, _, _) = vehicles.parseIntCompactDescr(compactDescr)
        if item_type_id == vehicles._VEHICLE:
            g_windowsManager = g_windowsManager
            import gui.WindowsManager
            freeXP = getattr(g_windowsManager.window, 'freeXP', 0)
            g_techTreeDP.load()
            (isAvailable, props) = g_techTreeDP.isNext2Unlock(compactDescr, self._ToolTipManager__unlocks, self._ToolTipManager__xpVehicles, freeXP)
            pricesDict = self._ToolTipManager__getUnlockPrices(compactDescr)
            if parentVehicle is not None:
                return (isAvailable, pricesDict.get(parentVehicle.descriptor.type.compactDescr, 0))
            return (isAvailable, props.xpCost)
        isAvailable = compactDescr in self._ToolTipManager__unlocks
        pricesDict = self._ToolTipManager__getUnlockPrices(compactDescr)
        if not pricesDict:
            return (isAvailable, 0)
        if parentVehicle is not None:
            return (isAvailable, pricesDict.get(parentVehicle.descriptor.type.compactDescr, 0))
        continue
        vehsCompDescrs = _[1]
        if not vehsCompDescrs:
            vehsCompDescrs = pricesDict.keys()
        
        continue
        return ([], _[2]([ pricesDict[vcd] for vcd in vehsCompDescrs ]))

    
    def _ToolTipManager__getUnlockPrices(self, compactDescr):
        return self._ToolTipManager__unlockPrices.get(compactDescr, dict())

    
    def onUnlocksUpdate(self, unlocks):
        self._ToolTipManager__unlocks |= unlocks

    
    def onVehicleXPUpdate(self, xps):
        self._ToolTipManager__xpVehicles.update(xps)

    
    def onEliteVehiclesUpdate(self, elites):
        self._ToolTipManager__eliteVehicles |= elites

    
    def onInventoryUpdate(self, *args):
        yield self._ToolTipManager__getVehiclesInfo()

    onInventoryUpdate = process(onInventoryUpdate)
    
    def _ToolTipManager__getSerializedToolTipData(self, tooltipType, tooltipComponent, data):
        return json.dumps(self._ToolTipManager__getToolTipData(tooltipType, tooltipComponent, data))

    
    def _ToolTipManager__getToolTipData(self, tooltipType, tooltipComponent, data):
        return {
            'type': tooltipType,
            'component': tooltipComponent,
            'data': data }

    
    def _ToolTipManager__getVehicleStatsBlock(self, vehicle, xp = True, dayliXP = True, unlockPrice = True, buyPrice = True, sellPrice = True, parentVehicle = None):
        result = list()
        if xp:
            xpValue = self._ToolTipManager__xpVehicles.get(vehicle.descriptor.type.compactDescr, 0)
            if xpValue:
                result.append([
                    'xp',
                    xpValue])
            
        
        if dayliXP:
            if vehicle.descriptor.type.compactDescr not in self._ToolTipManager__multipliedXPVehicles:
                result.append([
                    'dailyXPFactor',
                    self._ToolTipManager__dailyXPFactor])
            
        
        if unlockPrice:
            result.append([
                'unlock_price',
                self._ToolTipManager__getUnlockPrice(vehicle.descriptor.type.compactDescr, parentVehicle)[1]])
        
        if buyPrice and vehicle.compactDescr not in self._ToolTipManager__inventoryVehiclesDescrs.values():
            if type(vehicle) == ShopItem:
                if vehicle.isPremium:
                    pass
                1
            
            result.append([
                'buy_price',
                0])
        
        if sellPrice:
            if type(vehicle) != ShopItem:
                pass
            1
            'sell_price'([
                self._ToolTipManager__priceVehicles.get(vehicle.compactDescr, 0),
                0])
        
        return result

    
    def _ToolTipManager__getVehicleParameterValue(self, paramName, paramsDict, rawParamsDict):
        if paramName == 'enginePowerPerTon':
            return (paramName, BigWorld.wg_getNiceNumberFormat(rawParamsDict['enginePowerPerTon']))
        if paramName == 'damageAvgPerMinute':
            return (paramName, BigWorld.wg_getIntegralFormat(rawParamsDict[paramName]))
        if paramName == 'damageAvg':
  
