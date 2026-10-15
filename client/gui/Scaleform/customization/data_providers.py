# Source Generated with Decompyle++
# File: data_providers.pyc (Python 2.6)

import BigWorld
from abc import abstractmethod, ABCMeta
from debug_utils import LOG_DEBUG
import gui
from gui import SystemMessages
from items import vehicles
from helpers import i18n
from CurrentVehicle import g_currentVehicle
from gui.ClientHangarSpace import _CAMOUFLAGE_MIN_INTENSITY
from gui.Scaleform.data_providers import BaseDirectAccessDP
from gui.Scaleform.windows import UIInterface
from gui.Scaleform.utils.functions import makeTooltip
import Math
import time
import Event
from items.vehicles import CAMOUFLAGE_KINDS

class CamouflageGroupsDataProvider(BaseDirectAccessDP):
    
    def __init__(self, nationID):
        super(CamouflageGroupsDataProvider, self).__init__()
        self._CamouflageGroupsDataProvider__list = []
        self._nationID = nationID

    
    def setupFlashDp(self, proxy):
        return proxy.movie.contentHolder.main.window.form.camouflageGroupsDataProvider

    
    def buildList(self):
        customization = vehicles.g_cache.customization(self._nationID)
        result = []
        if customization is not None:
            groups = customization.get('camouflageGroups', { })
            for (name, info) in groups.iteritems():
                result.append({
                    'name': name,
                    'userString': info.get('userString', name),
                    'hasNew': info.get('hasNew', False),
                    'kind': CAMOUFLAGE_KINDS.get(name) })
            
        
        self._CamouflageGroupsDataProvider__list = sorted(result, cmp = self._CamouflageGroupsDataProvider__comparator)

    
    def emptyItem(self):
        return {
            'name': None,
            'userString': '',
            'hasNew': False }

    
    def list(self):
        return self._CamouflageGroupsDataProvider__list

    list = property(list)
    
    def _CamouflageGroupsDataProvider__comparator(self, item, other):
        return cmp(item.get('kind'), other.get('kind'))



class HornsDataProvider(BaseDirectAccessDP):
    
    def __init__(self):
        super(HornsDataProvider, self).__init__()
        self._HornsDataProvider__vehicleTags = set()
        self._HornsDataProvider__hornPriceFactor = 1
        self._HornsDataProvider__costs = { }
        self._HornsDataProvider__list = []

    
    def setupFlashDp(self, proxy):
        return proxy.movie.contentHolder.main.window.form.hornsDP

    
    def buildList(self, currentHornID):
        horns = vehicles.g_cache.horns()
        result = []
        if horns is not None:
            for (id, info) in horns.iteritems():
                allowedTags = info.get('vehicleTags', set())
                if self._HornsDataProvider__vehicleTags & allowedTags:
                    result.append({
                        'id': id,
                        'userString': info.get('userString', ''),
                        'gold': self.getCost(id),
                        'current': currentHornID == id })
                    continue
            
        
        self._HornsDataProvider__list = sorted(result, cmp = (lambda item, other: cmp(item.get('userString'), other.get('userString'))))

    
    def emptyItem(self):
        return {
            'id': None,
            'userString': '',
            'gold': 0,
            'current': False }

    
    def _makeCost(cls, defCost, priceFactor):
        return int(round(defCost * priceFactor))

    _makeCost = classmethod(_makeCost)
    
    def getCost(self, hornID):
        return self._makeCost(self._HornsDataProvider__costs.get(hornID, 0), self._HornsDataProvider__hornPriceFactor)

    
    def makeItem(self, hornID, isCurrent):
        horn = vehicles.g_cache.horns().get(hornID, { })
        return {
            'id': hornID,
            'userString': horn.get('userString', ''),
            'gold': self.getCost(hornID),
            'current': isCurrent }

    
    def setVehicleTypeParams(self, vehicleTags, hornPriceFactor):
        self._HornsDataProvider__vehicleTags = vehicleTags
        self._HornsDataProvider__hornPriceFactor = hornPriceFactor

    
    def setHornDefCosts(self, costs):
        self._HornsDataProvider__costs = costs

    
    def list(self):
        return self._HornsDataProvider__list

    list = property(list)


