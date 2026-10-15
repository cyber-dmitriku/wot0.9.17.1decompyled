# Source Generated with Decompyle++
# File: TutorialDispatcher.pyc (Python 2.6)

from debug_utils import LOG_DEBUG
from gui.Scaleform.windows import UIInterface
from tutorial.gui import GUIDispatcher

class TutorialDispatcher(GUIDispatcher, UIInterface):
    
    def __init__(self):
        super(TutorialDispatcher, self).__init__()
        self._isPopulated = False

    
    def __del__(self):
        LOG_DEBUG('TutorialDispatcher deleted')

    
    def populateUI(self, proxy):
        super(TutorialDispatcher, self).populateUI(proxy)
        self.uiHolder.addFsCallbacks({
            'Tutorial.Dispatcher.Refuse': self._TutorialDispatcher__gfx_onRefuseTraining,
            'Tutorial.Dispatcher.Restart': self._TutorialDispatcher__gfx_onRestartTraining })
        self._subscribe()
        self._isPopulated = True
        self.call('SetDisabled', [
            self._isDisabled])

    
    def dispossessUI(self):
        self._isPopulated = False
        self.uiHolder.removeFsCallbacks('Tutorial.Dispatcher.Refuse', 'Tutorial.Dispatcher.Restart')
        self._unsubscribe()
        super(TutorialDispatcher, self).dispossessUI()

    
    def setChapterInfo(self, title, description):
        self.call('SetChapterInfo', [
            title,
            description])

    
    def clearChapterInfo(self):
        self.call('ClearChapterInfo')

    
    def setTrainingRestartMode(self):
        super(TutorialDispatcher, self).setTrainingRestartMode()
        self.call('SetRestartMode')

    
    def setTrainingRunMode(self):
        super(TutorialDispatcher, self).setTrainingRunMode()
        self.call('SetRunMode')

    
    def setDisabled(self, disabled):
        super(TutorialDispatcher, self).setDisabled(disabled)
        self.call('SetDisabled', [
            disabled])

    
    def call(self, methodName, args = None):
        if self._isPopulated:
            super(TutorialDispatcher, self).call('Tutorial.Dispatcher.{0:>s}'.format(methodName), args = args)
        

    
    def _TutorialDispatcher__gfx_onRefuseTraining(self, _):
        self.refuseTraining()

    
    def _TutorialDispatcher__gfx_onRestartTraining(self, _):
        self.restartTraining()



