# Source Generated with Decompyle++
# File: SquadMembersListener.pyc (Python 2.6)

import BigWorld
import constants
from debug_utils import LOG_ERROR
from helpers import i18n
from messenger.UsersManager import UsersManager
from messenger.wrappers import SquadPlayerWrapper
import weakref

class SquadMembersListener(object):
    _SQUAD_ROSTER = 1
    _SQUAD_MAX_SIZE = 4
    _SquadMembersListener__playerState = constants.PREBATTLE_ACCOUNT_STATE.UNKNOWN
    _SquadMembersListener__playerRoles = 0
    _SquadMembersListener__teamState = constants.PREBATTLE_TEAM_STATE.NOT_READY
    _SquadMembersListener__players = { }
    _SquadMembersListener__playerStatesMessageKeys = {
        constants.PREBATTLE_ACCOUNT_STATE.READY: '#system_messages:squad/memberReady',
        constants.PREBATTLE_ACCOUNT_STATE.NOT_READY: '#system_messages:squad/memberNotReady',
        constants.PREBATTLE_ACCOUNT_STATE.OFFLINE: '#system_messages:squad/memberOffline' }
    
    def __init__(self, page):
        self._SquadMembersListener__pageProxy = weakref.proxy(page)

    
    def start(self):
        self._SquadMembersListener__subscribeToPrebattleEvents()

    
    def destroy(self):
        self._SquadMembersListener__unsubscribeFromPrebattleEvents()
        self._SquadMembersListener__pageProxy = None
        self._SquadMembersListener__playerState = constants.PREBATTLE_ACCOUNT_STATE.UNKNOWN
        self._SquadMembersListener__teamState = constants.PREBATTLE_TEAM_STATE.NOT_READY
        self._SquadMembersListener__players.clear()

    
    def isCanSendInvite(self):
        if self._SquadMembersListener__playerRoles & constants.PREBATTLE_ROLE.INVITE != 0 and not (len(self._SquadMembersListener__players) >= self._SQUAD_MAX_SIZE):
            pass
        return self._SquadMembersListener__teamState == constants.PREBATTLE_TEAM_STATE.NOT_READY

    
    def isCanKick(self):
        return self._SquadMembersListener__playerRoles & constants.PREBATTLE_ROLE.KICK_1 != 0

    
    def isCreator(self):
        return self._SquadMembersListener__playerRoles & constants.PREBATTLE_ROLE.COMPANY_CREATOR != 0

    
    def isPlayerReady(self):
        return self.getPlayerState() == constants.PREBATTLE_ACCOUNT_STATE.READY

    
    def isTeamReady(self):
        return self.getTeamState() != constants.PREBATTLE_TEAM_STATE.NOT_READY

    
    def getPlayerState(self):
        return self._SquadMembersListener__playerState

    
    def getTeamState(self):
        return self._SquadMembersListener__teamState

    
    def getPlayersList(self):
        return self._SquadMembersListener__players.values()

    
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
        

    
    def _SquadMembersListener__getClientPrebattle(self):
        player = BigWorld.player()
        if player:
            return getattr(player, 'prebattle', None)

    
    def _SquadMembersListener__setPlayerNotReadyState(self, state):
        if state == self._SquadMembersListener__playerState:
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
        

    
    def _SquadMembersListener__getRequiredInfo(self, prebattle):
        self._SquadMembersListener__players.clear()
        settings = prebattle.settings
        if settings is not None:
            type = settings.get('type')
            self._SQUAD_MAX_SIZE = settings.get('limit_max_count', { }).get(self._SQUAD_ROSTER, 4)
            if type != constants.PREBATTLE_TYPE.SQUAD:
                return False
        
        players = prebattle.rosters.get(self._SQUAD_ROSTER, { })
        for (accID, accInfo) in players.iteritems():
            player = SquadPlayerWrapper(id = accID, **None)
            player.roles = settings.get('roles', { }).get(player.dbID, 0)
            if UsersManager.isCurrentPlayer(player.dbID):
                self._SquadMembersListener__playerState = player.state
                self._SquadMembersListener__playerRoles = player.roles
            
            self._SquadMembersListener__players[accID] = player
        
        self._SquadMembersListener__teamState = prebattle.teamStates[self._SQUAD_ROSTER]
        return True

    
    def _SquadMembersListener__subscribeToPrebattleEvents(self):
        prebattle = self._SquadMembersListener__getClientPrebattle()
        if prebattle is not None:
            if not self._SquadMembersListener__getRequiredInfo(prebattle):
                LOG_ERROR('settings not set or it is not squad')
                return None
            prebattle.onRosterReceived += self._SquadMembersListener__onRosterReceived
            prebattle.onPlayerAdded += self._SquadMembersListener__onPlayerAdded
            prebattle.onPlayerRemoved += self._SquadMembersListener__onPlayerRemoved
            prebattle.onPlayerStateChanged += self._SquadMembersListener__onPlayerStateChanged
            prebattle.onSettingUpdated += self._SquadMembersListener__onSettingUpdated
            prebattle.onTeamStatesReceived += self._SquadMembersListener__onTeamStatesReceived
        elif constants.IS_DEVELOPMENT:
            LOG_ERROR("Can't subscribe to ClientPrebattle events. ClientPrebattle is None")
        

    
    def _SquadMembersListener__unsubscribeFromPrebattleEvents(self):
        prebattle = self._SquadMembersListener__getClientPrebattle()
        if prebattle is not None:
            prebattle.onRosterReceived += self._SquadMembersListener__onRosterReceived
            prebattle.onPlayerAdded -= self._SquadMembersListener__onPlayerAdded
            prebattle.onPlayerRemoved -= self._SquadMembersListener__onPlayerRemoved
            prebattle.onPlayerStateChanged -= self._SquadMembersListener__onPlayerStateChanged
            prebattle.onSettingUpdated -= self._SquadMembersListener__onSettingUpdated
            prebattle.onTeamStatesReceived -= self._SquadMembersListener__onTeamStatesReceived
        

    
    def _SquadMembersListener__onRosterReceived(self):
        prebattle = self._SquadMembersListener__getClientPrebattle()
        if prebattle is not None and self._SquadMembersListener__getRequiredInfo(prebattle):
            self._SquadMembersListener__pageProxy.refreshMemberList()
        

    
    def _SquadMembersListener__onPlayerStateChanged(self, id, roster, *args):
        if roster == self._SQUAD_ROSTER:
            player = self._SquadMembersListener__players.get(id)
            if player is not None:
                accInfo = self._SquadMembersListener__getClientPrebattle().rosters.get(roster).get(id)
                player.state = accInfo['state']
                player.vehCompDescr = accInfo['vehCompDescr']
                if UsersManager.isCurrentPlayer(player.dbID):
                    self._SquadMembersListener__playerState = player.state
                else:
                    messageKey = self._SquadMembersListener__playerStatesMessageKeys.get(player.state)
                    if messageKey is not None:
                        message = i18n.makeString(messageKey, player.name)
                        self._SquadMembersListener__pageProxy.addSystemMessage(message)
                    
                self._SquadMembersListener__pageProxy.refreshMemberList()
            
        

    
    def _SquadMembersListener__onPlayerAdded(self, id, roster, *args):
        if roster == self._SQUAD_ROSTER:
            accInfo = self._SquadMembersListener__getClientPrebattle().rosters.get(roster).get(id)
            player = SquadPlayerWrapper(id = id, **None)
            self._SquadMembersListener__players[id] = player
            self._SquadMembersListener__pageProxy.refreshMemberList()
            if BigWorld.player().id != id:
                message = i18n.makeString('#system_messages:squad/memberJoined', player.name)
                self._SquadMembersListener__pageProxy.addSystemMessage(message)
            
        

    
    def _SquadMembersListener__onPlayerRemoved(self, id, roster, *args):
        if roster == self._SQUAD_ROSTER:
            player = self._SquadMembersListener__players.pop(id)
            self._SquadMembersListener__pageProxy.refreshMemberList()
            if BigWorld.player().id != id:
                message = i18n.makeString('#system_messages:squad/memberLeave', player.name)
                self._SquadMembersListener__pageProxy.addSystemMessage(message)
            
        

    
    def _SquadMembersListener__onSettingUpdated(self, name):
        if name == 'roles':
            settings = self._SquadMembersListener__getClientPrebattle().settings
            if settings is not None:
                rolesMap = settings.get('roles', { })
                for player in self._SquadMembersListener__players.values():
                    roles = rolesMap.get(player.dbID, 0)
                    if player:
                        player.roles = roles
                        if UsersManager.isCurrentPlayer(player.dbID):
                            self._SquadMembersListener__playerState = player.state
                            self._SquadMembersListener__playerRoles = player.roles
                        
                    UsersManager.isCurrentPlayer(player.dbID)
                
                self._SquadMembersListener__pageProxy.refreshMemberList()
            
        
        if name == 'limit_max_count':
            settings = self._SquadMembersListener__getClientPrebattle().settings
            if settings is not None:
                self._SQUAD_MAX_SIZE = settings.get('limit_max_count', { }).get(self._SQUAD_ROSTER, 4)
                self._SquadMembersListener__pageProxy.refreshMemberList()
            
        

    
    def _SquadMembersListener__onTeamStatesReceived(self):
        self._SquadMembersListener__teamState = self._SquadMembersListener__getClientPrebattle().teamStates[self._SQUAD_ROSTER]
        self._SquadMembersListener__pageProxy.refreshMemberList()



