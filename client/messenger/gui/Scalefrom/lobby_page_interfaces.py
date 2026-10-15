# Source Generated with Decompyle++
# File: lobby_page_interfaces.pyc (Python 2.6)

import account_helpers
import BigWorld
import constants
import CurrentVehicle
from adisp import process
from debug_utils import LOG_WARNING, LOG_DEBUG
from gui.Scaleform.CommandArgsParser import CommandArgsParser
from gui.Scaleform.utils.requesters import StatsRequester
from gui.Scaleform.utils.functions import checkAmmoLevel
from messenger import MESSAGE_DATETIME_FORMAT_DICT, g_settings, passCensor
from messenger.SquadMembersListener import SquadMembersListener
from messenger.CompanyMembersListener import CompanyMembersListener
from messenger.BattleSessionMembersListener import BattleSessionMembersListener
from messenger.gui.interfaces import MessengerPageInterface
from messenger.gui.Scalefrom import CHMB_COMMANDS, CHMS_COMMANDS, JCH_COMMANDS, LAZY_CH_COMMANDS, SQUAD_CH_COMMANDS, TEAM_CH_COMMANDS, SQUAD_PRB_COMMANDS, TEAM_PRB_COMMANDS, BS_CH_COMMANDS, BS_PRB_COMMANDS
from messenger.gui.Scalefrom.search_interfaces import PrebattleSearchUsersInterface
from messenger.gui.Scalefrom.users_interfaces import PrebattleUsersRosterInterface
import functools
import time
from ConnectionManager import connectionManager
from gui.Scaleform import VoiceChatInterface
from predefined_hosts import g_preDefinedHosts
from gui import SystemMessages
from helpers import i18n

class _BasePageInterface(MessengerPageInterface):
    _isPopulated = False
    
    def __init__(self, channelId):
        self._cid = channelId
        self._movieViewHandler = None
        self._channelMessagesFunc = functools.partial(self.channels.getChannelMessages, channelId)
        self._BasePageInterface__sendMessageFunc = self._dispatcherProxy.handleChannelMessageInput
        self._BasePageInterface__tformat = MESSAGE_DATETIME_FORMAT_DICT[g_settings.userPreferences['datetimeIdx']]
        g_settings.onApplyUserPreferences += self._BasePageInterface__updateFormat

    
    def __del__(self):
        LOG_DEBUG('Deleted: %s' % self)

    
    def clear(self):
        self._cid = 0
        if self._isPopulated:
            self.dispossessUI()
        
        self._BasePageInterface__sendMessageFunc = None
        self._channelMessagesFunc = None
        g_settings.onApplyUserPreferences -= self._BasePageInterface__updateFormat

    
    def format(self, message, playerIsTarget = False, system = False):
        user = self.users.getUser(message.originator, message.originatorNickName)
        mformat = g_settings.getLobbyMsgFormat(message, user)
        return mformat % (message.originatorNickName, self._BasePageInterface__tformat(message.time), message.data)

    
    def addMessage(self, message, format = True, playerIsTarget = False, system = False):
        if format:
            pass
        1
        messageText = message.data
        if self._movieViewHandler:
            self._movieViewHandler.call(CHMS_COMMANDS.RecieveMessage(), [
                message.channel,
                messageText,
                not system])
        
        return messageText

    
    def addSystemMessage(self, message):
        if self._movieViewHandler:
            self._movieViewHandler.call(CHMS_COMMANDS.RecieveMessage(), [
                self._cid,
                message,
                False])
        

    
    def refreshMemberList(self):
        pass

    
    def open(self):
        if self._movieViewHandler:
            self._movieViewHandler.call(JCH_COMMANDS.OpenChannelPage(), [
                self._cid])
        

    
    def close(self):
        if self._movieViewHandler:
            self._movieViewHandler.call(JCH_COMMANDS.CloseChannelPage(), [
                self._cid])
        

    
    def _BasePageInterface__updateFormat(self):
        self._BasePageInterface__tformat = MESSAGE_DATETIME_FORMAT_DICT[g_settings.userPreferences['datetimeIdx']]

    
    def populateUI(self, handler):
        self._isPopulated = True
        self._movieViewHandler = handler
        self._movieViewHandler.addExternalCallbacks({
            CHMS_COMMANDS.SendMessage(): self.onSendChannelMessage,
            CHMS_COMMANDS.RequestMessageHistory(): self.onRequestChannelMessages })

    
    def dispossessUI(self):
        self._isPopulated = False
        self._movieViewHandler.removeExternalCallback(CHMS_COMMANDS.SendMessage(), self.onSendChannelMessage)
        self._movieViewHandler.removeExternalCallback(CHMS_COMMANDS.RequestMessageHistory(), self.onRequestChannelMessages)
        self._movieViewHandler = None

    
    def onSendChannelMessage(self, *args):
        parser = CommandArgsParser(self.onSendChannelMessage.__name__, 2, [
            long])
        (cid, rawMessageText) = parser.parse(*args)
        if cid == self._cid:
            self._BasePageInterface__sendMessageFunc(cid, rawMessageText)
        

    
    def onRequestChannelMessages(self, *args):
        parser = CommandArgsParser(self.onRequestChannelMessages.__name__, 1, [
            long])
        (cid,) = parser.parse(*args)
        if cid == self._cid:
            parser.addArg('\n'.join(self._channelMessagesFunc()))
            self._movieViewHandler.respond(parser.args())
        



class CommonPageInterface(_BasePageInterface):
    
    def __init__(self, channelId):
        _BasePageInterface.__init__(self, channelId)
        self._CommonPageInterface__memberCountFunc = functools.partial(self.channels.getMemberCount, channelId)
        self._CommonPageInterface__memberListFunc = functools.partial(self.channels.getMemberList, channelId)

    
    def clear(self):
        _BasePageInterface.clear(self)
        self._CommonPageInterface__memberCountFunc = None
        self._CommonPageInterface__memberListFunc = None

    
    def addMembers(self, members):
        return self.refreshMemberList()

    
    def addMember(self, member):
        return self.refreshMemberList()

    
    def removeMember(self, member):
        return self.refreshMemberList()

    
    def removeMembers(self, members):
        return self.refreshMemberList()

    
    def setMemberStatus(self, uid, status):
        self.refreshMemberList()

    
    def refreshMemberList(self):
        if self._movieViewHandler:
            self._movieViewHandler.call(CHMB_COMMANDS.RefreshList(), [
                self._CommonPageInterface__memberCountFunc(),
                self._cid])
        
        return True

    
    def populateUI(self, handler):
        _BasePageInterface.populateUI(self, handler)
        self._movieViewHandler.addExternalCallbacks({
            CHMB_COMMANDS.RequestLength(): self.onRequestMemberLength,
            CHMB_COMMANDS.RequestItemRange(): self.onRequestMemberItems })

    
    def dispossessUI(self):
        self._movieViewHandler.removeExternalCallback(CHMB_COMMANDS.RequestLength(), self.onRequestMemberLength)
        self._movieViewHandler.removeExternalCallback(CHMB_COMMANDS.RequestItemRange(), self.onRequestMemberItems)
        _BasePageInterface.dispossessUI(self)

    
    def onRequestMemberLength(self, *args):
        parser = CommandArgsParser(self.onRequestMemberLength.__name__, 1, [
            long])
        (cid,) = parser.parse(*args)
        if cid == self._cid:
            parser.addArg(self._CommonPageInterface__memberCountFunc())
            self._movieViewHandler.respond(parser.args())
        

    
    def onRequestMemberItems(self, *args):
        parser = CommandArgsParser(self.onRequestMemberItems.__name__, 3, [
            long,
            int,
            int])
        (cid, startIndex, endIndex) = parser.parse(*args)
        if cid == self._cid:
            list = sorted(self._CommonPageInterface__memberListFunc(), cmp = (lambda member, other: cmp(member.nickName.lower(), other.nickName.lower())))
            for item in list[startIndex:endIndex + 1]:
                user = self.users.getUser(item.uid, item.nickName)
                parser.addArgs(item + (item.status,), [
                    long])
                parser.addArgs([
                    user.roster,
                    user.himself,
                    ''])
                parser.addArgs(g_settings.getLobbyUserCS(user.roster, user.himself))
            
            self._movieViewHandler.respond(parser.args())
        



