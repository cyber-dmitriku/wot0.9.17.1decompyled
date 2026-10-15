# Source Generated with Decompyle++
# File: account_shared.pyc (Python 2.6)

import collections
import time

class AmmoIterator(object):
    
    def __init__(self, ammo):
        self._AmmoIterator__ammo = ammo
        self._AmmoIterator__idx = 0

    
    def __iter__(self):
        return self

    
    def next(self):
        if self._AmmoIterator__idx >= len(self._AmmoIterator__ammo):
            raise StopIteration
        self._AmmoIterator__idx >= len(self._AmmoIterator__ammo)
        idx = self._AmmoIterator__idx
        self._AmmoIterator__idx += 2
        return (self._AmmoIterator__ammo[idx], self._AmmoIterator__ammo[idx + 1])



def getAmmoDiff(ammo1, ammo2):
    diff = collections.defaultdict(int)
    for (compDescr, count) in AmmoIterator(ammo1):
        diff[compDescr] += count
    
    for (compDescr, count) in AmmoIterator(ammo2):
        diff[compDescr] -= count
    
    return diff


def getEquipmentsDiff(eqs1, eqs2):
    diff = collections.defaultdict(int)
    for eqCompDescr in eqs1:
        if eqCompDescr != 0:
            diff[eqCompDescr] += 1
            continue
    
    for eqCompDescr in eqs2:
        if eqCompDescr != 0:
            diff[eqCompDescr] -= 1
            continue
    
    return diff


def currentWeekPlayDaysCount(curTime, newDayStart, newWeekStart):
    curTime += newDayStart
    wday = time.gmtime(curTime).tm_wday + 1
    curWeekPlayDaysCnt = wday - newWeekStart
    if newWeekStart >= 0:
        if curWeekPlayDaysCnt == 0:
            curWeekPlayDaysCnt = 7
        elif curWeekPlayDaysCnt < 0:
            curWeekPlayDaysCnt += 7
        
    elif curWeekPlayDaysCnt == 8:
        curWeekPlayDaysCnt = 1
    elif curWeekPlayDaysCnt > 8:
        curWeekPlayDaysCnt -= 7
    
    return curWeekPlayDaysCnt


