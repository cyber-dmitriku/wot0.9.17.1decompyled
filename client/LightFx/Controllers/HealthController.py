# Source Generated with Decompyle++
# File: HealthController.pyc (Python 2.6)

from LightFx import LightManager

class HealthController:
    HEALTH_EFFECTS = [
        (9000, 'Full Health'),
        (0.6, 'Mid Health'),
        (0.3, 'Low Health'),
        (0, 'Dead')]
    
    def __init__(self, health, maxHealth):
        self._HealthController__prevHealth = health
        self._HealthController__maxHealth = maxHealth
        self._HealthController__prevHealthEffect = self.getHealthEffect(health)
        LightManager.g_instance.startLightEffect(self._HealthController__prevHealthEffect)

    
    def getHealthEffect(self, health):
        durability = health * 1 / self._HealthController__maxHealth
        healthEffect = ''
        for durabilityEffect in HealthController.HEALTH_EFFECTS:
            if durabilityEffect[0] < durability:
                break
            
            healthEffect = durabilityEffect[1]
        
        return healthEffect

    
    def updateHealth(self, health):
        curHealthEffect = self.getHealthEffect(health)
        if health != self._HealthController__prevHealth:
            LightManager.g_instance.stopLightEffect(self._HealthController__prevHealthEffect)
            LightManager.g_instance.startLightEffect(curHealthEffect)
        
        if curHealthEffect == 'Dead' and curHealthEffect != self._HealthController__prevHealthEffect:
            LightManager.g_instance.startLightEffect('Death')
        
        self._HealthController__prevHealth = health
        self._HealthController__prevHealthEffect = curHealthEffect



