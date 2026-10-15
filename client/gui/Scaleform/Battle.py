# Source Generated with Decompyle++
# File: Battle.pyc (Python 2.6)

import math
import GUI
import BigWorld
import ResMgr
import weakref
import Avatar
import FMOD
from account_helpers.AccountSettings import AccountSettings
import constants
import CommandMapping
from gui.Scaleform.Flash import Flash
from windows import BattleWindow
from SettingsInterface import SettingsInterface
from debug_utils import LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_ERROR
from gui import DEPTH_OF_Battle, DEPTH_OF_VehicleMarker, TANKMEN_ROLES_ORDER_DICT, GUI_SETTINGS, g_tankActiveCamouflage
from gui.BattleContext import g_battleContext, PLAYER_ENTITY_NAME
from helpers import i18n, html
from helpers.i18n import makeString
from PlayerEvents import g_playerEvents
from arena_achievements import BATTLE_HERO_TEXTS as heroesTexts, ACHIEVEMENTS as heroesNames
from gui.Scaleform.utils.sound import Sound
from gui.Scaleform.utils.functions import getBattleSubTypeBaseNumder, isControlPointExists
from MemoryCriticalController import g_critMemHandler
from items.vehicles import NUM_EQUIPMENT_SLOTS, VEHICLE_CLASS_TAGS
from messenger.gui import MessengerDispatcher
from messenger.wrappers import UserWrapper
from gui.Scaleform import VoiceChatInterface, ColorSchemeManager
from gui.Scaleform.Minimap import Minimap
from gui.Scaleform.RadialMenu import RadialMenu
from gui.Scaleform.CursorDelegator import g_cursorDelegator
from gui.Scaleform.ingame_help import IngameHelp
import BattleReplay
from gui.Scaleform.SoundManager import SoundManager
from gui.Scaleform import VehicleActions
import Math
_CONTOUR_ICONS_MASK = '../maps/icons/vehicle/contour/%(unicName)s.png'
_BASE_CAPTURE_SOUND_NAME_ENEMY = '/GUI/notifications_FX/base_capture_2'
_BASE_CAPTURE_SOUND_NAME_ALLY = '/GUI/notifications_FX/base_capture_1'