class RentalPackageDataProviderBase(BaseDirectAccessDP):
    __metaclass__ = ABCMeta
    DEFAULT_RENTAL_PACKAGE_IDX = 0
    
    def __init__(self, nationID):
        super(RentalPackageDataProviderBase, self).__init__()
        self._RentalPackageDataProviderBase__list = []
        self._RentalPackageDataProviderBase__selectedPackageIndex = self.DEFAULT_RENTAL_PACKAGE_IDX
        self._eventManager = Event.EventManager()
        self.onDataInited = Event.Event(self._eventManager)
        self.onRentalPackageChange = Event.Event(self._eventManager)
        self.nationID = nationID

    
    def setupFlashDp(self, proxy):
        pass

    setupFlashDp = abstractmethod(setupFlashDp)
    
    def getRentalPackages(self, refresh = False):
        pass

    getRentalPackages = abstractmethod(getRentalPackages)
    
    def _RentalPackageDataProviderBase__getSelectedPackageIndex(self):
        return self._RentalPackageDataProviderBase__selectedPackageIndex

    
    def _RentalPackageDataProviderBase__setSelectedPackageIndex(self, value):
        self._RentalPackageDataProviderBase__selectedPackageIndex = value
        self.onRentalPackageChange(self.selectedPackageIndex)

    selectedPackageIndex = property(_RentalPackageDataProviderBase__getSelectedPackageIndex, _RentalPackageDataProviderBase__setSelectedPackageIndex)
    selectedPackage = property((lambda self: self.requestItemAt(self._RentalPackageDataProviderBase__selectedPackageIndex)))
    
    def getIndexByDays(self, days):
        findIdx = self.DEFAULT_RENTAL_PACKAGE_IDX
        for (idx, item) in enumerate(self._RentalPackageDataProviderBase__list):
            if item.get('periodDays') == days:
                findIdx = idx
                break
                continue
        
        return findIdx

    
    def emptyItem(self):
        return {
            'periodDays': -1,
            'cost': -1,
            'isGold': False,
            'userString': '' }

    
    def list(self):
        return self._RentalPackageDataProviderBase__list

    list = property(list)
    
    def _onGetPackagesCost(self, resultID, costs, _, refresh):
        if resultID < 0:
            SystemMessages.pushI18nMessage('#system_messages:customization/camouflage_get_cost_server_error', type = SystemMessages.SM_TYPE.Error)
        else:
            self.buildList(costs)
        self.onDataInited(self.selectedPackage, refresh)

    
    def buildList(self, costs):
        items = { }
        if costs is not None:
            items = costs.copy()
        
        result = []
        nations = { }
        if items.has_key('nations'):
            nations = items.get('nations', { })
            del items['nations']
        
        if nations.has_key(self.nationID):
            items.update(nations.get(self.nationID))
        
        for (cost, isGold) in items.iteritems():
            if periodDays > 1:
                i18nPeriodDays = i18n.makeString('#menu:customization/period/days', periodDays)
            elif periodDays == 1:
                i18nPeriodDays = i18n.makeString('#menu:customization/period/day')
            else:
                i18nPeriodDays = i18n.makeString('#menu:customization/period/infinity')
            result.append({
                'periodDays': periodDays,
                'cost': cost,
                'isGold': isGold == 1,
                'userString': i18nPeriodDays })
        
        self._RentalPackageDataProviderBase__list = sorted(result, cmp = self._RentalPackageDataProviderBase__comparator, reverse = True)

    
    def _RentalPackageDataProviderBase__comparator(self, item, other):
        result = 0
        if item.get('periodDays') and other.get('periodDays'):
            result = cmp(item.get('periodDays'), other.get('periodDays'))
        elif item.get('periodDays') != other.get('periodDays'):
            if not item.get('periodDays'):
                pass
            1
            result = -1
        
        return result

    
    def getSelectedPackageIndex(self):
        return self.selectedPackageIndex

    
    def setSelectedPackageIndex(self, value):
        self.selectedPackageIndex = value



