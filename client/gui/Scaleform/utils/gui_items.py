# Source Generated with Decompyle++
# File: gui_items.pyc (Python 2.6)

import BigWorld
import math
import pickle
import nations
from AccountCommands import LOCK_REASON
from items.vehicles import VehicleDescr, getDictDescr, getDefaultAmmoForGun, VEHICLE_CLASS_TAGS
from items import ITEM_TYPE_NAMES, ITEM_TYPE_INDICES, getTypeInfoByName
from CurrentVehicle import g_currentVehicle
from helpers.i18n import makeString
from adisp import async, process
from debug_utils import *
from gui import SystemMessages, GUI_NATIONS, GUI_NATIONS_ORDER_INDEX, nationCompareByIndex, GUI_SETTINGS
from items.tankmen import TankmanDescr, getNationConfig, getSkillsConfig, SKILLS_BY_ROLES, MAX_SKILL_LEVEL, ACTIVE_SKILLS
from items import vehicles
from helpers.i18n import convert
from account_helpers.AccountSettings import AccountSettings
_ITEM_TYPES_ORDER = [
    'lightTank',
    'mediumTank',
    'heavyTank',
    'AT-SPG',
    'SPG',
    'vehicleGun',
    'vehicleTurret',
    'vehicleEngine',
    'vehicleChassis',
    'vehicleRadio',
    'ARMOR_PIERCING',
    'ARMOR_PIERCING_CR',
    'HOLLOW_CHARGE',
    'HIGH_EXPLOSIVE',
    'optionalDevice',
    'equipment']
_ICONS_MASK = '../maps/icons/%(type)s/%(subtype)s%(unicName)s.png'

