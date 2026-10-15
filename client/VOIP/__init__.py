# Source Generated with Decompyle++
# File: __init__.pyc (Python 2.6)

from ResponseHandler import ResponseHandler
import BigWorld
from Vivox.VivoxHandler import VivoxHandler as VOIPHandler
from Vivox.VivoxManager import VivoxManager as VOIPManager

def getResponseHandler():
    if not globals().has_key('__handler'):
        globals()['__handler'] = VOIPManager(VOIPHandler())
        BigWorld.VOIP.setHandler(__handler.channelsMgr)
    
    return __handler


