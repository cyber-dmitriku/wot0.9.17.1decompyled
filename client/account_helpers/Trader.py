# Source Generated with Decompyle++
# File: Trader.pyc (Python 2.6)

import AccountCommands
import offers
from functools import partial
from debug_utils import *

class Trader(object):
    
    def __init__(self, syncData):
        self._Trader__account = None
        self._Trader__syncData = syncData
        self._Trader__offersData = {
            'out': { },
            'in': { } }
        self._Trader__outOffers = offers.OutOffers(self._Trader__offersData)
        self._Trader__inOffers = offers.InOffers(self._Trader__offersData)

    
    def onAccountBecomePlayer(self):
        self._Trader__ignore = False

    
    def onAccountBecomeNonPlayer(self):
        self._Trader__ignore = True

    
    def setAccount(self, account):
        self._Trader__account = account

    
    def synchronize(self, isFullSync, diff):
        if isFullSync:
            self._Trader__offersData['out'].clear()
            self._Trader__offersData['in'].clear()
        
        offersDiff = diff.get('offers', None)
        if offersDiff is None:
            return None
        for kind in ('in', 'out'):
            subdiff = offersDiff.get(kind)
            if subdiff is None:
                continue
            
            data = self._Trader__offersData[kind]
            for (offerID, offerData) in subdiff.iteritems():
                if offerData is None:
                    data.pop(offerID, None)
                    continue
                offersDiff is None
                data[offerID] = offerData
            
        

    
    def getOffers(self, callback = None):
        if self._Trader__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, None, None)
            
            return None
        self._Trader__syncData.waitForSync(partial(self._Trader__onGetResponse, callback))

    
    def makeOffer_sellGold(self, passwd, dstClassName, dstDBID, validSec, outGold, inCredits, callback = None):
        if self._Trader__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr: callback(resultID, errorStr)
        else:
            proxy = None
        flags = offers.makeOfferFlags(offers.OFFER_SELL, offers.SRC_WARE_GOLD, offers.DST_WARE_CREDITS, offers.ENTITY_TYPE_IDS_BY_NAMES['Account'], offers.ENTITY_TYPE_IDS_BY_NAMES[dstClassName])
        self._Trader__account._makeTradeOffer(passwd, flags, dstDBID, validSec, inCredits, outGold, 0, proxy)

    
    def revokeOffer(self, outOfferID, callback = None):
        if self._Trader__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errString, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Trader__account._doCmdInt3(AccountCommands.CMD_REVOKE_TRADE_OFFER, outOfferID, 0, 0, proxy)

    
    def acceptOffer(self, passwd, inOfferID, callback = None):
        if self._Trader__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errString, ext = ({ },): callback(resultID, errString)
        else:
            proxy = None
        self._Trader__account._doCmdInt2Str(AccountCommands.CMD_ACCEPT_TRADE_OFFER, inOfferID, 0, passwd, proxy)

    
    def declineOffer(self, inOfferID, callback = None):
        if self._Trader__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        if callback is not None:
            
            proxy = lambda requestID, resultID, errString, ext = ({ },): callback(resultID)
        else:
            proxy = None
        self._Trader__account._doCmdInt3(AccountCommands.CMD_DECLINE_TRADE_OFFER, inOfferID, 0, 0, proxy)

    
    def _Trader__onGetResponse(self, callback, resultID):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None, None)
            
            return None
        if callback is not None:
            callback(resultID, self._Trader__inOffers, self._Trader__outOffers)
        