class FittingItem(object):
    
    def __init__(self, compactDescr, itemTypeName, priceOrder = (0, 0), suitFor = []):
        self._FittingItem__userType = None
        self.compactDescr = compactDescr
        self.itemTypeName = itemTypeName
        self.priceOrder = priceOrder
        self.price = (0, 0)
        self.isCurrent = False
        self._FittingItem__suitableVehicles = suitFor
        self.index = None

    
    def isRemovable(self):
        if self.type == ITEM_TYPE_NAMES[9]:
            return self.descriptor['removable']
        return True

    isRemovable = property(isRemovable)
    
    def userType(self):
        '''
\t\tTranslated item type
\t\t'''
        if self._FittingItem__userType is None:
            self._FittingItem__userType = getTypeInfoByName(self.itemTypeName)['userString']
        
        return self._FittingItem__userType

    userType = property(userType)
    
    def type(self):
        if self.itemTypeName == ITEM_TYPE_NAMES[1]:
            tags = VEHICLE_CLASS_TAGS.intersection(self.descriptor.type.tags)
            for tag in tags:
                return tag
            
        elif self.itemTypeName == ITEM_TYPE_NAMES[10]:
            return self.descriptor['kind']
        return self.itemTypeName

    type = property(type)
    
    def getPriceByModifiers(self, sellPriceModifiers):
        return (BigWorld.player().shop.getSellPrice(self.priceOrder, sellPriceModifiers), 0)

    
    def hasTurrets(self):
        '''
\t\t@return: True if vehicle has at least one not fake turret, False otherwise
\t\t'''
        if self.itemTypeName == ITEM_TYPE_NAMES[1]:
            return len(self.descriptor.type.hull.get('fakeTurrets', { }).get('lobby', ())) != len(self.descriptor.type.turrets)
        return False

    hasTurrets = property(hasTurrets)
    
    def isPremium(self):
        return bool(self.descriptor.type.tags & frozenset(('premium',)))

    isPremium = property(isPremium)
    
    def unicName(self):
        '''
\t\tItem identificator (name in xml)
\t\t'''
        if self.itemTypeName == ITEM_TYPE_NAMES[1]:
            return self.descriptor.type.name
        return self.descriptor['name']

    unicName = property(unicName)
    
    def name(self):
        '''
\t\tTranslated item identificator (userString in xml)
\t\t'''
        if self.itemTypeName == ITEM_TYPE_NAMES[1]:
            return self.descriptor.type.userString
        return self.descriptor['userString']

    name = property(name)
    
    def longName(self):
        '''
\t\tTranslated item name (userType + identificator)
\t\t'''
        if self.itemTypeName == ITEM_TYPE_NAMES[1]:
            return getVehicleFullName(self.descriptor)
        if self.itemTypeName == ITEM_TYPE_NAMES[10]:
            if self.nation == nations.INDICES['germany']:
                caliber = float(self.descriptor['caliber']) / 10
                dimension = makeString('#item_types:shell/dimension/sm')
            elif self.nation == nations.INDICES['usa']:
                caliber = float(self.descriptor['caliber']) / 25.4
                dimension = makeString('#item_types:shell/dimension/inch')
            else:
                caliber = self.descriptor['caliber']
                dimension = makeString('#item_types:shell/dimension/mm')
            return makeString('#item_types:shell/name') % {
                'kind': makeString('#item_types:shell/kinds/' + self.descriptor['kind']),
                'name': self.name,
                'caliber': BigWorld.wg_getNiceNumberFormat(caliber),
                'dimension': dimension }
        
        try:
            return self.userType + ' ' + self.descriptor['userString']
        except KeyError:
            self.itemTypeName == ITEM_TYPE_NAMES[10]
            self.itemTypeName == ITEM_TYPE_NAMES[1]
            return self.userType


    longName = property(longName)
    
    def shortName(self):
        '''
\t\tTranslated item name for vehicle 6 letters
\t\tTranslated item name for module 10 letters
\t\t'''
        if self.itemTypeName == ITEM_TYPE_NAMES[1]:
            return self.descriptor.type.shortUserString
        return self.descriptor['shortUserString']

    shortName = property(shortName)
    
    def description(self):
        '''
\t\tTranslated description from xml
\t\t'''
        if self.itemTypeName == ITEM_TYPE_NAMES[1]:
            if self.descriptor.type.description.find('_descr') == -1:
                return self.descriptor.type.description
            return ''
        return self.descriptor['description']

    description = property(description)
    
    def level(self):
        if self.itemTypeName in (ITEM_TYPE_NAMES[9], ITEM_TYPE_NAMES[10], ITEM_TYPE_NAMES[11]):
            return 0
        if self.itemTypeName == ITEM_TYPE_NAMES[1]:
            return self.descriptor.level
        if self.descriptor.has_key('level'):
            return self.descriptor['level']
        LOG_ERROR('Module %s:%s without level' % (self.type, self.unicName))
        return 0

    level = property(level)
    
    def tableName(self):
        return self.getTableName()

    tableName = property(tableName)
    
    def getTableName(self, vehicle = None):
        '''
\t\tTranslated table name consists short description of main parameters
\t\tShort name not included
\t\t'''
        if not GUI_SETTINGS.technicalInfo:
            return ''
        ItemsParameters = ItemsParameters
        import gui.Scaleform.utils
        if self.itemTypeName in (ITEM_TYPE_NAMES[9], ITEM_TYPE_NAMES[11]):
            return self.description
        
        try:
            description = makeString('#menu:descriptions/' + self.itemTypeName)
            itemParams = dict(ItemsParameters.g_instance.getParameters(self, vehicle))
            if self.itemTypeName == ITEM_TYPE_NAMES[1]:
                itemParams['caliber'] = BigWorld.wg_getIntegralFormat(self.descriptor.gun['shots'][0]['shell']['caliber'])
            
            return description % itemParams
        except Exception:
            self.itemTypeName in (ITEM_TYPE_NAMES[9], ITEM_TYPE_NAMES[11])
            LOG_CURRENT_EXCEPTION()
            return ''


    
    def toolTip(self):
        '''
\t\tLong description for ToolTips an other usage
\t\tIncludes full list of parameters
\t\t'''
        return self.longName

    toolTip = property(toolTip)
    
    def getParams(self, vehicle):
        ItemsParameters = ItemsParameters
        import gui.Scaleform.utils
        return ItemsParameters.g_instance.get(self, vehicle)

    
    def suitableVehicles(self):
        '''
\t\tList of vehicles module fits
\t\t'''
        return self._FittingItem__suitableVehicles

    suitableVehicles = property(suitableVehicles)
    
    def tags(self):
        '''
\t\tSet of tags
\t\t'''
        if self.itemTypeName == ITEM_TYPE_NAMES[1]:
            return self.descriptor.type.tags
        return self.descriptor['tags']

    tags = property(tags)
    
    def oldIcon(self):
        '''
\t\tpath wheree icon for item stored
\t\t'''
        return _ITEM_TYPES_ORDER.index(self.type) + 2 + self.nation * 5

    oldIcon = property(oldIcon)
    
    def icon(self):
        '''
\t\tpath where icon for item stored
\t\t'''
        if self.itemTypeName in (ITEM_TYPE_NAMES[9], ITEM_TYPE_NAMES[11]):
            return self.descriptor.icon[0]
        if self.itemTypeName == ITEM_TYPE_NAMES[10]:
            return _ICONS_MASK[:-4] % {
                'type': self.itemTypeName,
                'subtype': '',
                'unicName': self.descriptor['icon'][0] }
        return _ICONS_MASK % {
            'type': self.itemTypeName,
            'subtype': '',
            'unicName': self.unicName.replace(':', '-') }

    icon = property(icon)
    
    def iconContour(self):
        '''
\t\tpath where icon contour for item stored
\t\t'''
        return _ICONS_MASK % {
            'type': self.itemTypeName,
            'subtype': 'contour/',
            'unicName': self.unicName.replace(':', '-') }

    iconContour = property(iconContour)
    
    def iconSmall(self):
        '''
\t\tpath where icon contour for item stored
\t\t'''
        return _ICONS_MASK % {
            'type': self.itemTypeName,
            'subtype': 'small/',
            'unicName': self.unicName.replace(':', '-') }

    iconSmall = property(iconSmall)
    
    def _getMessage(self, type, extra = None):
        message = '#system_messages:fitting/'
        if self.itemTypeName == ITEM_TYPE_NAMES[1]:
            if extra is not None and len(extra) == 2:
                message += 'vehicle_dismantling_'
            else:
                message += 'vehicle_'
        elif self.itemTypeName == ITEM_TYPE_NAMES[10]:
            message += 'shell_'
        elif self.itemTypeName in (ITEM_TYPE_NAMES[9], ITEM_TYPE_NAMES[11]):
            message += 'artefact_'
        else:
            message += 'module_'
        message += type
        args = [
            message]
        if self.itemTypeName not in (ITEM_TYPE_NAMES[1], ITEM_TYPE_NAMES[10]):
            args.append(self.userType)
        
        args.append(self.name)
        if extra is not None:
            if isinstance(extra, tuple):
                args.extend(extra)
            else:
                args.append(extra)
        
        return makeString(*tuple(args))

    
    def unpack(pickleString):
        data = pickle.loads(pickleString)
        
        try:
            return data[0](*data[1])
        except:
            return None


    unpack = staticmethod(unpack)
    
    def __cmp__(self, other):
        if other is None:
            return 1
        nationCompareResult = nationCompareByIndex(self.nation, other.nation)
        if nationCompareResult:
            return nationCompareResult
        if self.type in _ITEM_TYPES_ORDER and other.type in _ITEM_TYPES_ORDER:
            if _ITEM_TYPES_ORDER.index(self.type) < _ITEM_TYPES_ORDER.index(other.type):
                return -1
            if _ITEM_TYPES_ORDER.index(self.type) > _ITEM_TYPES_ORDER.index(other.type):
                return 1
        else:
            LOG_WARNING('%s or %s is not in _ITEM_TYPES_ORDER = %s' % (self.type, other.type, _ITEM_TYPES_ORDER))
        if self.level < other.level:
            return -1
        if self.level > other.level:
            return 1
        if self.priceOrder[1] < other.priceOrder[1]:
            return -1
        if self.priceOrder[1] > other.priceOrder[1]:
            return 1
        if self.priceOrder[0] < other.priceOrder[0]:
            return -1
        if self.priceOrder[0] > other.priceOrder[0]:
            return 1
        if self.name < other.name:
            return -1
        if self.name > other.name:
            return 1
        return 0

    
    def __eq__(self, other):
        if other is None:
            return False
        if self.itemTypeName == ITEM_TYPE_NAMES[1]:
            return self.descriptor.type.id == other.descriptor.type.id
        return self.compactDescr == other.compactDescr



