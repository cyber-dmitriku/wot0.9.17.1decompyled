# Source Generated with Decompyle++
# File: __init__.pyc (Python 2.6)

import BigWorld
from AuxiliaryFx.FxController import AuxiliaryFxController
from AuxiliaryFx.Roccat import RoccatFxManager
import AuxiliaryFx

class IAuxiliaryFxManager:
    
    def isEnabled(self):
        return False

    
    def destroy(self):
        pass

    
    def start(self):
        pass


g_instance = None

class AuxiliaryFxManager:
    
    def __init__(self):
        self._AuxiliaryFxManager__fxManagers = [
            (RoccatFxManager.RoccatFxManager(), RoccatFxManager.RoccatVehicleFx)]
        self._AuxiliaryFxManager__chatActionsHandler = _ChatActionsHandler()

    
    def start(self):
        for (fxManager, _) in self._AuxiliaryFxManager__fxManagers:
            fxManager.start()
        

    
    def destroy(self):
        for (fxManager, _) in self._AuxiliaryFxManager__fxManagers:
            fxManager.destroy()
        
        self._AuxiliaryFxManager__fxManagers = None
        self._AuxiliaryFxManager__chatActionsHandler.destroy()
        self._AuxiliaryFxManager__chatActionsHandler = None

    
    def createFxController(self, vehicle):
        controllers = []
        for (fxManager, FxCtrl) in self._AuxiliaryFxManager__fxManagers:
            controllers.append(FxCtrl(vehicle, fxManager))
        
        return AuxiliaryFxController(controllers)

    
    def execEffect(self, effectName):
        for (fxManager, _) in self._AuxiliaryFxManager__fxManagers:
            execEffect = getattr(fxManager, effectName, None)
            if execEffect is not None:
                execEffect()
                continue
        


from messenger.gui import MessengerDispatcher
from PlayerEvents import g_playerEvents
from ConnectionManager import connectionManager as g_connectionManager
import gui.SystemMessages as gui

class _ChatActionsHandler:
    
    def __init__(self):
        g_playerEvents.onAccountBecomePlayer += self._ChatActionsHandler__subscribe
        g_connectionManager.onDisconnected += self._ChatActionsHandler__onDisconnected

    
    def _ChatActionsHandler__subscribe(self):
        messengerDispatcher = MessengerDispatcher.g_instance
        messengerDispatcher.invites.onReceivedInviteListModified += self._ChatActionsHandler__onReceivedInviteListModified
        messengerDispatcher.invites.onReceivedInviteListInited += self._ChatActionsHandler__onReceivedInviteListModified
        messengerDispatcher.serviceChannel.onReceiveServerMessage += self._ChatActionsHandler__onSysMessage
        messengerDispatcher.serviceChannel.onReceiveClientMessage += self._ChatActionsHandler__onSysMessage
        messengerDispatcher.channels.onJoinedToChannel += self._ChatActionsHandler__onChatEnter

    
    def destroy(self):
        messengerDispatcher = MessengerDispatcher.g_instance
        messengerDispatcher.invites.onReceivedInviteListModified -= self._ChatActionsHandler__onReceivedInviteListModified
        messengerDispatcher.invites.onReceivedInviteListInited -= self._ChatActionsHandler__onReceivedInviteListModified
        messengerDispatcher.serviceChannel.onReceiveServerMessage -= self._ChatActionsHandler__onSysMessage
        messengerDispatcher.serviceChannel.onReceiveClientMessage -= self._ChatActionsHandler__onSysMessage
        messengerDispatcher.channels.onJoinedToChannel -= self._ChatActionsHandler__onChatEnter

    
    def _ChatActionsHandler__onDisconnected(self):
        g_instance.execEffect('resetBackground')

    
    def _ChatActionsHandler__onReceivedInviteListModified(self, *args):
        if MessengerDispatcher.g_instance.invites.getUnreadCount():
            g_instance.execEffect('startInvitationEffect')
        else:
            g_instance.execEffect('stopInvitationEffect')

    
    def _ChatActionsHandler__onSysMessage(self, formatted, isPriority, notify, auxData):
        gameGreetingName = gui.SystemMessages.SM_TYPE.GameGreeting.name()
        if gameGreetingName not in auxData:
            g_instance.execEffect('systemMessageEffect')
        

    
    def _ChatActionsHandler__onChatEnter(self, channel):
        isCurrentPlayer = MessengerDispatcher.g_instance.users.isCurrentPlayer(channel.owner)
        if not isCurrentPlayer and channel.isPrivate:
            g_instance.execEffect('channelOpenedEffect')
        



