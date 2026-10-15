# Source Generated with Decompyle++
# File: data_providers.pyc (Python 2.6)

from abc import abstractmethod, ABCMeta, abstractproperty
from gui.Scaleform.CommandArgsParser import CommandArgsParser
from gui.Scaleform.windows import UIInterface

class BaseDataProvider(UIInterface):
    __metaclass__ = ABCMeta
    
    def __init__(self, prefix):
        UIInterface.__init__(self)
        self._BaseDataProvider__prefix = prefix

    
    def prefix(self):
        return self._BaseDataProvider__prefix

    
    def buildList(self, *args):
        pass

    buildList = abstractmethod(buildList)
    
    def emptyItem(self):
        pass

    emptyItem = abstractmethod(emptyItem)
    
    def list(self):
        pass

    list = abstractproperty(list)
    
    def length(self):
        return len(self.list)

    
    def requestItemAt(self, idx):
        if -1 < idx:
            pass
        idx < self.length()
        if 1:
            return self.list[idx]

    
    def requestItemRange(self, startIndex, endIndex):
        return self.list[startIndex:endIndex]

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self.uiHolder.addExternalCallbacks({
            '%s.RequestLength' % self._BaseDataProvider__prefix: self.onRequestLength,
            '%s.RequestItemAt' % self._BaseDataProvider__prefix: self.onRequestItemAt,
            '%s.RequestItemRange' % self._BaseDataProvider__prefix: self.onRequestItemRange })

    
    def dispossessUI(self):
        self.uiHolder.removeExternalCallbacks('%s.RequestLength' % self._BaseDataProvider__prefix, '%s.RequestItemAt' % self._BaseDataProvider__prefix, '%s.RequestItemRange' % self._BaseDataProvider__prefix)
        UIInterface.dispossessUI(self)

    
    def refresh(self):
        self.uiHolder.call('%s.RefreshList' % self._BaseDataProvider__prefix, [
            self.length()])

    
    def onRequestLength(self, *args):
        parser = CommandArgsParser(self.onRequestLength.__name__)
        parser.parse(*args)
        parser.addArg(self.length())
        self.respond(parser.args())

    
    def onRequestItemAt(self, *args):
        parser = CommandArgsParser(self.onRequestItemAt.__name__, 1, [
            int])
        (index,) = parser.parse(*args)
        item = self.requestItemAt(index)
        if item:
            parser.addArgs(item)
        else:
            parser.addArgs(self.emptyItem())
        self.respond(parser.args())

    
    def onRequestItemRange(self, *args):
        parser = CommandArgsParser(self.onRequestItemRange.__name__, 2, [
            int,
            int])
        (startIndex, endIndex) = parser.parse(*args)
        for item in self.list[startIndex:endIndex + 1]:
            parser.addArgs(item)
        
        self.respond(parser.args())



class BaseDirectAccessDP(UIInterface):
    __metaclass__ = ABCMeta
    
    def __init__(self):
        UIInterface.__init__(self)
        self._BaseDirectAccessDP__flashDP = None

    
    def _BaseDirectAccessDP__setFlashDP(self, dp):
        self._BaseDirectAccessDP__flashDP = dp

    
    def getFlashDP(self):
        return self._BaseDirectAccessDP__flashDP

    
    def buildList(self, *args):
        pass

    buildList = abstractmethod(buildList)
    
    def emptyItem(self):
        pass

    emptyItem = abstractmethod(emptyItem)
    
    def setupFlashDp(self, proxy):
        pass

    setupFlashDp = abstractmethod(setupFlashDp)
    
    def list(self):
        pass

    list = abstractproperty(list)
    
    def length(self):
        return len(self.list)

    
    def requestItemAt(self, idx):
        if -1 < idx:
            pass
        idx < self.length()
        if 1:
            return self.list[int(idx)]

    
    def requestItemRange(self, startIndex, endIndex):
        return self.list[int(startIndex):int(endIndex) + 1]

    
    def refresh(self):
        self._BaseDirectAccessDP__flashDP.invalidate(self.length())

    
    def lengthHandler(self):
        l = self.list
        return len(l)

    
    def requestItemAtHandler(self, idx):
        l = self.list
        if -1 < idx:
            pass
        idx < self.length()
        if 1:
            return l[int(idx)]

    
    def requestItemRangeHandler(self, startIndex, endIndex):
        l = self.list
        items = l[int(startIndex):int(endIndex) + 1]
        return items

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self._BaseDirectAccessDP__setFlashDP(self.setupFlashDp(proxy))
        self._BaseDirectAccessDP__flashDP.resync()
        self._BaseDirectAccessDP__flashDP.script = self

    
    def dispossessUI(self):
        self._BaseDirectAccessDP__flashDP.script = None
        self._BaseDirectAccessDP__flashDP = None
        UIInterface.dispossessUI(self)



