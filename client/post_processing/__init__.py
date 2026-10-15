# Source Generated with Decompyle++
# File: __init__.pyc (Python 2.6)

import BigWorld
import Math
import ResMgr
import weakref
import PostProcessing
import Settings
from PostProcessing.Effects import *
from functools import partial
from debug_utils import *

class _Effect:
    _Effect__FILE_EXT = '.ppchain'
    name = property((lambda self: self._Effect__name + _Effect._Effect__FILE_EXT))
    
    def __init__(self, fileName, ctrlName, optional, isAdvanced, isMapDepended, qualityRange):
        self._Effect__name = fileName
        self._Effect__ctrlName = ctrlName
        self._Effect__isAdvanced = isAdvanced
        self._Effect__isMapDepended = isMapDepended
        self._Effect__qualityRange = qualityRange
        self._Effect__optional = optional
        self._Effect__mapName = ''
        self._Effect__chain = None
        self._Effect__ctrl = None
        self._Effect__curQuality = None

    
    def prerequisites(self):
        if self._Effect__isMapDepended:
            return []
        return PostProcessing.prerequisites(self._Effect__name + _Effect._Effect__FILE_EXT)

    
    def create(self):
        if self._Effect__isMapDepended:
            return None
        self._Effect__create(self._Effect__name + _Effect._Effect__FILE_EXT)

    
    def destroy(self):
        if self._Effect__ctrl is not None:
            self._Effect__ctrl.destroy()
            self._Effect__ctrl = None
        
        self._Effect__chain = None
        self._Effect__curQuality = None

    
    def enable(self, settings):
        if not self._Effect__isSupported(settings):
            return []
        if self._Effect__isMapDepended:
            
            try:
                mapName = BigWorld.player().arena.arenaType.geometryName
            except:
                self._Effect__isSupported(settings)
                LOG_CODEPOINT_WARNING()
                return []

            if self._Effect__mapName != mapName:
                self._Effect__mapName = mapName
                self._Effect__create(self._Effect__name + '_' + self._Effect__mapName + _Effect._Effect__FILE_EXT)
            
        
        if self._Effect__ctrl is not None:
            self._Effect__ctrl.enable()
        
        return self._Effect__chain

    
    def disable(self):
        if self._Effect__ctrl is not None:
            self._Effect__ctrl.disable()
        

    
    def changeQuality(self, quality):
        self._Effect__curQuality = quality

    
    def _Effect__isSupported(self, settings):
        if self._Effect__optional == '':
            pass
        1
        isEnabled = settings[self._Effect__optional]
        mrtEnabled = False
        if self._Effect__curQuality in self._Effect__qualityRange and isEnabled:
            if self._Effect__isAdvanced or self._Effect__isAdvanced:
                return mrtEnabled
        return True

    
    def _Effect__create(self, fileName):
        self._Effect__chain = PostProcessing.load(fileName)
        if self._Effect__chain is None:
            self._Effect__chain = []
            self._Effect__ctrl = None
            LOG_WARNING('Post effect <%s> was not loaded.' % fileName)
        elif self._Effect__ctrlName is not None:
            self._Effect__ctrl = getattr(post_effect_controllers, self._Effect__ctrlName)()
            self._Effect__ctrl.create()
        