class Battle(BattleWindow):
    PLAYERS_PANEL_LENGTH = 15
    teamBasesPanel = property((lambda self: self._Battle__teamBasesPanel))
    consumablesPanel = property((lambda self: self._Battle__consumablesPanel))
    damagePanel = property((lambda self: self._Battle__damagePanel))
    vMarkersManager = property((lambda self: self._Battle__vMarkersManager))
    vErrorsPanel = property((lambda self: self._Battle__vErrorsPanel))
    vMsgsPanel = property((lambda self: self._Battle__vMsgsPanel))
    pMsgsPanel = property((lambda self: self._Battle__pMsgsPanel))
    minimap = property((lambda self: self._Battle__minimap))
    radialMenu = property((lambda self: self._Battle__radialMenu))
    damageInfoPanel = property((lambda self: self._Battle__damageInfoPanel))
    VEHICLE_DESTROY_TIMER = {
        'ALL': 'all',
        constants.VEHICLE_MISC_STATUS.VEHICLE_DROWN_WARNING: 'drown',
        constants.VEHICLE_MISC_STATUS.VEHICLE_IS_OVERTURNED: 'overturn',
        constants.VEHICLE_MISC_STATUS.IN_DEATH_ZONE: 'death_zone' }
    DENUNCIATIONS = {
        'bot': constants.DENUNCIATION.BOT,
        'flood': constants.DENUNCIATION.FLOOD,
        'offend': constants.DENUNCIATION.OFFEND,
        'notFairPlay': constants.DENUNCIATION.NOT_FAIR_PLAY,
        'teamKill': constants.DENUNCIATION.TEAMKILL,
        'allyEjection': constants.DENUNCIATION.ALLY_EJECTION,
        'openingOfAllyPos': constants.DENUNCIATION.OPENING_OF_ALLY_POS }
    _speakPlayers = { }
    _Battle__cameraVehicleID = -1
    
    def __init__(self):
        self._Battle__timerCallBackId = None
        self._Battle__vehicles = { }
        self._Battle__arena = BigWorld.player().arena
        self._Battle__playersPanelStateChanged = False
        self._Battle__soundManager = None
        BattleWindow.__init__(self, 'battle.swf')
        self._Battle__timerSound = Sound('/GUI/notifications_FX/timer')
        self._Battle__isTimerVisible = False
        self.component.wg_inputKeyMode = 1
        self.component.position.z = DEPTH_OF_Battle
        self.movie.backgroundAlpha = 0
        self.addFsCallbacks({
            'battle.leave': self.onExitBattle })
        self.addExternalCallbacks({
            'battle.showCursor': self.cursorVisibility,
            'Battle.UsersRoster.Appeal': self.onDenunciationReceived,
            'Battle.playersPanelStateChange': self.onPlayersPanelStateChange,
            'Battle.selectPlayer': self.selectPlayer })
        BigWorld.wg_setRedefineKeysMode(False)
        self.onPostmortemVehicleChanged(BigWorld.player().playerVehicleID)

    
    def showAll(self, isShow):
        self.call('battle.showAll', [
            isShow])
        self._Battle__vMarkersManager.active(isShow)

    
    def showCursor(self, isShow):
        self.cursorVisibility(-1, isShow)

    
    def onPlayersPanelStateChange(self, cid, state):
        ppSettings = dict(AccountSettings.getSettings('players_panel'))
        ppSettings['state'] = state
        AccountSettings.setSettings('players_panel', ppSettings)
        self._Battle__playersPanelStateChanged = True

    
    def soundManager(self):
        return self._Battle__soundManager

    soundManager = property(soundManager)
    
    def selectPlayer(self, cid, vehId):
        player = BigWorld.player()
        if isinstance(player, Avatar.PlayerAvatar):
            player.selectPlayer(int(vehId))
        

    
    def onDenunciationReceived(self, cid, uid, userName, topic):
        LOG_DEBUG('!', topic)
        topicID = self.DENUNCIATIONS.get(topic)
        if topicID is not None:
            self._Battle__makeDenunciation(uid, userName, topicID)
        

    
    def _Battle__makeDenunciation(self, uid, userName, topicID):
        player = BigWorld.player()
        violatorKind = constants.VIOLATOR_KIND.UNKNOWN
        for (id, p) in player.arena.vehicles.iteritems():
            if p['accountDBID'] == uid:
                if player.team == p['team']:
                    pass
                1
                violatorKind = constants.VIOLATOR_KIND.ENEMY
                continue
        
        player.makeDenunciation(uid, topicID, violatorKind)
        self._Battle__updatePlayers()
        topicStr = makeString('#menu:denunciation/type%d' % topicID)
        MessengerDispatcher.g_instance.currentWindow.showActionFailureMessage(makeString('#system_messages:denunciation/success') % {
            'name': userName,
            'topic': topicStr })

    
    def onPostmortemVehicleChanged(self, id):
        self._Battle__cameraVehicleID = id
        self._Battle__setPlayerInfo(id)
        self._Battle__updatePlayers()
        self._Battle__damagePanel.switchToVehicle(id)

    
    def showVehicleTimer(self, code, time, warnLvl = 'critical'):
        LOG_DEBUG('show vehicles destroy timer', code, time, warnLvl)
        self.call('destroyTimer.show', [
            self.VEHICLE_DESTROY_TIMER[code],
            time,
            warnLvl])

    
    def hideVehicleTimer(self, code):
        LOG_DEBUG('hide vehicles destroy timer', code)
        self.call('destroyTimer.hide', [
            self.VEHICLE_DESTROY_TIMER[code]])

    
    def showSixthSenseIndicator(self, isShow):
        self.call('sixthSenseIndicator.show', [
            isShow])

    
    def speakingPlayersReset(self):
        for id in self._speakPlayers.keys():
            self.setPlayerSpeaking(id, False)
        
        self._speakPlayers.clear()

    
    def setVisible(self, bool):
        LOG_DEBUG('[Battle] visible', bool)
        self.component.visible = bool

    
    def afterCreate(self):
        player = BigWorld.player()
        LOG_DEBUG('[Battle] afterCreate')
        setattr(self.movie, '_global.wg_isShowLanguageBar', constants.SHOW_LANGUAGE_BAR)
        setattr(self.movie, '_global.wg_isShowVoiceChat', GUI_SETTINGS.voiceChat)
        setattr(self.movie, '_global.wg_isChina', constants.IS_CHINA)
        BattleWindow.afterCreate(self)
        g_playerEvents.onBattleResultsReceived += self._Battle__showFinalStatsResults
        usersManager = MessengerDispatcher.g_instance.users
        usersManager.onUsersRosterUpdate += self._Battle__updatePlayers
        usersManager.onUsersRosterReceived += self._Battle__updatePlayers
        BigWorld.wg_setScreenshotNotifyCallback(self._Battle__screenshotNotifyCallback)
        player.inputHandler.onPostmortemVehicleChanged += self.onPostmortemVehicleChanged
        AccountSettings.onSettingsChanging += self._Battle__accs_onSettingsChanged
        if self._Battle__arena:
            self._Battle__arena.onPeriodChange += self._Battle__onSetArenaTime
            self._Battle__arena.onNewVehicleListReceived += self._Battle__updatePlayers
            self._Battle__arena.onNewStatisticsReceived += self._Battle__updatePlayers
            self._Battle__arena.onVehicleAdded += self._Battle__updatePlayers
            self._Battle__arena.onVehicleStatisticsUpdate += self._Battle__updatePlayers
            self._Battle__arena.onVehicleKilled += self._Battle__updatePlayers
            self._Battle__arena.onAvatarReady += self._Battle__updatePlayers
            self._Battle__arena.onTeamKiller += self._Battle__onTeamKiller
            self._Battle__arena.onVehicleUpdated += self._Battle__updatePlayers
        
        self.proxy = weakref.proxy(self)
        self._speakPlayers.clear()
        VoiceChatInterface.g_instance.populateUI(self.proxy)
        self.colorManager = ColorSchemeManager._ColorSchemeManager()
        self.colorManager.populateUI(self.proxy)
        self._Battle__settingsInterface = SettingsInterface()
        self._Battle__settingsInterface.populateUI(self.proxy)
        self._Battle__teamBasesPanel = TeamBasesPanel(self.proxy)
        self._Battle__fragCorrelation = FragCorrelationPanel(self.proxy)
        self._Battle__debugPanel = DebugPanel(self.proxy)
        self._Battle__consumablesPanel = ConsumablesPanel(self.proxy)
        self._Battle__damagePanel = DamagePanel(self.proxy)
        self._Battle__vMarkersManager = VehicleMarkersManager(self.proxy)
        self._Battle__ingameHelp = IngameHelp(self.proxy)
        self._Battle__minimap = Minimap(self.proxy)
        self._Battle__radialMenu = RadialMenu(self.proxy)
        self._Battle__soundManager = SoundManager()
        self._Battle__soundManager.populateUI(self.proxy)
        self._Battle__damageInfoPanel = VehicleDamageInfoPanel(self.proxy)
        isColorBlind = AccountSettings.getSettings('isColorBlind')
        self._Battle__vErrorsPanel = FadingMessagesPanel(self.proxy, 'VehicleErrorsPanel', 'gui/vehicle_errors_panel.xml', isColorBlind = isColorBlind)
        self._Battle__vMsgsPanel = FadingMessagesPanel(self.proxy, 'VehicleMessagesPanel', 'gui/vehicle_messages_panel.xml', isColorBlind = isColorBlind)
        self._Battle__pMsgsPanel = FadingMessagesPanel(self.proxy, 'PlayerMessagesPanel', 'gui/player_messages_panel.xml', isColorBlind = isColorBlind)
        MessengerDispatcher.g_instance.battleMessenger.updateColors(isColorBlind = isColorBlind)
        self._Battle__teamBasesPanel.start()
        self._Battle__debugPanel.start()
        self._Battle__consumablesPanel.start()
        self._Battle__damagePanel.start()
        self._Battle__ingameHelp.start()
        self._Battle__vErrorsPanel.start()
        self._Battle__vMsgsPanel.start()
        self._Battle__pMsgsPanel.start()
        self._Battle__vMarkersManager.start()
        self._Battle__vMarkersManager.setMarkerDuration(GUI_SETTINGS.markerHitSplashDuration)
        self._Battle__vMarkersManager.setMarkerSettings(AccountSettings.getSettings('markers'))
        self._Battle__initMemoryCriticalHandlers()
        MessengerDispatcher.g_instance.battleMessenger.start(self.proxy)
        g_guiResetters = g_guiResetters
        import game
        g_guiResetters.add(self._Battle__onRecreateDevice)
        g_repeatKeyHandlers = g_repeatKeyHandlers
        import game
        g_repeatKeyHandlers.add(self.component.handleKeyEvent)
        self._Battle__onRecreateDevice()
        self._Battle__setPlayerInfo(player.playerVehicleID)
        self._Battle__updatePlayers()
        self._Battle__populateData()
        self._Battle__minimap.start()
        self._Battle__radialMenu.setSettings(self._Battle__settingsInterface)
        self._Battle__radialMenu.populateUI(self.proxy)
        VoiceChatInterface.g_instance.onVoiceChatInitFailed += self.onVoiceChatInitFailed
        BigWorld.callback(1, self._Battle__setArenaTime)
        self.updateFlagsColor()
        self.movie.setFocussed()
        if self._Battle__arena.period == constants.ARENA_PERIOD.BATTLE:
            self.call('players_panel.setState', [
                AccountSettings.getSettings('players_panel')['state']])
        else:
            self.call('players_panel.setState', [
                'large'])
        self.call('sixthSenseIndicator.setDuration', [
            GUI_SETTINGS.sixthSenseDuration])
        g_tankActiveCamouflage[player.vehicleTypeDescriptor.type.compactDescr] = self._Battle__arena.arenaType.vehicleCamouflageKind
        if BattleReplay.g_replayCtrl.isPlaying:
            BattleReplay.g_replayCtrl.onBattleSwfLoaded()
        

    
    def beforeDelete(self):
        LOG_DEBUG('[Battle] beforeDelete')
        self._Battle__destroyMemoryCriticalHandlers()
        if self.colorManager:
            self.colorManager.dispossessUI()
        
        if VoiceChatInterface.g_instance:
            VoiceChatInterface.g_instance.dispossessUI()
        
        if self.component:
            g_repeatKeyHandlers = g_repeatKeyHandlers
            import game
            g_repeatKeyHandlers.discard(self.component.handleKeyEvent)
        
        AccountSettings.onSettingsChanging -= self._Battle__accs_onSettingsChanged
        self._Battle__teamBasesPanel.destroy()
        self._Battle__debugPanel.destroy()
        self._Battle__consumablesPanel.destroy()
        self._Battle__damagePanel.destroy()
        self._Battle__vMarkersManager.destroy()
        self._Battle__ingameHelp.destroy()
        self._Battle__vErrorsPanel.destroy()
        self._Battle__vMsgsPanel.destroy()
        self._Battle__pMsgsPanel.destroy()
        self._Battle__radialMenu.destroy()
        self._Battle__minimap.destroy()
        if self._Battle__soundManager:
            self._Battle__soundManager.dispossessUI()
            self._Battle__soundManager = None
        
        self._Battle__timerSound.stop()
        MessengerDispatcher.g_instance.battleMessenger.destroy()
        BattleWindow.beforeDelete(self)
        g_playerEvents.onBattleResultsReceived -= self._Battle__showFinalStatsResults
        usersManager = MessengerDispatcher.g_instance.users
        usersManager.onUsersRosterUpdate -= self._Battle__updatePlayers
        usersManager.onUsersRosterReceived -= self._Battle__updatePlayers
        if self._Battle__arena:
            self._Battle__arena.onPeriodChange -= self._Battle__onSetArenaTime
            self._Battle__arena.onNewVehicleListReceived -= self._Battle__updatePlayers
            self._Battle__arena.onNewStatisticsReceived -= self._Battle__updatePlayers
            self._Battle__arena.onVehicleAdded -= self._Battle__updatePlayers
            self._Battle__arena.onVehicleStatisticsUpdate -= self._Battle__updatePlayers
            self._Battle__arena.onVehicleKilled -= self._Battle__updatePlayers
            self._Battle__arena.onAvatarReady -= self._Battle__updatePlayers
            self._Battle__arena.onTeamKiller -= self._Battle__onTeamKiller
            self._Battle__arena.onVehicleUpdated -= self._Battle__updatePlayers
        
        self._Battle__arena = None
        VoiceChatInterface.g_instance.onVoiceChatInitFailed -= self.onVoiceChatInitFailed
        g_guiResetters = g_guiResetters
        import game
        g_guiResetters.discard(self._Battle__onRecreateDevice)
        self._Battle__settingsInterface.dispossessUI()
        self._Battle__settingsInterface = None

    
    def _Battle__screenshotNotifyCallback(self, path):
        self.vMsgsPanel.showMessage('SCREENSHOT_CREATED', {
            'path': path.encode('utf-8') })

    
    def onVoiceChatInitFailed(self):
        if GUI_SETTINGS.voiceChat:
            self.call('VoiceChat.initFailed', [])
        

    
    def clearCommands(self):
        pass

    
    def bindCommands(self):
        self._Battle__consumablesPanel.bindCommands()
        self._Battle__ingameHelp.buildCmdMapping()

    
    def updateFlagsColor(self):
        isColorBlind = AccountSettings.getSettings('isColorBlind')
        LOG_DEBUG('Update flags color scheme', isColorBlind)
        colorGreen = self.colorManager.getSubScheme('flag_team_green', isColorBlind = isColorBlind)['rgba']
        colorRed = self.colorManager.getSubScheme('flag_team_red', isColorBlind = isColorBlind)['rgba']
        if 1 == BigWorld.player().team:
            BigWorld.wg_setFlagColor(1, colorGreen / 255)
            BigWorld.wg_setFlagColor(2, colorRed / 255)
        else:
            BigWorld.wg_setFlagColor(2, colorGreen / 255)
            BigWorld.wg_setFlagColor(1, colorRed / 255)
        BigWorld.wg_setFlagEmblem(0, 'wg_emblem.dds', Math.Vector4(0, 0.1, 0.5, 0.9))
        BigWorld.wg_setFlagEmblem(1, 'wg_emblem.dds', Math.Vector4(0, 0.1, 0.5, 0.9))
        BigWorld.wg_setFlagEmblem(2, 'wg_emblem.dds', Math.Vector4(0, 0.1, 0.5, 0.9))

    
    def setPlayerSpeaking(self, accountDBID, flag):
        if not GUI_SETTINGS.voiceChat:
            return None
        self._speakPlayers[accountDBID] = flag
        self._Battle__callEx('setPlayerSpeaking', [
            accountDBID,
            flag])
        vID = g_battleContext.getVehIDByAccDBID(accountDBID)
        if vID > 0:
            self._Battle__vMarkersManager.showDynamic(vID, flag)
        

    
    def isPlayerSpeaking(self, accountDBID):
        if GUI_SETTINGS.voiceChat:
            return self._speakPlayers.get(accountDBID, False)
        return False

    
    def showPostmortemTips(self):
        if not g_battleContext.isPlayerObserver():
            self._Battle__callEx('showPostmortemTips', [
                1,
                5,
                1])
        

    
    def cursorVisibility(self, callbackId, visible, x = None, y = None, customCall = False, enableAiming = True):
        if visible:
            g_cursorDelegator.syncMousePosition(self, x, y, customCall)
        else:
            g_cursorDelegator.restoreMousePosition()
        if BigWorld.player() is not None and isinstance(BigWorld.player(), Avatar.PlayerAvatar):
            BigWorld.player().setForcedGuiControlMode(visible, False, enableAiming)
        

    
    def onExitBattle(self, arg):
        arena = getattr(BigWorld.player(), 'arena', None)
        LOG_DEBUG('onExitBattle', arena)
        if arena:
            BigWorld.player().leaveArena()
        

    
    def _Battle__setPlayerInfo(self, vID):
        (playerName, vTypeName) = ('', '')
        vInfo = self._Battle__arena.vehicles.get(vID)
        if vInfo is not None:
            playerName = g_battleContext.getFullPlayerName(vInfo, showVehShortName = False)
            vTypeName = vInfo['vehicleType'].type.userString
        
        self._Battle__callEx('setPlayerInfo', [
            playerName,
            vTypeName])

    
    def _Battle__populateData(self):
        AccountPrebattle = AccountPrebattle
        import account_helpers.AccountPrebattle
        getBattleSubTypeWinText = getBattleSubTypeWinText
        getArenaSubTypeName = getArenaSubTypeName
        isBaseExists = isBaseExists
        import gui.Scaleform.utils.functions
        arena = getattr(BigWorld.player(), 'arena', None)
        arenaData = [
            '',
            0,
            '',
            '',
            '']
        if arena:
            arenaData = [
                arena.arenaType.name]
            if not arena.extraData:
                pass
            descExtra = AccountPrebattle.getPrebattleDescription({ })
            arenaSubType = getArenaSubTypeName(BigWorld.player().arenaTypeID)
            if descExtra:
                arenaData.extend([
                    arena.guiType + 1,
                    descExtra])
            elif arena.guiType == constants.ARENA_GUI_TYPE.RANDOM:
                arenaData.extend([
                    arenaSubType,
                    '#arenas:type/%s/name' % arenaSubType])
            else:
                arenaData.extend([
                    arena.guiType + 1,
                    '#menu:loading/battleTypes/%d' % arena.guiType])
            if not arena.extraData:
                pass
            extraData = { }
            myTeam = BigWorld.player().team
            team1 = extraData.get('opponents', { }).get('%s' % myTeam, { }).get('name', '#menu:loading/team1')
            if myTeam == 1:
                pass
            1
            team2 = '2'('1', { }).get('name', '#menu:loading/team2')
            arenaData.extend([
                team1,
                team2])
            if isBaseExists(BigWorld.player().arenaTypeID, myTeam):
                pass
            1
            teamHasBase = 2
            winText = getBattleSubTypeWinText(BigWorld.player().arenaTypeID, teamHasBase)
            arenaData.append(winText)
        
        self._Battle__callEx('arenaData', arenaData)

    
    def _Battle__updatePlayers(self, *args):
        stat = {
            1: [],
            2: [] }
        squads = {
            1: { },
            2: { } }
        player = BigWorld.player()
        if player is None or type(player) != Avatar.PlayerAvatar:
            return None
        if self._Battle__arena is None:
            return None
        vehicles = self._Battle__arena.vehicles
        usersManager = MessengerDispatcher.g_instance.users
        for (vId, vData) in vehicles.items():
            if g_battleContext.isObserver(vId) and g_battleContext.isPlayerObserver():
                continue
            
            team = vData['team']
            if vData['name'] is not None:
                name = vData['name']
                user = usersManager.getUser(vData['accountDBID'], vData['name'])
            else:
                name = makeString('#ingame_gui:players_panel/unknown_name')
                user = UserWrapper()
            if vData['vehicleType'] is not None:
                vName = vData['vehicleType'].type.userString
                vShortName = vData['vehicleType'].type.shortUserString
                vIcon = _CONTOUR_ICONS_MASK % {
                    'unicName': vData['vehicleType'].type.name.replace(':', '-') }
                balanceWeight = vData['vehicleType'].balanceWeight
                vLevel = vData['vehicleType'].level
            else:
                vName = makeString('#ingame_gui:players_panel/unknown_vehicle')
                vShortName = makeString('#ingame_gui:players_panel/unknown_vehicle')
                vIcon = _CONTOUR_ICONS_MASK % {
                    'unicName': 'unknown' }
                balanceWeight = 0
                vLevel = -1
            isAlive = vData['isAlive']
            isAvatarReady = vData['isAvatarReady']
            vState = 0
            if isAlive:
                vState |= 1
            
            if isAvatarReady:
                vState |= 2
            
            if isAlive is None or isAvatarReady is None:
                vState = 4
            
            if vData['prebattleID'] > 0:
                if vData['prebattleID'] not in squads[team].keys():
                    squads[team][vData['prebattleID']] = 1
                else:
                    squads[team][vData['prebattleID']] += 1
            
            vStats = self._Battle__arena.statistics.get(vId, None)
            if vStats is None:
                pass
            1
            frags = vStats['frags']
            if vData['clanAbbrev']:
                userDisplayName = name + '[%s]' % vData['clanAbbrev']
            else:
                userDisplayName = name
            self._Battle__vehicles.update({
                vId: (userDisplayName, vName) })
            vehActions = VehicleActions.getBitMask(vData.get('events', { }))
            stat[team].append([
                name,
                vIcon,
                vShortName,
                vState,
                frags,
                vId,
                vData['prebattleID'],
                vData['clanAbbrev'],
                VoiceChatInterface.g_instance.isPlayerSpeaking(vData['accountDBID']),
                user.uid,
                user.roster,
                user.isMuted(),
                0,
                False,
                vData['isTeamKiller'],
                vLevel,
                vehActions,
                not isAlive,
                balanceWeight])
        
        squadsSorted = {
            1: sorted(squads[1].iteritems(), cmp = (lambda x, y: cmp(x[0], y[0]))),
            2: sorted(squads[2].iteritems(), cmp = (lambda x, y: cmp(x[0], y[0]))) }
        continue
        continue
        squadsFiltered = [
            2]
        teamFrags = [
            0,
            0]
        for team in (1, 2):
            value = [
                'team%d' % team,
                -1,
                -1,
                BigWorld.player().denunciationsLeft,
                AccountSettings.getSettings('isColorBlind'),
                None]
            data = sorted(stat[team], cmp = _playerComparator)
            for item in data:
                teamFrags[team - 1] += item[4]
                if item[6] in squadsFiltered[team]:
                    pass
                1
                sNumber = 0
                item[6] = sNumber
                if item[5] == player.playerVehicleID and item[6] > 0:
                    value[2] = item[6]
                
                value.extend(item[:-4])
                if team != player.team:
                    value[-1] = False
                
                value.append(self._Battle__cameraVehicleID == item[5])
                if AccountSettings.getSettings('players_panel')['showLevels']:
                    pass
                1
                item[15](0)
                value.append(item[16])
                value.append(item[5])
            
            if team == player.team:
                value[1] = player.playerVehicleID
            
            self._Battle__callEx('setTeam', value)
        
        playerTeam = player.team - 1
        enemyTeam = 1 - playerTeam
        self._Battle__fragCorrelation.updateFrags(teamFrags[playerTeam], teamFrags[enemyTeam])

    
    def _Battle__showFinalStatsResults(self, isActiveVehicle, results):
        if isActiveVehicle:
            if GUI_SETTINGS.battleStatsInHangar:
                if self._Battle__arena:
                    g_battleContext.lastArenaUniqueID = self._Battle__arena.arenaUniqueID
                
                self.onExitBattle(None)
            elif not self._Battle__vehicles:
                self._Battle__updatePlayers()
            
            if results['killerID']:
                killer = makeString('#ingame_gui:statistics/final/lifeInfo/dead', '%s (%s)' % self._Battle__vehicles.get(results['killerID'], ('n/a', 'n/a')))
            else:
                killer = makeString('#ingame_gui:statistics/final/lifeInfo/alive')
            if int(results['factors']['dailyXPFactor10'] / 10) > 1:
                pass
            isMultipliedXP = results['xp'] > 0
            if isMultipliedXP:
                pass
            1
            stats = [
                results['credits'],
                results['repair'],
                isMultipliedXP,
                i18n.makeString('#ingame_gui:statistics/final/stats/multipliedExp') % int(results['factors']['dailyXPFactor10'] / 10),
                i18n.makeString('#ingame_gui:statistics/final/stats/experience'),
                self._Battle__vehicles.get(BigWorld.player().playerVehicleID, ('n/a', 'n/a'))[0],
                killer]
            results['damaged'] = list(set(results['damaged']).difference(set(results['killed'])))
            for key in ('killed', 'damaged', 'spotted'):
                lt = set()
                for id in results[key]:
                    lt.add('%s (%s)' % self._Battle__vehicles.get(id, ('n/a', 'n/a')))
                
                stats.append(len(lt))
                stats.extend(lt)
            
            hl = set()
            if results.has_key('achieveIndices'):
                for (i, heroId) in enumerate(results['achieveIndices']):
                    herolist = [
                        makeString(heroesTexts[heroesNames[heroId]])]
                    if results.has_key('heroVehicleIDs') and len(results['heroVehicleIDs']) > i:
                        if self._Battle__arena.vehicles.get(results['heroVehicleIDs'][i], False):
                            if not self._Battle__arena.vehicles[results['heroVehicleIDs'][i]]['isAlive']:
                                herolist[0] += ' ' + makeString('#ingame_gui:statistics/final/personal/postmortem')
                            
                        
                        herolist.extend(self._Battle__vehicles.get(results['heroVehicleIDs'][i], ('n/a', 'n/a')))
                        hl.add('%s - %s (%s)' % tuple(herolist))
                        continue
                    results['xp']
                
            
            stats.append(len(hl))
            stats.extend(hl)
            for key in ('shots', 'hits', 'shotsReceived'):
                stats.append(makeString('#ingame_gui:statistics/final/personal/' + key, results[key]))
            
            for key in ('capturePoints', 'droppedCapturePoints'):
                stats.append(makeString('#ingame_gui:statistics/final/personal/' + key, min(results[key], 100)))
            
            self._Battle__callEx('showFinalStatistic', stats)
        

    
    def _Battle__showFinalStats(self, winnerTeam, reason):
        if hasattr(BigWorld.player(), 'team'):
            if winnerTeam == 0:
                pass
            1
            if winnerTeam == BigWorld.player().team:
                pass
            1
            status = 'lose'
            status = makeString('#menu:finalStatistic/commonStats/resultlabel/%s' % status)
            self._Battle__callEx('showStatus', [
                status])
        

    
    def _Battle__onSetArenaTime(self, *args):
        if self._Battle__timerCallBackId is not None:
            BigWorld.cancelCallback(self._Battle__timerCallBackId)
        
        self._Battle__setArenaTime()

    
    def _Battle__setArenaTime(self):
        self._Battle__timerCallBackId = None
        if self._Battle__arena is None:
            return None
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying:
            period = replayCtrl.getArenaPeriod()
            arenaLength = int(replayCtrl.getArenaLength())
            if period == 0:
                self._Battle__timerCallBackId = BigWorld.callback(1, self._Battle__setArenaTime)
                return None
        else:
            period = self._Battle__arena.period
            arenaLength = int(self._Battle__arena.periodEndTime - BigWorld.serverTime())
            if arenaLength > 0:
                pass
            1
            arenaLength = 0
            if replayCtrl.isRecording:
                replayCtrl.setArenaPeriod(period)
                replayCtrl.setArenaLength(arenaLength)
            
        self._Battle__callEx('timerBar.setTotalTime', [
            arenaLength])
        if period == constants.ARENA_PERIOD.WAITING:
            self._Battle__callEx('timerBig.setTimer', [
                makeString('#ingame_gui:timer/waiting')])
            self._Battle__isTimerVisible = True
        elif period == constants.ARENA_PERIOD.PREBATTLE:
            self._Battle__callEx('timerBig.setTimer', [
                makeString('#ingame_gui:timer/starting'),
                arenaLength])
            self._Battle__isTimerVisible = True
            if not (self._Battle__timerSound.isPlaying) and not (replayCtrl.isPlaying):
                self._Battle__timerSound.play()
            
        elif period == constants.ARENA_PERIOD.BATTLE and self._Battle__isTimerVisible:
            self._Battle__isTimerVisible = False
            self._Battle__timerSound.stop()
            self._Battle__callEx('timerBig.setTimer', [
                makeString('#ingame_gui:timer/started')])
            self._Battle__callEx('timerBig.hide')
            if not self._Battle__playersPanelStateChanged:
                self.call('players_panel.setState', [
                    AccountSettings.getSettings('players_panel')['state']])
            
        elif period == constants.ARENA_PERIOD.AFTERBATTLE:
            self._Battle__showFinalStats(*self._Battle__arena.periodAdditionalInfo)
            self.consumablesPanel._isOptDeviceEnabled = False
        
        if arenaLength > 1 or replayCtrl.isPlaying:
            if not replayCtrl.isPlaying:
                pass
            1
            self._Battle__timerCallBackId = 1(0, self._Battle__setArenaTime)
        

    
    def _Battle__onTeamKiller(self, vID):
        self._Battle__updatePlayers(vID)
        self._Battle__vMarkersManager.setTeamKiller(vID)

    
    def _Battle__onRecreateDevice(self):
        self.call('Stage.Update', list(GUI.screenResolution()))

    
    def _Battle__callEx(self, funcName, args = None):
        self.call('battle.' + funcName, args)

    
    def _Battle__initMemoryCriticalHandlers(self):
        for message in g_critMemHandler.messages:
            self._Battle__onMemoryCritical(message)
        
        g_critMemHandler.onMemCrit += self._Battle__onMemoryCritical

    
    def _Battle__destroyMemoryCriticalHandlers(self):
        g_critMemHandler.onMemCrit -= self._Battle__onMemoryCritical

    
    def _Battle__onMemoryCritical(self, message):
        self._Battle__vMsgsPanel.showMessage(message[1])

    
    def _Battle__accs_onSettingsChanged(self, name):
        LOG_DEBUG('__accs_onSettingsChanging', name)
        if name == 'isColorBlind':
            self.colorManager.update()
            isColorBlind = AccountSettings.getSettings('isColorBlind')
            self._Battle__vErrorsPanel.defineColorFlags(isColorBlind = isColorBlind)
            self._Battle__vMsgsPanel.defineColorFlags(isColorBlind = isColorBlind)
            self._Battle__pMsgsPanel.defineColorFlags(isColorBlind = isColorBlind)
            self.updateFlagsColor()
            self._Battle__vMarkersManager.updateMarkers()
            self._Battle__minimap.updateEntries()
            MessengerDispatcher.g_instance.battleMessenger.updateColors(isColorBlind = isColorBlind)
        
        if name == 'markers':
            self.vMarkersManager.setMarkerSettings(AccountSettings.getSettings('markers'))
            self._Battle__vMarkersManager.updateMarkerSettings()
        
        self._Battle__updatePlayers()

    
    def _Battle__getEntityUserString(self, entityName):
        player = BigWorld.player()
        if player and player.isVehicleAlive:
            extra = player.vehicleTypeDescriptor.extrasDict.get(entityName + 'Health')
            if extra is None:
                return entityName
            return extra.deviceUserString

    
    def _showTankmanIsSafeMessage(self, entityName):
        if not self._Battle__consumablesPanel.hasMedkit():
            return None
        tankman = self._Battle__getEntityUserString(entityName)
        if tankman:
            self._Battle__vErrorsPanel.showMessage('medkitTankmanIsSafe', {
                'entity': tankman })
        

    
    def _showDeviceIsNotDamagedMessage(self, entityName):
        if not self._Battle__consumablesPanel.hasRepairkit():
            return None
        if entityName == 'chassis':
            device = i18n.makeString('#ingame_gui:devices/chassis')
        else:
            device = self._Battle__getEntityUserString(entityName)
        if device:
            self._Battle__vErrorsPanel.showMessage('repairkitDeviceIsNotDamaged', {
                'entity': device })
        