class CamouflageRentalPackageDataProvider(RentalPackageDataProviderBase):
    
    def setupFlashDp(self, proxy):
        return proxy.movie.contentHolder.main.window.form.camouflageRentalPackageDP

    
    def getRentalPackages(self, refresh = False):
        (None, BigWorld.player().shop.getCamouflageCost)((lambda resultID, costs, rev: self._onGetPackagesCost(resultID, costs, rev, refresh)))



class EmblemRentalPackageDataProvider(RentalPackageDataProviderBase):
    __metaclass__ = ABCMeta
    
    def setupFlashDp(self, proxy):
        pass

    setupFlashDp = abstractmethod(setupFlashDp)
    
    def getRentalPackages(self, refresh = False):
        (None, BigWorld.player().shop.getPlayerEmblemCost)((lambda resultID, costs, rev: self._onGetPackagesCost(resultID, costs, rev, refresh)))



class EmblemLeftRentalPackageDataProvider(EmblemRentalPackageDataProvider):
    
    def setupFlashDp(self, proxy):
        return proxy.movie.contentHolder.main.window.form.emblemLeftRentalPackageDP



class EmblemRightRentalPackageDataProvider(EmblemRentalPackageDataProvider):
    
    def setupFlashDp(self, proxy):
        return proxy.movie.contentHolder.main.window.form.emblemRightRentalPackageDP



class InscriptionRentalPackageDataProvider(RentalPackageDataProviderBase):
    __metaclass__ = ABCMeta
    
    def setupFlashDp(self, proxy):
        pass

    setupFlashDp = abstractmethod(setupFlashDp)
    
    def getRentalPackages(self, refresh = False):
        (None, BigWorld.player().shop.getPlayerInscriptionCost)((lambda resultID, costs, rev: self._onGetPackagesCost(resultID, costs, rev, refresh)))



class InscriptionLeftRentalPackageDataProvider(InscriptionRentalPackageDataProvider):
    
    def setupFlashDp(self, proxy):
        return proxy.movie.contentHolder.main.window.form.inscriptionLeftRentalPackageDP



class InscriptionRightRentalPackageDataProvider(InscriptionRentalPackageDataProvider):
    
    def setupFlashDp(self, proxy):
        return proxy.movie.contentHolder.main.window.form.inscriptionRightRentalPackageDP



class InscriptionGroupsDataProvider(BaseDirectAccessDP):
    __metaclass__ = ABCMeta
    
    def __init__(self, nationID):
        super(InscriptionGroupsDataProvider, self).__init__()
        self._InscriptionGroupsDataProvider__list = []
        self._nationID = nationID

    
    def setupFlashDp(self, proxy):
        pass

    setupFlashDp = abstractmethod(setupFlashDp)
    
    def buildList(self):
        customization = vehicles.g_cache.customization(self._nationID)
        result = []
        if customization is not None:
            groups = customization.get('inscriptionGroups', { })
            for (name, group) in groups.iteritems():
                (emblemIDs, showInShop, priceFactor, groupUserString) = group
                if showInShop:
                    result.append({
                        'name': name,
                        'userString': groupUserString,
                        'hasNew': False })
                    continue
            
        
        self._InscriptionGroupsDataProvider__list = sorted(result, cmp = self._InscriptionGroupsDataProvider__comparator)

    
    def emptyItem(self):
        return {
            'name': None,
            'userString': '',
            'hasNew': False }

    
    def list(self):
        return self._InscriptionGroupsDataProvider__list

    list = property(list)
    
    def _InscriptionGroupsDataProvider__comparator(self, item, other):
        return cmp(item.get('name'), other.get('name'))



class InscriptionLeftGroupsDataProvider(InscriptionGroupsDataProvider):
    
    def setupFlashDp(self, proxy):
        return proxy.movie.contentHolder.main.window.form.inscriptionLeftGroupsDataProvider



class InscriptionRightGroupsDataProvider(InscriptionGroupsDataProvider):
    
    def setupFlashDp(self, proxy):
        return proxy.movie.contentHolder.main.window.form.inscriptionRightGroupsDataProvider



