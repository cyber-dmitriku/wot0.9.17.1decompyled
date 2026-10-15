# Source Generated with Decompyle++
# File: PrebattleInvitesManager.pyc (Python 2.6)

import BigWorld
from ConnectionManager import connectionManager
from PlayerEvents import g_playerEvents
from chat_shared import CHAT_RESPONSES
import constants
from debug_utils import LOG_ERROR, LOG_WARNING, LOG_DEBUG, deprecated
from external_strings_utils import truncate_utf8
from ids_generators import SequenceIDGenerator
from messenger import g_settings, invite_formatters, INVITE_COMMENT_MAX_LENGTH
from messenger.common import MessengerGlobalStorage
from messenger.wrappers import PrbInviteWrapper
import Event

class PrebattleInvitesManager(object):
    _cp_playerDbID = MessengerGlobalStorage('_playerDbId', -0x1L)
    _cp_clanInfo = MessengerGlobalStorage('_clanInfo', None)
    
    def __init__(self, usersManager):
        self._PrebattleInvitesManager__usersManager = usersManager
        self.formatter = invite_formatters.PrebattleInviteFormatter()
        self._IDGen = SequenceIDGenerator()
        self._IDMap = {
            'inviteIDs': { },
            'prbIDs': { } }
        self._PrebattleInvitesManager__receivedInvites = { }
        self._PrebattleInvitesManager__unreadInvitesCount = 0
        self._PrebattleInvitesManager__eventManager = Event.EventManager()
        self.onReceivedInviteListInited = Event.Event(self._PrebattleInvitesManager__eventManager)
        self.onReceivedInviteListModified = Event.Event(self._PrebattleInvitesManager__eventManager)

    
    def init(self):
        self._PrebattleInvitesManager__isUserRosterInited = False
        self._PrebattleInvitesManager__usersManager.onUsersRosterReceived += self._PrebattleInvitesManager__um_onUsersRosterReceived
        g_playerEvents.onPrebattleInvitesChanged += self._PrebattleInvitesManager__pe_onPrebattleInvitesChanged

    
    def clear(self):
        self._PrebattleInvitesManager__isUserRosterInited = False
        self._PrebattleInvitesManager__usersManager.onUsersRosterReceived -= self._PrebattleInvitesManager__um_onUsersRosterReceived
        g_playerEvents.onPrebattleInvitesChanged -= self._PrebattleInvitesManager__pe_onPrebattleInvitesChanged
        self._PrebattleInvitesManager__receivedInvites.clear()
        self._PrebattleInvitesManager__unreadInvitesCount = 0
        self._IDMap = {
            'inviteIDs': { },
            'prbIDs': { } }
        self._PrebattleInvitesManager__eventManager.clear()

    
    def sendInvites(self, accountsToInvite, comment):
        truncated = truncate_utf8(comment.strip(), INVITE_COMMENT_MAX_LENGTH)
        BigWorld.player().prb_sendInvites(accountsToInvite, truncated)

    
    def acceptInvite(self, inviteID):
        
        try:
            (prebattleID, peripheryID) = self._IDMap['inviteIDs'][inviteID]
        except KeyError:
            LOG_ERROR('Invite ID is invalid', inviteID, self._IDMap)
            return None

        BigWorld.player().prb_acceptInvite(prebattleID, peripheryID)
        if self._PrebattleInvitesManager__unreadInvitesCount > 0:
            self._PrebattleInvitesManager__unreadInvitesCount -= 1
        

    
    def declineInvite(self, inviteID):
        
        try:
            (prebattleID, peripheryID) = self._IDMap['inviteIDs'][inviteID]
        except KeyError:
            LOG_ERROR('Invite ID is invalid', inviteID, self._IDMap)
            return None

        BigWorld.player().prb_declineInvite(prebattleID, peripheryID)
        if self._PrebattleInvitesManager__unreadInvitesCount > 0:
            self._PrebattleInvitesManager__unreadInvitesCount -= 1
        

    
    def getInviteInfo(self, inviteID):
        
        try:
            (prebattleID, peripheryID) = self._IDMap['inviteIDs'][inviteID]
            return (prebattleID, peripheryID)
        except KeyError:
            return (0, 0)


    
    def _PrebattleInvitesManager__um_onUsersRosterReceived(self):
        if not self._PrebattleInvitesManager__isUserRosterInited:
            invitesData = getattr(BigWorld.player(), 'prebattleInvites', { })
            LOG_DEBUG('Users roster received, list of invites is available', invitesData)
            self._PrebattleInvitesManager__isUserRosterInited = True
            self._buildReceivedInviteList(invitesData)
            self.onReceivedInviteListInited()
        

    
    def _PrebattleInvitesManager__pe_onPrebattleInvitesChanged(self, diff):
        if not self._PrebattleInvitesManager__isUserRosterInited:
            LOG_DEBUG('Received invites ignored. Manager waits for client will receive a roster list')
            return None
        prbInvites = diff.get('prebattleInvites_r')
        if prbInvites is not None:
            self._buildReceivedInviteList(prbInvites)
        
        prbInvites = diff.get('prebattleInvites')
        if prbInvites is not None:
            self._PrebattleInvitesManager__updatePrebattleInvites(prbInvites)
        

    
    def _PrebattleInvitesManager__updatePrebattleInvites(self, prbInvites):
        receiver = BigWorld.player().name
        receiverDBID = self._cp_playerDbID
        receiverClanAbbrev = None
        if self._cp_clanInfo is not None and len(self._cp_clanInfo) > 0:
            receiverClanAbbrev = self._cp_clanInfo[1]
        
        added = []
        changed = []
        deleted = []
        modified = False
        for (prebattleID, peripheryID) in prbInvites.iteritems():
            data = None
            inviteID = self._makeInviteID(prebattleID, peripheryID)
            if data is None:
                if self._delInvite(inviteID):
                    modified = True
                    deleted.append(inviteID)
                    continue
                continue
            
            anotherPeriphery = connectionManager.peripheryID != peripheryID
            invite = PrbInviteWrapper(id = inviteID, receiver = receiver, receiverDBID = receiverDBID, receiverClanAbbrev = receiverClanAbbrev, peripheryID = peripheryID, anotherPeriphery = anotherPeriphery, **None)
            inList = inviteID in self._PrebattleInvitesManager__receivedInvites
            if not inList:
                if self._addInvite(invite):
                    modified = True
                    added.append(inviteID)
                
            self._addInvite(invite)
            if self._updateInvite(invite):
                modified = True
                changed.append(inviteID)
                continue
        
        if modified:
            self.onReceivedInviteListModified(added, changed, deleted)
        

    
    def handleChatActionFailureEvent(self, actionResponse, chatAction):
        if actionResponse in [
            CHAT_RESPONSES.inviteCommandError,
            CHAT_RESPONSES.inviteCreateError,
            CHAT_RESPONSES.inviteCreationNotAllowed]:
            return True
        return False

    
    def _makeInviteID(self, prebattleID, peripheryID):
        inviteID = self._IDMap['prbIDs'].get((prebattleID, peripheryID))
        if inviteID is None:
            inviteID = self._IDGen.next()
            self._IDMap['inviteIDs'][inviteID] = (prebattleID, peripheryID)
            self._IDMap['prbIDs'][(prebattleID, peripheryID)] = inviteID
        
        return inviteID

    
    def _addInvite(self, invite):
        if g_settings.userPreferences['invitesFromFriendsOnly']:
            user = self._PrebattleInvitesManager__usersManager.getUser(invite.creatorDBID, invite.creator)
            if not user.isFriend():
                LOG_DEBUG('Invite to be ignored:', invite)
                return False
        
        link = self.formatter.link(invite)
        if not len(link):
            if constants.IS_DEVELOPMENT:
                LOG_WARNING('Formatter not found. Invite data : ', invite)
            
            return False
        self._PrebattleInvitesManager__receivedInvites[invite.id] = (invite, link)
        if invite.isActive():
            self._PrebattleInvitesManager__unreadInvitesCount += 1
        
        return True

    
    def _updateInvite(self, other):
        inviteID = other.id
        (invite, _) = self._PrebattleInvitesManager__receivedInvites[inviteID]
        if other.isActive() and g_settings.userPreferences['invitesFromFriendsOnly']:
            user = self._PrebattleInvitesManager__usersManager.getUser(invite.creatorDBID, invite.creator)
            if not user.isFriend():
                LOG_DEBUG('Invite to be ignored:', invite)
                return False
        
        prevCount = invite.count
        invite = invite._merge(other)
        link = self.formatter.link(invite)
        self._PrebattleInvitesManager__receivedInvites[inviteID] = (invite, link)
        if invite.isActive() and prevCount < invite.count:
            self._PrebattleInvitesManager__unreadInvitesCount += 1
        
        return True

    
    def _delInvite(self, inviteID):
        result = inviteID in self._PrebattleInvitesManager__receivedInvites
        if result:
            self._PrebattleInvitesManager__receivedInvites.pop(inviteID)
        
        return result

    
    def _buildReceivedInviteList(self, invitesData):
        self._PrebattleInvitesManager__receivedInvites.clear()
        self._PrebattleInvitesManager__unreadInvitesCount = 0
        receiver = BigWorld.player().name
        receiverDBID = self._cp_playerDbID
        receiverClanAbbrev = None
        if self._cp_clanInfo is not None and len(self._cp_clanInfo) > 0:
            receiverClanAbbrev = self._cp_clanInfo[1]
        
        for (prebattleID, peripheryID) in invitesData.iteritems():
            data = None
            inviteID = self._makeInviteID(prebattleID, peripheryID)
            anotherPeriphery = connectionManager.peripheryID != peripheryID
            invite = PrbInviteWrapper(id = inviteID, receiver = receiver, receiverDBID = receiverDBID, receiverClanAbbrev = receiverClanAbbrev, peripheryID = peripheryID, anotherPeriphery = anotherPeriphery, **None)
            self._addInvite(invite)
        

    
    def _invalidateClanInfo(self):
        if not self._PrebattleInvitesManager__isUserRosterInited:
            return None
        receiverClanAbbrev = None
        changed = []
        if self._cp_clanInfo is not None and len(self._cp_clanInfo) > 0:
            receiverClanAbbrev = self._cp_clanInfo[1]
        
        for (invite, _) in self._PrebattleInvitesManager__receivedInvites.iteritems():
            if invite.receiverClanAbbrev != receiverClanAbbrev:
                invite = invite._replace(receiverClanAbbrev = receiverClanAbbrev)
                link = self.formatter.link(invite)
                self._PrebattleInvitesManager__receivedInvites[inviteID] = (invite, link)
                changed.append(inviteID)
                continue
        
        if len(changed) > 0:
            self.onReceivedInviteListModified([], changed, [])
        

    
    def getReceivedInviteCount(self):
        return len(self._PrebattleInvitesManager__receivedInvites)

    
    def getReceivedInvite(self, inviteID):
        return self._PrebattleInvitesManager__receivedInvites.get(inviteID)

    
    def getReceivedInvites(self, IDs = None):
        result = self._PrebattleInvitesManager__receivedInvites.values()
        if IDs is not None:
            result = (filter,)((lambda item: item[0].id in IDs), result)
        
        return result

    
    def getUnreadCount(self):
        return self._PrebattleInvitesManager__unreadInvitesCount

    
    def resetUnreadCount(self):
        self._PrebattleInvitesManager__unreadInvitesCount = 0



