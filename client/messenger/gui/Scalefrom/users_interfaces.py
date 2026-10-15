# Source Generated with Decompyle++
# File: users_interfaces.pyc (Python 2.6)

from gui import SystemMessages
from gui.Scaleform.CommandArgsParser import CommandArgsParser
from gui import GUI_SETTINGS
from messenger import MESSENGER_I18N_FILE, g_settings
from messenger.UsersManager import USERS_ROSTER_ACTIONS
from messenger.gui.interfaces import DispatcherProxyHolder
from messenger.gui.Scalefrom import UR_COMMANDS, C_COMMANDS, LIST_DP_TCOMMANDS
import constants

class _BaseUsersRosterInterface(DispatcherProxyHolder):
    DENUNCIATIONS = {
        'bot': constants.DENUNCIATION.BOT,
        'flood': constants.DENUNCIATION.FLOOD,
        'offend': constants.DENUNCIATION.OFFEND,
        'notFairPlay': constants.DENUNCIATION.NOT_FAIR_PLAY,
        'teamKill': constants.DENUNCIATION.TEAMKILL,
        'allyEjection': constants.DENUNCIATION.ALLY_EJECTION,
        'openingOfAllyPos': constants.DENUNCIATION.OPENING_OF_ALLY_POS }
    
    def __init__(self):
        self._movieViewHandler = None
        self._onlineFlag = None

    
    def _usersManager(self):
        return self._dispatcherProxy.users

    _usersManager = property(_usersManager)
    
    def populateUI(self, movieViewHandler):
        self._movieViewHandler = movieViewHandler

    
    def dispossessUI(self):
        self._movieViewHandler = None

    
    def _comparator(self, user, other):
        return cmp(user[1].lower(), other[1].lower())

    
    def onRequestFriendsLength(self, *args):
        parser = CommandArgsParser(self.onRequestFriendsLength.__name__)
        parser.parse(*args)
        parser.addArg(self._usersManager.getFriendsCount(isOnline = self._onlineFlag))
        self._movieViewHandler.respond(parser.args())

    
    def onRequestFriendItem(self, *args):
        parser = CommandArgsParser(self.onRequestFriendItem.__name__, 1, [
            int])
        (index,) = parser.parse(*args)
        list = sorted(self._usersManager.getFriendsList(isOnline = self._onlineFlag), cmp = self._comparator)
        if len(list) > index:
            parser.addArgs(list[index], [
                long])
        
        self._movieViewHandler.respond(parser.args())

    
    def onRequestFriendsItems(self, *args):
        parser = CommandArgsParser(self.onRequestFriendsItems.__name__, 2, [
            int,
            int])
        (startIndex, endIndex) = parser.parse(*args)
        list = sorted(self._usersManager.getFriendsList(isOnline = self._onlineFlag), cmp = self._comparator)
        for item in list[startIndex:endIndex + 1]:
            parser.addArgs(item, [
                long])
            parser.addArgs(g_settings.getLobbyUserCS(item[2]))
        
        self._movieViewHandler.respond(parser.args())

    
    def onRequestIgnoredLength(self, *args):
        parser = CommandArgsParser(self.onRequestIgnoredLength.__name__)
        parser.parse(*args)
        parser.addArg(self._usersManager.getIgnoredCount())
        self._movieViewHandler.respond(parser.args())

    
    def onRequestIgnoredItems(self, *args):
        parser = CommandArgsParser(self.onRequestIgnoredItems.__name__, 2, [
            int,
            int])
        (startIndex, endIndex) = parser.parse(*args)
        list = sorted(self._usersManager.getIgnoredList(), cmp = self._comparator)
        for item in list[startIndex:endIndex + 1]:
            parser.addArgs(item, [
                long])
            parser.addArgs(g_settings.getLobbyUserCS(item[2]))
        
        self._movieViewHandler.respond(parser.args())

    
    def onRequestMutedLength(self, *args):
        parser = CommandArgsParser(self.onRequestMutedLength.__name__)
        parser.parse(*args)
        parser.addArg(self._usersManager.getMutedCount())
        self._movieViewHandler.respond(parser.args())

    
    def onRequestMutedItems(self, *args):
        parser = CommandArgsParser(self.onRequestMutedItems.__name__, 2, [
            int,
            int])
        (startIndex, endIndex) = parser.parse(*args)
        list = sorted(self._usersManager.getMutedList(), cmp = self._comparator)
        for item in list[startIndex:endIndex + 1]:
            parser.addArgs(item, [
                long])
            parser.addArgs(g_settings.getLobbyUserCS(item[2]))
        
        self._movieViewHandler.respond(parser.args())

    
    def onRequestClanMembersLength(self, *args):
        parser = CommandArgsParser(self.onRequestClanMembersLength.__name__)
        parser.parse(*args)
        parser.addArg(self._usersManager.getClanMembersCount())
        self._movieViewHandler.respond(parser.args())

    
    def onRequestClanMembersItem(self, *args):
        parser = CommandArgsParser(self.onRequestClanMembersItem.__name__, 1, [
            int])
        (index,) = parser.parse(*args)
        list = sorted(self._usersManager.getClanMembersList(isOnline = self._onlineFlag), cmp = self._comparator)
        if len(list) > index:
            parser.addArgs(list[index], [
                long])
        
        self._movieViewHandler.respond(parser.args())

    
    def onRequestClanMembersItems(self, *args):
        parser = CommandArgsParser(self.onRequestClanMembersItems.__name__, 2, [
            int,
            int])
        (startIndex, endIndex) = parser.parse(*args)
        list = sorted(self._usersManager.getClanMembersList(isOnline = self._onlineFlag), cmp = self._comparator)
        for item in list[startIndex:endIndex + 1]:
            parser.addArgs(item, [
                long])
            parser.addArgs(g_settings.getLobbyUserCS(item[2]))
        
        self._movieViewHandler.respond(parser.args())

    
    def onAddToFriends(self, *args):
        parser = CommandArgsParser(self.onAddToFriends.__name__, 2, [
            long,
            str])
        (uid, name) = parser.parse(*args)
        self._usersManager.addFriend(uid, name)

    
    def onSetMuted(self, *args):
        parser = CommandArgsParser(self.onAddToFriends.__name__, 2, [
            long,
            str])
        (uid, name) = parser.parse(*args)
        self._usersManager.setMuted(uid, name)

    
    def onRemoveFromFriends(self, *args):
        parser = CommandArgsParser(self.onAddToFriends.__name__, 1, [
            long])
        (uid,) = parser.parse(*args)
        self._usersManager.removeFriend(uid)

    
    def onUnsetMuted(self, *args):
        parser = CommandArgsParser(self.onAddToFriends.__name__, 1, [
            long])
        (uid,) = parser.parse(*args)
        self._usersManager.unsetMuted(uid)

    
    def onAddToIgnored(self, *args):
        parser = CommandArgsParser(self.onAddToFriends.__name__, 2, [
            long,
            str])
        (uid, name) = parser.parse(*args)
        self._usersManager.addIgnored(uid, name)

    
    def onRemoveFromIgnored(self, *args):
        parser = CommandArgsParser(self.onAddToFriends.__name__, 1, [
            long])
        (uid,) = parser.parse(*args)
        self._usersManager.removeIgnored(uid)

    
    def onDenunciation(self, *args):
        parser = CommandArgsParser(self.onDenunciation.__name__, 3, [
            long,
            str,
            str])
        (uid, name, topic) = parser.parse(*args)
        topicID = self.DENUNCIATIONS.get(topic)
        if topicID is not None:
            self._usersManager.makeDenunciation(uid, name, topicID)
        

    
    def onCreatePrivateChannel(self, *args):
        parser = CommandArgsParser(self.onAddToFriends.__name__, 2, [
            long,
            str])
        (uid, name) = parser.parse(*args)
        self._usersManager.createPrivateChannel(uid, name)

    
    def onRequestUserInfo(self, *args):
        parser = CommandArgsParser(self.onAddToFriends.__name__, 2, [
            long,
            str])
        (uid, name) = parser.parse(*args)
        self._usersManager.requestUserInfo(uid, name)

    
    def onRequestVehicleStat(self, *args):
        parser = CommandArgsParser(self.onAddToFriends.__name__, 3, [
            long,
            str,
            str])
        (uid, name, vehicleId) = parser.parse(*args)
        self._usersManager.requestVehicleStat(uid, name, vehicleId)

    
    def onRequestRosterValue(self, *args):
        parser = CommandArgsParser(self.onRequestRosterValue.__name__, 2, [
            long,
            str])
        (uid, name) = parser.parse(*args)
        user = self._usersManager.getUser(uid, name)
        parser.addArgs(user.list(), converters = [
            long])
        self._movieViewHandler.respond(parser.args())

    
    def onSetOnlineFlag(self, *args):
        parser = CommandArgsParser(self.onSetOnlineFlag.__name__, 1)
        (self._onlineFlag,) = parser.parse(*args)