class EmblemGroupsDataProvider(BaseDirectAccessDP):
    __metaclass__ = ABCMeta
    
    def __init__(self):
        super(EmblemGroupsDataProvider, self).__init__()
        self._EmblemGroupsDataProvider__list = []

    
    def setupFlashDp(self, proxy):
        pass

    setupFlashDp = abstractmethod(setupFlashDp)
    
    def buildList(self):
        (groups, emblems, names) = vehicles.g_cache.playerEmblems()
        result = []
        if groups is not None:
            for (name, group) in groups.iteritems():
                (emblemIDs, showInShop, priceFactor, groupUserString) = group
                if showInShop:
                    result.append({
                        'name': name,
                        'userString': groupUserString,
                        'hasNew': False })
                    continue
            
        
        self._EmblemGroupsDataProvider__list = sorted(result, cmp = self._EmblemGroupsDataProvider__comparator)

    
    def emptyItem(self):
        return {
            'name': None,
            'userString': '',
            'hasNew': False }

    
    def list(self):
        return self._EmblemGroupsDataProvider__list

    list = property(list)
    
    def _EmblemGroupsDataProvider__comparator(self, item, other):
        return cmp(item.get('name'), other.get('name'))



class EmblemLeftGroupsDataProvider(EmblemGroupsDataProvider):
    
    def setupFlashDp(self, proxy):
        return proxy.movie.contentHolder.main.window.form.emblemLeftGroupsDataProvider



class EmblemRightGroupsDataProvider(EmblemGroupsDataProvider):
    
    def setupFlashDp(self, proxy):
        return proxy.movie.contentHolder.main.window.form.emblemRightGroupsDataProvider



class EmblemsDataProvider(UIInterface):
    
    def __init__(self):
        UIInterface.__init__(self)
        self._defCost = -1
        self._isGold = 0
        self._vehPriceFactor = 1
        self.currentItemID = None
        self._flashDP = None

    
    def _makeTextureUrl(cls, width, height, texture, itemSize, coords):
        if texture is None or len(texture) == 0:
            return ''
        if texture.startswith('gui'):
            texture = texture.replace('gui', '..', 1)
        
        return texture

    _makeTextureUrl = classmethod(_makeTextureUrl)
    
    def _makeSmallTextureUrl(cls, texture, itemSize, coords):
        return EmblemsDataProvider._makeTextureUrl(67, 67, texture, itemSize, coords)

    _makeSmallTextureUrl = classmethod(_makeSmallTextureUrl)
    
    def _makeCost(cls, defCost, vehPriceFactor, itemPriceFactor):
        return int(round(defCost * vehPriceFactor * itemPriceFactor))

    _makeCost = classmethod(_makeCost)
    
    def _makeDescription(cls, groupName, userString):
        result = ''
        if len(groupName) > 0 and len(userString) > 0:
            result = makeTooltip(header = groupName, body = userString)
        
        return result

    _makeDescription = classmethod(_makeDescription)
    
    def makeItem(self, itemID, isCurrent, lifeCycle, timeLeftString):
        (groups, emblems, names) = vehicles.g_cache.playerEmblems()
        itemInfo = None
        if emblems is not None:
            itemInfo = self._constructObject(itemID, groups, emblems, isCurrent, lifeCycle)
        
        if itemInfo is not None:
            itemInfo['timeLeft'] = timeLeftString
        else:
            itemInfo = {
                'timeLeft': timeLeftString,
                'id': itemID,
                'texturePath': None,
                'description': '',
                'price': {
                    'cost': 0,
                    'isGold': False },
                'current': isCurrent }
        return itemInfo

    
    def _constructObject(self, itemID, groups, emblems, isCurrent = False, withoutCheck = True):
        itemInfo = None
        emblem = emblems.get(itemID, None)
        if emblem is not None:
            (groupName, texture, bumpMap, emblemUserString) = emblem
            (emblemIDs, showInShop, priceFactor, groupUserString) = groups.get(groupName)
            if withoutCheck or showInShop:
                itemInfo = {
                    'id': itemID,
                    'texturePath': self._makeSmallTextureUrl(texture, None, None),
                    'description': self._makeDescription(groupUserString, emblemUserString),
                    'price': {
                        'cost': self._makeCost(self._defCost, self._vehPriceFactor, priceFactor),
                        'isGold': self._isGold == 1 },
                    'current': isCurrent }
            
        
        return itemInfo

    
    def getCost(self, itemID):
        priceFactor = 0
        (groups, emblems, names) = vehicles.g_cache.playerEmblems()
        emblem = emblems.get(itemID)
        if emblem is not None:
            (groupName, texture, bumpFile, emblemUserString) = emblem
            (emblemIDs, showInShop, priceFactor, groupUserString) = groups.get(groupName)
        
        return (self._makeCost(self._defCost, self._vehPriceFactor, priceFactor), self._isGold)

    
    def getCostForPackagePrice(self, itemID, packagePrice, isGold):
        return (-1, False)

    
    def setVehicleTypeParams(self, vehPriceFactor, itemID):
        self._vehPriceFactor = vehPriceFactor
        self.currentItemID = itemID

    
    def setDefaultCost(self, defCost, isGold):
        self._defCost = defCost
        self._isGold = isGold == 1

    
    def _EmblemsDataProvider__comparator(self, item, other):
        return cmp(item['id'], other['id'])

    
    def populateUI(self, proxy):
        super(EmblemsDataProvider, self).populateUI(proxy)
        self._flashDP = proxy.movie.contentHolder.main.window.form.emblemDP
        self._flashDP.script = self
        LOG_DEBUG('EmblemsDataProvider populateUI')

    
    def dispossessUI(self):
        LOG_DEBUG('EmblemsDataProvider dispossessUI', self._flashDP.groupName)
        self._flashDP.script = None
        self._flashDP = None
        super(EmblemsDataProvider, self).dispossessUI()

    
    def onRequestList(self, groupName):
        (groups, emblems, names) = vehicles.g_cache.playerEmblems()
        group = groups.get(groupName)
        result = []
        if group is not None:
            (emblemIDs, showInShop, priceFactor, groupUserString) = group
            if showInShop:
                for id in emblemIDs:
                    itemInfo = self._constructObject(id, groups, emblems, self.currentItemID == id, False)
                    if itemInfo is not None:
                        result.append(itemInfo)
                        continue
                
            
        
        return sorted(result, cmp = self._EmblemsDataProvider__comparator)

    
    def refresh(self):
        self._flashDP.invalidate(True)



