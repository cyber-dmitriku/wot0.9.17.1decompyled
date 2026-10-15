# Source Generated with Decompyle++
# File: StartGameVideo.pyc (Python 2.6)

import BigWorld
import SoundGroups
from debug_utils import LOG_DEBUG, LOG_ERROR
from gui.Scaleform import SCALEFORM_STARTUP_VIDEO_MASK, SCALEFORM_STARTUP_VIDEO_PATH
from gui.Scaleform.CommandArgsParser import CommandArgsParser
from gui.Scaleform.windows import UIInterface
from gui.Scaleform.Waiting import Waiting
import ResMgr

class StartGameVideo(UIInterface):
    
    def __init__(self):
        UIInterface.__init__(self)
        ds = ResMgr.openSection(SCALEFORM_STARTUP_VIDEO_PATH)
        self.movieFiles = []
        for filename in ds.keys():
            (basename, extension) = filename.split('.')
            if extension == 'usm' and basename[0:1] != '_':
                self.movieFiles.append(SCALEFORM_STARTUP_VIDEO_MASK % filename)
                continue
        
        ResMgr.purge(SCALEFORM_STARTUP_VIDEO_PATH, True)
        self.soundValue = SoundGroups.g_instance.getMasterVolume() * 100

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self.uiHolder.movie.backgroundAlpha = 0
        self.uiHolder.addExternalCallbacks({
            'StartGameVideo.StopVideo': self.onStopVideo,
            'StartGameVideo.NetSteamError': self.onNetSteamError })
        if self.movieFiles:
            BigWorld.wg_setMovieSoundMuted(False)
            self.showMovie(self.movieFiles.pop(0))
        else:
            BigWorld.callback((0,), (lambda : self.uiHolder.processLogin()))
        Waiting.hide('loadPage')

    
    def showMovie(self, movie):
        LOG_DEBUG('Startup Video: START - movie = %s, sound volume = %d per cent' % (movie, self.soundValue))
        self.call('StartGameVideo.PopulateUI', [
            movie,
            self.soundValue])

    
    def dispossessUI(self):
        self.uiHolder.removeExternalCallbacks('StartGameVideo.StopVideo', 'StartGameVideo.NetSteamError')
        BigWorld.wg_setMovieSoundMuted(True)
        UIInterface.dispossessUI(self)

    
    def onStopVideo(self, *args):
        if self.movieFiles:
            self.showMovie(self.movieFiles.pop(0))
            return None
        LOG_DEBUG('Startup Video: STOP')
        BigWorld.wg_setMovieSoundMuted(True)
        BigWorld.callback((0,), (lambda : self.uiHolder.processLogin()))

    
    def onNetSteamError(self, *args):
        parser = CommandArgsParser(self.onNetSteamError.__name__, 1, [
            str])
        (code,) = parser.parse(*args)
        LOG_ERROR('Startup Video: ERROR - NetStream code = {0:>s}'.format(code))
        BigWorld.wg_setMovieSoundMuted(True)
        BigWorld.callback((0,), (lambda : self.uiHolder.processLogin()))



