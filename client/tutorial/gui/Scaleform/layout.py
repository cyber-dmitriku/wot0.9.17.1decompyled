# Source Generated with Decompyle++
# File: layout.pyc (Python 2.6)

import GUI
import weakref
from gui import WindowsManager, SystemMessages
from gui.Scaleform.Waiting import Waiting
from gui.Scaleform.windows import UIInterface
from tutorial.gui import GUIProxy, GUIEvent
from tutorial.gui.Scaleform.TutorialConfig import TutorialConfig
from tutorial.gui.Scaleform.TutorialDispatcher import TutorialDispatcher
from tutorial.logger import LOG_ERROR, LOG_WARNING, LOG_DEBUG, LOG_CURRENT_EXCEPTION
TUTORIAL_LAYOUT_FILE = 'TutorialLayout.swf'

class TutorialUILoader(object):
    
    def __init__(self, handler):
        super(TutorialUILoader, self).__init__()
        self._loader = None
        self._handler = handler

    
    def __del__(self):
        LOG_DEBUG('TutorialUILoader deleted')

    
    def init(self, ui):
        loader = ui.getMember('tutorialLoader')
        if loader is None:
            LOG_ERROR('Tutorial loader not found')
            return None
        self._loader = loader
        self._loader.script = self

    
    def fini(self):
        if self._loader is not None:
            self._loader.script = None
        
        self._loader = None
        self._handler = None

    
    def load(self):
        if self._loader is None:
            return False
        result = True
        
        try:
            self._loader.loadTutorial(TUTORIAL_LAYOUT_FILE)
            LOG_DEBUG('UILoader.load:', TUTORIAL_LAYOUT_FILE)
        except AttributeError:
            self._loader is None
            result = False
        except:
            self._loader is None

        return result

    
    def unload(self):
        if self._loader is None:
            return False
        result = True
        
        try:
            self._loader.unloadTutorial()
            LOG_DEBUG('UILoader.unload:', TUTORIAL_LAYOUT_FILE)
        except AttributeError:
            self._loader is None
            result = False
        except:
            self._loader is None

        return result

    
    def gc_onLoadComplete(self, movieView):
        LOG_DEBUG('gc_onLoadComplete', movieView)
        self._handler._setMovieView(movieView)

    
    def gc_getScreenSize(self):
        LOG_DEBUG('gc_getScreenSize')
        return GUI.screenResolution()



