# Source Generated with Decompyle++
# File: LightControllersManager.pyc (Python 2.6)

from Controllers.HealthController import HealthController
import LightManager

class LightControllersManager:
    
    def __init__(self, vehicle):
        self._LightControllersManager__healthController = HealthController(vehicle.health, vehicle.typeDescriptor.maxHealth)

    
    def destroy(self):
        LightManager.g_instance.setStartupLights()

    
    def executeShotLight(self):
        LightManager.g_instance.startLightEffect('Shot')

    
    def executeHitLight(self):
        LightManager.g_instance.startLightEffect('Hit')

    
    def update(self, vehicle):
        self._LightControllersManager__healthController.updateHealth(vehicle.health)



