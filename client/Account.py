# Source Generated with Decompyle++
# File: Account.pyc (Python 2.6)

import BigWorld
import Keys
import cPickle
import zlib
import Event
import items
import copy
import nations
import AccountSyncData
import AccountCommands
import ArenaType
import ClientPrebattle
import constants
import Settings
import helpers.i18n as helpers
from account_helpers import Inventory, DossierCache, Shop, Stats, Trader, CustomFilesCache, BattleResultsCache
from itertools import izip
from ConnectionManager import connectionManager
from PlayerEvents import g_playerEvents as events
from constants import *
from streamIDs import CHAT_INITIALIZATION_ID, RangeStreamIDCallbacks, STREAM_ID_CHAT_MAX, STREAM_ID_CHAT_MIN
from debug_utils import *
from ContactInfo import ContactInfo
from ClientChat import ClientChat
from ChatManager import chatManager
from OfflineMapCreator import g_offlineMapCreator
from gui.Scaleform import VoiceChatInterface
from adisp import process
from wotdecorators import noexcept

class PlayerAccount(BigWorld.Entity, ClientChat):
    _PlayerAccount__onStreamCompletePredef = {
        AccountCommands.REQUEST_ID_PREBATTLES: 'receivePrebattles',
        AccountCommands.REQUEST_ID_PREBATTLE_ROSTER: 'receivePrebattleRoster' }
    
    def version_ru8001(self):
        pass

    
    def __init__(self):
        global g_accountRepository
        ClientChat.__init__(self)
        self._PlayerAccount__rangeStreamIDCallbacks = RangeStreamIDCallbacks()
        self._PlayerAccount__rangeStreamIDCallbacks.addRangeCallback((STREAM_ID_CHAT_MIN, STREAM_ID_CHAT_MAX), '_ClientChat__receiveStreamedData')
        if g_offlineMapCreator.Active():
            self.name = 'offline_account'
        
        if g_accountRepository is None:
            g_accountRepository = _AccountRepository(self.name, copy.copy(self.serverSettings['file_server']))
        
        self.contactInfo = g_accountRepository.contactInfo
        self.syncData = g_accountRepository.syncData
        self.inventory = g_accountRepository.inventory
        self.stats = g_accountRepository.stats
        self.trader = g_accountRepository.trader
        self.shop = g_accountRepository.shop
        self.dossierCache = g_accountRepository.dossierCache
        self.battleResultsCache = g_accountRepository.battleResultsCache
        self.customFilesCache = g_accountRepository.customFilesCache
        self.syncData.setAccount(self)
        self.inventory.setAccount(self)
        self.stats.setAccount(self)
        self.trader.setAccount(self)
        self.shop.setAccount(self)
        self.dossierCache.setAccount(self)
        self.battleResultsCache.setAccount(self)
        self.isLongDisconnectedFromCenter = False
        self.prebattle = None
        self.prebattleAutoInvites = g_accountRepository.prebattleAutoInvites
        self.prebattleInvites = g_accountRepository.prebattleInvites
        self.eventNotifications = g_accountRepository.eventNotifications
        self.clanMembers = g_accountRepository.clanMembers
        self.isInQueue = False
        self._PlayerAccount__onCmdResponse = { }
        self._PlayerAccount__onStreamComplete = { }

    
    def onBecomePlayer(self):
        LOG_DEBUG('Account.onBecomePlayer()')
        self.isPlayer = True
        self.databaseID = None
        self.inputHandler = AccountInputHandler()
        BigWorld.resetEntityManager(True, False)
        BigWorld.clearAllSpaces()
        self.syncData.onAccountBecomePlayer()
        self.inventory.onAccountBecomePlayer()
        self.stats.onAccountBecomePlayer()
        self.trader.onAccountBecomePlayer()
        self.shop.onAccountBecomePlayer()
        self.dossierCache.onAccountBecomePlayer()
        self.battleResultsCache.onAccountBecomePlayer()
        chatManager.switchPlayerProxy(self)
        events.onAccountBecomePlayer()
        yield VoiceChatInterface.g_instance.initialize(self.serverSettings['voipDomain'])
        yield VoiceChatInterface.g_instance.requestCaptureDevices()

    onBecomePlayer = process(onBecomePlayer)
    
    def onBecomeNonPlayer(self):
        LOG_DEBUG('Account.onBecomeNonPlayer()')
        if not hasattr(self, 'isPlayer') and self.isPlayer:
            return None
        self.isPlayer = False
        chatManager.switchPlayerProxy(None)
        self.syncData.onAccountBecomeNonPlayer()
        self.inventory.onAccountBecomeNonPlayer()
        self.stats.onAccountBecomeNonPlayer()
        self.trader.onAccountBecomeNonPlayer()
        self.shop.onAccountBecomeNonPlayer()
        self.dossierCache.onAccountBecomeNonPlayer()
        self.battleResultsCache.onAccountBecomeNonPlayer()
        self._PlayerAccount__cancelCommands()
        self.syncData.setAccount(None)
        self.inventory.setAccount(None)
        self.stats.setAccount(None)
        self.trader.setAccount(None)
        self.shop.setAccount(None)
        self.dossierCache.setAccount(None)
        self.battleResultsCache.setAccount(None)
        events.onAccountBecomeNonPlayer()
        del self.inputHandler

    
    def onCmdResponse(self, requestID, resultID, errorStr):
        callback = self._PlayerAccount__onCmdResponse.pop(requestID, None)
        if callback is not None:
            callback(requestID, resultID, errorStr)
        

    
    def onCmdResponseExt(self, requestID, resultID, errorStr, ext):
        ext = cPickle.loads(ext)
        if resultID == AccountCommands.RES_SHOP_DESYNC:
            self.shop.synchronize(ext.get('shopRev', None))
        
        callback = self._PlayerAccount__onCmdResponse.pop(requestID, None)
        if callback is not None:
            callback(requestID, resultID, errorStr, ext)
        

    
    def reloadShop(self):
        self.shop.synchronize(None)

    
    def onKickedFromServer(self, reason, isBan, expiryTime):
        LOG_MX('onKickedFromServer', reason, isBan, expiryTime)
        Disconnect = Disconnect
        import gui.Scaleform.Disconnect
        Disconnect.showKick(reason, isBan, expiryTime)

    
    def onStreamComplete(self, id, data):
        callback = self._PlayerAccount__rangeStreamIDCallbacks.getCallbackForStreamID(id)
        if callback is not None:
            getattr(self, callback)(id, data)
            return None
        callback = self._PlayerAccount__onStreamCompletePredef.get(id, None)
        if callback is not None:
            getattr(self, callback)(True, data)
            return None
        callback = self._PlayerAccount__onStreamComplete.pop(id, None)
        if callback is not None:
            callback(True, data)
        

    
    def onEnqueued(self):
        LOG_DEBUG('onEnqueued')
        self.isInQueue = True
        events.onEnqueued()

    
    def onEnqueueFailure(self, errorCode, errorStr):
        LOG_DEBUG('onEnqueueFailure', errorCode, errorStr)
        events.onEnqueueFailure(errorCode, errorStr)

    
    def onDequeued(self):
        LOG_DEBUG('onDequeued')
        self.isInQueue = False
        events.onDequeued()

    
    def onArenaCreated(self):
        LOG_DEBUG('onArenaCreated')
        self.prebattle = None
        events.isPlayerEntityChanging = True
        events.onArenaCreated()
        events.onPlayerEntityChanging()

    
    def onArenaJoinFailure(self, errorCode, errorStr):
        LOG_DEBUG('onArenaJoinFailure', errorCode, errorStr)
        events.isPlayerEntityChanging = False
        events.onPlayerEntityChangeCanceled()
        events.onArenaJoinFailure(errorCode, errorStr)

    
    def onPrebattleJoined(self, prebattleID):
        self.prebattle = ClientPrebattle.ClientPrebattle(prebattleID)
        events.onPrebattleJoined()

    
    def onPrebattleJoinFailure(self, errorCode):
        LOG_MX('onPrebattleJoinFailure', errorCode)
        events.onPrebattleJoinFailure(errorCode)

    
    def onPrebattleLeft(self):
        LOG_MX('onPrebattleLeft')
        self.prebattle = None
        events.onPrebattleLeft()

    
    def onKickedFromQueue(self):
        LOG_DEBUG('onKickedFromQueue')
        self.isInQueue = False
        events.onKickedFromQueue()

    
    def onKickedFromArena(self, reasonCode):
        LOG_DEBUG('onKickedFromArena', reasonCode)
        events.isPlayerEntityChanging = False
        events.onPlayerEntityChangeCanceled()
        events.onKickedFromArena(reasonCode)

    
    def onKickedFromPrebattle(self, reasonCode):
        LOG_DEBUG('onKickedFromPrebattle', reasonCode)
        self.prebattle = None
        events.onKickedFromPrebattle(reasonCode)

    
    def onCenterIsLongDisconnected(self, isLongDisconnected):
        LOG_DEBUG('onCenterIsLongDisconnected', isLongDisconnected)
        self.isLongDisconnectedFromCenter = isLongDisconnected
        events.onCenterIsLongDisconnected(isLongDisconnected)

    
    def handleKeyEvent(self, event):
        return False

    
    def showGUI(self, ctx):
        ctx = cPickle.loads(ctx)
        LOG_MX('showGUI', ctx)
        self.databaseID = ctx['databaseID']
        if 'prebattleID' in ctx:
            self.prebattle = ClientPrebattle.ClientPrebattle(ctx['prebattleID'])
        
        if 'queueID' in ctx:
            self.isInQueue = True
        
        if 'serverUTC' in ctx:
            import helpers.time_utils as tm
            tm.setTimeCorrection(ctx['serverUTC'])
        
        if 'isLongDisconnectedFromCenter' in ctx:
            isLongDisconnectedFromCenter = ctx['isLongDisconnectedFromCenter']
            if self.isLongDisconnectedFromCenter != isLongDisconnectedFromCenter:
                self.isLongDisconnectedFromCenter = isLongDisconnectedFromCenter
                events.onCenterIsLongDisconnected(isLongDisconnectedFromCenter)
            
        
        events.isPlayerEntityChanging = False
        events.onAccountShowGUI(ctx)
        BigWorld.Screener.setUserId(self.databaseID)

    
    def receiveQueueInfo(self, randomsQueueInfo, companiesQueueInfo):
        events.onQueueInfoReceived(randomsQueueInfo, companiesQueueInfo)

    
    def receivePrebattles(self, isSuccess, data):
        if isSuccess:
            
            try:
                data = zlib.decompress(data)
                (type, count, prebattles) = cPickle.loads(data)
            LOG_CURRENT_EXCEPTION()
            isSuccess = False

        
        if not isSuccess:
            type = 0
            count = 0
            prebattles = []
        
        events.onPrebattlesListReceived(type, count, prebattles)

    
    def receivePrebattleRoster(self, isSuccess, data):
        if isSuccess:
            
            try:
                data = zlib.decompress(data)
                (prebattleID, rosterAsList) = cPickle.loads(data)
            LOG_CURRENT_EXCEPTION()
            isSuccess = False

        
        if not isSuccess:
            prebattleID = 0
            rosterAsList = []
        
        events.onPrebattleRosterReceived(prebattleID, rosterAsList)

    
    def receiveActiveArenas(self, arenas):
        events.onArenaListReceived(arenas)

    
    def receiveServerStats(self, stats):
        events.onServerStatsReceived(stats)

    
    def updatePrebattle(self, updateType, argStr):
        if self.prebattle is not None:
            self.prebattle.update(updateType, argStr)
        

    
    def update(self, diff):
        self._update(True, cPickle.loads(diff))

    
    def resyncDossiers(self):
        self.dossierCache.resynchronize()

    
    def requestQueueInfo(self, queueType):
        if not events.isPlayerEntityChanging:
            self.base.doCmdInt3(AccountCommands.REQUEST_ID_NO_RESPONSE, AccountCommands.CMD_REQ_QUEUE_INFO, queueType, 0, 0)
        

    
    def requestPrebattles(self, type, sort_key, idle, start, end):
        if not events.isPlayerEntityChanging:
            self.base.doCmdIntArr(AccountCommands.REQUEST_ID_PREBATTLES, AccountCommands.CMD_REQ_PREBATTLES, [
                type,
                sort_key,
                int(idle),
                start,
                end])
        

    
    def requestPrebattlesByName(self, type, idle, creatorMask):
        if not events.isPlayerEntityChanging:
            self.base.doCmdInt2Str(AccountCommands.REQUEST_ID_PREBATTLES, AccountCommands.CMD_REQ_PREBATTLES_BY_CREATOR, type, int(idle), creatorMask)
        

    
    def requestPrebattlesByDivision(self, idle, division):
        if not events.isPlayerEntityChanging:
            self.base.doCmdInt3(AccountCommands.REQUEST_ID_PREBATTLES, AccountCommands.CMD_REQ_PREBATTLES_BY_DIVISION, int(idle), division, 0)
        

    
    def requestPrebattleRoster(self, prebattleID):
        if not events.isPlayerEntityChanging:
            self.base.doCmdInt3(AccountCommands.REQUEST_ID_PREBATTLE_ROSTER, AccountCommands.CMD_REQ_PREBATTLE_ROSTER, prebattleID, 0, 0)
        

    
    def requestServerStats(self):
        if not events.isPlayerEntityChanging:
            self.base.doCmdInt3(AccountCommands.REQUEST_ID_NO_RESPONSE, AccountCommands.CMD_REQ_SERVER_STATS, 0, 0, 0)
        

    
    def requestPlayerInfo(self, name, callback):
        if events.isPlayerEntityChanging:
            return None
        
        proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID, ext.get('dossier', ''), ext.get('clanDBID', 0), ext.get('clanInfo', None))
        self._doCmdStr(AccountCommands.CMD_REQ_PLAYER_INFO, name, proxy)

    
    def requestAccountDossier(self, name, callback):
        if events.isPlayerEntityChanging:
            return None
        
        proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID, ext.get('dossier', ''))
        self._doCmdStr(AccountCommands.CMD_REQ_ACCOUNT_DOSSIER, name, proxy)

    
    def requestVehicleDossier(self, name, vehTypeCompDescr, callback):
        if events.isPlayerEntityChanging:
            return None
        
        proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID, ext.get('dossier', ''))
        self._doCmdInt2Str(AccountCommands.CMD_REQ_VEHICLE_DOSSIER, vehTypeCompDescr, 0, name, proxy)

    
    def requestPlayerClanInfo(self, name, callback):
        if events.isPlayerEntityChanging:
            return None
        
        proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID, errorStr, ext.get('clanDBID', 0), ext.get('clanInfo', None))
        self._doCmdInt2Str(AccountCommands.CMD_REQ_PLAYER_CLAN_INFO, 0, 0, name, proxy)

    
    def enqueueForArena(self, vehInvID, gameplaysMask = 65535, arenaTypeID = 0):
        if events.isPlayerEntityChanging:
            return None
        self.base.doCmdInt3(AccountCommands.REQUEST_ID_NO_RESPONSE, AccountCommands.CMD_ENQUEUE_FOR_ARENA, vehInvID, gameplaysMask, arenaTypeID)

    
    def dequeue(self):
        if not events.isPlayerEntityChanging:
            self.base.doCmdInt3(AccountCommands.REQUEST_ID_NO_RESPONSE, AccountCommands.CMD_DEQUEUE, 0, 0, 0)
        

    
    def createArenaFromQueue(self):
        if not events.isPlayerEntityChanging:
            self.base.doCmdInt3(AccountCommands.REQUEST_ID_NO_RESPONSE, AccountCommands.CMD_FORCE_QUEUE, 0, 0, 0)
        

    
    def prb_createTraining(self, arenaTypeID, roundLength, isOpened, comment):
        if events.isPlayerEntityChanging:
            return None
        self.base.createTraining(arenaTypeID, roundLength, isOpened, comment)

    
    def prb_createSquad(self):
        if events.isPlayerEntityChanging:
            return None
        self.base.createSquad()

    
    def prb_createCompany(self, isOpened, comment, division = PREBATTLE_COMPANY_DIVISION.ABSOLUTE):
        if events.isPlayerEntityChanging:
            return None
        self.base.createCompany(isOpened, comment, division)

    
    def prb_createDev(self, arenaTypeID, roundLength, comment, bonusType = ARENA_BONUS_TYPE.REGULAR):
        if events.isPlayerEntityChanging:
            return None
        self.base.createDevPrebattle(bonusType, arenaTypeID, roundLength, comment)

    
    def prb_sendInvites(self, accountsToInvite, comment):
        if events.isPlayerEntityChanging:
            return None
        self.base.sendPrebattleInvites(accountsToInvite, comment)

    
    def prb_acceptInvite(self, prebattleID, peripheryID):
        if events.isPlayerEntityChanging:
            return None
        self.base.doCmdInt3(AccountCommands.REQUEST_ID_NO_RESPONSE, AccountCommands.CMD_PRB_ACCEPT_INVITE, prebattleID, peripheryID, 0)

    
    def prb_declineInvite(self, prebattleID, peripheryID):
        if events.isPlayerEntityChanging:
            return None
        self.base.doCmdInt3(AccountCommands.REQUEST_ID_NO_RESPONSE, AccountCommands.CMD_PRB_DECLINE_INVITE, prebattleID, peripheryID, 0)

    
    def prb_join(self, prebattleID):
        if events.isPlayerEntityChanging:
            return None
        self.base.doCmdInt3(AccountCommands.REQUEST_ID_NO_RESPONSE, AccountCommands.CMD_PRB_JOIN, prebattleID, 0, 0)

    
    def prb_leave(self, callback):
        if events.isPlayerEntityChanging:
            return None
        self._doCmdInt3(AccountCommands.CMD_PRB_LEAVE, 0, 0, (0,), (lambda requestID, resultID, errorStr: callback(resultID)))

    
    def prb_ready(self, vehInvID, callback):
        if events.isPlayerEntityChanging:
            return None
        self._doCmdInt3(AccountCommands.CMD_PRB_READY, vehInvID, 0, (0,), (lambda requestID, resultID, errorStr: callback(resultID)))

    
    def prb_notReady(self, state, callback):
        if events.isPlayerEntityChanging:
            return None
        self._doCmdInt3(AccountCommands.CMD_PRB_NOT_READY, state, 0, (0,), (lambda requestID, resultID, errorStr: callback(resultID)))

    
    def prb_assign(self, playerID, roster, callback):
        if events.isPlayerEntityChanging:
            return None
        self._doCmdInt3(AccountCommands.CMD_PRB_ASSIGN, playerID, roster, (0,), (lambda requestID, resultID, errorStr: callback(resultID)))

    
    def prb_swapTeams(self, callback):
        if events.isPlayerEntityChanging:
            return None
        self._doCmdInt3(AccountCommands.CMD_PRB_SWAP_TEAM, 0, 0, (0,), (lambda requestID, resultID, errorStr: callback(resultID)))

    
    def prb_changeArena(self, arenaTypeID, callback):
        if events.isPlayerEntityChanging:
            return None
        self._doCmdInt3(AccountCommands.CMD_PRB_CH_ARENA, arenaTypeID, 0, (0,), (lambda requestID, resultID, errorStr: callback(resultID)))

    
    def prb_changeRoundLength(self, roundLength, callback):
        if events.isPlayerEntityChanging:
            return None
        self._doCmdInt3(AccountCommands.CMD_PRB_CH_ROUND, roundLength, 0, (0,), (lambda requestID, resultID, errorStr: callback(resultID)))

    
    def prb_changeOpenStatus(self, isOpened, callback):
        if events.isPlayerEntityChanging:
            return None
        if isOpened:
            pass
        1
        AccountCommands.CMD_PRB_OPEN(1, 0, 0, (0,), (lambda requestID, resultID, errorStr: callback(resultID)))

    
    def prb_changeComment(self, comment, callback):
        if events.isPlayerEntityChanging:
            return None
        self._doCmdStr(AccountCommands.CMD_PRB_CH_COMMENT, (comment,), (lambda requestID, resultID, errorStr: callback(resultID)))

    
    def prb_changeArenaVoip(self, arenaVoipChannels, callback):
        if events.isPlayerEntityChanging:
            return None
        self._doCmdInt3(AccountCommands.CMD_PRB_CH_ARENAVOIP, arenaVoipChannels, 0, (0,), (lambda requestID, resultID, errorStr: callback(resultID)))

    
    def prb_teamReady(self, team, force, callback):
        if events.isPlayerEntityChanging:
            return None
        if force:
            pass
        1
        AccountCommands.CMD_PRB_TEAM_READY(team, 1, 0, (0,), (lambda requestID, resultID, errorStr: callback(resultID)))

    
    def prb_teamNotReady(self, team, callback):
        if events.isPlayerEntityChanging:
            return None
        self._doCmdInt3(AccountCommands.CMD_PRB_TEAM_NOT_READY, team, 0, (0,), (lambda requestID, resultID, errorStr: callback(resultID)))

    
    def prb_kick(self, playerID, callback):
        if events.isPlayerEntityChanging:
            return None
        self._doCmdInt3(AccountCommands.CMD_PRB_KICK, playerID, 0, (0,), (lambda requestID, resultID, errorStr: callback(resultID)))

    
    def prb_changeDivision(self, division, callback):
        if events.isPlayerEntityChanging:
            return None
        self._doCmdInt3(AccountCommands.CMD_PRB_CH_DIVISION, division, 0, (0,), (lambda requestID, resultID, errorStr: callback(resultID)))

    
    def challengeCaptcha(self, challenge, response, callback):
        if events.isPlayerEntityChanging:
            return None
        self._doCmdInt2Str(AccountCommands.CMD_CAPTCHA_CHALLENGE, len(challenge), 0, (challenge + response,), (lambda requestID, resultID, errorCode: callback(resultID, errorCode)))

    
    def setLanguage(self, language):
        self._doCmdStr(AccountCommands.CMD_SET_LANGUAGE, language, None)

    
    def makeDenunciation(self, violatorID, topicID, violatorKind):
        self._doCmdInt3(AccountCommands.CMD_MAKE_DENUNCIATION, violatorID, topicID, violatorKind, None)

    
    def banUnbanUser(self, accountDBID, restrType, banPeriod, reason, isBan, callback = None):
        reason = reason.encode('utf8')
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr, ext = ({ },): callback(resultID, errorStr, ext)
        else:
            proxy = None
        intArr = [
            accountDBID,
            restrType,
            banPeriod,
            isBan]
        strArr = [
            reason]
        self._doCmdIntArrStrArr(AccountCommands.CMD_BAN_UNBAN_USER, intArr, strArr, proxy)

    
    def completeTutorial(self, tutorialID, callback):
        g_currentVehicle = g_currentVehicle
        import CurrentVehicle
        if g_currentVehicle.isPresent():
            pass
        1
        curVehInvID = 0
        self._doCmdInt3(AccountCommands.CMD_COMPLETE_TUTORIAL, tutorialID, curVehInvID, (0,), (lambda requestID, resultID, errorStr: callback(resultID)))

    
    def verifyFinPassword(self, finPassword, callback):
        if callback is not None:
            
            proxy = lambda requestID, resultID, errorStr: callback(resultID, errorStr)
        else:
            proxy = None
        self._doCmdStr(AccountCommands.CMD_VERIFY_FIN_PSWD, finPassword, proxy)

    
    def steamInitTxn(self, steamID, itemID, callback):
        (None, None, None, self.shop.getGoldPackets)((lambda resultID, packets, rev: self._PlayerAccount__steamInitTxn(steamID, itemID, callback, packets)))

    
    def _PlayerAccount__steamInitTxn(self, steamID, itemID, callback, packets):
        
        try:
            packet = packets[itemID]
            data = str(steamID) + ':' + itemID + ';' + '%.2f' % packet['amount'] + ';' + packet['currency']
            None(None, (self._doCmdStr, AccountCommands.CMD_STEAM_INIT_TXN, data), (lambda requestID, error, errorStr: callback(steamID, itemID, error)))
        except:
            callback(steamID, itemID, AccountCommands.RES_FAILURE)


    
    def steamFinalizeTxn(self, steamID, orderID, callback):
        
        try:
            data = str(steamID) + ':' + str(orderID)
            None(None, (self._doCmdStr, AccountCommands.CMD_STEAM_FINALIZE_TXN, data), (lambda requestID, error, errorStr: callback(steamID, orderID, error)))
        except:
            callback(steamID, orderID, AccountCommands.RES_FAILURE)


    
    def ebankGetBalance(self, callback):
        self._doCmdStr(AccountCommands.CMD_EBANK_GET_BALANCE, '', (lambda requestID, error, errorStr, ebankProps = ({ },): callback(error, errorStr, ebankProps)))

    
    def ebankBuyGold(self, vcoin, callback):
        (None, None, self.shop.ebankVCoinExchangeRate)((lambda resultID, exchangeRate, rev: self._PlayerAccount__ebankBuyGold(rev, vcoin, callback)))

    
    def _PlayerAccount__ebankBuyGold(self, shopRev, vcoin, callback):
        self._doCmdInt3(AccountCommands.CMD_EBANK_BUY_GOLD, shopRev, vcoin, 0, (lambda requestID, error, errorStr, ebankProps = ({ },): callback(error, errorStr, ebankProps)))

    
    def _doCmdStr(self, cmd, str, callback):
        self._PlayerAccount__doCmd('doCmdStr', cmd, callback, str)

    
    def _doCmdInt3(self, cmd, int1, int2, int3, callback):
        self._PlayerAccount__doCmd('doCmdInt3', cmd, callback, int1, int2, int3)

    
    def _doCmdInt4(self, cmd, int1, int2, int3, int4, callback):
        self._PlayerAccount__doCmd('doCmdInt4', cmd, callback, int1, int2, int3, int4)

    
    def _doCmdInt2Str(self, cmd, int1, int2, str, callback):
        self._PlayerAccount__doCmd('doCmdInt2Str', cmd, callback, int1, int2, str)

    
    def _doCmdIntArr(self, cmd, arr, callback):
        self._PlayerAccount__doCmd('doCmdIntArr', cmd, callback, arr)

    
    def _doCmdIntArrStrArr(self, cmd, intArr, strArr, callback):
        self._PlayerAccount__doCmd('doCmdIntArrStrArr', cmd, callback, intArr, strArr)

    
    def _makeTradeOffer(self, passwd, flags, dstDBID, validSec, price, srcWares, srcItemCount, callback):
        if g_accountRepository is None:
            return None
        requestID = self._PlayerAccount__getRequestID()
        if requestID is None:
            return None
        if callback is not None:
            self._PlayerAccount__onCmdResponse[requestID] = callback
        
        self.base.makeTradeOfferByClient(requestID, passwd, flags, dstDBID, validSec, price, srcWares, srcItemCount)

    
    def _update(self, triggerEvents, diff):
        if triggerEvents:
            pass
        1
        '_update'(diff, 'full sync')
        isFullSync = diff.get('prevRev', None) is None
        self.syncData.revision = diff.get('rev', 0)
        self.inventory.synchronize(isFullSync, diff)
        self.stats.synchronize(isFullSync, diff)
        self.trader.synchronize(isFullSync, diff)
        self._PlayerAccount__synchronizeEventNotifications(diff)
        self._PlayerAccount__synchronizeCacheDict(self.prebattleAutoInvites, diff.get('account', None), 'prebattleAutoInvites', 'replace', events.onPrebattleAutoInvitesChanged)
        self._PlayerAccount__synchronizeCacheDict(self.prebattleInvites, diff, 'prebattleInvites', ('update',), (lambda : events.onPrebattleInvitesChanged(diff)))
        self._PlayerAccount__synchronizeCacheDict(self.clanMembers, diff.get('cache', None), 'clanMembers', 'replace', events.onClanMembersListChanged)
        if triggerEvents:
            events.onClientUpdated(diff)
            if not isFullSync:
                for vehTypeCompDescr in diff.get('stats', { }).get('eliteVehicles', ()):
                    events.onVehicleBecomeElite(vehTypeCompDescr)
                
                for (vehInvID, lockReason) in diff.get('cache', { }).get('vehsLock', { }).iteritems():
                    if lockReason is None:
                        lockReason = AccountCommands.LOCK_REASON.NONE
                    
                    events.onVehicleLockChanged(vehInvID, lockReason)
                
            
        

    
    def _subscribeForStream(self, requestID, callback):
        self._PlayerAccount__onStreamComplete[requestID] = callback

    
    def _PlayerAccount__getRequestID(self):
        if g_accountRepository is None:
            return None
        g_accountRepository.requestID += 1
        if g_accountRepository.requestID >= AccountCommands.REQUEST_ID_UNRESERVED_MAX:
            g_accountRepository.requestID = AccountCommands.REQUEST_ID_UNRESERVED_MIN
        
        return g_accountRepository.requestID

    
    def _PlayerAccount__doCmd(self, doCmdMethod, cmd, callback, *args):
        if g_accountRepository is None:
            return None
        requestID = self._PlayerAccount__getRequestID()
        if requestID is None:
            return None
        if callback is not None:
            self._PlayerAccount__onCmdResponse[requestID] = callback
        
        getattr(self.base, doCmdMethod)(requestID, cmd, *args)

    
    def _PlayerAccount__cancelCommands(self):
        for (requestID, callback) in self._PlayerAccount__onCmdResponse.iteritems():
            
            try:
                callback(requestID, AccountCommands.RES_NON_PLAYER, 'NON_PLAYER')
            continue
            LOG_CURRENT_EXCEPTION()
            continue

        
        self._PlayerAccount__onCmdResponse.clear()
        for callback in self._PlayerAccount__onStreamComplete.itervalues():
            
            try:
                callback(False, None)
            continue
            LOG_CURRENT_EXCEPTION()
            continue

        
        self._PlayerAccount__onStreamComplete.clear()

    
    def _PlayerAccount__synchronizeCacheDict(self, repDict, diffDict, key, syncMode, event):
        if not syncMode in ('update', 'replace'):
            raise AssertionError
        if diffDict is None:
            return None
        repl = diffDict.get('%s_r' % key, None)
        if repl is not None:
            repDict.clear()
            repDict.update(repl)
        
        diff = diffDict.get(key, None)
        if diff is not None:
            for (k, v) in diff.iteritems():
                if v is None:
                    repDict.pop(k, None)
                    continue
                
                if syncMode == 'replace':
                    repDict[k] = v
                    continue
                diffDict is None
                repDict.setdefault(k, { })
                repDict[k].update(v)
            
        
        if repl is not None or diff is not None:
            event()
        

    
    def _PlayerAccount__synchronizeEventNotifications(self, diff):
        diffDict = {
            'added': [],
            'removed': [] }
        if diff is None:
            return None
        repl = diff.get('eventNotifications_r', None)
        if repl is not None:
            self.eventNotifications = repl
            diffDict['added'].extend(repl)
        
        diff = diff.get('eventNotifications', None)
        if diff is not None:
            diffDict.update(diff)
        
        if repl is not None or diff is not None:
            events.onEventNotificationsChanged(diffDict)
            LOG_DZ('Account.__synchronizeEventNotifications, diff=%s' % diffDict)
        