class ShopItem(FittingItem):
    '''
\tRepresent an item from the shop
\t@param itemTypeName: item type @see: items.ITEM_TYPE_NAMES
\t@param id: in nation ID for vehicles, compactDescription for others
\t@param priceOrder: price in shop
\t@param suitFor: a list of vehicles module fits @see: self.suitableVehicles (not mandatory)
\t@param nation: nation index from nations.INDICES (not mandatory for all except vehicles)
\t'''
    
    def __init__(self, itemTypeName, compactDescr, nation = None, priceOrder = (0, 0), hidden = False):
        self._ShopItem__descriptor = None
        FittingItem.__init__(self, compactDescr, itemTypeName, priceOrder)
        self._ShopItem__nation = nation
        self.hidden = hidden
        if nation is None and self.itemTypeName == ITEM_TYPE_NAMES[1]:
            if not 'vehicle without nation':
                raise AssertionError
        

    
    def priceSync(self):
        return (self.priceOrder[0], self.priceOrder[1])

    priceSync = property(priceSync)
    
    def getPrice(self, callback):
        price = (self.priceOrder[0], self.priceOrder[1])
        callback(price)

    getPrice = async(getPrice)
    
    def nation(self):
        '''
\t\tNation index from nations.INDICES
\t\t'''
        if self._ShopItem__nation is None:
            self._ShopItem__nation = self.descriptor['id'][0]
        
        return self._ShopItem__nation

    nation = property(nation)
    
    def descriptor(self):
        '''
\t\tDescriptor for Item
\t\tVehicleDescr for vehicles
\t\t'''
        if self._ShopItem__descriptor is None:
            if self.itemTypeName == ITEM_TYPE_NAMES[1]:
                self._ShopItem__descriptor = VehicleDescr(typeID = (self.nation, self.compactDescr))
            else:
                self._ShopItem__descriptor = getDictDescr(self.compactDescr)
        
        return self._ShopItem__descriptor

    descriptor = property(descriptor)
    
    def target(self):
        '''
\t\tReturn 3 for all items
\t\tInventoryItem return 1 if module is current, 2 for all other
\t\t'''
        return 3

    target = property(target)
    
    def buy(self, count = 1, isShell = False, isCrew = True, crew_type = 0, isSlot = False, callback = None):
        '''
\t\tBuy this module in shop, and return it as InventoryItem in callback
\t\tFor vehicle buy default shells and crew.
\t\t@param callback:
\t\t@param count: number of modules to buy
\t\t@todo: refactor this (add auto apply), make it independent from other code? do not use callback
\t\t'''
        
        def getBuyResponse(code, itemInvID = (None, None, None, None)):
            if code >= 0:
                if callback is not None:
                    component = InventoryItem(self.itemTypeName, self.compactDescr, id = itemInvID, count = count)
                    message = ''
                    if self.itemTypeName == ITEM_TYPE_NAMES[1]:
                        message = self._getMessage('buy_success', formatPrice(buyPrice))
                    else:
                        message = self._getMessage('buy_success', (count, formatPrice(buyPrice)))
                    callback((True, message, getPurchaseSysMessageType(buyPrice), component))
                
            else:
                LOG_ERROR('Server response en error for buy item(%s - %s) operation code: %s' % (self.itemTypeName, self.name, code))
                RES_CENTER_DISCONNECTED = RES_CENTER_DISCONNECTED
                import AccountCommands
                message = 'buy_server_error'
                if code == RES_CENTER_DISCONNECTED:
                    message = 'buy_server_error_centerDown'
                
                if callback is not None:
                    callback((False, self._getMessage(message)))
                

        StatsRequester = StatsRequester
        import requesters
        yield StatsRequester().getCredits()
        credits = None
        yield StatsRequester().getGold()
        gold = None
        yield self.getPrice()
        buyPrice = None
        buyPrice = [
            buyPrice[0] * count,
            buyPrice[1] * count]
        if self.itemTypeName == 'vehicle':
            yield StatsRequester().getTankmanCost()
            tCost = None
            tankmenCount = len(self.descriptor.type.crewRoles)
            if isCrew:
                if crew_type == 1:
                    buyPrice[0] += tCost[1]['credits'] * tankmenCount
                elif crew_type == 2:
                    buyPrice[1] += tCost[2]['gold'] * tankmenCount
                
            
            if isShell:
                shells = vehicles.getDefaultAmmoForGun(self.descriptor.gun)
                for i in range(0, len(shells), 2):
                    (_, nationIdx, shellInnationIdx) = vehicles.parseIntCompactDescr(shells[i])
                    yield StatsRequester().getShellPrice(nationIdx, shells[i])
                    shellPrice = None
                    buyPrice[0] += shellPrice[0] * shells[i + 1]
                    buyPrice[1] += shellPrice[1] * shells[i + 1]
                
            
            if isSlot:
                yield StatsRequester().buySlot()
                success = None
                if not success:
                    SystemMessages.g_instance.pushI18nMessage('#system_messages:buy_slot/server_error', SystemMessages.SM_TYPE.Error)
                    return None
                yield StatsRequester().getSlotsPrices()
                price = success
                buyPrice[1] += price[1][0]
            
        
        if (credits, gold) >= tuple(buyPrice):
            if self.itemTypeName == 'vehicle':
                BigWorld.player().shop.buyVehicle(self.descriptor.type.id[0], self.descriptor.type.id[1], isShell, isCrew, crew_type, callback = getBuyResponse)
            else:
                BigWorld.player().shop.buy(ITEM_TYPE_INDICES[self.itemTypeName], self.nation, self.compactDescr, int(count), getBuyResponse)
        elif callback is not None:
            price = (buyPrice[0] - credits, buyPrice[1] - gold)
            callback((False, self._getMessage('buy_money_error', formatPrice(price))))
        

    buy = async(process(buy))
    
    def pack(self):
        return pickle.dumps([
            ShopItem,
            (self.itemTypeName, self.compactDescr, self.nation, self.priceOrder)])



