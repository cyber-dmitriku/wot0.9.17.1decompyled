# Source Generated with Decompyle++
# File: filters.pyc (Python 2.6)

import BigWorld
from debug_utils import LOG_WARNING, LOG_DEBUG, LOG_CURRENT_EXCEPTION
from external_strings_utils import normalized_unicode_trim
from helpers import html
from messenger import g_olDictionary, g_dnDictionary, g_settings, MESSAGE_MAX_LENGTH, MESSAGE_MAX_LENGTH_IN_BATTLE, MESSAGE_FLOOD_COOLDOWN
from messenger.UsersManager import UsersManager
import weakref

class IncomingFilter(object):
    
    def filter(self, chatAction):
        pass



class ObsceneLanguageFilter(IncomingFilter):
    
    def __init__(self):
        super(ObsceneLanguageFilter, self).__init__()
        g_olDictionary.resetReplacementFunction()

    
    def filter(self, chatAction):
        text = chatAction.data
        if UsersManager.isCurrentPlayer(chatAction.originator):
            return text
        return g_olDictionary.searchAndReplace(text)



class ColoringObsceneLanguageFilter(IncomingFilter):
    
    def __init__(self, usersManager):
        super(ColoringObsceneLanguageFilter, self).__init__()
        self._ColoringObsceneLanguageFilter__usersManager = weakref.ref(usersManager)
        self._ColoringObsceneLanguageFilter__current = None
        self._ColoringObsceneLanguageFilter__msgFormat = g_settings.coloringForBadWordFormat
        (g_olDictionary.overrideReplacementFunction,)((lambda world: self._ColoringObsceneLanguageFilter__processBadWord(world)))

    
    def __del__(self):
        if self._ColoringObsceneLanguageFilter__usersManager() is not None:
            self._ColoringObsceneLanguageFilter__usersManager().resetBreakers()
        

    
    def _ColoringObsceneLanguageFilter__processBadWord(self, word):
        if self._ColoringObsceneLanguageFilter__current is not None and self._ColoringObsceneLanguageFilter__usersManager() is not None:
            self._ColoringObsceneLanguageFilter__usersManager().markAsBreaker(self._ColoringObsceneLanguageFilter__current.originator, True)
        
        return self._ColoringObsceneLanguageFilter__msgFormat % word

    
    def filter(self, chatAction):
        self._ColoringObsceneLanguageFilter__current = chatAction
        text = chatAction.data
        if self._ColoringObsceneLanguageFilter__usersManager() is not None:
            self._ColoringObsceneLanguageFilter__usersManager().markAsBreaker(chatAction.originator, False)
        
        if UsersManager.isCurrentPlayer(chatAction.originator):
            return text
        return g_olDictionary.searchAndReplace(text)



class SpamFilter(IncomingFilter):
    
    def __init__(self):
        super(SpamFilter, self).__init__()
        
        try:
            self._filter = BigWorld.WGSpamFilter()
            self._filter.removeSpam('')
        except AttributeError:
            LOG_CURRENT_EXCEPTION()
            
            class Dummy(object):
                
                def removeSpam(self, text):
                    return text


            self._filter = Dummy()


    
    def filter(self, chatAction):
        text = chatAction.data
        if UsersManager.isCurrentPlayer(chatAction.originator):
            return text
        return self._filter.removeSpam(text)



class FloodFilter(IncomingFilter):
    
    def __init__(self):
        super(FloodFilter, self).__init__()
        self._FloodFilter__history = { }

    
    def filter(self, chatAction):
        text = chatAction.data
        userId = chatAction.originator
        if UsersManager.isCurrentPlayer(userId):
            return text
        userHistory = self._FloodFilter__history.get(userId)
        if userHistory is None:
            userHistory = []
            self._FloodFilter__history[userId] = []
        
        currTime = BigWorld.time()
        recentCount = len(userHistory) + 1
        for (msgTime, msgText) in userHistory:
            if currTime - msgTime > MESSAGE_FLOOD_COOLDOWN:
                recentCount -= 1
                continue
            UsersManager.isCurrentPlayer(userId)
            if text == msgText:
                text = ''
               
