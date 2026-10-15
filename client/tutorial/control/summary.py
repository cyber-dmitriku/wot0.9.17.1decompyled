# Source Generated with Decompyle++
# File: summary.pyc (Python 2.6)

from tutorial.control.functional import FunctionalVarSet
from tutorial.logger import LOG_ERROR, LOG_DEBUG

class _Flag(object):
    
    def __init__(self, name, active, store = True):
        super(_Flag, self).__init__()
        self.name = name
        self.active = active
        self.store = store

    
    def __repr__(self):
        return '{0:>s}: {1!r:s}'.format(self.name, self.active)

    
    def isActive(self):
        return self.active

    
    def activate(self):
        self.active = True

    
    def deactivate(self):
        self.active = False



class FlagSummary(object):
    
    def __init__(self, flagNames, initial = None):
        super(FlagSummary, self).__init__()
        if flagNames is None:
            flagNames = []
        
        if initial is None:
            initial = { }
        
        self._FlagSummary__flags = { }
        initialGetter = initial.get
        for name in flagNames:
            self._FlagSummary__flags[name] = _Flag(name, initialGetter(name, False))
        

    
    def __repr__(self):
        return 'FlagSummary({0:s}): {1!r:s}'.format(hex(id(self)), self._FlagSummary__flags.values())

    
    def deactivateFlag(self, flagName):
        LOG_DEBUG('Deactivate flag', flagName)
        if flagName in self._FlagSummary__flags:
            self._FlagSummary__flags[flagName].deactivate()
        else:
            self._FlagSummary__flags[flagName] = _Flag(flagName, False, store = False)

    
    def activateFlag(self, flagName):
        LOG_DEBUG('Activate flag: ', flagName)
        if flagName in self._FlagSummary__flags:
            self._FlagSummary__flags[flagName].activate()
        else:
            self._FlagSummary__flags[flagName] = _Flag(flagName, True, store = False)

    
    def isActiveFlag(self, flagName):
        activeFlag = False
        if flagName in self._FlagSummary__flags:
            activeFlag = self._FlagSummary__flags[flagName].isActive()
        
        return activeFlag

    
    def addFlag(self, flagName):
        if flagName not in self._FlagSummary__flags:
            self._FlagSummary__flags[flagName] = _Flag(flagName, False)
        

    
    def getDict(self):
        filtered = filter((lambda flag: flag.store), self._FlagSummary__flags.itervalues())
        return dict(map((lambda flag: (flag.name, flag.active)), filtered))



class VarSummary(object):
    
    def __init__(self, varSets):
        super(VarSummary, self).__init__()
        if varSets is None:
            varSets = []
        
        self._VarSummary__varSets = dict(map((lambda varSet: (varSet.getID(), FunctionalVarSet(varSet))), varSets))
        self._VarSummary__runtime = { }

    
    def get(self, varID):
        if varID in self._VarSummary__varSets:
            result = self._VarSummary__varSets[varID].getFirstActual()
        else:
            result = self._VarSummary__runtime.get(varID)
        return result

    
    def set(self, varID, value):
        if varID in self._VarSummary__varSets:
            LOG_ERROR('Var {0:>s} in not mutable.'.format(varID))
        else:
            LOG_DEBUG('Set var {0:>s}'.format(varID), value)
            self._VarSummary__runtime[varID] = value



