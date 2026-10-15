# Source Generated with Decompyle++
# File: SoundEventManager.pyc (Python 2.6)

__author__ = 'i_maliavko'
from gui.Scaleform.windows import UIInterface
from gui.ClientUpdateManager import g_clientUpdateManager
from CurrentVehicle import g_currentVehicle
from debug_utils import *

class SoundEventManager(UIInterface):
    SPEND_CREDITS_GOLD = 'effects.spend_credits_and_gold'
    SPEND_CREDITS = 'effects.spend_credits'
    SPEND_GOLD = 'effects.spend_gold'
    EARN_CREDITS_GOLD = 'effects.earn_credits_and_gold'
    EARN_CREDITS = 'effects.earn_credits'
    EARN_GOLD = 'effects.earn_gold'
    
    def __init__(self):
        UIInterface.__init__(self)
        self._SoundEventManager__credits = 0
        self._SoundEventManager__gold = 0

    
    def populateUI(self, proxy, credits = 0, gold = 0):
        UIInterface.populateUI(self, proxy)
        self._SoundEventManager__credits = credits
        self._SoundEventManager__gold = gold
        g_clientUpdateManager.addCallbacks({
            'stats': self.onStatsChanged })
        g_currentVehicle.onChanging += self.onVehicleChanging

    
    def dispossessUI(self):
        g_clientUpdateManager.removeObjectCallbacks(self)
        g_currentVehicle.onChanging -= self.onVehicleChanging
        UIInterface.dispossessUI(self)

    
    def _SoundEventManager__playSound(self, soundName):
        if self.uiHolder.soundManager is not None:
            self.uiHolder.soundManager.playSound(soundName)
        

    
    def onVehicleChanging(self):
        self._SoundEventManager__playSound('effects.vehicle_changing')

    
    def onStatsChanged(self, stats):
        newCredits = stats.get('credits', self._SoundEventManager__credits)
        newGold = stats.get('gold', self._SoundEventManager__gold)
        if newCredits < self._SoundEventManager__credits and newGold < self._SoundEventManager__gold:
            self._SoundEventManager__playSound(SoundEventManager.SPEND_CREDITS_GOLD)
        elif newCredits > self._SoundEventManager__credits and newGold > self._SoundEventManager__gold:
            self._SoundEventManager__playSound(SoundEventManager.EARN_CREDITS_GOLD)
        elif newCredits < self._SoundEventManager__credits:
            self._SoundEventManager__playSound(SoundEventManager.SPEND_CREDITS)
        elif newCredits > self._SoundEventManager__credits:
            self._SoundEventManager__playSound(SoundEventManager.EARN_CREDITS)
        elif newGold < self._SoundEventManager__gold:
            self._SoundEventManager__playSound(SoundEventManager.SPEND_GOLD)
        elif newGold > self._SoundEventManager__gold:
            self._SoundEventManager__playSound(SoundEventManager.EARN_GOLD)
        
        self._SoundEventManager__credits = newCredits
        self._SoundEventManager__gold = newGold



