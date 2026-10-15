# Source Generated with Decompyle++
# File: __init__.pyc (Python 2.6)

from abc import ABCMeta, abstractmethod

class HasID(object):
    __meta__ = ABCMeta
    
    def getID(self):
        pass

    getID = abstractmethod(getID)
    
    def setID(self, id):
        pass

    setID = abstractmethod(setID)


class HasTargetID(object):
    __meta__ = ABCMeta
    
    def getTargetID(self):
        pass

    getTargetID = abstractmethod(getTargetID)
    
    def setTargetID(self, id):
        pass

    setTargetID = abstractmethod(setTargetID)


