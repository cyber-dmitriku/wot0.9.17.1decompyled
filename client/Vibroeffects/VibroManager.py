# Source Generated with Decompyle++
# File: VibroManager.pyc (Python 2.6)

import BigWorld
import copy
from EffectsSettings import EffectsSettings
from VibroEffect import VibroEffect
import Settings
from debug_utils import *
import Event
from gui.Scaleform.SoundManager import BUTTON_TYPES
g_instance = None

class VibroManager:
    _VibroManager__CONNECTION_CHECK_PERIOD = 10
    
    class GroupSettings:
        pass

    
    def __init__(self):
        self._VibroManager__effects = { }
        self._VibroManager__quickEffects = { }
        self._VibroManager__vibrationObject = BigWorld.WGVibration()
        self._VibroManager__vibrationObject.reset()
        self._VibroManager__connectionCheckId = BigWorld.callback(VibroManager._VibroManager__CONNECTION_CHECK_PERIOD, self._VibroManager__checkConnection)
        self._VibroManager__eventManager = Event.EventManager()
        self.onConnect = Event.Event(self._VibroManager__eventManager)
        self.onDisconnect = Event.Event(self._VibroManager__eventManager)
        self._VibroManager__runningEffects = { }
        self._VibroManager__topEffect = None
        self._VibroManager__groupsSettings = { }
        for groupName in EffectsSettings.Groups.AllGroupNames:
            self._VibroManager__groupsSettings[groupName] = VibroManager.GroupSettings()
            self._VibroManager__groupsSettings[groupName].enabled = True
            self._VibroManager__groupsSettings[groupName].gain = 1
        
        EffectsSettings.loadSettings()
        self._VibroManager__gain = 1
        self._VibroManager__isEnabledByUser = True
        self.loadUserPrefs()
        self._VibroManager__isConnected = False
        self.connect()
        self.launchQuickEffect('startup_veff')

    
    def start(self):
        g_windowsManager = g_windowsManager
        import gui.WindowsManager
        if g_windowsManager.window is not None:
            g_windowsManager.window.addExternalCallback('StartGameVideo.StopVideo', self._VibroManager__onStopVideo)
            g_windowsManager.window.addExternalCallback('StartGameVideo.NetSteamError', self._VibroManager__onStopVideo)
        

    
    def _VibroManager__onStopVideo(self, *args):
        self.stopAllEffects()

    
    def playButtonClickEffect(self, buttonType):
        if not self._VibroManager__isConnected:
            return None
        self.launchQuickEffect('button_click_veff')

    
    def clearEffects(self):
        for effect in self._VibroManager__effects.values():
            effect.destroy()
        
        for effectPool in self._VibroManager__quickEffects.values():
            for effect in effectPool:
                effect.destroy()
            
        

    
    def destroy(self):
        self.clearEffects()
        self._VibroManager__effects = None
        self._VibroManager__quickEffects = None
        self._VibroManager__runningEffects = None
        self._VibroManager__vibrationObject = None
        self.saveUserPrefs()
        if self._VibroManager__connectionCheckId is not None:
            BigWorld.cancelCallback(self._VibroManager__connectionCheckId)
            self._VibroManager__connectionCheckId = None
        
        self._VibroManager__eventManager.clear()

    
    def loadUserPrefs(self):
        userPrefs = Settings.g_instance.userPrefs
        if not userPrefs.has_key(Settings.KEY_VIBRATION):
            self.saveUserPrefs()
        
        ds = userPrefs[Settings.KEY_VIBRATION]
        self.setGain(ds.readFloat('gain', 1))
        self.setEnabledByUser(ds.readBool('enabled_by_user', True))
        groupsSettingsSection = ds['groups']
        if groupsSettingsSection is None:
            return None
        for groupName in EffectsSettings.Groups.AllGroupNames:
            groupSection = groupsSettingsSection[groupName]
            if groupSection is not None:
                self._VibroManager__groupsSettings[groupName].enabled = groupSection.readBool('enabled', True)
                self._VibroManager__groupsSettings[groupName].gain = groupSection.readFloat('gain', 1)
                continue
            groupsSettingsSection is None
        

    
    def saveUserPrefs(self):
        userPrefs = Settings.g_instance.userPrefs
        if not userPrefs.has_key(Settings.KEY_VIBRATION):
            userPrefs.write(Settings.KEY_VIBRATION, '')
        
        ds = userPrefs[Settings.KEY_VIBRATION]
        ds.writeFloat('gain', self.getGain())
        ds.writeBool('enabled_by_user', self.isEnabledByUser())
        for groupName in EffectsSettings.Groups.AllGroupNames:
            ds.writeBool('groups/%s/enabled' % groupName, self._VibroManager__groupsSettings[groupName].enabled)
            ds.writeFloat('groups/%s/gain' % groupName, self._VibroManager__groupsSettings[groupName].gain)
        

    
    def getGroupsSettings(self):
        return copy.deepcopy(self._VibroManager__groupsSettings)

    
    def setGroupsSettings(self, settings):
        self._VibroManager__groupsSettings = copy.deepcopy(settings)
        for groupSettings in self._VibroManager__groupsSettings.values():
            if groupSettings.gain > 1:
                groupSettings.gain = 1
                continue
            if groupSettings.gain < 0:
                groupSettings.gain = 0
                continue
        

    
    def isGroupEnabled(self, groupName):
        if groupName in self._VibroManager__groupsSettings:
            return self._VibroManager__groupsSettings[groupName].enabled
        LOG_DEBUG('group not found: ' + groupName)
        return False

    
    def getGroupGain(self, groupName):
        if groupName in self._VibroManager__groupsSettings:
            return self._VibroManager__groupsSettings[groupName].gain
        LOG_DEBUG('group not found: ' + groupName)
        return 1

    
    def isEnabledByUser(self):
        return self._VibroManager__isEnabledByUser

    
    def setEnabledByUser(self, enable):
        if not enable:
            for effect in self._VibroManager__runningEffects.values():
                self.stopEffect(effect)
            
            self._VibroManager__runningEffects.clear()
        
        self._VibroManager__isEnabledByUser = enable

    
    def _VibroManager__checkConnection(self):
        self.connect()
        self._VibroManager__connectionCheckId = BigWorld.callback(VibroManager._VibroManager__CONNECTION_CHECK_PERIOD, self._VibroManager__checkConnection)

    
    def connect(self):
        wasConnected = self._VibroManager__isConnected
        if not wasConnected:
            self.clearEffects()
            self._VibroManager__quickEffects.clear()
            self._VibroManager__runningEffects.clear()
        
        self._VibroManager__isConnected = self._VibroManager__vibrationObject.connect()
        if self._VibroManager__isConnected and not wasConnected:
            self.onConnect()
            for effect in self._VibroManager__effects.values():
                effect.reInit(self.loadEffectFromFile(effect.name))
                self.stopEffect(effect)
            
        
        if not (self._VibroManager__isConnected) and wasConnected:
            self.onDisconnect()
        
        return self._VibroManager__isConnected

    
    def canWork(self):
        if self._VibroManager__isEnabledByUser:
            pass
        return self._VibroManager__isConnected

    
    def setGain(self, gain):
        if gain < 0:
            gain = 0
        
        if gain > 1:
            gain = 1
        
        self._VibroManager__gain = gain
        self._VibroManager__vibrationObject.setGain(self._VibroManager__gain)

    
    def getGain(self):
        return self._VibroManager__gain

    
    def getStatus(self):
        result = { }
        result['constant'] = self._VibroManager__effects
        result['quick'] = self._VibroManager__quickEffects
        result['running'] = self._VibroManager__runningEffects
        return result

    
    def getOverlappedGainMultiplier(self):
        return EffectsSettings.getOverlappedGainMultiplier()

    
    def loadEffectFromFile(self, effectName, priority = 0):
        if not self._VibroManager__isConnected:
            return VibroEffect(effectName, None, EffectsSettings.getEffectPriority(effectName), self._VibroManager__vibrationObject, EffectsSettings.getGroupForEffect(effectName))
        effectHandle = self._VibroManager__vibrationObject.createEffect()
        fileName = EffectsSettings.CFG_FOLDER + effectName + '.uwv'
        self._VibroManager__vibrationObject.loadEffectFromFile(effectHandle, fileName)
        effect = VibroEffect(effectName, effectHandle, EffectsSettings.getEffectPriority(effectName), self._VibroManager__vibrationObject, EffectsSettings.getGroupForEffect(effectName))
        return effect

    
    def getEffect(self, effectName):
        if effectName in self._VibroManager__effects:
            return self._VibroManager__effects[effectName]
        effect = self.loadEffectFromFile(effectName)
        self._VibroManager__effects[effectName] = effect
        return effect

    
    def launchQuickEffect(self, effectName, count = 1, gain = 100):
        if not self.canWork():
            return None
        if count is None:
            return None
        sourceEffect = None
        if effectName in self._VibroManager__quickEffects:
            effectsPool = self._VibroManager__quickEffects[effectName]
            for effect in effectsPool:
                if not effect.isRunning():
                    effect.setRelativeGain(gain)
                    self.startEffect(effect, count)
                    return None
                sourceEffect = effect
            
        
        if sourceEffect is None:
            effectToLaunch = self.loadEffectFromFile(effectName)
            self._VibroManager__quickEffects[effectName] = [
                effectToLaunch]
        else:
            effectToLaunch = VibroEffect(effectName, self._VibroManager__vibrationObject.cloneEffect(sourceEffect.handle), sourceEffect.getPriority(), self._VibroManager__vibrationObject, sourceEffect.group)
            self._VibroManager__quickEffects[effectName].append(effectToLaunch)
        effectToLaunch.setRelativeGain(gain)
        self.startEffect(effectToLaunch, count)

    
    def startEffect(self, vibroEffect, count = None):
        if not self.canWork() or not self.isGroupEnabled(vibroEffect.group):
            return None
        if vibroEffect.isRunning() or vibroEffect.handle is None:
            return None
        vibroEffect.onStart(count)
        self._VibroManager__runningEffects[vibroEffect.handle] = vibroEffect
        if self._VibroManager__topEffect is None or vibroEffect.getPriority() >= self._VibroManager__topEffect.getPriority():
            if self._VibroManager__topEffect is not None:
                self._VibroManager__drownEffect(self._VibroManager__topEffect)
            
            self._VibroManager__topEffect = vibroEffect
            self._VibroManager__topEffect.setRelativeGain(self._VibroManager__topEffect.getRelativeGain())
        
        self.update()

    
    def stopEffect(self, vibroEffect):
        if vibroEffect.handle is None:
            return None
        vibroEffect.onStop()

    
    def stopAllEffects(self):
        for effect in self._VibroManager__runningEffects.values():
            self.stopEffect(effect)
        
        self.update()

    
    def _VibroManager__drownEffect(self, vibroEffect):
        effectGain = self.getGroupGain(vibroEffect.group) * self.getOverlappedGainMultiplier() * vibroEffect.getRelativeGain()
        self._VibroManager__vibrationObject.setEffectGain(vibroEffect.handle, effectGain)

    
    def update(self):
        if not self.canWork():
            return None
        curTopEffect = None
        for vibroEffect in self._VibroManager__runningEffects.values()[:]:
            if not vibroEffect.isRunning():
                del self._VibroManager__runningEffects[vibroEffect.handle]
                continue
            self.canWork()
            if curTopEffect is None or curTopEffect.getPriority() < vibroEffect.getPriority():
                curTopEffect = vibroEffect
                continue
        
        if not self._VibroManager__topEffect is None:
            pass
        shouldRecalcGain = not self._VibroManager__topEffect.isRunning()
        if shouldRecalcGain:
            self._VibroManager__topEffect = curTopEffect
        
        for vibroEffect in self._VibroManager__runningEffects.values():
            if (shouldRecalcGain or vibroEffect.requiresGainChange()) and vibroEffect != self._VibroManager__topEffect:
                self._VibroManager__drownEffect(vibroEffect)
                continue
            if vibroEffect.requiresGainChange() or shouldRecalcGain:
                self._VibroManager__vibrationObject.setEffectGain(vibroEffect.handle, self.getGroupGain(vibroEffect.group) * vibroEffect.getRelativeGain())
                continue
        