class InventoryItem(FittingItem):
    '''
\tRepresent an item from the inventory
\t@param itemTypeName: item type @see: items.ITEM_TYPE_NAMES
\t@param id: in nation ID for vehicles, compactDescription for others
\t@param priceOrder: price in shop if needed for ordering
\t@param suitFor: a list of vehicles module fits @see: self.suitableVehicles (not mandatory)
\t@param nation: nation index from nations.INDICES (not mandatory for all except vehicles)
\t'''
    
    def __init__(self, itemTypeName, compactDescr = None, id = None, priceOrder = (0, 0), count = 1, isCurrent = False):
        self._InventoryItem__descriptor = None
        FittingItem.__init__(self, compactDescr, itemTypeName, priceOrder)
        self.inventoryId = id
        self.count = count
        self.isCurrent = isCurrent

    
    def getPrice(self, callback):
        
        def _InventoryItem__valueResponse(responseCode, value, revision = (0,)):
            if responseCode < 0:
                LOG_ERROR('Server return error for shop getSellPrice request: responseCode=%s' % responseCode)
            
            if callback:
                callback((value, 0))
            

        if not hasattr(BigWorld.player(), 'shop'):
            raise AssertionError, 'Request from shop is not possible'
        BigWorld.player().shop.getComponentSellPrice(self.compactDescr, _InventoryItem__valueResponse)

    getPrice = async(getPrice)
    
    def isSellPosible(self):
        return True

    isSellPosible = property(isSellPosible)
    
    def nation(self):
        '''
\t\tNation index from nations.INDICES
\t\t'''
        if self.itemTypeName == ITEM_TYPE_NAMES[1]:
            return self.descriptor.type.id[0]
        return self.descriptor['id'][0]

    nation = property(nation)
    
    def descriptor(self):
        '''
\t\tDescriptor for Item
\t\tVehicleDescr for vehicles
\t\tTankmanDescr for tankman
\t\t'''
        if self._InventoryItem__descriptor is None:
            if self.itemTypeName == 'vehicle':
                self._InventoryItem__descriptor = VehicleDescr(compactDescr = self.compactDescr)
            elif self.itemTypeName == 'tankman':
                self._InventoryItem__descriptor = TankmanDescr(compactDescr = self.compactDescr)
            else:
                self._InventoryItem__descriptor = getDictDescr(self.compactDescr)
        
        return self._InventoryItem__descriptor

    descriptor = property(descriptor)
    
    def target(self):
        '''
\t\tReturn 1 if module is current, 2 for all other
\t\tShopItem return 3 for all items
\t\t'''
        if self.isCurrent:
            return 1
        return 2

    target = property(target)
    
    def apply(self, callback, slotIdx = None, isUseGold = False, invVehicle = None):
        '''
\t\tInstall this module to current vehicle
\t\t@param callback:
\t\t@todo: refactor this, make it independent from other code? do not use callback
\t\t'''
        if self.itemTypeName == ITEM_TYPE_NAMES[1]:
            g_currentVehicle.vehicle = self
        elif invVehicle is None:
            invVehicle = g_currentVehicle.vehicle
        
        if invVehicle is not None and invVehicle.isAlive():
            if self.itemTypeName == ITEM_TYPE_NAMES[11]:
                currents = list(invVehicle.equipments)
                if len(currents) > slotIdx and currents[slotIdx] != self.compactDescr:
                    currents[slotIdx] = self.compactDescr
                    calbackType = self._InventoryItem__responseApply
                else:
                    currents[slotIdx] = 0
                    calbackType = self._InventoryItem__responseRemove
                None(None, (None, None, BigWorld.player().inventory.equipEquipments, invVehicle.inventoryId, currents), (lambda code: calbackType(code, callback, invVehicle, slotIdx = slotIdx, equipments = currents)))
                return None
            if self.itemTypeName == ITEM_TYPE_NAMES[9]:
                currents = list(invVehicle.descriptor.optionalDevices)
                for (i, current) in enumerate(currents):
                    if current:
                        currents[i] = current.compactDescr
                        continue
                    self.itemTypeName == ITEM_TYPE_NAMES[11]
                
                if self.compactDescr in currents:
                    mayRemove = invVehicle.descriptor.mayRemoveOptionalDevice(slotIdx)
                    if mayRemove[0]:
                        None(None, None, None, (BigWorld.player().inventory.equipOptionalDevice, invVehicle.inventoryId, 0, slotIdx, isUseGold), (lambda code: self._InventoryItem__responseRemove(code, callback, invVehicle, slotIdx = slotIdx, isUseGold = isUseGold)))
                        return None
                    error = mayRemove[1].replace(' ', '_')
                    type = 'remove_error_' + error
                    value = (False, self._getMessage(type))
                else:
                    mayInstall = invVehicle.descriptor.mayInstallOptionalDevice(self.compactDescr, slotIdx)
                    if mayInstall[0]:
                        None(None, None, BigWorld.player().inventory.equipOptionalDevice, (invVehicle.inventoryId, self.compactDescr, slotIdx, isUseGold), (lambda code: self._InventoryItem__responseApply(code, callback, invVehicle, slotIdx = slotIdx)))
                        return None
                    error = mayInstall[1].replace(' ', '_')
                    type = 'apply_error_' + error
                    value = (False, self._getMessage(type))
            elif self.descriptor['id'] == invVehicle.descriptor.getComponentsByType(self.itemTypeName)[0]['id']:
                value = (False, self._getMessage('apply_error_is_current'))
            elif self.itemTypeName != ITEM_TYPE_NAMES[3]:
                mayInstall = invVehicle.descriptor.mayInstallComponent(self.compactDescr)
                if mayInstall[0]:
                    None(self.itemTypeName == ITEM_TYPE_NAMES[11], (BigWorld.player().inventory.equip, invVehicle.inventoryId, self.compactDescr), (lambda code, ext: self._InventoryItem__responseApply(code, callback, invVehicle, ext)))
                    return None
                error = mayInstall[1].replace(' ', '_')
                type = 'apply_error_' + error
                if error == 'too_heavy' and self.itemTypeName == ITEM_TYPE_NAMES[2]:
                    type += '_chassis'
                
            else:
                mayInstall = invVehicle.descriptor.mayInstallTurret(self.compactDescr, 0)
                if mayInstall[0]:
                    self.itemTypeName == ITEM_TYPE_NAMES[11](mayInstall[0], BigWorld.player().inventory.equipTurret, (invVehicle.inventoryId, self.compactDescr, 0), (lambda code, ext: self._InventoryItem__responseApply(code, callback, invVehicle, ext, 0)))
                    return None
                self._InventoryItem__applyTurret(mayInstall[1] == 'too heavy', callback, invVehicle)
                return None
            value = (self.itemTypeName == ITEM_TYPE_NAMES[9], self._getMessage(type))
        else:
            message = 'apply_vehicle_'
            if self.itemTypeName == ITEM_TYPE_NAMES[9]:
                currents = list(invVehicle.descriptor.optionalDevices)
                for (i, current) in enumerate(currents):
                    if current:
                        currents[i] = current.compactDescr
                        continue
                
                if self.compactDescr in currents:
                    if not (self.isRemovable) or isUseGold or self.isRemovable:
                        message = 'remove_vehicle_'
                    else:
                        message = 'destroy_vehicle_'
                
            
            if g_currentVehicle.isLocked():
                value = (False, self._getMessage(message + 'locked'))
            else:
                value = (False, self._getMessage(message + 'broken'))
        if callback is not None:
            value = (value[0], value[1], { })
            callback(value)
        

    apply = async(apply)
    
    def __applyTurret(self, isToHeavy, callback, invVehicle):
        Requester = Requester
        import requesters
        yield Requester(ITEM_TYPE_NAMES[4]).getFromInventory()
        iGuns = None
        iGuns.sort(reverse = True)
        for iGun in iGuns:
            for None in self.descriptor['guns']:
                gun = None
                if iGun.compactDescr == gun['compactDescr']:
                    mayInstall = invVehicle.descriptor.mayInstallTurret(self.compactDescr, gun['compactDescr'])
                    if mayInstall[0]:
                        None(None, None, (BigWorld.player().inventory.equipTurret, invVehicle.inventoryId, self.compactDescr, gun['compactDescr']), (lambda code, ext: self._InventoryItem__responseApply(code, callback, invVehicle, ext, gun['compactDescr'])))
                        return None
                    if mayInstall[1] == 'too heavy':
                        isToHeavy = True
                    
            
        
        if isToHeavy:
            value = (False, self._getMessage('apply_error_too_heavy'), [])
        else:
            value = (False, self._getMessage('apply_error_no_gun'), [])
        if callback is not None:
            callback(value)
        

    _InventoryItem__applyTurret = process(__applyTurret)
    
    def _InventoryItem__responseApply(self, code, callback, invVehicle, removed = None, gun = None, slotIdx = None, equipments = None):
        if removed is None:
            removed = { }
        
        if code >= 0:
            value = (True, self._getMessage('apply_success'), removed)
            if equipments:
                pass
            elif slotIdx is not None:
                invVehicle.descriptor.installOptionalDevice(self.compactDescr, slotIdx)
            elif gun is not None:
                invVehicle.descriptor.installTurret(self.compactDescr, gun)
                if gun:
                    value = (True, self._getMessage('apply_success_gun_change', getDictDescr(gun)['userString']), removed)
                
            else:
                invVehicle.descriptor.installComponent(self.compactDescr)
        else:
            LOG_ERROR('Server response an error for install item(%s - %s) operation code: %s' % (self.itemTypeName, self.descriptor['name'], code))
            value = (False, self._getMessage('server_apply_error'), removed)
        if callback is not None:
            callback(value)
        

    
    def __responseRemove(self, code, callback, invVehicle, slotIdx, equipments = [], isUseGold = False):
        StatsRequester = StatsRequester
        import requesters
        yield StatsRequester().getPaidRemovalCost()
        cost = None
        if code >= 0:
            if equipments:
                pass
            1
            invVehicle.descriptor.removeOptionalDevice(slotIdx)
            if self.isRemovable:
                value = (True, self._getMessage('remove_success'), { })
            elif isUseGold:
                value = (True, self._getMessage('remove_gold_success', cost), { })
            else:
                value = (True, self._getMessage('destroy_success'), { })
        else:
            LOG_ERROR('Server response en error for remove item(%s - %s) operation code: %s' % (self.itemTypeName, self.descriptor['name'], code))
            value = (False, self._getMessage('server_remove_error'))
        if callback is not None:
            callback(value)
        

    _InventoryItem__responseRemove = process(__responseRemove)
    
    def sell(self, callback = None, count = 1):
        '''
\t\tBuy this module in shop, and return it as InventoryItem in callback
\t\t@param callback:
\t\t@param count: number of modules to buy
\t\t@todo: refactor this (add auto apply), make it independent from other code? do not use callback
\t\t'''
        
        def getSellResponse(code):
            if code >= 0:
                if callback is not None:
                    message = self._getMessage('sell_success', (count, formatPrice(sellPrice)))
                    callback((True, message))
                
            else:
                LOG_ERROR('Server response en error for sell item(%s - %s) operation code: %s' % (self.itemTypeName, self.name, code))
                if callback is not None:
                    callback((False, self._getMessage('sell_server_error')))
                

        yield self.getPrice()
        sellPrice = (None, None, None, None)
        sellPrice = (sellPrice[0] * count, sellPrice[1] * count)
        if self.inventoryId is not None:
            pass
        1
        ITEM_TYPE_INDICES[self.itemTypeName](self.inventoryId, self.compactDescr, count, getSellResponse)

    sell = async(process(sell))
    
    def pack(self):
        return pickle.dumps([
            InventoryItem,
            (self.itemTypeName, self.compactDescr, self.inventoryId)])



