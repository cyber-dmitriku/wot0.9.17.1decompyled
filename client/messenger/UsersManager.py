# Source Generated with Decompyle++
# File: UsersManager.pyc (Python 2.6)

import BigWorld
from chat_shared import CHAT_ACTIONS, USERS_ROSTER_FRIEND, USERS_ROSTER_IGNORED, CHAT_RESPONSES, USERS_ROSTER_VOICE_MUTED
from collections import defaultdict, deque
from messenger import BREAKERS_MAX_LENGTH
from messenger.common import MessangerSubscriber, MessengerGlobalStorage
from messenger.wrappers import UserWrapper
import Event
import constants
from adisp import async
from debug_utils import LOG_ERROR, LOG_DEBUG

def _userWrapperFactory():
    return UserWrapper()


class USERS_ROSTER_ACTIONS(object):
    (AddToFriend, RemoveFromFriend, AddToIgnored, RemoveFromIgnored, SetMuted, UnsetMuted) = range(6)


class CLAN_INIT_STEPS(object):
    RECEIVE_CLAN_INFO = 1
    RECEIVE_MEMBERS_LIST = 2
    RECEIVE_MEMBERS_STATUSES = 4
    INIT = RECEIVE_CLAN_INFO | RECEIVE_MEMBERS_LIST | RECEIVE_MEMBERS_STATUSES


