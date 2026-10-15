# Source Generated with Decompyle++
# File: DossierCache.pyc (Python 2.6)

import BigWorld
import AccountCommands
import constants
import dossiers
import cPickle
import os
import base64
from functools import partial
from SyncController import SyncController
from items import vehicles, tankmen
from PlayerEvents import g_playerEvents as events
from constants import DOSSIER_TYPE
from AccountCommands import VEHICLE_SETTINGS_FLAG
from debug_utils import *

class DossierCache(object):
    
    def __init__(self, accountName):
        self._DossierCache__account = None
        self._DossierCache__syncController = None
        p = os.path
        prefsFilePath = unicode(BigWorld.wg_getPreferencesFilePath(), 'utf-8', errors = 'ignore')
        self._DossierCache__cacheDir = p.join(p.dirname(prefsFilePath), 'dossier_cache')
        self._DossierCache__cacheFileName = p.join(self._DossierCache__cacheDir, '%s.dat' % base64.b32encode('%s;%s' % (str(BigWorld.server()), accountName)))
        self._DossierCache__cache = { }
        self._DossierCache__maxChangeTime = 0
        self._DossierCache__version = 0
        self._DossierCache__ignore = True
        self._DossierCache__isSynchronizing = False
        self._DossierCache__syncID = 0
        self._DossierCache__isFirstSync = True
        self._DossierCache__readCache()

    
    def onAccountBecomePlayer(self):
        self._DossierCache__ignore = False
        self._DossierCache__isFirstSync = True
        self.synchronize()

    
    def onAccountBecomeNonPlayer(self):
        self._DossierCache__ignore = True
        self._DossierCache__isSynchronizing = False

    
    def setAccount(self, account):
        self._DossierCache__account = account
        if self._DossierCache__syncController is not None:
            self._DossierCache__syncController.destroy()
            self._DossierCache__syncController = None
        
        if account is not None:
            self._DossierCache__syncController = SyncController(account, self._DossierCache__sendSyncRequest, self._DossierCache__onSyncResponse, self._DossierCache__onSyncComplete)
        

    
    def synchronize(self):
        if self._DossierCache__ignore:
            return None
        if self._DossierCache__isSynchronizing:
            return None
        self._DossierCache__isSynchronizing = True
        self._DossierCache__syncController.request(self._DossierCache__getNextSyncID(), None)

    
    def resynchronize(self):
        LOG_MX('resynchronize', self._DossierCache__maxChangeTime)
        if self._DossierCache__ignore:
            return None
        self._DossierCache__isSynchronizing = True
        self._DossierCache__syncController.request(self._DossierCache__getNextSyncID(), None)

    
    def waitForSync(self, callback):
        if self._DossierCache__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, None)
            
            return None
        if not self._DossierCache__isSynchronizing:
            callback(AccountCommands.RES_CACHE)
            return None
        
        proxy = lambda resultID, data: callback(resultID)
        self._DossierCache__syncController.request(self._DossierCache__syncID, proxy)

    
    def get(self, dossierType, ownerID, callback = None):
        if self._DossierCache__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, '')
            
            return None
        if not self._DossierCache__isSynchronizing:
            self._DossierCache__onGetResponse(AccountCommands.RES_CACHE, dossierType, ownerID, callback)
            return None
        
        proxy = lambda resultID, data: self._DossierCache__onGetResponse(resultID, dossierType, ownerID, callback)
        self._DossierCache__syncController.request(self._DossierCache__syncID, proxy)

    
    def _DossierCache__onSyncResponse(self, syncID, resultID, ext = { }):
        if resultID == AccountCommands.RES_NON_PLAYER:
            return None
        if syncID != self._DossierCache__syncID:
            return None
        if resultID < 0:
            LOG_ERROR('Dossier synchronization failed. Repeating')
            self.resynchronize()
            return None

    
    def _DossierCache__onSyncComplete(self, syncID, data):
        if data is None:
            return None
        (actualCacheVersion, dossiersList) = data
        if not len(dossiersList) % 4 == 0:
            raise AssertionError
        LOG_MX('__onSyncComplete', actualCacheVersion, len(dossiersList))
        if actualCacheVersion != self._DossierCache__version:
            self._DossierCache__cache.clear()
            self._DossierCache__version = actualCacheVersion
        
        if syncID == self._DossierCache__syncID:
            self._DossierCache__isSynchronizing = False
        
        for i in xrange(len(dossiersList) / 4):
            (dossierType, ownerID, changeTime, dossierCompDescr) = dossiersList[4 * i:4 * (i + 1)]
            self._DossierCache__cache[(dossierType, ownerID)] = (changeTime, dossierCompDescr)
            self._DossierCache__maxChangeTime = max(self._DossierCache__maxChangeTime, changeTime)
        
        if self._DossierCache__isFirstSync:
            self._DossierCache__isFirstSync = False
        else:
            events.onDossiersResync()
        if dossiers:
            self._DossierCache__writeCache()
        

    
    def _DossierCache__onGetResponse(self, resultID, dossierType, ownerID, callback):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None)
            
            return None
        if self._DossierCache__isSynchronizing:
            self.get(dossierType, ownerID, callback)
            return None
        dossierCompDescr = self._DossierCache__cache.get((dossierType, ownerID), (0, ''))[1]
        if callback is not None:
            callback(resultID, dossierCompDescr)
        

    
    def _DossierCache__getNextSyncID(self):
        self._DossierCache__syncID += 1
        if self._DossierCache__syncID > 30000:
            self._DossierCache__syncID = 1
        
        return self._DossierCache__syncID

    
    def _DossierCache__sendSyncRequest(self, syncID, proxy):
        if self._DossierCache__ignore:
            return None
        self._DossierCache__account._doCmdInt3(AccountCommands.CMD_SYNC_DOSSIERS, self._DossierCache__version, self._DossierCache__maxChangeTime, 0, proxy)

    
    def _DossierCache__readCache(self):
        self._DossierCache__cache = { }
        self._DossierCache__version = 0
        self._DossierCache__maxChangeTime = 0
        fileHandler = None
        
        try:
            if not os.path.isfile(self._DossierCache__cacheFileName):
                return None
            fileHandler = open(self._DossierCache__cacheFileName, 'rb')
            (self._DossierCache__version, self._DossierCache__cache) = cPickle.load(fileHandler)
            for (changeTime, dossierCompDescr) in self._DossierCache__cache.itervalues():
                self._DossierCache__maxChangeTime = max(self._DossierCache__maxChangeTime, changeTime)
        except:
            LOG_CURRENT_EXCEPTION()

        if fileHandler is not None:
            fileHandler.close()
        

    
    def _DossierCache__writeCache(self):
        fileHandler = None
        
        try:
            if not os.path.isdir(self._DossierCache__cacheDir):
                os.makedirs(self._DossierCache__cacheDir)
            
            fileHandler = open(self._DossierCache__cacheFileName, 'wb')
            cPickle.dump((self._DossierCache__version, self._DossierCache__cache), fileHandler, -1)
        except:
            LOG_CURRENT_EXCEPTION()

        if fileHandler is not None:
            fileHandler.close()
        



