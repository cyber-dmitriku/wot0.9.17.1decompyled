# Source Generated with Decompyle++
# File: game.pyc (Python 2.6)

import AreaDestructibles
import BigWorld
import constants
import CommandMapping
import ResMgr
from post_processing import g_postProcessing
from ConnectionManager import connectionManager
from CurrentVehicle import g_currentVehicle
from debug_utils import LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_ERROR
import GUI
from gui import AOGAS, CLIENT_ENCODING, SystemMessages
from gui.WindowsManager import g_windowsManager
from gui.Scaleform.GameLoading import GameLoading
from gui.Scaleform.Waiting import Waiting
from messenger import gui as messengerGUI
from messenger.gui import MessengerDispatcher
import MusicController
import Settings
from TmpConsoleCmds import *
from MemoryCriticalController import g_critMemHandler
import VOIP
from gui.Scaleform.Disconnect import Disconnect
from gui.Scaleform import VoiceChatInterface
from gui import InputHandler
import sys
import asyncore

try:
    from tutorial.TutorialLoader import init as tutorialLoaderInit
    from tutorial.TutorialLoader import fini as tutorialLoaderFini
except ImportError:
    LOG_ERROR('Module tutorial not found')
    
    tutorialLoaderInit = lambda : pass
    
    tutorialLoaderFini = lambda : pass

__import__('__main__').GameLoading = GameLoading
import locale
locale.setlocale(locale.LC_TIME, '')
from gui.Scaleform import fonts_config
fonts_config.g_fontConfigMap.load()
g_guiResetters = set()
g_repeatKeyHandlers = set()
g_replayCtrl = None

def autoFlushPythonLog():
    BigWorld.flushPythonLog()
    BigWorld.callback(5, autoFlushPythonLog)


def init(scriptConfig, engineConfig, userPreferences, loadingScreenGUI = None):
    global g_replayCtrl
    
    try:
        if constants.IS_DEVELOPMENT:
            autoFlushPythonLog()
        
        LOG_DEBUG('init')
        BigWorld.wg_initCustomSettings()
        Settings.g_instance = Settings.Settings(scriptConfig, engineConfig, userPreferences)
        CommandMapping.g_instance = CommandMapping.CommandMapping()
        DecalMap = DecalMap
        import helpers
        DecalMap.g_instance = DecalMap.DecalMap(scriptConfig['decal'])
        EdgeDetectColorController = EdgeDetectColorController
        import helpers
        EdgeDetectColorController.g_instance = EdgeDetectColorController.EdgeDetectColorController(scriptConfig['silhouetteColors'])
        import SoundGroups as SoundGroups
        SoundGroups.g_instance = SoundGroups.SoundGroups()
        import BattleReplay as BattleReplay
        g_replayCtrl = BattleReplay.BattleReplay()
        BattleReplay.g_replayCtrl = BattleReplay.BattleReplay()
        g_replayCtrl.registerWotReplayFileExtension()
        
        try:
            import Vibroeffects as Vibroeffects
            Vibroeffects.VibroManager.g_instance = Vibroeffects.VibroManager.VibroManager()
            Vibroeffects.VibroManager.g_instance.connect()
        except:
            LOG_CURRENT_EXCEPTION()

        AOGAS.init()
        tutorialLoaderInit()
        BigWorld.callback(0.1, asyncore_call)
        messengerGUI.init()
        SystemMessagesInterface = SystemMessagesInterface
        import gui.Scaleform
        SystemMessages.g_instance = SystemMessagesInterface.SystemMessagesInterface()
        SystemMessages.g_instance.init()
        import items as items
        items.init(False)
        import ArenaType as ArenaType
        ArenaType.init()
        import dossiers as dossiers
        dossiers.init()
        ParametersCache = ParametersCache
        import gui.Scaleform.utils
        ParametersCache.g_instance.init()
        BigWorld.worldDrawEnabled(False)
        if loadingScreenGUI:
            loadingScreenGUI.script.active(False)
        
        AreaDestructibles.init()
        MusicController.init()
        g_postProcessing.init()
        import LcdKeyboard as LcdKeyboard
        LcdKeyboard.enableLcdKeyboardSpecificKeys(True)
        
        try:
            LightManager = LightManager
            import LightFx
            LightManager.g_instance = LightManager.LightManager()
            import AuxiliaryFx as AuxiliaryFx
            AuxiliaryFx.g_instance = AuxiliaryFx.AuxiliaryFxManager()
        except:
            LOG_CURRENT_EXCEPTION()

    except Exception:
        LOG_CURRENT_EXCEPTION()
        BigWorld.quit()