class TeamBasesPanel(object):
    _TeamBasesPanel__settings = {
        0: {
            'weight': 2,
            'color': 'red',
            'capturing': i18n.makeString('#ingame_gui:player_messages/ally_base_captured_by_notification'),
            'captured': i18n.makeString('#ingame_gui:player_messages/ally_base_captured_notification') },
        3: {
            'weight': 1,
            'color': 'green',
            'capturing': i18n.makeString('#ingame_gui:player_messages/enemy_base_captured_by_notification'),
            'captured': i18n.makeString('#ingame_gui:player_messages/enemy_base_captured_notification') },
        'controlPoint': {
            'weight': 3,
            'color': {
                0: 'red',
                3: 'green' },
            'capturing': i18n.makeString('#ingame_gui:player_messages/base_captured_by_notification'),
            'captured': i18n.makeString('#ingame_gui:player_messages/base_captured_notification') } }
    
    def __init__(self, parentUI):
        self._TeamBasesPanel__ui = parentUI
        self._TeamBasesPanel__captureSounds = { }
        self._TeamBasesPanel__baseIds = set()

    
    def start(self):
        LOG_DEBUG('TeamBasesPanel.start')
        arena = BigWorld.player().arena
        arena.onTeamBasePointsUpdate += self._TeamBasesPanel__onTeamBasePointsUpdate
        arena.onTeamBaseCaptured += self._TeamBasesPanel__onTeamBaseCaptured
        arena.onPeriodChange += self._TeamBasesPanel__onPeriodChange

    
    def destroy(self):
        LOG_DEBUG('TeamBasesPanel.destroy')
        arena = getattr(BigWorld.player(), 'arena', None)
        if arena is not None:
            arena.onTeamBasePointsUpdate -= self._TeamBasesPanel__onTeamBasePointsUpdate
            arena.onTeamBaseCaptured -= self._TeamBasesPanel__onTeamBaseCaptured
            arena.onPeriodChange -= self._TeamBasesPanel__onPeriodChange
        
        self._TeamBasesPanel__stopCaptureSound()

    
    def _getID(self, team, baseID):
        if baseID is None:
            baseID = 0
        
        return (int(baseID) << 2) + team

    
    def _TeamBasesPanel__onTeamBasePointsUpdate(self, team, baseID, points, capturingStopped):
        if team not in (1, 2):
            return None
        id = self._getID(team, baseID)
        if not points:
            if id in self._TeamBasesPanel__baseIds:
                self._TeamBasesPanel__baseIds.remove(id)
            
            self._TeamBasesPanel__callFlash('remove', [
                id])
            self._TeamBasesPanel__stopCaptureSound(team)
        elif id in self._TeamBasesPanel__baseIds:
            if capturingStopped:
                pass
            1
            'stop'('updatePoints', [
                id,
                points])
        else:
            self._TeamBasesPanel__baseIds.add(id)
            if isControlPointExists(BigWorld.player().arenaTypeID):
                settings = self._TeamBasesPanel__settings.get('controlPoint', { })
                color = settings.get('color', { }).get(team ^ BigWorld.player().team, 'green')
            else:
                settings = self._TeamBasesPanel__settings.get(team ^ BigWorld.player().team, { })
                color = settings.get('color', 'green')
            self._TeamBasesPanel__callFlash('add', [
                id,
                settings.get('weight', 0),
                color,
                settings.get('capturing', '') % getBattleSubTypeBaseNumder(BigWorld.player().arenaTypeID, team, baseID),
                points])
            if capturingStopped:
                self._TeamBasesPanel__callFlash('stop', [
                    id,
                    points])
            
        if not capturingStopped:
            self._TeamBasesPanel__playCaptureSound(team)
        else:
            self._TeamBasesPanel__stopCaptureSound(team)

    
    def _TeamBasesPanel__onTeamBaseCaptured(self, team, baseID):
        if team not in (1, 2):
            return None
        id = self._getID(team, baseID)
        if isControlPointExists(BigWorld.player().arenaTypeID):
            settings = self._TeamBasesPanel__settings.get('controlPoint', { })
            color = settings.get('color', { }).get(team ^ BigWorld.player().team, 'green')
        else:
            settings = self._TeamBasesPanel__settings.get(team ^ BigWorld.player().team, { })
            color = settings.get('color', 'green')
        if id in self._TeamBasesPanel__baseIds:
            self._TeamBasesPanel__callFlash('setCaptured', [
                id,
                settings.get('captured', '') % getBattleSubTypeBaseNumder(BigWorld.player().arenaTypeID, team, baseID)])
        else:
            self._TeamBasesPanel__baseIds.add(id)
            self._TeamBasesPanel__callFlash('add', [
                id,
                color,
                settings.get('weight', 0),
                settings.get('captured', '') % getBattleSubTypeBaseNumder(BigWorld.player().arenaTypeID, team, baseID),
                100])
        self._TeamBasesPanel__stopCaptureSound(team)

    
    def _TeamBasesPanel__onPeriodChange(self, period, *args):
        if period != constants.ARENA_PERIOD.AFTERBATTLE:
            return None
        self._TeamBasesPanel__callFlash('clear', [])
        self._TeamBasesPanel__stopCaptureSound()

    
    def _TeamBasesPanel__callFlash(self, funcName, args):
        self._TeamBasesPanel__ui.call('battle.teamBasesPanel.{0:>s}'.format(funcName), args)

    
    def _TeamBasesPanel__playCaptureSound(self, team):
        arena = getattr(BigWorld.player(), 'arena', None)
        if arena is not None and arena.period == constants.ARENA_PERIOD.AFTERBATTLE:
            return None
        snd = self._TeamBasesPanel__captureSounds.get(team)
        if snd is None:
            
            try:
                if team == BigWorld.player().team:
                    pass
                1
                isAllyTeam = False
                if isAllyTeam:
                    snd = FMOD.getSound(_BASE_CAPTURE_SOUND_NAME_ALLY)
                    self._TeamBasesPanel__captureSounds[team] = snd
            except Exception:
                arena.period == constants.ARENA_PERIOD.AFTERBATTLE
                LOG_CURRENT_EXCEPTION()
            


    
    def _TeamBasesPanel__stopCaptureSound(self, team = None):
        if team is None:
            for t in self._TeamBasesPanel__captureSounds.keys():
                self._TeamBasesPanel__stopCaptureSound(t)
            
        else:
            snd = self._TeamBasesPanel__captureSounds.get(team)
            if snd is not None:
                
                try:
                    snd.stop()
                except Exception:
                    LOG_CURRENT_EXCEPTION()

                del self._TeamBasesPanel__captureSounds[team]
            



