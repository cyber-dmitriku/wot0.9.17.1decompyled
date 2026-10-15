# Source Generated with Decompyle++
# File: DeathController.pyc (Python 2.6)

from OnceController import OnceController

class DeathController:
    _DeathController__wasVehicleAlive = None
    
    def update(self, isVehicleAlive):
        if self._DeathController__wasVehicleAlive and not isVehicleAlive:
            OnceController('crit_death_veff')
        
        self._DeathController__wasVehicleAlive = isVehicleAlive



