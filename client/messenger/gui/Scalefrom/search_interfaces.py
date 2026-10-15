# Source Generated with Decompyle++
# File: search_interfaces.pyc (Python 2.6)

import BigWorld
from constants import CHANNEL_SEARCH_RESULTS_LIMIT, USER_SEARCH_RESULTS_LIMIT
from debug_utils import LOG_DEBUG
from external_strings_utils import _ACCOUNT_NAME_MIN_LENGTH, _ACCOUNT_NAME_MAX_LENGTH, isAccountNameValid
from helpers import i18n
from gui import SystemMessages
from gui.Scaleform.CommandArgsParser import CommandArgsParser
from messenger import g_settings, MESSENGER_I18N_FILE, getOperationInCooldownMsg
from messenger.gui.interfaces import DispatcherProxyHolder
import chat_shared

class SearchInterface(DispatcherProxyHolder):
    
    def __init__(self, commandPrefix):
        self._SearchInterface__movieViewHandler = None
        self._SearchInterface__commandPrefix = commandPrefix
        self._SearchInterface__refreshListCommand = '%s.RefreshList' % commandPrefix
        self._SearchInterface__findFailedCommand = '%s.FindFailed' % commandPrefix
        self._SearchInterface__searchCache = []
        self._SearchInterface__searchRequiestID = None

    
    def __del__(self):
        LOG_DEBUG('Deleted: SearchInterface')

    
    def populateUI(self, movieViewHandler):
        self._SearchInterface__movieViewHandler = movieViewHandler
        self._SearchInterface__movieViewHandler.addExternalCallbacks({
            '%s.SearchToken' % self._SearchInterface__commandPrefix: self.onSearchToken,
            '%s.RequestItemAt' % self._SearchInterface__commandPrefix: self.onSearchResultRequestItemAt,
            '%s.RequestItemRange' % self._SearchInterface__commandPrefix: self.onSearchResultRequestItemRange,
            '%s.RequestSearchLimitLabel' % self._SearchInterface__commandPrefix: self.onRequestSearchLimitLabel })

    
    def dispossessUI(self):
        self._SearchInterface__movieViewHandler.removeExternalCallbacks('%s.SearchToken' % self._SearchInterface__commandPrefix, '%s.RequestItemAt' % self._SearchInterface__commandPrefix, '%s.RequestItemRange' % self._SearchInterface__commandPrefix, '%s.RequestSearchLimitLabel' % self._SearchInterface__commandPrefix)
        self._SearchInterface__movieViewHandler = None
        self._SearchInterface__searchProcessor = None
        self._SearchInterface__searchCache = []
        self._SearchInterface__searchRequiestID = None

    
    def processor(self):
        return self._SearchInterface__searchProcessor

    processor = property(processor)
    
    def handler(self):
        return self._SearchInterface__movieViewHandler

    handler = property(handler)
    
    def prefix(self):
        return self._SearchInterface__commandPrefix

    prefix = property(prefix)
    
    def cache(self):
        return self._SearchInterface__searchCache

    cache = property(cache)
    
    def find(self, requestID, token):
        pass

    
    def parse(self, result):
        pass

    
    def parseFailedResponse(self, actionResponse, data):
        pass

    
    def _getSearchResultLimit(self):
        pass

    
    def refresh(self):
        self._SearchInterface__movieViewHandler.call(self._SearchInterface__refreshListCommand, [
            len(self._SearchInterface__searchCache)])

    
    def setErrorMessage(self, message, messageType = SystemMessages.SM_TYPE.Error):
        SystemMessages.pushMessage(message, type = messageType)
        self._SearchInterface__movieViewHandler.call(self._SearchInterface__findFailedCommand)

    
    def onSearchTokenFailed(self, requestID, actionResponse, data):
        if requestID == self._SearchInterface__searchRequiestID:
            self.parseFailedResponse(actionResponse, data)
        

    
    def onSearchTokenComplete(self, requestID, result):
        if requestID != self._SearchInterface__searchRequiestID:
            return None
        if not len(result):
            SystemMessages.pushI18nMessage('#messenger:client/information/emptySearchResult/message', type = SystemMessages.SM_TYPE.Warning)
        
        result = self.parse(result)
        self._SearchInterface__searchCache = result
        self._SearchInterface__movieViewHandler.call(self._SearchInterface__refreshListCommand, [
            len(result)])

    
    def onSearchToken(self, *args):
        parser = CommandArgsParser(self.onSearchToken.__name__, 1, [
            str])
        (token,) = parser.parse(*args)
        self._SearchInterface__searchRequiestID = BigWorld.player().acquireRequestID()
        self.find(self._SearchInterface__searchRequiestID, token)

    
    def onSearchResultRequestItemAt(self, *args):
        parser = CommandArgsParser(self.onSearchResultRequestItemAt.__name__, 1, [
            int])
        (index,) = parser.parse(*args)
        if len(self._SearchInterface__searchCache) > index:
            parser.addArgs(self._SearchInterface__searchCache[index], [
                long])
        
        self._SearchInterface__movieViewHandler.respond(parser.args())

    
    def onSearchResultRequestItemRange(self, *args):
        parser = CommandArgsParser(self.onSearchResultRequestItemRange.__name__, 2, [
            int,
            int])
        (startIndex, endIndex) = parser.parse(*args)
        list = self._SearchInterface__searchCache
        for item in list[startIndex:endIndex + 1]:
            parser.addArgs(item, [
                long])
        
        self._SearchInterface__movieViewHandler.respond(parser.args())

    
    def onRequestSearchLimitLabel(self, *args):
        parser = CommandArgsParser(self.onRequestSearchLimitLabel.__name__, 1, [
            str])
        (i18nKey,) = parser.parse(*args)
        limit = self._getSearchResultLimit()
        if limit is not None:
            pass
        1
        args = []
        parser.addArg(i18n.makeString(i18nKey, *args))
        self._SearchInterface__movieViewHandler.respond(parser.args())



