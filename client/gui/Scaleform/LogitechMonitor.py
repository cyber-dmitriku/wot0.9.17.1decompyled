# Source Generated with Decompyle++
# File: LogitechMonitor.pyc (Python 2.6)

import BigWorld
import _Scaleform
import Avatar
import constants
import CommandMapping
from debug_utils import LOG_DEBUG
from gui.Scaleform.Flash import Flash
from adisp import process
from gui.Scaleform.utils.requesters import StatsRequester
from gui.Scaleform.utils import dossiers_utils
from messenger.wrappers import ChatActionWrapper
from messenger import filters, g_settings
from messenger.gui import MessengerDispatcher
from gui.Scaleform.ColorSchemeManager import _ColorSchemeManager
from CurrentVehicle import g_currentVehicle
from helpers import i18n
from time import time
from gui.Scaleform.utils.functions import getArenaSubTypeName

class _LogitachFlash(Flash):
    
    def __init__(self, isColored, width, height):
        if isColored:
            pass
        1
        swf = 'keyboardMono.swf'
        Flash.__init__(self, swf)
        self.movie.wg_outputToLogitechLcd = True

    
    def __del__(self):
        if self.movie:
            self.movie.wg_outputToLogitechLcd = False
        
        LOG_DEBUG('_LogitachFlash::destroy', self)

    
    def movie(self):
        return self.component.movie

    movie = property(movie)


class _LogitechScreen(object):
    
    def __init__(self, component, frame):
        self.uiHolder = component
        self._LogitechScreen__frameLabel = frame

    
    def __del__(self):
        LOG_DEBUG('_LogitechScreen::destroy', self)

    
    def load(self, isColored):
        LOG_DEBUG('Logitech changeScreen: ', self._LogitechScreen__frameLabel)
        self.uiHolder.call('logitech.gotoFrame', [
            self._LogitechScreen__frameLabel])
        if not isColored:
            self.onLoadedMono()
        

    
    def onLoaded(self):
        pass

    
    def onLoadedMono(self):
        pass

    
    def destroy(self, isColored):
        if not isColored:
            self.onUnloadMono()
        
        self.uiHolder = None
        self.onUnload()

    
    def onUnload(self):
        pass

    
    def onUnloadMono(self):
        pass

    
    def onChangeView(self):
        self.call('logitech.changeView', [])

    
    def call(self, methodName, args = None):
        self.uiHolder.call(methodName, args)



class _LogoScreen(_LogitechScreen):
    
    def __init__(self, component):
        _LogitechScreen.__init__(self, component, 'logo')

    
    def onLoadedMono(self):
        self.uiHolder.call('logitech.setMonoText', [
            i18n.makeString('#menu:login/version')])



class _StatsScreen(_LogitechScreen):
    
    def __init__(self, component):
        _LogitechScreen.__init__(self, component, 'stats')

    
    def onLoadedMono(self):
        self.onVehicleChange()
        g_currentVehicle.onChanged += self.onVehicleChange

    
    def onUnloadMono(self):
        g_currentVehicle.onChanged -= self.onVehicleChange

    
    def onVehicleChange(self):
        self.uiHolder.call('logitech.setMonoText', [
            g_currentVehicle.vehicle.name + '\r\n' + i18n.makeString(g_currentVehicle.getReadyMessage()[0])])

    
    def onLoaded(self):
        yield StatsRequester().getAccountDossier()
        dossier = None
        self.call('logitech.setStatsData', dossiers_utils.getDossierTotalBlocksSummary(dossier, isCompact = True))

    onLoaded = process(onLoaded)


class _BattleLoadingScreen(_LogitechScreen):
    _MAP_SOURCE = '../maps/icons/map/screen/%s.png'
    
    def __init__(self, component):
        _LogitechScreen.__init__(self, component, 'mapLoading')

    
    def onLoaded(self):
        arena = getattr(BigWorld.player(), 'arena', None)
        if arena:
            self.call('logitech.setMap', [
                arena.arenaType.name,
                '#arenas:type/%s/name' % getArenaSubTypeName(BigWorld.player().arenaTypeID),
                self._MAP_SOURCE % arena.arenaType.geometryName])
        