def start():
    LOG_DEBUG('start')
    connectionManager.onConnected += onConnected
    connectionManager.onDisconnected += onDisconnected
    messengerGUI.start()
    if len(sys.argv) > 2:
        if sys.argv[1] == 'offlineTest':
            
            try:
                TestArena2Object = TestArena2Object
                import cat.tasks.TestArena2
                LOG_DEBUG(sys.argv)
                LOG_DEBUG('starting offline test: %s', sys.argv[2])
                if len(sys.argv) > 3:
                    TestArena2Object.startOffline(sys.argv[2], sys.argv[3])
                else:
                    TestArena2Object.startOffline(sys.argv[2])
            LOG_DEBUG('Game start FAILED with:')
            LOG_CURRENT_EXCEPTION()

        elif sys.argv[1] == 'validationTest':
            
            try:
                g_windowsManager.start()
                LOG_DEBUG('starting validationTest')
                import Cat as Cat
                Cat.Tasks.Validation.ParamsObject.setResultFileName(sys.argv[2])
                BigWorld.callback(10, Cat.Tasks.Validation.startAllValidationTests)
            LOG_DEBUG('Game start FAILED with:')
            LOG_CURRENT_EXCEPTION()

        elif sys.argv[1] == 'resourcesValidationTest':
            
            try:
                g_windowsManager.start()
                LOG_DEBUG('starting resourcesValidationTest')
                import Cat as Cat
                Cat.Tasks.Validation.ParamsObject.setResultFileName(sys.argv[2])
                BigWorld.callback(10, Cat.Tasks.Validation.startResourcesValidationTest)
            LOG_DEBUG('Game start FAILED with:')
            LOG_CURRENT_EXCEPTION()

        
    else:
        g_windowsManager.start()
    
    try:
        import Vibroeffects
        Vibroeffects.VibroManager.g_instance.start()
    except:
        LOG_CURRENT_EXCEPTION()

    
    try:
        import LightFx
        LightFx.LightManager.g_instance.start()
        import AuxiliaryFx
        AuxiliaryFx.g_instance.start()
    except:
        LOG_CURRENT_EXCEPTION()



def fini():
    global g_replayCtrl
    LOG_DEBUG('fini')
    BigWorld.wg_setScreenshotNotifyCallback(None)
    g_critMemHandler.restore()
    g_critMemHandler.destroy()
    if constants.IS_CAT_LOADED:
        import Cat
        Cat.fini()
    
    MusicController.g_musicController.destroy()
    connectionManager.onConnected -= onConnected
    connectionManager.onDisconnected -= onDisconnected
    messengerGUI.fini()
    g_postProcessing.fini()
    EdgeDetectColorController = EdgeDetectColorController
    import helpers
    if EdgeDetectColorController.g_instance is not None:
        EdgeDetectColorController.g_instance.destroy()
        EdgeDetectColorController.g_instance = None
    
    BigWorld.resetEntityManager(False, False)
    BigWorld.clearAllSpaces()
    Waiting = Waiting
    import gui.Scaleform.Waiting
    Waiting.close()
    g_windowsManager.destroy()
    SystemMessages.g_instance.destroy()
    AOGAS.fini()
    tutorialLoaderFini()
    g_currentVehicle.cleanup()
    import LcdKeyboard
    LcdKeyboard.finalize()
    import Vibroeffects
    if Vibroeffects.VibroManager.g_instance is not None:
        Vibroeffects.VibroManager.g_instance.destroy()
        Vibroeffects.VibroManager.g_instance = None
    
    if g_replayCtrl is not None:
        g_replayCtrl.stop()
        g_replayCtrl = None
        import BattleReplay
        BattleReplay.g_replayCtrl = None
    
    LightManager = LightManager
    import LightFx
    if LightManager.g_instance is not None:
        LightManager.g_instance.destroy()
        LightManager.g_instance = None
    
    import AuxiliaryFx
    if AuxiliaryFx.g_instance is not None:
        AuxiliaryFx.g_instance.destroy()
        AuxiliaryFx.g_instance = None
    
    g_preDefinedHosts = g_preDefinedHosts
    import predefined_hosts
    if g_preDefinedHosts is not None:
        g_preDefinedHosts.fini()
    
    g_clientUpdateManager = g_clientUpdateManager
    import gui.ClientUpdateManager
    if g_clientUpdateManager is not None:
        g_clientUpdateManager.dispose()
    
    voipRespHandler = VOIP.getResponseHandler()
    if voipRespHandler is not None:
        VOIP.getResponseHandler().destroy()
    
    Settings.g_instance.save()