class InventoryVehicle(InventoryItem):
    NOT_FULL_AMMO_MULTIPLIER = 0.2
    
    class STATE_LEVEL:
        CRITICAL = 'critical'
        INFO = 'info'
        WARNING = 'warning'

    
    def __init__(self, compactDescr, id, crew = [], shells = { }, ammoLayout = { }, repairCost = 0, health = 0, lock = 0, equipments = [], equipmentsLayout = [], settings = 0):
        InventoryItem.__init__(self, ITEM_TYPE_NAMES[1], compactDescr = compactDescr, id = id, count = 1)
        self._InventoryVehicle__shells = []
        self._InventoryVehicle__ammoLayout = ammoLayout
        self.setShellsList(shells)
        self.repairCost = repairCost
        self._InventoryVehicle__health = health
        self._InventoryVehicle__crew = crew
        self.lock = lock
        self._InventoryVehicle__equipments = equipments
        self.equipmentsLayout = equipmentsLayout
        self._InventoryVehicle__settings = settings

    
    def sell(self, sellEqs = False, performDismantling = False, callback = None):
        VehicleItemsRequester = VehicleItemsRequester
        Requester = Requester
        import requesters
        if not self.isSellPosible:
            callback((False, self._getMessage('sell_server_error')))
            return None
        yield self.getSellPrice(sellEqs, performDismantling)
        (getMoney, putMoney) = self.isSellPosible
        
        def getSellResponse(code):
            if code >= 0:
                if callback is not None:
                    formatArgs = [
                        formatPrice(getMoney)]
                    if putMoney[0] != 0 or putMoney[1] != 0:
                        formatArgs.append(formatPrice(putMoney))
                    
                    message = self._getMessage('sell_success', tuple(formatArgs))
                    callback((True, message))
                
            else:
                LOG_ERROR('Server response en error for sell item(%s - %s) operation code: %s' % (self.itemTypeName, self.name, code))
                if callback is not None:
                    callback((False, self._getMessage('sell_server_error')))
                

        componentCompDescrs = list()
        devs = VehicleItemsRequester((self,)).getItems(('optionalDevice',))
        if sellEqs:
            for shell in self.shells:
                componentCompDescrs.append(shell.compactDescr)
            
            eqs = VehicleItemsRequester((self,)).getItems(('equipment',))
            for eq in eqs:
                componentCompDescrs.append(eq.compactDescr)
            
            for dev in devs:
                if dev.descriptor['removable']:
                    componentCompDescrs.append(dev.compactDescr)
                    continue
                (None, None, None, None)
            
        
        if not performDismantling:
            for dev in devs:
                if not dev.descriptor['removable']:
                    componentCompDescrs.append(dev.compactDescr)
                    continue
            
        
        BigWorld.player().inventory.sellVehicle(self.inventoryId, sellEqs, sellEqs, False, sellEqs, performDismantling, sellEqs, componentCompDescrs, getSellResponse)

    sell = async(process(sell))
    
    def canSell(self):
        st = self.getState()
        if not st == 'undamaged' and st == 'crewNotFull':
            pass
        return st == 'ammoNotFull'

    canSell = property(canSell)
    
    def vehicleType(self):
        for tag in vehicles.VEHICLE_CLASS_TAGS.intersection(self.descriptor.type.tags):
            return tag
        

    vehicleType = property(vehicleType)
    
    def getSellPrice(self, sellEqs = True, performDismantling = False, callback = None):
        VehicleItemsRequester = VehicleItemsRequester
        StatsRequester = StatsRequester
        Requester = Requester
        import requesters
        yield self.getPrice()
        getMoney = None
        getMoney = list(getMoney)
        putMoney = [
            0,
            0]
        artefacts = VehicleItemsRequester((self,)).getItems(('equipment', 'optionalDevice'))
        devicesRemovablePrice = 0
        devicesNotRemovablePrice = 0
        devicesNotRemovableCount = 0
        equipmentsPrice = 0
        yield StatsRequester().getAmmoSellPrice(self.getShellsList())
        shellsPrice = None
        for art in artefacts:
            yield art.getPrice()
            artPrice = None
            if not hasattr(art.descriptor, 'removable') or art.descriptor['removable']:
                if not hasattr(art.descriptor, 'removable'):
                    equipmentsPrice += artPrice[0]
                else:
                    devicesRemovablePrice += artPrice[0]
            hasattr(art.descriptor, 'removable')
            devicesNotRemovablePrice += artPrice[0]
            devicesNotRemovableCount += 1
        
        getMoney[0] += shellsPrice + equipmentsPrice
        if not sellEqs:
            getMoney[0] -= devicesRemovablePrice
            getMoney[0] -= shellsPrice
            getMoney[0] -= equipmentsPrice
        
        if performDismantling:
            getMoney[0] -= devicesNotRemovablePrice
            yield StatsRequester().getPaidRemovalCost()
            removeDeviceCost = None
            putMoney[1] += removeDeviceCost * devicesNotRemovableCount
        
        callback((getMoney, putMoney))

    getSellPrice = async(process(getSellPrice))
    
    def sellParams(self, callback):
        VehicleItemsRequester = VehicleItemsRequester
        StatsRequester = StatsRequester
        Requester = Requester
        import requesters
        artefacts = VehicleItemsRequester((self,)).getItems(('equipment', 'optionalDevice'))
        yield StatsRequester().getPaidRemovalCost()
        removeDeviceCost = None
        yield Requester('vehicle').getFromShop()
        shopVehicles = None
        yield self.getPrice()
        vehiclePrice = None
        yield StatsRequester().getAmmoSellPrice(self.getShellsList())
        shellsPrice = None
        shellsCount = 0
        for shell in self.shells:
            shellsCount += shell.count
        
        vehicleFullPrice = vehiclePrice[0] + shellsPrice
        crewCount = 0
        for tankman in self.crew:
            if tankman is not None:
                crewCount += 1
                continue
        
        artefactsCount = 0
        artefactsRemovableCount = 0
        artefactsRemovablePrice = shellsPrice
        artefactsNotRemovablePrice = 0
        artefactsDismantlingPrice = 0
        for art in artefacts:
            artefactsCount += 1
            yield art.getPrice()
            artPrice = None
            if not hasattr(art.descriptor, 'removable') or art.descriptor['removable']:
                if not hasattr(art.descriptor, 'removable'):
                    vehicleFullPrice += artPrice[0]
                
                artefactsRemovablePrice += artPrice[0]
                artefactsRemovableCount += 1
                continue
            artefactsNotRemovablePrice += artPrice[0]
            artefactsDismantlingPrice += removeDeviceCost
        
        if not crewCount != 0 and artefactsRemovableCount != 0:
            pass
        callback([
            self.pack(),
            makeString('#dialogs:vehicleSellDialog/title') % self.name,
            makeString('#dialogs:vehicleSellDialog/content/tankmenField') % crewCount,
            makeString('#dialogs:vehicleSellDialog/content/equipmentsField') % artefactsCount,
            makeString('#dialogs:vehicleSellDialog/content/shellsField') % shellsCount,
            vehicleFullPrice,
            artefactsRemovablePrice,
            artefactsNotRemovablePrice,
            artefactsDismantlingPrice,
            shellsCount != 0])

    sellParams = async(process(sellParams))
    
    def isUnique(self, callback):
        Requester = Requester
        import requesters
        yield Requester('vehicle').getFromShop()
        shopVehicles = None
        isUnique = True
        for sv in shopVehicles:
            if sv.descriptor.type.id == self.descriptor.type.id:
                isUnique = sv.hidden
                break
                continue
        
        callback(isUnique)

    isUnique = async(process(isUnique))
    
    def getPrice(self, callback):
        
        def _InventoryVehicle__valueResponse(responseCode, value, revision = (0,)):
            if responseCode < 0:
                LOG_ERROR('Server return error for shop getSellPrice request: responseCode=%s' % responseCode)
            
            if callback:
                callback((value, 0))
            

        if not hasattr(BigWorld.player(), 'shop'):
            raise AssertionError, 'Request from shop is not possible'
        BigWorld.player().shop.getVehicleSellPrice(self.compactDescr, _InventoryVehicle__valueResponse)

    getPrice = async(getPrice)
    
    def _InventoryVehicle__getHealth(self):
        if not self.repairCost:
            return self.descriptor.maxHealth
        if self._InventoryVehicle__health > 0:
            return self._InventoryVehicle__health
        return 0

    
    def _InventoryVehicle__setHealth(self, value):
        self._InventoryVehicle__health = min(value, self.descriptor.maxHealth)

    health = property(_InventoryVehicle__getHealth, _InventoryVehicle__setHealth)
    
    def crew(self):
        return self._InventoryVehicle__crew

    crew = property(crew)
    
    def _InventoryVehicle__getFavorite(self):
        vcls = list(AccountSettings.getFavorites('vehicles'))
        return self.inventoryId in vcls

    
    def _InventoryVehicle__setFavorite(self, isFavorite):
        vcls = list(AccountSettings.getFavorites('vehicles'))
        if isFavorite and self.inventoryId not in vcls:
            vcls.append(self.inventoryId)
        elif not isFavorite and self.inventoryId in vcls:
            vcls.remove(self.inventoryId)
        
        AccountSettings.setFavorites('vehicles', vcls)

    favorite = property(_InventoryVehicle__getFavorite, _InventoryVehicle__setFavorite)
    
    def isCrewFull(self):
        if None not in self._InventoryVehicle__crew:
            pass
        return self._InventoryVehicle__crew != []

    
    def isAmmoFull(self):
        loadedCount = 0
        for shell in self.shells:
            loadedCount += shell.count
        
        return loadedCount >= self.getShellsMaxCount() * self.NOT_FULL_AMMO_MULTIPLIER

    
    def modelState(self):
        if self._InventoryVehicle__health < 0:
            return 'exploded'
        if self.repairCost > 0 and self.health == 0:
            return 'destroyed'
        return 'undamaged'

    modelState = property(modelState)
    
    def isSellPosible(self):
        if self.repairCost == 0 and not (self.lock):
            return True
        return False

    isSellPosible = property(isSellPosible)
    
    def _InventoryVehicle__getEquipmets(self):
        return self._InventoryVehicle__equipments

    equipments = property(_InventoryVehicle__getEquipmets)
    
    def _InventoryVehicle__getShells(self):
        return self._InventoryVehicle__shells

    
    def _InventoryVehicle__setShells(self, shells):
        self._InventoryVehicle__shells = shells

    shells = property(_InventoryVehicle__getShells, _InventoryVehicle__setShells)
    
    def getShellsList(self):
        shells = []
        for shell in self._InventoryVehicle__shells:
            shells.append(shell.compactDescr)
            shells.append(shell.count)
        
        return shells

    
    def getShellsDefaultList(self):
        shells = []
        for shell in self._InventoryVehicle__shells:
            shells.append(shell.compactDescr)
            shells.append(shell.default)
        
        return shells

    
    def getShellsMaxCount(self):
        return VehicleItem(self.descriptor.gun).descriptor['maxAmmo']

    
    def setShellsList(self, shellsList = None):
        if shellsList is None:
            return None
        defaults = listToDict(self._InventoryVehicle__getDefaultsForCurrentConfiguration())
        shellsDict = listToDict(shellsList)
        self._InventoryVehicle__shells = []
        shellsList = list(shellsList)
        for shot in self.descriptor.gun['shots']:
            if shot['shell']['compactDescr'] not in shellsDict.keys():
                shellsList.append(shot['shell']['compactDescr'])
                shellsList.append(0)
                continue
            shellsList is None
        
        
        def getShellParams(cDescr):
            for shot in self.descriptor.gun['shots']:
                if cDescr == shot['shell']['compactDescr']:
                    return shot
            

        while len(shellsList) != 0:
            cDescr = shellsList[0]
            count = shellsList[1]
            shellsList = shellsList[2:]
            shot = getShellParams(cDescr)
            default = defaults.get(cDescr, 0)
            if shot is not None:
                self._InventoryVehicle__shells.append(VehicleShellSlot(shot['shell'], cDescr, count, default, shot['piercingPower'], shot['shell']['damage']))
                continue
            (None,)

    
    def _InventoryVehicle__setEquipmentsList(self, equipemtsList = []):
        self._InventoryVehicle__equipemts = []
        for equipemt in equipemtsList:
            self._InventoryVehicle__equipemts.append(VehicleItem(compactDescr = equipemt))
        

    
    def _InventoryVehicle__getDefaultsForCurrentConfiguration(self):
        defaults = self._InventoryVehicle__ammoLayout.get((self.descriptor.turret['compactDescr'], self.descriptor.gun['compactDescr']), [])
        if not defaults:
            defaults = getDefaultAmmoForGun(self.descriptor.gun)
        
        return defaults

    
    def _InventoryVehicle__isCurrent(self):
        return self.inventoryId == g_currentVehicle.vehicle.inventoryId

    
    def _InventoryVehicle__setCurrent(self, value):
        pass

    isCurrent = property(_InventoryVehicle__isCurrent, _InventoryVehicle__setCurrent)
    
    def getState(self):
        if self.lock == LOCK_REASON.ON_ARENA:
            return 'battle'
        if self.lock:
            return 'locked'
        ms = self.modelState
        if ms == 'undamaged':
            if self.repairCost > 0:
                return 'damaged'
            if not self.isCrewFull():
                return 'crewNotFull'
            if not self.isAmmoFull():
                return 'ammoNotFull'
        
        return ms

    
    def getStateLevel(self):
        state = self.getState()
        if state in ('crewNotFull', 'damaged', 'exploded', 'destroyed'):
            return InventoryVehicle.STATE_LEVEL.CRITICAL
        if state in ('undamaged',):
            return InventoryVehicle.STATE_LEVEL.INFO
        return InventoryVehicle.STATE_LEVEL.WARNING

    
    def loadShells(self, shells, callback):
        
        def loadShellsResponse(responseCode):
            response = (False, '#system_messages:charge/server_error')
            if responseCode < 0:
                LOG_ERROR('Server return error for inventory equipShells request: responseCode=%s.' % responseCode)
            else:
                response = (True, '#system_messages:charge/success')
            if callback:
                callback(response)
            

        if not hasattr(BigWorld.player(), 'inventory'):
            raise AssertionError, 'Load shells is not possible'
        if shells is None:
            shells = self._InventoryVehicle__getDefaultsForCurrentConfiguration()
        
        defaults = listToDict(getDefaultAmmoForGun(self.descriptor.gun))
        defaultsCount = 0
        for (cDescr, count) in defaults.iteritems():
            defaultsCount += count
        
        shellsCount = 0
        for (cDescr, count) in listToDict(shells).iteritems():
            shellsCount += count
        
        if shellsCount > defaultsCount:
            callback((False, '#system_messages:charge/server_error'))
        
        BigWorld.player().inventory.equipShells(self.inventoryId, shells, loadShellsResponse)

    loadShells = async(loadShells)
    
    def repair(self, callback):
        
        def checkCredit(code, value):
            
            def repairResponse(code):
                if code >= 0:
                    if callback is not None:
                        message = makeString('#system_messages:repair/success', self.name, formatPrice((repairCost, 0)))
                        callback((True, message))
                    
                else:
                    LOG_ERROR('Server response en error for repair vehicle(%s - %s) operation code: %s' % (self.name, self.inventoryId, code))
                    if callback is not None:
                        callback((False, makeString('#system_messages:repair/server_error', self.name)))
                    

            if value >= self.repairCost:
                repairCost = self.repairCost
                BigWorld.player().inventory.repair(self.inventoryId, repairResponse)
            elif callback is not None:
                callback((False, makeString('#system_messages:repair/credit_error', int(self.repairCost - value), self.name)))
            

        BigWorld.player().stats.get('credits', checkCredit)

    repair = async(repair)
    
    def isElite(self, callback):
        StatsRequester = StatsRequester
        import gui.Scaleform.utils.requesters
        yield StatsRequester().getEliteVehicles()
        eliteVehicles = None
        callback(self.isGroupElite(eliteVehicles))

    isElite = async(process(isElite))
    
    def isGroupElite(self, eliteVehicles):
        if not len(self.descriptor.type.unlocksDescrs) == 0:
            pass
        return self.descriptor.type.compactDescr in eliteVehicles

    
    def isXPToTman(self):
        VEHICLE_SETTINGS_FLAG = VEHICLE_SETTINGS_FLAG
        import AccountCommands
        return bool(self._InventoryVehicle__settings & VEHICLE_SETTINGS_FLAG.XP_TO_TMAN)

    isXPToTman = property(isXPToTman)
    
    def setXPToTmen(self, isOn, callback):
        
        def response(responseCode):
            if responseCode < 0:
                LOG_ERROR('Server return error for setXPToTmen request: responseCode=%s.' % responseCode)
            
            if callback:
                callback(responseCode >= 0)
            

        VEHICLE_SETTINGS_FLAG = VEHICLE_SETTINGS_FLAG
        import AccountCommands
        BigWorld.player().inventory.changeVehicleSetting(self.inventoryId, VEHICLE_SETTINGS_FLAG.XP_TO_TMAN, bool(isOn), response)

    setXPToTmen = async(setXPToTmen)
    
    def isAutoRepair(self):
        VEHICLE_SETTINGS_FLAG = VEHICLE_SETTINGS_FLAG
        import AccountCommands
        return bool(self._InventoryVehicle__settings & VEHICLE_SETTINGS_FLAG.AUTO_REPAIR)

    isAutoRepair = property(isAutoRepair)
    
    def setAutoRepair(self, isOn, callback):
        
        def response(responseCode):
            if responseCode < 0:
                LOG_ERROR('Server return error for setAutoRepair request: responseCode=%s.' % responseCode)
            
            if callback:
                callback(responseCode >= 0)
            

        VEHICLE_SETTINGS_FLAG = VEHICLE_SETTINGS_FLAG
        import AccountCommands
        BigWorld.player().inventory.changeVehicleSetting(self.inventoryId, VEHICLE_SETTINGS_FLAG.AUTO_REPAIR, bool(isOn), response)

    setAutoRepair = async(setAutoRepair)
    
    def isAutoLoad(self):
        VEHICLE_SETTINGS_FLAG = VEHICLE_SETTINGS_FLAG
        import AccountCommands
        return bool(self._InventoryVehicle__settings & VEHICLE_SETTINGS_FLAG.AUTO_LOAD)

    isAutoLoad = property(isAutoLoad)
    
    def setAutoLoad(self, isOn, callback):
        
        def response(responseCode):
            if responseCode < 0:
                LOG_ERROR('Server return error for setAutoLoad request: responseCode=%s.' % responseCode)
            
            if callback:
                callback(responseCode >= 0)
            

        VEHICLE_SETTINGS_FLAG = VEHICLE_SETTINGS_FLAG
        import AccountCommands
        BigWorld.player().inventory.changeVehicleSetting(self.inventoryId, VEHICLE_SETTINGS_FLAG.AUTO_LOAD, bool(isOn), response)

    setAutoLoad = async(setAutoLoad)
    
    def isAutoEquip(self):
        VEHICLE_SETTINGS_FLAG = VEHICLE_SETTINGS_FLAG
        import AccountCommands
        return bool(self._InventoryVehicle__settings & VEHICLE_SETTINGS_FLAG.AUTO_EQUIP)

    isAutoEquip = property(isAutoEquip)
    
    def setAutoEquip(self, isOn, callback):
        
        def response(responseCode):
            if responseCode < 0:
                LOG_ERROR('Server return error for AUTO_EQUIP request: responseCode=%s.' % responseCode)
            
            if callback:
                callback(responseCode >= 0)
            

        VEHICLE_SETTINGS_FLAG = VEHICLE_SETTINGS_FLAG
        import AccountCommands
        BigWorld.player().inventory.changeVehicleSetting(self.inventoryId, VEHICLE_SETTINGS_FLAG.AUTO_EQUIP, bool(isOn), response)

    setAutoEquip = async(setAutoEquip)
    
    def isLocked(self):
        return self.lock != LOCK_REASON.NONE

    
    def isBroken(self):
        return self.repairCost > 0

    
    def isAlive(self):
        if not self.isBroken():
            pass
        return not self.isLocked()

    
    def __repr__(self):
        return 'InventoryVehicle<id:%d, repairCost:%f, lock:%d>' % (self.inventoryId, self.repairCost, self.lock)

    
    def pack(self):
        return pickle.dumps([
            InventoryVehicle,
            (self.compactDescr, self.inventoryId, self.crew)])

    
    def __eq__(self, other):
        if other is not None and isinst