Account = PlayerAccount

class AccountInputHandler:
    
    def handleKeyEvent(self, event):
        return False

    
    def handleMouseEvent(self, dx, dy, dz):
        return False



class _AccountRepository(object):
    
    def __init__(self, name, fileServerSettings):
        self.contactInfo = ContactInfo()
        self.fileServerSettings = fileServerSettings
        self.syncData = AccountSyncData.AccountSyncData()
        self.inventory = Inventory.Inventory(self.syncData)
        self.stats = Stats.Stats(self.syncData)
        self.trader = Trader.Trader(self.syncData)
        self.shop = Shop.Shop()
        self.dossierCache = DossierCache.DossierCache(name)
        self.battleResultsCache = BattleResultsCache.BattleResultsCache()
        self.prebattleAutoInvites = { }
        self.prebattleInvites = { }
        self.clanMembers = { }
        self.customFilesCache = CustomFilesCache.CustomFilesCache()
        self.eventNotifications = []
        self.requestID = AccountCommands.REQUEST_ID_UNRESERVED_MIN



def _delAccountRepository():
    global g_accountRepository
    LOG_MX('_delAccountRepository')
    if g_accountRepository is None:
        LOG_WARNING('AccountRepository is None')
        return None
    g_accountRepository.customFilesCache.close()
    g_accountRepository = None

g_accountRepository = None
connectionManager.onDisconnected += _delAccountRepository