class _BattleScreen(_LogitechScreen):
    _BattleScreen__viewCmds = ('CMD_CHAT_SHORTCUT_ATTACK', 'CMD_CHAT_SHORTCUT_BACKTOBASE', 'CMD_CHAT_SHORTCUT_FOLLOWME', 'CMD_CHAT_SHORTCUT_POSITIVE', 'CMD_CHAT_SHORTCUT_NEGATIVE', 'CMD_CHAT_SHORTCUT_HELPME', 'CMD_CHAT_SHORTCUT_ATTACK_MY_TARGET')
    _BattleScreen__timerCallBackId = None
    _BattleScreen__debugCallBackId = None
    
    def __init__(self, component):
        _LogitechScreen.__init__(self, component, 'battle')
        self.messenger = None
        self._colorManager = None

    
    def onLoadedMono(self):
        self.onUpdateMono()

    
    def onUnloadMono(self):
        if self._BattleScreen__timerCallBackId:
            BigWorld.cancelCallback(self._BattleScreen__timerCallBackId)
            self._BattleScreen__timerCallBackId = None
        

    
    def onUpdateMono(self):
        self._BattleScreen__timerCallBackId = None
        player = BigWorld.player()
        if player is None or type(player) != Avatar.PlayerAvatar:
            return None
        arena = BigWorld.player().arena
        if arena is None:
            return None
        arenaLength = int(arena.periodEndTime - BigWorld.serverTime())
        if arenaLength > 0:
            pass
        1
        arenaLength = 0
        (allayFrags, enemyFrags, _, _) = self.getFrags()
        msg = '%s :%s\n%d :%d\n' % (i18n.makeString('#ingame_gui:player_messages/allied_team_name'), i18n.makeString('#ingame_gui:player_messages/enemy_team_name'), allayFrags, enemyFrags)
        if arena.period == constants.ARENA_PERIOD.BATTLE:
            (m, s) = divmod(arenaLength, 60)
            msg += '\n%s: %d :%02d' % (i18n.makeString('#ingame_gui:timer/battlePeriod'), m, s)
        
        self.uiHolder.call('logitech.setMonoText', [
            msg])
        self._BattleScreen__timerCallBackId = BigWorld.callback(1, self.onUpdateMono)

    
    def onLoaded(self):
        _alliedTeamName = '#ingame_gui:player_messages/allied_team_name'
        _enemyTeamName = '#ingame_gui:player_messages/enemy_team_name'
        self.call('battle.fragCorrelationBar.setTeamNames', [
            _alliedTeamName,
            _enemyTeamName])
        player = BigWorld.player()
        if player is None or type(player) != Avatar.PlayerAvatar:
            return None
        arena = BigWorld.player().arena
        if arena is None:
            return None
        self._BattleScreen__updateDebug()
        self._BattleScreen__onSetArenaTime()
        self._BattleScreen__updatePlayers()
        self.setCommands()
        arena.onPeriodChange += self._BattleScreen__onSetArenaTime
        arena.onNewVehicleListReceived += self._BattleScreen__updatePlayers
        arena.onNewStatisticsReceived += self._BattleScreen__updatePlayers
        arena.onVehicleAdded += self._BattleScreen__updatePlayers
        arena.onVehicleStatisticsUpdate += self._BattleScreen__updatePlayers
        arena.onVehicleKilled += self._BattleScreen__updatePlayers
        arena.onAvatarReady += self._BattleScreen__updatePlayers
        LogitechBattleMessanger.instance(self.uiHolder)
        self._colorManager = _ColorSchemeManager()
        self._colorManager.populateUI(self.uiHolder)

    
    def onUnload(self):
        player = BigWorld.player()
        if player is None or type(player) != Avatar.PlayerAvatar:
            return None
        arena = BigWorld.player().arena
        if arena is None:
            return None
        arena.onPeriodChange -= self._BattleScreen__onSetArenaTime
        arena.onNewVehicleListReceived -= self._BattleScreen__updatePlayers
        arena.onNewStatisticsReceived -= self._BattleScreen__updatePlayers
        arena.onVehicleAdded -= self._BattleScreen__updatePlayers
        arena.onVehicleStatisticsUpdate -= self._BattleScreen__updatePlayers
        arena.onVehicleKilled -= self._BattleScreen__updatePlayers
        arena.onAvatarReady -= self._BattleScreen__updatePlayers
        if self._BattleScreen__timerCallBackId:
            BigWorld.cancelCallback(self._BattleScreen__timerCallBackId)
            self._BattleScreen__timerCallBackId = None
        
        if self._BattleScreen__debugCallBackId:
            BigWorld.cancelCallback(self._BattleScreen__debugCallBackId)
            self._BattleScreen__debugCallBackId = None
        
        if self._colorManager:
            self._colorManager.dispossessUI()
        
        _LogitechScreen.onUnload(self)

    
    def _BattleScreen__updatePlayers(self, *args):
        self.call('battle.fragCorrelationBar.updateFrags', list(self.getFrags()))

    
    def getFrags(self):
        player = BigWorld.player()
        if player is None or type(player) != Avatar.PlayerAvatar:
            return None
        arena = BigWorld.player().arena
        if arena is None:
            return None
        vehicles = arena.vehicles
        frags = {
            1: 0,
            2: 0 }
        total = {
            1: 0,
            2: 0 }
        for (vId, vData) in vehicles.items():
            vStats = arena.statistics.get(vId, None)
            if vStats is None:
                pass
            1
            0 += vStats['frags']
            total[vData['team']] += 1
        
        playerTeam = player.team
        enemyTeam = 3 - playerTeam
        return (frags[playerTeam], frags[enemyTeam], total[playerTeam], total[enemyTeam])

    
    def _BattleScreen__onSetArenaTime(self, *args):
        self._BattleScreen__timerCallBackId = None
        player = BigWorld.player()
        if player is None or type(player) != Avatar.PlayerAvatar:
            return None
        arena = BigWorld.player().arena
        if arena is None:
            return None
        arenaLength = int(arena.periodEndTime - BigWorld.serverTime())
        if arenaLength > 0:
            pass
        1
        arenaLength = 0
        self.call('battle.timerBar.setTotalTime', [
            arenaLength])
        if arenaLength > 1:
            self._BattleScreen__timerCallBackId = BigWorld.callback(1, self._BattleScreen__onSetArenaTime)
        

    
    def _BattleScreen__updateDebug(self):
        self._BattleScreen__debugCallBackId = None
        player = BigWorld.player()
        if player is None or not hasattr(player, 'playerVehicleID'):
            return None
        isLaggingNow = False
        vehicle = BigWorld.entity(player.playerVehicleID)
        if vehicle is not None and isinstance(vehicle.filter, BigWorld.WGVehicleFilter):
            isLaggingNow = vehicle.filter.isLaggingNow
        
        ping = min(BigWorld.LatencyInfo().value[3] * 1000, 999)
        if ping < 999:
            ping = max(1, ping - 500 * constants.SERVER_TICK_LENGTH)
        
        fps = BigWorld.getFPS()[0]
        self.call('battle.debugBar.updateInfo', [
            int(fps),
            int(ping),
            isLaggingNow])
        self._BattleScreen__debugCallBackId = BigWorld.callback(0.01, self._BattleScreen__updateDebug)

    
    def setCommands(self):
        cmdMap = CommandMapping.g_instance
        viewCmdMapping = []
        for command in self._BattleScreen__viewCmds:
            key = cmdMap.get(command)
            viewCmdMapping.append(command)
            if key is not None:
                pass
            1
            BigWorld.keyToString(key)('NONE')
        
        self.call('battle.ingameHelp.setCommandMapping', viewCmdMapping)



