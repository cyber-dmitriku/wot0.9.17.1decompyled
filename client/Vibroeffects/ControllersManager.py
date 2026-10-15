# Source Generated with Decompyle++
# File: ControllersManager.pyc (Python 2.6)

from Controllers.HitController import HitController
from Controllers.DeathController import DeathController
from Controllers.EngineController import EngineController
from Controllers.RammingController import RammingController
from Controllers.SwitchController import SwitchController
from Controllers.TrackBreakingController import TrackBreakingController
from Controllers.ShootingController import ShootingController
from Controllers.OnceController import OnceController
import Vibroeffects.VibroManager as VibroManager

class ControllersManager:
    
    def __init__(self):
        self._ControllersManager__engineVibrationCtrl = EngineController()
        self._ControllersManager__fireVibrationCtrl = SwitchController('crit_fire_veff')
        self._ControllersManager__trackBreakingVibrationCtrl = TrackBreakingController()
        self._ControllersManager__deathVibrationCtrl = DeathController()
        self._ControllersManager__rammingVibrationCtrl = RammingController()

    
    def destroy(self):
        self._ControllersManager__engineVibrationCtrl.destroy()
        self._ControllersManager__fireVibrationCtrl.destroy()
        self._ControllersManager__rammingVibrationCtrl.destroy()
        VibroManager.g_instance.stopAllEffects()

    
    def update(self, vehicle, isLeftTrackBroken, isRightTrackBroken):
        if not VibroManager.g_instance.canWork():
            return None
        self._ControllersManager__deathVibrationCtrl.update(vehicle.isAlive())
        self._ControllersManager__updateEngine(vehicle)
        if vehicle.isAlive():
            self._ControllersManager__trackBreakingVibrationCtrl.update(vehicle, isLeftTrackBroken, isRightTrackBroken)
        else:
            self._ControllersManager__fireVibrationCtrl.switch(False)
        VibroManager.g_instance.update()

    
    def switchFireVibrations(self, enableFire):
        if self._ControllersManager__fireVibrationCtrl is not None:
            self._ControllersManager__fireVibrationCtrl.switch(enableFire)
        

    
    def executeRammingVibrations(self, vehicleSpeed, matKind):
        if VibroManager.g_instance.canWork():
            self._ControllersManager__rammingVibrationCtrl.execute(vehicleSpeed, matKind)
        

    
    def executeHitVibrations(self, shotResult):
        if VibroManager.g_instance.canWork():
            HitController(shotResult)
        

    
    def executeShootingVibrations(self, caliber):
        if VibroManager.g_instance.canWork():
            ShootingController(caliber)
        

    
    def executeCriticalHitVibrations(self, vehicle, extrasName):
        if not VibroManager.g_instance.canWork():
            return None
        if extrasName == 'gunHealth':
            OnceController('crit_run_veff')
        elif extrasName == 'engineHealth':
            OnceController('crit_engine_veff')
        else:
            for tankman in vehicle.typeDescriptor.type.tankmen:
                if extrasName == tankman.name:
                    OnceController('crit_contusion_veff')
                    break
                    continue
                VibroManager.g_instance.canWork()
            

    
    def _ControllersManager__updateEngine(self, vehicle):
        dirFlags = vehicle.engineMode[1]
        if dirFlags & 4 != 0:
            self._ControllersManager__engineVibrationCtrl.setTurn('left')
        elif dirFlags & 8 != 0:
            self._ControllersManager__engineVibrationCtrl.setTurn('right')
        else:
            self._ControllersManager__engineVibrationCtrl.setTurn('')
        self._ControllersManager__engineVibrationCtrl.update(vehicle)



