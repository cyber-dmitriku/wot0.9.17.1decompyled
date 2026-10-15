# Source Generated with Decompyle++
# File: streamIDs.pyc (Python 2.6)

STREAM_ID_CHAT_MIN = 1
STREAM_ID_CHAT_MAX = 99
CHAT_INITIALIZATION_ID = 50
STREAM_ID_AVATAR_BATTLE_RESULS = 100
STREAM_ID_ACCOUNT_CMDS_MIN = 200
STREAM_ID_ACCOUNT_CMDS_MAX = 30000

class RangeStreamIDCallbacks(object):
    
    def __init__(self, rangeFactor = 100):
        self._RangeStreamIDCallbacks__callbacks = dict()
        self._RangeStreamIDCallbacks__rangeFactor = int(rangeFactor)

    
    def addRangeCallback(self, range, callback):
        for key in self._RangeStreamIDCallbacks__getKeySequence(range):
            self._RangeStreamIDCallbacks__callbacks[key] = callback
        

    
    def delRangeCallback(self, range):
        for key in self._RangeStreamIDCallbacks__getKeySequence(range):
            if key in self._RangeStreamIDCallbacks__callbacks:
                del self._RangeStreamIDCallbacks__callbacks[key]
                continue
        

    
    def clear(self):
        self._RangeStreamIDCallbacks__callbacks.clear()

    
    def getCallbackForStreamID(self, streamID):
        key = streamID / self._RangeStreamIDCallbacks__rangeFactor
        return self._RangeStreamIDCallbacks__callbacks.get(key, None)

    
    def _RangeStreamIDCallbacks__getKeySequence(self, range):
        lowBound = int(range[0])
        highBound = range[1]
        if highBound < lowBound:
            highBound = lowBound
            lowBound = highBound
        
        lowKeyCandidate = lowBound / self._RangeStreamIDCallbacks__rangeFactor
        highKeyCandidate = highBound / self._RangeStreamIDCallbacks__rangeFactor
        return xrange(lowKeyCandidate, highKeyCandidate + 1)


if __name__ == '__main__':
    rangeCBs = RangeStreamIDCallbacks()
    rangeCBs.addRangeCallback((1, 99), (lambda streamID: (streamID, (1, 99))))
    rangeCBs.addRangeCallback((100, 300), (lambda streamID: (streamID, (100, 300))))
    rangeCBs.addRangeCallback((301, 399), (lambda streamID: (streamID, (301, 399))))
    rangeCBs.addRangeCallback((101, 200), (lambda streamID: (streamID, (101, 200))))
    rangeCBs.addRangeCallback((400, 599), (lambda streamID: (streamID, (400, 599))))
    
    def outStreamIdCB(streamID):
        cb = rangeCBs.getCallbackForStreamID(streamID)
        if cb:
            pass
        1
        print streamID % (str(cb(streamID)), 'None')

    outStreamIdCB(50)
    outStreamIdCB(100)
    outStreamIdCB(150)
    outStreamIdCB(300)
    outStreamIdCB(301)
    outStreamIdCB(399)
    outStreamIdCB(400)
    outStreamIdCB(401)
    rangeCBs.delRangeCallback((101, 199))
    outStreamIdCB(100)
    outStreamIdCB(101)
    outStreamIdCB(150)
    outStreamIdCB(199)
    outStreamIdCB(200)
    rangeCBs.delRangeCallback((101, 200))
    outStreamIdCB(199)
    outStreamIdCB(200)
    outStreamIdCB(201)
    outStreamIdCB(299)
    outStreamIdCB(300)


