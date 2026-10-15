# Source Generated with Decompyle++
# File: FxController.pyc (Python 2.6)


class IAuxiliaryVehicleFx:
    
    def __init__(self, vehicle, fxManager):
        self._vehicle = vehicle
        self._fxManager = fxManager

    
    def destroy(self):
        pass

    
    def executeShotEffect(self):
        pass

    
    def executeHitEffect(self):
        pass

    
    def update(self, vehicle):
        pass



class AuxiliaryFxController:
    
    def __init__(self, fxControllers):
        self._AuxiliaryFxController__controllers = fxControllers

    
    def destroy(self):
        for controller in self._AuxiliaryFxController__controllers:
            controller.destroy()
        
        self._AuxiliaryFxController__controllers = None

    
    def executeShotEffect(self):
        for controller in self._AuxiliaryFxController__controllers:
            controller.executeShotEffect()
        

    
    def executeHitEffect(self):
        for controller in self._AuxiliaryFxController__controllers:
            controller.executeHitEffect()
        

    
    def update(self, vehicle):
        for controller in self._AuxiliaryFxController__controllers:
            controller.update(vehicle)
        



