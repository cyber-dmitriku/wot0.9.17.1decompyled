# Source Generated with Decompyle++
# File: sound.pyc (Python 2.6)

import FMOD

class Sound(object):
    
    def __init__(self, soundPath):
        self._Sound__sndTick = FMOD.getSound(soundPath)
        self._Sound__isPlaying = True
        self.stop()

    
    def isPlaying(self):
        return self._Sound__isPlaying

    isPlaying = property(isPlaying)
    
    def play(self):
        self.stop()
        if self._Sound__sndTick:
            self._Sound__sndTick.play()
        
        self._Sound__isPlaying = True

    
    def stop(self):
        if self._Sound__sndTick:
            self._Sound__sndTick.stop()
        
        self._Sound__isPlaying = False