class UsersRosterInterface(_BaseUsersRosterInterface):
    _UsersRosterInterface__userTransferUserMsgKeys = {
        USERS_ROSTER_ACTIONS.AddToFriend: '#%s:client/information/addToFriends/message' % MESSENGER_I18N_FILE,
        USERS_ROSTER_ACTIONS.AddToIgnored: '#%s:client/information/addToIgnored/message' % MESSENGER_I18N_FILE,
        USERS_ROSTER_ACTIONS.SetMuted: '#%s:client/information/setMuted/message' % MESSENGER_I18N_FILE,
        USERS_ROSTER_ACTIONS.UnsetMuted: '#%s:client/information/unsetMuted/message' % MESSENGER_I18N_FILE,
        USERS_ROSTER_ACTIONS.RemoveFromFriend: '#%s:client/information/removeFromFriends/message' % MESSENGER_I18N_FILE,
        USERS_ROSTER_ACTIONS.RemoveFromIgnored: '#%s:client/information/removeFromIgnored/message' % MESSENGER_I18N_FILE }
    
    def populateUI(self, movieViewHandler):
        _BaseUsersRosterInterface.populateUI(self, movieViewHandler)
        self._movieViewHandler.addExternalCallbacks({
            UR_COMMANDS.FriendsRequestLength(): self.onRequestFriendsLength,
            UR_COMMANDS.FriendsRequestItemAt(): self.onRequestFriendItem,
            UR_COMMANDS.FriendsRequestItemRange(): self.onRequestFriendsItems,
            UR_COMMANDS.IgnoredRequestLength(): self.onRequestIgnoredLength,
            UR_COMMANDS.IgnoredRequestItemRange(): self.onRequestIgnoredItems,
            UR_COMMANDS.MutedRequestLength(): self.onRequestMutedLength,
            UR_COMMANDS.MutedRequestItemRange(): self.onRequestMutedItems,
            UR_COMMANDS.ClanRequestLength(): self.onRequestClanMembersLength,
            UR_COMMANDS.ClanRequestItemRange(): self.onRequestClanMembersItems,
            UR_COMMANDS.AddToFriends(): self.onAddToFriends,
            UR_COMMANDS.RemoveFromFriends(): self.onRemoveFromFriends,
            UR_COMMANDS.AddToIgnored(): self.onAddToIgnored,
            UR_COMMANDS.RemoveFromIgnored(): self.onRemoveFromIgnored,
            UR_COMMANDS.CreatePrivateChannel(): self.onCreatePrivateChannel,
            C_COMMANDS.RequestUserInfo(): self.onRequestUserInfo,
            C_COMMANDS.RequestVehicleStat(): self.onRequestVehicleStat,
            UR_COMMANDS.RequestRosterValue(): self.onRequestRosterValue,
            UR_COMMANDS.SetMuted(): self.onSetMuted,
            UR_COMMANDS.UnsetMuted(): self.onUnsetMuted,
            UR_COMMANDS.Denunciation(): self.onDenunciation })
        users = self._usersManager
        users.onFriendStatusUpdated += self.onRefreshFriendsList
        users.onClanMembersListRefresh += self.onRefreshClanMembersList
        users.onClanMemberStatusesUpdated += self.onRefreshClanMembersList
        users.onUsersRosterUpdate += self.onUsersRosterUpdate
        users.onUsersRosterReceived += self.onUsersRosterReceived

    
    def dispossessUI(self):
        users = self._usersManager
        if users:
            users.onFriendStatusUpdated -= self.onRefreshFriendsList
            users.onClanMembersListRefresh -= self.onRefreshClanMembersList
            users.onClanMemberStatusesUpdated -= self.onRefreshClanMembersList
            users.onUsersRosterUpdate -= self.onUsersRosterUpdate
            users.onUsersRosterReceived -= self.onUsersRosterReceived
        
        self._movieViewHandler.removeExternalCallbacks(UR_COMMANDS.FriendsRequestLength(), UR_COMMANDS.FriendsRequestItemAt(), UR_COMMANDS.FriendsRequestItemRange(), UR_COMMANDS.IgnoredRequestLength(), UR_COMMANDS.IgnoredRequestItemRange(), UR_COMMANDS.MutedRequestLength(), UR_COMMANDS.MutedRequestItemRange(), UR_COMMANDS.ClanRequestLength(), UR_COMMANDS.ClanRequestItemRange(), UR_COMMANDS.AddToFriends(), UR_COMMANDS.RemoveFromFriends(), UR_COMMANDS.AddToIgnored(), UR_COMMANDS.RemoveFromIgnored(), UR_COMMANDS.CreatePrivateChannel(), C_COMMANDS.RequestUserInfo(), C_COMMANDS.RequestVehicleStat(), UR_COMMANDS.RequestRosterValue(), UR_COMMANDS.SetMuted(), UR_COMMANDS.UnsetMuted(), UR_COMMANDS.Denunciation())
        _BaseUsersRosterInterface.dispossessUI(self)

    
    def onRefreshFriendsList(self):
        self._movieViewHandler.call(UR_COMMANDS.FriendsRefreshList(), [
            self._usersManager.getFriendsCount()])

    
    def onRefreshIgnoredList(self):
        self._movieViewHandler.call(UR_COMMANDS.IgnoredRefreshList(), [
            self._usersManager.getIgnoredCount()])

    
    def onRefreshMutedList(self):
        self._movieViewHandler.call(UR_COMMANDS.MutedRefreshList(), [
            self._usersManager.getMutedCount()])

    
    def onRefreshClanMembersList(self):
        self._movieViewHandler.call(UR_COMMANDS.ClanRefreshList(), [
            self._usersManager.getClanMembersCount()])

    
    def onUsersRosterUpdate(self, action, user):
        self.onRefreshFriendsList()
        self.onRefreshIgnoredList()
        self.onRefreshMutedList()
        self.onRefreshClanMembersList()
        if not (GUI_SETTINGS.voiceChat):
            if action == USERS_ROSTER_ACTIONS.SetMuted or action == USERS_ROSTER_ACTIONS.UnsetMuted:
                return None
            messageKey = self._UsersRosterInterface__userTransferUserMsgKeys.get(action)
            if messageKey is not None:
                SystemMessages.pushI18nMessage(messageKey, user.userName)
            

    
    def onUsersRosterReceived(self):
        self.onRefreshFriendsList()
        self.onRefreshIgnoredList()
        self.onRefreshMutedList()
        self.onRefreshClanMembersList()



