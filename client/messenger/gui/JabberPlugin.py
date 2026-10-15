# Source Generated with Decompyle++
# File: JabberPlugin.pyc (Python 2.6)

import BigWorld
from Jabber import Client
from adisp import process
from debug_utils import LOG_DEBUG
from functools import partial
from gui.Scaleform.utils.requesters import StatsRequester
from messenger.gui.interfaces import ProtocolPlugin
from messenger.wrappers import ChannelWrapper, MemberWrapper, ChatActionWrapper
from functools import partial

class JabberPlugin(ProtocolPlugin):
    _JabberPlugin__fakeChannel = ChannelWrapper()
    
    def __init__(self):
        self._JabberPlugin__client = Client.Client()
        self._JabberPlugin__mucEntities = { }

    
    def connect(self):
        settings = getattr(BigWorld.player(), 'serverSettings', { })
        host = settings.get('xmpp_host')
        port = settings.get('xmpp_port')
        if host is None or port is None:
            raise Exception, 'XMPP: Jabber: server host or port is not defined'
        port is None
        credentials = settings.get('xmpp_credentials', '')
        if credentials:
            self._JabberPlugin__processConnect((host, port), credentials)
        

    
    def _JabberPlugin__processConnect(self, host, credentials):
        self._JabberPlugin__client.eventConnected += self.onJabberConnected
        self._JabberPlugin__client.eventDisconnected += self.onJabberServerDisconnected
        h = (host[0].decode('utf-8'), host[1].decode('utf-8'))
        c = (BigWorld.player().name.decode('utf-8'), credentials.decode('utf-8'))
        self._JabberPlugin__client.connect(h, c)

    
    def disconnect(self):
        for entity in self._JabberPlugin__mucEntities.itervalues():
            entity.eventMessage -= self.onJabberMessage
            entity.eventUserOnline -= self.onJabberUserOnline
            entity.eventUserOffline -= self.onJabberUserOffline
        
        self._JabberPlugin__mucEntities.clear()
        self._JabberPlugin__client.eventConnected -= self.onJabberConnected
        self._JabberPlugin__client.eventDisconnected -= self.onJabberServerDisconnected
        self._JabberPlugin__client.disconnect()

    
    def broadcast(self, cid, message):
        result = False
        entity = self._JabberPlugin__mucEntities.get(cid)
        if entity is not None:
            entity.sendMessage(message.decode('utf-8'))
            result = True
        
        return result

    
    def onJabberServerDisconnected(self):
        settings = getattr(BigWorld.player(), 'serverSettings', { })
        credentials = (BigWorld.player().name.decode('utf-8'), settings.get('xmpp_credentials', '').decode('utf-8'))
        host = (settings.get('xmpp_host').decode('utf-8'), settings.get('xmpp_port').decode('utf-8'))
        BigWorld.callback(10, partial(self._JabberPlugin__client.connect, host, credentials))

    
    def __requestClanInfo(self):
        yield StatsRequester().getClanInfo()
        clanInfo = None
        if len(clanInfo) > 1 and clanInfo[1] is not None and len(clanInfo[1]) > 0:
            room = unicode(clanInfo[1].lower(), 'utf-8', errors = 'ignore')
            self._JabberPlugin__joinToClanConference(room)
        

    _JabberPlugin__requestClanInfo = process(__requestClanInfo)
    
    def _JabberPlugin__joinToClanConference(self, room):
        LOG_DEBUG('__joinToClanConference', room)
        self._JabberPlugin__fakeChannel = ChannelWrapper(id = hash(room), channelName = room, isSystem = True, flags = 0)
        self.channels._addChannel(self._JabberPlugin__fakeChannel)
        entity = self._JabberPlugin__client.joinConference(room, Client.Client.CLAN_CONFERENCE_NAME)
        self._JabberPlugin__receiveMUCEntity(entity)

    
    def _JabberPlugin__receiveMUCEntity(self, entity):
        cid = self._JabberPlugin__fakeChannel.cid
        self.channels._setJoinedFlag(cid, True)
        self._JabberPlugin__mucEntities[cid] = entity
        currentWindow = self._dispatcherProxy._getCurrent(cid)
        if currentWindow.addChannel(self._JabberPlugin__fakeChannel):
            if self._JabberPlugin__fakeChannel.greeting:
                self.channels.addChannelMessage(cid, self._JabberPlugin__fakeChannel.greeting)
            
        
        entity.eventMessage += self.onJabberMessage
        entity.eventUserOnline += self.onJabberUserOnline
        entity.eventUserOffline += self.onJabberUserOffline

    
    def _JabberPlugin__receiveUserOnline(self, nickName):
        cid = self._JabberPlugin__fakeChannel.cid
        uid = hash(nickName)
        if not self.channels.hasExistMember(cid, uid):
            member = MemberWrapper(id = uid, nickName = nickName)
            self.channels._addMember(cid, member)
            currentWindow = self._dispatcherProxy._getCurrent(cid)
            page = currentWindow.getChannelPage(cid)
            if page:
                page.addMember(member)
            
        

    
    def _JabberPlugin__receiveUserOffline(self, nickName):
        cid = self._JabberPlugin__fakeChannel.cid
        uid = hash(nickName)
        if self.channels._removeMemeber(cid, uid):
            currentWindow = self._dispatcherProxy._getCurrent(cid)
            page = currentWindow.getChannelPage(cid)
            if page:
                page.removeMember(uid)
            
        

    
    def _JabberPlugin__receiveMessage(self, nickName, message):
        cid = self._JabberPlugin__fakeChannel.cid
        uid = hash(nickName)
        wrapper = ChatActionWrapper(channel = cid, originator = uid, originatorNickName = nickName, data = message)
        currentWindow = self._dispatcherProxy._getCurrent(cid)
        self._dispatcherProxy._filterChain.chainIn(wrapper)
        messageText = currentWindow.addChannelMessage(wrapper)
        if messageText:
            self.channels.addChannelMessage(cid, messageText)
        

    
    def onJabberConnected(self):
        LOG_DEBUG('onJabberConnected')
        self._JabberPlugin__requestClanInfo()

    
    def onJabberMessage(self, nickName, message):
        LOG_DEBUG('onJabberMessage')
        self._JabberPlugin__receiveMessage(nickName, message)

    
    def onJabberUserOnline(self, nickName):
        LOG_DEBUG('onJabberUserOnline', nickName)
        self._JabberPlugin__receiveUserOnline(nickName)

    
    def onJabberUserOffline(self, userName):
        LOG_DEBUG('onJabberUserOffline', userName)
        self._JabberPlugin__receiveUserOffline(userName)



