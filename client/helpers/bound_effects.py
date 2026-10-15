# Source Generated with Decompyle++
# File: bound_effects.pyc (Python 2.6)

import BigWorld
import Math
import BattleReplay
from debug_utils import *
from functools import partial
from helpers.EffectsList import EffectsListPlayer

class StaticSceneBoundEffects(object):
    
    def __init__(self):
        self._models = { }
        self._StaticSceneBoundEffects__incrementalEffectID = -1

    
    def destroy(self):
        self._matProv = None
        for (id, elem) in self._models.items():
            elem['effectsPlayer'].stop()
            model = elem['model']
            if model is not None:
                BigWorld.delModel(model)
                BigWorld.delAlwaysUpdateModel(model)
            
            del self._models[id]
        

    
    def addNew(self, position, effectsList, stages, callbackOnStop, **args):
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.isTimeWarpInProgress:
            return -1
        model = BigWorld.player().newFakeModel()
        model.position = position
        BigWorld.addModel(model)
        BigWorld.addAlwaysUpdateModel(model)
        dir = args.get('dir', None)
        if dir is not None:
            model.rotate(dir.yaw, (0, 1, 0))
        
        self._StaticSceneBoundEffects__incrementalEffectID += 1
        effectID = self._StaticSceneBoundEffects__incrementalEffectID
        desc = dict()
        desc['model'] = model
        desc['effectsPlayer'] = EffectsListPlayer(effectsList, stages, **None)
        desc['effectsPlayer'].play(model, None, partial(self._StaticSceneBoundEffects__callbackBeforeDestroy, effectID, callbackOnStop))
        self._models[effectID] = desc
        return effectID

    
    def stop(self, effectID):
        if self._models.has_key(effectID):
            desc = self._models[effectID]
            desc['effectsPlayer'].stop()
            BigWorld.delModel(desc['model'])
            BigWorld.delAlwaysUpdateModel(desc['model'])
            del self._models[effectID]
        

    
    def _StaticSceneBoundEffects__callbackBeforeDestroy(self, effectID, callbackOnStop):
        if callbackOnStop is not None:
            callbackOnStop()
        
        self.stop(effectID)



class ModelBoundEffects(object):
    
    def __init__(self, model, nodeName = ''):
        self._ModelBoundEffects__model = model
        self._ModelBoundEffects__nodeName = nodeName
        self._effects = list()

    
    def destroy(self):
        for elem in self._effects[:]:
            elem.stop()
            self._effects.remove(elem)
        
        self._model = None

    
    def addNew(self, matProv, effectsList, stages, **args):
        desc = EffectsListPlayer(effectsList, stages, position = (self._ModelBoundEffects__nodeName, matProv), **None)
        desc.play(self._ModelBoundEffects__model, None, partial(self._effects.remove, desc))
        self._effects.append(desc)

    
    def reattachTo(self, model):
        self._ModelBoundEffects__model = model
        for elem in self._effects:
            elem.reattachTo(model)
        



