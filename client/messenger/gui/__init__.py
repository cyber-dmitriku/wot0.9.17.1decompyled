# Source Generated with Decompyle++
# File: __init__.pyc (Python 2.6)

from ConnectionManager import connectionManager
from debug_utils import LOG_ERROR
import exceptions
from messenger.gui import MessengerDispatcher
from PlayerEvents import g_playerEvents

def init():
    
    try:
        MessengerLobbyInterface = MessengerLobbyInterface
        import messenger.gui.Scalefrom.MessengerLobbyInterface
        MessengerBattleInterface = MessengerBattleInterface
        import messenger.gui.Scalefrom.MessengerBattleInterface
        MessengerDispatcher.g_instance = MessengerDispatcher.MessengerDispatcher(MessengerLobbyInterface, MessengerBattleInterface)
    except exceptions.ImportError:
        LOG_ERROR('Package messenger.gui.Scaleform not defined')
        raise 



def start():
    messenger = MessengerDispatcher.g_instance
    if messenger is not None:
        g_playerEvents.onAccountBecomePlayer += messenger.onLobbyConnect
        connectionManager.onDisconnected += messenger.onDisconnect
    


def fini():
    messenger = MessengerDispatcher.g_instance
    if messenger is not None:
        g_playerEvents.onAccountBecomePlayer -= messenger.onLobbyConnect
        connectionManager.onDisconnected -= messenger.onDisconnect
        messenger.onDisconnect()
    