def onChangeEnvironments(inside):
    LOG_DEBUG('onChangeEnvironments')


def onRecreateDevice():
    LOG_DEBUG('onRecreateDevice')
    for c in g_guiResetters:
        
        try:
            c()
        continue
        except Exception:
            LOG_CURRENT_EXCEPTION()
            continue
        

    


def onStreamComplete(id, desc, data):
    player = BigWorld.player()
    if player is None:
        LOG_ERROR('onStreamComplete: no player entity available for process stream (%d, %s) data' % (id, desc))
    else:
        player.onStreamComplete(id, data)


def onConnected():
    VOIP.getResponseHandler().onConnected()


def onDisconnected():
    g_currentVehicle.firstTimeInitialized = False
    g_currentVehicle.reset(True)
    VOIP.getResponseHandler().logout()
    VOIP.getResponseHandler().unsubscribeChatActions()
    VoiceChatInterface.g_instance.reset()


def handleCharEvent(char, key, mods):
    char = unicode(char.encode('iso8859'), CLIENT_ENCODING)
    if GUI.handleCharEvent(char, key, mods):
        return True
    return False


def handleAxisEvent(event):
    return False


def handleKeyEvent(event):
    (isDown, key, mods, isRepeat) = convertKeyEvent(event)
    if isRepeat:
        if onRepeatKeyEvent(event):
            return True
    
    if g_replayCtrl.isPlaying:
        if g_replayCtrl.handleKeyEvent(isDown, key, mods, isRepeat, event):
            return True
    
    if constants.IS_CAT_LOADED:
        import Cat
        if Cat.handleKeyEventBeforeGUI(isDown, key, mods, event):
            return True
    
    if not isRepeat:
        InputHandler.g_instance.handleKeyEvent(event)
        if GUI.handleKeyEvent(event):
            return True
    
    if constants.IS_CAT_LOADED:
        import Cat
        if Cat.handleKeyEventAfterGUI(isDown, key, mods, event):
            return True
    
    if not isRepeat:
        if MessengerDispatcher.g_instance.editing():
            return True
    
    inputHandler = getattr(BigWorld.player(), 'inputHandler', None)
    if inputHandler is not None:
        if inputHandler.handleKeyEvent(event):
            return True
    
    return False


def handleMouseEvent(event):
    (dx, dy, dz, cursorPos) = convertMouseEvent(event)
    if constants.IS_CAT_LOADED:
        import Cat
        if Cat.handleMouseEvent(dx, dy, dz):
            return True
    
    if Disconnect.getWindow() is not None:
        Disconnect.getWindow().handleMouseEvent(event)
        return True
    if g_replayCtrl.isPlaying:
        if g_replayCtrl.handleMouseEvent(dx, dy, dz):
            return True
    
    if GUI.handleMouseEvent(event):
        return True
    inputHandler = getattr(BigWorld.player(), 'inputHandler', None)
    if inputHandler is None:
        return False
    return inputHandler.handleMouseEvent(dx, dy, dz)


