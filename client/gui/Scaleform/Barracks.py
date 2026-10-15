# Source Generated with Decompyle++
# File: Barracks.pyc (Python 2.6)

import BigWorld
from account_helpers.AccountSettings import AccountSettings, BARRACKS_FILTER
from adisp import process
from debug_utils import LOG_DEBUG
from items.tankmen import getSkillsConfig, ROLES
from helpers.i18n import convert, makeString
from gui import SystemMessages, nationCompareByIndex
from PlayerEvents import g_playerEvents
from gui.Scaleform.TankmenInterface import TankmenInterface
from gui.Scaleform.Waiting import Waiting
from gui.Scaleform.windows import UIInterface
from gui.Scaleform.utils.requesters import Requester, StatsRequester
from CurrentVehicle import g_currentVehicle
from account_helpers.AccountPrebattle import AccountPrebattle

class Barracks(UIInterface):
    
    def __init__(self):
        UIInterface.__init__(self)
        self.tankmenInterface = TankmenInterface(self)
        self.filter = dict(AccountSettings.getFilter(BARRACKS_FILTER))

    
    def __del__(self):
        LOG_DEBUG('BarracksHandler deleted')

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self.tankmenInterface.populateUI(proxy)
        self.uiHolder.movie.backgroundAlpha = 0
        self.uiHolder.movie.wg_inputKeyMode = 1
        self.uiHolder.addExternalCallbacks({
            'barracks.update': self.onUpdate,
            'barracks.setFilter': self.onSetFilter,
            'barracks.invalidataTanksList': self.onInvalidateTanksList,
            'barracks.showRecruitWindow': self.onShowRecruitWindow,
            'barracks.checkBerthBuyDialog': self.onCheckBerthBuyDialog,
            'barracks.buyBerths': self.onBuyBerths })
        if AccountPrebattle.get():
            AccountPrebattle.get().onPlayerStateChanged += self.onSquadPlayerStateChange
        
        g_playerEvents.onShopResync += self.update
        self._Barracks__setTankmenFilter()
        Waiting.hide('loadPage')

    
    def dispossessUI(self):
        g_playerEvents.onShopResync -= self.update
        if AccountPrebattle.get():
            AccountPrebattle.get().onPlayerStateChanged -= self.onSquadPlayerStateChange
        
        self.uiHolder.removeExternalCallbacks('barracks.update', 'barracks.setFilter', 'barracks.invalidataTanksList', 'barracks.showRecruitWindow', 'barracks.checkBerthBuyDialog', 'barracks.buyBerths')
        self.tankmenInterface.dispossessUI()
        UIInterface.dispossessUI(self)

    
    def onSquadPlayerStateChange(self, id, roster):
        self.update()

    
    def onUpdate(self, callbackID):
        self.update()

    
    def update(self):
        self._Barracks__updateTankmen()

    
    def onInvalidateTanksList(self, callbackID):
        self._Barracks__updateTanksList()

    
    def onCheckBerthBuyDialog(self, callbackID):
        yield StatsRequester().getGold()
        gold = None
        yield StatsRequester().getTankmenBerthsCount()
        berths = None
        yield StatsRequester().getBerthsPrices()
        berthsPrices = None
        berthPrice = BigWorld.player().shop.getNextBerthPackPrice(berths, berthsPrices)
        self.call('barracks.showBerthBuyDialog', [
            gold,
            berthPrice,
            berthsPrices[1]])

    onCheckBerthBuyDialog = process(onCheckBerthBuyDialog)
    
    def onBuyBerths(self, callbackID):
        Waiting.show('buyBerths')
        yield StatsRequester().getTankmenBerthsCount()
        berths = None
        yield StatsRequester().getBerthsPrices()
        berthsPrices = None
        berthPrice = BigWorld.player().shop.getNextBerthPackPrice(berths, berthsPrices)
        yield StatsRequester().buyBerths()
        success = None
        if success:
            self.update()
            SystemMessages.g_instance.pushI18nMessage('#system_messages:buy_berths/success', berthPrice, type = SystemMessages.SM_TYPE.PurchaseForGold)
        else:
            SystemMessages.g_instance.pushI18nMessage('#system_messages:buy_berths/server_error', type = SystemMessages.SM_TYPE.Error)
        self.uiHolder.updateAccountInfo()
        Waiting.hide('buyBerths')

    onBuyBerths = process(onBuyBerths)
    
    def __updateTanksList(self):
        yield Requester('vehicle').getFromInventory()
        modulesAll = None
        modulesAll.sort()
        data = [
            len(modulesAll)]
        filteredItemsCount = 0
        for module in modulesAll:
            if (self.filter['nation'] != -1 or self.filter['nation'] != module.descriptor.type.id[0] or self.filter['tankType'] != -1) and self.filter['tankType'] != module.type:
                filteredItemsCount += 1
                continue
            
            data.append(module.type)
            data.append(module.descriptor.type.id[0])
            data.append(module.descriptor.type.id[1])
            data.append(module.descriptor.type.shortUserString)
        
        data[0] -= filteredItemsCount
        self.call('barracks.updateTanksList', data)

    _Barracks__updateTanksList = process(__updateTanksList)
    
    def _Barracks__setTankmenFilter(self):
        data = []
        data.append(self.filter['nation'])
        data.append(self.filter['role'])
        data.append(self.filter['tankType'])
        data.append(self.filter['location'])
        data.append(self.filter['nationID'])
        self.call('barracks.setTankmenFilter', data)

    
    def onSetFilter(self, callbackID, nation, role, tankType, location, nationID):
        self.filter['nation'] = nation
        self.filter['role'] = role
        self.filter['tankType'] = tankType
        self.filter['location'] = location
        self.filter['nationID'] = nationID
        AccountSettings.setFilter(BARRACKS_FILTER, self.filter)
        self._Barracks__updateTankmen()

    
    def onShowRecruitWindow(self, callbackID):
        yield StatsRequester().getCredits()
        credits = None
        yield StatsRequester().getGold()
        gold = None
        yield StatsRequester().getTankmanCost()
        upgradeParams = None
        data = [
            credits,
            gold,
            round(upgradeParams[1]['credits']),
            upgradeParams[2]['gold'],
            len(ROLES)]
        for role in ROLES:
            data.append(role)
            data.append(convert(getSkillsConfig()[role]['userString']))
        
        yield StatsRequester().getUnlocks()
        unlocks = None
        yield Requester('vehicle').getFromShop()
        modulesAll = None
        modulesAll.sort()
        for module in modulesAll:
            compdecs = module.descriptor.type.compactDescr
            if compdecs in unlocks:
                data.append(module.type)
                data.append(module.descriptor.type.id[0])
                data.append(module.descriptor.type.id[1])
                data.append(module.descriptor.type.shortUserString)
                continue
        
        self.call('barracks.showRecruit', data)

    onShowRecruitWindow = process(onShowRecruitWindow)
    
    def __updateTankmen(self):
        Waiting.show('updateTankmen')
        yield Requester('tankman').getFromInventory()
        tankmen = None
        yield Requester('vehicle').getFromInventory()
        vcls = None
        yield StatsRequester().getTankmenBerthsCount()
        slots = None
        yield StatsRequester().getTankmenBerthsCount()
        berths = None
        yield StatsRequester().getBerthsPrices()
        berthsPrices = None
        berthPrice = BigWorld.player().shop.getNextBerthPackPrice(berths, berthsPrices)
        data = [
            len(tankmen),
            slots,
            0,
            BigWorld.wg_getGoldFormat(berthPrice),
            berthsPrices[1]]
        TANKMEN_ROLES_ORDER = {
            'commander': 0,
            'gunner': 1,
            'driver': 2,
            'radioman': 3,
            'loader': 4 }
        
        def tankmenSortFunc(first, second):
            if first is None or second is None:
                return 1
            res = nationCompareByIndex(first.nation, second.nation)
            if res != 0:
                return res
            if first.isInTank and not (second.isInTank):
                return -1
            if not (first.isInTank) and second.isInTank:
                return 1
            if first.isInTank and second.isInTank:
                (tman1vehicle, tman2vehicle) = (None, None)
                for vcl in vcls:
                    if vcl.inventoryId == first.vehicleID:
                        tman1vehicle = vcl
                    
                    if vcl.inventoryId == second.vehicleID:
                        tman2vehicle = vcl
                    
                    if tman1vehicle is not None and tman2vehicle is not None:
                        break
                        continue
                
                res = tman1vehicle.__cmp__(tman2vehicle)
                if res != 0:
                    return res
                if TANKMEN_ROLES_ORDER[first.descriptor.role] < TANKMEN_ROLES_ORDER[second.descriptor.role]:
                    return -1
                if TANKMEN_ROLES_ORDER[first.descriptor.role] > TANKMEN_ROLES_ORDER[second.descriptor.role]:
                    return 1
            
            if first.lastname < second.lastname:
                return -1
            if first.lastname > second.lastname:
                return 1
            return 1

        tankmen.sort(tankmenSortFunc)
        for tankman in tankmen:
            if not tankman.isInTank:
                data[2] += 1
            
            if not self.filter['nation'] != -1 or tankman.nation != self.filter['nation']:
                if not self.filter['role'] != -1 or tankman.descriptor.role != self.filter['role']:
                    if not self.filter['tankType'] != -1 or tankman.vehicleType != self.filter['tankType']:
                        if not self.filter['location'] == 'tanks' or tankman.isInTank != True:
                            if self.filter['location'] == 'barracks' or tankman.isInTank == True or self.filter['nationID'] != None:
                                if self.filter['location'] != tankman.vehicle.type.id[1] or self.filter['nationID'] != tankman.nation:
                                    continue
                                
            (slot, vehicleID) = (None, None)
            if tankman.isInTank == True:
                for vcl in vcls:
                    if vcl.inventoryId == tankman.vehicleID:
                        vehicle = vcl
                        vehicleID = vehicle.inventoryId
                        break
                        continue
                    (None, None)
                
                for i in range(len(vehicle.crew)):
                    if vehicle.crew[i] == tankman.inventoryId:
                        slot = i
                        break
                        continue
                
            
            data.append(tankman.firstname)
            data.append(tankman.lastname)
            data.append(tankman.rank)
            data.append(tankman.roleLevel)
            data.append(tankman.role)
            data.append(tankman.vehicle.type.shortUserString)
            data.append(tankman.icon)
            data.append(tankman.iconRank)
            data.append(tankman.iconRole)
            data.append(tankman.vehicleIconContour)
            data.append(tankman.inventoryId)
            data.append(tankman.nation)
            data.append(tankman.vehicle.type.id[1])
            data.append(slot)
            data.append(tankman.descriptor.role)
            data.append(tankman.vehicleType)
            data.append(tankman.isInTank)
            if tankman.isInTank and g_currentVehicle.isPresent():
                pass
            1
            tankman.vehicleID == g_currentVehicle.vehicle.inventoryId(False)
            data.append(vehicleID)
            data.append(tankman.pack())
            if tankman.isInTank:
                pass
            1
            (isLocked, msg) = (False, '')
            data.append(isLocked)
            data.append(msg)
            if tankman.isInTank:
                pass
            1
            vehicle.repairCost > 0(None)
            if tankman.isInTank:
                pass
            1
            vehicle.type == tankman.vehicleType(True)
            if tankman.isInTank:
                pass
            1
            vehicle.shortName == tankman.vehicle.type.shortUserString(True)
        
        self.call('barracks.setTankmen', data)
        self.call('PersonalcCaseManager.update', [])
        Waiting.hide('updateTankmen')

    _Barracks__updateTankmen = process(__updateTankmen)


