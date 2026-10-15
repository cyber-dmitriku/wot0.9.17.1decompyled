# Source Generated with Decompyle++
# File: __init__.pyc (Python 2.6)

import BigWorld
from ConnectionManager import connectionManager
from CurrentVehicle import g_currentVehicle
from PlayerEvents import g_playerEvents
import Event
from debug_utils import LOG_ERROR

class GUIEvent(object):
    
    def __init__(self, type, targetID):
        super(GUIEvent, self).__init__()
        self.type = type
        self.targetID = targetID



class GUIProxy(object):
    eManager = Event.EventManager()
    onGUILoaded = Event.Event(eManager)
    onMouseClicked = Event.Event(eManager)
    onPageChanging = Event.Event(eManager)
    
    def init(self):
        pass

    
    def fini(self):
        pass

    
    def clear(self):
        pass

    
    def loadConfig(self, filePath):
        pass

    
    def reloadConfig(self, filePath):
        pass

    
    def updateLockedAreas(self, areas):
        pass

    
    def updateActiveAreas(self, areas):
        pass

    
    def getSceneID(self):
        pass

    
    def goToScene(self, sceneID):
        pass

    
    def playEffect(self, effectName, args, itemRef = None, containerRef = None):
        pass

    
    def stopEffect(self, effectName, effectID):
        pass

    
    def showWaiting(self, messageID, isSingle = False):
        pass

    
    def hideWaiting(self, messageID):
        pass

    
    def showErrorMessage(self, key, *args, **kwargs):
        pass

    
    def setItemProps(self, itemRef, props, revert = False):
        pass

    
    def isGuiDialogDisplayed(self):
        return False

    
    def isTutorialDialogDisplayed(self, dialogID):
        return False

    
    def findItem(self, itemID, criteria):
        pass

    
    def invokeCommand(self, command):
        pass

    
    def getGuiRoot(self):
        pass

    
    def defineDispatcher(cls):
        pass

    defineDispatcher = classmethod(defineDispatcher)
    
    def setChapterInfo(self, title, description):
        pass

    
    def clearChapterInfo(self):
        pass

    
    def setTrainingRestartMode(self):
        pass

    
    def setTrainingRunMode(self):
        pass



class GUIDispatcher(object):
    DEFAULT_MODE = 0
    RUN_MODE = 1
    RESTART_MODE = 2
    
    def __init__(self):
        super(GUIDispatcher, self).__init__()
        self._mode = GUIDispatcher.DEFAULT_MODE
        self._isDisabled = False

    
    def _subscribe(self):
        self._validate(getattr(BigWorld.player(), 'prebattle', None) is not None)
        g_playerEvents.onAccountShowGUI += self._GUIDispatcher__pe_onAccountShowGUI
        g_playerEvents.onEnqueued += self._GUIDispatcher__pe_onEnqueued
        g_playerEvents.onDequeued += self._GUIDispatcher__pe_onDequeued
        g_playerEvents.onKickedFromQueue += self._GUIDispatcher__pe_onKickedFromQueue
        g_playerEvents.onPrebattleJoined += self._GUIDispatcher__pe_onPrebattleJoined
        g_playerEvents.onPrebattleLeft += self._GUIDispatcher__pe_onPrebattleLeft
        g_playerEvents.onKickedFromPrebattle += self._GUIDispatcher__pe_onKickedFromPrebattle
        connectionManager.onDisconnected += self._GUIDispatcher__cm_onDisconnected

    
    def _validate(self, inPrebattle):
        if inPrebattle:
            self.setDisabled(True)
        

    
    def _unsubscribe(self):
        g_playerEvents.onAccountShowGUI -= self._GUIDispatcher__pe_onAccountShowGUI
        g_playerEvents.onEnqueued -= self._GUIDispatcher__pe_onEnqueued
        g_playerEvents.onDequeued -= self._GUIDispatcher__pe_onDequeued
        g_playerEvents.onKickedFromQueue -= self._GUIDispatcher__pe_onKickedFromQueue
        g_playerEvents.onPrebattleJoined -= self._GUIDispatcher__pe_onPrebattleJoined
        g_playerEvents.onPrebattleLeft -= self._GUIDispatcher__pe_onPrebattleLeft
        g_playerEvents.onKickedFromPrebattle -= self._GUIDispatcher__pe_onKickedFromPrebattle
        connectionManager.onDisconnected -= self._GUIDispatcher__cm_onDisconnected

    
    def refuseTraining(self):
        if self._mode == GUIDispatcher.RUN_MODE:
            g_loader = g_loader
            import tutorial.TutorialLoader
            g_loader.refuse()
        else:
            LOG_ERROR('TUTORIAL. Tutorial is not run.', self._mode)

    
    def restartTraining(self):
        if self._mode == GUIDispatcher.RESTART_MODE:
            g_loader = g_loader
            import tutorial.TutorialLoader
            g_loader.restart()
        else:
            LOG_ERROR('TUTORIAL. Tutorial is not stopped.', self._mode)

    
    def setChapterInfo(self, title, description):
        pass

    
    def clearChapterInfo(self):
        pass

    
    def setDisabled(self, disabled):
        self._isDisabled = disabled

    
    def setTrainingRestartMode(self):
        self._mode = GUIDispatcher.RESTART_MODE

    
    def setTrainingRunMode(self):
        self._mode = GUIDispatcher.RUN_MODE

    
    def _GUIDispatcher__pe_onAccountShowGUI(self, ctx):
        self._validate(ctx.get('prebattleID') is not None)

    
    def _GUIDispatcher__pe_onEnqueued(self, *args):
        self.setDisabled(True)

    
    def _GUIDispatcher__pe_onDequeued(self, *args):
        self.setDisabled(False)

    
    def _GUIDispatcher__pe_onKickedFromQueue(self, *args):
        self.setDisabled(False)

    
    def _GUIDispatcher__pe_onPrebattleJoined(self, *args):
        self.setDisabled(True)

    
    def _GUIDispatcher__pe_onPrebattleLeft(self, *args):
        self.setDisabled(False)

    
    def _GUIDispatcher__pe_onKickedFromPrebattle(self, *args):
        self.setDisabled(False)

    
    def _GUIDispatcher__cm_onDisconnected(self):
        self.clearChapterInfo()



