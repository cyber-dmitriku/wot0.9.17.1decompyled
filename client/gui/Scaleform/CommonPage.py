# Source Generated with Decompyle++
# File: CommonPage.pyc (Python 2.6)

import BigWorld
import GUI
import datetime
import Keys
import weakref
import Event
import constants
import account_helpers
import nations
import dossiers
from adisp import process, async
from CurrentVehicle import g_currentVehicle
from debug_utils import LOG_DEBUG, LOG_CURRENT_EXCEPTION, LOG_ERROR
from exceptions import DeprecationWarning
from gui import SystemMessages, GUI_NATIONS, GUI_SETTINGS
from gui.ClientUpdateManager import g_clientUpdateManager
from gui.Scaleform import main_interfaces, VoiceChatInterface
from gui.Scaleform.BattleDispatcherInterface import BattleDispatcherInterface
from gui.Scaleform.CursorDelegator import g_cursorDelegator
from gui.Scaleform.SettingsInterface import SettingsInterface
from gui.Scaleform.SoundManager import SoundManager
from gui.Scaleform.Waiting import Waiting
from gui.Scaleform.CaptchaView import CaptchaView
from gui.Scaleform.windows import GUIWindow
from gui.Scaleform.TankmenInterface import TankmenInterface
from gui.Scaleform.ToolTipManager import ToolTipManager
from gui.Scaleform.BuyGoldWindow import BuyGoldWindow
from gui.Scaleform.SoundEventManager import SoundEventManager
from gui.Scaleform.utils.functions import async_showConfirmDialog
from gui.Scaleform.BattleResults import BattleResultsManager
from gui.Scaleform.utils.key_mapping import getScaleformKey, voidSymbol
from gui.Scaleform.utils.gui_items import getItemByCompact, formatPrice, InventoryVehicle
from gui.Scaleform.utils.functions import makeTooltip, stripShortDescrTags
from gui.Scaleform.utils.requesters import StatsRequester, Requester
from gui.Scaleform.utils.HangarSpace import g_hangarSpace
from gui.Scaleform.utils.RareAchievementsCache import g_rareAchievesCache
from messenger.gui import MessengerDispatcher
from PlayerEvents import g_playerEvents
from items import vehicles
from helpers.links import getPaymentWebsiteURL, openPaymentWebsite, openFinPasswordWebsite
from helpers.i18n import convert, makeString
from helpers.time_utils import makeLocalServerTime
from gui.Scaleform.utils import dossiers_utils
from items.vehicles import getDefaultAmmoForGun, parseIntCompactDescr
from account_helpers.AccountSettings import AccountSettings
from items.tankmen import getSkillsConfig
from external_strings_utils import isPasswordValid
from LogitechMonitor import LogitechMonitor
import BattleReplay

