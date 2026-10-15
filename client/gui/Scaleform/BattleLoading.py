# Source Generated with Decompyle++
# File: BattleLoading.pyc (Python 2.6)

import BigWorld
import constants
import ArenaType
import BattleReplay
from helpers.tips import getTip
from gui.Scaleform import VoiceChatInterface
from gui.Scaleform.windows import UIInterface
from gui.Scaleform.Waiting import Waiting
from account_helpers.AccountPrebattle import AccountPrebattle
from messenger.gui import MessengerDispatcher
from gui.Scaleform.utils.functions import getBattleSubTypeWinText, getArenaSubTypeName, isBaseExists
from helpers.i18n import makeString
from gui.Scaleform import ColorSchemeManager
from gui.Scaleform import VehicleActions
from debug_utils import LOG_DEBUG
_MAP_BG_SOURCE = '../maps/icons/map/screen/%s.png'
_CONTOUR_ICONS_MASK = '../maps/icons/vehicle/contour/%(unicName)s.png'

class BattleLoading(UIInterface):
    
    def __init__(self):
        self.onLoaded = None
        self.callbackId = None
        self._BattleLoading__arena = getattr(BigWorld.player(), 'arena', None)
        self._BattleLoading__progress = 0
        self._BattleLoading__winTextInit = False
        UIInterface.__init__(self)

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        if self._BattleLoading__arena:
            self._BattleLoading__arena.onNewVehicleListReceived += self._BattleLoading__updatePlayers
            self._BattleLoading__arena.onNewStatisticsReceived += self._BattleLoading__updatePlayers
            self._BattleLoading__arena.onVehicleAdded += self._BattleLoading__updatePlayers
            self._BattleLoading__arena.onVehicleStatisticsUpdate += self._BattleLoading__updatePlayers
            self._BattleLoading__arena.onVehicleKilled += self._BattleLoading__updatePlayers
            self._BattleLoading__arena.onAvatarReady += self._BattleLoading__updatePlayers
            self._BattleLoading__arena.onVehicleUpdated += self._BattleLoading__updatePlayers
            MessengerDispatcher.g_instance.users.onUsersRosterReceived += self._BattleLoading__updatePlayers
        
        self.uiHolder.addExternalCallbacks({
            'loading.getData': self._BattleLoading__populateData })
        self.colorManager = ColorSchemeManager._ColorSchemeManager()
        self.colorManager.populateUI(proxy)
        self.uiHolder.movie.backgroundAlpha = 1
        self._BattleLoading__populateData()
        self.isSpaceLoaded()
        Waiting.hide('loadPage')
        Waiting.close()

    
    def dispossessUI(self):
        if self.callbackId is not None:
            BigWorld.cancelCallback(self.callbackId)
            self.callbackId = None
        
        if self._BattleLoading__arena:
            self._BattleLoading__arena.onNewVehicleListReceived -= self._BattleLoading__updatePlayers
            self._BattleLoading__arena.onNewStatisticsReceived -= self._BattleLoading__updatePlayers
            self._BattleLoading__arena.onVehicleAdded -= self._BattleLoading__updatePlayers
            self._BattleLoading__arena.onVehicleStatisticsUpdate -= self._BattleLoading__updatePlayers
            self._BattleLoading__arena.onVehicleKilled -= self._BattleLoading__updatePlayers
            self._BattleLoading__arena.onAvatarReady -= self._BattleLoading__updatePlayers
            self._BattleLoading__arena.onVehicleUpdated -= self._BattleLoading__updatePlayers
            MessengerDispatcher.g_instance.users.onUsersRosterReceived -= self._BattleLoading__updatePlayers
        
        if self.colorManager:
            self.colorManager.dispossessUI()
        
        self.uiHolder.removeExternalCallbacks('loading.getData')
        self._BattleLoading__arena = None
        UIInterface.dispossessUI(self)

    
    def isSpaceLoaded(self):
        self.callbackId = None
        if BattleReplay.g_replayCtrl.isTimeWarpInProgress:
            pass
        1
        status = BigWorld.spaceLoadStatus()
        if status > self._BattleLoading__progress:
            self._BattleLoading__progress = status
            self._BattleLoading__setProgress(status)
        
        if status < 1:
            self.callbackId = BigWorld.callback(0.5, self.isSpaceLoaded)
            BigWorld.SetDrawInflux(False)
            return None
        BigWorld.SetDrawInflux(True)
        BigWorld.player().onSpaceLoaded()
        self.isLoaded()

    
    def isLoaded(self):
        self.callbackId = None
        if not BigWorld.worldDrawEnabled():
            self.callbackId = BigWorld.callback(0.5, self.isLoaded)
            return None
        g_windowsManager = g_windowsManager
        import gui.WindowsManager
        BigWorld.callback(0.1, g_windowsManager.showBattle)

    
    def _BattleLoading__setProgress(self, value):
        self.call('loading.setProgress', [
            value])

    
    def _BattleLoading__populateData(self, callbackID = None):
        arena = getattr(BigWorld.player(), 'arena', None)
        if arena:
            self.call('loading.setMap', [
                arena.arenaType.name])
            self.call('loading.setMapBG', [
                _MAP_BG_SOURCE % arena.arenaType.geometryName])
            if not arena.extraData:
                pass
            descExtra = AccountPrebattle.getPrebattleDescription({ })
            arenaSubType = getArenaSubTypeName(BigWorld.player().arenaTypeID)
            if descExtra:
                self.call('loading.setBattleType', [
                    arena.guiType + 1,
                    descExtra])
            elif arena.guiType == constants.ARENA_GUI_TYPE.RANDOM:
                self.call('loading.setBattleType', [
                    arenaSubType,
                    '#arenas:type/%s/name' % arenaSubType])
            else:
                self.call('loading.setBattleType', [
                    arena.guiType + 1,
                    '#menu:loading/battleTypes/%d' % arena.guiType])
        
        self.call('loading.setTip', [
            getTip()])
        self._BattleLoading__updatePlayers()

    
    def _BattleLoading__updatePlayers(self, *args):
        stat = {
            1: [],
            2: [] }
        squads = {
            1: { },
            2: { } }
        player = BigWorld.player()
        if player is None:
            return None
        if self._BattleLoading__arena is None:
            return None
        vehicles = self._BattleLoading__arena.vehicles
        for (vId, vData) in vehicles.items():
            team = vData['team']
            if vData['name'] is not None:
                pass
            1
            name = makeString('#ingame_gui:players_panel/unknown_name')
            if vData['clanAbbrev']:
                name = name + '[%s]' % vData['clanAbbrev']
            
            if vData['vehicleType'] is not None:
                vShortName = vData['vehicleType'].type.shortUserString
                vName = vData['vehicleType'].type.userString
                vIcon = _CONTOUR_ICONS_MASK % {
                    'unicName': vData['vehicleType'].type.name.replace(':', '-') }
                balanceWeight = vData['vehicleType'].balanceWeight
            else:
                vName = makeString('#ingame_gui:players_panel/unknown_vehicle')
                vShortName = makeString('#ingame_gui:players_panel/unknown_vehicle')
                vIcon = _CONTOUR_ICONS_MASK % {
                    'unicName': 'unknown' }
                balanceWeight = 0
            if vData['isAlive']:
                pass
            isAlive = vData['isAvatarReady']
            vehActions = VehicleActions.getBitMask(vData.get('events', { }))
            if vData['prebattleID'] != 0:
                if vData['prebattleID'] not in squads[team].keys():
                    squads[team][vData['prebattleID']] = 1
                else:
                    squads[team][vData['prebattleID']] += 1
            
            user = MessengerDispatcher.g_instance.users.getUser(vData['accountDBID'], name)
            stat[team].append([
                name,
                vIcon,
                vShortName,
                not isAlive,
                vId,
                vData['prebattleID'],
                balanceWeight,
                vName,
                not vData['isAlive'],
                vData['name'],
                vData['accountDBID'],
                user.isMuted(),
                vehActions,
                VoiceChatInterface.g_instance.isPlayerSpeaking(vData['accountDBID']),
                vData['isTeamKiller']])
        
        squadsSorted = { }
        squadsSorted[1] = sorted(squads[1].iteritems(), cmp = (lambda x, y: cmp(x[0], y[0])))
        squadsSorted[2] = sorted(squads[2].iteritems(), cmp = (lambda x, y: cmp(x[0], y[0])))
        squadsFiltered = { }
        continue
        squadsFiltered[1] = _[1]
        continue
        squadsFiltered[2] = _[2]
        for team in (1, 2):
            playerVehicleID = None
            if hasattr(player, 'playerVehicleID'):
                playerVehicleID = player.playerVehicleID
            
            value = [
                'team2',
                -1,
                -1]
            data = sorted(stat[team], cmp = _playerComparator)
            for item in data:
                if item[5] in squadsFiltered[team]:
                    pass
                1
                item[5] = 0
                if item[9] == player.name or value[1] == -1 or item[4] == playerVehicleID:
                    value[1] = item[4]
                    if item[5] > 0:
                        value[2] = item[5]
                    
                    value[0] = 'team1'
                    self.setTeams(team)
                    if not self._BattleLoading__winTextInit:
                        self._BattleLoading__winTextInit = True
                        if isBaseExists(BigWorld.player().arenaTypeID, team):
                            pass
                        1
                        teamHasBase = 2
                        winText = getBattleSubTypeWinText(BigWorld.player().arenaTypeID, teamHasBase)
                        self.call('loading.setWinText', [
                            winText])
                    
                
                value.extend(item[:-7])
                value.append(item[10])
                value.append(item[11])
                value.append(item[12])
                value.append(item[13])
                value.append(item[14])
            
            self.call('loading.setTeam', value)
        

    
    def setTeams(self, myTeam):
        arena = getattr(BigWorld.player(), 'arena', None)
        if arena:
            if not arena.extraData:
                pass
            extraData = { }
            team1 = extraData.get('opponents', { }).get('%s' % myTeam, { }).get('name', '#menu:loading/team1')
            if myTeam == 1:
                pass
            1
            team2 = '2'('1', { }).get('name', '#menu:loading/team2')
            self.call('loading.setTeams', [
                team1,
                team2])
        



def _playerComparator(x1, x2):
    if x1[8] < x2[8]:
        return -1
    if x1[8] > x2[8]:
        return 1
    if x1[6] < x2[6]:
        return 1
    if x1[6] > x2[6]:
        return -1
    if x1[2] < x2[2]:
        return -1
    if x1[2] > x2[2]:
        return 1
    if x1[9] < x2[9]:
        return -1
    if x1[9] > x2[9]:
        return 1
    return 0


