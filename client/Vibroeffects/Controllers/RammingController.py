# Source Generated with Decompyle++
# File: RammingController.pyc (Python 2.6)

import BigWorld
from OnceController import OnceController
from constants import DESTRUCTIBLE_MATKIND

class RammingController:
    RAMMING_EXECUTION_DELAY = 2.5
    MIN_IMPACT_SPEED = 3
    _RammingController__executionForbidden = None
    
    def _RammingController__allowExecution(self):
        self._RammingController__executionForbidden = None

    
    def destroy(self):
        if self._RammingController__executionForbidden is not None:
            BigWorld.cancelCallback(self._RammingController__executionForbidden)
        

    
    def execute(self, vehicleSpeed, matKind):
        if not (self._RammingController__executionForbidden) and vehicleSpeed >= self.MIN_IMPACT_SPEED:
            effectName = 'ramming_vehicle_veff'
            if matKind is not None:
                if DESTRUCTIBLE_MATKIND.MIN <= matKind:
                    pass
                matKind <= DESTRUCTIBLE_MATKIND.MAX
                if 1:
                    effectName = 'ramming_destructible_veff'
                else:
                    effectName = 'ramming_indestructible_veff'
            OnceController(effectName)
            self._RammingController__executionForbidden = BigWorld.callback(self.RAMMING_EXECUTION_DELAY, self._RammingController__allowExecution)
        