class CommonPage(GUIWindow):
    '''
\tInterface common swf, serves:
\t- implementation common lobby functions (collect statistics, exit/logoff, etc.)
\t- to load the appropriate interface is loaded from flash page
\t'''
    _CommonPage__mainInterface = None
    _CommonPage__settingsInterface = None
    currentInterface = None
    _CommonPage__statsCallbackId = None
    _CommonPage__isSubscribe = False
    _CommonPage__soundManager = None
    
    def __init__(self):
        self.proxy = weakref.proxy(self)
        GUIWindow.__init__(self, 'common.swf')
        self._CommonPage__settingsInterface = None
        self._CommonPage__battleDispatcher = None
        self.tutorialDispatcher = None
        self.commandsBinded = False
        self.gold = 0
        self.credits = 0
        self.freeXP = 0
        self.eventSoundChecker = SoundEventManager()
        self.addExternalCallbacks({
            'Loader.LoadStart': self.onLoadStart,
            'Loader.LoadInit': self.onLoadInit,
            'common.getAccountInfo': self.onUpdateAccountInfo,
            'common.Exchange': self.onExchange,
            'common.spaceMove': self.onSpaceMove,
            'common.getModuleInfo': self.onModuleInfo,
            'common.getAchievementInfo': self.onAchievementInfo,
            'common.getVehicleInfo': self.onVehicleInfo,
            'common.getXPExchangeInfo': self.getExchangeXPInfo,
            'common.XPToTmen': self.onXPToTmen,
            'profile.getPremiumCost': self.getPremiumCost,
            'profile.PrebiumBuy': self.buyPremium,
            'common.payment': self.onPayment,
            'common.steamPayment': self.onSteamPayment,
            'common.restoreFinPass': self.onFinPasswordWebPage,
            'common.getNations': self.getNations,
            'common.getShopBuyWindowStats': self._CommonPage__onShopBuyWindowGetStats,
            'common.buyItem': self._CommonPage__onBuyItem,
            'common.saveShopBuyWindowSetting': self._CommonPage__onSaveShopBuyWindowSetting,
            'common.showWaiting': self.onShowWaiting,
            'common.hideWaiting': self.onCloseWaiting,
            'common.transferMoney': self.onTransferMoney,
            'common.transferMoneyPopulateUI': self.onTransferMoneyPopulateUI,
            'common.showMoneyTransfer': self.onShowMoneyTransfer,
            'gatheringWindow.submit': self.onGatheringWindowSubmit,
            'gatheringWindow.populate': self.onPopulateGatheringWindow,
            'exchangeWindow.submit': self.onExchangeXPWindowSubmit })
        self.onXPConverted = Event.Event()
        BigWorld.wg_setRedefineKeysMode(True)

    
    def afterCreate(self):
        GUIWindow.afterCreate(self)
        LOG_DEBUG('[CommonPage] afterCreate')
        self.movie.setFocussed()
        setattr(self.movie, '_global.wg_isDevelopment', constants.IS_DEVELOPMENT)
        setattr(self.movie, '_global.wg_isShowLanguageBar', constants.SHOW_LANGUAGE_BAR)
        setattr(self.movie, '_global.wg_isShowServerStats', constants.IS_SHOW_SERVER_STATS)
        setattr(self.movie, '_global.wg_isShowVoiceChat', GUI_SETTINGS.voiceChat)
        setattr(self.movie, '_global.wg_isChina', constants.IS_CHINA)
        BigWorld.wg_setScreenshotNotifyCallback(self._CommonPage__screenshotNotifyCallback)
        self._CommonPage__soundManager = SoundManager()
        self._CommonPage__soundManager.populateUI(self.proxy)
        self.buyGoldWindow = BuyGoldWindow()
        self.buyGoldWindow.populateUI(self.proxy)
        self.tooltipManager = ToolTipManager()
        self.tooltipManager.populateUI(self.proxy)
        self.battleResults = BattleResultsManager()
        self.battleResults.populateUI(self.proxy)
        VoiceChatInterface.g_instance.populateUI(self.proxy)
        if self._CommonPage__mainInterface:
            self._CommonPage__mainInterface.populateUI(self.proxy)
        
        if not len(getPaymentWebsiteURL()) != 0:
            pass
        paymentBtnEnabled = constants.IS_VIETNAM
        self.call('common.disablePaymentButon', [
            not paymentBtnEnabled])
        g_guiResetters = g_guiResetters
        import game
        g_guiResetters.add(self.onUpdateStage)
        self.onUpdateStage()
        BattleReplay.g_replayCtrl.onCommonSwfLoaded()

    
    def beforeDelete(self):
        self.eventSoundChecker.dispossessUI()
        self.buyGoldWindow.dispossessUI()
        if self._CommonPage__soundManager:
            self._CommonPage__soundManager.dispossessUI()
            self._CommonPage__soundManager = None
        
        if self.tooltipManager is not None:
            self.tooltipManager.dispossessUI()
            self.tooltipManager = None
        
        if self.battleResults is not None:
            self.battleResults.dispossessUI()
            self.battleResults = None
        
        if VoiceChatInterface.g_instance:
            VoiceChatInterface.g_instance.dispossessUI()
        
        if self._CommonPage__mainInterface:
            self._CommonPage__mainInterface.dispossessUI()
        
        self._unsubscribe()
        LOG_DEBUG('[CommonPage] beforeDelete')
        GUIWindow.beforeDelete(self)
        g_guiResetters = g_guiResetters
        import game
        g_guiResetters.discard(self.onUpdateStage)
        BattleReplay.g_replayCtrl.onCommonSwfUnloaded()

    
    def bindExCallbackToKey(self, key, command, function):
        
        try:
            gfx_key = getScaleformKey(key)
            if gfx_key != voidSymbol:
                self.movie.invoke(('bindExCallbackToKey', [
                    gfx_key,
                    command]))
                self.addExternalCallback(command, function)
            else:
                LOG_ERROR("Can't convert key:", key)
        except:
            LOG_CURRENT_EXCEPTION()


    
    def clearExCallbackToKey(self, key, command, function = None):
        
        try:
            gfx_key = getScaleformKey(key)
            if gfx_key != voidSymbol:
                self.movie.invoke(('clearExCallbackToKey', [
                    gfx_key]))
                self.removeExternalCallback(command, function = function)
            else:
                LOG_ERROR("Can't convert key:", key)
        except:
            LOG_CURRENT_EXCEPTION()


    
    def _subscribe(self):
        if self._CommonPage__isSubscribe:
            return None
        self._CommonPage__isSubscribe = True
        g_clientUpdateManager.addCallbacks({
            'stats.credits': self.setCredits,
            'stats.gold': self.setGold,
            'stats.freeXP': self.setFreeXP,
            'stats.clanInfo': self.setClanInfo,
            'stats.denunciationsLeft': self.setDenunciationsCount,
            'stats.hasFinPassword': self.onMoneyTransferUpdate,
            'stats.vehTypeXP': self._CommonPage__changeCurrentVehicle,
            'account': self.onAccountChanged,
            'shop.exchangeRate': self.setExchangeRate,
            'inventory.8.compDescr': self.onTankmanChanged })
        g_currentVehicle.onChanged += self._CommonPage__changeCurrentVehicle
        g_playerEvents.onServerStatsReceived += self.onStatsReceived
        g_playerEvents.onVehicleLockChanged += self.lockChange
        g_playerEvents.onVehicleBecomeElite += self.onVehicleBecomeElite
        g_playerEvents.onShopResyncStarted += self.onShopResyncStarted
        g_playerEvents.onShopResync += self.onShopResync
        g_playerEvents.onCenterIsLongDisconnected += self.centerIsUnavailable
        self.centerIsUnavailable(True)
        self.captcha = CaptchaView()
        self.captcha.populateUI(self.proxy)
        MessengerDispatcher.g_instance.currentWindow.populateUI(self)
        self._CommonPage__settingsInterface = SettingsInterface(enableRedefineKeysMode = False)
        self._CommonPage__settingsInterface.populateUI(self.proxy)
        self._CommonPage__battleDispatcher = BattleDispatcherInterface()
        self._CommonPage__battleDispatcher.populateUI(self.proxy)

    
    def _unsubscribe(self):
        if not self._CommonPage__isSubscribe:
            return None
        self._CommonPage__isSubscribe = False
        g_currentVehicle.onChanged -= self._CommonPage__changeCurrentVehicle
        g_playerEvents.onServerStatsReceived -= self.onStatsReceived
        g_playerEvents.onVehicleLockChanged -= self.lockChange
        g_playerEvents.onVehicleBecomeElite -= self.onVehicleBecomeElite
        g_playerEvents.onShopResyncStarted -= self.onShopResyncStarted
        g_playerEvents.onShopResync -= self.onShopResync
        g_playerEvents.onCenterIsLongDisconnected -= self.centerIsUnavailable
        self.captcha.dispossessUI()
        self.captcha = None
        if self.tutorialDispatcher is not None:
            self.tutorialDispatcher.dispossessUI()
            self.tutorialDispatcher = None
        
        MessengerDispatcher.g_instance.currentWindow.dispossessUI()
        if self._CommonPage__statsCallbackId is not None:
            BigWorld.cancelCallback(self._CommonPage__statsCallbackId)
            self._CommonPage__statsCallbackId = None
        
        g_clientUpdateManager.removeObjectCallbacks(self)
        self._CommonPage__settingsInterface.dispossessUI()
        self._CommonPage__settingsInterface = None
        self._CommonPage__battleDispatcher.dispossessUI()
        self._CommonPage__battleDispatcher = None

    
    def __populateData(self, callback):
        yield self.tooltipManager.request()
        yield StatsRequester().getCredits()
        credits = None
        yield StatsRequester().getGold()
        gold = None
        self.eventSoundChecker.populateUI(self, credits, gold)
        callback(True)

    _CommonPage__populateData = async(process(__populateData))
    
    def soundManager(self):
        return self._CommonPage__soundManager

    soundManager = property(soundManager)
    
    def onMoneyTransferUpdate(self, *args):
        self.call('MoneyTransfer.update', [])

    
    def onAccountChanged(self, args):
        if 'attrs' in args or 'premiumExpiryTime' in args:
            attrs = args.get('attrs', 0)
            expiryTime = args.get('premiumExpiryTime', 0)
            if expiryTime > 0:
                attrs |= constants.ACCOUNT_ATTR.PREMIUM
            
            self.setAccountsAttrs(attrs, premiumExpiryTime = expiryTime)
        

    
    def onTankmanChanged(self, args):
        for (id, compDescr) in args.iteritems():
            self._CommonPage__notifyFlashTankmanChange(id)
        

    
    def clearCommands(self):
        cmdMapping = g_instance
        import CommandMapping
        key = cmdMapping.get('CMD_VOICECHAT_MUTE')
        self.clearExCallbackToKey(key, 'VoiceChat.PushToTalk', function = self.onVoiceChatPTT)

    
    def bindCommands(self):
        self.commandsBinded = True
        cmdMapping = g_instance
        import CommandMapping
        key = cmdMapping.get('CMD_VOICECHAT_MUTE')
        self.bindExCallbackToKey(key, 'VoiceChat.PushToTalk', self.onVoiceChatPTT)

    
    def _CommonPage__screenshotNotifyCallback(self, path):
        SystemMessages.g_instance.pushMessage(convert(makeString('#menu:screenshot/save')) % {
            'path': path }, SystemMessages.SM_TYPE.Information)

    
    def showCursor(self, isShow):
        self.call('common.showCursor', [
            isShow])

    
    def _CommonPage__callPasswordResponse(self, code, errString):
        result = 'valid'
        if code < 0:
            if errString == 'WRONG_PASSWD':
                result = 'invalid'
            elif errString == 'WRONG_PASSWD_LIMIT':
                result = 'limit'
            elif errString == 'WRONG_PASSWD_VALID':
                result = 'wrong'
            
        
        self.call('common.validatePasswordResponse', [
            result == 'valid',
            makeString('#dialogs:finance_dialog/results/%s' % result)])

    
    def onShowMoneyTransfer(self, callbackId, uid, userName):
        yield StatsRequester().getRestrictions()
        rs = None
        if constants.RESTRICTION_TYPE.TRADING in rs:
            for r in rs[constants.RESTRICTION_TYPE.TRADING].itervalues():
                lExpiryTime = makeLocalServerTime(r.get('expiryTime', 0))
                if r.get('expiryTime', 0) == 0 or datetime.datetime.utcfromtimestamp(lExpiryTime) > datetime.datetime.utcnow():
                    reason = makeString('#dialogs:moneyTransferRestriction/message') % makeString(r.get('reason', ''))
                    expiryTime = r.get('expiryTime', 0)
                    if expiryTime != 0:
                        expiry = makeString('#dialogs:moneyTransferRestriction/message_expiry') % BigWorld.wg_getLongDateFormat(expiryTime) + ' ' + BigWorld.wg_getShortTimeFormat(expiryTime)
                    else:
                        expiry = ''
                    self.call('common.showMessageDialog', [
                        'moneyTransferRestriction',
                        False,
                        False,
                        '%s %s' % (reason, expiry)])
                    return None
            
        
        self.call('common.showMoneyTransfer', [
            uid,
            userName])

    onShowMoneyTransfer = process(onShowMoneyTransfer)
    
    def onTransferMoney(self, callbackId, uid, userName, gold, password = ''):
        yield StatsRequester().hasFinPassword()
        has_fin_pass = None
        
        def callback(code, errString):
            self._CommonPage__callPasswordResponse(code, errString)
            Waiting.hide('transferMoney')
            if code < 0:
                if not (errString == 'WRONG_PASSWD') and not (errString == 'WRONG_PASSWD_LIMIT'):
                    SystemMessages.g_instance.pushMessage(makeString('#system_messages:tradingError/%s' % errString), SystemMessages.SM_TYPE.Error)
                
                return None

        Waiting.show('transferMoney')
        if password != '':
            password = password.strip()
            if not isPasswordValid(password):
                self._CommonPage__callPasswordResponse(-1, 'WRONG_PASSWD_VALID')
                Waiting.hide('transferMoney')
                return None
        
        BigWorld.player().trader.makeOffer_sellGold(password, 'Account', int(uid), 20, int(gold), 0, callback)

    onTransferMoney = process(onTransferMoney)
    
    def onTransferMoneyPopulateUI(self, callbackId, uid, userName):
        Waiting.show('loadStats')
        yield StatsRequester().getUserClanInfo(userName)
        (userClanId, userClanInfo) = None
        yield StatsRequester().getGold()
        gold = None
        yield StatsRequester().getTradeFees()
        fees = None
        yield StatsRequester().getClanInfo()
        clanInfo = None
        yield StatsRequester().hasFinPassword()
        has_fin_pass = None
        if clanInfo is not None and userClanInfo is not None:
            pass
        is_clan = clanInfo[2] == userClanInfo[2]
        args = [
            userName,
            is_clan,
            gold,
            has_fin_pass]
        if is_clan:
            pass
        1
        fee = fees.get('sameClan'('default', (0, 0))[1], 2)
        args.append(fee)
        descr = makeString('#dialogs:moneyTransfer/labelNotification') % int(fee * 100)
        if not is_clan:
            pass
        1
        descr + makeString('#dialogs:moneyTransfer/not_a_clan')(descr)
        self.call('common.moneyTransferPopulateUI', args)
        Waiting.hide('loadStats')

    onTransferMoneyPopulateUI = process(onTransferMoneyPopulateUI)
    
    def onPopulateGatheringWindow(self, callbackId, isReset, *args):
        Waiting.show('loadStats')
        checkedVcls = list(args)
        yield StatsRequester().getCredits()
        credits = None
        yield StatsRequester().getGold()
        gold = None
        yield StatsRequester().getFreeXPConversion()
        rate = None
        actionRate = rate
        if rate:
            yield StatsRequester().getVehicleTypeExperiences()
            xps = None
            yield StatsRequester().getEliteVehicles()
            eliteVcls = None
            yield Requester('vehicle').getFromShop()
            vcls = None
            yield Requester('vehicle').getFromInventory()
            vclsInv = None
            
            def getSmallIcon(vehType):
                return '../maps/icons/vehicle/small/%s.png' % vehType.name.replace(':', '-')

            actionDiscount = 1 - float(actionRate[1]) / rate[1]
            values = [
                credits,
                gold,
                rate[0],
                rate[1],
                100 * actionDiscount]
            for vehicle in vcls:
                if vehicle.descriptor.type.compactDescr in eliteVcls:
                    xp = xps.get(vehicle.descriptor.type.compactDescr, 0)
                    if not xp:
                        continue
                    
                    values.append(vehicle.pack())
                    values.append(vehicle.type)
                    values.append(vehicle.shortName)
                    values.append(xp)
                    if isReset:
                        pass
                    1
                    True(vehicle.pack() in checkedVcls)
                    values.append(getSmallIcon(vehicle.descriptor.type))
                    values.append(vehicle.nation)
                    continue
            
            self.call('gatheringWindow.populate', values)
        
        Waiting.hide('loadStats')

    onPopulateGatheringWindow = process(onPopulateGatheringWindow)
    
    def onExchangeXPWindowSubmit(self, cid, exchangeXP, vehCompDescr):
        yield self._CommonPage__exchangeVehicleXP(int(exchangeXP), [
            vehCompDescr])
        success = None
        self.call('exchangeWindow.response', [
            success])

    onExchangeXPWindowSubmit = process(onExchangeXPWindowSubmit)
    
    def onGatheringWindowSubmit(self, cid, exchangeXP, *args):
        vclsCompacts = list(args)
        continue
        vehTypeCompDescrs = [ getItemByCompact(x).descriptor.type.compactDescr for x in vclsCompacts ]
        yield self._CommonPage__exchangeVehicleXP(int(exchangeXP), vehTypeCompDescrs)
        success = _[1]
        self.call('gatheringWindow.response', [
            success])

    onGatheringWindowSubmit = process(onGatheringWindowSubmit)
    
    def __exchangeVehicleXP(self, exchangeXP, vehTypeCompDescrs, callback):
        yield Requester('vehicle').getFromShop()
        vcls = None
        yield StatsRequester().getEliteVehicles()
        eliteVcls = None
        yield StatsRequester().getVehicleTypeExperiences()
        xps = None
        yield StatsRequester().getFreeXPConversion()
        rate = None
        common_xp = 0
        for vehicle in vcls:
            if vehicle.descriptor.type.compactDescr in eliteVcls:
                common_xp += xps.get(vehicle.descriptor.type.compactDescr, 0)
                continue
        
        xpToExchange = min(common_xp, exchangeXP)
        goldToExchange = round(rate[1] * exchangeXP / rate[0])
        success = False
        message = makeString('#dialogs:exchangeXPConfirmation/message') % {
            'exp': BigWorld.wg_getIntegralFormat(xpToExchange),
            'gold': BigWorld.wg_getGoldFormat(goldToExchange) }
        yield async_showConfirmDialog('exchangeXPConfirmation', customMessage = message)
        isConfirmed = None
        if isConfirmed:
            Waiting.show('exchangeVehiclesXP')
            yield StatsRequester().convertVehiclesXP(exchangeXP, vehTypeCompDescrs)
            success = None
            if success:
                SystemMessages.pushI18nMessage('#system_messages:exchangeXP/success', BigWorld.wg_getIntegralFormat(exchangeXP), formatPrice((0, goldToExchange)), type = SystemMessages.SM_TYPE.FinancialTransactionWithGold)
            else:
                SystemMessages.pushI18nMessage(makeString('#system_messages:exchangeVehiclesXP/server_error') % int(exchangeXP))
            Waiting.hide('exchangeVehiclesXP')
        
        callback(success)

    _CommonPage__exchangeVehicleXP = async(process(__exchangeVehicleXP))
    
    def lockChange(self, id, lock):
        if g_currentVehicle.vehicle and id == g_currentVehicle.vehicle.inventoryId:
            g_currentVehicle.update()
        

    
    def _CommonPage__onSaveShopBuyWindowSetting(self, callbackId, value):
        AccountSettings.setSettings('shopBuyWindow', value)

    
    def __onBuyItem(self, callbackId, id, count, isShell = False, crew_type = 0, isSlot = False):
        Waiting.show('buyItem')
        item = getItemByCompact(id)
        isCrew = crew_type is not None
        if item.itemTypeName == 'vehicle':
            yield item.getPrice()
            itemPrice = None
            if itemPrice == (0, 0) and crew_type == 0 and not isSlot:
                yield StatsRequester().getFreeVehicleLeft()
                leftVehicles = None
                if leftVehicles == 0:
                    self.call('common.showMessageDialog', [
                        'freeVehicleLeftLimit',
                        False,
                        False])
                    Waiting.hide('buyItem')
                    return None
            
        
        if isCrew:
            pass
        1
        yield 'count'(count = 'isShell', isShell = 'isCrew', isCrew = 'crew_type', ¤k = 0, isSlot = isSlot)
        success = item.buy
        if item.itemTypeName == 'vehicle':
            if not g_currentVehicle.isPresent():
                g_currentVehicle.update()
            
            if self.currentInterface == 'shop':
                self._CommonPage__mainInterface.populateFilters()
            
        
        if success[0]:
            pass
        1
        success[1]('type', ¤k = SystemMessages.SM_TYPE.Error)
        self.call('shop.buyComplete', [
            success[0],
            success[1]])
        g_currentVehicle.onChanged()
        Waiting.hide('buyItem')

    _CommonPage__onBuyItem = process(__onBuyItem)
    
    def __onShopBuyWindowGetStats(self, callbackId, id):
        isOpen = AccountSettings.getSettings('shopBuyWindow')
        item = getItemByCompact(id)
        yield StatsRequester().getTankmanCost()
        upgradeParams = None
        yield StatsRequester().getEliteVehicles()
        eliteVcls = None
        tankmenCount = len(item.descriptor.type.crewRoles)
        yield item.getPrice()
        price = None
        data = [
            isOpen]
        data.append(item.name)
        data.append(item.longName)
        data.append(item.description)
        data.append(item.type)
        data.append(item.icon)
        data.append(item.nation)
        data.append(item.level)
        data.append('premium' in item.tags)
        data.append(item.descriptor.type.compactDescr in eliteVcls)
        data.append(tankmenCount)
        data.append(upgradeParams[1]['credits'] * tankmenCount)
        data.append(upgradeParams[2]['gold'] * tankmenCount)
        if price[1] == 0:
            pass
        1
        price[0](price[1])
        sPrice = [
            0,
            0]
        shells = getDefaultAmmoForGun(item.descriptor.gun)
        for i in range(0, len(shells), 2):
            (_, nationIdx, shellInnationIdx) = parseIntCompactDescr(shells[i])
            yield StatsRequester().getShellPrice(nationIdx, shells[i])
            shellPrice = data.append
            sPrice[0] += shellPrice[0] * shells[i + 1]
            sPrice[1] += shellPrice[1] * shells[i + 1]
        
        data.append(sPrice[0])
        data.append(sPrice[1])
        yield StatsRequester().getSlotsCount()
        slots = None
        yield StatsRequester().getSlotsPrices()
        slotsPrices = None
        slotPrice = BigWorld.player().shop.getNextSlotPrice(slots, slotsPrices)
        yield Requester('vehicle').getFromInventory()
        vehicles = None
        data.append(slotPrice)
        data.append(len(vehicles) >= slots)
        self.call('ShopBuyWindow.PopulateUI', data)

    _CommonPage__onShopBuyWindowGetStats = process(__onShopBuyWindowGetStats)
    
    def __processDownloadStatus(self, callback):
        StatsRequester = StatsRequester
        import gui.Scaleform.utils.requesters
        
        def waitForDossierSync(callback):
            BigWorld.player().dossierCache.waitForSync(callback)

        waitForDossierSync = async(waitForDossierSync)
        Waiting.close()
        Waiting.show('download/inventory')
        yield StatsRequester().getAccountAttrs()
        attrs = None
        Waiting.hide('download/inventory')
        Waiting.show('download/shop')
        yield StatsRequester().getSellPriceModifiers()
        Waiting.hide('download/shop')
        Waiting.show('download/dossier')
        yield waitForDossierSync()
        Waiting.hide('download/dossier')
        yield StatsRequester().getAccountDossier()
        dossier = None
        if dossier is not None:
            g_rareAchievesCache.request(dossier['rareAchievements'])
        
        Waiting.hide('download/dossier')
        isPremiumAccount = account_helpers.isPremiumAccount(attrs)
        if g_hangarSpace.inited:
            g_hangarSpace.refreshSpace(isPremiumAccount)
        else:
            g_hangarSpace.init(isPremiumAccount)
        callback(True)

    _CommonPage__processDownloadStatus = async(process(__processDownloadStatus))
    
    def processLobby(self, isInQueue = False):
        yield self._CommonPage__processDownloadStatus()
        yield self._CommonPage__populateData()
        g_cursorDelegator.activateCursor()
        yield g_currentVehicle.getFromServer()
        s = None
        self._subscribe()
        if not account_helpers.AccountPrebattle.AccountPrebattle.isTraining():
            self.movie.invoke(('loginSuccess',))
        else:
            self.movie.invoke(('loadTraining',))
        if constants.IS_SHOW_SERVER_STATS:
            self._CommonPage__requestServerStats()
        
        self.updateAccountInfo()
        self._CommonPage__battleDispatcher.start(isInQueue)
        Waiting.hide('enter')

    processLobby = process(processLobby)
    
    def processLogin(self):
        g_cursorDelegator.activateCursor()
        self._unsubscribe()
        self.commandsBinded = False
        self.movie.invoke(('loadLogin',))

    
    def processStartGameVideo(self):
        g_cursorDelegator.activateCursor()
        self.movie.invoke(('loadStartGameVideo',))

    
    def processBattleLoading(self):
        self._unsubscribe()
        self.movie.invoke(('loadBattleLoading',))

    
    def onShowWaiting(self, callbackId, message = ''):
        LOG_DEBUG('waiting open from flash "%s"' % message)
        Waiting.show('Flash')

    
    def onCloseWaiting(self, callbackId):
        LOG_DEBUG('waiting close from flash')
        Waiting.hide('Flash')

    
    def setCredits(self, credits):
        self.credits = credits
        self.call('common.creditsResponse', [
            credits])

    
    def setGold(self, gold):
        self.gold = gold
        self.call('common.goldResponse', [
            gold])

    
    def getSteamPackets(self):
        yield StatsRequester().getSteamGoldPackets()
        packets = None
        data = []
        for (key, pack) in packets.items():
            data.append(key)
            data.append(BigWorld.wg_getGoldFormat(pack['gold']))
            data.append(BigWorld.wg_getNiceNumberFormat(pack['amount']))
            data.append(pack['currency'])
        
        self.call('common.setSteamPackets', data)

    getSteamPackets = process(getSteamPackets)
    
    def setFreeXP(self, freeXP):
        self.freeXP = freeXP
        self.call('common.setFreeXP', [
            freeXP])
        self.call('common.experienceResponse', [
            freeXP])

    
    def setNations(self):
        result = []
        for name in nations.NAMES:
            result.append(name)
        
        self.call('common.nations', result)

    
    def setDenunciationsCount(self, count):
        self.call('common.denunciations', [
            count])

    
    def setAccountType(self, accountType, premiumExpiryTime = 0):
        raise DeprecationWarning, "Account type doesn't support"

    
    def setAccountsAttrs(self, attrs, premiumExpiryTime = 0):
        if not (GUI_SETTINGS.goldTransfer) and attrs & constants.ACCOUNT_ATTR.TRADING:
            attrs ^= constants.ACCOUNT_ATTR.TRADING
        
        isPremiumAccount = account_helpers.isPremiumAccount(attrs)
        if g_hangarSpace.inited:
            g_hangarSpace.refreshSpace(isPremiumAccount)
        
        if isPremiumAccount:
            if not premiumExpiryTime > 0:
                raise AssertionError
            self.call('common.setProfileType', [
                True,
                '#menu:accountTypes/premium'])
            lExpiryTime = makeLocalServerTime(premiumExpiryTime)
            delta = datetime.datetime.utcfromtimestamp(lExpiryTime) - datetime.datetime.utcnow()
            if delta.days > 0:
                if delta.seconds > 0:
                    pass
                1
                timeLeft = delta.days
                timeMetric = makeString('#menu:header/account/premium/days')
            elif delta.days == 0:
                import math as math
                timeLeft = math.ceil(delta.seconds / 3600)
                timeMetric = makeString('#menu:header/account/premium/hours')
            else:
                LOG_ERROR('timedelta with negative days', premiumExpiryTime, delta)
                return None
            (delta.days > 0).call('common.setPremiumParams', [
                timeLeft,
                timeMetric,
                makeString('#menu:common/premiumContinue'),
                delta.days > 360])
        else:
            self.call('common.setProfileType', [
                False,
                '#menu:accountTypes/base'])
        self.call('common.accountAttrs', [
            attrs])
        self.call('common.premiumResponse', [
            isPremiumAccount])
        MessengerDispatcher.g_instance.setAccountsAttrs(attrs)

    
    def setClanInfo(self, clanInfo):
        name = BigWorld.player().name
        yield StatsRequester().isTeamKiller()
        isTeamKiller = None
        yield StatsRequester().getClanDBID()
        clanDBID = None
        if clanInfo is not None and len(clanInfo) > 1:
            name = '%s [%s]' % (name, clanInfo[1])
        
        self.call('common.nameResponse', [
            name,
            isTeamKiller,
            clanInfo != None])
        MessengerDispatcher.g_instance.setClanInfo(clanInfo)
        if clanDBID is not None and clanDBID != 0:
            tID = 'clanInfo' + name
            yield dossiers_utils.getClanEmblemTextureID(clanDBID, False, tID)
            success = None
            if success:
                self.call('common.setClanEmblem', [
                    tID])
            
        

    setClanInfo = process(setClanInfo)
    
    def setExchangeRate(self, exchangeRate):
        self.call('common.exchangeRateResponse', [
            exchangeRate,
            exchangeRate])

    
    def updateAccountInfo(self):
        yield StatsRequester().getExchangeRate()
        exchangeRate = None
        self.setExchangeRate(exchangeRate)
        self.updateMoneyStats()
        self.updateXPInfo()
        self.updateClanInfo()
        self.updateAccountAttrs()
        self.setServerInfo()

    updateAccountInfo = process(updateAccountInfo)
    
    def updateMoneyStats(self):
        yield StatsRequester().getCredits()
        credits = None
        self.setCredits(credits)
        yield StatsRequester().getGold()
        gold = None
        self.setGold(gold)

    updateMoneyStats = process(updateMoneyStats)
    
    def updateAccountType(self):
        raise DeprecationWarning, "Account type doesn't support"

    
    def updateAccountAttrs(self):
        yield StatsRequester().getAccountAttrs()
        accAttrs = None
        yield StatsRequester().getDenunciations()
        denunciations = None
        isPremium = account_helpers.isPremiumAccount(accAttrs)
        premiumExpiryTime = 0
        if isPremium:
            yield StatsRequester().getPremiumExpiryTime()
            premiumExpiryTime = None
        
        self.setAccountsAttrs(accAttrs, premiumExpiryTime = premiumExpiryTime)
        self.setDenunciationsCount(denunciations)
        self.setNations()

    updateAccountAttrs = process(updateAccountAttrs)
    
    def updateClanInfo(self):
        yield StatsRequester().getClanInfo()
        clanInfo = None
        self.setClanInfo(clanInfo)

    updateClanInfo = process(updateClanInfo)
    
    def updateXPInfo(self):
        yield StatsRequester().getFreeExperience()
        freeXP = None
        self.setFreeXP(freeXP)

    updateXPInfo = process(updateXPInfo)
    
    def _updateFightButton(self):
        if self._CommonPage__battleDispatcher is not None:
            self._CommonPage__battleDispatcher.updateFightButton()
        

    
    def _CommonPage__requestServerStats(self):
        self.statsCallbackId = None
        if hasattr(BigWorld.player(), 'requestServerStats'):
            BigWorld.player().requestServerStats()
        

    
    def onStatsReceived(self, stats):
        if constants.IS_SHOW_SERVER_STATS:
            self.movie.setServerStats(dict(stats))
            self.statsCallbackId = BigWorld.callback(5, self._CommonPage__requestServerStats)
        

    
    def setServerInfo(self):
        connectionManager = connectionManager
        import ConnectionManager
        if connectionManager.serverUserName:
            tooltipBody = makeString('#tooltips:header/info/players_online_full/body')
            tooltipFullData = makeTooltip('#tooltips:header/info/players_online_full/header', tooltipBody % {
                'servername': connectionManager.serverUserName })
            self.call('common.setServerInfo', [
                connectionManager.serverUserName,
                tooltipFullData])
        

    
    def onUpdateStage(self):
        self.call('Stage.Update', list(GUI.screenResolution()))

    
    def getPremiumCost(self, callbackId):
        yield StatsRequester().getPremiumCost()
        premiumCost = None
        premiumCost = sorted(premiumCost.items(), reverse = True)
        args = []
        for (period, cost) in premiumCost:
            args.append({
                'days': period,
                'price': cost,
                'discountPrice': cost })
        
        pw = self.getMember('windowLayout.premiumWndClip.form.premiumForm')
        if pw:
            pw.setCosts(args)
        else:
            LOG_ERROR('No premium window in flash!')

    getPremiumCost = process(getPremiumCost)
    
    def buyPremium(self, callbackId, days, price):
        yield StatsRequester().getAccountAttrs()
        attrs = None
        if account_helpers.isPremiumAccount(attrs):
            dialogTitle = 'premiumContinueConfirmation'
        else:
            dialogTitle = 'premiumBuyConfirmation'
        message = makeString('#dialogs:%s/message' % dialogTitle, days, BigWorld.wg_getGoldFormat(price))
        yield async_showConfirmDialog(dialogTitle, customMessage = message)
        isConfirmed = None
        if isConfirmed and days:
            self._CommonPage__upgradeToPremium(days)
            self.call('profile.PremiumBuyApprove')
        else:
            self.call('profile.PremiumBuyDecline')

    buyPremium = process(buyPremium)
    
    def __upgradeToPremium(self, days):
        Waiting.show('loadStats')
        yield StatsRequester().getAccountAttrs()
        attrs = None
        isPremium = account_helpers.isPremiumAccount(attrs)
        yield StatsRequester().upgradeToPremium(days)
        success = None
        if success:
            yield StatsRequester().getPremiumCost()
            premiumCost = None
            if premiumCost:
                if isPremium:
                    successMessage = '#system_messages:premium/continueSuccess'
                else:
                    successMessage = '#system_messages:premium/buyingSuccess'
                SystemMessages.g_instance.pushI18nMessage(successMessage, days, formatPrice((0, premiumCost[int(days)])), type = SystemMessages.SM_TYPE.PurchaseForGold)
            
            self._updateFightButton()
        else:
            SystemMessages.g_instance.pushI18nMessage('#system_messages:premium/server_error', days, type = SystemMessages.SM_TYPE.Error)
        Waiting.hide('loadStats')

    _CommonPage__upgradeToPremium = process(__upgradeToPremium)
    
    def __changeCurrentVehicle(self, *args):
        yield StatsRequester().getFreeExperience()
        freeExperience = None
        unspentXP = None
        isElite = False
        isXPToTman = False
        self._updateFightButton()
        if g_currentVehicle.isPresent():
            yield StatsRequester().getVehicleTypeExperiences()
            experiences = None
            unspentXP = experiences.get(g_currentVehicle.vehicle.descriptor.type.compactDescr, 0)
            yield g_currentVehicle.vehicle.isElite()
            isElite = None
            if isElite:
                pass
            isXPToTman = g_currentVehicle.vehicle.isXPToTman
            self.call('common.vehicleChangeResponse', [
                g_currentVehicle.vehicle.inventoryId])
            self.call('hangar.setVehicleExperience', [
                unspentXP,
                freeExperience,
                isElite,
                isXPToTman])
        

    _CommonPage__changeCurrentVehicle = process(__changeCurrentVehicle)
    
    def updateTankParams(self):
        yield StatsRequester().getFreeExperience()
        freeExperience = None
        if g_currentVehicle.isPresent():
            self.call('common.tankNameResponse', [
                g_currentVehicle.vehicle.name])
            for tag in vehicles.VEHICLE_CLASS_TAGS.intersection(g_currentVehicle.vehicle.tags):
                tankType = tag
            
            self.call('common.tankTypeResponse', [
                tankType])
            yield g_currentVehicle.vehicle.isElite()
            elite = None
            self.call('common.tankEliteResponse', [
                elite])
        else:
            self.call('common.tankNameResponse', [
                ''])
            self.call('common.tankTypeResponse', [
                ''])
            self.call('common.tankEliteResponse', [
                False])

    updateTankParams = process(updateTankParams)
    

