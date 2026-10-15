# Source Generated with Decompyle++
# File: GraphicsPresets.pyc (Python 2.6)

import BigWorld
import ResMgr
from MemoryCriticalController import g_critMemHandler
from debug_utils import LOG_ERROR, LOG_DEBUG
from gui import SystemMessages
from helpers import i18n
graphicsPresetsResource = 'system/data/graphics_settings_presets.xml'

class GraphicsPresets:
    CUSTOM_PRESET_KEY = 'CUSTOM'
    GRAPHICS_QUALITY_SETTINGS = ('RENDER_PIPELINE', 'TEXTURE_QUALITY', 'DECALS_QUALITY', 'OBJECT_LOD', 'FAR_PLANE', 'TERRAIN_QUALITY', 'SHADOWS_QUALITY', 'LIGHTING_QUALITY', 'SPEEDTREE_QUALITY', 'FLORA_QUALITY', 'WATER_QUALITY', 'EFFECTS_QUALITY', 'POST_PROCESSING_QUALITY', 'SNIPER_MODE_EFFECTS_QUALITY', 'VEHICLE_DUST_ENABLED', 'SNIPER_MODE_GRASS_ENABLED', 'VEHICLE_TRACES_ENABLED', 'SNIPER_MODE_SWINGING_ENABLED')
    GRAPHICS_QUALITY_SETTINGS_PRESETS_EXCLUDE = ('SNIPER_MODE_SWINGING_ENABLED',)
    
    def __init__(self):
        section = ResMgr.openSection(graphicsPresetsResource)
        self._GraphicsPresets__presets = { }
        self._GraphicsPresets__presetsKeys = []
        self._GraphicsPresets__currentSetings = None
        self._GraphicsPresets__settingsNeedRestart = set()
        self._GraphicsPresets__settingsDelayed = set()
        for group in section.values():
            presetKey = group.asString
            self._GraphicsPresets__presetsKeys.append(presetKey)
            self._GraphicsPresets__presets[presetKey] = { }
            for setting in group.values():
                label = setting.readString('label')
                if label:
                    self._GraphicsPresets__presets[presetKey][label] = setting.readInt('activeOption')
                    continue
            
        
        self._GraphicsPresets__presetsKeys.append(GraphicsPresets.CUSTOM_PRESET_KEY)
        self.checkCurrentPreset()

    
    def checkCurrentPreset(self):
        self.selectedPresetKey = GraphicsPresets.CUSTOM_PRESET_KEY
        for (key, settings) in self._GraphicsPresets__presets.items():
            foundOption = True
            for (label, value) in settings.items():
                if self._GraphicsPresets__currentSettingsMap.get(label) != value and label in GraphicsPresets.GRAPHICS_QUALITY_SETTINGS:
                    LOG_DEBUG('preset %s breaks at %s' % (key, label))
                    foundOption = False
                    break
                    continue
            
            if foundOption:
                self.selectedPresetKey = key
                break
                continue
        
        LOG_DEBUG('current preset: %s' % self.selectedPresetKey)

    
    def getGraphicsPresetsData(self):
        graphQualitySettings = BigWorld.graphicsSettings()
        qualitySettings = {
            'quality': { },
            'presets': None }
        for (label, index, values, _, advanced, _, _) in graphQualitySettings:
            if label in GraphicsPresets.GRAPHICS_QUALITY_SETTINGS:
                options = []
                for (i, val) in enumerate(values):
                    (valueLabel, supportFlag, advanced, _) = val
                    if supportFlag:
                        options.append({
                            'label': '#settings:graphicsQuality/' + valueLabel,
                            'data': i,
                            'advanced': advanced })
                        continue
                
                qualitySettings['quality'][label] = {
                    'value': index,
                    'options': options }
                continue
        
        presets = {
            'current': self._GraphicsPresets__presetsKeys.index(self.selectedPresetKey),
            'values': [] }
        for (index, presetKey) in enumerate(self._GraphicsPresets__presetsKeys):
            preset = {
                'index': index,
                'key': presetKey,
                'settings': { } }
            settings = self._GraphicsPresets__presets.get(presetKey, { })
            for (label, value) in settings.items():
                if label in GraphicsPresets.GRAPHICS_QUALITY_SETTINGS:
                    preset['settings'][label] = value
                    continue
            
            presets['values'].append(preset)
        
        qualitySettings['presets'] = presets
        return qualitySettings

    
    def __currentSettingsMap(self):
        if self._GraphicsPresets__currentSetings is None:
            graphQualitySettings = BigWorld.graphicsSettings()
            self._GraphicsPresets__currentSetings = { }
            sNeedRestart = []
            sDelayed = []
            for (label, index, _, _, _, needsRestart, delayed) in graphQualitySettings:
                self._GraphicsPresets__currentSetings[label] = index
                if needsRestart:
                    sNeedRestart.append(label)
                
                if delayed:
                    sDelayed.append(label)
                    continue
            
            self._GraphicsPresets__settingsNeedRestart = set(sNeedRestart)
            self._GraphicsPresets__settingsDelayed = set(sDelayed)
        
        return self._GraphicsPresets__currentSetings

    _GraphicsPresets__currentSettingsMap = property(__currentSettingsMap)
    
    def applyGraphicsPreset(self, presetName):
        if self._GraphicsPresets__presets.has_key(presetName):
            self.applyGraphicsPresets(self._GraphicsPresets__presetsKeys.index(presetName), self._GraphicsPresets__presets[presetName])
            return True
        return False

    
    def applyGraphicsPresets(self, presetIndex, customSettings):
        newPresetKey = self._GraphicsPresets__presetsKeys[presetIndex]
        newPreset = { }
        if newPresetKey == self.CUSTOM_PRESET_KEY:
            newPreset = customSettings
        elif newPresetKey != self.selectedPresetKey:
            newPreset = self._GraphicsPresets__presets[newPresetKey]
        
        for key in GraphicsPresets.GRAPHICS_QUALITY_SETTINGS_PRESETS_EXCLUDE:
            newPreset[key] = customSettings[key]
        
        notSetOptions = []
        LOG_DEBUG('Setting preset: %s' % newPresetKey)
        for key in GraphicsPresets.GRAPHICS_QUALITY_SETTINGS:
            value = newPreset.get(key, None)
            if value is None:
                LOG_ERROR('No value for setting: %s' % key)
                continue
            
            
            try:
                LOG_DEBUG('set setting %s = %s' % (key, value))
                BigWorld.setGraphicsSetting(key, value)
                if key == 'TEXTURE_QUALITY':
                    if g_critMemHandler.originQuality != -1:
                        g_critMemHandler.originQuality = value
                    
            continue
            notSetOptions.append(i18n.makeString('#settings:%s' % key))
            LOG_ERROR("selectGraphicsOptions: unable to set value '%s' for option '%s'" % (value, key))
            continue

        
        if notSetOptions:
            if newPresetKey == self.CUSTOM_PRESET_KEY:
                SystemMessages.pushI18nMessage('#system_messages:graficsOptionsFail', ', '.join(notSetOptions), type = SystemMessages.SM_TYPE.Error)
            else:
                SystemMessages.pushI18nMessage('#system_messages:graficsPresetFail', type = SystemMessages.SM_TYPE.Error)
        
        self._GraphicsPresets__currentSetings = None
        self.checkCurrentPreset()

    
    def checkApplyGraphicsPreset(self, presetIndex, customSettings):
        newPresetKey = self._GraphicsPresets__presetsKeys[presetIndex]
        presetForApply = { }
        if newPresetKey == self.CUSTOM_PRESET_KEY:
            presetForApply = customSettings
        elif newPresetKey != self.selectedPresetKey:
            presetForApply = self._GraphicsPresets__presets[newPresetKey]
        
        for key in GraphicsPresets.GRAPHICS_QUALITY_SETTINGS_PRESETS_EXCLUDE:
            presetForApply[key] = customSettings[key]
        
        if not presetForApply:
            return False
        delayedSettings = False
        for (key, value) in presetForApply.items():
            if value != self._GraphicsPresets__currentSettingsMap.get(key):
                if key in self._GraphicsPresets__settingsNeedRestart:
                    return 'restartNeeded'
                if key in self._GraphicsPresets__settingsDelayed:
                    delayedSettings = True
                
            key in self._GraphicsPresets__settingsDelayed
        
        if delayedSettings:
            return 'hasPendingSettings'
        return 'apply'