class ClanPageInterface(CommonPageInterface):
    
    def addMember(self, member):
        self.users.setClanMemberStatus(member.uid, True)
        return super(ClanPageInterface, self).addMember(member)

    
    def addMembers(self, members):
        uids = map((lambda member: member.uid), members)
        self.users.setClanMemberStatuses(uids, True)
        return super(ClanPageInterface, self).addMembers(members)

    
    def removeMember(self, member):
        self.users.setClanMemberStatus(member, False)
        return super(ClanPageInterface, self).removeMember(member)

    
    def removeMembers(self, members):
        uids = map((lambda member: member.uid), members)
        self.users.setClanMemberStatuses(uids, False)
        return super(ClanPageInterface, self).removeMembers(members)

    
    def setMemberStatus(self, uid, status):
        self.users.setClanMemberStatus(uid, status)
        super(ClanPageInterface, self).setMemberStatus(uid, status)



class SquadPageInterface(_BasePageInterface):
    
    def __init__(self, channelId):
        _BasePageInterface.__init__(self, channelId)
        self._SquadPageInterface__searchUsers = PrebattleSearchUsersInterface(prefix = 'Prebattle.Squad.SearchUsers')
        self._SquadPageInterface__contacts = PrebattleUsersRosterInterface(prefix = 'Prebattle.Squad')
        self._SquadPageInterface__firstTimeOpen = self._dispatcherProxy.requestCreatePrb == constants.PREBATTLE_TYPE.SQUAD

    
    def clear(self):
        _BasePageInterface.clear(self)
        self._SquadPageInterface__searchUsers = None
        self._SquadPageInterface__contacts = None

    
    def addMembers(self, members):
        return self.refreshMemberList()

    
    def addMember(self, member):
        return self.refreshMemberList()

    
    def removeMember(self, member):
        return self.refreshMemberList()

    
    def removeMembers(self, members):
        return self.refreshMemberList()

    
    def refreshMemberList(self):
        if self._movieViewHandler:
            self._movieViewHandler.call(SQUAD_CH_COMMANDS.SetPlayerRoles(), [
                self._sMemberListener.isCanSendInvite(),
                self._sMemberListener.isCanKick(),
                self._sMemberListener.isCreator(),
                self._sMemberListener.isPlayerReady(),
                self._sMemberListener.isTeamReady()])
            self._movieViewHandler.call(SQUAD_CH_COMMANDS.RefreshMemberList(), self._SquadPageInterface__getMembersList())
            self._SquadPageInterface__setReady()
        

    
    def _SquadPageInterface__comparator(self, player, other):
        if player.isCommander ^ other.isCommander:
            if player.isCommander:
                pass
            1
            result = 1
        else:
            result = cmp(player.time, other.time)
        return result

    
    def _SquadPageInterface__getMembersList(self):
        list = sorted(self._sMemberListener.getPlayersList(), cmp = self._SquadPageInterface__comparator)
        memberList = []
        for player in list:
            user = self.users.getUser(player.dbID, player.name)
            colors = g_settings.getLobbyUserCS(user.roster, user.himself)
            memberList.extend([
                user.uid,
                int(player.accId),
                player.name,
                player.state,
                player.time,
                player.vUserString,
                user.roster,
                user.himself,
                player.displayName,
                VoiceChatInterface.g_instance.isPlayerSpeaking(user.uid)])
            memberList.extend(colors)
        
        return memberList

    
    def populateUI(self, handler):
        _BasePageInterface.populateUI(self, handler)
        self._sMemberListener = SquadMembersListener(self)
        self._sMemberListener.start()
        CurrentVehicle.g_currentVehicle.onChanged += self._SquadPageInterface__cv_onCurrentVehicleChanged
        self._movieViewHandler.addExternalCallbacks({
            SQUAD_CH_COMMANDS.InvalidateMemberList(): self.onInvalidateMemberList,
            SQUAD_CH_COMMANDS.KickPlayer(): self.onKickPlayer,
            SQUAD_CH_COMMANDS.Ready(): self.onReady,
            SQUAD_CH_COMMANDS.Leave(): self.onLeave,
            SQUAD_PRB_COMMANDS.Send(): self.onSendInvitation,
            SQUAD_PRB_COMMANDS.ShowError(): self.onReceiveInvitationError,
            SQUAD_CH_COMMANDS.IsVehicleReady(): self.onIsVehicleReady })
        self._SquadPageInterface__searchUsers.populateUI(handler)
        self._SquadPageInterface__contacts.populateUI(handler)
        self.open()

    
    def dispossessUI(self):
        if not self._isPopulated:
            return None
        if self._movieViewHandler:
            self._movieViewHandler.call(SQUAD_PRB_COMMANDS.CloseWindow())
        
        self._movieViewHandler.removeExternalCallbacks(SQUAD_CH_COMMANDS.InvalidateMemberList(), SQUAD_CH_COMMANDS.KickPlayer(), SQUAD_CH_COMMANDS.Ready(), SQUAD_CH_COMMANDS.Leave(), SQUAD_PRB_COMMANDS.Send(), SQUAD_PRB_COMMANDS.ShowError(), SQUAD_CH_COMMANDS.IsVehicleReady())
        CurrentVehicle.g_currentVehicle.onChanged -= self._SquadPageInterface__cv_onCurrentVehicleChanged
        self._sMemberListener.destroy()
        self._sMemberListener = None
        self._SquadPageInterface__searchUsers.dispossessUI()
        self._SquadPageInterface__contacts.dispossessUI()
        _BasePageInterface.dispossessUI(self)

    
    def onInvalidateMemberList(self, *args):
        self.refreshMemberList()
        if self._SquadPageInterface__firstTimeOpen and self._sMemberListener.isCanSendInvite():
            self._movieViewHandler.call(SQUAD_CH_COMMANDS.OpenInvitationsWindow())
        
        self._SquadPageInterface__firstTimeOpen = False

    
    def onKickPlayer(self, *args):
        parser = CommandArgsParser(self.onKickPlayer.__name__, 1, [
            int])
        (accId,) = parser.parse(*args)
        self._sMemberListener.kickPlayer(accId)

    
    def onReady(self, callbackID):
        if self._sMemberListener.isPlayerReady():
            BigWorld.player().prb_notReady((constants.PREBATTLE_ACCOUNT_STATE.NOT_READY,), (lambda code: self._SquadPageInterface__changeComplete(code, 'notReady')))
        else:
            
            def setMemberReady():
                yield checkAmmoLevel()
                result = None
                if result:
                    account_helpers.AccountPrebattle.AccountPrebattle.setMemdberReady()
                

            setMemberReady = process(setMemberReady)
            if self._movieViewHandler.captcha.isCaptchaRequired():
                self._movieViewHandler.captcha.showCaptcha(setMemberReady)
            else:
                setMemberReady()

    
    def onLeave(self, callbackID):
        (BigWorld.player().prb_leave,)((lambda code: self._SquadPageInterface__changeComplete(code, 'leave')))

    
    def _SquadPageInterface__changeComplete(self, result, chtype):
        if result < 0:
            LOG_DEBUG('Change %s error code: %s' % (chtype, result))
        

    
    def onSendInvitation(self, responseId, *args):
        prebattleID = BigWorld.player().prebattle.id
        isCanSend = self._sMemberListener.isCanSendInvite()
        if isCanSend and prebattleID:
            self.invites.sendInvites(list(args[1:]), args[0])
            self._movieViewHandler.respond([
                responseId,
                constants.REQUEST_COOLDOWN.PREBATTLE_INVITES])
        else:
            LOG_WARNING('Can not send invites: canSendInvite = %r, prebattleRoomId = %d' % (isCanSend, prebattleID))

    
    def onReceiveInvitationError(self, _, message):
        SystemMessages.pushI18nMessage(message, type = SystemMessages.SM_TYPE.Error)

    
    def onIsVehicleReady(self, responseId):
        vehicle = CurrentVehicle.g_currentVehicle
        if vehicle is not None or not vehicle.isBroken():
            1
        ready = False
        self._movieViewHandler.respond([
            responseId,
            ready])

    
    def _SquadPageInterface__setReady(self):
        vehicle = CurrentVehicle.g_currentVehicle
        if vehicle is not None or not vehicle.isBroken():
            1
        ready = False
        if self._movieViewHandler is not None:
            self._movieViewHandler.call(SQUAD_CH_COMMANDS.SetVehicleReady(), [
                ready])
        

    
    def _SquadPageInterface__cv_onCurrentVehicleChanged(self, *args):
        self._SquadPageInterface__setReady()



