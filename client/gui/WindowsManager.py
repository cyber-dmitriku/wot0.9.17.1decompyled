# Source Generated with Decompyle++
# File: WindowsManager.pyc (Python 2.6)

import BigWorld
from ConnectionManager import connectionManager
from gui.Scaleform.CommonPage import CommonPage
from gui.Scaleform.Battle import Battle
from PlayerEvents import g_playerEvents
import Settings
from gui.Scaleform.LogitechMonitor import LogitechMonitor
from debug_utils import LOG_ERROR
from predefined_hosts import g_preDefinedHosts

class WindowsManager(object):
    
    def __init__(self):
        self._WindowsManager__window = None
        self._WindowsManager__battleWindow = None
        self._subscribe()
        self._WindowsManager__currentLanguage = None

    
    def _WindowsManager__getBattleWindow(self):
        return self._WindowsManager__battleWindow

    battleWindow = property(_WindowsManager__getBattleWindow)
    
    def _WindowsManager__getWindow(self):
        return self._WindowsManager__window

    
    def _WindowsManager__setWindow(self, windowClass):
        if windowClass is None or not isinstance(self._WindowsManager__window, windowClass):
            if self._WindowsManager__window is not None:
                self._WindowsManager__window.close()
            
            if windowClass is not None:
                pass
            1
            self._WindowsManager__window = None
        

    window = property(_WindowsManager__getWindow, _WindowsManager__setWindow)
    
    def _subscribe(self):
        g_playerEvents.onAccountShowGUI += self.showLobby
        g_playerEvents.onAccountBecomeNonPlayer += self.clearHangar
        g_playerEvents.onAvatarBecomePlayer += self.showBattleLoading

    
    def _unsubscribe(self):
        g_playerEvents.onAccountShowGUI -= self.showLobby
        g_playerEvents.onAccountBecomeNonPlayer -= self.clearHangar
        g_playerEvents.onAvatarBecomePlayer -= self.showBattleLoading

    
    def destroy(self):
        LogitechMonitor.destroy()
        self._unsubscribe()
        self.hideAll()

    
    def start(self):
        LogitechMonitor.init()
        prefs = Settings.g_instance.userPrefs
        if not prefs is None:
            pass
        showStartupMovie = prefs.readInt(Settings.KEY_SHOW_STARTUP_MOVIE, 1) == 1
        if not BigWorld.wg_isSSE2Supported():
            showStartupMovie = False
        
        g_replayCtrl = g_replayCtrl
        import BattleReplay
        if g_replayCtrl.autoStartBattleReplay():
            return None
        if showStartupMovie:
            self.showStartGameVideo()
        else:
            self.showLogin()

    
    def showStartGameVideo(self):
        self.window = CommonPage
        self.window.active(True)
        self.window.processStartGameVideo()

    
    def showLogin(self):
        self._WindowsManager__currentLanguage = None
        self.window = CommonPage
        self.window.active(True)
        self.window.processLogin()

    
    def showLobby(self, ctx = { }):
        if self._WindowsManager__currentLanguage is None:
            getClientLanguage = getClientLanguage
            import helpers
            self._WindowsManager__currentLanguage = getClientLanguage()
            BigWorld.player().setLanguage(self._WindowsManager__currentLanguage)
        
        self.window = CommonPage
        self.window.active(True)
        self.window.processLobby(ctx.has_key('queueID'))

    
    def getHangarSpace(self):
        if not hasattr(self.window, 'currentInterface') or not (self.window.currentInterface == 'hangar'):
            return None
        return self.window.space

    
    def hideAll(self):
        self.window = None
        self.clearHangar()

    
    def clearHangar(self):
        g_hangarSpace = g_hangarSpace
        import gui.Scaleform.utils.HangarSpace
        g_hangarSpace.destroy()

    
    def showBattleLoading(self):
        g_preDefinedHosts.savePeripheryTL(connectionManager.peripheryID)
        BigWorld.wg_setReducedFpsMode(True)
        self.window = CommonPage
        self.window.active(True)
        self.window.processBattleLoading()

    
    def showBattle(self):
        if self._WindowsManager__window is not None and not isinstance(self._WindowsManager__window, Battle):
            self._WindowsManager__window.close()
            self._WindowsManager__window = None
        
        BigWorld.wg_setReducedFpsMode(False)
        if self._WindowsManager__battleWindow:
            self._WindowsManager__window = self._WindowsManager__battleWindow
            self.window.component.visible = True
        

    
    def showPostMortem(self):
        LogitechMonitor.onScreenChange('postmortem')
        if self._WindowsManager__battleWindow:
            self._WindowsManager__battleWindow.showPostmortemTips()
        

    
    def startBattle(self):
        LogitechMonitor.onScreenChange('battle')
        self._WindowsManager__battleWindow = Battle()
        self._WindowsManager__battleWindow.active(True)
        self._WindowsManager__battleWindow.component.visible = False
        return self._WindowsManager__battleWindow

    
    def destroyBattle(self):
        self._WindowsManager__battleWindow.active(False)
        self._WindowsManager__battleWindow = None

    
    def showBotsMenu(self):
        import exceptions as exceptions
        
        try:
            BotsMenu = BotsMenu
            import gui.Scaleform.development.BotsMenu
            BotsMenu(self._WindowsManager__battleWindow).active(True)
        except exceptions.ImportError:
            LOG_ERROR = LOG_ERROR
            import debug_utils
            LOG_ERROR('Package gui.Scaleform.development not found.')



g_windowsManager = WindowsManager()

