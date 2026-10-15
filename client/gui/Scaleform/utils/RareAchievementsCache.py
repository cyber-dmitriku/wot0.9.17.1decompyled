# Source Generated with Decompyle++
# File: RareAchievementsCache.pyc (Python 2.6)

import Event
from debug_utils import *
from helpers import i18n, getClientLanguage
from account_helpers.rare_achievements import getRareAchievementImage, getRareAchievementText

class _RaresCache(object):
    DEFAULT_TITLE = i18n.makeString('#tooltips:achievement/action/unavailable/title')
    DEFAULT_DESCR = i18n.makeString('#tooltips:achievement/action/unavailable/descr')
    
    def __init__(self):
        self._RaresCache__cache = dict()
        self.onTextReceived = Event.Event()
        self.onImageReceived = Event.Event()

    
    def request(self, listOfIds):
        LOG_DEBUG('Request action achievements data')
        if not len(listOfIds):
            return None
        landId = getClientLanguage()
        for achieveId in listOfIds:
            getRareAchievementText(landId, achieveId, self._RaresCache__onTextReceived)
            getRareAchievementImage(achieveId, self._RaresCache__onImageReceived)
        

    
    def _RaresCache__onTextReceived(self, id, text):
        achieveData = self._RaresCache__cache.setdefault(id, dict())
        title = text.get('title')
        descr = text.get('description')
        LOG_DEBUG('Text received for achievement: %d; title: %s; descr: %s' % (id, type(title), type(descr)))
        if not (descr is not None or 'descr' not in achieveData) and achieveData['descr'] != descr and title is not None and 'title' not in achieveData:
            pass
        isGenerateEvent = achieveData['title'] != title
        if descr is not None:
            achieveData['descr'] = text.get('description')
        
        if title is not None:
            achieveData['title'] = title
        
        if isGenerateEvent:
            self.onTextReceived(id, achieveData['title'], achieveData['descr'])
        

    
    def _RaresCache__onImageReceived(self, id, imageData):
        achieveData = self._RaresCache__cache.setdefault(id, dict())
        LOG_DEBUG('Image received for achievement: %d %s' % (id, type(imageData)))
        if imageData is None:
            return None
        if not 'image' not in achieveData:
            pass
        isGenerateEvent = achieveData['image'] != imageData
        achieveData['image'] = imageData
        if isGenerateEvent:
            self.onImageReceived(id, imageData)
        

    
    def getTitle(self, id):
        if not self._RaresCache__cache.get(id, dict()).get('title'):
            pass
        return _RaresCache.DEFAULT_TITLE

    
    def getDescription(self, id):
        if not self._RaresCache__cache.get(id, dict()).get('descr'):
            pass
        return _RaresCache.DEFAULT_DESCR

    
    def getImageData(self, id):
        return self._RaresCache__cache.get(id, dict()).get('image')


g_rareAchievesCache = _RaresCache()

