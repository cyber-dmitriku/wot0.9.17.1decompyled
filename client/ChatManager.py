# Source Generated with Decompyle++
# File: ChatManager.pyc (Python 2.6)

from chat_shared import CHAT_ACTIONS, CHAT_CHANNEL_BATTLE, CHAT_CHANNEL_BATTLE_TEAM
import Event
from Singleton import Singleton

class ChatManager(Singleton):
    
    def instance():
        return ChatManager()

    instance = staticmethod(instance)
    
    def _singleton_init(self):
        self.battleTeamChannelID = 0
        self.battleCommonChannelID = 0
        self.playerProxy = None
        self._ChatManager__chatActionCallbacks = { }

    
    def subscribeChatAction(self, callback, action, channelId = None):
        cbs = self._ChatManager__getChatActionCallbacks(action, channelId)
        cbs += callback

    
    def unsubscribeChatAction(self, callback, action, channelId = None):
        cbs = self._ChatManager__getChatActionCallbacks(action, channelId)
        cbs -= callback

    
    def unsubcribeAllChatActions(self):
        for handlers in self._ChatManager__chatActionCallbacks.values():
            handlers.clear()
        

    
    def _ChatManager__getChatActionCallbacks(self, action, channelId):
        if channelId is not None:
            pass
        1
        channelId = 0
        key = (action, channelId)
        if key not in self._ChatManager__chatActionCallbacks:
            handlers = Event.Event()
            self._ChatManager__chatActionCallbacks[key] = Event.Event()
        else:
            handlers = self._ChatManager__chatActionCallbacks[key]
        return handlers

    
    def switchPlayerProxy(self, proxy):
        self._ChatManager__cleanupMyCallbacks()
        self._ChatManager__setProxyChatActionsCallbacks({ })
        self.playerProxy = proxy
        self._ChatManager__setProxyChatActionsCallbacks(self._ChatManager__chatActionCallbacks)
        self._ChatManager__setupMyCallbacks()

    
    def _ChatManager__setProxyChatActionsCallbacks(self, callbacks):
        if self.playerProxy is not None:
            self.playerProxy.setChatActionsCallbacks(callbacks)
        

    
    def _ChatManager__cleanupMyCallbacks(self):
        if self.playerProxy is not None:
            self.battleTeamChannelID = 0
            self.battleCommonChannelID = 0
            self.playerProxy.unsubscribeChatAction(self._ChatManager__onChannelsListReceived, CHAT_ACTIONS.requestChannels)
        

    
    def _ChatManager__setupMyCallbacks(self):
        if self.playerProxy is not None:
            self.playerProxy.subscribeChatAction(self._ChatManager__onChannelsListReceived, CHAT_ACTIONS.requestChannels)
        

    
    def _ChatManager__onChannelsListReceived(self, chatActionData):
        for chInfo in chatActionData['data']:
            flags = chInfo.get('flags', 0)
            if flags & CHAT_CHANNEL_BATTLE == CHAT_CHANNEL_BATTLE:
                if flags & CHAT_CHANNEL_BATTLE_TEAM == CHAT_CHANNEL_BATTLE_TEAM:
                    self.battleTeamChannelID = chInfo.get('id', 0)
                else:
                    self.battleCommonChannelID = chInfo.get('id', 0)
            flags & CHAT_CHANNEL_BATTLE_TEAM == CHAT_CHANNEL_BATTLE_TEAM
        


chatManager = ChatManager.instance()