class TutorialLayout(GUIProxy, UIInterface):
    
    def __init__(self):
        super(TutorialLayout, self).__init__()
        self.config = TutorialConfig()
        self.loader = TutorialUILoader(weakref.proxy(self))
        self._guiRef = None
        self._dispatcherRef = None
        self._movieView = None

    
    def __del__(self):
        LOG_DEBUG('TutorialLayout deleted')

    
    def populateUI(self, proxy):
        super(TutorialLayout, self).populateUI(proxy)
        self.loader.init(proxy)
        self.uiHolder.addExternalCallbacks({
            'Loader.LoadStart': self._TutorialLayout__dispatchPageChangingEvent })

    
    def dispossessUI(self):
        self.loader.fini()
        self.uiHolder.removeExternalCallback('Loader.LoadStart', function = self._TutorialLayout__dispatchPageChangingEvent)
        super(TutorialLayout, self).dispossessUI()

    
    def init(self):
        
        try:
            window = WindowsManager.g_windowsManager.window
            self._guiRef = weakref.ref(window)
            proxy = window.proxy
            dispatcher = window.tutorialDispatcher
            if dispatcher is None:
                dispatcher = TutorialDispatcher()
                dispatcher.populateUI(proxy)
                window.tutorialDispatcher = dispatcher
            
            self._dispatcherRef = weakref.ref(dispatcher)
        except AttributeError:
            LOG_CURRENT_EXCEPTION()
            return False

        self.populateUI(proxy)
        if not self.loader.load():
            return False
        self.setTrainingRunMode()
        self.call('common.closeAllWindows')
        return True

    
    def _setMovieView(self, movie):
        if self._movieView is not None:
            self._movieView.script = None
        
        self._movieView = movie
        self._movieView.script = self
        self.onGUILoaded()

    
    def clear(self):
        if self._guiRef is not None and self._guiRef() is not None:
            self.clearChapterInfo()
            if self._movieView is not None:
                self._movieView.clearStage()
            
            self.call('common.closeAllWindows')
        

    
    def fini(self):
        self.eManager.clear()
        if self._guiRef is None or self._guiRef() is None:
            return None
        self.loader.unload()
        if self._movieView is not None:
            self._movieView.script = None
            self._movieView = None
        
        self.call('common.closeAllWindows')
        self.dispossessUI()

    
    def loadConfig(self, filePath):
        self.config.loadConfig(filePath)

    
    def reloadConfig(self, filePath):
        self.config.reloadConfig(filePath)

    
    def updateLockedAreas(self, areas):
        getter = self.config.getArea
        data = []
        for area in areas:
            areaID = area.getID()
            props = getter(areaID)
            if props['path'] is None:
                LOG_ERROR('Target path for locked area not found ', areaID)
                continue
            
            props['areaID'] = areaID
            data.append(props)
        
        self._movieView.areas.updateLockedAreas(data)

    
    def updateActiveAreas(self, areas):
        areaGetter = self.config.getArea
        itemGetter = self.config.getItem
        data = []
        for area in areas:
            areaID = area.getID()
            props = areaGetter(area.getID())
            path = props['path']
            targetID = props['targetID']
            if path is None or targetID is None:
                targetID = area.getTargetID()
                item = itemGetter(targetID)
                if item is not None:
                    path = item['path']
                else:
                    LOG_ERROR('Target path for active area not found', areaID)
            
            if targetID is None or path is None:
                LOG_WARNING('Target path or ID for active area not found', areaID, targetID, path)
                continue
            
            props.update({
                'areaID': areaID,
                'targetID': targetID,
                'path': path,
                'useMask': area.isUseMask(),
                'maskMode': area.getHideMaskMode(),
                'actionType': 0 })
            action = area.getAction(targetID)
            if action is not None:
                props['actionType'] = action.getType()
            
            data.append(props)
        
        self._movieView.areas.updateActiveAreas(data)

    
    def getSceneID(self):
        result = None
        if not Waiting.isVisible():
            guiPage = self.uiHolder.currentInterface
            result = self.config.getSceneID(guiPage)
        
        return result

    
    def goToScene(self, sceneID):
        method = self.config.getGoToSceneMethod(sceneID)
        if method is not None:
            self.uiHolder.movie.invoke((method,))
        

    
    def playEffect(self, effectName, args, itemRef = None, containerRef = None):
        if itemRef is not None:
            item = self.config.getItem(itemRef)
            if item is None:
                LOG_ERROR('GUI Item not found', effectName, itemRef)
                return None
            if args is None:
                args = []
            
            args.append(item['path'])
        
        if containerRef is not None:
            container = self.config.getItem(containerRef)
            if container is None:
                LOG_ERROR('GUI Item not found', effectName, containerRef)
                return None
            if args is None:
                args = []
            
            args.append(container['path'])
        
        self._movieView.effects.play(effectName, args)

    
    def stopEffect(self, effectName, effectID):
        self._movieView.effects.stop(effectName, effectID)

    
    def showWaiting(self, messageID, isSingle = False):
        Waiting.show('tutorial-{0:>s}'.format(messageID), isSingle = isSingle)

    
    def hideWaiting(self, messageID):
        if Waiting.isVisible():
            Waiting.hide('tutorial-{0:>s}'.format(messageID))
        

    
    def showErrorMessage(self, key, *args, **kwargs):
        kwargs['type'] = SystemMessages.SM_TYPE.Error
        SystemMessages.g_instance.pushI18nMessage(key, *args, **args)

    
    def setItemProps(self, itemRef, props, revert = False):
        item = self.config.getItem(itemRef)
        if item is None:
            LOG_ERROR('GUI Item not found', itemRef)
            return None
        self._movieView.items.setProps(itemRef, item['path'], props, revert)

    
    def isGuiDialogDisplayed(self):
        return self._movieView.isGuiDialogOnStage()

    
    def isTutorialDialogDisplayed(self, dialogID):
        return self._movieView.isTutorialDialogOnStage(dialogID)

    
    def findItem(self, itemID, criteria):
        itemPath = None
        if criteria is None:
            item = self.config.getItem(itemID)
            locked = True
            valuePath = None
            value = None
        else:
            (parentID, valuePath, value) = criteria
            item = self.config.getItem(parentID)
            locked = False
        itemPath = self._movieView.findTargetByCriteria(item['path'], valuePath, value)
        if not locked:
            if itemPath is not None:
                self.config.addItem(itemID, itemPath)
            else:
                self.config.removeItem(itemID)
        
        return itemPath

    
    def invokeCommand(self, command):
        (name, args) = command
        self.uiHolder.call(name, args[:])

    
    def getGuiRoot(self):
        
        try:
            root = WindowsManager.g_windowsManager.window
        except AttributeError:
            LOG_CURRENT_EXCEPTION()
            root = None

        return root

    
    def defineDispatcher(cls):
        dispatcher = None
        
        try:
            window = WindowsManager.g_windowsManager.window
            dispatcher = getattr(window, 'tutorialDispatcher', None)
            if dispatcher is None and window is not None:
                dispatcher = TutorialDispatcher()
                dispatcher.populateUI(window.proxy)
                window.tutorialDispatcher = dispatcher
        except AttributeError:
            LOG_CURRENT_EXCEPTION()

        return dispatcher

    defineDispatcher = classmethod(defineDispatcher)
    
    def setChapterInfo(self, title, description):
        if self._dispatcherRef() is not None:
            self._dispatcherRef().setChapterInfo(title, description)
        else:
            LOG_ERROR('Tutorial dispatcher is not defined.')

    
    def clearChapterInfo(self):
        if self._dispatcherRef() is not None:
            self._dispatcherRef().clearChapterInfo()
        else:
            LOG_ERROR('Tutorial dispatcher is not defined.')

    
    def setTrainingRestartMode(self):
        if self._dispatcherRef() is not None:
            self._dispatcherRef().setTrainingRestartMode()
        else:
            LOG_ERROR('Tutorial dispatcher is not defined.')

    
    def setTrainingRunMode(self):
        if self._dispatcherRef() is not None:
            self._dispatcherRef().setTrainingRunMode()
        else:
            LOG_ERROR('Tutorial dispatcher is not defined.')

    
    def _TutorialLayout__dispatchPageChangingEvent(self, _, pageName):
        sceneID = self.config.getSceneID(pageName)
        if sceneID is None:
            self.clear()
            LOG_WARNING('Scene alias not found, page:', pageName)
        elif self._movieView is not None:
            self._movieView.effects.stopAll()
            self.onPageChanging(sceneID)
        

    
    def gc_proxyMouseClick(self, targetID):
        self.onMouseClicked(GUIEvent(None, targetID))