class SearchChannelsInterface(SearchInterface):
    
    def __init__(self, prefix = 'Messenger.SearchChannels'):
        SearchInterface.__init__(self, prefix)

    
    def __del__(self):
        LOG_DEBUG('Deleted: SearchChannelsInterface')

    
    def processor(self):
        return self._dispatcherProxy.channels

    processor = property(processor)
    
    def populateUI(self, movieViewHandler):
        SearchInterface.populateUI(self, movieViewHandler)
        self.processor.onRequestChannelsComplete += self.onSearchTokenComplete
        self.processor.onFindChannelsFailed += self.onSearchTokenFailed
        self.handler.addExternalCallbacks({
            '%s.JoinToChannel' % self.prefix: self.onJoinToChannel })

    
    def dispossessUI(self):
        self.handler.removeExternalCallback('%s.JoinToChannel' % self.prefix)
        self.processor.onRequestChannelsComplete -= self.onSearchTokenComplete
        self.processor.onFindChannelsFailed -= self.onSearchTokenFailed
        SearchInterface.dispossessUI(self)

    
    def onJoinToChannel(self, *args):
        parser = CommandArgsParser(self.onJoinToChannel.__name__, 1, [
            int])
        (index,) = parser.parse(*args)
        channelData = self.cache[index]
        self.processor.joinToChannel(channelData.cid, '')

    
    def find(self, requestID, token):
        self.processor.findChannels(token, requestID = requestID)

    
    def parse(self, result):
        return sorted(result, cmp = self._SearchChannelsInterface__comparator)

    
    def parseFailedResponse(self, actionResponse, data):
        if actionResponse == chat_shared.CHAT_RESPONSES.commandInCooldown:
            message = getOperationInCooldownMsg('findChatChannels', data.get('cooldownPeriod', -1))
            self.setErrorMessage(message)
        

    
    def _getSearchResultLimit(self):
        return CHANNEL_SEARCH_RESULTS_LIMIT

    
    def _SearchChannelsInterface__comparator(self, channel, other):
        return cmp(channel.channelName.lower(), other.channelName.lower())



