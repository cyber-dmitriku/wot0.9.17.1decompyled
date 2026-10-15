# Source Generated with Decompyle++
# File: HornCooldown.pyc (Python 2.6)

import BigWorld
import Event

class HornCooldown:
    
    def __init__(self, windowSize, maxSignals, state = None):
        self._HornCooldown__windowSize = windowSize
        self._HornCooldown__maxSignals = maxSignals
        if state is not None:
            self._HornCooldown__signals = state
            self._HornCooldown__reduce(BigWorld.time())
            del self._HornCooldown__signals[:-maxSignals]
        else:
            self._HornCooldown__signals = []
        self._HornCooldown__banEvent = Event.Event()
        self._HornCooldown__banStartTime = 0
        self._HornCooldown__banPeriod = 0

    
    def banEvent(self):
        return self._HornCooldown__banEvent

    banEvent = property(banEvent)
    
    def ask(self):
        curTime = BigWorld.time()
        if self._HornCooldown__banPeriod > 0:
            if curTime - self._HornCooldown__banStartTime < self._HornCooldown__banPeriod:
                return False
            self._HornCooldown__banPeriod = 0
        
        self._HornCooldown__reduce(curTime)
        if len(self._HornCooldown__signals) < self._HornCooldown__maxSignals:
            self._HornCooldown__signals.append(curTime)
            bt = self.banTime()
            if bt > 0:
                self._HornCooldown__banEvent(bt)
            
            return True
        return False

    
    def banTime(self):
        curTime = BigWorld.time()
        if self._HornCooldown__banPeriod > 0:
            past = curTime - self._HornCooldown__banStartTime
            if past < self._HornCooldown__banPeriod:
                return self._HornCooldown__banPeriod - past
            self._HornCooldown__banPeriod = 0
        
        if len(self._HornCooldown__signals) < self._HornCooldown__maxSignals:
            return 0
        return max(0, self._HornCooldown__signals[0] + self._HornCooldown__windowSize - curTime)

    
    def ban(self, period):
        if self.banTime() < period:
            self._HornCooldown__banStartTime = BigWorld.time()
            self._HornCooldown__banPeriod = period
            self._HornCooldown__banEvent(period)
        

    
    def _HornCooldown__reduce(self, curTime):
        if len(self._HornCooldown__signals) == 0:
            return None
        cutTime = curTime - self._HornCooldown__windowSize
        if cutTime > self._HornCooldown__signals[-1]:
            del self._HornCooldown__signals[:]
            return None
        for (i, time) in enumerate(self._HornCooldown__signals):
            if time > cutTime:
                del self._HornCooldown__signals[:i]
                return None
        