class CompanyPageInterface(_BasePageInterface):
    
    def __init__(self, channelId):
        _BasePageInterface.__init__(self, channelId)
        self._CompanyPageInterface__searchUsers = PrebattleSearchUsersInterface(prefix = 'Prebattle.Team.SearchUsers')
        self._CompanyPageInterface__contacts = PrebattleUsersRosterInterface(prefix = 'Prebattle.Team')
        self._CompanyPageInterface__firstTimeOpen = False
        self._CompanyPageInterface__lastNotReady = 0
        self._CompanyPageInterface__notReadyCallback = None

    
    def clear(self):
        _BasePageInterface.clear(self)
        self._invitesManager = None
        self._CompanyPageInterface__searchUsers = None
        self._CompanyPageInterface__contacts = None

    
    def addMembers(self, members):
        return self.refreshMemberList()

    
    def addMember(self, member):
        return self.refreshMemberList()

    
    def removeMember(self, member):
        return self.refreshMemberList()

    
    def removeMembers(self, members):
        return self.refreshMemberList()

    
    def refreshSettings(self):
        if self._movieViewHandler:
            self._movieViewHandler.call(TEAM_CH_COMMANDS.SetPlayerRoles(), [
                self._sMemberListener.isCanSendInvite(),
                self._sMemberListener.isCanKick(),
                self._sMemberListener.isCanAssign(),
                self._sMemberListener.isCanChangeComment(),
                self._sMemberListener.isCanChangeOpenState(),
                self._sMemberListener.isCanChangeDivision(),
                self._sMemberListener.isCreator(),
                self._sMemberListener.isPlayerReady(),
                self._sMemberListener.isTeamReady(),
                self._sMemberListener.isInMainRoster(),
                self._sMemberListener.comment,
                self._sMemberListener.isOpened,
                self._sMemberListener.creator,
                self._sMemberListener.maxCountLimit])
            self.setDivisions()
            self._CompanyPageInterface__setReady()
        

    
    def refreshMemberList(self):
        if self._movieViewHandler:
            self._movieViewHandler.call(TEAM_CH_COMMANDS.RefreshMemberList(), self._CompanyPageInterface__getMembersList())
        

    
    def open(self):
        _BasePageInterface.open(self)
        self._CompanyPageInterface__firstTimeOpen = True

    
    def _CompanyPageInterface__comparator(self, player, other):
        if player.isCommander ^ other.isCommander:
            if player.isCommander:
                pass
            1
            result = 1
        else:
            result = cmp(player.time, other.time)
        return result

    
    def _CompanyPageInterface__getMembersList(self):
        list = sorted(self._sMemberListener.getPlayersList(1), cmp = self._CompanyPageInterface__comparator)
        (minLightVehicleLevel, maxLightVehicleLevel) = self._sMemberListener.getLightTanksLevelsLimits()
        (minMediumVehicleLevel, maxMediumVehicleLevel) = self._sMemberListener.getMediumTanksLevelsLimits()
        (minHeavyVehicleLevel, maxHeavyVehicleLevel) = self._sMemberListener.getHeavyTanksLevelsLimits()
        (minSPGVehicleLevel, maxSPGVehicleLevel) = self._sMemberListener.getSPGLevelsLimits()
        (minATSPGVehicleLevel, maxATSPGVehicleLevel) = self._sMemberListener.getATSPGLevelsLimits()
        memberList = [
            len(list)]
        maxLightTanksLevel = 0
        maxMediumTanksLevel = 0
        maxHeavyTanksLevel = 0
        maxSPGLevel = 0
        maxATSPGLevel = 0
        totalLevel = 0
        for player in list:
            user = self.users.getUser(player.dbID, player.name)
            colors = g_settings.getLobbyUserCS(user.roster, user.himself)
            vehicleType = None
            if player.isVehicleLightTank:
                minVLevel = minLightVehicleLevel
                maxVLevel = maxLightVehicleLevel
                maxLightTanksLevel = max(player.vLevel, maxLightTanksLevel)
                vehicleType = 'lightTank'
            elif player.isVehicleMediumTank:
                minVLevel = minMediumVehicleLevel
                maxVLevel = maxMediumVehicleLevel
                maxMediumTanksLevel = max(player.vLevel, maxMediumTanksLevel)
                vehicleType = 'mediumTank'
            elif player.isVehicleHeavyTank:
                minVLevel = minHeavyVehicleLevel
                maxVLevel = maxHeavyVehicleLevel
                maxHeavyTanksLevel = max(player.vLevel, maxHeavyTanksLevel)
                vehicleType = 'heavyTank'
            elif player.isVehicleSPG:
                minVLevel = minSPGVehicleLevel
                maxVLevel = maxSPGVehicleLevel
                maxSPGLevel = max(player.vLevel, maxSPGLevel)
                vehicleType = 'spg'
            elif player.isVehicleATSPG:
                minVLevel = minATSPGVehicleLevel
                maxVLevel = maxATSPGVehicleLevel
                maxATSPGLevel = max(player.vLevel, maxATSPGLevel)
                vehicleType = 'at-spg'
            
            if not (player.vLevel) and player.vLevel >= minVLevel:
                pass
            memberList.extend([
                user.uid,
                int(player.accId),
                player.name == self._sMemberListener.creatorName,
                vehicleType,
                player.name,
                player.state,
                player.time,
                player.vUserString,
                player.vRomanLevel,
                user.roster,
                user.himself,
                player.displayName,
                VoiceChatInterface.g_instance.isPlayerSpeaking(user.uid),
                player.vLevel <= maxVLevel])
            memberList.extend(colors)
            totalLevel += player.vLevel
        
        (totalMin, totalMax) = self._sMemberListener.getTotalLevelsLimits()
        memberList.extend((maxLightTanksLevel, minLightVehicleLevel, maxLightVehicleLevel, i18n.makeString('#tooltips:redButton/disabled/vehicleLightLevelLimits/body', minLightVehicleLevel, maxLightVehicleLevel), maxMediumTanksLevel, minMediumVehicleLevel, maxMediumVehicleLevel, i18n.makeString('#tooltips:redButton/disabled/vehicleMediumLevelLimits/body', minMediumVehicleLevel, maxMediumVehicleLevel), maxHeavyTanksLevel, minHeavyVehicleLevel, maxHeavyVehicleLevel, i18n.makeString('#tooltips:redButton/disabled/vehicleHeavyLevelLimits/body', minHeavyVehicleLevel, maxHeavyVehicleLevel), maxSPGLevel, minSPGVehicleLevel, maxSPGVehicleLevel, i18n.makeString('#tooltips:redButton/disabled/vehicleSPGLevelLimits/body', minSPGVehicleLevel, maxSPGVehicleLevel), maxATSPGLevel, minATSPGVehicleLevel, maxATSPGVehicleLevel, i18n.makeString('#tooltips:redButton/disabled/vehicleATSPGLevelLimits/body', minATSPGVehicleLevel, maxATSPGVehicleLevel)))
        memberList.extend((totalLevel, totalMin, totalMax, i18n.makeString('#tooltips:redButton/disabled/vehicleTotalLevelLimits/body', totalMin, totalMax)))
        list = sorted(self._sMemberListener.getPlayersList(17), cmp = self._CompanyPageInterface__comparator)
        memberList.append(len(list))
        for player in list:
            user = self.users.getUser(player.dbID, player.name)
            colors = g_settings.getLobbyUserCS(user.roster, user.himself)
            vehicleType = None
            if player.isVehicleLightTank:
                minVLevel = minLightVehicleLevel
                maxVLevel = maxLightVehicleLevel
                vehicleType = 'lightTank'
            elif player.isVehicleMediumTank:
                minVLevel = minMediumVehicleLevel
                maxVLevel = maxMediumVehicleLevel
                vehicleType = 'mediumTank'
            elif player.isVehicleHeavyTank:
                minVLevel = minHeavyVehicleLevel
                maxVLevel = maxHeavyVehicleLevel
                vehicleType = 'heavyTank'
            elif player.isVehicleSPG:
                minVLevel = minSPGVehicleLevel
                maxVLevel = maxSPGVehicleLevel
                vehicleType = 'spg'
            elif player.isVehicleATSPG:
                minVLevel = minATSPGVehicleLevel
                maxVLevel = maxATSPGVehicleLevel
                vehicleType = 'at-spg'
            
            if not (player.vLevel) and player.vLevel >= minVLevel:
                pass
            memberList.extend([
                user.uid,
                int(player.accId),
                player.name == self._sMemberListener.creatorName,
                vehicleType,
                player.name,
                player.state,
                player.time,
                player.vUserString,
                player.vRomanLevel,
                user.roster,
                user.himself,
                player.displayName,
                VoiceChatInterface.g_instance.isPlayerSpeaking(user.uid),
                player.vLevel <= maxVLevel])
            memberList.extend(colors)
        
        return memberList

    
    def populateUI(self, handler):
        _BasePageInterface.populateUI(self, handler)
        self._sMemberListener = CompanyMembersListener(self)
        self._sMemberListener.start()
        CurrentVehicle.g_currentVehicle.onChanged += self._CompanyPageInterface__cv_onCurrentVehicleChanged
        self._movieViewHandler.addExternalCallbacks({
            TEAM_CH_COMMANDS.InvalidateMemberList(): self.onInvalidateMemberList,
            TEAM_CH_COMMANDS.KickPlayer(): self.onKickPlayer,
            TEAM_CH_COMMANDS.AssignPlayer(): self.onAssignPlayer,
            TEAM_CH_COMMANDS.UnAssignPlayer(): self.onUnassignPlayer,
            TEAM_CH_COMMANDS.ChangeOpenState(): self.onChangeOpenState,
            TEAM_CH_COMMANDS.ChangeDivision(): self.onChangeDivision,
            TEAM_CH_COMMANDS.ChangeComment(): self.onChangeComment,
            TEAM_CH_COMMANDS.Ready(): self.onReady,
            TEAM_CH_COMMANDS.Leave(): self.onLeave,
            TEAM_PRB_COMMANDS.Send(): self.onSendInvitation,
            TEAM_PRB_COMMANDS.ShowError(): self.onReceiveInvitationError,
            TEAM_CH_COMMANDS.IsVehicleReady(): self.onIsVehicleReady })
        self._CompanyPageInterface__searchUsers.populateUI(handler)
        self._CompanyPageInterface__contacts.populateUI(handler)
        self.open()

    
    def dispossessUI(self):
        if not self._isPopulated:
            return None
        if self._movieViewHandler:
            self._movieViewHandler.call(TEAM_PRB_COMMANDS.CloseWindow())
        
        self._movieViewHandler.removeExternalCallbacks(TEAM_CH_COMMANDS.InvalidateMemberList(), TEAM_CH_COMMANDS.KickPlayer(), TEAM_CH_COMMANDS.AssignPlayer(), TEAM_CH_COMMANDS.UnAssignPlayer(), TEAM_CH_COMMANDS.ChangeOpenState(), TEAM_CH_COMMANDS.ChangeComment(), TEAM_CH_COMMANDS.ChangeDivision(), TEAM_CH_COMMANDS.Ready(), TEAM_CH_COMMANDS.Leave(), TEAM_PRB_COMMANDS.Send(), TEAM_PRB_COMMANDS.ShowError(), TEAM_CH_COMMANDS.IsVehicleReady())
        CurrentVehicle.g_currentVehicle.onChanged -= self._CompanyPageInterface__cv_onCurrentVehicleChanged
        self._sMemberListener.destroy()
        self._sMemberListener = None
        self._CompanyPageInterface__searchUsers.dispossessUI()
        self._CompanyPageInterface__contacts.dispossessUI()
        _BasePageInterface.dispossessUI(self)

    
    def onInvalidateMemberList(self, *args):
        self.refreshSettings()
        self.refreshMemberList()
        if self._CompanyPageInterface__firstTimeOpen:
            if self._sMemberListener.isCanSendInvite():
                self._movieViewHandler.call(TEAM_CH_COMMANDS.OpenInvitationsWindow())
            
        
        self._CompanyPageInterface__firstTimeOpen = False

    
    def onKickPlayer(self, *args):
        parser = CommandArgsParser(self.onKickPlayer.__name__, 1, [
            int])
        (accId,) = parser.parse(*args)
        self._sMemberListener.kickPlayer(accId)

    
    def onAssignPlayer(self, callbackID, uid):
        None(BigWorld.player().prb_assign, (uid, 1), (lambda code: self._CompanyPageInterface__assignComplete(code, uid, 1)))

    
    def onUnassignPlayer(self, callbackID, uid):
        None(BigWorld.player().prb_assign, (uid, 17), (lambda code: self._CompanyPageInterface__assignComplete(code, uid, 17)))

    
    def _CompanyPageInterface__assignComplete(self, result, uid, roster):
        if result < 0:
            LOG_DEBUG('Assign playerID: %s to roster: %s error code: %s' % (uid, roster, result))
        

    
    def onChangeOpenState(self, callbackID, isOpen):
        BigWorld.player().prb_changeOpenStatus((isOpen,), (lambda code: self._CompanyPageInterface__changeComplete(code, 'openStatus')))

    
    def onChangeDivision(self, callbackID, division):
        if division in constants.PREBATTLE_COMPANY_DIVISION.RANGE:
            BigWorld.player().prb_changeDivision((division,), (lambda code: self._CompanyPageInterface__changeComplete(code, 'division')))
        

    
    def setDivisions(self):
        d = [
            self._sMemberListener.division]
        for (id, name) in constants.PREBATTLE_COMPANY_DIVISION_NAMES.items():
            d.append(id)
            d.append(name)
        
        self._movieViewHandler.call(TEAM_CH_COMMANDS.SetDivisions(), d)

    
    def onChangeComment(self, callbackID, comment):
        BigWorld.player().prb_changeComment((comment,), (lambda code: self._CompanyPageInterface__changeComplete(code, 'comment')))

    
    def onReady(self, callbackID):
        
        def callback():
            if self._CompanyPageInterface__notReadyCallback is not None:
                BigWorld.cancelCallback(self._CompanyPageInterface__notReadyCallback)
                self._CompanyPageInterface__notReadyCallback = None
            
            self._CompanyPageInterface__ready(callbackID)

        t = self._CompanyPageInterface__lastNotReady + constants.REQUEST_COOLDOWN.PREBATTLE_NOT_READY
        if t < time.time():
            callback()
        else:
            self._CompanyPageInterface__notReadyCallback = BigWorld.callback(t - time.time(), callback)

    
    def _CompanyPageInterface__ready(self, cid):
        if self._sMemberListener.isPlayerReady():
            self._CompanyPageInterface__lastNotReady = time.time()
            BigWorld.player().prb_notReady((constants.PREBATTLE_ACCOUNT_STATE.NOT_READY,), (lambda code: self._CompanyPageInterface__changeComplete(code, 'notReady')))
        else:
            
            def setMemberReady():
                yield checkAmmoLevel()
                result = None
                if result:
                    if account_helpers.AccountPrebattle.AccountPrebattle.setMemdberReady():
                        return None
                
                if self._movieViewHandler is not None:
                    self._movieViewHandler.call(TEAM_CH_COMMANDS.LockReadyButton(), [
                        False])
                

            setMemberReady = (process,)(setMemberReady)
            if self._movieViewHandler.captcha.isCaptchaRequired():
                self._movieViewHandler.captcha.showCaptcha(setMemberReady)
            else:
                setMemberReady()

    
    def onLeave(self, callbackID):
        (BigWorld.player().prb_leave,)((lambda code: self._CompanyPageInterface__changeComplete(code, 'leave')))

    
    def _CompanyPageInterface__changeComplete(self, result, chtype):
        if result < 0:
            LOG_DEBUG('Change %s error code: %s' % (chtype, result))
        else:
            LOG_DEBUG('Change %s success' % chtype)

    
    def onSendInvitation(self, responseId, *args):
        prebattleID = BigWorld.player().prebattle.id
        isCanSend = self._sMemberListener.isCanSendInvite()
        if isCanSend and prebattleID:
            self.invites.sendInvites(list(args[1:]), args[0])
            self._movieViewHandler.respond([
                responseId,
                constants.REQUEST_COOLDOWN.PREBATTLE_INVITES])
        else:
            LOG_WARNING('Can not send invites: canSendInvite = %r, prebattleRoomId = %d' % (isCanSend, prebattleID))

    
    def onReceiveInvitationError(self, responseId, message):
        SystemMessages.pushI18nMessage(message, type = SystemMessages.SM_TYPE.Error)

    
    def onIsVehicleReady(self, responseId):
        vehicle = CurrentVehicle.g_currentVehicle
        if vehicle is not None or not vehicle.isBroken():
            1
        ready = False
        self._movieViewHandler.respond([
            responseId,
            ready])

    
    def _CompanyPageInterface__cv_onCurrentVehicleChanged(self, *args):
        self._CompanyPageInterface__setReady()

    
    def _CompanyPageInterface__setReady(self):
        vehicle = CurrentVehicle.g_currentVehicle
        if vehicle is not None or not vehicle.isBroken():
            1
        ready = False
        if self._movieViewHandler is not None:
            self._movieViewHandler.call(TEAM_CH_COMMANDS.SetVehicleReady(), [
                ready])
        



