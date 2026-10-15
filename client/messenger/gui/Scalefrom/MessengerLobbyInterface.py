# Source Generated with Decompyle++
# File: MessengerLobbyInterface.pyc (Python 2.6)

from debug_utils import *
from helpers import i18n
from gui import SystemMessages
from gui.Scaleform.CommandArgsParser import CommandArgsParser
from gui.Scaleform.utils import dossiers_utils
from gui.Scaleform.utils.RareAchievementsCache import g_rareAchievesCache
from messenger import g_settings, LAZY_CHANNELS, MESSAGE_MAX_LENGTH, MESSENGER_I18N_FILE
from messenger import isBroadcatInCooldown, BROADCAST_COOL_DOWN_MESSAGE
from messenger.ChannelsManager import CREATE_CHANNEL_RESULT
from messenger.gui.interfaces import MessengerWindowInterface
from messenger.gui.Scalefrom.FAQInterface import FAQInterface
from messenger.gui.Scalefrom import C_COMMANDS, CHMS_COMMANDS, WP_COMMANDS
from messenger.gui.Scalefrom import lobby_page_interfaces as pages
from messenger.gui.Scalefrom.InvitesInterface import InvitesInterface
from messenger.gui.Scalefrom.JoinedChannelsInterface import JoinedChannelsInterface
from messenger.gui.Scalefrom.search_interfaces import SearchChannelsInterface, SearchUsersInterface
from messenger.gui.Scalefrom.ServiceChannelInterface import ServiceChannelInterface
from messenger.gui.Scalefrom.users_interfaces import UsersRosterInterface
import weakref
import BigWorld
import constants
from adisp import process

