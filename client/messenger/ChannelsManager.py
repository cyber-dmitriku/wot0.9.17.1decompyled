# Source Generated with Decompyle++
# File: ChannelsManager.pyc (Python 2.6)

import constants
import BigWorld
from chat_shared import CHAT_ACTIONS, CHAT_RESPONSES
from collections import defaultdict, deque
from debug_utils import LOG_DEBUG
from messenger import VISIBLE_MESSAGE_MAX_LENGTH
from messenger.common import MessangerSubscriber
from messenger.exeptions import ChannelNotFound
from messenger.wrappers import ChatActionWrapper, ChannelWrapper, MemberWrapper
import Event
import time

def _messageDequeFactory():
    return deque([], VISIBLE_MESSAGE_MAX_LENGTH)


def _channelFactory():
    return ChannelWrapper()


def _memberFactory():
    return []


class CREATE_CHANNEL_RESULT(object):
    (doRequest, activeChannelLimitReached) = range(2)


class ChannelsManager(MessangerSubscriber):
    _ChannelsManager__channelMap = defaultdict(_channelFactory)
    _ChannelsManager__channelMessages = defaultdict(_messageDequeFactory)
    _ChannelsManager__memberMap = defaultdict(_memberFactory)
    _ChannelsManager__creationChannelInfo = { }
    
    def __init__(self):
        MessangerSubscriber.__init__(self)
        self._ChannelsManager__eventManager = Event.EventManager()
        self.onRequestChannelsComplete = Event.Event(self._ChannelsManager__eventManager)
        self.onFindChannelsFailed = Event.Event(self._ChannelsManager__eventManager)
        self.onConnectingToSecureChannel = Event.Event(self._ChannelsManager__eventManager)
        self.onChannelRefresh = Event.Event(self._ChannelsManager__eventManager)
        self.onReceiveLazyChannels = Event.Event(self._ChannelsManager__eventManager)
        self.onJoinedToChannel = Event.Event(self._ChannelsManager__eventManager)
        self._responseHandlers = {
            CHAT_RESPONSES.commandInCooldown: '_ChannelsManager__onCommandInCooldown' }

    
    def subscribeToActions(self):
        self.subscribeAction(self.onRequestChannels, CHAT_ACTIONS.requestChannels)
        self.subscribeAction(self.onRequestChannelMembers, CHAT_ACTIONS.requestMembers)
        self.subscribeAction(self.onChannelInfoUpdated, CHAT_ACTIONS.channelInfoUpdated)
        self.subscribeAction(self.onChatChannelCreated, CHAT_ACTIONS.createChannel)

    
    def requestSystemChannels(self):
        '''
\t\tRequest system channels from server.
\t\tTo process the response through subscribing
\t\tBigWorld.player().subscribeChatAction
\t\t'''
        self.subscribeAction(self.onRequestSystemChannels, CHAT_ACTIONS.requestChannels)
        BigWorld.player().requestSystemChatChannels()

    
    def joinToSystemChannels(self):
        '''
\t\tRequest system channels from server and join to received channels.
\t\tTo process the response through subscribing
\t\tBigWorld.player().subscribeChatAction
\t\t'''
        self.subscribeAction(self.onRequestSystemChannelsForJoin, CHAT_ACTIONS.requestChannels)
        BigWorld.player().requestSystemChatChannels()

    
    def requestChannelMembers(self, cid):
        '''
\t\tRequest to the server about the members of this channel.
\t\t@param cid: channel id
\t\t'''
        BigWorld.player().requestChatChannelMembers(cid)

    
    def joinToChannel(self, cid, password = None, selected = False):
        """
\t\tRequest to the server on the current player's accession to the channel.
\t\t@param cid: channel id
\t\t@param password: channel password
\t\t@param selected: is activate channel tab
\t\t"""
        channel = self.getChannel(cid)
        if not channel:
            raise ChannelNotFound(cid)
        channel.selected = selected
        if channel.joined:
            return None
        if channel and channel.isSecured and not password:
            self.onConnectingToSecureChannel(channel)
            return None
        BigWorld.player().enterChat(cid, password)

    
    def exitFromChannel(self, cid):
        '''
\t\tRequest to the server on the current player leave channel.
\t\t@param cid: channel id
\t\t'''
        BigWorld.player().leaveChat(cid)

    
    def createChannel(self, name, password = None):
        '''
\t\tRequest to the server creating channel with name and
\t\tpassword (optional, need for secure channels).
\t\t@param name: channel name
\t\t@param password: channel password
\t\t'''
        if self.isActiveChannelLimitReached():
            return CREATE_CHANNEL_RESULT.activeChannelLimitReached
        if name.startswith('#'):
            name = name[1:]
        
        if password:
            self._ChannelsManager__creationChannelInfo[name] = password
        
        BigWorld.player().createChatChannel(name, password)
        return CREATE_CHANNEL_RESULT.doRequest

    
    def findChannels(self, token, requestID = None):
        '''
\t\tSearch on a server channels by token.
\t\tNote: to be excluded channels in which the player is already connected.
\t\t@param token: word which is searched in name of channels
\t\t@param requestID: unique id to search request
\t\t'''
        BigWorld.player().findChatChannels(token, requestID = requestID)

    
    def onRequestChannels(self, chatAction, isSystem = False, join = False, selected = False):
        chatActionDict = dict(chatAction)
        data = chatActionDict.get('data', [])
        requestID = chatActionDict.get('requestID', [])
        channels = set()
        lazy = set()
        for channelData in data:
            channel = ChannelWrapper(**None)
            channels.add(channel)
            cid = channel.cid
            if channel.lazy:
                channel.hidden = self._ChannelsManager__hiddenAttrForLazyChannels.get(channel.lazy, False)
                lazy.add(channel)
            
            self._ChannelsManager__channelMap[cid] = self._ChannelsManager__channelMap[cid].update(channel)
            if join:
                self.joinToChannel(cid, selected = selected)
                continue
        
        self.onRequestChannelsComplete(requestID, channels)
        if len(lazy) > 0:
            self.onReceiveLazyChannels(lazy)
        

    
    def onRequestSystemChannels(self, chatAction):
        self.onRequestChannels(chatAction, isSystem = True)
        self.unsubscribeActionByName(self, 'onRequestSystemChannels', CHAT_ACTIONS.requestChannels)

    
    def onRequestSystemChannelsForJoin(self, chatAction):
        self.onRequestChannels(chatAction, isSystem = True, join = True, selected = True)
        self.unsubscribeActionByName(self, 'onRequestSystemChannelsForJoin', CHAT_ACTIONS.requestChannels)

    
    def onRequestPrebattleChannelForJoin(self, chatAction):
        self.onRequestChannels(chatAction, isSystem = True, join = True, selected = True)
        self.unsubscribeActionByName(self, 'onRequestPrebattleChannelForJoin', CHAT_ACTIONS.requestChannels)

    
    def onRequestChannelMembers(self, chatAction):
        wrapper = ChatActionWrapper(**None)
        cid = wrapper.channel
        for memberData in wrapper.data:
            member = MemberWrapper(**None)
            if member not in self._ChannelsManager__memberMap[cid]:
                self._ChannelsManager__memberMap[cid].append(member)
                continue
        

    
    def onChannelInfoUpdated(self, chatAction):
        if chatAction.has_key('data'):
            pass
        1
        result = { }
        channel = ChannelWrapper(**None)
        cid = channel.cid
        self._ChannelsManager__channelMap[cid] = self._ChannelsManager__channelMap[cid].update(channel)
        self.onChannelRefresh(self._ChannelsManager__channelMap[cid])

    
    def onChatChannelCreated(self, chatAction):
        '''
\t\tEvent handler. Channel is created.
\t\t'''
        if chatAction.has_key('data'):
            pass
        1
        result = { }
        channel = ChannelWrapper(**None)
        cid = channel.cid
        self._ChannelsManager__channelMap[cid] = self._ChannelsManager__channelMap[cid].update(channel)
        password = None
        if self._ChannelsManager__creationChannelInfo.has_key(channel.channelName):
            password = self._ChannelsManager__creationChannelInfo.pop(channel.channelName)
        
        self.joinToChannel(cid, password = password, selected = True)

    
    def _ChannelsManager__onCommandInCooldown(self, actionResponse, chatAction):
        data = chatAction.get('data', {
            'command': None,
            'cooldownPeriod': -1 })
        result = False
        if data['command'] == 'findChatChannels':
            result = True
            self.onFindChannelsFailed(chatAction.get('requestID', -1), actionResponse, data)
        
        return result

    
    def updateChannelWrappers(self):
        channels = self.getChannelList()
        for channel in channels:
            cid = channel.cid
            updatedChannel = ChannelWrapper(id = cid, owner = channel.owner, **None)
            self._ChannelsManager__channelMap[cid] = channel.update(updatedChannel)
            self.onChannelRefresh(self._ChannelsManager__channelMap[cid])
        

    
    def addChannelMessage(self, cid, message):
        self._ChannelsManager__channelMessages[cid].append(message)

    
    def getChannelMessages(self, cid):
        return self._ChannelsManager__channelMessages[cid]

    
    def getChannelList(self, joined = True, lazy = False, isBattle = False):
        return (None, None, filter)((lambda channel: if (channel.joined == joined or lazy is True) and channel.lazy != 0 and not (channel.hidden):
passchannel.isBattle == isBattle), self._ChannelsManager__channelMap.values())

    
    def getLazyChannelList(self, joined = None):
        return (filter,)((lambda channel: if not channel.lazy != 0 and joined is None:
passchannel.joined == joined), self._ChannelsManager__channelMap.values())

    
    def getPrebattleChannelList(self):
        return filter((lambda channel: if channel.isPrebattle:
passnot (channel.waitingDestroyedEvent)), self._ChannelsManager__channelMap.values())

    
    def getSquadChannel(self):
        result = filter((lambda channel: if channel.isSquad:
passnot (channel.waitingDestroyedEvent)), self._ChannelsManager__channelMap.values())
        if len(result):
            return result[0]

    
    def getWaitinigToDestroyChannelList(self):
        return filter((lambda channel: channel.waitingDestroyedEvent), self._ChannelsManager__channelMap.values())

    
    def getChannelCount(self, joined = True, isBattle = False):
        return len(self.getChannelList(joined = joined, isBattle = isBattle))

    
    def _addChannel(self, channel):
        old = self._ChannelsManager__channelMap[channel.cid]
        self._ChannelsManager__channelMap[channel.cid] = old._replace(**None)

    
    def _removeChannel(self, cid, clearChannelInfo = True, waitingDestroyedEvent = False):
        if not clearChannelInfo:
            pass
        forceClearChannelInfo = self.isBattle(cid)
        if forceClearChannelInfo:
            if self._ChannelsManager__channelMap.has_key(cid):
                self._ChannelsManager__channelMap.pop(cid)
            
        else:
            self._setJoinedFlag(cid, False)
            self._ChannelsManager__channelMap[cid].waitingDestroyedEvent = waitingDestroyedEvent
        if self._ChannelsManager__memberMap.has_key(cid):
            self._ChannelsManager__memberMap.pop(cid)
        
        if self._ChannelsManager__channelMessages.has_key(cid):
            self._ChannelsManager__channelMessages.pop(cid)
        

    
    def _setJoinedFlag(self, cid, flag):
        self._ChannelsManager__channelMap[cid].joined = flag
        if flag:
            self._ChannelsManager__channelMap[cid].joinedTime = time.time()
        
        self._ChannelsManager__channelMessages[cid].clear()

    
    def getMemberCount(self, cid):
        return len(self._ChannelsManager__memberMap[cid])

    
    def getMemberList(self, cid):
        return self._ChannelsManager__memberMap[cid]

    
    def hasExistMember(self, cid, uid):
        return MemberWrapper(id = uid) in self._ChannelsManager__memberMap[cid]

    
    def _addMember(self, cid, member):
        if member not in self._ChannelsManager__memberMap[cid]:
            self._ChannelsManager__memberMap[cid].append(member)
        

    
    def _addMembers(self, cid, members):
        filtered = (None, filter)((lambda member: member not in self._ChannelsManager__memberMap[cid]), members)
        if len(filtered) > 0:
            self._ChannelsManager__memberMap[cid].extend(filtered)
            return True
        return False

    
    def _removeMemeber(self, cid, uid):
        member = MemberWrapper(id = uid)
        if member in self._ChannelsManager__memberMap[cid]:
            self._ChannelsManager__memberMap[cid].remove(member)
            return True
        return False

    
    def _removeMembers(self, cid, members):
        filtered = (None, filter)((lambda member: member in self._ChannelsManager__memberMap[cid]), members)
        if len(filtered) > 0:
            for member in filtered:
                self._ChannelsManager__memberMap[cid].remove(member)
            
            return True
        return False

    
    def _setMemberStatus(self, cid, uid, status):
        if not self._ChannelsManager__memberMap.has_key(cid):
            return None
        member = MemberWrapper(id = uid)
        if member in self._ChannelsManager__memberMap[cid]:
            index = self._ChannelsManager__memberMap[cid].index(member)
            self._ChannelsManager__memberMap[cid][index].status = status
        

    
    def getNickName(self, cid, uid):
        member = MemberWrapper(id = uid)
        if member in self._ChannelsManager__memberMap[cid]:
            index = self._ChannelsManager__memberMap[cid].index(member)
            return self._ChannelsManager__memberMap[cid][index].nickName
        return 'Unknown'

    
    def getChannel(self, cid):
        if cid in self._ChannelsManager__channelMap:
            return self._ChannelsManager__channelMap[cid]

    
    def isActiveChannelLimitReached(self):
        return constants.USER_ACTIVE_CHANNELS_LIMIT < len(self.getChannelList())

    
    def clear(self):
        self._ChannelsManager__channelMap.clear()
        self._ChannelsManager__memberMap.clear()
        self._ChannelsManager__channelMessages.clear()
        self._ChannelsManager__creationChannelInfo.clear()
        self._ChannelsManager__eventManager.clear()

    
    def isReadOnly(self, cid):
        return self._ChannelsManager__channelMap[cid].isReadOnly

    
    def isSystem(self, cid):
        return self._ChannelsManager__channelMap[cid].isSystem

    
    def isBattle(self, cid):
        return self._ChannelsManager__channelMap[cid].isBattle

    
    def isLazyChannel(self, cid):
        return self._ChannelsManager__channelMap[cid].lazy

    
    def proxyToBattle(self, cid):
        return self._ChannelsManager__channelMap[cid].isSquad

    _ChannelsManager__hiddenAttrForLazyChannels = { }
    
    def getLazyChannelIdByClientIdx(self, clientIdx):
        for channel in self._ChannelsManager__channelMap.itervalues():
            if channel.lazy == clientIdx:
                return channel.cid
        

    
    def exitFromAllLazyChannels(self):
        for channel in self.getLazyChannelList(joined = True):
            self.exitFromChannel(channel.cid)
        

    
    def setIsLazyChannelHidden(self, clientIdx, flag):
        result = None
        self._ChannelsManager__hiddenAttrForLazyChannels[clientIdx] = flag
        for channel in self._ChannelsManager__channelMap.itervalues():
            if channel.lazy == clientIdx:
                if channel.hidden != flag:
                    channel.hidden = flag
                    result = channel.cid
                
                break
                continue
        
        return result



