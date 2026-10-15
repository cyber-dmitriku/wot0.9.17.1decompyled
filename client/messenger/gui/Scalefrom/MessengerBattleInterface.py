# Source Generated with Decompyle++
# File: MessengerBattleInterface.pyc (Python 2.6)

from debug_utils import LOG_DEBUG
from gui.Scaleform.CommandArgsParser import CommandArgsParser
from messenger import isBroadcatInCooldown, BROADCAST_COOL_DOWN_MESSAGE
from messenger import MESSENGER_I18N_FILE, BATTLE_CHANNELS
from helpers import i18n
from messenger import MESSAGE_MAX_LENGTH_IN_BATTLE, g_settings
from messenger.UsersManager import USERS_ROSTER_ACTIONS, UsersManager
from messenger.gui.Scalefrom import battle_page_interfaces as battle_pages
from messenger.gui.interfaces import MessengerWindowInterface
from messenger.gui.Scalefrom import BTMS_COMMANDS
import VOIP
import BattleReplay

class MessengerBattleInterface(MessengerWindowInterface):
    _MessengerBattleInterface__userTransferUserMsgKeys = {
        USERS_ROSTER_ACTIONS.AddToFriend: '#{0:>s}:client/information/addToFriends/message'.format(MESSENGER_I18N_FILE),
        USERS_ROSTER_ACTIONS.AddToIgnored: '#{0:>s}:client/information/addToIgnored/message'.format(MESSENGER_I18N_FILE),
        USERS_ROSTER_ACTIONS.RemoveFromFriend: '#{0:>s}:client/information/removeFromFriends/message'.format(MESSENGER_I18N_FILE),
        USERS_ROSTER_ACTIONS.RemoveFromIgnored: '#{0:>s}:client/information/removeFromIgnored/message'.format(MESSENGER_I18N_FILE) }
    
    def __init__(self):
        self._MessengerBattleInterface__channelPages = { }
        self._MessengerBattleInterface__ui = None
        self._MessengerBattleInterface__focused = False
        self._initialized = 0

    
    def start(self, parentUI):
        self.channels.exitFromAllLazyChannels()
        self.users.onUsersRosterUpdate += self._MessengerBattleInterface__onUsersRosterUpdate
        self._MessengerBattleInterface__ui = parentUI
        self._MessengerBattleInterface__ui.addExternalCallbacks({
            BTMS_COMMANDS.PopulateUI(): self._MessengerBattleInterface__onPopulateUI,
            BTMS_COMMANDS.CheckCooldownPeriod(): self._MessengerBattleInterface__onCheckCooldownPeriod,
            BTMS_COMMANDS.SendMessage(): self._MessengerBattleInterface__onSendChannelMessage,
            BTMS_COMMANDS.ChangeFocus(): self._MessengerBattleInterface__onChangeFocus,
            BTMS_COMMANDS.AddToFriends(): self._MessengerBattleInterface__onAddToFriends,
            BTMS_COMMANDS.RemoveFromFriends(): self._MessengerBattleInterface__onRemoveFromFriends,
            BTMS_COMMANDS.AddToIgnored(): self._MessengerBattleInterface__onAddToIgnored,
            BTMS_COMMANDS.RemoveFromIgnored(): self._MessengerBattleInterface__onRemoveFromIgnored,
            BTMS_COMMANDS.AddMuted(): self._MessengerBattleInterface__onSetMuted,
            BTMS_COMMANDS.RemoveMuted(): self._MessengerBattleInterface__onUnsetMuted,
            BTMS_COMMANDS.ReceiverChanged(): self._MessengerBattleInterface__onReceiverChanged })
        squad = self.channels.getSquadChannel()
        if squad:
            self.addChannel(squad)
        
        self._MessengerBattleInterface__flashCall(BTMS_COMMANDS.RefreshUI())
        if self._initialized == BATTLE_CHANNELS.INITIALIZED:
            self.enable()
        

    
    def destroy(self):
        self._MessengerBattleInterface__flashCall(BTMS_COMMANDS.ClearMessages())
        self.users.onUsersRosterUpdate -= self._MessengerBattleInterface__onUsersRosterUpdate
        if self._MessengerBattleInterface__ui:
            self._MessengerBattleInterface__ui.removeExternalCallbacks(BTMS_COMMANDS.PopulateUI(), BTMS_COMMANDS.CheckCooldownPeriod(), BTMS_COMMANDS.SendMessage(), BTMS_COMMANDS.ChangeFocus(), BTMS_COMMANDS.AddToFriends(), BTMS_COMMANDS.RemoveFromFriends(), BTMS_COMMANDS.AddToIgnored(), BTMS_COMMANDS.RemoveFromIgnored(), BTMS_COMMANDS.AddMuted(), BTMS_COMMANDS.RemoveMuted(), BTMS_COMMANDS.ReceiverChanged())
        
        self._MessengerBattleInterface__ui = None

    
    def _MessengerBattleInterface__onUsersRosterUpdate(self, action, user):
        messageKey = self._MessengerBattleInterface__userTransferUserMsgKeys.get(action)
        if messageKey is not None:
            self.showActionFailureMessage(i18n.makeString(messageKey) % user.userName)
        

    
    def updateColors(self, **kwargs):
        battle_pages.updateColors(**None)
        args = []
        for (cid, page) in self._MessengerBattleInterface__channelPages.iteritems():
            args.append(cid)
            args.append(page.getRecvConfig()[0])
        
        if len(args):
            self._MessengerBattleInterface__flashCall(BTMS_COMMANDS.UpdateReceivers(), args)
        

    
    def enable(self):
        if BattleReplay.g_replayCtrl.isPlaying:
            return None
        self.users.requestUsersRoster()
        self._MessengerBattleInterface__flashCall(BTMS_COMMANDS.ChannelsInit())

    
    def show(self):
        pass

    
    def close(self):
        self.clear()

    
    def getChannelPage(self, cid):
        if cid in self._MessengerBattleInterface__channelPages:
            return self._MessengerBattleInterface__channelPages[cid]

    
    def addChannel(self, channel):
        result = False
        page = None
        cid = channel.cid
        if cid not in self._MessengerBattleInterface__channelPages:
            page = battle_pages.create(channel)
        
        if page:
            self._MessengerBattleInterface__channelPages[cid] = page
            self._initialized |= page._initFlag
            result = True
            args = page.getRecvConfig()[:]
            args.insert(0, cid)
            self._MessengerBattleInterface__flashCall(BTMS_COMMANDS.JoinToChannel(), args)
            if self._initialized == BATTLE_CHANNELS.INITIALIZED:
                self.enable()
            
        
        return result

    
    def removeChannel(self, cid):
        result = False
        if cid in self._MessengerBattleInterface__channelPages:
            self._MessengerBattleInterface__channelPages.pop(cid)
            result = True
        
        return result

    
    def addChannelMessage(self, message, targetIsCurrentPlayer = False):
        cid = message.channel
        messageText = ''
        if cid in self._MessengerBattleInterface__channelPages:
            messageText = self._MessengerBattleInterface__channelPages[cid].addMessage(message, playerIsTarget = targetIsCurrentPlayer)
        else:
            messageText = battle_pages.addDefMessage(message)
        self._MessengerBattleInterface__flashCall(BTMS_COMMANDS.RecieveMessage(), [
            message.channel,
            messageText,
            UsersManager.isCurrentPlayer(message.originator),
            targetIsCurrentPlayer])
        if BattleReplay.g_replayCtrl.isRecording:
            BattleReplay.g_replayCtrl.onBattleChatMessage(messageText, UsersManager.isCurrentPlayer(message.originator), targetIsCurrentPlayer)
        
        return messageText

    
    def addFormattedMessage(self, messageText, isCurrentPlayer, targetIsCurrentPlayer = False):
        self._MessengerBattleInterface__flashCall(BTMS_COMMANDS.RecieveMessage(), [
            0,
            messageText,
            isCurrentPlayer,
            targetIsCurrentPlayer])

    
    def addSystemMessage(self, message):
        pass

    
    def clear(self):
        self._MessengerBattleInterface__channelPages.clear()
        self._initialized = 0
        battle_pages.storeReceiver4NextBattles()

    
    def editing(self):
        return self._MessengerBattleInterface__focused

    
    def showActionFailureMessage(self, message, title = None, modal = False):
        self._MessengerBattleInterface__flashCall(BTMS_COMMANDS.ShowActionFailureMessage(), [
            g_settings.htmlTemplates.format('battleErrorMessage', ctx = {
                'error': message })])

    
    def _MessengerBattleInterface__flashCall(self, funcName, args = None):
        if self._MessengerBattleInterface__ui:
            self._MessengerBattleInterface__ui.call(funcName, args)
        

    
    def _MessengerBattleInterface__flashRespond(self, args = None):
        self._MessengerBattleInterface__ui.respond(args)

    
    def _MessengerBattleInterface__onChangeFocus(self, _, focused):
        LOG_DEBUG('[BattleMessanger]', '__onChangeFocus = %s' % focused)
        if focused:
            responseHandler = VOIP.getResponseHandler()
            if responseHandler is not None and responseHandler.channelsMgr.currentChannel:
                responseHandler.setMicMute(muted = True)
            
        
        self._MessengerBattleInterface__focused = focused

    
    def _MessengerBattleInterface__onPopulateUI(self, *args):
        LOG_DEBUG('[BattleMessanger]', '__onPopulateUI')
        settings = g_settings.battleSettings
        parser = CommandArgsParser(self._MessengerBattleInterface__onPopulateUI.__name__)
        parser.parse(*args)
        parser.addArgs([
            settings['messageLifeTime'],
            settings['messageAlphaSpeed'],
            settings['inactiveStateAlpha'],
            MESSAGE_MAX_LENGTH_IN_BATTLE,
            settings['hintText'],
            settings['toolTipText']])
        self._MessengerBattleInterface__flashRespond(parser.args())

    
    def _MessengerBattleInterface__onCheckCooldownPeriod(self, *args):
        LOG_DEBUG('[BattleMessanger]', '__onCheckCooldownPeriod')
        parser = CommandArgsParser(self._MessengerBattleInterface__onCheckCooldownPeriod.__name__, 1, [
            long])
        (cid,) = parser.parse(*args)
        flag = isBroadcatInCooldown()
        parser.addArgs([
            cid,
            not flag])
        self._MessengerBattleInterface__flashRespond(parser.args())
        if flag:
            message = g_settings.htmlTemplates.format('battleErrorMessage', ctx = {
                'error': BROADCAST_COOL_DOWN_MESSAGE })
            self._MessengerBattleInterface__flashCall(BTMS_COMMANDS.RecieveMessage(), [
                cid,
                message,
                False])
        

    
    def _MessengerBattleInterface__onSendChannelMessage(self, *args):
        LOG_DEBUG('[BattleMessanger]', '__onSendChannelMessage')
        parser = CommandArgsParser(self._MessengerBattleInterface__onSendChannelMessage.__name__, 2, [
            long])
        (cid, rawMsgText) = parser.parse(*args)
        self._dispatcherProxy.handleChannelMessageInput(cid, rawMsgText, isBattle = True)
        self.focused = False

    
    def _MessengerBattleInterface__onAddToFriends(self, _, uid, userName):
        self.users.addFriend(uid, userName)

    
    def _MessengerBattleInterface__onRemoveFromFriends(self, _, uid):
        self.users.removeFriend(uid)

    
    def _MessengerBattleInterface__onAddToIgnored(self, _, uid, userName):
        self.users.addIgnored(uid, userName)

    
    def _MessengerBattleInterface__onRemoveFromIgnored(self, _, uid):
        self.users.removeIgnored(uid)

    
    def _MessengerBattleInterface__onSetMuted(self, _, uid, userName):
        self.users.setMuted(uid, userName)

    
    def _MessengerBattleInterface__onUnsetMuted(self, _, uid):
        self.users.unsetMuted(uid)

    
    def _MessengerBattleInterface__onReceiverChanged(self, *args):
        LOG_DEBUG('__onReceiverChanged', args)
        parser = CommandArgsParser(self._MessengerBattleInterface__onReceiverChanged.__name__, 1, [
            long])
        (cid,) = parser.parse(*args)
        if cid in self._MessengerBattleInterface__channelPages:
            self._MessengerBattleInterface__channelPages[cid].setCurrent()
        



