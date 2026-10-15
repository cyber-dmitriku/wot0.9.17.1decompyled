# Source Generated with Decompyle++
# File: ids_generators.pyc (Python 2.6)

import time

class Int32IDGenerator(object):
    
    def __init__(self):
        self._Int32IDGenerator__nextID = 0

    
    def next(self):
        self._Int32IDGenerator__nextID += 1
        if self._Int32IDGenerator__nextID > 65535:
            self._Int32IDGenerator__nextID = 0
        
        currTime = int(time.time())
        return ((currTime & 32767) << 16) + self._Int32IDGenerator__nextID



class SequenceIDGenerator(object):
    
    def __init__(self, lowBound = 0, highBound = 32767):
        self._SequenceIDGenerator__lowBound = lowBound
        self._SequenceIDGenerator__highBound = highBound
        self._SequenceIDGenerator__sequenceID = lowBound

    
    def next(self):
        self._SequenceIDGenerator__sequenceID += 1
        if self._SequenceIDGenerator__sequenceID >= self._SequenceIDGenerator__highBound:
            self._SequenceIDGenerator__sequenceID = self._SequenceIDGenerator__lowBound
        
        return self._SequenceIDGenerator__sequenceID

    currSequenceID = property((lambda self: self._SequenceIDGenerator__sequenceID))
    nextSequenceID = property((lambda self: self.next()))