class BattleSessionPageInterface(_BasePageInterface):
    
    def __init__(self, channelId):
        _BasePageInterface.__init__(self, channelId)
        self._BattleSessionPageInterface__searchUsers = PrebattleSearchUsersInterface(prefix = 'Prebattle.BS.SearchUsers')
        self._BattleSessionPageInterface__contacts = PrebattleUsersRosterInterface(prefix = 'Prebattle.BS')
        self._BattleSessionPageInterface__firstTimeOpen = False
        self._BattleSessionPageInterface__startTimeCalbackId = None

    
    def clear(self):
        _BasePageInterface.clear(self)
        self._invitesManager = None
        self._BattleSessionPageInterface__searchUsers = None
        self._BattleSessionPageInterface__contacts = None

    
    def addMembers(self, members):
        return self.refreshMemberList()

    
    def addMember(self, member):
        return self.refreshMemberList()

    
    def removeMember(self, member):
        return self.refreshMemberList()

    
    def removeMembers(self, members):
        return self.refreshMemberList()

    
    def refreshSettings(self):
        if self._movieViewHandler:
            params = [
                self._sMemberListener.isCanSendInvite(),
                self._sMemberListener.isCanKick(),
                self._sMemberListener.isCanAssign(),
                self._sMemberListener.isCreator(),
                self._sMemberListener.isPlayerReady(),
                self._sMemberListener.isTeamReady()]
            params.extend(self._sMemberListener.params)
            self._movieViewHandler.call(BS_CH_COMMANDS.SetPlayerRoles(), params)
            if self._BattleSessionPageInterface__startTimeCalbackId:
                BigWorld.cancelCallback(self._BattleSessionPageInterface__startTimeCalbackId)
            
            self.refreshStartTime()
        

    
    def refreshStartTime(self):
        self._BattleSessionPageInterface__startTimeCalbackId = None
        if self._movieViewHandler:
            startTime = self._sMemberListener.startTime
            if startTime > 0:
                self._BattleSessionPageInterface__startTimeCalbackId = BigWorld.callback(10, self.refreshStartTime)
            
            self._movieViewHandler.call(BS_CH_COMMANDS.SetStartTime(), [
                startTime])
        

    
    def refreshMemberList(self):
        if self._movieViewHandler:
            self._movieViewHandler.call(BS_CH_COMMANDS.RefreshMemberList(), self._BattleSessionPageInterface__getMembersList())
        

    
    def open(self):
        _BasePageInterface.open(self)
        self._BattleSessionPageInterface__firstTimeOpen = True

    
    def _BattleSessionPageInterface__comparator(self, player, other):
        if player.isCommander ^ other.isCommander:
            if player.isCommander:
                pass
            1
            result = 1
        else:
            result = cmp(player.time, other.time)
        return result

    
    def _BattleSessionPageInterface__getMembersList(self):
        list = sorted(self._sMemberListener.getPlayersList(self._sMemberListener._ROSTERS[0]), cmp = self._BattleSessionPageInterface__comparator)
        memberList = [
            len(list)]
        totalLevel = 0
        for player in list:
            user = self.users.getUser(player.dbID, player.name)
            colors = g_settings.getLobbyUserCS(user.roster, user.himself)
            memberList.extend([
                user.uid,
                int(player.accId),
                player.name,
                player.state,
                player.time,
                player.vUserString,
                player.vRomanLevel,
                user.roster,
                user.himself,
                player.displayName,
                True])
            memberList.extend(colors)
            totalLevel += player.vLevel
        
        memberList.append(totalLevel)
        memberList.extend(self._sMemberListener.totalLevelLimit)
        memberList.append(self._sMemberListener.maxPlayersLimit)
        list = sorted(self._sMemberListener.getPlayersList(self._sMemberListener._ROSTERS[1]), cmp = self._BattleSessionPageInterface__comparator)
        memberList.append(len(list))
        for player in list:
            user = self.users.getUser(player.dbID, player.name)
            colors = g_settings.getLobbyUserCS(user.roster, user.himself)
            memberList.extend([
                user.uid,
                int(player.accId),
                player.name,
                player.state,
                player.time,
                player.vUserString,
                player.vRomanLevel,
                user.roster,
                user.himself,
                player.displayName,
                True])
            memberList.extend(colors)
        
        return memberList

    
    def populateUI(self, handler):
        _BasePageInterface.populateUI(self, handler)
        self._sMemberListener = BattleSessionMembersListener(self)
        self._sMemberListener.start()
        self._movieViewHandler.addExternalCallbacks({
            BS_CH_COMMANDS.InvalidateMemberList(): self.onInvalidateMemberList,
            BS_CH_COMMANDS.KickPlayer(): self.onKickPlayer,
            BS_CH_COMMANDS.AssignPlayer(): self.onAssignPlayer,
            BS_CH_COMMANDS.UnAssignPlayer(): self.onUnassignPlayer,
            BS_CH_COMMANDS.Ready(): self.onReady,
            BS_CH_COMMANDS.Leave(): self.onLeave,
            BS_PRB_COMMANDS.Send(): self.onSendInvitation,
            BS_PRB_COMMANDS.ShowError(): self.onReceiveInvitationError,
            BS_CH_COMMANDS.IsVehicleReady(): self.onIsVehicleReady })
        CurrentVehicle.g_currentVehicle.onChanged += self._BattleSessionPageInterface__cv_onCurrentVehicleChanged
        self._BattleSessionPageInterface__searchUsers.populateUI(handler)
        self._BattleSessionPageInterface__contacts.populateUI(handler)
        self.open()

    
    def dispossessUI(self):
        if not self._isPopulated:
            return None
        if self._movieViewHandler:
            self._movieViewHandler.call(BS_PRB_COMMANDS.CloseWindow())
        
        CurrentVehicle.g_currentVehicle.onChanged -= self._BattleSessionPageInterface__cv_onCurrentVehicleChanged
        self._movieViewHandler.removeExternalCallbacks(BS_CH_COMMANDS.InvalidateMemberList(), BS_CH_COMMANDS.KickPlayer(), BS_CH_COMMANDS.AssignPlayer(), BS_CH_COMMANDS.UnAssignPlayer(), BS_CH_COMMANDS.Ready(), BS_CH_COMMANDS.Leave(), BS_PRB_COMMANDS.Send(), BS_PRB_COMMANDS.ShowError(), BS_CH_COMMANDS.IsVehicleReady())
        self._sMemberListener.destroy()
        self._sMemberListener = None
        self._BattleSessionPageInterface__searchUsers.dispossessUI()
        self._BattleSessionPageInterface__contacts.dispossessUI()
        self._movieViewHandler.call(BS_CH_COMMANDS.CloseInvitationsWindow())
        _BasePageInterface.dispossessUI(self)

    
    def onInvalidateMemberList(self, *args):
        self.refreshSettings()
        self.refreshMemberList()
        self._BattleSessionPageInterface__firstTimeOpen = False

    
    def onKickPlayer(self, *args):
        parser = CommandArgsParser(self.onKickPlayer.__name__, 1, [
            int])
        (accId,) = parser.parse(*args)
        self._sMemberListener.kickPlayer(accId)

    
    def onAssignPlayer(self, callbackID, uid):
        None(BigWorld.player().prb_assign, (uid, self._sMemberListener._ROSTERS[0]), (lambda code: self._BattleSessionPageInterface__assignComplete(code, uid, 1)))

    
    def onUnassignPlayer(self, callbackID, uid):
        None(BigWorld.player().prb_assign, (uid, self._sMemberListener._ROSTERS[1]), (lambda code: self._BattleSessionPageInterface__assignComplete(code, uid, 17)))

    
    def _BattleSessionPageInterface__assignComplete(self, result, uid, roster):
        if result < 0:
            LOG_DEBUG('Assign playerID: %s to roster: %s error code: %s' % (uid, roster, result))
        

    
    def onReady(self, callbackID):
        if self._sMemberListener.isPlayerReady():
            BigWorld.player().prb_notReady((constants.PREBATTLE_ACCOUNT_STATE.NOT_READY,), (lambda code: self._BattleSessionPageInterface__changeComplete(code, 'notReady')))
        else:
            
            def setMemberReady():
                yield checkAmmoLevel()
                result = None
                if result:
                    account_helpers.AccountPrebattle.AccountPrebattle.setMemdberReady()
                

            setMemberReady = process(setMemberReady)
            if self._movieViewHandler.captcha.isCaptchaRequired():
                self._movieViewHandler.captcha.showCaptcha(setMemberReady)
            else:
                setMemberReady()

    
    def onLeave(self, callbackID):
        (BigWorld.player().prb_leave,)((lambda code: self._BattleSessionPageInterface__changeComplete(code, 'leave')))

    
    def _BattleSessionPageInterface__changeComplete(self, result, chtype):
        if result < 0:
            LOG_DEBUG('Change %s error code: %s' % (chtype, result))
        

    
    def onSendInvitation(self, responseId, *args):
        prebattleID = BigWorld.player().prebattle.id
        isCanSend = self._sMemberListener.isCanSendInvite()
        respondArgs = [
            responseId]
        if isCanSend and prebattleID:
            auxText = args[0]
            for receiverName in args[1:]:
                requestID = self.invites.createPrebattleInvite(receiverName, auxText, prebattleID, constants.PREBATTLE_TYPE.TOURNAMENT)
                respondArgs.append(requestID)
            
            self._movieViewHandler.respond(respondArgs)
        else:
            LOG_WARNING('Can not send invites: canSendInvite = %r, prebattleRoomId = %d' % (isCanSend, prebattleID))

    
    def onReceiveInvitationError(self, responseId, message):
        SystemMessages.pushI18nMessage(message, type = SystemMessages.SM_TYPE.Error)

    
    def _BattleSessionPageInterface__isCurrentVehicleReady(self):
        vehicle = CurrentVehicle.g_currentVehicle
        ready = False
        if vehicle is not None:
            isBSVehicleLockMode = account_helpers.AccountPrebattle.AccountPrebattle.getSettings().get('vehicleLockMode', False)
            isVehicleTypeLocked = vehicle.isVehicleTypeLocked()
            if isBSVehicleLockMode:
                pass
            typeLock = isVehicleTypeLocked
            if not vehicle.isBroken() and vehicle.isCrewFull():
                pass
            ready = not typeLock
        
        return ready

    
    def onIsVehicleReady(self, responseId):
        self._movieViewHandler.respond([
            responseId,
            self._BattleSessionPageInterface__isCurrentVehicleReady()])

    
    def _BattleSessionPageInterface__cv_onCurrentVehicleChanged(self, *args):
        self._BattleSessionPageInterface__setReady()

    
    def _BattleSessionPageInterface__setReady(self):
        if self._movieViewHandler is not None:
            self._movieViewHandler.call(BS_CH_COMMANDS.SetVehicleReady(), [
                self._BattleSessionPageInterface__isCurrentVehicleReady()])
        



