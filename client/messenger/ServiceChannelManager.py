# Source Generated with Decompyle++
# File: ServiceChannelManager.pyc (Python 2.6)

import BigWorld
from chat_shared import CHAT_ACTIONS
from collections import deque
from constants import IS_DEVELOPMENT
from debug_utils import *
from messenger import SCH_MSGS_MAX_LENGTH, SCH_CLIENT_FORMATTERS_DICT, SCH_SERVER_FORMATTERS_DICT, SCH_CLIENT_MSG_TYPE
from messenger.common import MessangerSubscriber
from messenger.wrappers import ServiceChannelMessage
import Event
from adisp import process, async

class ServiceChannelManager(MessangerSubscriber):
    _ServiceChannelManager__messages = deque([], SCH_MSGS_MAX_LENGTH)
    
    def __init__(self):
        MessangerSubscriber.__init__(self)
        self._ServiceChannelManager__unreadMessageCount = 0
        self.onReceiveServerMessage = Event.Event()
        self.onReceiveClientMessage = Event.Event()
        self._ServiceChannelManager__expirationShown = False

    
    def subscribeToActions(self):
        self.subscribeAction(self.onReceiveSysMessage, CHAT_ACTIONS.sysMessage)
        self.subscribeAction(self.onReceivePersonalSysMessage, CHAT_ACTIONS.personalSysMessage)

    
    def clear(self):
        self._ServiceChannelManager__messages.clear()
        self.onReceiveServerMessage.clear()
        self.onReceiveClientMessage.clear()

    
    def __addServerMessage(self, message):
        yield (lambda callback: callback(True))
        formatter = SCH_SERVER_FORMATTERS_DICT.get(message.type)
        if formatter:
            
            try:
                notify = formatter.notify()
                isAsync = formatter.isAsync()
                if isAsync:
                    yield formatter.format(message)
                    formatted = None
                else:
                    formatted = formatter.format(message)
                formatted.update({
                    'msgTypeId': message.type })
            except:
                LOG_CURRENT_EXCEPTION()
                return None

            if formatted:
                if message.isHighImportance:
                    pass
                priority = message.active
                self._ServiceChannelManager__messages.append((formatted, True, priority, notify, []))
                self._ServiceChannelManager__unreadMessageCount += 1
                if message.isHighImportance:
                    pass
                self.onReceiveServerMessage(formatted, message.active, notify, [])
            elif IS_DEVELOPMENT:
                LOG_WARNING('Not enough data to format. Action data : ', message)
            
        elif IS_DEVELOPMENT:
            LOG_WARNING('Formatter not found. Action data : ', message)
        

    _ServiceChannelManager__addServerMessage = process(__addServerMessage)
    
    def _ServiceChannelManager__addClientMessage(self, message, type, isPriority = False, auxData = None):
        if auxData is None:
            auxData = []
        
        formatter = SCH_CLIENT_FORMATTERS_DICT.get(type)
        if formatter:
            
            try:
                formatted = formatter.format(message, auxData)
                notify = formatter.notify()
            except:
                LOG_CURRENT_EXCEPTION()
                return None

            self._ServiceChannelManager__messages.append((formatted, False, isPriority, notify, auxData))
            self._ServiceChannelManager__unreadMessageCount += 1
            self.onReceiveClientMessage(formatted, isPriority, notify, auxData)
        elif IS_DEVELOPMENT:
            LOG_WARNING('Formatter not found:', type, message)
        

    
    def requestLastServiceMessages(self):
        BigWorld.player().requestLastSysMessages()

    
    def onReceiveSysMessage(self, chatAction):
        message = ServiceChannelMessage.fromChatAction(chatAction)
        self._ServiceChannelManager__addServerMessage(message)

    
    def onReceivePersonalSysMessage(self, chatAction):
        message = ServiceChannelMessage.fromChatAction(chatAction, personal = True)
        self._ServiceChannelManager__addServerMessage(message)

    
    def pushClientSysMessage(self, message, type, isPriority = False):
        self._ServiceChannelManager__addClientMessage(message, SCH_CLIENT_MSG_TYPE.SYS_MSG_TYPE, isPriority = isPriority, auxData = [
            type.name()])

    
    def pushClientMessage(self, message, type, isPriority = False, auxData = None):
        self._ServiceChannelManager__addClientMessage(message, type, isPriority = isPriority, auxData = auxData)

    
    def getServiceMessagesCount(self):
        return len(self._ServiceChannelManager__messages)

    
    def getServiceMessages(self):
        return map((lambda item: item[0]), self._ServiceChannelManager__messages)

    
    def fireReceiveMessageEvents(self):
        if not self._ServiceChannelManager__unreadMessageCount:
            return None
        unreadMessages = list(self._ServiceChannelManager__messages)[-(self._ServiceChannelManager__unreadMessageCount):]
        for (message, isServerMsg, flag, notify, auxData) in unreadMessages:
            if isServerMsg:
                pass
            1
            dispatchEvent = self.onReceiveClientMessage
            dispatchEvent(message, flag, notify, auxData)
        

    
    def resetUnreadCount(self):
        self._ServiceChannelManager__unreadMessageCount = 0



