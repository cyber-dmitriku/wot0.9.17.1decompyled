# Source Generated with Decompyle++
# File: AccountSyncData.pyc (Python 2.6)

import AccountCommands
from SyncController import SyncController
from debug_utils import *

class AccountSyncData(object):
    
    def __init__(self):
        self.revision = 0
        self._AccountSyncData__account = None
        self._AccountSyncData__syncController = None
        self._AccountSyncData__ignore = True
        self._AccountSyncData__isSynchronized = False
        self._AccountSyncData__syncID = 0
        self._AccountSyncData__subscribers = []
        self._AccountSyncData__isFirstSync = True

    
    def onAccountBecomePlayer(self):
        self._AccountSyncData__ignore = False
        self._AccountSyncData__isFirstSync = True
        self._synchronize()

    
    def onAccountBecomeNonPlayer(self):
        self._AccountSyncData__ignore = True
        self._AccountSyncData__isSynchronized = False

    
    def setAccount(self, account):
        self._AccountSyncData__account = account
        if self._AccountSyncData__syncController is not None:
            self._AccountSyncData__syncController.destroy()
            self._AccountSyncData__syncController = None
        
        if account is not None:
            self._AccountSyncData__syncController = SyncController(account, self._AccountSyncData__sendSyncRequest, self._AccountSyncData__onSyncResponse, self._AccountSyncData__onSyncComplete)
        

    
    def waitForSync(self, callback):
        if self._AccountSyncData__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER)
            
            return None
        if self._AccountSyncData__isSynchronized:
            callback(AccountCommands.RES_CACHE)
            return None
        if callback is not None:
            self._AccountSyncData__subscribers.append(callback)
        

    
    def _synchronize(self):
        if self._AccountSyncData__ignore:
            return None
        if self._AccountSyncData__isSynchronized:
            return None
        self._AccountSyncData__syncController.request(self._AccountSyncData__getNextSyncID(), None)

    
    def _resynchronize(self):
        LOG_MX('resynchronize')
        if self._AccountSyncData__ignore:
            return None
        self._AccountSyncData__isSynchronized = False
        self.revision = 0
        self._AccountSyncData__syncController.request(self._AccountSyncData__getNextSyncID(), None)

    
    def _AccountSyncData__onSyncResponse(self, syncID, resultID, ext = { }):
        if resultID == AccountCommands.RES_NON_PLAYER:
            return None
        if syncID != self._AccountSyncData__syncID:
            return None
        if resultID < 0:
            LOG_ERROR('Data synchronization failed.')
            self._resynchronize()
            return None
        if self.revision != ext.get('prevRev', self.revision):
            LOG_ERROR('Incorrect diff received', self.revision, ext['prevRev'])
            self._resynchronize()
            return None
        self.revision = ext.get('rev', self.revision)
        self._AccountSyncData__isSynchronized = True
        self._AccountSyncData__account._update(not (self._AccountSyncData__isFirstSync), ext)
        self._AccountSyncData__isFirstSync = False
        subscribers = self._AccountSyncData__subscribers
        self._AccountSyncData__subscribers = []
        for callback in subscribers:
            callback(resultID)
        

    
    def _AccountSyncData__onSyncComplete(self, syncID, data):
        if syncID != self._AccountSyncData__syncID:
            return None
        if data is None:
            return None
        self.revision = data['rev']
        self._AccountSyncData__account._update(False, data)
        self._synchronize()

    
    def _AccountSyncData__getNextSyncID(self):
        self._AccountSyncData__syncID += 1
        if self._AccountSyncData__syncID > 30000:
            self._AccountSyncData__syncID = 1
        
        return self._AccountSyncData__syncID

    
    def _AccountSyncData__sendSyncRequest(self, id, proxy):
        if self._AccountSyncData__ignore:
            return None
        self._AccountSyncData__account._doCmdInt3(AccountCommands.CMD_SYNC_DATA, self.revision, 0, 0, proxy)



def synchronizeDicts(diff, cache):
    for (key, value) in diff.iteritems():
        if value is None:
            cache.pop(key, None)
            continue
        if isinstance(value, dict):
            synchronizeDicts(value, cache.setdefault(key, { }))
            continue
        cache[key] = value
    


