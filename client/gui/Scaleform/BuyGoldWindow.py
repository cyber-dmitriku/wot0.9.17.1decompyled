# Source Generated with Decompyle++
# File: BuyGoldWindow.pyc (Python 2.6)

__author__ = 'i_maliavko'
import BigWorld
import constants
import time
from helpers import i18n
from windows import UIInterface
from adisp import process, async
from debug_utils import *
from gui.Scaleform.utils.requesters import StatsRequester
from gui.Scaleform.Waiting import Waiting
from gui import SystemMessages
from helpers.links import openPaymentWebsite

class BuyGoldWindow(UIInterface):
    FLASH_SHOW_WND = 'common.showExchangeVcoinWnd'
    FLASH_SEND_DATA = 'common.exchangeVCoinData'
    FLASH_CLOSE_WND = 'common.exchangeVCoinClose'
    CACHE_ENABLED = False
    VCOIN_COUNT_STEP = 10
    
    def __init__(self):
        UIInterface.__init__(self)
        self._BuyGoldWindow__balanceCooldown = time.time()
        self._BuyGoldWindow__balanceCallback = None
        self._BuyGoldWindow__buyCooldown = time.time()
        self._BuyGoldWindow__buyCallback = None
        self._BuyGoldWindow__syncCallbacks = []
        self._BuyGoldWindow__visible = False
        self.isCached = False
        self.isWaitForSync = False
        self.balance = 0
        self.exchangeRate = 0
        self.error = ''
        self.minTransactVal = 50
        self.maxTransactVal = 500000

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self.uiHolder.addExternalCallbacks({
            'common.ExchangeVcoin': self.onBuyGold,
            'common.ExchangeVcoinClosed': self.onWindowClosed,
            'common.showPaymentWebSite': self.onShowWebSite })

    
    def dispossessUI(self):
        if self.uiHolder is not None:
            self.uiHolder.removeExternalCallbacks('common.ExchangeVcoin', 'common.ExchangeVcoinClosed', 'common.showPaymentWebSite')
        
        UIInterface.dispossessUI(self)

    
    def isBalanceCooldowned(self):
        return self._BuyGoldWindow__balanceCooldown >= time.time()

    
    def isBuyingCooldowned(self):
        return self._BuyGoldWindow__buyCooldown >= time.time()

    
    def _BuyGoldWindow__updateBalanceCooldown(self):
        self._BuyGoldWindow__balanceCooldown = time.time() + constants.REQUEST_COOLDOWN.EBANK_GET_BALANCE

    
    def _BuyGoldWindow__updateBuyingCooldown(self):
        self._BuyGoldWindow__buyCooldown = time.time() + constants.REQUEST_COOLDOWN.EBANK_BUY_GOLD

    
    def _BuyGoldWindow__cancelBalanceCallback(self):
        if self._BuyGoldWindow__balanceCallback is not None:
            BigWorld.cancelCallback(self._BuyGoldWindow__balanceCallback)
            self._BuyGoldWindow__balanceCallback = None
        

    
    def _BuyGoldWindow__cancelBuyCallback(self):
        if self._BuyGoldWindow__buyCallback is not None:
            BigWorld.cancelCallback(self._BuyGoldWindow__buyCallback)
            self._BuyGoldWindow__buyCallback = None
        

    
    def visible(self):
        return self._BuyGoldWindow__visible

    visible = property(visible)
    
    def onShowWebSite(self, cid):
        openPaymentWebsite()

    
    def __buyGold(self, vcoin):
        self._BuyGoldWindow__buyCallback = None
        yield StatsRequester().ebankBuyGold(vcoin)
        (success, errStr) = None
        if success:
            self._BuyGoldWindow__showSuccessSysMsg(vcoin * self.exchangeRate, vcoin)
            self._BuyGoldWindow__updateBuyingCooldown()
            self.close()
            return None
        self._BuyGoldWindow__showErrorSysMsg(errStr)
        self._BuyGoldWindow__sendData()

    _BuyGoldWindow__buyGold = process(__buyGold)
    
    def onBuyGold(self, cid, vcoin):
        self._BuyGoldWindow__buyCallback = None((BigWorld.callback, max(self._BuyGoldWindow__buyCooldown - time.time(), 0)), (lambda : self._BuyGoldWindow__buyGold(int(vcoin))))

    
    def onWindowClosed(self, cid):
        self._BuyGoldWindow__close()

    
    def _BuyGoldWindow__show(self):
        self.call(BuyGoldWindow.FLASH_SHOW_WND, [])
        self._BuyGoldWindow__visible = True
        
        def syncData():
            self._BuyGoldWindow__balanceCallback = None
            yield self._BuyGoldWindow__syncEBankData()
            if len(self.error) and self.visible:
                self.close()
                LOG_ERROR('Server error while getting EBank data: %s' % self.error)
                self._BuyGoldWindow__showErrorSysMsg(self.error)
                return None
            self._BuyGoldWindow__sendData()

        syncData = (process,)(syncData)
        self._BuyGoldWindow__balanceCallback = BigWorld.callback((max(self._BuyGoldWindow__balanceCooldown - time.time(), 0),), (lambda : syncData()))

    
    def show(self):
        PlayerAccount = PlayerAccount
        import Account
        if self._BuyGoldWindow__visible or not isinstance(BigWorld.player(), PlayerAccount):
            return None
        self._BuyGoldWindow__show()

    
    def close(self):
        self.call(BuyGoldWindow.FLASH_CLOSE_WND, [])
        self._BuyGoldWindow__close()

    
    def _BuyGoldWindow__close(self):
        self._BuyGoldWindow__visible = False
        self._BuyGoldWindow__cancelBalanceCallback()
        self._BuyGoldWindow__cancelBuyCallback()

    
    def _BuyGoldWindow__sendData(self):
        self.call(BuyGoldWindow.FLASH_SEND_DATA, [
            self.balance,
            self.exchangeRate,
            self.exchangeRate,
            self.minTransactVal,
            self.maxTransactVal,
            BuyGoldWindow.VCOIN_COUNT_STEP])

    
    def clearCache(self):
        self.isCached = False

    
    def __syncEBankData(self, callback):
        yield StatsRequester().ebankGetExchangeRate()
        self.exchangeRate = None
        yield StatsRequester().ebankGetMinTransactionValue()
        self.minTransactVal = None
        yield StatsRequester().ebankGetMaxTransactionValue()
        self.maxTransactVal = None
        if self.isCached:
            callback(False)
            return None
        self._BuyGoldWindow__syncCallbacks.append(callback)
        if self.isWaitForSync:
            return None
        self.isCached = False
        self.isWaitForSync = True
        yield StatsRequester().ebankGetBalance()
        (self.balance, self.error) = self.isWaitForSync
        self._BuyGoldWindow__updateBalanceCooldown()
        if BuyGoldWindow.CACHE_ENABLED:
            pass
        self.isCached = not len(self.error)
        self.isWaitForSync = False
        for c in self._BuyGoldWindow__syncCallbacks:
            c(True)
        
        self._BuyGoldWindow__syncCallbacks = []

    _BuyGoldWindow__syncEBankData = async(process(__syncEBankData))
    
    def _BuyGoldWindow__showSuccessSysMsg(self, gold, vcoin):
        SystemMessages.g_instance.pushMessage(i18n.makeString('#system_messages:ebank/response/success') % {
            'gold': BigWorld.wg_getGoldFormat(gold),
            'vcoin': BigWorld.wg_getIntegralFormat(vcoin) }, type = SystemMessages.SM_TYPE.FinancialTransactionWithGold)

    
    def _BuyGoldWindow__showErrorSysMsg(self, msg):
        SystemMessages.g_instance.pushMessage(i18n.makeString('#system_messages:ebank/response/%s' % str(msg)), type = SystemMessages.SM_TYPE.Error)



