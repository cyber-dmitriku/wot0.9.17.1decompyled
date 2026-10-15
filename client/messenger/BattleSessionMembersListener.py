# Source Generated with Decompyle++
# File: BattleSessionMembersListener.pyc (Python 2.6)

from account_helpers.AccountPrebattle import AccountPrebattle
import BigWorld
import constants
from debug_utils import LOG_ERROR
from helpers import time_utils
from datetime import datetime, timedelta
from helpers import i18n
from messenger.UsersManager import UsersManager
from messenger.wrappers import TeamPlayerWrapper
import weakref

class BattleSessionMembersListener(object):
    _TEAM_ROSTERS = {
        1: (1, 17),
        2: (2, 18) }
    _ROSTERS = (1, 17)
    _MAX_SIZE = 20
    _BattleSessionMembersListener__playerState = constants.PREBATTLE_ACCOUNT_STATE.UNKNOWN
    _BattleSessionMembersListener__playerRoles = 0
    _BattleSessionMembersListener__isFull = False
    _BattleSessionMembersListener__teamState = constants.PREBATTLE_TEAM_STATE.NOT_READY
    _BattleSessionMembersListener__players = { }
    _BattleSessionMembersListener__playerStatesMessageKeys = {
        constants.PREBATTLE_ACCOUNT_STATE.READY: '#system_messages:bs/memberReady',
        constants.PREBATTLE_ACCOUNT_STATE.NOT_READY: '#system_messages:bs/memberNotReady',
        constants.PREBATTLE_ACCOUNT_STATE.OFFLINE: '#system_messages:bs/memberOffline' }
    
    def __init__(self, page):
        self._BattleSessionMembersListener__pageProxy = weakref.proxy(page)

    
    def start(self):
        self._BattleSessionMembersListener__subscribeToPrebattleEvents()

    
    def destroy(self):
        self._BattleSessionMembersListener__unsubscribeFromPrebattleEvents()
        self._BattleSessionMembersListener__pageProxy = None
        self._BattleSessionMembersListener__playerState = constants.PREBATTLE_ACCOUNT_STATE.UNKNOWN
        self._BattleSessionMembersListener__isFull = False
        self._BattleSessionMembersListener__teamState = constants.PREBATTLE_TEAM_STATE.NOT_READY
        self._BattleSessionMembersListener__players.clear()

    
    def isCanSendInvite(self):
        if self._BattleSessionMembersListener__playerRoles & constants.PREBATTLE_ROLE.INVITE != 0 and not (self._BattleSessionMembersListener__isFull):
            pass
        return self._BattleSessionMembersListener__teamState == constants.PREBATTLE_TEAM_STATE.NOT_READY

    
    def isCanKick(self):
        if AccountPrebattle.getMemberTeam() == 1:
            return self._BattleSessionMembersListener__playerRoles & constants.PREBATTLE_ROLE.KICK_1 != 0
        return self._BattleSessionMembersListener__playerRoles & constants.PREBATTLE_ROLE.KICK_2 != 0

    
    def isCanAssign(self):
        if self._BattleSessionMembersListener__teamState != constants.PREBATTLE_TEAM_STATE.NOT_READY:
            return False
        if AccountPrebattle.getMemberTeam() == 1:
            return self._BattleSessionMembersListener__playerRoles & constants.PREBATTLE_ROLE.ASSIGNMENT_1 != 0
        return self._BattleSessionMembersListener__playerRoles & constants.PREBATTLE_ROLE.ASSIGNMENT_2 != 0

    
    def isCanChangeComment(self):
        return self._BattleSessionMembersListener__playerRoles & constants.PREBATTLE_ROLE.CHANGE_COMMENT != 0

    
    def isCreator(self):
        return self._BattleSessionMembersListener__playerRoles & constants.PREBATTLE_ROLE.COMPANY_CREATOR != 0

    
    def isCanChangeOpenState(self):
        return self._BattleSessionMembersListener__playerRoles & constants.PREBATTLE_ROLE.OPEN_CLOSE != 0

    
    def isPlayerReady(self):
        return self.getPlayerState() == constants.PREBATTLE_ACCOUNT_STATE.READY

    
    def isTeamReady(self):
        return self.getTeamState() != constants.PREBATTLE_TEAM_STATE.NOT_READY

    
    def params(self):
        params = []
        if not self._BattleSessionMembersListener__getClientPrebattle().settings:
            pass
        settings = { }
        if not self._BattleSessionMembersListener__getClientPrebattle().properties:
            pass
        properties = { }
        extraData = settings.get('extraData', { })
        session = AccountPrebattle.getPrebattleLocalizedData(extraData).get('session_name', '')
        description = AccountPrebattle.getPrebattleLocalizedData(extraData).get('desc', '')
        if session:
            description = session + '\n' + description
        
        params.append(description)
        battlesLimit = settings.get('battlesLimit', 0)
        winsLimit = settings.get('winsLimit', '-')
        params.append('%d/%s' % (battlesLimit, str(winsLimit)))
        arenaTypeID = settings.get('arenaTypeID', False)
        if arenaTypeID:
            g_cache = g_cache
            import ArenaType
            params.append(g_cache[arenaTypeID].name)
        else:
            params.append('')
        firstTeam = extraData.get('opponents', { }).get('1', { }).get('name', '')
        secondTeam = extraData.get('opponents', { }).get('2', { }).get('name', '')
        params.append(firstTeam)
        params.append(secondTeam)
        wins = properties.get('wins', [
            0,
            0,
            0])
        params.append('%d:%d' % (wins[1], wins[2]))
        params.append(AccountPrebattle.getPrebattleLocalizedData(extraData).get('event_name', ''))
        return params

    params = property(params)
    
    def startTime(self):
        if not self._BattleSessionMembersListener__getClientPrebattle().settings:
            pass
        settings = { }
        startTime = settings.get('startTime', 0)
        if startTime:
            localUTC = datetime.utcfromtimestamp(time_utils.makeLocalServerTime(startTime))
            if localUTC > datetime.utcnow():
                delta = datetime.utcfromtimestamp(time_utils.makeLocalServerTime(startTime)) - datetime.utcnow()
                return delta.seconds
        
        return 0

    startTime = property(startTime)
    
    def totalLevelLimit(self):
        return self._BattleSessionMembersListener__getClientPrebattle().settings.get('limit_total_level', (0, 65535))

    totalLevelLimit = property(totalLevelLimit)
    
    def maxPlayersLimit(self):
        return self._BattleSessionMembersListener__getClientPrebattle().settings.get('limit_max_count', { }).get(AccountPrebattle.getMemberTeam(), '-')

    maxPlayersLimit = property(maxPlayersLimit)
    
    def isOpened(self):
        return bool(self._BattleSessionMembersListener__getClientPrebattle().settings.get('isOpened', False))

    isOpened = property(isOpened)
    
    def creator(self):
        creator = self._BattleSessionMembersListener__getClientPrebattle().settings.get('creator', '')
        clan = self._BattleSessionMembersListener__getClientPrebattle().settings.get('creatorClanAbbrev', '')
        if clan != '':
            creator += '[%s]' % clan
        
        return creator

    creator = property(creator)
    
    def getPlayerState(self):
        return self._BattleSessionMembersListener__playerState

    
    def getTeamState(self):
        return self._BattleSessionMembersListener__teamState

    
    def getPlayersList(self, roster):
        return self._BattleSessionMembersListener__players.get(roster, { }).values()

    
    def kickPlayer(self, accId):
        player = BigWorld.player()
        if player:
            pass
        1
        kickFunc = None
        if kickFunc is not None:
            kickFunc(accId, (lambda resultID: pass))
        elif constants.IS_DEVELOPMENT:
            LOG_ERROR('Method BigWorld.player().prb_kick not found')
        

    
    def _BattleSessionMembersListener__getClientPrebattle(self):
        player = BigWorld.player()
        if player:
            return getattr(player, 'prebattle', None)

    
    def _BattleSessionMembersListener__setPlayerNotReadyState(self, state):
        if state == self._BattleSessionMembersListener__playerState:
            return None
        player = BigWorld.player()
        if player:
            pass
        1
        setStateFunc = None
        if setStateFunc is not None:
            setStateFunc(state, (lambda resultID: pass))
        elif constants.IS_DEVELOPMENT:
            LOG_ERROR('Method BigWorld.player().prb_notReady not found')
        

    
    def _BattleSessionMembersListener__getRequiredInfo(self, prebattle):
        self._BattleSessionMembersListener__players.clear()
        settings = prebattle.settings
        if settings is not None:
            type = settings.get('type')
            if AccountPrebattle.getMemberTeam():
                self._ROSTERS = self._TEAM_ROSTERS[AccountPrebattle.getMemberTeam()]
            
            continue
            self._MAX_SIZE = _[1]([ settings.get('limit_max_count', { }).get(roster, 4) for roster in self._ROSTERS ])
            if type not in (constants.PREBATTLE_TYPE.TOURNAMENT, constants.PREBATTLE_TYPE.CLAN):
                return False
        
        for roster in self._ROSTERS:
            players = prebattle.rosters.get(roster, { })
            for (accID, accInfo) in players.iteritems():
                player = TeamPlayerWrapper(id = accID, **None)
                player.roles = settings.get('roles', { }).get(player.dbID, 0)
                if not player.roles:
                    player.roles = settings.get('clanRoles', { }).get(player.clanDBID, 0)
                
                if not player.roles:
                    player.roles = settings.get('teamRoles', { }).get(AccountPrebattle.getMemberTeam(), 0)
                
                if UsersManager.isCurrentPlayer(player.dbID):
                    self._BattleSessionMembersListener__playerState = player.state
                    self._BattleSessionMembersListener__playerRoles = player.roles
                
                if not self._BattleSessionMembersListener__players.get(roster, { }):
                    self._BattleSessionMembersListener__players[roster] = { }
                
                self._BattleSessionMembersListener__players[roster][accID] = player
            
        
        continue
        self._BattleSessionMembersListener__isFull = _[2]([ len(players) for players in self._BattleSessionMembersListener__players.values() ]) == self._MAX_SIZE
        self._BattleSessionMembersListener__teamState = prebattle.teamStates[self._ROSTERS[0]]
        return True

    
    def _BattleSessionMembersListener__subscribeToPrebattleEvents(self):
        prebattle = self._BattleSessionMembersListener__getClientPrebattle()
        if prebattle is not None:
            if not self._BattleSessionMembersListener__getRequiredInfo(prebattle):
                LOG_ERROR('settings not set or it is not team')
                return None
            prebattle.onRosterReceived += self._BattleSessionMembersListener__onRosterReceived
            prebattle.onPlayerAdded += self._BattleSessionMembersListener__onPlayerAdded
            prebattle.onPlayerRemoved += self._BattleSessionMembersListener__onPlayerRemoved
            prebattle.onPlayerStateChanged += self._BattleSessionMembersListener__onPlayerStateChanged
            prebattle.onSettingUpdated += self._BattleSessionMembersListener__onSettingUpdated
            prebattle.onTeamStatesReceived += self._BattleSessionMembersListener__onTeamStatesReceived
            prebattle.onPlayerRosterChanged += self._BattleSessionMembersListener__onPlayerRosterChanged
            prebattle.onPropertiesReceived += self._BattleSessionMembersListener__onPropertiesChange
            prebattle.onPropertyUpdated += self._BattleSessionMembersListener__onPropertiesChange
        elif constants.IS_DEVELOPMENT:
            LOG_ERROR("Can't subscribe to ClientPrebattle events. ClientPrebattle is None")
        

    
    def _BattleSessionMembersListener__unsubscribeFromPrebattleEvents(self):
        prebattle = self._BattleSessionMembersListener__getClientPrebattle()
        if prebattle is not None:
            prebattle.onRosterReceived -= self._BattleSessionMembersListener__onRosterReceived
            prebattle.onPlayerAdded -= self._BattleSessionMembersListener__onPlayerAdded
            prebattle.onPlayerRemoved -= self._BattleSessionMembersListener__onPlayerRemoved
            prebattle.onPlayerStateChanged -= self._BattleSessionMembersListener__onPlayerStateChanged
            prebattle.onSettingUpdated -= self._BattleSessionMembersListener__onSettingUpdated
            prebattle.onTeamStatesReceived -= self._BattleSessionMembersListener__onTeamStatesReceived
            prebattle.onPlayerRosterChanged -= self._BattleSessionMembersListener__onPlayerRosterChanged
            prebattle.onPropertiesReceived += self._BattleSessionMembersListener__onPropertiesChange
            prebattle.onPropertyUpdated += self._BattleSessionMembersListener__onPropertiesChange
        

    
    def _BattleSessionMembersListener__onRosterReceived(self):
        prebattle = self._BattleSessionMembersListener__getClientPrebattle()
        if prebattle is not None and self._BattleSessionMembersListener__getRequiredInfo(prebattle):
            self._BattleSessionMembersListener__pageProxy.refreshMemberList()
        

    
    def _BattleSessionMembersListener__onPlayerStateChanged(self, id, roster, *args):
        if roster in self._ROSTERS:
            player = self._BattleSessionMembersListener__players.get(roster, { }).get(id)
            if player is not None:
                accInfo = self._BattleSessionMembersListener__getClientPrebattle().rosters.get(roster).get(id)
                player.state = accInfo['state']
                player.vehCompDescr = accInfo['vehCompDescr']
                self._BattleSessionMembersListener__pageProxy.refreshMemberList()
                if UsersManager.isCurrentPlayer(player.dbID):
                    self._BattleSessionMembersListener__playerState = player.state
                    self._BattleSessionMembersListener__pageProxy.refreshSettings()
                else:
                    messageKey = self._BattleSessionMembersListener__playerStatesMessageKeys.get(player.state)
                    if messageKey is not None:
                        message = i18n.makeString(messageKey, player.name)
                        self._BattleSessionMembersListener__pageProxy.addSystemMessage(message)
                    
            
        

    
    def _BattleSessionMembersListener__onPlayerAdded(self, id, roster, *args):
        if roster in self._ROSTERS:
            accInfo = self._BattleSessionMembersListener__getClientPrebattle().rosters.get(roster).get(id)
            player = TeamPlayerWrapper(id = id, **None)
            if not self._BattleSessionMembersListener__players.get(roster, { }):
                self._BattleSessionMembersListener__players[roster] = { }
            
            self._BattleSessionMembersListener__players[roster][id] = player
            continue
            self._BattleSessionMembersListener__isFull = _[1]([ len(players) for players in self._BattleSessionMembersListener__players.values() ]) == self._MAX_SIZE
            self._BattleSessionMembersListener__pageProxy.refreshMemberList()
            if BigWorld.player().id != id:
                message = i18n.makeString('#system_messages:bs/memberJoined', player.name)
                self._BattleSessionMembersListener__pageProxy.addSystemMessage(message)
            
        

    
    def _BattleSessionMembersListener__onPlayerRemoved(self, id, roster, *args):
        if roster in self._ROSTERS:
            player = self._BattleSessionMembersListener__players.get(roster, { }).pop(id)
            continue
            self._BattleSessionMembersListener__isFull = _[1]([ len(players) for players in self._BattleSessionMembersListener__players.values() ]) == self._MAX_SIZE
            self._BattleSessionMembersListener__pageProxy.refreshMemberList()
            if BigWorld.player().id != id:
                message = i18n.makeString('#system_messages:bs/memberLeave', player.name)
                self._BattleSessionMembersListener__pageProxy.addSystemMessage(message)
            
        

    
    def _BattleSessionMembersListener__onSettingUpdated(self, name):
        if name == 'roles':
            settings = self._BattleSessionMembersListener__getClientPrebattle().settings
            if settings is not None:
                rolesMap = settings.get('roles', { })
                for roster in self._ROSTERS:
                    for player in self._BattleSessionMembersListener__players.get(roster, { }).values():
                        roles = rolesMap.get(player.dbID, 0)
                        if player:
                            player.roles = roles
                            if UsersManager.isCurrentPlayer(player.dbID):
                                self._BattleSessionMembersListener__playerState = player.state
                                self._BattleSessionMembersListener__playerRoles = player.roles
                            
                        UsersManager.isCurrentPlayer(player.dbID)
                    
                
                self._BattleSessionMembersListener__pageProxy.refreshMemberList()
            
        
        if name == 'limit_max_count':
            settings = self._BattleSessionMembersListener__getClientPrebattle().settings
            if settings is not None:
                continue
                self._MAX_SIZE = _[1]([ settings.get('limit_max_count', { }).get(roster, 4) for roster in self._ROSTERS ])
            
        
        self._BattleSessionMembersListener__pageProxy.refreshSettings()

    
    def _BattleSessionMembersListener__onTeamStatesReceived(self):
        self._BattleSessionMembersListener__teamState = self._BattleSessionMembersListener__getClientPrebattle().teamStates[self._ROSTERS[0]]
        self._BattleSessionMembersListener__pageProxy.refreshSettings()

    
    def _BattleSessionMembersListener__onPlayerRosterChanged(self, accId, oldRoster, roster, actorID):
        if not self._BattleSessionMembersListener__players.get(roster, { }):
            self._BattleSessionMembersListener__players[roster] = { }
        
        player = self._BattleSessionMembersListener__players[oldRoster][accId]
        if not self._BattleSessionMembersListener__players[self._ROSTERS[0]].get(actorID):
            pass
        actor = self._BattleSessionMembersListener__players[self._ROSTERS[1]].get(actorID)
        self._BattleSessionMembersListener__players[roster][accId] = self._BattleSessionMembersListener__players[oldRoster].pop(accId)
        self._BattleSessionMembersListener__pageProxy.refreshMemberList()
        if actor:
            if roster == self._ROSTERS[0]:
                message = i18n.makeString('#system_messages:memberRosterChangedMain', actor.name, player.name)
            else:
                message = i18n.makeString('#system_messages:memberRosterChangedSecond', actor.name, player.name)
            self._BattleSessionMembersListener__pageProxy.addSystemMessage(message)
        

    
    def _BattleSessionMembersListener__onPropertiesChange(self, name = None):
        self._BattleSessionMembersListener__pageProxy.refreshSettings()