class VehicleDamageInfoPanel(object):
    
    def __init__(self, parent):
        self.parent = parent
        self.isShown = False

    
    def show(self, vehicleID, damagedExtras = [], destroyedExtras = []):
        if vehicleID not in BigWorld.player().arena.vehicles or not BigWorld.player().arena.vehicles[vehicleID].has_key('vehicleType'):
            return None
        extras = BigWorld.player().arena.vehicles[vehicleID]['vehicleType'].extras
        isFire = False
        itemsList = []
        for (i, id) in enumerate(damagedExtras):
            if extras[id].name == 'fire':
                isFire = True
                continue
            
            itemsList.append({
                'name': extras[id].name,
                'userName': extras[id].deviceUserString,
                'state': 'damaged' })
        
        for (i, id) in enumerate(destroyedExtras):
            itemsList.append({
                'name': extras[id].name,
                'userName': extras[id].deviceUserString,
                'state': 'destroyed' })
        
        self.parent.movie.showDamageInfoPanel(vehicleID, itemsList, isFire)
        self.isShown = True

    
    def hide(self):
        if not self.isShown:
            return None
        self.parent.movie.hideDamageInfoPanel()
        self.isShown = False



class FragCorrelationPanel(object):
    
    def __init__(self, parentUI):
        self._FragCorrelationPanel__ui = parentUI
        _alliedTeamName = i18n.makeString('#ingame_gui:player_messages/allied_team_name')
        _enemyTeamName = i18n.makeString('#ingame_gui:player_messages/enemy_team_name')
        self._FragCorrelationPanel__callFlash('setTeamNames', [
            _alliedTeamName,
            _enemyTeamName])

    
    def updateFrags(self, alliedFrags, enemyFrags):
        self._FragCorrelationPanel__callFlash('updateFrags', [
            alliedFrags,
            enemyFrags])

    
    def _FragCorrelationPanel__callFlash(self, funcName, args):
        self._FragCorrelationPanel__ui.call('battle.fragCorrelationBar.' + funcName, args)