class EmblemsLeftDataProvider(EmblemsDataProvider):
    
    def populateUI(self, proxy):
        self.uiHolder = proxy
        self._flashDP = proxy.movie.contentHolder.main.window.form.emblemLeftDP
        self._flashDP.script = self
        LOG_DEBUG('EmblemsLeftDataProvider populateUI')



class EmblemsRightDataProvider(EmblemsDataProvider):
    
    def populateUI(self, proxy):
        self.uiHolder = proxy
        self._flashDP = proxy.movie.contentHolder.main.window.form.emblemRightDP
        self._flashDP.script = self
        LOG_DEBUG('EmblemsRightDataProvider populateUI')



class InscriptionDataProvider(EmblemsDataProvider):
    
    def __init__(self, nationID):
        super(InscriptionDataProvider, self).__init__()
        self.nationID = nationID

    
    def _makeSmallTextureUrl(cls, texture, itemSize, coords):
        return EmblemsDataProvider._makeTextureUrl(150, 76, texture, itemSize, coords)

    _makeSmallTextureUrl = classmethod(_makeSmallTextureUrl)
    
    def makeItem(self, itemID, isCurrent, lifeCycle, timeLeftString):
        customization = vehicles.g_cache.customization(self.nationID)
        itemInfo = None
        if customization is not None:
            groups = customization.get('inscriptionGroups', { })
            inscriptions = customization.get('inscriptions', { })
            if inscriptions is not None:
                itemInfo = self._constructObject(itemID, groups, inscriptions, isCurrent, lifeCycle)
            
            if itemInfo is not None:
                itemInfo['timeLeft'] = timeLeftString
            else:
                itemInfo = {
                    'timeLeft': timeLeftString,
                    'id': itemID,
                    'texturePath': None,
                    'description': '',
                    'price': {
                        'cost': 0,
                        'isGold': False },
                    'current': isCurrent }
        
        return itemInfo

    
    def _constructObject(self, itemID, groups, inscriptions, isCurrent = False, withoutCheck = True):
        itemInfo = None
        inscription = inscriptions.get(itemID, None)
        if inscription is not None:
            (groupName, texture, bumpMap, inscriptionUserString) = inscription
            (inscriptionIDs, showInShop, priceFactor, groupUserString) = groups.get(groupName)
            if withoutCheck or showInShop:
                itemInfo = {
                    'id': itemID,
                    'texturePath': self._makeSmallTextureUrl(texture, None, None),
                    'description': self._makeDescription(groupUserString, inscriptionUserString),
                    'price': {
                        'cost': self._makeCost(self._defCost, self._vehPriceFactor, priceFactor),
                        'isGold': self._isGold == 1 },
                    'current': isCurrent }
            
        
        return itemInfo

    
    def getCost(self, itemID):
        priceFactor = 0
        customization = vehicles.g_cache.customization(self.nationID)
        if customization is not None:
            groups = customization.get('inscriptionGroups', { })
            inscriptions = customization.get('inscriptions', { })
            inscription = inscriptions.get(itemID)
            if inscription is not None:
                (groupName, texture, bumpMap, inscriptionUserString) = inscription
                (inscriptionIDs, showInShop, priceFactor, groupUserString) = groups.get(groupName)
            
        
        return (self._makeCost(self._defCost, self._vehPriceFactor, priceFactor), self._isGold)

    
    def getCostForPackagePrice(self, itemID, packagePrice, isGold):
        return (-1, False)

    
    def onRequestList(self, groupName):
        customization = vehicles.g_cache.customization(self.nationID)
        result = []
        if customization is not None:
            groups = customization.get('inscriptionGroups', { })
            group = groups.get(groupName, { })
            inscriptions = customization.get('inscriptions', { })
            if group is not None:
                (emblemIDs, showInShop, priceFactor, groupUserString) = group
                if showInShop:
                    for id in emblemIDs:
                        itemInfo = self._constructObject(id, groups, inscriptions, self.currentItemID == id, False)
                        if itemInfo is not None:
                            result.append(itemInfo)
                            continue
                    
                
            
        
        return sorted(result, cmp = self._InscriptionDataProvider__comparator)

    
    def _InscriptionDataProvider__comparator(self, item, other):
        return cmp(item['id'], other['id'])



