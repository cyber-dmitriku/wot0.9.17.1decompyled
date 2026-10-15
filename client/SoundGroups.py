# Source Generated with Decompyle++
# File: SoundGroups.pyc (Python 2.6)

import BigWorld
import FMOD
import Settings
from debug_utils import *
g_instance = None

class SoundGroups(object):
    
    def __init__(self):
        self._SoundGroups__volumeByCategory = { }
        self._SoundGroups__masterVolume = 1
        self._SoundGroups__isWindowVisible = BigWorld.isWindowVisible()
        self._SoundGroups__groups = {
            'arena': ('/vehicles/tanks', '/hits/hits', '/hits/explosions', '/hits/tank_death', '/weapons/large_fire', '/weapons/medium_fire', '/weapons/small_fire', '/weapons/tracer', '/GUI/notifications_FX', '/ingame_voice/notifications_VO', '/objects/wire_barricade', '/objects/tent', '/objects/dog_house', '/objects/structures', '/objects/treefall', '/objects/wood_box_mid', '/objects/telegraph_pole', '/objects/buildings', '/objects/fuel_tank', '/objects/fence', '/objects/fuel_barrel', '/objects/fire', '/objects/hay_stack', '/objects/metall_pole_huge') }
        self._SoundGroups__categories = {
            'voice': ('ingame_voice',),
            'vehicles': ('vehicles',),
            'effects': ('hits', 'weapons', 'environment', 'battle_gui'),
            'gui': ('gui',),
            'music': ('music',),
            'ambient': ('ambient',),
            'masterVivox': (),
            'micVivox': (),
            'masterFadeVivox': () }
        defMasterVolume = 0.5
        defCategoryVolumes = {
            'music': 0.5,
            'masterVivox': 0.7,
            'micVivox': 0.8 }
        userPrefs = Settings.g_instance.userPrefs
        if not userPrefs.has_key(Settings.KEY_SOUND_PREFERENCES):
            userPrefs.write(Settings.KEY_SOUND_PREFERENCES, '')
            self._SoundGroups__masterVolume = defMasterVolume
            for categoryName in self._SoundGroups__categories.keys():
                self._SoundGroups__volumeByCategory[categoryName] = defCategoryVolumes.get(categoryName, 1)
            
            self.savePreferences()
        else:
            ds = userPrefs[Settings.KEY_SOUND_PREFERENCES]
            self._SoundGroups__masterVolume = ds.readFloat('masterVolume', defMasterVolume)
            for categoryName in self._SoundGroups__categories.keys():
                volume = ds.readFloat('volume_' + categoryName, defCategoryVolumes.get(categoryName, 1))
                self._SoundGroups__volumeByCategory[categoryName] = volume
            
        self.applyPreferences()
        self._SoundGroups__muteCallbackID = BigWorld.callback(0.25, self._SoundGroups__muteByWindowVisibility)

    
    def __del__(self):
        if self._SoundGroups__muteCallbackID is not None:
            BigWorld.cancelCallback(self._SoundGroups__muteCallbackID)
            self._SoundGroups__muteCallbackID = None
        

    
    def loadSounds(self, groupName):
        for group in self._SoundGroups__groups[groupName]:
            
            try:
                FMOD.loadSoundGroup(group)
            continue
            except Exception:
                LOG_CURRENT_EXCEPTION()
                continue
            

        

    
    def unloadSounds(self, groupName):
        for group in self._SoundGroups__groups[groupName]:
            
            try:
                FMOD.unloadSoundGroup(group)
            continue
            except Exception:
                LOG_CURRENT_EXCEPTION()
                continue
            

        

    
    def enableLobbySounds(self, enable):
        for categoryName in ('ambient', 'gui'):
            if not enable:
                pass
            1
            volume = self._SoundGroups__volumeByCategory[categoryName]
            self.setVolume(categoryName, volume, False)
        

    
    def enableArenaSounds(self, enable):
        for categoryName in ('voice', 'vehicles', 'effects', 'ambient'):
            if not enable:
                pass
            1
            volume = self._SoundGroups__volumeByCategory[categoryName]
            self.setVolume(categoryName, volume, False)
        

    
    def setMasterVolume(self, volume):
        self._SoundGroups__masterVolume = volume
        FMOD.setMasterVolume(volume)
        self.savePreferences()

    
    def getMasterVolume(self):
        return self._SoundGroups__masterVolume

    
    def setVolume(self, categoryName, volume, updatePrefs = True):
        for category in self._SoundGroups__categories[categoryName]:
            
            try:
                BigWorld.wg_setCategoryVolume(category, volume)
            continue
            except Exception:
                LOG_CURRENT_EXCEPTION()
                continue
            

        
        if updatePrefs:
            self._SoundGroups__volumeByCategory[categoryName] = volume
            self.savePreferences()
        

    
    def getVolume(self, categoryName):
        return self._SoundGroups__volumeByCategory[categoryName]

    
    def savePreferences(self):
        ds = Settings.g_instance.userPrefs[Settings.KEY_SOUND_PREFERENCES]
        ds.writeFloat('masterVolume', self._SoundGroups__masterVolume)
        for categoryName in self._SoundGroups__volumeByCategory.keys():
            ds.writeFloat('volume_' + categoryName, self._SoundGroups__volumeByCategory[categoryName])
        

    
    def applyPreferences(self):
        if not self._SoundGroups__isWindowVisible:
            FMOD.setMasterVolume(0)
            return None
        self.setMasterVolume(self._SoundGroups__masterVolume)
        for categoryName in self._SoundGroups__volumeByCategory.keys():
            self.setVolume(categoryName, self._SoundGroups__volumeByCategory[categoryName], updatePrefs = False)
        

    
    def _SoundGroups__muteByWindowVisibility(self):
        isWindowVisible = BigWorld.isWindowVisible()
        if self._SoundGroups__isWindowVisible != isWindowVisible:
            self._SoundGroups__isWindowVisible = isWindowVisible
            self.applyPreferences()
        
        self._SoundGroups__muteCallbackID = BigWorld.callback(0.25, self._SoundGroups__muteByWindowVisibility)



