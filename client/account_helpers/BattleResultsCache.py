# Source Generated with Decompyle++
# File: BattleResultsCache.pyc (Python 2.6)

import os
import BigWorld
import cPickle
import AccountCommands
import zlib
import base64
from functools import partial
from battle_results_shared import *
from debug_utils import *
BATTLE_RESULTS_VERSION = 1
CACHE_DIR = os.path.join(os.path.dirname(unicode(BigWorld.wg_getPreferencesFilePath(), 'utf-8', errors = 'ignore')), 'battle_results')

class BattleResultsCache(object):
    
    def __init__(self):
        self._BattleResultsCache__account = None
        self._BattleResultsCache__ignore = True
        self._BattleResultsCache__waiting = False
        clean()

    
    def onAccountBecomePlayer(self):
        self._BattleResultsCache__ignore = False
        self._BattleResultsCache__waiting = False

    
    def onAccountBecomeNonPlayer(self):
        self._BattleResultsCache__ignore = True

    
    def setAccount(self, account):
        self._BattleResultsCache__account = account

    
    def get(self, arenaUniqueID, callback):
        if self._BattleResultsCache__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, None)
            
            return None
        if self._BattleResultsCache__waiting:
            if callback is not None:
                callback(AccountCommands.RES_COOLDOWN, None)
            
            return None
        battleResults = load(self._BattleResultsCache__account.name, arenaUniqueID)
        if battleResults is not None:
            if callback is not None:
                callback(AccountCommands.RES_CACHE, convertToFullForm(battleResults))
            
            return None
        self._BattleResultsCache__waiting = True
        proxy = partial(self._BattleResultsCache__onGetResponse, callback)
        self._BattleResultsCache__account._doCmdInt3(AccountCommands.CMD_REQ_BATTLE_RESULTS, arenaUniqueID, 0, 0, proxy)

    
    def _BattleResultsCache__onGetResponse(self, callback, requestID, resultID, errorStr, ext = { }):
        if resultID != AccountCommands.RES_STREAM:
            self._BattleResultsCache__waiting = False
            if callback is not None:
                callback(resultID, None)
            
            return None
        self._BattleResultsCache__account._subscribeForStream(requestID, partial(self._BattleResultsCache__onStreamComplete, callback))

    
    def _BattleResultsCache__onStreamComplete(self, callback, isSuccess, data):
        self._BattleResultsCache__waiting = False
        
        try:
            battleResults = cPickle.loads(zlib.decompress(data))
            save(self._BattleResultsCache__account.name, battleResults)
            if callback is not None:
                callback(AccountCommands.RES_STREAM, convertToFullForm(battleResults))
            
            self._BattleResultsCache__account.base.doCmdInt3(AccountCommands.REQUEST_ID_NO_RESPONSE, AccountCommands.CMD_BATTLE_RESULTS_RECEIVED, battleResults[0], 0, 0)
        except:
            LOG_CURRENT_EXCEPTION()
            if callback is not None:
                callback(AccountCommands.RES_FAILURE, None)
            




def save(accountName, battleResults):
    fileHandler = None
    
    try:
        arenaUniqueID = battleResults[0]
        folderName = getFolderName(accountName, arenaUniqueID)
        if not os.path.isdir(folderName):
            os.makedirs(folderName)
        
        fileName = os.path.join(folderName, '%s.dat' % arenaUniqueID)
        fileHandler = open(fileName, 'wb')
        cPickle.dump((BATTLE_RESULTS_VERSION, battleResults), fileHandler, -1)
    except:
        LOG_CURRENT_EXCEPTION()

    if fileHandler is not None:
        fileHandler.close()
    


def load(accountName, arenaUniqueID):
    fileHandler = None
    
    try:
        fileName = os.path.join(getFolderName(accountName, arenaUniqueID), '%s.dat' % arenaUniqueID)
        if not os.path.isfile(fileName):
            return None
        fileHandler = open(fileName, 'rb')
        (version, battleResults) = cPickle.load(fileHandler)
    except:
        LOG_CURRENT_EXCEPTION()

    if fileHandler is not None:
        fileHandler.close()
    
    if version == BATTLE_RESULTS_VERSION:
        return battleResults


def getFolderName(accountName, arenaUniqueID):
    battleStartTime = arenaUniqueID & 0xFFFFFFFFL
    battleStartDay = battleStartTime / 86400
    return os.path.join(CACHE_DIR, base64.b32encode('%s;%s' % (accountName, battleStartDay)))


def clean():
    
    try:
        for (root, dirs, files) in os.walk(CACHE_DIR, topdown = False):
            for name in files:
                os.remove(os.path.join(root, name))
            
            for name in dirs:
                os.rmdir(os.path.join(root, name))
            
    except:
        LOG_CURRENT_EXCEPTION()



def convertToFullForm(compactForm):
    fullForm = {
        'arenaUniqueID': compactForm[0],
        'personal': listToDict(VEH_FULL_RESULTS, compactForm[1]),
        'common': { },
        'players': { },
        'vehicles': { } }
    fullForm['personal']['details'] = VehicleInteractionDetails.fromPacked(fullForm['personal']['details']).toDict()
    (commonAsList, playersAsList, vehiclesAsList) = cPickle.loads(compactForm[2])
    fullForm['common'] = listToDict(COMMON_RESULTS, commonAsList)
    for (accountDBID, playerAsList) in playersAsList.iteritems():
        fullForm['players'][accountDBID] = listToDict(PLAYER_INFO, playerAsList)
    
    for (vehicleID, vehicleAsList) in vehiclesAsList.iteritems():
        fullForm['vehicles'][vehicleID] = listToDict(VEH_PUBLIC_RESULTS, vehicleAsList)
    
    return fullForm