def handleInputLangChangeEvent():
    return False


def addChatMsg(*msg):
    print 'Message:', msg

_PYTHON_MACROS = {
    'p': 'BigWorld.player()',
    't': 'BigWorld.target()',
    'B': 'BigWorld',
    'v': 'BigWorld.entities[BigWorld.player().playerVehicleID]',
    'b': 'BigWorld.player().addBotToArena',
    'w': 'import Weather; Weather.weather().summon',
    'cam_pos': 'BigWorld.player().inputHandler._AvatarInputHandler__curCtrl.setCameraPosition',
    'gc': 'import gc; gc.set_debug(gc.DEBUG_LEAK | gc.DEBUG_STATS);gc.collect(2)',
    'gcd': 'import gc; gc.set_debug(gc.DEBUG_LEAK | gc.DEBUG_STATS);from debug_utils import dump_garbage; dump_garbage()',
    'connect': 'ls=game.LanServers();ls.searchAndConnect',
    'create': 'BigWorld.player().createArena',
    'list': 'alr = game.ArenaListRequester',
    'start': 'BigWorld.player().startArena',
    'join': 'BigWorld.player().joinArena',
    'leave': 'BigWorld.player().leaveArena',
    'cv': 'import vehicles_check;vehicles_check.check',
    'chat': 'from messenger.gui.MessengerDispatcher import g_instance;g_instance',
    'battleUI': 'from gui.WindowsManager import g_windowsManager; g_windowsManager.battleWindow',
    'tutorial': 'from tutorial import TutorialLoader; TutorialLoader.g_loader.tutorial',
    'sf_player': 'from gui.Scaleform.development import sf_player_test; sf_player_test',
    'page': 'from gui.WindowsManager import g_windowsManager; page = g_windowsManager.window._CommonPage__mainInterface',
    'stats': 'from gui.WindowsManager import g_windowsManager; g_windowsManager.window.battleResults.onBattleResultsShow(1, 0)' }

def expandMacros(line):
    import re as re
    patt = '\\$(' + reduce((lambda x, y: x + '|' + y), _PYTHON_MACROS.iterkeys()) + ')(\\W|\\Z)'
    
    def repl(match):
        return _PYTHON_MACROS[match.group(1)] + match.group(2)

    return re.sub(patt, repl, line)


def wg_onChunkLoad(spaceID, chunkID, numDestructibles, isOutside):
    if not isOutside:
        return None
    if spaceID != AreaDestructibles.g_destructiblesManager.getSpaceID():
        AreaDestructibles.g_destructiblesManager.startSpace(spaceID)
    
    AreaDestructibles.g_destructiblesManager.onChunkLoad(chunkID, numDestructibles)


def wg_onChunkLoose(spaceID, chunkID, isOutside):
    if not isOutside:
        return None
    if spaceID == AreaDestructibles.g_destructiblesManager.getSpaceID():
        AreaDestructibles.g_destructiblesManager.onChunkLoose(chunkID)
    


def convertKeyEvent(event):
    isDown = event.isKeyDown()
    key = event.key
    isRepeat = event.isRepeatedEvent()
    if event.isShiftDown():
        pass
    1
    if event.isCtrlDown():
        pass
    1
    if event.isAltDown():
        pass
    1
    mods = 0
    return (isDown, key, mods, isRepeat)


def convertMouseEvent(event):
    return (event.dx, event.dy, event.dz, event.cursorPosition)


def onRepeatKeyEvent(event):
    safeCopy = frozenset(g_repeatKeyHandlers)
    processed = False
    for handler in safeCopy:
        
        try:
            processed = handler(event)
            if processed:
                break
        continue
        except Exception:
            LOG_CURRENT_EXCEPTION()
            continue
        

    
    safeCopy = None
    return processed


def onMemoryCritical():
    g_critMemHandler()


def asyncore_call():
    
    try:
        asyncore.loop(count = 1)
    except:
        LOG_CURRENT_EXCEPTION()

    BigWorld.callback(0.1, asyncore_call)


