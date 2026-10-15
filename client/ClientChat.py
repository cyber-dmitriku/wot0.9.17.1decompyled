# Source Generated with Decompyle++
# File: ClientChat.pyc (Python 2.6)

import cPickle
import zlib
import time
from collections import deque
from invites import INVITE_TYPES
import helpers.time_utils as tm
import BigWorld
import Event
import chat_shared
from debug_utils import LOG_CURRENT_EXCEPTION, LOG_RF, LOG_ERROR
from chat_shared import CHAT_RESPONSES, CHAT_ACTIONS, CHAT_COMMANDS, parseCommandMessage, ChatCommandError, isCommandMessage, buildChatActionData, ChatError, ChatCommandInCooldown, SYS_MESSAGE_TYPE
from ids_generators import SequenceIDGenerator
from messenger.gui import MessengerDispatcher
from constants import USER_SEARCH_MODE
g_replayCtrl = None

class ClientChat(object):
    _ClientChat__dataProcessors = [
        '_ClientChat__dataTimeProcessor',
        '_ClientChat__inviteDataTimeProcessor',
        '_ClientChat__systemMessageTimeProcessor']
    _ClientChat__actionHandlers = {
        CHAT_ACTIONS.receiveInvite.index(): '_ClientChat__onReceiveInvite' }
    
    def __init__(self):
        if not isinstance(self, BigWorld.Entity):
            raise AssertionError
        self._ClientChat__chatActionCallbacks = { }
        self._idGen = SequenceIDGenerator()

    
    def acquireRequestID(self):
        return self._idGen.next()

    
    def requestSystemChatChannels(self):
        self._ClientChat__baseChatCommand(CHAT_COMMANDS.requestSystemChatChannels)

    
    def findChatChannels(self, sample, requestID = None):
        if requestID is None:
            requestID = self.acquireRequestID()
        
        
        try:
            self._ClientChat__baseChatCommand(CHAT_COMMANDS.findChatChannels, stringArg1 = sample, ignoreCooldown = False, requestID = requestID)
        except ChatError:
            ex = None
            self._processChatError(CHAT_ACTIONS.requestChannels, 0, ex, requestID = requestID)


    
    def getChannelInfoById(self, channelId):
        self._ClientChat__baseChatCommand(CHAT_COMMANDS.getChannelInfoById, int64Arg = channelId)

    
    def requestChatChannelMembers(self, channelId):
        self._ClientChat__baseChannelChatCommand(channelId, CHAT_COMMANDS.requestChatChannelMembers)

    
    def requestChatChannelMembersCount(self, channelId):
        self._ClientChat__baseChannelChatCommand(channelId, CHAT_COMMANDS.getMembersCount)

    
    def createChatChannel(self, channelName, password = None):
        
        try:
            if password is not None:
                pass
            1
            CHAT_COMMANDS.createChatChannel('stringArg1', channelName = 'stringArg2', password = '', ignoreCooldown = False)
        except ChatError:
            ex = None
            self._processChatError(CHAT_COMMANDS.createChatChannel, 0, ex)


    
    def destroyChatChannel(self, channelId):
        self._ClientChat__baseChannelChatCommand(channelId, CHAT_COMMANDS.destroyChatChannel)

    
    def enterChat(self, channelId, password = None):
        if password is not None:
            pass
        1
        channelId(CHAT_COMMANDS.enterChatChannel, 'stringArg1', password = '')

    
    def broadcast(self, channelId, message):
        if not len(message) or message.isspace():
            return None
        message = message.rstrip()
        if not isCommandMessage(message):
            
            try:
                self._ClientChat__baseChannelChatCommand(channelId, CHAT_COMMANDS.broadcast, stringArg1 = message, ignoreCooldown = False)
            except ChatError:
                message.isspace()
                ex = None
                self._processChatError(CHAT_ACTIONS.broadcast, channelId, ex)
            

        
        try:
            (command, int64Arg, int16Arg, stringArg1, stringArg2) = parseCommandMessage(message)
            self._ClientChat__baseChannelChatCommand(channelId, command, int64Arg, int16Arg, stringArg1, stringArg2, ignoreCooldown = False)
        except ChatCommandError:
            message.isspace()
            ex = None
            self._processChatError(CHAT_ACTIONS.userChatCommand, channelId, ex)
        except:
            message.isspace()


    
    def leaveChat(self, channelId):
        self._ClientChat__baseChannelChatCommand(channelId, CHAT_COMMANDS.leaveChatChannel)

    
    def onChatActionFailure(self, actionData):
        MessengerDispatcher.g_instance.onChatActionFailure(actionData)

    
    def onChatAction(self, chatActionData):
        global g_replayCtrl
        if g_replayCtrl is None:
            import BattleReplay as BattleReplay
            g_replayCtrl = BattleReplay.g_replayCtrl
        
        if g_replayCtrl.isRecording:
            g_replayCtrl.cancelSaveCurrMessage()
        
        for processor in self._ClientChat__dataProcessors:
            getattr(self, processor)(chatActionData)
        
        if CHAT_RESPONSES[chatActionData['actionResponse']] != CHAT_RESPONSES.success:
            self.onChatActionFailure(chatActionData)
        else:
            hanlerName = self._ClientChat__actionHandlers.get(chatActionData['action'], None)
            if hanlerName:
                getattr(self, hanlerName)(chatActionData)
            
            chId = chatActionData['channel']
            commonCallbacks = self._ClientChat__getChatActionCallbacks(CHAT_ACTIONS[chatActionData['action']], 0)
            commonCallbacks(chatActionData)
            if chId != 0:
                channelCallbacks = self._ClientChat__getChatActionCallbacks(CHAT_ACTIONS[chatActionData['action']], chId)
                channelCallbacks(chatActionData)
            

    
    def requestLastSysMessages(self):
        self._ClientChat__baseChatCommand(CHAT_COMMANDS.requestLastSysMessages)

    
    def findUsers(self, userNamePattern, onlineMode = None, requestID = None):
        if onlineMode is None:
            searchMode = USER_SEARCH_MODE.ALL
        elif onlineMode:
            searchMode = USER_SEARCH_MODE.ONLINE
        else:
            searchMode = USER_SEARCH_MODE.OFFLINE
        self._ClientChat__baseChatCommand(CHAT_COMMANDS.findUser, int16Arg = searchMode, stringArg1 = userNamePattern, requestID = requestID)

    
    def requestUsersRoster(self, flags = 0):
        self._ClientChat__baseChatCommand(CHAT_COMMANDS.requestUsersRoster, int16Arg = flags)

    
    def logVivoxLogin(self):
        self._ClientChat__baseChatCommand(CHAT_COMMANDS.logVivoxLogin)

    
    def requestFriendStatus(self, friendID = -1):
        self._ClientChat__baseChatCommand(CHAT_COMMANDS.requestFriendStatus, int64Arg = friendID)

    
    def addFriend(self, friendID, friendName):
        self._ClientChat__baseChatCommand(CHAT_COMMANDS.addFriend, int64Arg = friendID, stringArg1 = friendName)

    
    def createPrivate(self, friendID, friendName):
        self._ClientChat__baseChatCommand(CHAT_COMMANDS.createPrivate, int64Arg = friendID, stringArg1 = friendName)

    
    def removeFriend(self, friendID):
        self._ClientChat__baseChatCommand(CHAT_COMMANDS.removeFriend, int64Arg = friendID)

    
    def addIgnored(self, ignoredID, ignoredName):
        self._ClientChat__baseChatCommand(CHAT_COMMANDS.addIgnored, int64Arg = ignoredID, stringArg1 = ignoredName)

    
    def removeIgnored(self, ignoredID):
        self._ClientChat__baseChatCommand(CHAT_COMMANDS.removeIgnored, int64Arg = ignoredID)

    
    def setMuted(self, mutedID, mutedName):
        self._ClientChat__baseChatCommand(CHAT_COMMANDS.setMuted, int64Arg = mutedID, stringArg1 = mutedName)

    
    def unsetMuted(self, mutedID):
        self._ClientChat__baseChatCommand(CHAT_COMMANDS.unsetMuted, int64Arg = mutedID)

    
    def createPrebattleInvite(self, receiverName, auxText, prebattleID, prebattleType, requestID = None):
        self._ClientChat__baseInviteCommand(CHAT_COMMANDS.createInvite, INVITE_TYPES.PREBATTLE, receiverName, prebattleID, prebattleType, stringArg2 = auxText, requestID = requestID)

    
    def createBarterInvite(self, receiverName, auxText, itemID, requestID = None):
        self._ClientChat__baseInviteCommand(CHAT_COMMANDS.createInvite, INVITE_TYPES.BARTER, receiverName, itemID, stringArg2 = auxText, requestID = requestID)

    
    def acceptPrebattleInvite(self, invi
