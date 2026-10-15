# Source Generated with Decompyle++
# File: ClientUpdateManager.pyc (Python 2.6)

__author__ = 'i_maliavko'
import inspect
from debug_utils import *
from PlayerEvents import g_playerEvents

class _ClientUpdateManager(object):
    EVENT_TYPE_DELIMITER = '.'
    
    def __init__(self):
        self._ClientUpdateManager__handlers = dict()
        g_playerEvents.onClientUpdated += self._ClientUpdateManager__onClientUpdate

    
    def dispose(self):
        g_playerEvents.onClientUpdated -= self._ClientUpdateManager__onClientUpdate

    
    def _ClientUpdateManager__onClientUpdate(self, diff):
        for (handler, diffpaths) in self._ClientUpdateManager__handlers.iteritems():
            for diffpath in diffpaths:
                (isFire, args) = self._ClientUpdateManager__processPath(diffpath, diff)
                if isFire:
                    handler(args)
                    break
                    continue
            
        

    
    def _ClientUpdateManager__subscribeHandler(self, handler, diffpath):
        if handler not in self._ClientUpdateManager__handlers:
            self._ClientUpdateManager__handlers[handler] = []
        
        if diffpath not in self._ClientUpdateManager__handlers[handler]:
            self._ClientUpdateManager__handlers[handler].append(diffpath)
        

    
    def _ClientUpdateManager__unsubscribeHandler(self, handler, diffpath):
        if handler in self._ClientUpdateManager__handlers:
            if diffpath in self._ClientUpdateManager__handlers[handler]:
                self._ClientUpdateManager__handlers[handler].remove(diffpath)
            
            if not len(self._ClientUpdateManager__handlers[handler]):
                del self._ClientUpdateManager__handlers[handler]
            
        

    
    def addCallback(self, diffpath, handler):
        self._ClientUpdateManager__subscribeHandler(handler, diffpath)

    
    def addCallbacks(self, map_of_handlers):
        for (diffpath, handler) in map_of_handlers.iteritems():
            self._ClientUpdateManager__subscribeHandler(handler, diffpath)
        

    
    def removeCallback(self, diffpath, handler):
        self._ClientUpdateManager__unsubscribeHandler(handler, diffpath)

    
    def removeObjectCallbacks(self, obj_instance):
        self._ClientUpdateManager__handlers = dict((filter,)((lambda item: if inspect.ismethod(item[0]):
passitem[0].__self__ is not obj_instance), self._ClientUpdateManager__handlers.iteritems()))

    
    def _ClientUpdateManager__processPath(self, diffpath, diff):
        diff_ptr = diff
        if diffpath == '':
            return (True, diff_ptr)
        for key in diffpath.split(self.EVENT_TYPE_DELIMITER):
            if not key.isdigit():
                pass
            1
            key = int(key)
            if type(diff_ptr) != dict or key not in diff_ptr:
                return (False, None)
            diff_ptr = diff_ptr[key]
        
        return (True, diff_ptr)


g_clientUpdateManager = _ClientUpdateManager()