class UsersManager(MessangerSubscriber):
    _UsersManager__contacts = defaultdict(_userWrapperFactory)
    _UsersManager__clanMembers = defaultdict(_userWrapperFactory)
    _UsersManager__clanInitSteps = 0
    _UsersManager__breakers = deque([], BREAKERS_MAX_LENGTH)
    _cp_playerDbId = MessengerGlobalStorage('_playerDbId', -0x1L)
    _cp_accountAttrs = MessengerGlobalStorage('_accountAttrs', -1)
    _cp_clanInfo = MessengerGlobalStorage('_clanInfo', None)
    
    def __init__(self):
        MessangerSubscriber.__init__(self)
        self._UsersManager__eventManager = Event.EventManager()
        self.onFindUsersComplete = Event.Event(self._UsersManager__eventManager)
        self.onFindUsersFailed = Event.Event(self._UsersManager__eventManager)
        self.onFriendStatusUpdated = Event.Event(self._UsersManager__eventManager)
        self.onUsersRosterUpdate = Event.Event(self._UsersManager__eventManager)
        self.onClanMembersListRefresh = Event.Event(self._UsersManager__eventManager)
        self.onClanMemberStatusesUpdated = Event.Event(self._UsersManager__eventManager)
        self.onUsersRosterReceived = Event.Event()
        self.onDenunciationReceived = Event.Event()
        self.onAccountDossierRequest = Event.Event()
        self.onVehicleDossierRequest = Event.Event()
        self._responseHandlers = {
            CHAT_RESPONSES.commandInCooldown: '_UsersManager__onCommandInCooldown',
            CHAT_RESPONSES.incorrectCharacter: '_UsersManager__onIncorrectCharacter' }
        self._UsersManager__replayCtrl = None

    
    def subscribeToActions(self):
        '''
\t\tSubscribe to chat action.
\t\t'''
        self.subscribeAction(self.onFindUsers, CHAT_ACTIONS.findUsers)
        self.subscribeAction(self.onAddFriend, CHAT_ACTIONS.addFriend)
        self.subscribeAction(self.onAddIgnored, CHAT_ACTIONS.addIgnored)
        self.subscribeAction(self.onRemoveFriend, CHAT_ACTIONS.removeFriend)
        self.subscribeAction(self.onRemoveIgnored, CHAT_ACTIONS.removeIgnored)
        self.subscribeAction(self.onFriendStatusUpdate, CHAT_ACTIONS.friendStatusUpdate)
        self.subscribeAction(self.onRequestUsersRoster, CHAT_ACTIONS.requestUsersRoster)
        self.subscribeAction(self.onSetMuted, CHAT_ACTIONS.setMuted)
        self.subscribeAction(self.onUnsetMuted, CHAT_ACTIONS.unsetMuted)

    
    def findUsers(self, token, onlineMode = None, requestID = None):
        '''
\t\tRequest to server: finds users with specified criteria - token
\t\t@param token: searches name of users
\t\t@param onlineMode: defines search mode:
\t\t\tNone - search routine returns online and offline users
\t\t\tTrue - search routine returns only online users
\t\t\tFalse - search routine returns only offline users
\t\t@param requestID: unique id to search request
\t\t'''
        BigWorld.player().findUsers(token, onlineMode = onlineMode, requestID = requestID)

    
    def addFriend(self, friendID, friendName):
        '''
\t\tRequest to server: adds user to the fiends list.
\t\t@param friendID: user database id
\t\t@param friendName: user name
\t\t'''
        BigWorld.player().addFriend(friendID, friendName)

    
    def setMuted(self, userID, userName):
        '''
\t\tRequest to server: set user muted
\t\t@param userID: user database id
\t\t@param userName: user name
\t\t'''
        BigWorld.player().setMuted(userID, userName)

    
    def addIgnored(self, ignoredID, ignoredName):
        '''
\t\tRequest to server: adds user to the ignored list.
\t\t@param ignoredID: user database id
\t\t@param ignoredName: user name
\t\t'''
        BigWorld.player().addIgnored(ignoredID, ignoredName)

    
    def removeFriend(self, friendID):
        '''
\t\tRequest to server: remove user to the fiends list.
\t\t@param friendID: user database id
\t\t'''
        BigWorld.player().removeFriend(friendID)

    
    def unsetMuted(self, userID):
        '''
\t\tRequest to server: unset user muted.
\t\t@param userID: user database id
\t\t'''
        BigWorld.player().unsetMuted(userID)

    
    def makeDenunciation(self, userID, userName, topicID):
        BigWorld.player().makeDenunciation(userID, topicID, constants.VIOLATOR_KIND.UNKNOWN)
        self.onDenunciationReceived(userName, topicID)

    
    def removeIgnored(self, ignoredID):
        '''
\t\tRequest to server: remove user to the ignored list.
\t\t@param ignoredID: user database id
\t\t'''
        BigWorld.player().removeIgnored(ignoredID)

    
    def requestUsersRoster(self):
        '''
\t\tRequest to server: get list of friends and ignored users.
\t\t'''
        BigWorld.player().requestUsersRoster()

    
    def requestFriendStatus(self, friendID = -1):
        '''
\t\tRequest to server: get friend online status.
\t\t@param friendID: user id
\t\t'''
        BigWorld.player().requestFriendStatus(friendID)

    
    def createPrivateChannel(self, friendID, friendName):
        '''
\t\tRequest to server: create private channel with friend.
\t\t@param friendID: user id
\t\t@param friendName: user name
\t\t'''
        BigWorld.player().createPrivate(friendID, friendName)

    
    def requestClanInfo(self, name, callback):
        
        def response(resultID, clanDBID, clanInfo):
            if resultID < 0:
                LOG_ERROR('Server return error for clan info request: responseCode=%s' % resultID)
                return None
            callback((clanDBID, clanInfo))

        BigWorld.player().requestPlayerClanInfo(name, response)

    requestClanInfo = async(requestClanInfo)
    
    def requestClanEmblem(self, clanDBID, callback):
        
        def response(url, file):
            callback((url, file))

        clan_emblems = BigWorld.player().serverSettings['file_server'].get('clan_emblems', { })
        url_template = clan_emblems.get('url_template')
        if url_template is not None and len(url_template):
            
            try:
                url = url_template % clanDBID
                BigWorld.player().customFilesCache.get(url, response, True)
            except TypeError:
                (None,)
                LOG_ERROR('Invalid url_template for clan emblems', url_template)
                callback((None, None))
            

        callback((None, None))

    requestClanEmblem = async(requestClanEmblem)
    
    def requestUserInfo(self, uid, name):
        user = UserWrapper(uid, name)
        if uid in self._UsersManager__contacts:
            user = self._UsersManager__contacts[uid]
        
        self.onAccountDossierRequest(user)

    
    def requestVehicleStat(self, uid, name, vehicleID):
        user = UserWrapper(uid, name)
        if uid in self._UsersManager__contacts:
            user = self._UsersManager__contacts[uid]
        
        self.onVehicleDossierRequest(user, vehicleID)

    
    def setClanInfo(self, clanInfo):
        LOG_DEBUG('setClanInfo', clanInfo)
        if clanInfo is not None:
            pass
        hasClanInfo = len(clanInfo) > 0
        if not (self._UsersManager__clanInitSteps & CLAN_INIT_STEPS.RECEIVE_CLAN_INFO) and hasClanInfo:
            self._UsersManager__clanInitSteps |= CLAN_INIT_STEPS.RECEIVE_CLAN_INFO
        
        if hasClanInfo:
            for uid in self._UsersManager__clanMembers.iterkeys():
                self._UsersManager__clanMembers[uid].clanName = clanInfo[1]
            
        
        self._cp_clanInfo = clanInfo
        if self._UsersManager__clanInitSteps & CLAN_INIT_STEPS.INIT:
            self.onClanMembersListRefresh()
        

    
    def setClanMembersList(self, clanMembers):
        LOG_DEBUG('setClanMembersList', clanMembers)
        if not self._UsersManager__clanInitSteps & CLAN_INIT_STEPS.RECEIVE_MEMBERS_LIST:
            self._UsersManager__clanInitSteps |= CLAN_INIT_STEPS.RECEIVE_MEMBERS_LIST
        
        if self._cp_clanInfo is not None and len(self._cp_clanInfo) > 0:
            pass
        1
        clanAbbrev = None
        for (uid, name) in clanMembers.iteritems():
            if self._cp_playerDbId != uid:
                self._UsersManager__clanMembers[uid].uid = uid
                self._UsersManager__clanMembers[uid].userName = name
                self._UsersManager__clanMembers[uid].clanName = clanAbbrev
                continue
            self._cp_clanInfo[1]
        
        if self._UsersManager__clanInitSteps & CLAN_INIT_STEPS.INIT:
            self.onClanMembersListRefresh()
        

    
    def setClanMemberStatus(self, uid, status):
        LOG_DEBUG('setClanMemberStatus', uid, status)
        if not self._UsersManager__clanInitSteps & CLAN_INIT_STEPS.RECEIVE_MEMBERS_STATUSES:
            self._UsersManager__clanInitSteps |= CLAN_INIT_STEPS.RECEIVE_MEMBERS_STATUSES
        
        if self._cp_playerDbId != uid:
            self._UsersManager__clanMembers[uid].uid = uid
            self._UsersManager__clanMembers[uid].online = status
            if self._UsersManager__clanInitSteps & CLAN_INIT_STEPS.INIT:
                self.onClanMemberStatusesUpdated()
            
        

    
    def setClanMemberStatuses(self, uids, status):
        LOG_DEBUG('setClanMemberStatuses', uids, status)
        updated = False
        if not self._UsersManager__clanInitSteps & CLAN_INIT_STEPS.RECEIVE_MEMBERS_STATUSES:
            self._UsersManager__clanInitSteps |= CLAN_INIT_STEPS.RECEIVE_MEMBERS_STATUSES
        
        for uid in uids:
            if self._cp_playerDbId != uid:
                self._UsersManager__clanMembers[uid].uid = uid
                self._UsersManager__clanMembers[uid].online = status
                updated = True
                continue
        
        if self._UsersManager__clanInitSteps & CLAN_INIT_STEPS.INIT and updated:
            self.onClanMemberStatusesUpdated()
        

    
    def onFindUsers(self, chatAction):
        chatActionDict = dict(chatAction)
        result = chatActionDict.get('data', [])
        requestID = chatActionDict.get('requestID', [])
        users = []
        for userData in result:
            user = UserWrapper.fromSearchAction(*userData)
            if not len(user.userName):
                continue
            
            user.himself = self.isCurrentPlayer(user.uid)
            if user.uid in self._UsersManager__contacts:
                user.roster = self._UsersManager__contacts[user.uid].roster
            
            users.append(user)
        
        self.onFindUsersComplete(requestID, users)

    
    def onAddFriend(self, chatAction):
        '''
\t\tResponse from server to a add to friends request (@see: UsersManager.addFriend).
\t\t@param chatAction: chat action data
\t\t'''
        userData = [
            -1,
            False]
        if chatAction.has_key('data'):
            userData = list(chatAction['data'])
        
        user = UserWrapper(*userData)
        if user.uid in self._UsersManager__contacts:
            user.roster = self._UsersManager__contacts[user.uid].roster
        
        user.roster |= USERS_ROSTER_FRIEND
        if bool(user.roster & USERS_ROSTER_IGNORED):
            user.roster ^= USERS_ROSTER_IGNORED
        
        self._UsersManager__contacts[user.uid].update(user)
        if self._UsersManager__clanMembers.has_key(user.uid):
            self._UsersManager__clanMembers[user.uid].update(user)
        
        self.onUsersRosterUpdate(USERS_ROSTER_ACTIONS.AddToFriend, user)

    
    def onSetMuted(self, chatAction):
        '''
\t\tResponse from server to set user muted (@see: UsersManager.addFriend).
\t\t@param chatAction: chat action data
\t\t'''
        userData = [
            -1,
            False]
        if chatAction.has_key('data'):
            userData = list(chatAction['data'])
        
        user = UserWrapper(*userData)
        if user.uid in self._UsersManager__contacts:
            user.roster = self._UsersManager__contacts[user.uid].roster
        
        user.roster |= USERS_ROSTER_VOICE_MUTED
        self._UsersManager__contacts[user.uid].update(user)
        if self._UsersManager__clanMembers.has_key(user.uid):
            self._UsersManager__clanMembers[user.uid].update(user)
        
        self.onUsersRosterUpdate(USERS_ROSTER_ACTIONS.SetMuted, user)

    
    def onUnsetMuted(self, chatAction):
        '''
\t\tResponse from server to unset user muted (@see: UsersManager.removeFriend).
\t\t@param chatAction: chat action data
\t\t'''
        if chatAction.has_key('data'):
            pass
        1
        userData = -1
        uid = long(userData)
        if self._UsersManager__contacts.has_key(uid) and bool(self._UsersManager__contacts[uid].roster & USERS_ROSTER_VOICE_MUTED):
            user = self._UsersManager__contacts[uid]
            user.roster ^= USERS_ROSTER_VOICE_MUTED
            self._UsersManager__contacts[user.uid].update(user)
            if self._UsersManager__clanMembers.has_key(user.uid):
                self._UsersManager__clanMembers[user.uid].update(user)
            
            self.onUsersRosterUpdate(USERS_ROSTER_ACTIONS.UnsetMuted, user)
        

    
    def onAddIgnored(self, chatAction):
        '''
\t\tResponse from server to a add to ignored request (@see: UsersManager.addIgnored).
\t\t@param chatAction: chat action data
\t\t'''
        userData = [
            -1,
            False]
        if chatAction.has_key('data'):
            userData = list(chatAction['data'])
        
        user = UserWrapper(*userData)
        if user.uid in self._UsersManager__contacts:
            user.roster = self._UsersManager__contacts[user.uid].roster
        
        user.roster |= USERS_ROSTER_IGNORED
        if bool(user.roster & USERS_ROSTER_FRIEND):
            user.roster ^= USERS_ROSTER_FRIEND
        
        self._UsersManager__contacts[user.uid].update(user)
        if self._UsersManager__clanMembers.has_key(user.uid):
            self._UsersManager__clanMembers[user.uid].update(user)
        
        self.onUsersRosterUpdate(USERS_ROSTER_ACTIONS.AddToIgnored, user)

    
    def onRemoveFriend(self, chatAction):
        '''
\t\tResponse from server to a remove from friends request (@see: UsersManager.removeFriend).
\t\t@param chatAction: chat action data
\t\t'''
        if chatAction.has_key('data'):
            pass
        1
        userData = -1
        uid = long(userData)
        if self._UsersManager__contacts.has_key(uid) and bool(self._UsersManager__contacts[uid].roster & USERS_ROSTER_FRIEND):
            user = self._UsersManager__contacts[uid]
            user.roster ^= USERS_ROSTER_FRIEND
            self._UsersManager__contacts[user.uid].update(user)
            if self._UsersManager__clanMembers.has_key(user.uid):
                self._UsersManager__clanMembers[user.uid].update(user)
            
            self.onUsersRosterUpdate(USERS_ROSTER_ACTIONS.RemoveFromFriend, user)
        

    
    def onRemoveIgnored(self, chatAction):
        '''
\t\tResponse from server to a remove from ignored request (@see: UsersManager.removeIgnored).
\t\t@param chatAction: chat action data
\t\t'''
        if chatAction.has_key('data'):
            pass
        1
        userData = -1
        uid = long(userData)
        if self._UsersManager__contacts.has_key(uid) and bool(self._UsersManager__contacts[uid].roster & USERS_ROSTER_IGNORED):
            user = self._UsersManager__contacts[uid]
            user.roster ^= USERS_ROSTER_IGNORED
            self._UsersManager__contacts[user.uid].update(user)
            if self._UsersManager__clanMembers.has_key(user.uid):
                self._UsersManager__clanMembers[user.uid].update(user)
            
            self.onUsersRosterUpdate(USERS_ROSTER_ACTIONS.RemoveFromIgnored, user)
        

    
    def onFriendStatusUpdate(self, chatAction):
        if chatAction.has_key('data'):
            pass
        1
        userData = [
            -1,
            False]
        (uid, status) = userData.iteritems().next()
        if self._UsersManager__contacts.has_key(uid):
            self._UsersManager__contacts[uid].online = status
        
        self.onFriendStatusUpdated()

    
    def onRequestUsersRoster(self, chatAction):
        '''
\t\tServer response to a request friends and ignore list (@see: UsersManager.requestUsersRoster).
\t\t@param chatAction: chat action data
\t\t'''
        if self._UsersManager__replayCtrl is None:
            import BattleReplay as BattleReplay
            self._UsersManager__replayCtrl = BattleReplay.g_replayCtrl
        
        if self._UsersManager__replayCtrl.isRecording:
            self._UsersManager__replayCtrl.cancelSaveCurrMessage()
        
        data = dict(chatAction)
        result = data.get('data', [])
        flags = data.get('flags', 0)
        if not flags:
            self._UsersManager__contacts.clear()
        
        for userData in result:
            user = UserWrapper(*userData)
            self._UsersManager__contacts[user.uid].update(user)
        
        self.onUsersRosterReceived()

    
    def _UsersManager__onCommandInCooldown(self, actionResponse, chatAction):
        data = chatAction.get('data', {
            'command': None,
            'cooldownPeriod': -1 })
        result = False
        if data['command'] == 'findUser':
            result = True
            self.onFindUsersFailed(chatAction.get('requestID', -0x1L), actionResponse, data)
        
        return result

    
    def _UsersManager__onIncorrectCharacter(self, actionResponse, chatAction):
        action = chatAction.get('action')
        result = False
        if action == CHAT_ACTIONS.findUsers.index():
            result = True
            self.onFindUsersFailed(chatAction.get('requestID', -0x1L), actionResponse, None)
        
        return result

    
    def clear(self):
        self._UsersManager__contacts = defaultdict(_userWrapperFactory)
        self._UsersManager__clanMembers.clear()
        self._UsersManager__clanInitSteps = 0
        self._UsersManager__breakers.clear()
        self._UsersManager__eventManager.clear()
        self._cp_playerDbId = -0x1L
        self._cp_clanInfo = None
        self._cp_accountAttrs = -1

    
    def getFriendsCount(self, isOnline = None):
        if isOnline is not None:
            filtered = (filter,)((lambda user: if user.online == isOnline:
passbool(user.roster & USERS_ROSTER_FRIEND)), self._UsersManager__contacts.values())
        else:
            filtered = filter((lambda user: bool(user.roster & USERS_ROSTER_FRIEND)), self._UsersManager__contacts.values())
        return len(filtered)

    
    def getMutedCount(self, isOnline = None):
        filtered = filter((lambda user: bool(user.roster & USERS_ROSTER_VOICE_MUTED)), self._UsersManager__contacts.values())
        return len(filtered)

    
    def getIgnoredCount(self):
        filtered = filter((lambda user: bool(user.roster & USERS_ROSTER_IGNORED)), self._UsersManager__contacts.values())
        return len(filtered)

    
    def getClanMembersCount(self, isOnline = None):
        if isOnline is not None:
            filtered = (filter,)((lambda user: user.online == isOnline), self._UsersManager__clanMembers.values())
            length = len(filtered)
        else:
            length = len(self._UsersManager__clanMembers)
        return length

    
    def getFriendsList(self, isOnline = None):
        if isOnline is not None:
            users = (filter,)((lambda user: if user.online == isOnline:
passbool(user.roster & USERS_ROSTER_FRIEND)), self._UsersManager__contacts.values())
        else:
            users = filter((lambda user: bool(user.roster & USERS_ROSTER_FRIEND)), self._UsersManager__contacts.values())
        continue
        return [ user.tuple() for user in users ]

    
    def getMutedList(self, isOnline = None):
        users = filter((lambda user: bool(user.roster & USERS_ROSTER_VOICE_MUTED)), self._UsersManager__contacts.values())
        continue
        return [ user.tuple() for user in users ]

    
    def getIgnoredList(self):
        users = filter((lambda user: bool(user.roster & USERS_ROSTER_IGNORED)), self._UsersManager__contacts.values())
        continue
        return [ user.tuple() for user in users ]

    
    def getClanMembersList(self, isOnline = None):
        if isOnline is not None:
            users = (filter,)((lambda user: user.online == isOnline), self._UsersManager__clanMembers.values())
        else:
            users = self._UsersManager__clanMembers.values()
        continue
        return [ user.tuple() for user in users ]

    
    def getUser(self, uid, name):
        user = UserWrapper(uid, name)
        if user.uid in self._UsersManager__contacts:
            user = self._UsersManager__contacts[uid]
        
        user.himself = self.isCurrentPlayer(user.uid)
        user.breaker = uid in self._UsersManager__breakers
        return user

    
    def markAsBreaker(self, uid, flag):
        if flag:
            if uid not in self._UsersManager__breakers:
                self._UsersManager__breakers.append(uid)
            
        elif uid in self._UsersManager__breakers:
            self._UsersManager__breakers.remove(uid)
        

    
    def resetBreakers(self):
        self._UsersManager__breakers.clear()

    
    def cp_canViewColoringBadWords(self):
        if not self._cp_accountAttrs & constants.ACCOUNT_ATTR.CHAT_ADMIN != 0:
            pass
        return self._cp_accountAttrs & constants.ACCOUNT_ATTR.ADMIN != 0

    
    def isCurrentPlayer(cls, playerDbId):
        return UsersManager._cp_playerDbId.value() == playerDbId

    isCurrentPlayer = classmethod(isCurrentPlayer)