class MessengerLobbyInterface(MessengerWindowInterface):
    _MessengerLobbyInterface__channelsWindow = { }
    _MessengerLobbyInterface__managementWindow = { }
    
    def __init__(self):
        self._MessengerLobbyInterface__active = False
        self._MessengerLobbyInterface__isCensored = True
        self._MessengerLobbyInterface__initCallbacks = False
        self._MessengerLobbyInterface__movieViewHandler = None
        self._MessengerLobbyInterface__channelPages = { }
        self._MessengerLobbyInterface__joinedChannels = JoinedChannelsInterface()
        self._MessengerLobbyInterface__searchChannels = SearchChannelsInterface()
        self._MessengerLobbyInterface__searchUsers = SearchUsersInterface()
        self._MessengerLobbyInterface__usersRoster = UsersRosterInterface()
        self._MessengerLobbyInterface__serviceChannel = ServiceChannelInterface()
        self._MessengerLobbyInterface__invitesInterface = InvitesInterface()
        self._MessengerLobbyInterface__faq = FAQInterface()

    
    def populateUI(self, handler):
        self.show()
        persistens = g_settings.userPreferences['windowsPersistens']
        self._MessengerLobbyInterface__channelsWindow = persistens['channels']
        self._MessengerLobbyInterface__managementWindow = persistens['management']
        self._MessengerLobbyInterface__isCensored = g_settings.userPreferences['enableOlFilter']
        proxy = weakref.proxy(handler)
        self._MessengerLobbyInterface__movieViewHandler = proxy
        self._MessengerLobbyInterface__initCallbacks = True
        self._MessengerLobbyInterface__joinedChannels.populateUI(proxy)
        for page in self._MessengerLobbyInterface__channelPages.values():
            page.populateUI(self._MessengerLobbyInterface__movieViewHandler)
        
        channelsInfo = (filter,)((lambda item: item.cid not in self._MessengerLobbyInterface__channelPages.keys()), self.channels.getChannelList())
        for info in channelsInfo:
            self._MessengerLobbyInterface__createChannelPage(info)
        
        self._MessengerLobbyInterface__searchChannels.populateUI(proxy)
        self._MessengerLobbyInterface__searchUsers.populateUI(proxy)
        self._MessengerLobbyInterface__usersRoster.populateUI(proxy)
        self._MessengerLobbyInterface__serviceChannel.populateUI(proxy)
        self._MessengerLobbyInterface__invitesInterface.populateUI(proxy)
        self._MessengerLobbyInterface__faq.populateUI(proxy)
        self._MessengerLobbyInterface__onReceiveLazyChannels(self.channels.getLazyChannelList())
        self.channels.onConnectingToSecureChannel += self._MessengerLobbyInterface__onConnectingToSecureChannel
        self.channels.onReceiveLazyChannels += self._MessengerLobbyInterface__onReceiveLazyChannels
        self.users.onUsersRosterUpdate += self._MessengerLobbyInterface__onUsersRosterUpdate
        self.users.onDenunciationReceived += self._MessengerLobbyInterface__onDenunciationReceived
        self.users.onAccountDossierRequest += self.onAccountDossierRequest
        self.users.onVehicleDossierRequest += self.onVehicleDossierRequest
        g_rareAchievesCache.onTextReceived += self.onRareDataReceived
        g_rareAchievesCache.onImageReceived += self.onRareDataReceived
        g_settings.onApplyUserPreferences += self._MessengerLobbyInterface__onApplyUserPreferences
        self._MessengerLobbyInterface__movieViewHandler.addExternalCallbacks({
            C_COMMANDS.PopulateUI(): self.onPopulateUI,
            C_COMMANDS.JoinToChannel(): self.onJoinToChannel,
            CHMS_COMMANDS.CheckCooldownPeriod(): self.onCheckCooldownPeriod,
            C_COMMANDS.CreateChannel(): self.onCreateChannel,
            C_COMMANDS.CreateChannelClientError(): self.onCreateChannelClientError,
            WP_COMMANDS.RequestChannelsPersistents(): self.onRequestChannelsPersistents,
            WP_COMMANDS.SetChannelPersistent(): self.onSetChannelPersistent,
            WP_COMMANDS.RequestManagementPersistents(): self.onRequestManagementPersistents,
            WP_COMMANDS.SetManagementPersistent(): self.onSetManagementPersistent,
            'userInfo.close': self.onUserInfoClose })
        self._MessengerLobbyInterface__movieViewHandler.call(C_COMMANDS.RefreshUI(), [
            MESSAGE_MAX_LENGTH])

    
    def dispossessUI(self):
        self.close()
        self._MessengerLobbyInterface__storeWindowsPersistent()
        self.channels.onConnectingToSecureChannel -= self._MessengerLobbyInterface__onConnectingToSecureChannel
        self.channels.onReceiveLazyChannels -= self._MessengerLobbyInterface__onReceiveLazyChannels
        g_rareAchievesCache.onImageReceived -= self.onRareDataReceived
        g_rareAchievesCache.onTextReceived -= self.onRareDataReceived
        self.users.onAccountDossierRequest -= self.onAccountDossierRequest
        self.users.onVehicleDossierRequest -= self.onVehicleDossierRequest
        self.users.onDenunciationReceived -= self._MessengerLobbyInterface__onDenunciationReceived
        self.users.onUsersRosterUpdate -= self._MessengerLobbyInterface__onUsersRosterUpdate
        g_settings.onApplyUserPreferences -= self._MessengerLobbyInterface__onApplyUserPreferences
        self._MessengerLobbyInterface__movieViewHandler.removeExternalCallbacks(C_COMMANDS.PopulateUI(), C_COMMANDS.CreateChannel(), C_COMMANDS.CreateChannelClientError(), C_COMMANDS.JoinToChannel(), CHMS_COMMANDS.CheckCooldownPeriod(), WP_COMMANDS.RequestChannelsPersistents(), WP_COMMANDS.SetChannelPersistent(), WP_COMMANDS.RequestManagementPersistents(), WP_COMMANDS.SetManagementPersistent(), 'userInfo.close')
        self._MessengerLobbyInterface__movieViewHandler = None
        for page in self._MessengerLobbyInterface__channelPages.values():
            page.dispossessUI()
        
        self._MessengerLobbyInterface__joinedChannels.dispossessUI()
        self._MessengerLobbyInterface__searchChannels.dispossessUI()
        self._MessengerLobbyInterface__searchUsers.dispossessUI()
        self._MessengerLobbyInterface__usersRoster.dispossessUI()
        self._MessengerLobbyInterface__serviceChannel.dispossessUI()
        self._MessengerLobbyInterface__invitesInterface.dispossessUI()
        self._MessengerLobbyInterface__faq.dispossessUI()

    
    def show(self):
        self._MessengerLobbyInterface__active = True

    
    def close(self):
        self._MessengerLobbyInterface__active = False

    
    def clear(self):
        for (_, page) in self._MessengerLobbyInterface__channelPages.iteritems():
            page.clear()
        
        self._MessengerLobbyInterface__channelPages.clear()
        self._MessengerLobbyInterface__joinedChannels.clear()
        self.channels.onConnectingToSecureChannel -= self._MessengerLobbyInterface__onConnectingToSecureChannel
        self.channels.onReceiveLazyChannels -= self._MessengerLobbyInterface__onReceiveLazyChannels
        self.users.onAccountDossierRequest -= self.onAccountDossierRequest
        self.users.onVehicleDossierRequest -= self.onVehicleDossierRequest
        self.users.onDenunciationReceived -= self._MessengerLobbyInterface__onDenunciationReceived
        self.users.onUsersRosterUpdate -= self._MessengerLobbyInterface__onUsersRosterUpdate

    
    def getChannelPage(self, cid):
        return self._MessengerLobbyInterface__channelPages.get(cid)

    
    def addChannelMessage(self, message):
        cid = message.channel
        page = self.getChannelPage(cid)
        messageText = None
        if page:
            messageText = page.addMessage(message, format = True)
            if not (self._MessengerLobbyInterface__active) and self.channels.proxyToBattle(cid):
                self._dispatcherProxy.battleMessenger.addChannelMessage(message)
            elif not self.channels.isLazyChannel(cid) and not (self._MessengerLobbyInterface__active):
                self._MessengerLobbyInterface__joinedChannels.waiting(cid)
            
        
        return messageText

    
    def addSystemMessage(self, message):
        page = self.getChannelPage(message.channel)
        if page:
            page.addMessage(message, format = False, system = True)
        

    
    def addChannel(self, channel):
        if self._MessengerLobbyInterface__initCallbacks:
            self._MessengerLobbyInterface__joinedChannels.refresh()
        
        self._MessengerLobbyInterface__createChannelPage(channel)
        if not (self._MessengerLobbyInterface__active) and self.channels.proxyToBattle(channel.cid):
            self._dispatcherProxy.battleMessenger.addChannel(channel)
        
        return True

    
    def removeChannel(self, cid):
        page = self.getChannelPage(cid)
        if page:
            page.clear()
            self._MessengerLobbyInterface__channelPages.pop(cid)
        
        if self._MessengerLobbyInterface__initCallbacks:
            self._MessengerLobbyInterface__joinedChannels.remove(cid)
        

    
    def _MessengerLobbyInterface__createChannelPage(self, channel):
        cid = channel.cid
        if not self.getChannelPage(cid):
            clazz = pages.CommonPageInterface
            if channel.isClan:
                clazz = pages.ClanPageInterface
            elif channel.isSquad:
                clazz = pages.SquadPageInterface
            elif channel.isCompany:
                clazz = pages.CompanyPageInterface
            elif channel.isBattleSession:
                clazz = pages.BattleSessionPageInterface
            
            self._MessengerLobbyInterface__channelPages[cid] = clazz(cid)
            if self._MessengerLobbyInterface__initCallbacks and self._MessengerLobbyInterface__movieViewHandler:
                self._MessengerLobbyInterface__channelPages[cid].populateUI(self._MessengerLobbyInterface__movieViewHandler)
            
        

    
    def _MessengerLobbyInterface__createLazyChannelPage(self, channel):
        cid = channel.cid
        if not self.getChannelPage(cid):
            clazz = pages.LazyPageInterface
            if channel.lazy == LAZY_CHANNELS.COMPANIES[0]:
                clazz = pages.CompaniesPageInterface
            elif channel.lazy == LAZY_CHANNELS.SPECIAL_BATTLES[0]:
                clazz = pages.BattleSessionsPageInterface
            
            self._MessengerLobbyInterface__channelPages[cid] = clazz(cid)
            if self._MessengerLobbyInterface__movieViewHandler:
                self._MessengerLobbyInterface__channelPages[cid].populateUI(self._MessengerLobbyInterface__movieViewHandler)
            
        
        self._MessengerLobbyInterface__channelPages[cid].setJoined(channel.joined)

    
    def showActionFailureMessage(self, message, title = None, modal = False):
        if modal and self._MessengerLobbyInterface__movieViewHandler:
            self._MessengerLobbyInterface__movieViewHandler.call(C_COMMANDS.AlertReceived(), [
                'error',
                title,
                message])
        else:
            SystemMessages.pushMessage(message, type = SystemMessages.SM_TYPE.Error)

    
    def setJoinedToLazyChannel(self, cid, joined):
        page = self.getChannelPage(cid)
        if page is not None:
            page.setJoined(joined)
        

    
    def refreshChannelList(self):
        self._MessengerLobbyInterface__joinedChannels.refresh()

    
    def onRareDataReceived(self, id, *args):
        for (userName, dossier) in dossiers_utils.g_dossiersCache.iteritems():
            None((None, BigWorld.callback, 3), (lambda : self._MessengerLobbyInterface__movieViewHandler.call(C_COMMANDS.UpdateActionMedal() + userName, dossiers_utils.getRareAchievementMedalData(None, id))))
        

    
    def onAccountDossierRequest(self, user):
        r = dossiers_utils.getUserDossier(user.userName)
        yield r.getAccountDossier()
        dossier = None
        if dossier is None:
            if r.isHidden:
                self._MessengerLobbyInterface__movieViewHandler.call(C_COMMANDS.ReceivedUserInfoFailed(), [
                    i18n.makeString('#dialogs:messenger/userInfoHidden/message') % user.userName])
            else:
                self._MessengerLobbyInterface__movieViewHandler.call('common.showMessageDialog', [
                    'messenger/userInfoNotAvailable',
                    True,
                    False,
                    i18n.makeString('#dialogs:messenger/userInfoNotAvailable/message') % user.userName])
            return None
        yield r.getClanInfo()
        (clanDBID, clanInfo) = dossier is None
        g_rareAchievesCache.request(dossier['rareAchievements'])
        title = i18n.makeString('#%s:dialogs/userInfo/title' % MESSENGER_I18N_FILE, user.displayName)
        userInfo = user.list()
        userInfo = [
            title,
            int(userInfo[0])] + userInfo[1:]
        vehList = dossiers_utils.getDossierVehicleList(dossier)
        userInfo.extend([
            dossier['creationTime'],
            dossier['lastBattleTime'],
            len(vehList)])
        userInfo.extend(vehList)
        achievList = dossiers_utils.getDossierMedals(dossier)
        userInfo.extend([
            len(achievList)])
        userInfo.extend(achievList)
        statsList = dossiers_utils.getDossierTotalBlocks(dossier)
        userInfo.extend([
            len(statsList)])
        userInfo.extend(statsList)
        userInfo.extend(dossiers_utils.getCommonInfo(user.userName, dossier, clanInfo, None))
        self._MessengerLobbyInterface__movieViewHandler.call(C_COMMANDS.ReceivedUserInfo(), userInfo)
        if clanDBID is not None and clanDBID != 0:
            tID = 'userInfoForm' + BigWorld.player().name
            yield dossiers_utils.getClanEmblemTextureID(clanDBID, True, tID)
            success = None
            if success:
                self._MessengerLobbyInterface__movieViewHandler.call(C_COMMANDS.ReceivedClanEmblem() + user.userName, [
                    tID])
            
        

    onAccountDossierRequest = process(onAccountDossierRequest)
    
    def onVehicleDossierRequest(self, user, vehicleID):
        r = dossiers_utils.getUserDossier(user.userName)
        if vehicleID == 'ALL':
            yield r.getAccountDossier()
            dossier = None
            data = dossiers_utils.getDossierTotalBlocks(dossier)
            dossierType = constants.DOSSIER_TYPE.ACCOUNT
        else:
            yield r.getVehicleDossier(int(float(vehicleID)))
            dossier = None
            data = dossiers_utils.getDossierVehicleBlocks(dossier, int(float(vehicleID)))
            dossierType = constants.DOSSIER_TYPE.VEHICLE
        self._MessengerLobbyInterface__movieViewHandler.call(C_COMMANDS.ReceivedVehicleStat() + user.userName, data)
        self._MessengerLobbyInterface__movieViewHandler.call(C_COMMANDS.ReceivedAchievementsStat() + user.userName, dossiers_utils.getDossierMedals(dossier, dossierType))

    onVehicleDossierRequest = process(onVehicleDossierRequest)
    
    def onUserInfoClose(self, cid, userName):
        LOG_DEBUG('Close user dossier cache: %s' % str(userName))
        dossiers_utils.closeUserDossier(userName)

    
    def onPopulateUI(self, *args):
        settings = g_settings.lobbySettings
        userPrefs = g_settings.userPreferences
        parser = CommandArgsParser(self.onPopulateUI.__name__)
        parser.parse(*args)
        parser.addArg(MESSAGE_MAX_LENGTH)
        parser.addArgs([
            settings['popUpMessageLifeTime'],
            settings['popUpMessageAlphaSpeed'],
            settings['popUpMessageStackLength']])
        parser.addArgs([
            userPrefs['enableStoreMws'],
            userPrefs['enableStoreCws']])
        self._MessengerLobbyInterface__movieViewHandler.respond(parser.args())

    
    def onCheckCooldownPeriod(self, *args):
        parser = CommandArgsParser(self.onCheckCooldownPeriod.__name__, 1)
        (cid,) = parser.parse(*args)
        flag = isBroadcatInCooldown()
        parser.addArg(not flag)
        self._MessengerLobbyInterface__movieViewHandler.respond(parser.args())
        if flag:
            self._MessengerLobbyInterface__movieViewHandler.call(CHMS_COMMANDS.RecieveMessage(), [
                cid,
                BROADCAST_COOL_DOWN_MESSAGE,
                False])
        

    
    def onCreateChannelClientError(self, *args):
        parser = CommandArgsParser(self.onCreateChannelClientError.__name__, 1, [
            str])
        (messageKey,) = parser.parse(*args)
        SystemMessages.pushI18nMessage(messageKey, type = SystemMessages.SM_TYPE.Error)

    
    def onCreateChannel(self, *args):
        parser = CommandArgsParser(self.onCreateChannel.__name__, 2, [
            str,
            str])
        (channelName, password) = parser.parse(*args)
        channelName = ' '.join(filter((lambda word: len(word)), channelName.split(' ')))
        result = self.channels.createChannel(channelName, password)
        if result == CREATE_CHANNEL_RESULT.activeChannelLimitReached:
            key = '#%s:dialogs/createChannel/errors/activeChannelLimitReached/message' % MESSENGER_I18N_FILE
            SystemMessages.pushI18nMessage(key, type = SystemMessages.SM_TYPE.Error)
        

    
    def onJoinToChannel(self, *args):
        parser = CommandArgsParser(self.onJoinToChannel.__name__, 2, [
            long,
            str])
        (cid, password) = parser.parse(*args)
        self.channels.joinToChannel(cid, password)

    
    def onRequestChannelsPersistents(self, *args):
        '''
\t\tReturn the list of channels windows persistent, saved from previous sessions
\t\t'''
        parser = CommandArgsParser(self.onRequestChannelsPersistents.__name__)
        parser.parse(*args)
        for (channelId, persistent) in self._MessengerLobbyInterface__channelsWindow.iteritems():
            parser.addArg(channelId, int)
            parser.addArgs(persistent)
        
        self._MessengerLobbyInterface__movieViewHandler.respond(parser.args())

    
    def onSetChannelPersistent(self, *args):
        '''
\t\tWhen you close the channel window if the size and position of the window
\t\tis different from the default, than save
\t\t'''
        parser = CommandArgsParser(self.onSetChannelPersistent.__name__, 5, [
            int,
            float,
            float,
            float,
            float])
        (channelId, x, y, width, height) = parser.parse(*args)
        self._MessengerLobbyInterface__channelsWindow[channelId] = (x, y, width, height)

    
    def onRequestManagementPersistents(self, *args):
        '''
\t\tReturn the list of management windows persistent, saved from previous sessions
\t\t'''
        parser = CommandArgsParser(self.onRequestManagementPersistents.__name__)
        parser.parse(*args)
        for (windowName, persistent) in self._MessengerLobbyInterface__managementWindow.iteritems():
            parser.addArg(windowName, str)
            parser.addArgs(persistent)
        
        self._MessengerLobbyInterface__movieViewHandler.respond(parser.args())

    
    def onSetManagementPersistent(self, *args):
        '''
\t\tWhen you close the management window if the size and position of the window
\t\tis different from the default, than save
\t\t'''
        parser = CommandArgsParser(self.onSetManagementPersistent.__name__, 5, [
            str,
            float,
            float,
            float,
            float])
        (windowName, x, y, width, height) = parser.parse(*args)
        self._MessengerLobbyInterface__managementWindow[windowName] = (x, y, width, height)

    
    def _MessengerLobbyInterface__filterChannelWindowsPersistents(self):
        '''
\t\tFiltered list of windows persistent.
\t\tOnly returns the window channels, which are joined.
\t\t'''
        joinedChannels = self.channels.getChannelList(joined = True, isBattle = False)
        filtered = { }
        if len(joinedChannels):
            for channel in joinedChannels:
                cid = channel.cid
                if self._MessengerLobbyInterface__channelsWindow.has_key(cid):
                    filtered[cid] = self._MessengerLobbyInterface__channelsWindow[cid]
                    continue
            
        else:
            filtered = self._MessengerLobbyInterface__channelsWindow
        return filtered

    
    def _MessengerLobbyInterface__storeWindowsPersistent(self):
        
        try:
            path = '_root._level0.lobbyMessengerLoader.flushManagementWindows'
            managementStr = self._MessengerLobbyInterface__movieViewHandler.movie.invoke((path,))
            if len(managementStr):
                pass
            1
            args = []
            for idx in xrange(0, len(args), 5):
                self._MessengerLobbyInterface__managementWindow[str(args[idx])] = (float(args[idx + 1]), float(args[idx + 2]), float(args[idx + 3]), float(args[idx + 4]))
        except AttributeError:
            LOG_ERROR('Error when flushing opened management windows in chat')

        
        try:
            path = '_root._level0.lobbyMessengerLoader.flushChannelsWindows'
            channelsStr = self._MessengerLobbyInterface__movieViewHandler.movie.invoke((path,))
            if len(channelsStr):
                pass
            1
            args = []
            for idx in xrange(0, len(args), 5):
                self._MessengerLobbyInterface__channelsWindow[long(args[idx])] = (float(args[idx + 1]), float(args[idx + 2]), float(args[idx + 3]), float(args[idx + 4]))
        except AttributeError:
            LOG_ERROR('Error when flushing opened channels windows in chat')

        g_settings.applyWindowPersistens(self._MessengerLobbyInterface__managementWindow, self._MessengerLobbyInterface__filterChannelWindowsPersistents())

    
    def _MessengerLobbyInterface__onReceiveLazyChannels(self, channels):
        for channel in channels:
            if channel.lazy:
                self._MessengerLobbyInterface__createLazyChannelPage(channel)
                continue
        
        self._MessengerLobbyInterface__joinedChannels.refresh()

    
    def _MessengerLobbyInterface__onConnectingToSecureChannel(self, channel):
        channelInfo = i18n.convert(i18n.makeString('#%s:dialogs/connectingToSecureChannel/labels/info' % MESSENGER_I18N_FILE, channel.channelName))
        self._MessengerLobbyInterface__movieViewHandler.call(C_COMMANDS.ConnectToSecureChannel(), [
            channel.cid,
            channelInfo])

    
    def _MessengerLobbyInterface__onDenunciationReceived(self, userName, topicID):
        topicStr = i18n.makeString('#menu:denunciation/type%d' % topicID)
        SystemMessages.pushMessage(i18n.makeString('#system_messages:denunciation/success') % {
            'name': userName,
            'topic': topicStr }, type = SystemMessages.SM_TYPE.Information)

    
    def _MessengerLobbyInterface__onUsersRosterUpdate(self, action, user):
        for (_, page) in self._MessengerLobbyInterface__channelPages.iteritems():
            page.refreshMemberList()
        

    
    def _MessengerLobbyInterface__onApplyUserPreferences(self):
        userPreferences = g_settings.userPreferences
        persistens = userPreferences['windowsPersistens']
        enableStoreMws = userPreferences['enableStoreMws']
        enableStoreCws = userPreferences['enableStoreCws']
        self._MessengerLobbyInterface__channelsWindow = persistens['channels']
        self._MessengerLobbyInterface__managementWindow = persistens['management']
        self._MessengerLobbyInterface__movieViewHandler.call(WP_COMMANDS.SetEnableStorePersistents(), [
            enableStoreMws,
            enableStoreCws])
        if self._MessengerLobbyInterface__isCensored != g_settings.userPreferences['enableOlFilter']:
            self._MessengerLobbyInterface__joinedChannels.updateChannelWrappers()
            self._MessengerLobbyInterface__isCensored = not (self._MessengerLobbyInterface__isCensored)
            self.refreshChannelList()
        



