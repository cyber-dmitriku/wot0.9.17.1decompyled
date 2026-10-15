# Source Generated with Decompyle++
# File: DebugPanel.pyc (Python 2.6)

import BigWorld
from gui.DebugView import DebugView
from gui.DebugView import DebugViewItem
from debug_utils import *

class DebugPanel(DebugView):
    
    def __init__(self, textureName = '', parentGUI = None, updateInterval = 0.1):
        DebugView.__init__(self, textureName, parentGUI)
        self._DebugPanel__cbIDUpdate = None
        self._DebugPanel__cbUpdateInterval = -1
        self.setUpdateInterval(updateInterval)

    
    def destroy(self):
        self.setUpdateInterval(-1)
        DebugView.destroy(self)

    
    def setUpdateInterval(self, interval = 0.1):
        self._DebugPanel__cbUpdateInterval = interval
        if self._DebugPanel__cbIDUpdate is not None:
            BigWorld.cancelCallback(self._DebugPanel__cbIDUpdate)
            self._DebugPanel__cbIDUpdate = None
        
        if self._DebugPanel__cbUpdateInterval >= 0:
            self._DebugPanel__onUpdate()
        

    
    def addItem(self, keyname, item):
        if not isinstance(item, DebugPanelItem):
            return None
        DebugView.addItem(self, keyname, item)

    
    def update(self):
        for item in self.iteritems():
            v = item.request()
            if v is not None:
                item.setValue(v)
                continue
        
        DebugView.update(self)

    
    def _DebugPanel__onUpdate(self):
        self._DebugPanel__cbIDUpdate = None
        self.update()
        self._DebugPanel__cbIDUpdate = BigWorld.callback((self._DebugPanel__cbUpdateInterval,), (lambda : self._DebugPanel__onUpdate()))



class DebugPanelItem(DebugViewItem):
    
    def __init__(self, name = '', updater = None, mapper = None):
        DebugViewItem.__init__(self, name)
        self._DebugPanelItem__updater = updater
        self._DebugPanelItem__mapper = mapper

    
    def destroy(self):
        self._DebugPanelItem__updater.destroy()
        self._DebugPanelItem__updater = None
        self._DebugPanelItem__mapper = None
        DebugViewItem.destroy(self)

    
    def request(self):
        if self._DebugPanelItem__updater is None:
            return None
        
        try:
            v = self._DebugPanelItem__updater.request()
            if v is None:
                return None
            if self._DebugPanelItem__mapper is None:
                return str(v)
            return str(self._DebugPanelItem__mapper(v))
        except:
            self._DebugPanelItem__updater is None
            LOG_DEBUG('DebugPanelItem: value request failed. Look exception below')
            LOG_CURRENT_EXCEPTION()
            return None


    
    def setUpdaterMapper(self, updater, mapper):
        self._DebugPanelItem__updater = updater
        self._DebugPanelItem__mapper = mapper



class DebugPanelItemUpdater:
    
    def __init__(self, functor, interval = 0):
        self._DebugPanelItemUpdater__value = None
        self._DebugPanelItemUpdater__cbIDValid = None
        self._DebugPanelItemUpdater__cbFunctor = None
        self._DebugPanelItemUpdater__cbInterval = -1
        self.setFunctor(functor, interval)

    
    def destroy(self):
        self.setFunctor(None, -1)

    
    def request(self):
        self._DebugPanelItemUpdater__validate()
        return self._DebugPanelItemUpdater__value

    
    def setFunctor(self, functor, interval):
        self._DebugPanelItemUpdater__invalidate()
        self._DebugPanelItemUpdater__cbFunctor = functor
        self._DebugPanelItemUpdater__cbInterval = interval

    
    def getValid(self):
        return self._DebugPanelItemUpdater__cbIDValid is not None

    
    def _DebugPanelItemUpdater__validate(self):
        if self.getValid():
            return None
        self._DebugPanelItemUpdater__value = None
        
        try:
            self._DebugPanelItemUpdater__value = self._DebugPanelItemUpdater__cbFunctor()
        except:
            self.getValid()
            LOG_DEBUG('DebugPanelItemUpdater: value validating failed. Look exception below')
            LOG_CURRENT_EXCEPTION()
            return None

        self._DebugPanelItemUpdater__cbIDValid = BigWorld.callback((self._DebugPanelItemUpdater__cbInterval,), (lambda : self._DebugPanelItemUpdater__doInvalidate()))

    
    def _DebugPanelItemUpdater__invalidate(self):
        if self._DebugPanelItemUpdater__cbIDValid is not None:
            BigWorld.cancelCallback(self._DebugPanelItemUpdater__cbIDValid)
            self._DebugPanelItemUpdater__doInvalidate()
        

    
    def _DebugPanelItemUpdater__doInvalidate(self):
        self._DebugPanelItemUpdater__cbIDValid = None