class _PostmortemScreen(_BattleScreen):
    
    def __init__(self, component):
        _LogitechScreen.__init__(self, component, 'postmortem')
        self.messenger = None

    
    def load(self, isColored):
        _BattleScreen.load(self, isColored)
        if isColored:
            self.onLoaded()
        

    
    def setCommands(self):
        self.call('battle.ingameHelp.setCommandMapping', [])

    
    def onUnload(self):
        LogitechBattleMessanger.destroyInstance()



class LogitechBattleMessanger(object):
    _LogitechBattleMessanger__inst = None
    
    def instance(uiHolder = None):
        if LogitechBattleMessanger._LogitechBattleMessanger__inst is None:
            LogitechBattleMessanger._LogitechBattleMessanger__inst = LogitechBattleMessanger()
            LogitechBattleMessanger._LogitechBattleMessanger__inst.create()
        
        return LogitechBattleMessanger._LogitechBattleMessanger__inst.messenger.start(uiHolder)

    instance = staticmethod(instance)
    
    def destroyInstance():
        if LogitechBattleMessanger._LogitechBattleMessanger__inst:
            LogitechBattleMessanger._LogitechBattleMessanger__inst.destroy()
        
        LogitechBattleMessanger._LogitechBattleMessanger__inst = None

    destroyInstance = staticmethod(destroyInstance)
    
    def __init__(self):
        self.messenger = None

    
    def create(self):
        MessengerBattleInterface = MessengerBattleInterface
        import messenger.gui.Scalefrom.MessengerBattleInterface
        self.messenger = MessengerBattleInterface()
        chatManager = chatManager
        import ChatManager
        CHAT_ACTIONS = CHAT_ACTIONS
        import chat_shared
        chatManager.subscribeChatAction(self.onBroadcast, CHAT_ACTIONS.broadcast)
        chatManager.subscribeChatAction(self.onSelfEnterChat, CHAT_ACTIONS.selfEnter)

    
    def destroy(self):
        chatManager = chatManager
        import ChatManager
        CHAT_ACTIONS = CHAT_ACTIONS
        import chat_shared
        chatManager.unsubscribeChatAction(self.onBroadcast, CHAT_ACTIONS.broadcast)
        chatManager.unsubscribeChatAction(self.onSelfEnterChat, CHAT_ACTIONS.selfEnter)
        self.messenger.destroy()
        self.messenger = None

    
    def onBroadcast(self, chatAction):
        '''
\t\tEvent handler.
\t\tWhen player post message to channel, adds message to this channel
\t\t'''
        wrapper = ChatActionWrapper(**None)
        cid = wrapper.channel
        filterChain = filters.FilterChain()
        if g_settings.userPreferences['enableOlFilter']:
            filterChain.addFilter('olFilter', filters.ObsceneLanguageFilter())
        
        filterChain.chainIn(wrapper)
        self.messenger.addChannelMessage(wrapper)

    
    def onSelfEnterChat(self, chatAction):
        wrapper = ChatActionWrapper(**None)
        cid = wrapper.channel
        uid = wrapper.originator
        channel = MessengerDispatcher.g_instance.channels.getChannel(cid)
        if not channel:
            ChannelNotFound = ChannelNotFound
            import messenger.exeptions
            raise ChannelNotFound(cid)
        self.messenger.addChannel(channel)



