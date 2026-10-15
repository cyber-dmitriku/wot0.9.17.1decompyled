# Source Generated with Decompyle++
# File: LightEffectsCache.pyc (Python 2.6)

import ResMgr
import LightEffect

class LightEffectsCache:
    SETTINGS_PATH = 'scripts/alienware_light_fx.xml'
    _LightEffectsCache__ACTION_MAPPING = {
        'Morph': 1,
        'Pulse': 2,
        'Color': 3 }
    _LightEffectsCache__lightEffects = { }
    
    def allEffects():
        return LightEffectsCache._LightEffectsCache__lightEffects

    allEffects = staticmethod(allEffects)
    
    def load():
        settingsSection = ResMgr.openSection(LightEffectsCache.SETTINGS_PATH)
        lightEffectsDesc = (lambda .0: for section in .0:
if section.name == 'lightEffect':
sectioncontinue)(settingsSection.values())
        for lightEffectSection in lightEffectsDesc:
            LightEffectsCache._LightEffectsCache__addLightEffect(lightEffectSection)
        

    load = staticmethod(load)
    
    def __parseDescriptions(descriptionStr):
        descriptions = descriptionStr.split(',')
        result = []
        for descriptionStr in descriptions:
            result.append(descriptionStr.strip())
        
        return result

    _LightEffectsCache__parseDescriptions = staticmethod(__parseDescriptions)
    
    def __addLightEffect(lightEffectSection):
        name = lightEffectSection.readString('name')
        duration = lightEffectSection.readFloat('duration')
        if duration == -1:
            duration = None
        
        lightActions = { }
        for section in lightEffectSection.values():
            if section.name == 'light':
                lightDescriptions = LightEffectsCache._LightEffectsCache__parseDescriptions(section.readString('lightDescription'))
                for lightDescription in lightDescriptions:
                    color = section.readVector4('color')
                    action = LightEffectsCache._LightEffectsCache__ACTION_MAPPING[section.readString('action')]
                    lightActions[lightDescription] = LightEffect.OneLightAction(lightDescription, color, action)
                
        
        LightEffectsCache._LightEffectsCache__lightEffects[name] = LightEffect.LightEffect(name, lightActions, duration)

    _LightEffectsCache__addLightEffect = staticmethod(__addLightEffect)
    
    def getEffect(effectName):
        return LightEffectsCache._LightEffectsCache__lightEffects[effectName]

    getEffect = staticmethod(getEffect)