class LazyPageInterface(_BasePageInterface):
    _LazyPageInterface__EXIT_DELAY = 10
    _LazyPageInterface__exitCallbackID = None
    
    def __init__(self, channelId):
        _BasePageInterface.__init__(self, channelId)
        self._LazyPageInterface__joined = False

    
    def populateUI(self, handler):
        _BasePageInterface.populateUI(self, handler)
        self._movieViewHandler.addExternalCallbacks({
            LAZY_CH_COMMANDS.IsJoinedToChannel(): self.onIsJoinedToChannel,
            LAZY_CH_COMMANDS.RequestJoinToChannel(): self.onRequestJoinToChannel,
            LAZY_CH_COMMANDS.RequestExitFromChannel(): self.onRequestExitFromChannel })

    
    def dispossessUI(self):
        if not self._isPopulated:
            return None
        self._movieViewHandler.removeExternalCallbacks(LAZY_CH_COMMANDS.IsJoinedToChannel(), LAZY_CH_COMMANDS.RequestJoinToChannel(), LAZY_CH_COMMANDS.RequestExitFromChannel())
        _BasePageInterface.dispossessUI(self)

    
    def addMessage(self, message, format = True, playerIsTarget = False, system = False):
        if format:
            pass
        1
        messageText = message.data
        if self._movieViewHandler:
            self._movieViewHandler.call(CHMS_COMMANDS.RecieveMessage(), [
                message.channel,
                messageText,
                False])
        
        return messageText

    
    def clear(self):
        _BasePageInterface.clear(self)
        self._LazyPageInterface__clearExitCallback()
        self._LazyPageInterface__joined = False

    
    def setJoined(self, joined):
        if self._LazyPageInterface__joined ^ joined:
            LOG_DEBUG('lazy channel (id, joined):', self._cid, joined)
            self._LazyPageInterface__joined = joined
            if self._movieViewHandler is not None:
                self._movieViewHandler.call(LAZY_CH_COMMANDS.SetJoinedToChannel(), [
                    self._cid,
                    joined])
            
        

    
    def isJoined(self):
        return self._LazyPageInterface__joined

    
    def _LazyPageInterface__clearExitCallback(self):
        if self._LazyPageInterface__exitCallbackID is not None:
            BigWorld.cancelCallback(self._LazyPageInterface__exitCallbackID)
            self._LazyPageInterface__exitCallbackID = None
        

    
    def onIsJoinedToChannel(self, *args):
        parser = CommandArgsParser(self.onIsJoinedToChannel.__name__, 1, [
            int])
        (cid,) = parser.parse(*args)
        if self._cid != cid:
            return None
        if self._LazyPageInterface__joined:
            self._LazyPageInterface__clearExitCallback()
        
        parser.addArg(self._LazyPageInterface__joined)
        self._movieViewHandler.respond(parser.args())

    
    def onRequestJoinToChannel(self, callbackID, cid):
        if self._cid != cid:
            return None
        self._LazyPageInterface__clearExitCallback()
        if not self._LazyPageInterface__joined:
            self.channels.joinToChannel(self._cid)
        

    
    def onRequestExitFromChannel(self, callbackID, cid):
        if self._cid != cid:
            return None
        self._LazyPageInterface__clearExitCallback()
        if self._LazyPageInterface__joined:
            self._LazyPageInterface__exitCallbackID = BigWorld.callback(self._LazyPageInterface__EXIT_DELAY, self._LazyPageInterface__exitFromLazyChannel)
        

    
    def _LazyPageInterface__exitFromLazyChannel(self):
        self._LazyPageInterface__exitCallbackID = None
        self.channels.exitFromChannel(self._cid)