class DebugPanel(object):
    _DebugPanel__UPDATE_INTERVAL = 0.01
    
    def __init__(self, parentUI):
        self._DebugPanel__ui = parentUI
        self._DebugPanel__timeInterval = None

    
    def start(self):
        self._DebugPanel__timeInterval = _TimeInterval(self._DebugPanel__UPDATE_INTERVAL, '_DebugPanel__update', weakref.proxy(self))
        self._DebugPanel__timeInterval.start()
        self._DebugPanel__update()

    
    def destroy(self):
        self._DebugPanel__timeInterval.stop()

    
    def _DebugPanel__update(self):
        player = BigWorld.player()
        if player is None or not hasattr(player, 'playerVehicleID'):
            return None
        fps = 0
        recordedFps = -1
        ping = 0
        isLaggingNow = False
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.fps > 0:
            fps = BigWorld.getFPS()[1]
            recordedFps = replayCtrl.fps
            ping = replayCtrl.ping
            isLaggingNow = replayCtrl.isLaggingNow
        else:
            isLaggingNow = False
            vehicle = BigWorld.entity(player.playerVehicleID)
            if vehicle is not None and isinstance(vehicle.filter, BigWorld.WGVehicleFilter):
                isLaggingNow = vehicle.filter.isLaggingNow
            
            ping = min(BigWorld.LatencyInfo().value[3] * 1000, 999)
            if ping < 999:
                ping = max(1, ping - 500 * constants.SERVER_TICK_LENGTH)
            
            fps = BigWorld.getFPS()[1]
            if replayCtrl.isRecording:
                replayCtrl.setFpsPingLag(fps, ping, isLaggingNow)
            
        self._DebugPanel__ui.call('battle.debugBar.updateInfo', [
            int(fps),
            int(ping),
            isLaggingNow,
            int(recordedFps)])



class ConsumablesPanel(object):
    _ConsumablesPanel__supportedTags = set(('medkit', 'repairkit', 'stimulator', 'trigger', 'fuel', 'extinguisher'))
    _ConsumablesPanel__orderSets = {
        'medkit': TANKMEN_ROLES_ORDER_DICT['enum'],
        'repairkit': ('engine', 'ammoBay', 'gun', 'turretRotator', 'chassis', 'surveyingDevice', 'radio', 'fuelTank') }
    _ConsumablesPanel__mergedEntities = {
        'chassis': ('leftTrack', 'rightTrack') }
    _SHELL_ICON_PATH = '../maps/icons/ammopanel/ammo/%s'
    _NO_SHELL_ICON_PATH = '../maps/icons/ammopanel/ammo/NO_%s'
    _COMMAND_MAPPING_KEY_MASK = 'CMD_AMMO_CHOICE_%d'
    _START_EQUIPMENT_SLOT_IDX = 3
    
    def __init__(self, parentUI):
        self._ConsumablesPanel__ui = parentUI
        self._ConsumablesPanel__ui.addExternalCallbacks({
            'battle.consumablesPanel.onClickToSlot': self.onClickToSlot,
            'battle.consumablesPanel.onCollapseEquipment': self.onCollapseEquipment })
        self._ConsumablesPanel__shellKCMap = { }
        self._ConsumablesPanel__equipmentKCMap = { }
        self._ConsumablesPanel__equipmentTagsByIdx = { }
        self._ConsumablesPanel__entitiesKCMap = { }
        self._ConsumablesPanel__expandEquipmentIdx = None
        self._ConsumablesPanel__processedInfo = None
        self._ConsumablesPanel__emptyEquipmentSlotCount = 0
        self._isOptDeviceEnabled = False
        self._ConsumablesPanel__disableTurretRotator = not vehicleHasTurretRotator(BigWorld.player().vehicleTypeDescriptor)

    
    def start(self):
        self._isOptDeviceEnabled = True
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.replayContainsGunReloads:
            self._ConsumablesPanel__cbIdSetCooldown = BigWorld.callback(0, self.setCooldownFromReplay)
        else:
            self._ConsumablesPanel__cbIdSetCooldown = None

    
    def destroy(self):
        self._isOptDeviceEnabled = False
        if self._ConsumablesPanel__cbIdSetCooldown is not None:
            BigWorld.cancelCallback(self._ConsumablesPanel__cbIdSetCooldown)
            self._ConsumablesPanel__cbIdSetCooldown = None
        
        self._ConsumablesPanel__ui = None

    
    def setItemQuantityInSlot(self, idx, quantity):
        if self._ConsumablesPanel__equipmentTagsByIdx.has_key(idx):
            self._ConsumablesPanel__equipmentTagsByIdx[idx][1] = quantity
        
        self._ConsumablesPanel__callFlash('setItemQuantityInSlot', [
            idx,
            quantity])

    
    def setCoolDownTime(self, idx, timeRemaining):
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and idx <= 2 and replayCtrl.replayContainsGunReloads:
            return None
        if replayCtrl.isRecording and idx is not None:
            replayCtrl.setConsumableSlotCooldown(idx, timeRemaining, True)
        
        self._ConsumablesPanel__callFlash('setCoolDownTime', [
            idx,
            timeRemaining])

    
    def setCoolDownPosAsPercent(self, idx, percent):
        self._ConsumablesPanel__callFlash('setCoolDownPosAsPercent', [
            idx,
            percent])

    
    def setCooldownFromReplay(self):
        player = BigWorld.player()
        if isinstance(player, Avatar.PlayerAvatar):
            for idx in xrange(0, 3):
                self.setCoolDownPosAsPercent(idx, 100 * BattleReplay.g_replayCtrl.getConsumableSlotCooldownAmount(idx))
            
        
        self._ConsumablesPanel__cbIdSetCooldown = BigWorld.callback(0, self.setCooldownFromReplay)

    
    def setDisabled(self, currentShellIdx):
        self.setCoolDownTime(currentShellIdx, 0)
        self.setCurrentShell(-1)
        self.setNextShell(-1)
        if self._ConsumablesPanel__expandEquipmentIdx is not None:
            self.collapseEquipmentSlot(self._ConsumablesPanel__expandEquipmentIdx)
        

    
    def _ConsumablesPanel__getKey(self, idx):
        if -1 < idx:
            pass
        idx < 10
        if not 1:
            raise AssertionError
        if idx < 9:
            pass
        1
        cmdMappingKey = 0
        keyCode = CommandMapping.g_instance.get(cmdMappingKey)
        keyChr = ''
        if keyCode is not None and keyCode != 0:
            keyChr = BigWorld.keyToString(keyCode)
        
        return (keyCode, keyChr)

    
    def bindCommands(self):
        shellKCMap = { }
        for idx in self._ConsumablesPanel__shellKCMap.values():
            (keyCode, keyChr) = self._ConsumablesPanel__getKey(idx)
            shellKCMap[keyCode] = idx
            self._ConsumablesPanel__callFlash('setKeyToSlot', [
                idx,
                keyCode,
                keyChr])
        
        self._ConsumablesPanel__shellKCMap = shellKCMap
        equipmentKCMap = { }
        for idx in self._ConsumablesPanel__equipmentKCMap.values():
            (keyCode, keyChr) = self._ConsumablesPanel__getKey(idx)
            equipmentKCMap[keyCode] = idx
            self._ConsumablesPanel__callFlash('setKeyToSlot', [
                idx,
                keyCode,
                keyChr])
        
        self._ConsumablesPanel__equipmentKCMap = equipmentKCMap

    
    def setShellQuantityInSlot(self, idx, quantity, quantityInClip):
        if self._ConsumablesPanel__equipmentTagsByIdx.has_key(idx):
            self._ConsumablesPanel__equipmentTagsByIdx[idx][1] = quantity
        
        self._ConsumablesPanel__callFlash('setShellQuantityInSlot', [
            idx,
            quantity,
            quantityInClip])

    
    def addShellSlot(self, idx, quantity, quantityInClip, clipCapacity, shellDescr, piercingPower):
        kind = shellDescr['kind']
        icon = shellDescr['icon'][0]
        toolTip = i18n.convert(i18n.makeString('#ingame_gui:shells_kinds/{0:>s}'.format(kind), caliber = shellDescr['caliber'], userString = shellDescr['userString'], damage = str(int(shellDescr['damage'][0])), piercingPower = str(int(piercingPower[0]))))
        shellIconPath = self._SHELL_ICON_PATH % icon
        noShellIconPath = self._NO_SHELL_ICON_PATH % icon
        (keyCode, keyChr) = self._ConsumablesPanel__getKey(idx)
        self._ConsumablesPanel__shellKCMap[keyCode] = idx
        self._ConsumablesPanel__callFlash('addShellSlot', [
            idx,
            keyCode,
            keyChr,
            quantity,
            quantityInClip,
            clipCapacity,
            shellIconPath,
            noShellIconPath,
            toolTip])

    
    def setCurrentShell(self, idx):
        self._ConsumablesPanel__callFlash('setCurrentShell', [
            idx])

    
    def setNextShell(self, idx):
        self._ConsumablesPanel__callFlash('setNextShell', [
            idx])

    
    def hasMedkit(self):
        for (tagName, quantity) in self._ConsumablesPanel__equipmentTagsByIdx.values():
            if tagName == 'medkit':
                return quantity > 0
        
        return False

    
    def hasRepairkit(self):
        for (tagName, quantity) in self._ConsumablesPanel__equipmentTagsByIdx.values():
            if tagName == 'repairkit':
                return quantity > 0
        
        return False

    
    def checkEquipmentSlotIdx(self, idx):
        return max(self._START_EQUIPMENT_SLOT_IDX, idx)

    
    def addEquipmentSlot(self, idx, quantity, equipmentDescr):
        tags = self._ConsumablesPanel__supportedTags & equipmentDescr.tags
        tagName = None
        if len(tags) == 1:
            tagName = tags.pop()
        
        iconPath = equipmentDescr.icon[0]
        toolTip = '{0:>s}\n{1:>s}'.format(equipmentDescr.userString, equipmentDescr.description)
        (keyCode, keyChr) = (None, None)
        if tagName:
            (keyCode, keyChr) = self._ConsumablesPanel__getKey(idx)
            self._ConsumablesPanel__equipmentKCMap[keyCode] = idx
            self._ConsumablesPanel__equipmentTagsByIdx[idx] = [
                tagName,
                quantity]
        
        self._ConsumablesPanel__callFlash('addEquipmentSlot', [
            idx,
            keyCode,
            keyChr,
            tagName,
            quantity,
            iconPath,
            toolTip])

    
    def addEmptyEquipmentSlot(self, idx):
        self._ConsumablesPanel__emptyEquipmentSlotCount += 1
        toolTip = i18n.makeString('#ingame_gui:consumables_panel/equipment/tooltip/empty')
        self._ConsumablesPanel__callFlash('addEquipmentSlot', [
            idx,
            None,
            None,
            None,
            0,
            None,
            toolTip])
        if self._ConsumablesPanel__emptyEquipmentSlotCount == NUM_EQUIPMENT_SLOTS:
            self._ConsumablesPanel__callFlash('showEquipmentSlots', [
                False])
        

    
    def expandEquipmentSlot(self, idx, tagName, entityStates):
        orderSet = self._ConsumablesPanel__orderSets.get(tagName)
        if orderSet is None:
            if constants.IS_DEVELOPMENT:
                LOG_ERROR('Order set not determine for tag %s' % tagName)
            
            return None
        self._ConsumablesPanel__expandEquipmentIdx = idx
        self._ConsumablesPanel__processedInfo = (tagName, entityStates)
        args = self._ConsumablesPanel__buildEntitiesInfoList(idx, tagName, entityStates, orderSet)
        self._ConsumablesPanel__callFlash('expandEquipmentSlot', args)

    
    def updateExpandedEquipmentSlot(self, entityName, entityState):
        if self._ConsumablesPanel__expandEquipmentIdx and self._ConsumablesPanel__processedInfo:
            (tagName, entityStates) = self._ConsumablesPanel__processedInfo
            if entityStates.has_key(entityName):
                if entityState != 'repaired':
                    pass
                1
                entityStates[entityName] = 'critical'
                self._ConsumablesPanel__processedInfo = (tagName, entityStates)
                idx = self._ConsumablesPanel__expandEquipmentIdx
                orderSet = self._ConsumablesPanel__orderSets[tagName]
                args = self._ConsumablesPanel__buildEntitiesInfoList(idx, tagName, entityStates, orderSet)
                self._ConsumablesPanel__callFlash('updateExpandedEquipmentSlot', args)
            
        

    
    def collapseEquipmentSlot(self, idx):
        self._ConsumablesPanel__callFlash('collapseEquipmentSlot', [
            idx])

    
    def _ConsumablesPanel__buildEntitiesInfoList(self, idx, tagName, entityStates, orderSet):
        args = [
            idx,
            tagName]
        for (entityIdx, entityName) in enumerate(orderSet):
            entityState = None
            disabled = True
            (keyCode, keyChr) = self._ConsumablesPanel__getKey(entityIdx)
            if self._ConsumablesPanel__mergedEntities.has_key(entityName):
                realName = None
                for name in self._ConsumablesPanel__mergedEntities[entityName]:
                    state = entityStates.get(name, None)
                    disabled &= (not entityStates.has_key(name))
                    if realName is None and state == 'critical':
                        realName = name
                        entityState = 'critical'
                        continue
                    if state == 'destroyed':
                        realName = name
                        entityState = 'destroyed'
                        break
                        continue
                
                if realName is not None:
                    self._ConsumablesPanel__entitiesKCMap[keyCode] = (realName, False)
                else:
                    self._ConsumablesPanel__entitiesKCMap[keyCode] = (entityName, True)
            elif entityStates.has_key(entityName):
                entityState = entityStates[entityName]
                if entityName == 'turretRotator':
                    pass
                disabled = self._ConsumablesPanel__disableTurretRotator
                if not disabled:
                    self._ConsumablesPanel__entitiesKCMap[keyCode] = (entityName, entityState not in ('destroyed', 'critical'))
                
            
            args.extend([
                keyCode,
                keyChr,
                entityName,
                entityState,
                disabled])
        
        return args

    
    def _ConsumablesPanel__removeExpandEquipment(self, idx):
        if idx == self._ConsumablesPanel__expandEquipmentIdx:
            self._ConsumablesPanel__expandEquipmentIdx = None
            self._ConsumablesPanel__processedInfo = None
            self._ConsumablesPanel__entitiesKCMap.clear()
        

    
    def addOptionalDevice(self, idx, deviceDescr):
        iconPath = deviceDescr.icon[0]
        toolTip = '{0:>s}\n{1:>s}'.format(deviceDescr.userString, deviceDescr.description)
        self._ConsumablesPanel__callFlash('addOptionalDeviceSlot', [
            idx,
            iconPath,
            toolTip])

    
    def setOptionalDeviceState(self, idx, isOn):
        if self._isOptDeviceEnabled:
            if isOn:
                pass
            1
            idx(-1, 0)
        

    
    def handleKey(self, key):
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying:
            return None
        if self._ConsumablesPanel__expandEquipmentIdx is not None:
            if key in self._ConsumablesPanel__entitiesKCMap.keys():
                slotIdx = self._ConsumablesPanel__expandEquipmentIdx
                (devName, isNormal) = self._ConsumablesPanel__entitiesKCMap[key]
                if not isNormal:
                    self.collapseEquipmentSlot(slotIdx)
                    BigWorld.player().onEquipmentButtonPressed(slotIdx, deviceName = devName)
                elif self._ConsumablesPanel__processedInfo is None:
                    LOG_ERROR("Can't determine equipment tag", slotIdx, devName)
                    return None
                (tagName, _) = self._ConsumablesPanel__processedInfo
                if tagName == 'medkit':
                    self._ConsumablesPanel__ui._showTankmanIsSafeMessage(devName)
                elif tagName == 'repairkit':
                    self._ConsumablesPanel__ui._showDeviceIsNotDamagedMessage(devName)
                else:
                    LOG_ERROR("Can't determine message for tag", tagName)
            
            return None
        if key in self._ConsumablesPanel__shellKCMap.keys():
            BigWorld.player().onAmmoButtonPressed(self._ConsumablesPanel__shellKCMap[key])
        elif key in self._ConsumablesPanel__equipmentKCMap.keys():
            BigWorld.player().onEquipmentButtonPressed(self._ConsumablesPanel__equipmentKCMap[key])
        

    
    def onClickToSlot(self, _, keyCode):
        self.handleKey(int(keyCode))

    
    def onCollapseEquipment(self, _, idx):
        self._ConsumablesPanel__removeExpandEquipment(int(idx))

    
    def _ConsumablesPanel__callFlash(self, funcName, args = None):
        self._ConsumablesPanel__ui.call('battle.consumablesPanel.%s' % funcName, args)



