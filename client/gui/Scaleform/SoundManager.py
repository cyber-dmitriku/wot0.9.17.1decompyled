# Source Generated with Decompyle++
# File: SoundManager.pyc (Python 2.6)

from debug_utils import *
import ResMgr
from items import _xml
from gui.Scaleform.windows import UIInterface
from gui.Scaleform.utils.sound import Sound
import Vibroeffects

class BUTTON_TYPES(object):
    NORMAL = 'normal'


class RENDERER_TYPES(object):
    NORMAL = 'normal'


class SoundSettings(dict):
    
    def __init__(self):
        self._SoundSettings__schemas = { }
        self._SoundSettings__groups = { }
        self._SoundSettings__overrides = { }

    
    def populateSettings(dataSection):
        res = SoundSettings()
        for (typeName, settings) in dataSection.items():
            if typeName == 'overrides':
                for (overrideName, events) in settings.items():
                    res._SoundSettings__overrides[overrideName] = { }
                    for (eventName, event) in events.items():
                        res._SoundSettings__overrides[overrideName][eventName] = event.asString
                    
                
            if typeName == 'schemas':
                for (schemaName, parts) in settings.items():
                    res._SoundSettings__schemas[schemaName] = { }
                    for (partName, subParts) in parts.items():
                        for (subPartName, data) in subParts.items():
                            if partName == 'sounds':
                                res._SoundSettings__schemas[schemaName][subPartName] = data.asString
                                continue
                            if partName == 'groups':
                                res._SoundSettings__groups[subPartName] = schemaName
                                continue
                        
                    
                
            if typeName == 'default':
                for (eventName, event) in settings.items():
                    res[eventName] = event.asString
                
            res[typeName] = settings.asString
        
        return res

    populateSettings = staticmethod(populateSettings)
    
    def getSoundName(self, soundType, soundId, state):
        if len(soundId) and self._SoundSettings__overrides.has_key(soundId) > 0:
            sound = self._SoundSettings__overrides.get(soundId, { }).get(state, '')
        elif len(soundType) > 0 and self._SoundSettings__groups.has_key(soundType):
            schemaName = self._SoundSettings__groups.get(soundType, '')
            sound = self._SoundSettings__schemas.get(schemaName, { }).get(state, '')
        elif len(soundType) > 0 and self._SoundSettings__schemas.has_key(soundType):
            sound = self._SoundSettings__schemas.get(soundType, { }).get(state, '')
        else:
            sound = self.get(state, '')
        return sound



class SoundManager(UIInterface):
    
    def __init__(self):
        self._SoundManager__soundEvents = { }
        self._SoundManager__loadConfig()

    
    def _SoundManager__loadConfig(self):
        xmlPath = 'gui/gui_sounds_new.xml'
        section = ResMgr.openSection(xmlPath)
        if section is None:
            _xml.raiseWrongXml(None, xmlPath, 'can not open or read')
        
        for (groupName, types) in section.items():
            self._SoundManager__soundEvents[groupName] = SoundSettings.populateSettings(types)
        

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        sm = self.uiHolder.movie.soundManager
        sm.script = self

    
    def soundEventHandler(self, control, state, type, id):
        self.tryPlaySnd(control, state, type, id)

    
    def dispossessUI(self):
        self.uiHolder.movie.soundManager.script = None
        UIInterface.dispossessUI(self)

    
    def playSound(self, dictPath):
        if dictPath is None:
            return None
        scope = self._SoundManager__soundEvents
        for key in str(dictPath).split('.'):
            if key not in scope:
                return None
            scope = scope[key]
        
        if type(scope) != str:
            LOG_ERROR('Invalid soundpath under key: %s', dictPath)
            return None
        Sound(scope).play()

    
    def onButtonEvent(self, callbackID, state, type, id):
        self.tryPlaySnd('buttons', state, type, id)

    
    def onItemRendererEvent(self, callbackID, state, type):
        self.tryPlaySnd('itemRenderer', state, type, 'fakeId')

    
    def tryPlaySnd(self, sndType, state, type, id):
        sound = self._SoundManager__soundEvents.get(sndType, SoundSettings()).getSoundName(type, id, state)
        if sound:
            Sound(sound).play()
            if state == 'press':
                Vibroeffects.VibroManager.g_instance.playButtonClickEffect(type)
            
        



