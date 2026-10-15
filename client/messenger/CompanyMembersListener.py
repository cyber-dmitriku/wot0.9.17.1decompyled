# Source Generated with Decompyle++
# File: CompanyMembersListener.pyc (Python 2.6)

import BigWorld
import constants
from debug_utils import LOG_ERROR, LOG_DEBUG
from helpers import i18n
from messenger import passCensor
from messenger.UsersManager import UsersManager
from messenger.wrappers import TeamPlayerWrapper
import weakref

class CompanyMembersListener(object):
    _ROSTERS = (1, 17)
    _MAX_SIZE = 20
    _CompanyMembersListener__playerState = constants.PREBATTLE_ACCOUNT_STATE.UNKNOWN
    _CompanyMembersListener__playerRoles = 0
    _CompanyMembersListener__playerRoster = None
    _CompanyMembersListener__isFull = False
    _CompanyMembersListener__teamState = constants.PREBATTLE_TEAM_STATE.NOT_READY
    _CompanyMembersListener__players = { }
    _CompanyMembersListener__playerStatesMessageKeys = {
        constants.PREBATTLE_ACCOUNT_STATE.READY: '#system_messages:team/memberReady',
        constants.PREBATTLE_ACCOUNT_STATE.NOT_READY: '#system_messages:team/memberNotReady',
        constants.PREBATTLE_ACCOUNT_STATE.OFFLINE: '#system_messages:team/memberOffline' }
    division = constants.PREBATTLE_COMPANY_DIVISION.ABSOLUTE
    
    def __init__(self, page):
        self._CompanyMembersListener__pageProxy = weakref.proxy(page)

    
    def start(self):
        self._CompanyMembersListener__subscribeToPrebattleEvents()

    
    def destroy(self):
        self._CompanyMembersListener__unsubscribeFromPrebattleEvents()
        self._CompanyMembersListener__pageProxy = None
        self._CompanyMembersListener__playerState = constants.PREBATTLE_ACCOUNT_STATE.UNKNOWN
        self._CompanyMembersListener__isFull = False
        self._CompanyMembersListener__teamState = constants.PREBATTLE_TEAM_STATE.NOT_READY
        self._CompanyMembersListener__players.clear()

    
    def isCanSendInvite(self):
        if self._CompanyMembersListener__playerRoles & constants.PREBATTLE_ROLE.INVITE != 0 and not (self._CompanyMembersListener__isFull):
            pass
        return self._CompanyMembersListener__teamState == constants.PREBATTLE_TEAM_STATE.NOT_READY

    
    def isCanKick(self):
        return self._CompanyMembersListener__playerRoles & constants.PREBATTLE_ROLE.KICK_1 != 0

    
    def isCanAssign(self):
        if self._CompanyMembersListener__teamState == constants.PREBATTLE_TEAM_STATE.NOT_READY:
            pass
        return self._CompanyMembersListener__playerRoles & constants.PREBATTLE_ROLE.ASSIGNMENT_1 != 0

    
    def isCanChangeComment(self):
        return self._CompanyMembersListener__playerRoles & constants.PREBATTLE_ROLE.CHANGE_COMMENT != 0

    
    def isCanChangeDivision(self):
        if self._CompanyMembersListener__playerRoles & constants.PREBATTLE_ROLE.CHANGE_DIVISION != 0:
            pass
        return not self.isTeamReady()

    
    def isCreator(self):
        return self._CompanyMembersListener__playerRoles & constants.PREBATTLE_ROLE.COMPANY_CREATOR != 0

    
    def isCanChangeOpenState(self):
        return self._CompanyMembersListener__playerRoles & constants.PREBATTLE_ROLE.OPEN_CLOSE != 0

    
    def isPlayerReady(self):
        return self.getPlayerState() == constants.PREBATTLE_ACCOUNT_STATE.READY

    
    def isTeamReady(self):
        return self.getTeamState() != constants.PREBATTLE_TEAM_STATE.NOT_READY

    
    def isInMainRoster(self):
        return self._CompanyMembersListener__playerRoster == self._ROSTERS[0]

    
    def comment(self):
        prebattle = self._CompanyMembersListener__getClientPrebattle()
        if prebattle is not None:
            pass
        1
        comment = ''
        if self.isCreator():
            return comment
        return passCensor(comment)

    comment = property(comment)
    
    def isOpened(self):
        prebattle = self._CompanyMembersListener__getClientPrebattle()
        if prebattle is not None:
            return bool(prebattle.settings.get('isOpened', False))
        return False

    isOpened = property(isOpened)
    
    def creator(self):
        prebattle = self._CompanyMembersListener__getClientPrebattle()
        creator = ''
        if prebattle is not None:
            creator = prebattle.settings.get('creator', '')
            clan = prebattle.settings.get('creatorClanAbbrev', '')
            if clan != '':
                creator += '[%s]' % clan
            
        
        return creator

    creator = property(creator)
    
    def creatorName(self):
        prebattle = self._CompanyMembersListener__getClientPrebattle()
        if prebattle is not None:
            return prebattle.settings.get('creator', '')
        return ''

    creatorName = property(creatorName)
    
    def getLevelsLimits(self):
        prebattle = self._CompanyMembersListener__getClientPrebattle()
        if prebattle is not None:
            return prebattle.settings.get('limit_level', (1, 10))
        return (1, 10)

    
    def getSPGLevelsLimits(self):
        prebattle = self._CompanyMembersListener__getClientPrebattle()
        if prebattle is not None:
            (mn, mx) = self.getLevelsLimits()
            return prebattle.settings.get('limit_class_level', { }).get('SPG', (mn, mx))
        return (1, 10)

    
    def getATSPGLevelsLimits(self):
        prebattle = self._CompanyMembersListener__getClientPrebattle()
        if prebattle is not None:
            (mn, mx) = self.getLevelsLimits()
            return prebattle.settings.get('limit_class_level', { }).get('AT-SPG', (mn, mx))
        return (1, 10)

    
    def getHeavyTanksLevelsLimits(self):
        prebattle = self._CompanyMembersListener__getClientPrebattle()
        if prebattle is not None:
            (mn, mx) = self.getLevelsLimits()
            return prebattle.settings.get('limit_class_level', { }).get('heavyTank', (mn, mx))
        return (1, 10)

    
    def getMediumTanksLevelsLimits(self):
        prebattle = self._CompanyMembersListener__getClientPrebattle()
        if prebattle is not None:
            (mn, mx) = self.getLevelsLimits()
            return prebattle.settings.get('limit_class_level', { }).get('mediumTank', (mn, mx))
        return (1, 10)

    
    def getLightTanksLevelsLimits(self):
        prebattle = self._CompanyMembersListener__getClientPrebattle()
        if prebattle is not None:
            (mn, mx) = self.getLevelsLimits()
            return prebattle.settings.get('limit_class_level', { }).get('lightTank', (mn, mx))
        return (1, 10)

    
    def getTotalLevelsLimits(self):
        prebattle = self._CompanyMembersListener__getClientPrebattle()
        if prebattle is not None:
            return prebattle.settings.get('limit_total_level', (1, 150))
        return (1, 150)

    
    def maxCountLimit(self):
        prebattle = self._CompanyMembersListener__getClientPrebattle()
        if prebattle is not None:
            return prebattle.settings.get('limit_max_Count', { }).get(self._ROSTERS[0], 15)
        return 15

    maxCountLimit = property(maxCountLimit)
    
    def getPlayerState(self):
        return self._CompanyMembersListener__playerState

    
    def getTeamState(self):
        return self._CompanyMembersListener__teamState

    
    def getPlayersList(self, roster):
        return self._CompanyMembersListener__players.get(roster, { }).values()

    
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
        

    
    def _CompanyMembersListener__getClientPrebattle(self):
        player = BigWorld.player()
        if player:
            return getattr(player, 'prebattle', None)

    
    def _CompanyMembersListener__setPlayerNotReadyState(self, state):
        if state == self._CompanyMembersListener__playerState:
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
        

    
    def _CompanyMembersListener__getRequiredInfo(self, prebattle):
        self._CompanyMembersListener__players.clear()
        settings = prebattle.settings
        if settings is not None:
            type = settings.get('type')
            continue
            self._MAX_SIZE = _[1]([ settings.get('limit_max_count', { }).get(roster, 4) for roster in self._ROSTERS ])
            if type != constants.PREBATTLE_TYPE.COMPANY:
                return False
            self.division = settings.get('division', constants.PREBATTLE_COMPANY_DIVISION.ABSOLUTE)
        
        for roster in self._ROSTERS:
            players = prebattle.rosters.get(roster, { })
            for (accID, accInfo) in players.iteritems():
                player = TeamPlayerWrapper(id = accID, **None)
                player.roles = settings.get('roles', { }).get(player.dbID, 0)
                if UsersManager.isCurrentPlayer(player.dbID):
                    self._CompanyMembersListener__playerState = player.state
                    self._CompanyMembersListener__playerRoles = player.roles
                    self._CompanyMembersListener__playerRoster = roster
                
                if not self._CompanyMembersListener__players.get(roster, { }):
                    self._CompanyMembersListener__players[roster] = { }
                
                self._CompanyMembersListener__players[roster][accID] = player
            
        
        continue
        self._CompanyMembersListener__isFull = _[2]([ len(players) for players in self._CompanyMembersListener__players.values() ]) == self._MAX_SIZE
        self._CompanyMembersListener__teamState = prebattle.teamStates[self._ROSTERS[0]]
        return True

    
    def _CompanyMembersListener__subscribeToPrebattleEvents(self):
        prebattle = self._CompanyMembersListener__getClientPrebattle()
        if prebattle is not None:
            if not self._CompanyMembersListener__getRequiredInfo(prebattle):
                LOG_ERROR('settings not set or it is not team')
                return None
            prebattle.onRosterReceived += self._CompanyMembersListener__onRosterReceived
            prebattle.onPlayerAdded += self._CompanyMembersListener__onPlayerAdded
            prebattle.onPlayerRemoved += self._CompanyMembersListener__onPlayerRemoved
            prebattle.onPlayerStateChanged += self._CompanyMembersListener__onPlayerStateChanged
            prebattle.onSettingUpdated += self._CompanyMembersListener__onSettingUpdated
            prebattle.onTeamStatesReceived += self._CompanyMembersListener__onTeamStatesReceived
            prebattle.onPlayerRosterChanged += self._CompanyMembersListener__onPlayerRosterChanged
        elif constants.IS_DEVELOPMENT:
            LOG_ERROR("Can't subscribe to ClientPrebattle events. ClientPrebattle is None")
        

    
    def _CompanyMembersListener__unsubscribeFromPrebattleEvents(self):
        prebattle = self._CompanyMembersListener__getClientPrebattle()
        if prebattle is not None:
            prebattle.onRosterReceived -= self._CompanyMembersListener__onRosterReceived
            prebattle.onPlayerAdded -= self._CompanyMembersListener__onPlayerAdded
            prebattle.onPlayerRemoved -= self._CompanyMembersListener__onPlayerRemoved
            prebattle.onPlayerStateChanged -= self._CompanyMembersListener__onPlayerStateChanged
            prebattle.onSettingUpdated -= self._CompanyMembersListener__onSettingUpdated
            prebattle.onTeamStatesReceived -= self._CompanyMembersListener__onTeamStatesReceived
            prebattle.onPlayerRosterChanged -= self._CompanyMembersListener__onPlayerRosterChanged
        

    
    def _CompanyMembersListener__onRosterReceived(self):
        prebattle = self._CompanyMembersListener__getClientPrebattle()
        if prebattle is not None and self._CompanyMembersListener__getRequiredInfo(prebattle):
            self._CompanyMembersListener__pageProxy.refreshMemberList()
        

    
    def _CompanyMembersListener__onPlayerStateChanged(self, id, roster, *args):
        if roster in self._ROSTERS:
            player = self._CompanyMembersListener__players.get(roster, { }).get(id)
            if player is not None:
                accInfo = self._CompanyMembersListener__getClientPrebattle().rosters.get(roster).get(id)
                player.state = accInfo['state']
                player.vehCompDescr = accInfo['vehCompDescr']
                self._CompanyMembersListener__pageProxy.refreshMemberList()
                if UsersManager.isCurrentPlayer(player.dbID):
                    self._CompanyMembersListener__playerState = player.state
                    self._CompanyMembersListener__pageProxy.refreshSettings()
                else:
                    messageKey = self._CompanyMembersListener__playerStatesMessageKeys.get(player.state)
                    if messageKey is not None:
                        message = i18n.makeString(messageKey, player.name)
                        self._CompanyMembersListener__pageProxy.addSystemMessage(message)
                    
            
        

    
    def _CompanyMembersListener__onPlayerAdded(self, id, roster, *args):
        if roster in self._ROSTERS:
            accInfo = self._CompanyMembersListener__getClientPrebattle().rosters.get(roster).get(id)
            player = TeamPlayerWrapper(id = id, **None)
            if not self._CompanyMembersListener__players.get(roster, { }):
                self._CompanyMembersListener__players[roster] = { }
            
            self._CompanyMembersListener__players[roster][id] = player
            continue
            self._CompanyMembersListener__isFull = _[1]([ len(players) for players in self._CompanyMembersListener__players.values() ]) == self._MAX_SIZE
            self._CompanyMembersListener__pageProxy.refreshMemberList()
            if BigWorld.player().id != id:
                message = i18n.makeString('#system_messages:team/memberJoined', player.name)
                self._CompanyMembersListener__pageProxy.addSystemMessage(message)
            
        

    
    def _CompanyMembersListener__onPlayerRemoved(self, id, roster, *args):
        if roster in self._ROSTERS:
            player = self._CompanyMembersListener__players.get(roster, { }).pop(id)
            continue
            self._CompanyMembersListener__isFull = _[1]([ len(players) for players in self._CompanyMembersListener__players.values() ]) == self._MAX_SIZE
            self._CompanyMembersListener__pageProxy.refreshMemberList()
            if BigWorld.player().id != id:
                message = i18n.makeString('#system_messages:team/memberLeave', player.name)
                self._CompanyMembersListener__pageProxy.addSystemMessage(message)
            
        

    
    def _CompanyMembersListener__onSettingUpdated(self, name):
        settings = self._CompanyMembersListener__getClientPrebattle().settings
        if name in ('roles', 'limit_level', 'limit_total_level'):
            if settings is not None:
                rolesMap = settings.get('roles', { })
                if name == 'roles':
                    for roster in self._ROSTERS:
                        for player in self._CompanyMembersListener__players.get(roster, { }).values():
                            roles = rolesMap.get(player.dbID, 0)
                            if player:
                                player.roles = roles
                                if UsersManager.isCurrentPlayer(player.dbID):
                                    self._CompanyMembersListener__playerState = player.state
                                    self._CompanyMembersListener__playerRoles = player.roles
                                
                            UsersManager.isCurrentPlayer(player.dbID)
                        
                    
                
                self._CompanyMembersListener__pageProxy.refreshMemberList()
            
        
        if name == 'limit_max_count':
            if settings is not None:
                continue
                self._MAX_SIZE = _[1]([ settings.get('limit_max_count', { }).get(roster, 4) for roster in self._ROSTERS ])
            
        
        if name == 'division':
            if settings is not None:
                self.division = settings.get('division', constants.PREBATTLE_COMPANY_DIVISION.ABSOLUTE)
            
        
        self._CompanyMembersListener__pageProxy.refreshSettings()

    
    def _CompanyMembersListener__onTeamStatesReceived(self):
        self._CompanyMembersListener__teamState = self._CompanyMembersListener__getClientPrebattle().teamStates[self._ROSTERS[0]]
        self._CompanyMembersListener__pageProxy.refreshSettings()

    
    def _CompanyMembersListener__onPlayerRosterChanged(self, accId, oldRoster, roster, actorID):
        if not self._CompanyMembersListener__players.get(roster, { }):
            self._CompanyMembersListener__players[roster] = { }
        
        player = self._CompanyMembersListener__players[oldRoster][accId]
        if not self._CompanyMembersListener__players[self._ROSTERS[0]].get(actorID):
            pass
        actor = self._CompanyMembersListener__players[self._ROSTERS[1]].get(actorID)
        if UsersManager.isCurrentPlayer(player.dbID):
            self._CompanyMembersListener__playerRoster = roster
            self._CompanyMembersListener__pageProxy.refreshSettings()
        
        self._CompanyMembersListener__players[roster][accId] = self._CompanyMembersListener__players[oldRoster].pop(accId)
        self._CompanyMembersListener__pageProxy.refreshMemberList()
        if actor:
            if roster == self._ROSTERS[0]:
                message = i18n.makeString('#system_messages:memberRosterChangedMain', actor.name, player.name)
            else:
                message = i18n.makeString('#system_messages:memberRosterChangedSecond', actor.name, player.name)
            self._CompanyMembersListener__pageProxy.addSystemMessage(message)
        