class DamagePanel:
    _WAITING_INTERVAL = 0.05
    _UPDATING_INTERVAL = 0.03
    
    def __init__(self, parentUI):
        self._DamagePanel__ui = parentUI
        self._DamagePanel__hasYawLimits = False
        self._DamagePanel__vID = 0
        self._DamagePanel__speed = 0
        self._DamagePanel__health = 0
        self._DamagePanel__waitingTI = _TimeInterval(self._WAITING_INTERVAL, '_waiting', weakref.proxy(self))
        self._DamagePanel__updateTI = _TimeInterval(self._UPDATING_INTERVAL, '_updateSelf', weakref.proxy(self))
        self._DamagePanel__tankIndicator = _TankIndicatorCtrl(self._DamagePanel__ui)
        self._DamagePanel__ui.addExternalCallbacks({
            'battle.damagePanel.onClickToDeviceIcon': self._DamagePanel__onClickToDeviceIcon,
            'battle.damagePanel.onClickToTankmenIcon': self._DamagePanel__onClickToTankmenIcon })

    
    def start(self):
        self._DamagePanel__tankIndicator.start()
        self._DamagePanel__vID = BigWorld.player().playerVehicleID
        self._DamagePanel__waitingTI.start()

    
    def destroy(self):
        self._DamagePanel__waitingTI.stop()
        self._DamagePanel__waitingTI = None
        self._DamagePanel__updateTI.stop()
        self._DamagePanel__updateTI = None
        self._DamagePanel__tankIndicator.destroy()
        self._DamagePanel__tankIndicator = None
        self._DamagePanel__hasYawLimits = False
        self._DamagePanel__ui = None

    
    def updateHealth(self, health):
        if self._DamagePanel__health is not health:
            self._DamagePanel__health = health
            self._DamagePanel__callFlash('updateHealth', [
                health])
        

    
    def updateSpeed(self, speed):
        if self._DamagePanel__speed is not speed:
            self._DamagePanel__speed = speed
            self._DamagePanel__callFlash('updateSpeed', [
                speed])
        

    
    def setCruiseMode(self, mode):
        self._DamagePanel__callFlash('setCruiseMode', [
            mode])

    
    def switchToVehicle(self, vID):
        if self._DamagePanel__vID is vID or vID is None:
            return None
        self._reset()
        self._DamagePanel__waitingTI.stop()
        self._DamagePanel__updateTI.stop()
        self._DamagePanel__vID = vID
        self._DamagePanel__waitingTI.start()

    
    def _reset(self):
        self._DamagePanel__vID = 0
        self._DamagePanel__speed = 0
        self._DamagePanel__health = 0
        self._DamagePanel__hasYawLimits = False
        self._DamagePanel__callFlash('reset')

    
    def _waiting(self):
        vehicle = BigWorld.entity(self._DamagePanel__vID)
        if vehicle is not None:
            self._DamagePanel__waitingTI.stop()
            self._setup(vehicle)
        

    
    def _setup(self, vehicle):
        vTypeDesc = vehicle.typeDescriptor
        vType = vTypeDesc.type
        yawLimits = vTypeDesc.turret['yawLimits']
        self._DamagePanel__tankIndicator._setup(vehicle)
        self._DamagePanel__hasYawLimits = yawLimits is not None
        modulesLayout = vehicleHasTurretRotator(vTypeDesc)
        continue
        crewLayout = [ elem[0] for elem in vType.crewRoles ]
        order = TANKMEN_ROLES_ORDER_DICT['plain']
        lastIdx = len(order)
        
        def comparator(item, other):
            if item in order:
                pass
            1
            itemIdx = lastIdx
            if other in order:
                pass
            1
            otherIdx = lastIdx
            return cmp(itemIdx, otherIdx)

        crewLayout = sorted(crewLayout, cmp = comparator)
        self._DamagePanel__callFlash('setIconsLayout', crewLayout + [
            modulesLayout])
        self._DamagePanel__callFlash('setMaxHealth', [
            vTypeDesc.maxHealth])
        self._DamagePanel__callFlash('updateHealth', [
            vehicle.health])
        if vehicle.isPlayer and self._DamagePanel__hasYawLimits:
            aih = BigWorld.player().inputHandler
            auto = False
            if aih is not None:
                auto = aih.getAutorotation()
            
            self.onVehicleAutorotationEnabled(auto)
        
        if not vehicle.isAlive():
            self.onVehicleDestroyed()
            return None
        self._DamagePanel__updateTI = None
        if vehicle.isPlayer:
            pass
        1
        self._DamagePanel__updateTI = 0.03('_updateSelf', '_updateOther', weakref.proxy(self))
        self._DamagePanel__updateTI.start()

    
    def _updateSelf(self):
        player = BigWorld.player()
        if player is None:
            return None
        vehicle = BigWorld.entity(self._DamagePanel__vID)
        if vehicle is not None and vehicle.isStarted:
            (speed, _) = player.getOwnVehicleSpeeds()
            self.updateSpeed(int(speed * 3.6))
        

    
    def _updateOther(self):
        vehicle = BigWorld.entity(self._DamagePanel__vID)
        if vehicle is not None:
            self.updateHealth(vehicle.health)
            if vehicle.isStarted:
                
                try:
                    speed = vehicle.filter.speedInfo.value[0]
                    (fwdSpeedLimit, bckwdSpeedLimit) = vehicle.typeDescriptor.physics['speedLimits']
                    speed = max(min(speed, fwdSpeedLimit), -bckwdSpeedLimit)
                    self.updateSpeed(int(speed * 3.6))
                except (AttributeError, IndexError, ValueError):
                    LOG_CURRENT_EXCEPTION()
                    LOG_ERROR('Can not update speed. Stop')
                    self._DamagePanel__updateTI.stop()
                

            if not vehicle.isAlive():
                self.onVehicleDestroyed()
                self._DamagePanel__updateTI.stop()
            
        

    
    def updateState(self, type, state):
        LOG_DEBUG('[DamagePanel.updateState] type = %s state = %s' % (type, state))
        self._DamagePanel__callFlash('updateState', [
            type,
            state])

    
    def onVehicleDestroyed(self):
        self._DamagePanel__updateTI.stop()
        self._DamagePanel__callFlash('onVehicleDestroyed')
        self._DamagePanel__callFlash('onCrewDeactivated')

    
    def onCrewDeactivated(self):
        self._DamagePanel__callFlash('onCrewDeactivated')

    
    def onFireInVehicle(self, bool):
        self._DamagePanel__callFlash('onFireInVehicle', [
            bool])

    
    def onVehicleAutorotationEnabled(self, value):
        if self._DamagePanel__hasYawLimits:
            self._DamagePanel__callFlash('onVehicleAutorotationEnabled', [
                value])
        

    
    def _DamagePanel__onClickToTankmenIcon(self, _, entityName, entityState):
        if BattleReplay.g_replayCtrl.isPlaying:
            return None
        if entityState == 'normal':
            self._DamagePanel__ui._showTankmanIsSafeMessage(entityName)
            return None
        BigWorld.player().onDamageIconButtonPressed('medkit', entityName)

    
    def _DamagePanel__onClickToDeviceIcon(self, _, entityName, entityState):
        if BattleReplay.g_replayCtrl.isPlaying:
            return None
        if entityState == 'normal':
            self._DamagePanel__ui._showDeviceIsNotDamagedMessage(entityName)
            return None
        BigWorld.player().onDamageIconButtonPressed('repairkit', entityName)

    
    def _DamagePanel__callFlash(self, funcName, args = None):
        self._DamagePanel__ui.call('battle.damagePanel.' + funcName, args)



