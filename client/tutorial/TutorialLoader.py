# Source Generated with Decompyle++
# File: TutorialLoader.pyc (Python 2.6)

import BigWorld
from AccountCommands import RES_SUCCESS
from ConnectionManager import connectionManager
from constants import IS_TUTORIAL_ENABLED
from PlayerEvents import g_playerEvents
import dossiers
from functools import partial
from tutorial import Tutorial
from tutorial import TutorialCache
from tutorial.logger import LOG_ERROR

class _TutorialLoader(object):
    
    def __init__(self):
        super(_TutorialLoader, self).__init__()
        self._TutorialLoader__afterBattle = False
        self._TutorialLoader__tutorial = None

    
    def init(self):
        g_playerEvents.onAccountShowGUI += self._TutorialLoader__pe_onAccountShowGUI
        g_playerEvents.onAvatarBecomePlayer += self._TutorialLoader__pe_onAvatarBecomePlayer
        connectionManager.onDisconnected += self._TutorialLoader__cm_onDisconnected

    
    def fini(self):
        g_playerEvents.onAccountShowGUI -= self._TutorialLoader__pe_onAccountShowGUI
        g_playerEvents.onAvatarBecomePlayer -= self._TutorialLoader__pe_onAvatarBecomePlayer
        connectionManager.onDisconnected -= self._TutorialLoader__cm_onDisconnected
        if self._TutorialLoader__tutorial is not None:
            self._TutorialLoader__tutorial.stop()
        

    
    def tutorial(self):
        return self._TutorialLoader__tutorial

    tutorial = property(tutorial)
    
    def tryingToRun(self, restart = False, inPrebattle = False):
        cache = TutorialCache.TutorialCache(BigWorld.player().name)
        ctx = {
            'cache': cache,
            'afterBattle': self._TutorialLoader__afterBattle,
            'restart': restart,
            'inPrebattle': inPrebattle }
        self._TutorialLoader__afterBattle = False
        if not cache.isTrainingFinished() or restart:
            if self._TutorialLoader__tutorial is None:
                self._TutorialLoader__tutorial = Tutorial()
                if self._TutorialLoader__tutorial._descriptor is None:
                    LOG_ERROR('Tutorial descriptor is not valid. Tutorial is not available.')
                    return None
            
            BigWorld.player().stats.get('tutorialsCompleted', partial(self._TutorialLoader__cb_onGetTutorialsCompleted, ctx))
        

    
    def refuse(self):
        if self._TutorialLoader__tutorial is not None:
            self._TutorialLoader__tutorial.refuse()
        

    
    def restart(self):
        self.tryingToRun(restart = True)

    
    def _TutorialLoader__pe_onAccountShowGUI(self, ctx):
        self.tryingToRun(inPrebattle = 'prebattleID' in ctx)

    
    def _TutorialLoader__pe_onAvatarBecomePlayer(self):
        self._TutorialLoader__afterBattle = True
        if self._TutorialLoader__tutorial is not None:
            self._TutorialLoader__tutorial.stop()
        

    
    def _TutorialLoader__cm_onDisconnected(self):
        if self._TutorialLoader__tutorial is not None:
            self._TutorialLoader__tutorial.stop()
        

    
    def _TutorialLoader__cb_onGetTutorialsCompleted(self, ctx, resultID, completed):
        if resultID < RES_SUCCESS:
            LOG_ERROR('Server return error on request tutorialsCompleted', resultID, completed)
            self._TutorialLoader__tutorial = None
            return None
        ctx['bonusCompleted'] = completed
        cache = ctx['cache']
        if self._TutorialLoader__tutorial._descriptor.isAllBonusesReceived(completed):
            cache.setTrainingFinished(True)
            self._TutorialLoader__tutorial = None
            return None
        if cache.isTrainingRefused():
            if ctx['restart'] and not ctx['inPrebattle']:
                self._TutorialLoader__tutorial.restart(ctx)
            else:
                self._TutorialLoader__tutorial.pause(ctx)
            return None
        if cache.isEmpty() and not completed:
            BigWorld.player().stats.get('dossier', partial(self._TutorialLoader__cb_onGetDossier, ctx))
        else:
            self._TutorialLoader__doRun(ctx)

    
    def _TutorialLoader__cb_onGetDossier(self, ctx, resultID, dossierCompDescr):
        if resultID < RES_SUCCESS:
            LOG_ERROR('Server return error on request dossier', resultID, dossierCompDescr)
            if self._TutorialLoader__tutorial is not None:
                self._TutorialLoader__tutorial = None
            
            return None
        dossierDescr = dossiers.getAccountDossierDescr(dossierCompDescr)
        if not dossierDescr['battlesCount']:
            self._TutorialLoader__doRun(ctx)
        else:
            ctx['cache'].setTrainingFinished(True)
            self._TutorialLoader__tutorial = None

    
    def _TutorialLoader__doRun(self, ctx):
        if ctx['inPrebattle']:
            self._TutorialLoader__tutorial.pause(ctx)
        else:
            self._TutorialLoader__tutorial.run(ctx)


g_loader = None

def init():
    global g_loader
    if IS_TUTORIAL_ENABLED:
        g_loader = _TutorialLoader()
        g_loader.init()
    


def fini():
    global g_loader
    if IS_TUTORIAL_ENABLED:
        if g_loader is not None:
            g_loader.fini()
            g_loader = None
        
    


