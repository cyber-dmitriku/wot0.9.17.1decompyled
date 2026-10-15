# Source Generated with Decompyle++
# File: __init__.pyc (Python 2.6)

from AccountCommands import RES_TUTORIAL_DISABLED
import BigWorld
from tutorial import doc_loader
from tutorial import settings
from tutorial.control import setTutorialProxy, clearTutorialProxy
from tutorial.control import states, summary
from tutorial.control import functional
from tutorial.data import chapter
from tutorial.logger import LOG_WARNING, LOG_ERROR, LOG_DEBUG
import weakref

class INITIAL_FLAG(object):
    GUI_LOADED = 1
    CHAPTER_RESOLVED = 2
    INITIALIZED = GUI_LOADED | CHAPTER_RESOLVED


class Tutorial(object):
    
    def __init__(self):
        super(Tutorial, self).__init__()
        self._cache = None
        self._Tutorial__callbackID = None
        self._currentChapter = None
        self._currentState = None
        self._descriptor = doc_loader.loadDescriptorData()
        self._data = None
        self._tutorialStopped = True
        self._nextChapter = False
        self._nextScene = None
        self._funcScene = None
        self._funcInfo = None
        self._flags = None
        self._vars = None
        self._effectsQueue = []
        self._gui = None
        self._bonusCompleted = 0
        self._initialized = 0

    
    def __del__(self):
        LOG_DEBUG('Tutorial deleted')

    
    def run(self, ctx):
        self._cache = ctx.get('cache', None)
        if self._cache is None:
            LOG_ERROR('Cache is not init.')
            return None
        self._bonusCompleted = ctx.get('bonusCompleted', 0)
        if not self._tutorialStopped:
            LOG_ERROR('Tutorial is already running.')
            return None
        self._gui = settings.TUTORIAL_GUI_CLASS()
        self._gui.onGUILoaded += self._Tutorial__onGUILoaded
        if not self._gui.init():
            self._gui.onGUILoaded -= self._Tutorial__onGUILoaded
            LOG_ERROR('GUI can not init. Tutorial is stopping.')
            return None
        LOG_DEBUG('Start training', ctx)
        self._tutorialStopped = False
        proxy = weakref.proxy(self)
        setTutorialProxy(proxy)
        if self._Tutorial__resolveInitialChapter(ctx):
            self._cache.setAfterBattle(ctx.get('afterBattle', False))
            self._gui.loadConfig(self._descriptor.getGuiFilePath())
            self._gui.onMouseClicked += self._Tutorial__onMouseClicked
            self._gui.onPageChanging += self._Tutorial__onPageChanging
            self._Tutorial__tryRunFirstState(INITIAL_FLAG.CHAPTER_RESOLVED)
        

    
    def stop(self, finished = False):
        if self._tutorialStopped:
            return None
        if self._Tutorial__callbackID is not None:
            BigWorld.cancelCallback(self._Tutorial__callbackID)
            self._Tutorial__callbackID = None
        
        if finished:
            self._cache.setTrainingFinished(True)
        elif self._flags:
            pass
        
        None(self._tutorialStopped, None)
        self._cache = None
        if self._data is not None:
            self._data.clear()
        
        self._gui.fini()
        self._gui = None
        clearTutorialProxy()
        self.removeEffectsInQueue()
        self._nextChapter = False
        self._tutorialStopped = True
        self._initialized = 0

    
    def refuse(self):
        title = self._data.getTitle()
        description = self._data.getDescription(afterBattle = self._cache.isAfterBattle())
        self._cache.setTrainingRefused(True)
        self.stop()
        dispatcher = settings.TUTORIAL_GUI_CLASS.defineDispatcher()
        dispatcher.setTrainingRestartMode()
        dispatcher.setChapterInfo(title, description)

    
    def pause(self, ctx):
        self._cache = ctx.get('cache', None)
        if self._cache is None:
            LOG_ERROR('Cache is not init.')
            return None
        self._bonusCompleted = ctx.get('bonusCompleted', 0)
        if self._Tutorial__resolveInitialChapter(ctx):
            dispatcher = settings.TUTORIAL_GUI_CLASS.defineDispatcher()
            chapter = self._descriptor.getChapter(self._currentChapter)
            dispatcher.setTrainingRestartMode()
            dispatcher.setChapterInfo(chapter.getTitle(), chapter.getDescription(afterBattle = self._cache.isAfterBattle()))
        
        self._cache = None

    
    def restart(self, ctx):
        if 'cache' in ctx:
            ctx['cache'].setTrainingRefused(False)
        
        self.run(ctx)

    
    def _Tutorial__timeLoop(self):
        self._Tutorial__callbackID = None
        if not self._tutorialStopped:
            self._tick()
            self._Tutorial__callbackID = BigWorld.callback(0.1, self._Tutorial__timeLoop)
        

    
    def _tick(self):
        if not self._nextChapter:
            self._currentState._tick()
        else:
            self.loadCurrentChapter()

    
    def _Tutorial__resolveInitialChapter(self, ctx):
        self._currentChapter = None
        allBonuses = self._descriptor.getAllBonuses()
        if self._bonusCompleted and not (self._bonusCompleted & allBonuses):
            LOG_ERROR('It is not possible to determine the current chapter. Tutorial is stopping', self._bonusCompleted, allBonuses)
            self.stop()
            return False
        fromCache = self._cache.currentChapter()
        if fromCache is not None:
            chapter = self._descriptor.getChapter(fromCache)
            if self._descriptor.isChapterInitial(chapter, self._bonusCompleted):
                self._currentChapter = fromCache
                if not ctx['afterBattle']:
                    ctx['afterBattle'] = self._cache.isAfterBattle()
                
            else:
                self._cache.setAfterBattle(False, flush = False)
                self._cache.clearChapterData(flush = False)
                if chapter is not None:
                    pass
                1
                'Initial chapter not found in cache or bonuses is invalid'(fromCache, chapter.getBonusID(), None, self._bonusCompleted)
        
        if self._currentChapter is None:
            self._currentChapter = self._descriptor.getInitialChapterID(bonusCompleted = self._bonusCompleted)
        
        if self._currentChapter is None:
            LOG_ERROR('Initial chapter not found. Tutorial is stopping')
            self.stop()
            return False
        return True

    
    def _Tutorial__tryRunFirstState(self, next):
        self._initialized |= next
        if self._initialized == INITIAL_FLAG.INITIALIZED:
            self._currentState = states.TutorialStateLoading()
            self._currentState._tick()
            self.loadCurrentChapter()
            self._Tutorial__timeLoop()
        

    
    def loadCurrentChapter(self):
        afterBattle = self._cache.isAfterBattle()
        LOG_DEBUG('Chapter is loading', self._currentChapter, afterBattle)
        self._gui.showWaiting('chapter-loading', isSingle = True)
        if self._data is not None:
            self._data.clear()
        
        chapter = self._descriptor.getChapter(self._currentChapter)
        self._data = doc_loader.loadChapterData(chapter, afterBattle = afterBattle)
        if self._data is None:
            LOG_ERROR('Chapter documentation is not valid. Tutorial is stopping', self._currentChapter)
            self._gui.hideWaiting('chapter-loading')
            self.stop()
            return None
        self._flags = summary.FlagSummary(self._data.getFlags(), initial = self._cache.flags())
        self._vars = summary.VarSummary(self._data.getVarSets())
        self._funcInfo = functional.FunctionalChapterInfo(self._data.getInfoConditions())
        self._funcInfo.update()
        self._nextScene = self._data.getInitialScene()
        self._currentState = states.TutorialStateNextScene()
        LOG_DEBUG('Set new state TutorialStateNextScene', self._nextScene.getID())
        self._nextChapter = False
        self._gui.hideWaiting('chapter-loading')

    
    def requestForBonus(self):
        if not self._data.hasBonus():
            LOG_ERROR('Chapter has not bonus.')
            return None
        if self._data.isBonusReceived(self._bonusCompleted):
            LOG_ERROR('Bonus already received.')
            return None
        bonusID = self._data.getBonusID()
        self._isBonusReceived = False
        waitingID = self._data.getBonusMessage()
        if not len(waitingID):
            waitingID = 'request-bonus'
        
        self._gui.showWaiting(waitingID)
        self._data.hasBonus()((self._data.isBonusReceived(self._bonusCompleted), BigWorld.player().completeTutorial, bonusID), (lambda resultID: self._Tutorial__cb_onCompleteTutorial(bonusID, waitingID, resultID)))

    
    def setState(self, stateID):
        state = states.factory(stateID)
        if state is not None:
            LOG_DEBUG('Set new state', state.__name__)
            self._currentState = state()
        else:
            LOG_ERROR('Can not sets current state', stateID)

    
    def evaluateState(self):
        if len(self._effectsQueue):
            if not isinstance(self._currentState, states.TutorialStateRunEffects):
                self.setState(states.STATE_RUN_EFFECTS)
            
        else:
            self.setState(states.STATE_LEARNING)

    
    def getFirstElementOfTop(self):
        result = None
        if len(self._effectsQueue):
            top = self._effectsQueue[0]
            if not len(top):
                self._effectsQueue.pop(0)
                if len(self._effectsQueue):
                    top = self._effectsQueue[0]
                
            
            if len(top):
                result = top.pop(0)
            
        
        return result

    
    def storeEffectsInQueue(self, effects, benefit = False):
        if effects is None or len(effects) == 0:
            LOG_ERROR('Effect list is not defined')
        elif benefit:
            self._effectsQueue.insert(0, effects)
        else:
            self._effectsQueue.append(effects)
        if self._currentState.allowedToSwitch():
            self.setState(states.STATE_RUN_EFFECTS)
        

    
    def removeEffectsInQueue(self):
        self._effectsQueue = []

    
    def getFlags(self):
        return self._flags

    
    def getVars(self):
        return self._vars

    
    def invalidateFlags(self):
        self._funcInfo.update()
        if self._funcScene is not None:
            self._funcScene._sceneToBeUpdated = True
        

    
    def goToNextChapter(self, chapterID):
        self._cache.clearChapterData()
        self.removeEffectsInQueue()
        self._currentChapter = chapterID
        self._nextChapter = True

    
    def getNextScene(self):
        return self._nextScene

    
    def getFunctionalScene(self):
        return self._funcScene

    
    def setFunctionalScene(self, scene):
        self._funcScene = scene

    
    def _Tutorial__onGUILoaded(self):
        self._Tutorial__tryRunFirstState(INITIAL_FLAG.GUI_LOADED)

    
    def _Tutorial__onMouseClicked(self, event):
        self._currentState.mouseClicked(event)

    
    def _Tutorial__onPageChanging(self, sceneID):
        if self._nextScene.getID() == sceneID:
            return None
        scene = self._data.getScene(sceneID)
        if scene is None:
            LOG_WARNING('Scene {0:>s} not found in chapter {1:>s}'.format(sceneID, self._currentChapter))
            return None
        self._nextScene = scene
        self.setState(states.STATE_WAIT_SCENE)

    
    def _Tutorial__cb_onCompleteTutorial(self, bonusID, waitingID, resultID):
        if not self._tutorialStopped:
            self._gui.hideWaiting(waitingID)
        
        self._isBonusReceived = True
        if resultID < 0:
            LOG_ERROR('Server return error on request completeTutorial.', resultID)
            if resultID == RES_TUTORIAL_DISABLED:
                errorKey = '#tutorial:messages/tutorial-disabled'
            else:
                errorKey = '#tutorial:messages/request-bonus-failed'
            self._gui.showErrorMessage(errorKey)
            self.stop()
            return None
        LOG_DEBUG('Received bonus', bonusID)
        self._bonusCompleted |= 1 << bonusID

    
    def _reload(self, ab = False):
        if not self._tutorialStopped:
            self._cache.setAfterBattle(ab)
            self._gui.reloadConfig(self._descriptor.getGuiFilePath())
            self._gui.clear()
            doc_loader.clearChapterData(self._data)
            self.loadCurrentChapter()
        else:
            LOG_DEBUG('Tutorial is not running.')

    
    def _showDialog(self, dialogID):
        if not self._tutorialStopped:
            self.storeEffectsInQueue(functional.factory([
                chapter.HasTargetEffect(dialogID, chapter.Effect.SHOW_DIALOG)]), benefit = True)
        else:
            LOG_DEBUG('Tutorial is not running.')