class _TankIndicatorCtrl:
    
    def __init__(self, parentUI):
        self._TankIndicatorCtrl__ui = parentUI

    
    def __del__(self):
        LOG_DEBUG('_TankIndicatorCtrl deleted')

    
    def start(self):
        self._define()

    
    def destroy(self):
        setattr(self._TankIndicatorCtrl__ui.component, 'tankIndicator', None)
        self._TankIndicatorCtrl__ui = None

    
    def _define(self):
        mc = GUI.WGTankIndicatorFlash(self._TankIndicatorCtrl__ui.movie, '_root.damagePanel.tankIndicator')
        mc.wg_inputKeyMode = 2
        self._TankIndicatorCtrl__ui.component.addChild(mc, 'tankIndicator')

    
    def _setup(self, vehicle):
        vTypeDesc = vehicle.typeDescriptor
        vTags = vTypeDesc.type.tags
        yawLimits = vTypeDesc.turret['yawLimits']
        if 'SPG' in vTags:
            type = 'SPG'
        elif 'AT-SPG' in vTags:
            type = 'AT-SPG'
        else:
            type = 'Tank'
        hasYawLimits = yawLimits is not None
        if type in ('SPG', 'AT-SPG'):
            if not hasYawLimits or vehicleHasTurretRotator(vTypeDesc):
                type = 'Tank'
            
        self._TankIndicatorCtrl__flashCall('setType', [
            type])
        if hasYawLimits:
            args = [
                math.degrees(-yawLimits[0]),
                math.degrees(yawLimits[1]),
                True]
        else:
            args = [
                0,
                0,
                False]
        self._TankIndicatorCtrl__flashCall('setGunConstraints', args)
        if vehicle.isPlayer:
            hullMat = BigWorld.player().getOwnVehicleMatrix()
        else:
            hullMat = vehicle.matrix
        turretMat = vehicle.appearance.turretMatrix
        tankIndicator = self._TankIndicatorCtrl__ui.component.tankIndicator
        if hasYawLimits:
            pass
        1
        tankIndicator.wg_turretYawConstraints = Math.Vector2(0, 0)
        tankIndicator.wg_hullMatProv = hullMat
        tankIndicator.wg_turretMatProv = turretMat

    
    def _TankIndicatorCtrl__flashCall(self, funcName, args = None):
        if self._TankIndicatorCtrl__ui:
            self._TankIndicatorCtrl__ui.call('battle.tankIndicator.{0:>s}'.format(funcName), args)
        



class VehicleMarkersManager(Flash):
    _VehicleMarkersManager__SWF_FILE_NAME = 'VehicleMarkersManager.swf'
    ATTACK_REASONS = [
        'attack',
        'fire',
        'ramming',
        'world_collision',
        'death_zone',
        'drowning']
    
    class DAMAGE_TYPE:
        FROM_UNKNOWN = 0
        FROM_ALLY = 1
        FROM_ENEMY = 2
        FROM_SQUAD = 3
        FROM_PLAYER = 4

    
    def __init__(self, parentUI):
        Flash.__init__(self, self._VehicleMarkersManager__SWF_FILE_NAME)
        self.component.wg_inputKeyMode = 2
        self.component.position.z = DEPTH_OF_VehicleMarker
        self.component.drawWithRestrictedViewPort = False
        self.movie.backgroundAlpha = 0
        self.colorManager = ColorSchemeManager._ColorSchemeManager()
        self.colorManager.populateUI(weakref.proxy(self))
        self._VehicleMarkersManager__ownUI = None
        self._VehicleMarkersManager__parentUI = parentUI
        self._VehicleMarkersManager__markers = dict()

    
    def showExtendedInfo(self, value):
        self._VehicleMarkersManager__invokeCanvas('setShowExInfoFlag', [
            value])
        for handle in self._VehicleMarkersManager__markers.iterkeys():
            self._VehicleMarkersManager__invokeMarker(handle, 'showExInfo', [
                value])
        

    
    def setScaleProps(self, minScale = 40, maxScale = 100, defScale = 100, speed = 3):
        if constants.IS_DEVELOPMENT:
            self._VehicleMarkersManager__ownUI.scaleProperties = (minScale, maxScale, defScale, speed)
        

    
    def setAlphaProps(self, minAlpha = 40, maxAlpha = 100, defAlpha = 100, speed = 3):
        if constants.IS_DEVELOPMENT:
            self._VehicleMarkersManager__ownUI.alphaProperties = (minAlpha, maxAlpha, defAlpha, speed)
        

    
    def start(self):
        self.active(True)
        self._VehicleMarkersManager__ownUI = GUI.WGVehicleMarkersCanvasFlash(self.movie)
        self._VehicleMarkersManager__ownUI.wg_inputKeyMode = 2
        self._VehicleMarkersManager__ownUI.scaleProperties = GUI_SETTINGS.markerScaleSettings
        self._VehicleMarkersManager__ownUI.alphaProperties = GUI_SETTINGS.markerBgSettings
        self._VehicleMarkersManager__ownUIProxy = weakref.proxy(self._VehicleMarkersManager__ownUI)
        self._VehicleMarkersManager__parentUI.component.addChild(self._VehicleMarkersManager__ownUI, 'vehicleMarkersManager')
        self._VehicleMarkersManager__markersCanvasUI = self.getMember('vehicleMarkersCanvas')

    
    def destroy(self):
        if self._VehicleMarkersManager__parentUI is not None:
            setattr(self._VehicleMarkersManager__parentUI.component, 'vehicleMarkersManager', None)
        
        self._VehicleMarkersManager__parentUI = None
        self._VehicleMarkersManager__ownUI = None
        self._VehicleMarkersManager__markersCanvasUI = None
        self.colorManager.dispossessUI()
        self.close()

    
    def createMarker(self, vProxy):
        vInfo = dict(vProxy.publicInfo)
        if g_battleContext.isObserver(vProxy.id):
            return -1
        isFriend = vInfo['team'] == BigWorld.player().team
        vehicles = BigWorld.player().arena.vehicles
        vInfoEx = vehicles.get(vProxy.id, { })
        vTypeDescr = vProxy.typeDescriptor
        maxHealth = vTypeDescr.maxHealth
        mProv = vProxy.model.node('HP_gui')
        tags = set(vTypeDescr.type.tags & VEHICLE_CLASS_TAGS)
        if len(tags) > 0:
            pass
        1
        vClass = ''
        vType = vTypeDescr.type
        vIconSource = _CONTOUR_ICONS_MASK % {
            'unicName': vType.name.replace(':', '-') }
        entityName = g_battleContext.getPlayerEntityName(vProxy.id, vInfoEx)
        if BigWorld.player().team == vInfoEx.get('team'):
            pass
        1
        entityType = 'enemy'
        speaking = False
        if GUI_SETTINGS.voiceChat:
            speaking = VoiceChatInterface.g_instance.isPlayerSpeaking(vInfoEx.get('accountDBID', 0))
        
        hunting = VehicleActions.isHunting(vInfoEx.get('events', { }))
        if isFriend:
            pass
        1
        handle = mProv('VehicleMarkerAlly', 'VehicleMarkerEnemy')
        self._VehicleMarkersManager__markers[handle] = _VehicleMarker(vProxy, self._VehicleMarkersManager__ownUIProxy, handle)
        self._VehicleMarkersManager__invokeMarker(handle, 'init', [
            vClass,
            vIconSource,
            vType.shortUserString,
            vType.level,
            g_battleContext.getFullPlayerName(vInfoEx, showVehShortName = False),
            vProxy.health,
            maxHealth,
            entityName.name(),
            speaking,
            hunting,
            entityType])
        self._VehicleMarkersManager__parentUI.call('minimap.entryInited', [])
        return handle

    
    def destroyMarker(self, handle):
        if self._VehicleMarkersManager__markers.has_key(handle):
            del self._VehicleMarkersManager__markers[handle]
            self._VehicleMarkersManager__ownUI.delMarker(handle)
        

    
    def updateMarkerState(self, handle, newState, isImmediate = False):
        self._VehicleMarkersManager__invokeMarker(handle, 'updateState', [
            newState,
            isImmediate])

    
    def showActionMarker(self, handle, newState):
        self._VehicleMarkersManager__invokeMarker(handle, 'showActionMarker', [
            newState])

    
    def _VehicleMarkersManager__getVehicleDamageType(self, attackerID):
        if not attackerID:
            return VehicleMarkersManager.DAMAGE_TYPE.FROM_UNKNOWN
        if attackerID == BigWorld.player().playerVehicleID:
            return VehicleMarkersManager.DAMAGE_TYPE.FROM_PLAYER
        entityName = g_battleContext.getPlayerEntityName(attackerID, BigWorld.player().arena.vehicles.get(attackerID, dict()))
        if entityName == PLAYER_ENTITY_NAME.squadman:
            return VehicleMarkersManager.DAMAGE_TYPE.FROM_SQUAD
        if entityName == PLAYER_ENTITY_NAME.ally:
            return VehicleMarkersManager.DAMAGE_TYPE.FROM_ALLY
        if entityName == PLAYER_ENTITY_NAME.enemy:
            return VehicleMarkersManager.DAMAGE_TYPE.FROM_ENEMY
        return VehicleMarkersManager.DAMAGE_TYPE.FROM_UNKNOWN

    
    def onVehicleHealthChanged(self, handle, curHealth, attackerID = -1, attackReasonID = 0):
        self._VehicleMarkersManager__invokeMarker(handle, 'updateHealth', [
            curHealth,
            self._VehicleMarkersManager__getVehicleDamageType(attackerID),
            VehicleMarkersManager.ATTACK_REASONS[attackReasonID]])

    
    def showDynamic(self, vID, flag):
        handle = getattr(BigWorld.entity(vID), 'marker', None)
        if handle is not None and GUI_SETTINGS.voiceChat:
            self._VehicleMarkersManager__invokeMarker(handle, 'setSpeaking', [
                flag])
        

    
    def setTeamKiller(self, vID):
        if not g_battleContext.isTeamKiller(vID = vID):
            return None
        handle = getattr(BigWorld.entity(vID), 'marker', None)
        if handle is not None:
            self._VehicleMarkersManager__invokeMarker(handle, 'setEntityName', [
                PLAYER_ENTITY_NAME.teamKiller.name()])
        

    
    def _VehicleMarkersManager__invokeMarker(self, handle, function, args = None):
        if handle == -1:
            return None
        if args is None:
            args = []
        
        self._VehicleMarkersManager__ownUI.markerInvoke(handle, (function, args))

    
    def _VehicleMarkersManager__invokeCanvas(self, function, args = None):
        if args is None:
            args = []
        
        self.call('battle.vehicleMarkersCanvas.' + function, args)

    
    def setMarkerSettings(self, settings):
        if self._VehicleMarkersManager__markersCanvasUI:
            self._VehicleMarkersManager__markersCanvasUI.setMarkerSettings(settings)
        

    
    def setMarkerDuration(self, value):
        self._VehicleMarkersManager__invokeCanvas('setMarkerDuration', [
            value])

    
    def updateMarkers(self):
        self.colorManager.update()
        for handle in self._VehicleMarkersManager__markers.iterkeys():
            self._VehicleMarkersManager__invokeMarker(handle, 'update', [])
        

    
    def updateMarkerSettings(self):
        for handle in self._VehicleMarkersManager__markers.iterkeys():
            self._VehicleMarkersManager__invokeMarker(handle, 'updateMarkerSettings', [])
        