class WGPostProcessing:
    _WGPostProcessing__CONFIG_FILE_NAME = 'scripts/post_effects.xml'
    
    def __init__(self):
        self._WGPostProcessing__curQuality = None
        self._WGPostProcessing__curEffects = list()
        self._WGPostProcessing__modes = dict()
        self._WGPostProcessing__settings = dict()
        self._WGPostProcessing__curMode = None

    
    def prerequisites(self):
        ret = []
        return ret

    
    def init(self):
        self._WGPostProcessing__loadSettings()
        PostProcessing.g_graphicsSettingListeners.append(_FuncObj(self, 'onSelectQualityOption'))
        PostProcessing.init()
        PostProcessing.chain(None)
        section = ResMgr.openSection(WGPostProcessing._WGPostProcessing__CONFIG_FILE_NAME)
        self._WGPostProcessing__load(section)
        for mode in self._WGPostProcessing__modes.itervalues():
            for effect in mode:
                effect.create()
            
        

    
    def fini(self):
        self._WGPostProcessing__curEffects = []
        for mode in self._WGPostProcessing__modes.itervalues():
            for effect in mode:
                effect.destroy()
            
        
        PostProcessing.fini()
        self._WGPostProcessing__saveSettings()

    
    def enable(self, mode):
        if self._WGPostProcessing__modes.get(mode, None) is None:
            LOG_WARNING('Effect mode with name %s was not found.' % mode)
            return None
        self._WGPostProcessing__curMode = mode
        self._WGPostProcessing__gatherEffects('common')
        self._WGPostProcessing__gatherEffects(mode)
        chain = []
        for effect in self._WGPostProcessing__curEffects:
            chain += effect.enable(self._WGPostProcessing__settings)
        
        PostProcessing.chain(chain)

    
    def disable(self):
        self._WGPostProcessing__curMode = None
        for effect in self._WGPostProcessing__curEffects:
            effect.disable()
        
        self._WGPostProcessing__curEffects = []
        PostProcessing.chain([])

    
    def refresh(self):
        if self._WGPostProcessing__curMode is None:
            return None
        curMode = self._WGPostProcessing__curMode
        self.disable()
        self.enable(curMode)

    
    def setSetting(self, key, value):
        if self._WGPostProcessing__settings.get(key, None) is None:
            LOG_WARNING("Setting '%s' was not found." % key)
            return None
        self._WGPostProcessing__settings[key] = value

    
    def getSetting(self, key):
        return self._WGPostProcessing__settings.get(key, False)

    
    def onSelectQualityOption(self, quality):
        LOG_NOTE('The quality = %s was selected.' % quality)
        self._WGPostProcessing__curQuality = quality
        BigWorld.callback(0.1, partial(self._WGPostProcessing__onQualityChanged, self._WGPostProcessing__curQuality))

    
    def _printCurrentChain(self):
        chain = []
        for effect in self._WGPostProcessing__curEffects:
            chain.append(effect.name)
        
        print 'Current chain: %s' % chain

    
    def _WGPostProcessing__onQualityChanged(self, quality):
        for mode in self._WGPostProcessing__modes.itervalues():
            for effect in mode:
                effect.changeQuality(quality)
            
        
        self.refresh()

    
    def _WGPostProcessing__gatherEffects(self, mode):
        for effect in self._WGPostProcessing__modes[mode]:
            self._WGPostProcessing__curEffects.append(effect)
        

    
    def _WGPostProcessing__load(self, section):
        for s in section.items():
            self._WGPostProcessing__modes[s[0]] = _loadMode(s[1])
        

    
    def _WGPostProcessing__loadSettings(self):
        userPrefs = Settings.g_instance.userPrefs
        usePostMortemEffect = True
        if userPrefs.has_key(Settings.KEY_ENABLE_MORTEM_POST_EFFECT_OLD):
            usePostMortemEffect = userPrefs.readBool(Settings.KEY_ENABLE_MORTEM_POST_EFFECT_OLD, True)
            userPrefs.deleteSection(Settings.KEY_ENABLE_MORTEM_POST_EFFECT_OLD)
            userPrefs.writeBool(Settings.KEY_ENABLE_MORTEM_POST_EFFECT, usePostMortemEffect)
        else:
            usePostMortemEffect = userPrefs.readBool(Settings.KEY_ENABLE_MORTEM_POST_EFFECT, True)
        self._WGPostProcessing__settings['mortem_post_effect'] = usePostMortemEffect

    
    def _WGPostProcessing__saveSettings(self):
        userPrefs = Settings.g_instance.userPrefs
        userPrefs.writeBool(Settings.KEY_ENABLE_MORTEM_POST_EFFECT, self._WGPostProcessing__settings['mortem_post_effect'])


g_postProcessing = WGPostProcessing()

def _fromMaskToQualityRange(mask):
    out = []
    if mask[0] == 1:
        out.append(0)
    
    if mask[1] == 1:
        out.append(1)
    
    if mask[2] == 1:
        out.append(2)
    
    return out


def _loadEffect(section):
    file = section.readString('file', '')
    qualityRange = _fromMaskToQualityRange(section.readVector3('qualityMask', (1, 1, 1)))
    ctrl = section.readString('controller', '')
    isMapDepended = section.has_key('mapDepended')
    isAdvanced = section.has_key('advanced')
    optional = section.readString('optional', '')
    if ctrl == '':
        pass
    1
    return file(None, ctrl, optional, isAdvanced, isMapDepended, qualityRange)


def _loadMode(section):
    effects = []
    for s in section.items():
        effects.append(_loadEffect(s[1]))
    
    return effects


class _FuncObj:
    
    def __init__(self, obj, funcName):
        self._FuncObj__weakObj = weakref.ref(obj)
        self._FuncObj__funcName = funcName

    
    def __call__(self, args):
        if self._FuncObj__weakObj() is not None:
            getattr(self._FuncObj__weakObj(), self._FuncObj__funcName)(args)
        else:
            LOG_CODEPOINT_WARNING('weak object has been already destroyed.')



