# Source Generated with Decompyle++
# File: ServiceChannelInterface.pyc (Python 2.6)

from messenger.gui.interfaces import DispatcherProxyHolder
from messenger.gui.Scalefrom import SCH_COMMANDS
from debug_utils import LOG_DEBUG

class ServiceChannelInterface(DispatcherProxyHolder):
    
    def __init__(self):
        self._ServiceChannelInterface__movieViewHandler = None

    
    def serviceChannelManager(self):
        return self._dispatcherProxy.serviceChannel

    serviceChannelManager = property(serviceChannelManager)
    
    def populateUI(self, movieViewHandler):
        self._ServiceChannelInterface__movieViewHandler = movieViewHandler
        self._ServiceChannelInterface__serviceChannelUI = self._ServiceChannelInterface__movieViewHandler.getMember('lobbyMessengerLoader.contentHolder.lobbyMessenger.serviceChannel')
        self._ServiceChannelInterface__serviceChannelUI.script = self
        self.serviceChannelManager.onReceiveServerMessage += self._ServiceChannelInterface__onReceiveServerMessage
        self.serviceChannelManager.onReceiveClientMessage += self._ServiceChannelInterface__onReceiveClientMessage
        self._ServiceChannelInterface__movieViewHandler.addExternalCallbacks({
            SCH_COMMANDS.RequestMessageHistory(): self.onRequestMessageHistory,
            SCH_COMMANDS.RequestUnreadMessages(): self.onRequestUnreadMessages,
            SCH_COMMANDS.ClearUnreadMessagesCount(): self.onClearUnreadMessagesCount })

    
    def dispossessUI(self):
        self.clear()
        self.serviceChannelManager.onReceiveServerMessage -= self._ServiceChannelInterface__onReceiveServerMessage
        self.serviceChannelManager.onReceiveClientMessage -= self._ServiceChannelInterface__onReceiveClientMessage
        self._ServiceChannelInterface__movieViewHandler.removeExternalCallbacks(SCH_COMMANDS.RequestMessageHistory(), SCH_COMMANDS.RequestUnreadMessages(), SCH_COMMANDS.ClearUnreadMessagesCount())
        self._ServiceChannelInterface__movieViewHandler = None
        self._ServiceChannelInterface__serviceChannelUI.script = None
        self._ServiceChannelInterface__serviceChannelUI = None

    
    def clear(self):
        if self._ServiceChannelInterface__serviceChannelUI:
            self._ServiceChannelInterface__serviceChannelUI.clearList(True)
        
        self.serviceChannelManager.resetUnreadCount()

    
    def onRequestMessageHistory(self):
        if self._ServiceChannelInterface__serviceChannelUI:
            self._ServiceChannelInterface__serviceChannelUI.page.buildMessageHistory(self.serviceChannelManager.getServiceMessages())
        

    
    def onRequestUnreadMessages(self, *args):
        self.serviceChannelManager.fireReceiveMessageEvents()

    
    def onClearUnreadMessagesCount(self, *args):
        self.serviceChannelManager.resetUnreadCount()

    
    def _ServiceChannelInterface__onReceiveServerMessage(self, message, isPriority, notify, auxData):
        if self._ServiceChannelInterface__serviceChannelUI:
            self._ServiceChannelInterface__serviceChannelUI.receiveMessage(message, isPriority, notify, auxData)
        

    
    def _ServiceChannelInterface__onReceiveClientMessage(self, message, isPriority, notify, auxData):
        if self._ServiceChannelInterface__serviceChannelUI:
            self._ServiceChannelInterface__serviceChannelUI.receiveMessage(message, isPriority, notify, auxData)
        