class CompaniesPageInterface(LazyPageInterface):
    
    def __init__(self, channelId):
        LazyPageInterface.__init__(self, channelId)

    
    def clear(self):
        super(CompaniesPageInterface, self).clear()

    
    def refreshCompanyList(self, callbackID, ownerFilter, isNotInBattle, divisionFilter):
        if divisionFilter:
            BigWorld.player().requestPrebattlesByDivision(isNotInBattle, divisionFilter)
        elif ownerFilter == '':
            BigWorld.player().requestPrebattles(constants.PREBATTLE_TYPE.COMPANY, constants.PREBATTLE_CACHE_KEY.CREATE_TIME, isNotInBattle, -50, 0)
        else:
            BigWorld.player().requestPrebattlesByName(constants.PREBATTLE_TYPE.COMPANY, isNotInBattle, ownerFilter)
        if self._movieViewHandler:
            self._movieViewHandler.call(TEAM_CH_COMMANDS.CreateEnable(), [
                BigWorld.player().prebattle is None])
        
        return True

    
    def joinCompany(self, callbackID, companyID):
        currentPrebattle = account_helpers.AccountPrebattle.AccountPrebattle.get()
        if currentPrebattle and companyID == currentPrebattle.id:
            channels = self.channels.getPrebattleChannelList()
            if channels:
                page = self._dispatcherProxy.currentWindow.getChannelPage(channels[0].cid)
                if page is not None:
                    page.open()
                
            
            return None
        
        def joinFunc():
            yield account_helpers.AccountPrebattle.AccountPrebattle.join(companyID)
            success = None

        joinFunc = (process,)(joinFunc)
        if self._movieViewHandler.captcha.isCaptchaRequired():
            self._movieViewHandler.captcha.showCaptcha(joinFunc)
        else:
            joinFunc()

    
    def getPlayers(self, callbackID, teamID):
        BigWorld.player().requestPrebattleRoster(teamID)

    
    def createCompany(self, callbackID):
        yield StatsRequester().getAccountAttrs()
        accAttrs = None
        isPremium = account_helpers.isPremiumAccount(accAttrs)
        if isPremium:
            if self._movieViewHandler.captcha.isCaptchaRequired():
                self._movieViewHandler.captcha.showCaptcha(self._CompaniesPageInterface__doCreateCompany)
            else:
                self._CompaniesPageInterface__doCreateCompany()
        else:
            self._movieViewHandler.call('common.premiumNeeded', [
                'team'])

    createCompany = process(createCompany)
    
    def _CompaniesPageInterface__doCreateCompany(self):
        BigWorld.player().prb_createCompany(True, '', constants.PREBATTLE_COMPANY_DIVISION.CHAMPION)

    
    def _CompaniesPageInterface__reciveList(self, type, count, prebattles):
        if self._movieViewHandler and type == constants.PREBATTLE_TYPE.COMPANY:
            teamsList = []
            prebattles.reverse()
            for (_, id, info) in prebattles:
                teamsList.append(id)
                creator = info.get(constants.PREBATTLE_CACHE_KEY.CREATOR, '')
                clan = info.get(constants.PREBATTLE_CACHE_KEY.CREATOR_CLAN_ABBREV, '')
                if clan != '':
                    creator += '[%s]' % clan
                
                teamsList.append(creator)
                teamsList.append(passCensor(info.get(constants.PREBATTLE_CACHE_KEY.COMMENT, '')))
                teamsList.append(info.get(constants.PREBATTLE_CACHE_KEY.PLAYER_COUNT, 0))
                teamsList.append(constants.PREBATTLE_COMPANY_DIVISION_NAMES.get(info.get(constants.PREBATTLE_CACHE_KEY.DIVISION, 0)))
            
            self._movieViewHandler.call(TEAM_CH_COMMANDS.RefreshList(), teamsList)
        

    
    def _CompaniesPageInterface__recivePlayersList(self, prebattleID, roster):
        pList = [
            prebattleID]
        for (id, name, dbId, roster, _, time, _, _, clanAbbrev) in roster:
            if roster == 1:
                user = self.users.getUser(dbId, name)
                name = user.userName
                if len(clanAbbrev) > 0:
                    name = '%s[%s]' % (name, clanAbbrev)
                
                pList.append(name)
                pList.append(g_settings.getLobbyUserCS(user.roster, user.himself)[1])
                continue
        
        self._movieViewHandler.call(TEAM_CH_COMMANDS.GetPlayers(), pList)

    
    def populateUI(self, handler):
        LazyPageInterface.populateUI(self, handler)
        g_playerEvents = g_playerEvents
        import PlayerEvents
        self._movieViewHandler.addExternalCallbacks({
            TEAM_CH_COMMANDS.RefreshList(): self.refreshCompanyList,
            TEAM_CH_COMMANDS.CreateTeam(): self.createCompany,
            TEAM_CH_COMMANDS.JoinTeam(): self.joinCompany,
            TEAM_CH_COMMANDS.GetPlayers(): self.getPlayers,
            'Messenger.TeamsChannel.GetDivisions': self.onGetDivisions })
        g_playerEvents.onPrebattlesListReceived += self._CompaniesPageInterface__reciveList
        g_playerEvents.onPrebattleRosterReceived += self._CompaniesPageInterface__recivePlayersList
        g_playerEvents.onPrebattleJoined += self._CompaniesPageInterface__disableCreate
        g_playerEvents.onPrebattleLeft += self._CompaniesPageInterface__enableCreate
        g_playerEvents.onKickedFromPrebattle += self._CompaniesPageInterface__enableCreate

    
    def dispossessUI(self):
        g_playerEvents = g_playerEvents
        import PlayerEvents
        g_playerEvents.onPrebattlesListReceived -= self._CompaniesPageInterface__reciveList
        g_playerEvents.onPrebattleRosterReceived -= self._CompaniesPageInterface__recivePlayersList
        g_playerEvents.onPrebattleJoined -= self._CompaniesPageInterface__disableCreate
        g_playerEvents.onPrebattleLeft -= self._CompaniesPageInterface__enableCreate
        g_playerEvents.onKickedFromPrebattle -= self._CompaniesPageInterface__enableCreate
        self._movieViewHandler.removeExternalCallbacks(TEAM_CH_COMMANDS.RefreshList(), TEAM_CH_COMMANDS.CreateTeam(), TEAM_CH_COMMANDS.JoinTeam(), TEAM_CH_COMMANDS.GetPlayers(), 'Messenger.TeamsChannel.GetDivisions')
        LazyPageInterface.dispossessUI(self)

    
    def onGetDivisions(self, cid):
        d = [
            0,
            'ALL']
        for (id, name) in constants.PREBATTLE_COMPANY_DIVISION_NAMES.items():
            d.append(id)
            d.append(name)
        
        self._movieViewHandler.call(TEAM_CH_COMMANDS.UpdateDivisions(), d)

    
    def _CompaniesPageInterface__disableCreate(self):
        if self._movieViewHandler:
            self._movieViewHandler.call(TEAM_CH_COMMANDS.CreateEnable(), [
                False])
        

    
    def _CompaniesPageInterface__enableCreate(self, code = None):
        if self._movieViewHandler:
            self._movieViewHandler.call(TEAM_CH_COMMANDS.CreateEnable(), [
                True])
        



