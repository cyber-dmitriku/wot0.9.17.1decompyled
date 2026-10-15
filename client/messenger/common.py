# Source Generated with Decompyle++
# File: common.pyc (Python 2.6)

from ChatManager import chatManager
from debug_utils import LOG_ERROR

class MessangerSubscriber(object):
    _responseHandlers = { }
    
    def subscribeAction(self, callback, action, cid = None):
        chatManager.subscribeChatAction(callback, action, cid)

    
    def unsubscribeAction(self, callback, action, cid = None):
        chatManager.unsubscribeChatAction(callback, action, cid)

    
    def unsubscribeActionByName(self, object, callbackName, action, cid = None):
        if hasattr(object, callbackName):
            callback = getattr(object, callbackName)
            chatManager.unsubscribeChatAction(callback, action, cid)
        

    
    def unsubcribeAllActions(self):
        chatManager.unsubcribeAllChatActions()

    
    def handleChatActionFailureEvent(self, actionResponse, chatAction):
        handler = self._responseHandlers.get(actionResponse)
        if handler is None:
            return False
        if hasattr(self, handler):
            return getattr(self, handler)(actionResponse, chatAction)
        LOG_ERROR('handleChatActionFailureEvent: response handler for response %s(%s) not registered' % (actionResponse, actionResponse.index()))
        return False



class MessengerGlobalStorage(object):
    __slots__ = ('attribute',)
    _MessengerGlobalStorage__storage = { }
    
    def __init__(self, attribute, defaultValue):
        self.attribute = attribute
        if not self._MessengerGlobalStorage__storage.has_key(attribute):
            self._MessengerGlobalStorage__storage[attribute] = defaultValue
        

    
    def __set__(self, _, value):
        self._MessengerGlobalStorage__storage[self.attribute] = value

    
    def __get__(self, instance, owner = None):
        if instance is None:
            return self
        return self._MessengerGlobalStorage__storage[self.attribute]

    
    def value(self):
        return self._MessengerGlobalStorage__storage[self.attribute]