class SearchUsersInterface(SearchInterface):
    
    def __init__(self, prefix = 'Messenger.SearchUsers'):
        SearchInterface.__init__(self, prefix)
        self._onlineFlag = None

    
    def __del__(self):
        LOG_DEBUG('Deleted: SearchUsersInterface')

    
    def processor(self):
        return self._dispatcherProxy.users

    processor = property(processor)
    
    def populateUI(self, movieViewHandler):
        SearchInterface.populateUI(self, movieViewHandler)
        self.processor.onUsersRosterUpdate += self._SearchUsersInterface__onUsersRosterUpdate
        self.processor.onFindUsersComplete += self.onSearchTokenComplete
        self.processor.onFindUsersFailed += self.onSearchTokenFailed
        self.handler.addExternalCallbacks({
            '%s.AddToFriends' % self.prefix: self.onAddToFriends,
            '%s.AddToIgnored' % self.prefix: self.onAddToIgnored,
            '%s.SetOnlineFlag' % self.prefix: self.onSetOnlineFlag })

    
    def dispossessUI(self):
        self.handler.removeExternalCallbacks('%s.AddToFriends' % self.prefix, '%s.AddToIgnored' % self.prefix, '%s.SetOnlineFlag' % self.prefix)
        self.processor.onUsersRosterUpdate -= self._SearchUsersInterface__onUsersRosterUpdate
        self.processor.onFindUsersComplete -= self.onSearchTokenComplete
        self.processor.onFindUsersFailed -= self.onSearchTokenFailed
        SearchInterface.dispossessUI(self)

    
    def onAddToFriends(self, *args):
        parser = CommandArgsParser(self.onAddToFriends.__name__, 1, [
            int])
        (index,) = parser.parse(*args)
        userData = self.cache[index]
        self.processor.addFriend(userData[0], userData[1])

    
    def onAddToIgnored(self, *args):
        parser = CommandArgsParser(self.onAddToIgnored.__name__, 1, [
            int])
        (index,) = parser.parse(*args)
        userData = self.cache[index]
        self.processor.addIgnored(userData[0], userData[1])

    
    def onSetOnlineFlag(self, *args):
        parser = CommandArgsParser(self.onSetOnlineFlag.__name__, 1)
        (self._onlineFlag,) = parser.parse(*args)
        self.handler.respond(parser.args())

    
    def find(self, requestID, token):
        token = token.strip()
        if not len(token):
            message = i18n.makeString('#%s:client/warnning/emptyUserSearchToken/message' % MESSENGER_I18N_FILE)
            self.setErrorMessage(message)
            return None
        if not isAccountNameValid(token):
            message = i18n.makeString('#%s:client/warnning/invalidUserSearchToken/message' % MESSENGER_I18N_FILE, _ACCOUNT_NAME_MIN_LENGTH, _ACCOUNT_NAME_MAX_LENGTH)
            self.setErrorMessage(message)
            return None
        self.processor.findUsers(token, onlineMode = self._onlineFlag, requestID = requestID)

    
    def parse(self, result):
        result = sorted(result, cmp = self._SearchUsersInterface__comparator)
        continue
        return [ user.list() + g_settings.getLobbyUserCS(user.roster, himself = user.himself) for user in result ]

    
    def parseFailedResponse(self, actionResponse, data):
        if actionResponse == chat_shared.CHAT_RESPONSES.commandInCooldown:
            message = getOperationInCooldownMsg('findUsers', data.get('cooldownPeriod', -1))
            self.setErrorMessage(message)
        elif actionResponse == chat_shared.CHAT_RESPONSES.incorrectCharacter:
            message = i18n.makeString('#%s:client/warnning/invalidUserSearchToken/message' % MESSENGER_I18N_FILE, _ACCOUNT_NAME_MIN_LENGTH, _ACCOUNT_NAME_MAX_LENGTH)
            self.setErrorMessage(message)
        

    
    def _getSearchResultLimit(self):
        return USER_SEARCH_RESULTS_LIMIT

    
    def _SearchUsersInterface__comparator(self, user, other):
        return cmp(user.userName.lower(), other.userName.lower())

    
    def _SearchUsersInterface__onUsersRosterUpdate(self, action, user):
        '''
\t\tUpdate search cache when changes user roster list
\t\t'''
        for (idx, userData) in enumerate(self.cache):
            if userData[0] == user.uid:
                newData = user.list()
                newData[3] = userData[3]
                self.cache[idx] = newData + g_settings.getLobbyUserCS(user.roster, himself = user.himself)
                break
                continue
        
        self.refresh()



class PrebattleSearchUsersInterface(SearchUsersInterface):
    
    def __init__(self, prefix = 'Training.SearchUsers'):
        SearchUsersInterface.__init__(self, prefix)

    
    def __del__(self):
        LOG_DEBUG('Deleted: PrebattleSearchUsersInterface')

    
    def processor(self):
        return self._dispatcherProxy.users

    processor = property(processor)
    
    def populateUI(self, movieViewHandler):
        SearchUsersInterface.populateUI(self, movieViewHandler)
        self.handler.addExternalCallbacks({
            '%s.RequestAllItems' % self.prefix: self.onRequestAllItems })

    
    def dispossessUI(self):
        self.handler.removeExternalCallbacks('%s.RequestAllItems' % self.prefix)
        SearchUsersInterface.dispossessUI(self)

    
    def parse(self, result):
        result = sorted(result, cmp = self._PrebattleSearchUsersInterface__comparator)
        users = []
        for user in result:
            if not user.himself:
                users.append(user.list() + g_settings.getLobbyUserCS(user.roster, himself = user.himself))
                continue
        
        return users

    
    def _PrebattleSearchUsersInterface__comparator(self, user, other):
        return cmp(user.userName.lower(), other.userName.lower())

    
    def onRequestAllItems(self, *args):
        parser = CommandArgsParser(self.onRequestAllItems.__name__)
        parser.parse(*args)
        for item in self.cache:
            if not item[3]:
                continue
            
            parser.addArgs(item[:6], [
                int])
        
        self.handler.respond(parser.args())