class PrebattleUsersRosterInterface(_BaseUsersRosterInterface):
    
    def __init__(self, prefix = 'Prebattle'):
        _BaseUsersRosterInterface.__init__(self)
        self._PrebattleUsersRosterInterface__friendsPrefix = '%s.Friends' % prefix
        self._PrebattleUsersRosterInterface__clanPrefix = '%s.ClanMembers' % prefix

    
    def populateUI(self, movieViewHandler):
        _BaseUsersRosterInterface.populateUI(self, movieViewHandler)
        self._movieViewHandler.addExternalCallbacks({
            LIST_DP_TCOMMANDS.RequestLength(self._PrebattleUsersRosterInterface__friendsPrefix): self.onRequestFriendsLength,
            LIST_DP_TCOMMANDS.RequestItemAt(self._PrebattleUsersRosterInterface__friendsPrefix): self.onRequestFriendItem,
            LIST_DP_TCOMMANDS.RequestItemRange(self._PrebattleUsersRosterInterface__friendsPrefix): self.onRequestFriendsItems,
            '%s.SetOnlineFlag' % self._PrebattleUsersRosterInterface__friendsPrefix: self.onSetFriendsOnlineFlag,
            '%s.RequestAllItems' % self._PrebattleUsersRosterInterface__friendsPrefix: self.onRequestFriendsAllItems,
            LIST_DP_TCOMMANDS.RequestLength(self._PrebattleUsersRosterInterface__clanPrefix): self.onRequestClanMembersLength,
            LIST_DP_TCOMMANDS.RequestItemAt(self._PrebattleUsersRosterInterface__clanPrefix): self.onRequestClanMembersItem,
            LIST_DP_TCOMMANDS.RequestItemRange(self._PrebattleUsersRosterInterface__clanPrefix): self.onRequestClanMembersItems,
            '%s.SetOnlineFlag' % self._PrebattleUsersRosterInterface__clanPrefix: self.onSetClanMembersOnlineFlag,
            '%s.RequestAllItems' % self._PrebattleUsersRosterInterface__clanPrefix: self.onRequestClanMembersAllItems })
        users = self._usersManager
        users.onFriendStatusUpdated += self.onRefreshFriendsList
        users.onClanMembersListRefresh += self.onRefreshClanMembersList
        users.onClanMemberStatusesUpdated += self.onRefreshClanMembersList
        users.onUsersRosterUpdate += self.onUsersRosterUpdate
        users.onUsersRosterReceived += self.onRefreshList

    
    def dispossessUI(self):
        users = self._usersManager
        if users:
            users.onFriendStatusUpdated -= self.onRefreshFriendsList
            users.onClanMembersListRefresh -= self.onRefreshClanMembersList
            users.onClanMemberStatusesUpdated -= self.onRefreshClanMembersList
            users.onUsersRosterUpdate -= self.onUsersRosterUpdate
            users.onUsersRosterReceived -= self.onRefreshList
        
        self._movieViewHandler.removeExternalCallbacks(LIST_DP_TCOMMANDS.RequestLength(self._PrebattleUsersRosterInterface__friendsPrefix), LIST_DP_TCOMMANDS.RequestItemAt(self._PrebattleUsersRosterInterface__friendsPrefix), LIST_DP_TCOMMANDS.RequestItemRange(self._PrebattleUsersRosterInterface__friendsPrefix), '%s.SetOnlineFlag' % self._PrebattleUsersRosterInterface__friendsPrefix, '%s.RequestAllItems' % self._PrebattleUsersRosterInterface__friendsPrefix, LIST_DP_TCOMMANDS.RequestLength(self._PrebattleUsersRosterInterface__clanPrefix), LIST_DP_TCOMMANDS.RequestItemAt(self._PrebattleUsersRosterInterface__clanPrefix), LIST_DP_TCOMMANDS.RequestItemRange(self._PrebattleUsersRosterInterface__clanPrefix), '%s.SetOnlineFlag' % self._PrebattleUsersRosterInterface__clanPrefix, '%s.RequestAllItems' % self._PrebattleUsersRosterInterface__clanPrefix)
        _BaseUsersRosterInterface.dispossessUI(self)

    
    def onRefreshFriendsList(self):
        self._movieViewHandler.call(LIST_DP_TCOMMANDS.RefreshList(self._PrebattleUsersRosterInterface__friendsPrefix), [
            self._usersManager.getFriendsCount(isOnline = self._onlineFlag)])

    
    def onRefreshClanMembersList(self):
        self._movieViewHandler.call(LIST_DP_TCOMMANDS.RefreshList(self._PrebattleUsersRosterInterface__clanPrefix), [
            self._usersManager.getClanMembersCount(isOnline = self._onlineFlag)])

    
    def onUsersRosterUpdate(self, action, _):
        if action in [
            USERS_ROSTER_ACTIONS.AddToFriend,
            USERS_ROSTER_ACTIONS.RemoveFromFriend,
            USERS_ROSTER_ACTIONS.SetMuted,
            USERS_ROSTER_ACTIONS.UnsetMuted]:
            self.onRefreshList()
        

    
    def onRefreshList(self):
        self.onRefreshFriendsList()
        self.onRefreshClanMembersList()

    
    def onSetFriendsOnlineFlag(self, *args):
        _BaseUsersRosterInterface.onSetOnlineFlag(self, *args)
        self.onRefreshFriendsList()

    
    def onSetClanMembersOnlineFlag(self, *args):
        _BaseUsersRosterInterface.onSetOnlineFlag(self, *args)
        self.onRefreshClanMembersList()

    
    def onRequestFriendsAllItems(self, *args):
        parser = CommandArgsParser(self.onRequestFriendsAllItems.__name__)
        parser.parse(*args)
        list = sorted(self._usersManager.getFriendsList(isOnline = True), cmp = self._comparator)
        for item in list:
            parser.addArgs(item, [
                long])
        
        self._movieViewHandler.respond(parser.args())

    
    def onRequestClanMembersAllItems(self, *args):
        parser = CommandArgsParser(self.onRequestClanMembersAllItems.__name__)
        parser.parse(*args)
        list = sorted(self._usersManager.getClanMembersList(isOnline = True), cmp = self._comparator)
        for item in list:
            parser.addArgs(item, [
                long])
        
        self._movieViewHandler.respond(parser.args())