class BattleSessionsPageInterface(LazyPageInterface):
    
    def __init__(self, channelId):
        LazyPageInterface.__init__(self, channelId)
        self._BattleSessionsPageInterface__prebattleNotifications = []
        self._BattleSessionsPageInterface__notifiedPrebattles = set()

    
    def clear(self):
        super(BattleSessionsPageInterface, self).clear()

    
    def populateUI(self, handler):
        LazyPageInterface.populateUI(self, handler)
        self._movieViewHandler.addExternalCallbacks({
            BS_CH_COMMANDS.RefreshList(): self.update,
            BS_CH_COMMANDS.Join(): self.joinBS,
            BS_CH_COMMANDS.GetPlayers(): self.getPlayers })
        self.update()
        g_playerEvents = g_playerEvents
        import PlayerEvents
        g_playerEvents.onPrebattleAutoInvitesChanged += self.update
        g_playerEvents.onPrebattleRosterReceived += self._BattleSessionsPageInterface__recivePlayersList

    
    def dispossessUI(self):
        g_playerEvents = g_playerEvents
        import PlayerEvents
        g_playerEvents.onPrebattleAutoInvitesChanged -= self.update
        g_playerEvents.onPrebattleRosterReceived -= self._BattleSessionsPageInterface__recivePlayersList
        self._movieViewHandler.removeExternalCallbacks(BS_CH_COMMANDS.RefreshList(), BS_CH_COMMANDS.Join(), BS_CH_COMMANDS.GetPlayers())
        LazyPageInterface.dispossessUI(self)
        self._BattleSessionsPageInterface__prebattleNotifications = []
        self._BattleSessionsPageInterface__notifiedPrebattles = set()

    
    def addPrebattleNotification(self, prebattleId, prebattleType, text):
        if prebattleId in self._BattleSessionsPageInterface__notifiedPrebattles:
            return None
        iconId = 'BattleResultIcon'
        if prebattleType == constants.PREBATTLE_TYPE.CLAN:
            iconId = 'ClanBattleResultIcon'
        elif prebattleType == constants.PREBATTLE_TYPE.TOURNAMENT:
            iconId = 'TournamentBattleResultIcon'
        
        formatted = g_settings.htmlTemplates.format('inviteToSpecialBattle', ctx = {
            'icon': iconId,
            'text': text })
        self._BattleSessionsPageInterface__prebattleNotifications.append(formatted)
        self._BattleSessionsPageInterface__notifiedPrebattles.add(prebattleId)
        if self._movieViewHandler:
            self._movieViewHandler.call(CHMS_COMMANDS.RecieveMessage(), [
                self._cid,
                formatted,
                True])
        

    
    def onRequestChannelMessages(self, *args):
        parser = CommandArgsParser(self.onRequestChannelMessages.__name__, 1, [
            long])
        (cid,) = parser.parse(*args)
        if cid == self._cid:
            history = list(self._channelMessagesFunc())
            history.extend(self._BattleSessionsPageInterface__prebattleNotifications)
            parser.addArg('\n'.join(history))
            self._movieViewHandler.respond(parser.args())
        

    
    def update(self, callbackId = None):
        
        def cmpPrebatles(x, y):
            xST = x[1].get('startTime', time.time())
            yST = y[1].get('startTime', time.time())
            if xST < yST:
                return -1
            if xST > yST:
                return 1
            return 0

        makeLocalServerTime = makeLocalServerTime
        import helpers.time_utils
        teamsList = []
        prebattles = BigWorld.player().prebattleAutoInvites.items()
        prebattles.sort(cmpPrebatles)
        for (id, info) in prebattles:
            teamsList.append(id)
            extraData = info.get('description', { })
            description = account_helpers.AccountPrebattle.AccountPrebattle.getPrebattleDescription(extraData)
            teamsList.append(description)
            team1 = extraData.get('opponents', { }).get('1', { }).get('name', '')
            team2 = extraData.get('opponents', { }).get('2', { }).get('name', '')
            teamsList.append(' vs. '.join([
                team1,
                team2]))
            startTime = info.get('startTime', time.time())
            startTime = makeLocalServerTime(startTime)
            frmtStartTime = BigWorld.wg_getLongTimeFormat(startTime)
            if startTime - time.time() > 8640:
                frmtStartTime += ' ' + BigWorld.wg_getLongDateFormat(startTime)
            
            startTimeString = i18n.makeString('#messenger:lobby/bsChannels/title/startTime', frmtStartTime)
            teamsList.append(startTimeString)
            if len(description) > 0:
                prebattleType = info.get('type')
                self.addPrebattleNotification(id, prebattleType, u'%s, %s' % (description, unicode(frmtStartTime, 'utf-8')))
                continue
        
        self._movieViewHandler.call(BS_CH_COMMANDS.RefreshList(), teamsList)

    
    def _BattleSessionsPageInterface__recivePlayersList(self, prebattleID, roster):
        pList = [
            prebattleID]
        for (id, name, dbId, roster, _, time, _, _, clanAbbrev) in roster:
            if roster == 1:
                user = self.users.getUser(dbId, name)
                name = user.userName
                if len(clanAbbrev) > 0:
                    name = '%s[%s]' % (name, clanAbbrev)
                
                pList.append(name)
                pList.append(g_settings.getLobbyUserCS(user.roster, user.himself)[1])
                continue
        
        self._movieViewHandler.call(BS_CH_COMMANDS.GetPlayers(), pList)

    
    def joinBS(self, _, teamID):
        currentPrebattle = account_helpers.AccountPrebattle.AccountPrebattle.get()
        if currentPrebattle and teamID == currentPrebattle.id:
            channels = self.channels.getPrebattleChannelList()
            if channels:
                self._dispatcherProxy.currentWindow.getChannelPage(channels[0].cid).open()
            
            return None
        peripheryID = BigWorld.player().prebattleAutoInvites.get(teamID, { }).get('peripheryID', 0)
        if peripheryID and peripheryID != connectionManager.peripheryID:
            pInfo = g_preDefinedHosts.periphery(peripheryID)
            if pInfo is None:
                SystemMessages.pushI18nMessage(i18n.makeString('#system_messages:arena_start_errors/join/WRONG_PERIPHERY_UNKNOWN'), type = SystemMessages.SM_TYPE.Warning)
            else:
                SystemMessages.pushI18nMessage(i18n.makeString('#system_messages:arena_start_errors/join/WRONG_PERIPHERY_KNOWN') % pInfo[0], type = SystemMessages.SM_TYPE.Warning)
            return None
        
        def joinFunc():
            yield account_helpers.AccountPrebattle.AccountPrebattle.join(teamID)
            success = None

        joinFunc = (process,)(joinFunc)
        if self._movieViewHandler.captcha.isCaptchaRequired():
            self._movieViewHandler.captcha.showCaptcha(joinFunc)
        else:
            joinFunc()

    
    def getPlayers(self, callbackID, teamID):
        ''' Join to team instead of getting players. Maybe temporary? '''
        self.joinBS(callbackID, teamID)