class LogitechMonitor(object):
    _LogitechMonitor__component = None
    _LogitechMonitor__screen = None
    _LogitechMonitor__currentScreen = None
    _LogitechMonitor__isColored = False
    SCREEN_TO_FRAME = {
        'login': _LogoScreen,
        'hangar': _StatsScreen,
        'battleloading': _BattleLoadingScreen,
        'battle': _BattleScreen,
        'postmortem': _PostmortemScreen }
    
    def init():
        LogitechMonitor.onScreenChange('login')
        import LcdKeyboard as LcdKeyboard
        if LcdKeyboard._g_instance:
            LcdKeyboard._g_instance.changeNotifyCallback = LogitechMonitor.onChange
        

    init = staticmethod(init)
    
    def onChange(isEnabled, isColored, width, height):
        if isEnabled:
            LogitechMonitor.destroy()
            LogitechMonitor._LogitechMonitor__isColored = isColored
            LogitechMonitor._LogitechMonitor__component = _LogitachFlash(isColored, width, height)
            LogitechMonitor._LogitechMonitor__component.addExternalCallback('logitech.frameLoaded', LogitechMonitor.onScreenLoaded)
            LOG_DEBUG('Logitech keyboard display found: colored = %s,  size = %sx%s' % (isColored, width, height))
            LogitechMonitor.onScreenChange()
        else:
            LogitechMonitor.destroy()
            LOG_DEBUG('No logitech keyboard color display found')

    onChange = staticmethod(onChange)
    
    def isPresent():
        return LogitechMonitor._LogitechMonitor__component is not None

    isPresent = staticmethod(isPresent)
    
    def isPresentColor():
        return LogitechMonitor._LogitechMonitor__isColored

    isPresentColor = staticmethod(isPresentColor)
    
    def destroy():
        LogitechMonitor._LogitechMonitor__isColored = False
        if LogitechMonitor._LogitechMonitor__screen:
            LogitechMonitor._LogitechMonitor__screen.destroy(LogitechMonitor._LogitechMonitor__isColored)
            LogitechMonitor._LogitechMonitor__screen = None
        
        if LogitechMonitor._LogitechMonitor__component:
            LogitechMonitor._LogitechMonitor__component.close()
            LogitechMonitor._LogitechMonitor__component = None
        

    destroy = staticmethod(destroy)
    
    def onScreenChange(currentScreen = None):
        if currentScreen in LogitechMonitor.SCREEN_TO_FRAME.keys():
            LogitechMonitor._LogitechMonitor__currentScreen = currentScreen
        
        if LogitechMonitor._LogitechMonitor__component:
            screenClass = LogitechMonitor.SCREEN_TO_FRAME[LogitechMonitor._LogitechMonitor__currentScreen]
            if not isinstance(LogitechMonitor._LogitechMonitor__screen, screenClass):
                if LogitechMonitor._LogitechMonitor__screen:
                    LogitechMonitor._LogitechMonitor__screen.destroy(LogitechMonitor._LogitechMonitor__isColored)
                
                LogitechMonitor._LogitechMonitor__screen = screenClass(LogitechMonitor._LogitechMonitor__component)
            
            LogitechMonitor._LogitechMonitor__screen.load(LogitechMonitor._LogitechMonitor__isColored)
        

    onScreenChange = staticmethod(onScreenChange)
    
    def onScreenLoaded(callBackID, screenLabel):
        if LogitechMonitor._LogitechMonitor__screen:
            LOG_DEBUG('LogitechMonitor::screen loaded:', screenLabel)
            LogitechMonitor._LogitechMonitor__screen.onLoaded()
        

    onScreenLoaded = staticmethod(onScreenLoaded)
    
    def onChangeView():
        if LogitechMonitor._LogitechMonitor__screen:
            LOG_DEBUG('LogitechMonitor::screen change view:')
            LogitechMonitor._LogitechMonitor__screen.onChangeView()
        

    onChangeView = staticmethod(onChangeView)


