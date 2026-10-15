# Source Generated with Decompyle++
# File: EffectsSettings.pyc (Python 2.6)

import ResMgr

class EffectsSettings:
    DELAY_BETWEEN_EFFECTS = 0.1
    COUNT_INFINITY = 0xFFFFFFFFL
    CFG_FOLDER = 'vibroeffects/'
    AccelerationThreshold = 0
    DecelerationThreshold = 0
    
    class Groups:
        ENGINE = 'engine'
        ACCELERATION = 'acceleration'
        SHOTS = 'shots'
        HITS = 'hits'
        DAMAGE = 'damage'
        GUI = 'gui'
        COLLISIONS = 'collisions'
        AllGroupNames = [
            ENGINE,
            ACCELERATION,
            SHOTS,
            HITS,
            DAMAGE,
            GUI,
            COLLISIONS]

    _EffectsSettings__effects = { }
    _EffectsSettings__overlappedGainMultiplier = 0
    _EffectsSettings__guiButtonsVibrations = { }
    
    def __loadGuiButtonsSettings(buttonsSection):
        for (buttonType, effectNameSection) in buttonsSection.items():
            EffectsSettings._EffectsSettings__guiButtonsVibrations[buttonType] = effectNameSection.asString
        

    _EffectsSettings__loadGuiButtonsSettings = staticmethod(__loadGuiButtonsSettings)
    
    def loadSettings():
        root = ResMgr.openSection(EffectsSettings.CFG_FOLDER + 'effects_settings.xml')
        EffectsSettings._EffectsSettings__loadGuiButtonsSettings(root['buttons'])
        effectsSection = root['effects']
        if effectsSection is not None:
            continue
            effects = _[1]
            for effect in effects:
                
                class EffectData:
                    pass

                data = EffectData()
                data.priority = effect.readInt('priority')
                data.group = effect.readString('group')
                EffectsSettings._EffectsSettings__effects[effect.readString('name')] = data
            
        
        EffectsSettings._EffectsSettings__overlappedGainMultiplier = root.readFloat('overlapped_gain_multiplier', 0)
        if EffectsSettings._EffectsSettings__overlappedGainMultiplier < 0:
            EffectsSettings._EffectsSettings__overlappedGainMultiplier = 0
        elif EffectsSettings._EffectsSettings__overlappedGainMultiplier > 1:
            EffectsSettings._EffectsSettings__overlappedGainMultiplier = 1
        
        EffectsSettings.AccelerationThreshold = root.readFloat('acceleration_threshold', 0)
        EffectsSettings.DecelerationThreshold = root.readFloat('deceleration_threshold', 0)

    loadSettings = staticmethod(loadSettings)
    
    def getEffectPriority(effectName):
        if effectName in EffectsSettings._EffectsSettings__effects:
            return EffectsSettings._EffectsSettings__effects[effectName].priority
        raise Exception("Cannot find effect's priority " + effectName)

    getEffectPriority = staticmethod(getEffectPriority)
    
    def getOverlappedGainMultiplier():
        return EffectsSettings._EffectsSettings__overlappedGainMultiplier

    getOverlappedGainMultiplier = staticmethod(getOverlappedGainMultiplier)
    
    def getGroupForEffect(effectName):
        if effectName in EffectsSettings._EffectsSettings__effects:
            return EffectsSettings._EffectsSettings__effects[effectName].group
        raise Exception("Cannot find effect's group " + effectName)

    getGroupForEffect = staticmethod(getGroupForEffect)
    
    def getButtonEffect(buttonType):
        return EffectsSettings._EffectsSettings__guiButtonsVibrations.get(buttonType, None)

    getButtonEffect = staticmethod(getButtonEffect)


