# Source Generated with Decompyle++
# File: time_utils.pyc (Python 2.6)

import time
import BigWorld
import datetime
import calendar

class _TimeCorrector(object):
    
    def __init__(self):
        self._evalTimeCorrection(time.time())

    
    def _evalTimeCorrection(self, serverUTCTime):
        self._TimeCorrector__clientLoginTime = BigWorld.time()
        self._TimeCorrector__serverLoginUTCTime = serverUTCTime

    
    def _TimeCorrector__loginDelta(self):
        return BigWorld.time() - self._TimeCorrector__clientLoginTime

    timeCorrection = property((lambda self: self.serverUTCTime - time.time()))
    serverUTCTime = property((lambda self: self._TimeCorrector__serverLoginUTCTime + self._TimeCorrector__loginDelta()))

_g_instance = _TimeCorrector()

def setTimeCorrection(serverUTCTime):
    _g_instance._evalTimeCorrection(serverUTCTime)


def makeLocalServerTime(serverTime):
    if serverTime:
        return serverTime - _g_instance.timeCorrection


def makeLocalServerDatetime(serverDatetime):
    if isinstance(serverDatetime, datetime.datetime):
        return serverDatetime - datetime.timedelta(seconds = _g_instance.timeCorrection)


def utcToLocalDatetime(utcDatetime):
    return datetime.datetime.fromtimestamp(calendar.timegm(utcDatetime.timetuple()))