class _VehicleMarker:
    
    def __init__(self, vProxy, uiProxy, handle):
        self.vProxy = vProxy
        self.uiProxy = uiProxy
        self.handle = handle
        self.vProxy.appearance.onModelChanged += self._VehicleMarker__onModelChanged

    
    def destroy(self):
        self.vProxy.appearance.onModelChanged -= self._VehicleMarker__onModelChanged
        self.vProxy = None
        self.uiProxy = None
        self.handle = -1

    
    def _VehicleMarker__onModelChanged(self):
        self.uiProxy.markerSetMatrix(self.handle, self.vProxy.model.node('HP_gui'))



class FadingMessagesPanel(object):
    _FadingMessagesPanel__settings = []
    _FadingMessagesPanel__messageDict = { }
    _EXTRA_COLOR_FORMAT = '<font color="#{0:02X}{1:02X}{2:02X}">{3:>s}</font>'
    
    def __init__(self, parentUI, name, cfgFileName, isColorBlind = False):
        self._FadingMessagesPanel__ui = parentUI
        self._FadingMessagesPanel__name = name
        self._FadingMessagesPanel__pathPrefix = 'battle.' + name + '.' + '%s'
        self._FadingMessagesPanel__readConfig(cfgFileName)
        self._FadingMessagesPanel__ui.addExternalCallbacks({
            'battle.%s.PopulateUI' % name: self._FadingMessagesPanel__onPopulateUI })
        self.defineColorFlags(isColorBlind = isColorBlind)

    
    def start(self):
        self._FadingMessagesPanel__callFlash('RefreshUI')

    
    def destroy(self):
        self._FadingMessagesPanel__ui = None

    
    def defineColorFlags(self, isColorBlind = False):
        if isColorBlind:
            pass
        1
        self._FadingMessagesPanel__colorGroup = 'default'

    
    def showMessage(self, key, args = None, extra = None):
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.isTimeWarpInProgress:
            return None
        (msgText, colors) = self._FadingMessagesPanel__messageDict.get(key, (None, ''))
        if msgText is None:
            if args:
                pass
            1
            key(key, args.get('colorAlias'), None)
            return None
        if args is not None:
            self._FadingMessagesPanel__formatEntitiesEx(args, extra = extra)
            
            try:
                msgText = msgText % args
            except TypeError:
                msgText is None
                LOG_CURRENT_EXCEPTION()
            

        if self._FadingMessagesPanel__colorGroup in colors:
            pass
        1
        key(msgText, colors.get, self._FadingMessagesPanel__colorGroup('default'))

    
    def _FadingMessagesPanel__showMessage(self, key, msgText, color):
        LOG_DEBUG('%s: show message with key = %s' % (self._FadingMessagesPanel__name, key))
        self._FadingMessagesPanel__callFlash('ShowMessage', [
            key,
            msgText,
            color])

    
    def _FadingMessagesPanel__formatEntitiesEx(self, args, extra = None):
        if extra is None:
            extra = ()
        
        csManager = self._FadingMessagesPanel__ui.colorManager
        for (argName, vID) in extra:
            arg = args.get(argName)
            rgba = None
            if g_battleContext.isTeamKiller(vID = vID):
                rgba = csManager.getScheme('teamkiller').get(self._FadingMessagesPanel__colorGroup, { }).get('rgba')
            elif g_battleContext.isSquadMan(vID = vID):
                rgba = csManager.getScheme('squad').get(self._FadingMessagesPanel__colorGroup, { }).get('rgba')
            
            if arg and rgba:
                args[argName] = self._EXTRA_COLOR_FORMAT.format(int(rgba[0]), int(rgba[1]), int(rgba[2]), arg)
                continue
        

    
    def _FadingMessagesPanel__readConfig(self, cfgFileName):
        self._FadingMessagesPanel__settings = []
        import ResMgr as ResMgr
        sec = ResMgr.openSection(cfgFileName)
        if sec is None:
            raise Exception, "can not open '%s'" % cfgFileName
        sec is None
        self._FadingMessagesPanel__settings.append(sec.readInt('maxLinesCount', -1))
        direction = sec.readString('direction')
        if direction not in ('up', 'down'):
            raise Exception, 'Wrong direction value in %s' % cfgFileName
        direction not in ('up', 'down')
        self._FadingMessagesPanel__settings.append(direction)
        self._FadingMessagesPanel__settings.append(sec.readFloat('lifeTime'))
        self._FadingMessagesPanel__settings.append(sec.readFloat('alphaSpeed'))
        self._FadingMessagesPanel__settings.append(sec.readBool('showUniqueOnly', False))
        self._FadingMessagesPanel__messageDict = dict()
        for (mTag, mSec) in sec['messages'].items():
            text = mSec.readString('text')
            text = html.translation(text)
            aliasesSec = mSec['colorAlias']
            aliases = aliasesSec.items()
            if len(aliases):
                groups = dict((lambda .0: for (key, section) in .0:
(key, section.asString))(aliases))
            else:
                groups = {
                    'default': aliasesSec.asString }
            self._FadingMessagesPanel__messageDict[mTag] = (text, groups)
        

    
    def _FadingMessagesPanel__callFlash(self, funcName, args = None):
        self._FadingMessagesPanel__ui.call(self._FadingMessagesPanel__pathPrefix % funcName, args)

    
    def _FadingMessagesPanel__onPopulateUI(self, requestId):
        args = [
            requestId]
        args.extend(self._FadingMessagesPanel__settings)
        self._FadingMessagesPanel__ui.respond(args)



def _playerComparator(x1, x2):
    INDEX_IS_ALIVE = 17
    INDEX_BALANCE_WEIGHT = 18
    INDEX_VEHICLE_NAME = 2
    INDEX_PLAYER_NAME = 0
    if x1[INDEX_IS_ALIVE] < x2[INDEX_IS_ALIVE]:
        return -1
    if x1[INDEX_IS_ALIVE] > x2[INDEX_IS_ALIVE]:
        return 1
    if x1[INDEX_BALANCE_WEIGHT] < x2[INDEX_BALANCE_WEIGHT]:
        return 1
    if x1[INDEX_BALANCE_WEIGHT] > x2[INDEX_BALANCE_WEIGHT]:
        return -1
    if x1[INDEX_VEHICLE_NAME] < x2[INDEX_VEHICLE_NAME]:
        return -1
    if x1[INDEX_VEHICLE_NAME] > x2[INDEX_VEHICLE_NAME]:
        return 1
    if x1[INDEX_PLAYER_NAME] < x2[INDEX_PLAYER_NAME]:
        return -1
    if x1[INDEX_PLAYER_NAME] > x2[INDEX_PLAYER_NAME]:
        return 1
    return 0


class _TimeInterval:
    
    def __init__(self, interval, funcName, scopeProxy = None):
        self._TimeInterval__cbId = None
        self._TimeInterval__interval = interval
        self._TimeInterval__funcName = funcName
        self._TimeInterval__scopeProxy = scopeProxy

    
    def start(self):
        if self._TimeInterval__cbId is not None:
            LOG_ERROR('To start a new time interval You should before stop already the running time interval.')
            return None
        self._TimeInterval__cbId = BigWorld.callback(self._TimeInterval__interval, self._TimeInterval__update)

    
    def stop(self):
        if self._TimeInterval__cbId is not None:
            BigWorld.cancelCallback(self._TimeInterval__cbId)
            self._TimeInterval__cbId = None
        

    
    def _TimeInterval__update(self):
        self._TimeInterval__cbId = None
        self._TimeInterval__cbId = BigWorld.callback(self._TimeInterval__interval, self._TimeInterval__update)
        if self._TimeInterval__scopeProxy is not None:
            funcObj = getattr(self._TimeInterval__scopeProxy, self._TimeInterval__funcName, None)
            if funcObj is not None:
                funcObj()
            
        



def vehicleHasTurretRotator(vTypeDesc):
    result = True
    if vTypeDesc.type.tags & set([
        'SPG',
        'AT-SPG']) and len(vTypeDesc.hull.get('fakeTurrets', { }).get('battle', ())) > 0:
        result = False
    
    return result