class InscriptionLeftDataProvider(InscriptionDataProvider):
    
    def populateUI(self, proxy):
        self.uiHolder = proxy
        self._flashDP = proxy.movie.contentHolder.main.window.form.inscriptionLeftDP
        self._flashDP.script = self
        LOG_DEBUG('InscriptionLeftDataProvider populateUI')



class InscriptionRightDataProvider(InscriptionDataProvider):
    
    def populateUI(self, proxy):
        self.uiHolder = proxy
        self._flashDP = proxy.movie.contentHolder.main.window.form.inscriptionRightDP
        self._flashDP.script = self
        LOG_DEBUG('InscriptionRightDataProvider populateUI')



class CamouflagesDataProvider(UIInterface):
    
    def __init__(self, nationID):
        UIInterface.__init__(self)
        self.currentGroup = None
        self._CamouflagesDataProvider__defCost = -1
        self._CamouflagesDataProvider__isGold = 0
        self._CamouflagesDataProvider__vehPriceFactor = 1
        self.currentItemID = None
        self._flashDP = None
        self._nationID = nationID

    
    def _makeTextureUrl(cls, width, height, texture, colors, armorColor, lifeCycle = None):
        if texture is None or len(texture) == 0:
            return ''
        weights = Math.Vector4((colors[0] >> 24) / 255, (colors[1] >> 24) / 255, (colors[2] >> 24) / 255, (colors[3] >> 24) / 255)
        if lifeCycle is not None:
            (startTime, days) = lifeCycle
            if days > 0:
                timeAmount = float((time.time() - startTime) / days * 86400)
                if timeAmount > 1:
                    weights *= _CAMOUFLAGE_MIN_INTENSITY
                elif timeAmount > 0:
                    weights *= (1 - timeAmount) * (1 - _CAMOUFLAGE_MIN_INTENSITY) + _CAMOUFLAGE_MIN_INTENSITY
                
            
        
        return 'img://camouflage,{0:d},{1:d},"{2:>s}",{3[0]:d},{3[1]:d},{3[2]:d},{3[3]:d},{4[0]:n},{4[1]:n},{4[2]:n},{4[3]:n},{5:d}'.format(width, height, texture, colors, weights, armorColor)

    _makeTextureUrl = classmethod(_makeTextureUrl)
    
    def _makeSmallTextureUrl(cls, texture, colors, armorColor, lifeCycle = None):
        return CamouflagesDataProvider._makeTextureUrl(67, 67, texture, colors, armorColor, lifeCycle = lifeCycle)

    _makeSmallTextureUrl = classmethod(_makeSmallTextureUrl)
    
    def _makeCost(cls, defCost, vehPriceFactor, camPriceFactor):
        return int(round(defCost * vehPriceFactor * camPriceFactor))

    _makeCost = classmethod(_makeCost)
    
    def _makeDescription(cls, groups, groupName, description):
        if not description and groupName:
            return ''
        name = groups.get(groupName, { }).get('userString')
        return makeTooltip(header = name, body = description)

    _makeDescription = classmethod(_makeDescription)
    
    def getCamouflageDescr(self, camouflageID):
        camouflage = None
        customization = vehicles.g_cache.customization(self._nationID)
        if customization is not None:
            camouflages = customization.get('camouflages', { })
            camouflage = camouflages.get(camouflageID, None)
        
        return camouflage

    
    def makeItem(self, camouflageID, isCurrent, lifeCycle, timeLeftString, kind):
        customization = vehicles.g_cache.customization(self._nationID)
        camouflageInfo = None
        if customization is not None:
            groups = customization.get('camouflageGroups', { })
            armorColor = customization.get('armorColor', 0)
            camouflageInfo = self._constructObject(camouflageID, groups, customization.get('camouflages', { }), armorColor, lifeCycle, isCurrent)
        
        if camouflageInfo is not None:
            camouflageInfo['timeLeft'] = timeLeftString
        else:
            camouflageInfo = {
                'timeLeft': timeLeftString,
                'id': camouflageID,
                'texturePath': None,
                'description': self.getDefaultDescription(kind),
                'price': {
                    'cost': 0,
                    'isGold': False },
                'isNew': False,
                'invisibilityLbl': '',
                'current': False }
        return camouflageInfo

    
    def _constructObject(self, cID, groups, camouflages, armorColor, lifeCycle = None, isCurrent = False, withoutCheck = True, currentCompactDescriptor = None):
        camouflageInfo = None
        camouflage = camouflages.get(cID, None)
        if camouflage is not None:
            if withoutCheck or camouflage.get('showInShop', False):
                denyCompactDescriptor = camouflage.get('deny')
                if currentCompactDescriptor not in denyCompactDescriptor or currentCompactDescriptor is None:
                    invisibilityFactor = camouflage.get('invisibilityFactor', 1)
                    invisibilityPercent = int(round((invisibilityFactor - 1) * 100))
                    invisibilityLbl = gui.makeHtmlString('html_templates:lobby/customization', 'camouflage-hint', {
                        'percents': invisibilityPercent }, sourceKey = self._CamouflagesDataProvider__getKindById(camouflage.get('kind', 0)))
                    camouflageInfo = {
                        'id': cID,
                        'texturePath': self._makeSmallTextureUrl(camouflage.get('texture'), camouflage.get('colors', (0, 0, 0, 0)), armorColor, lifeCycle = lifeCycle),
                        'description': self._makeDescription(groups, camouflage.get('groupName', ''), camouflage.get('description', '')),
                        'price': {
                            'cost': self._makeCost(self._CamouflagesDataProvider__defCost, self._CamouflagesDataProvider__vehPriceFactor, camouflage.get('priceFactor', 1)),
                            'isGold': self._CamouflagesDataProvider__isGold == 1 },
                        'isNew': camouflage.get('isNew', False),
                        'invisibilityLbl': invisibilityLbl,
                        'current': isCurrent }
                
            
        return camouflageInfo

    
    def getCost(self, camouflageID):
        camouflage = vehicles.g_cache.customization(self._nationID).get('camouflages', { }).get(camouflageID, { })
        return (self._makeCost(self._CamouflagesDataProvider__defCost, self._CamouflagesDataProvider__vehPriceFactor, camouflage.get('priceFactor', 1)), self._CamouflagesDataProvider__isGold)

    
    def getCostForPackagePrice(self, camouflageID, packagePrice, isGold):
        camouflage = vehicles.g_cache.customization(self._nationID).get('camouflages', { }).get(camouflageID, { })
        return (self._makeCost(packagePrice, self._CamouflagesDataProvider__vehPriceFactor, camouflage.get('priceFactor', 1)), isGold)

    
    def setVehicleTypeParams(self, vehPriceFactor, camouflageID):
        self._CamouflagesDataProvider__vehPriceFactor = vehPriceFactor
        self.currentItemID = camouflageID

    
    def setDefaultCost(self, defCost, isGold):
        self._CamouflagesDataProvider__defCost = defCost
        self._CamouflagesDataProvider__isGold = isGold == 1

    
    def _CamouflagesDataProvider__comparator(self, item, other):
        if item['isNew'] ^ other['isNew']:
            if item['isNew']:
                pass
            1
            result = 1
        else:
            result = cmp(item['id'], other['id'])
        return result

    
    def _CamouflagesDataProvider__getKindById(self, kindId):
        kind = 'winter'
        for (k, v) in CAMOUFLAGE_KINDS.iteritems():
            if v == kindId:
                kind = k
                continue
        
        return kind

    
    def populateUI(self, proxy):
        super(CamouflagesDataProvider, self).populateUI(proxy)
        self._flashDP = proxy.movie.contentHolder.main.window.form.camouflageDP
        self._flashDP.script = self
        LOG_DEBUG('CamouflagesDataProvider populateUI')

    
    def dispossessUI(self):
        LOG_DEBUG('CamouflagesDataProvider dispossessUI', self._flashDP.groupName)
        self._flashDP.script = None
        self._flashDP = None
        super(CamouflagesDataProvider, self).dispossessUI()

    
    def getDefaultHintText(self, _):
        return gui.makeHtmlString('html_templates:lobby/customization', 'camouflage-hint', sourceKey = 'default')

    
    def getDefaultDescription(self, kindID):
        kindKey = '#tooltips:customization/camouflage/{0:>s}'.format(self._CamouflagesDataProvider__getKindById(kindID))
        bodyKey = '#tooltips:customization/camouflage/empty'
        return makeTooltip(body = i18n.makeString(bodyKey, kind = i18n.makeString(kindKey)))

    
    def setGroupCurrentItemId(self, itemId):
        if itemId is not None:
            pass
        1
        self.currentItemID = None

    
    def onRequestList(self, groupName):
        self.currentGroup = groupName
        customization = vehicles.g_cache.customization(self._nationID)
        result = []
        if customization is not None:
            groups = customization.get('camouflageGroups', { })
            group = groups.get(groupName, { })
            camouflages = customization.get('camouflages', { })
            armorColor = customization.get('armorColor', 0)
            ids = group.get('ids', [])
            currCmpctDescr = g_currentVehicle.vehicle.descriptor.type.compactDescr
            for id in ids:
                camouflageInfo = self._constructObject(id, groups, camouflages, armorColor, isCurrent = self.currentItemID == id, withoutCheck = False, currentCompactDescriptor = currCmpctDescr)
                if camouflageInfo is not None:
                    result.append(camouflageInfo)
                    continue
            
        
        return sorted(result, cmp = self._CamouflagesDataProvider__comparator)

    
    def refresh(self):
        self._flashDP.invalidate(True)



