# Source Generated with Decompyle++
# File: TutorialCache.pyc (Python 2.6)

import BigWorld
import base64
import cPickle
import os
from debug_utils import LOG_CURRENT_EXCEPTION
from tutorial.settings import TUTORIAL_VERSION

class TutorialCache(object):
    
    def __init__(self, accountName):
        p = os.path
        prefsFilePath = unicode(BigWorld.wg_getPreferencesFilePath(), 'utf-8', errors = 'ignore')
        self._TutorialCache__cacheDir = p.join(p.dirname(prefsFilePath), 'tutorial_cache')
        self._TutorialCache__cacheFileName = p.join(self._TutorialCache__cacheDir, '{0:>s}.dat'.format(base64.b32encode('{0:>s};{1:>s}'.format(str(BigWorld.server()), accountName))))
        self._TutorialCache__version = TUTORIAL_VERSION
        self._TutorialCache__cache = {
            'finished': False,
            'refused': False,
            'afterBattle': False,
            'flags': { },
            'currentChapter': None }
        self._TutorialCache__read()

    
    def __repr__(self):
        return 'TutorialCache({0:s}): {1!r:s}'.format(hex(id(self)), self._TutorialCache__cache)

    
    def _TutorialCache__read(self):
        file = None
        
        try:
            if not os.path.isfile(self._TutorialCache__cacheFileName):
                return None
            file = open(self._TutorialCache__cacheFileName, 'rb')
            (self._TutorialCache__version, cache) = cPickle.load(file)
            if self._TutorialCache__version != TUTORIAL_VERSION:
                self._TutorialCache__version = TUTORIAL_VERSION
            else:
                self._TutorialCache__cache.update(cache)
        except Exception:
            LOG_CURRENT_EXCEPTION()
        finally:
            if file is not None:
                file.close()
            


    
    def _TutorialCache__write(self):
        output = None
        
        try:
            if not os.path.isdir(self._TutorialCache__cacheDir):
                os.makedirs(self._TutorialCache__cacheDir)
            
            output = open(self._TutorialCache__cacheFileName, 'wb')
            cPickle.dump((self._TutorialCache__version, self._TutorialCache__cache), output, -1)
        except Exception:
            LOG_CURRENT_EXCEPTION()
        finally:
            if output is not None:
                output.close()
            


    
    def update(self, currentChapter, flags):
        if currentChapter is not None:
            self._TutorialCache__cache['currentChapter'] = currentChapter
        
        if flags is not None:
            self._TutorialCache__cache['flags'] = flags
        
        self._TutorialCache__write()

    
    def setTrainingFinished(self, flag, flush = True):
        self._TutorialCache__cache['finished'] = flag
        if flush:
            self._TutorialCache__write()
        

    
    def isTrainingFinished(self):
        return self._TutorialCache__cache['finished']

    
    def setTrainingRefused(self, flag, flush = True):
        self._TutorialCache__cache['refused'] = flag
        if flush:
            self._TutorialCache__write()
        

    
    def isTrainingRefused(self):
        return self._TutorialCache__cache['refused']

    
    def setAfterBattle(self, flag, flush = True):
        self._TutorialCache__cache['afterBattle'] = flag
        if flush:
            self._TutorialCache__write()
        

    
    def isAfterBattle(self):
        return self._TutorialCache__cache['afterBattle']

    
    def currentChapter(self):
        return self._TutorialCache__cache['currentChapter']

    
    def flags(self):
        return self._TutorialCache__cache['flags']

    
    def clearChapterData(self, flush = True):
        self._TutorialCache__cache['flags'] = { }
        self._TutorialCache__cache['afterBattle'] = False
        if flush:
            self._TutorialCache__write()
        

    
    def isEmpty(self):
        if not self._TutorialCache__cache['currentChapter'] is None:
            pass
        return not len(self._TutorialCache__cache['flags'])



