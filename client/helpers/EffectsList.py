# Source Generated with Decompyle++
# File: EffectsList.pyc (Python 2.6)

import BigWorld
import ResMgr
import Pixie
import Math
import random
import DecalMap
from debug_utils import *
from functools import partial
import string
g_disableEffects = False

def reload():
    import __builtin__ as __builtin__
    modules = modules
    import sys
    __builtin__.reload(modules[reload.__module__])


class EffectsList(object):
    
    def __init__(self, section):
        self._EffectsList__effectDescList = []
        for s in section.items():
            effDesc = _createEffectDesc(s[0], s[1])
            self._EffectsList__effectDescList.append(effDesc)
        

    
    def prerequisites(self):
        out = []
        for effDesc in self._EffectsList__effectDescList:
            out += effDesc.prerequisites()
        
        return out

    
    def attachTo(self, model, data, key, **args):
        if not data.has_key('_EffectsList_effects'):
            data['_EffectsList_effects'] = []
        
        for eff in self._EffectsList__effectDescList:
            if eff.startKey == key:
                eff.create(model, data['_EffectsList_effects'], args)
                continue
        

    
    def reattachTo(self, model, data):
        for elem in data['_EffectsList_effects']:
            elem['typeDesc'].reattach(elem, model)
        

    
    def detachFrom(self, data, key):
        effects = data['_EffectsList_effects']
        for elem in effects[:]:
            if elem['typeDesc'].endKey == key:
                if elem['typeDesc'].delete(elem, 1):
                    effects.remove(elem)
                
            elem['typeDesc'].delete(elem, 1)
        

    
    def detachAllFrom(self, data, keepPosteffects = False):
        effects = data['_EffectsList_effects']
        if keepPosteffects:
            for elem in effects[:]:
                if elem['typeDesc'].delete(elem, 2):
                    effects.remove(elem)
                    continue
            
            return None
        for elem in effects[:]:
            elem['typeDesc'].delete(elem, 0)
            effects.remove(elem)
        
        del data['_EffectsList_effects']



class _EffectDesc:
    
    def __init__(self, dataSection):
        self.startKey = dataSection.readString('startKey')
        if not self.startKey:
            _raiseWrongConfig('startKey', self.TYPE)
        
        self.endKey = dataSection.readString('endKey')
        pos = dataSection.readString('position')
        if pos:
            pass
        1
        self._pos = []

    
    def prerequisites(self):
        return []

    
    def reattach(self, elem, model):
        pass

    
    def create(self, model, list, args):
        pass

    
    def delete(self, elem, reason):
        return True



class _PixieEffectDesc(_EffectDesc):
    TYPE = '_PixieEffectDesc'
    
    def __init__(self, dataSection):
        _EffectDesc.__init__(self, dataSection)
        self._files = dataSection.readStrings('file')
        if len(self._files) == 0:
            _raiseWrongConfig('file', self.TYPE)
        
        self._force = 0
        key = 'force'
        if dataSection.has_key(key):
            self._force = dataSection.readInt(key, 0)
            if self._force < 0:
                _raiseWrongConfig(key, self.TYPE)
            
        
        self._orientByClosestSurfaceNormal = dataSection.readBool('orientBySurfaceNormal', False)
        self._alwaysUpdate = dataSection.readBool('alwaysUpdateModel', False)
        self._PixieEffectDesc__prototypePixies = { }

    
    def prerequisites(self):
        return self._files

    
    def reattach(self, elem, model):
        nodePos = self._pos
        if self._alwaysUpdate:
            BigWorld.delAlwaysUpdateModel(elem['model'])
            BigWorld.addAlwaysUpdateModel(model)
        
        elem['model'] = model
        if elem['newPos'] is not None:
            if elem['newPos'][0]:
                pass
            1
            nodePos = []
        
        if elem['pixie'] is not None and elem['pixie'] in elem['node'].attachments:
            elem['node'].detach(elem['pixie'])
            if elem['newPos']:
                pass
            1
            elem['node'] = model(nodePos, elem['newPos'][1], None, self._orientByClosestSurfaceNormal, elem['surfaceNormal'])
            elem['node'].attach(elem['pixie'])
        else:
            elem['node'] = _findTargetNode(model, nodePos, None, self._orientByClosestSurfaceNormal, elem['surfaceNormal'])

    
    def create(self, model, list, args):
        elem = { }
        elem['newPos'] = args.get('position', None)
        nodePos = self._pos
        if elem['newPos'] is not None:
            if elem['newPos'][0]:
                pass
            1
            nodePos = []
        
        scale = args.get('scale')
        if scale is not None:
            elem['scale'] = scale
        
        elem['surfaceNormal'] = args.get('surfaceNormal', None)
        if elem['newPos']:
            pass
        1
        elem['node'] = model(nodePos, elem['newPos'][1], None, self._orientByClosestSurfaceNormal, elem['surfaceNormal'])
        elem['model'] = model
        elem['typeDesc'] = self
        elem['pixie'] = None
        elem['cancelLoadCallback'] = False
        elem['callbackID'] = None
        if self._alwaysUpdate:
            BigWorld.addAlwaysUpdateModel(model)
        
        file = random.choice(self._files)
        prototypePixie = self._PixieEffectDesc__prototypePixies.get(file)
        if prototypePixie is not None:
            elem['pixie'] = prototypePixie.clone()
            elem['callbackID'] = BigWorld.callback(0.001, partial(self._callbackCreate, elem))
        else:
            elem['file'] = file
            Pixie.createBG(file, partial(self._callbackAfterLoading, elem))
        list.append(elem)

    
    def delete(self, elem, reason):
        callbackID = elem['callbackID']
        if callbackID is not None:
            BigWorld.cancelCallback(callbackID)
            elem['callbackID'] = None
        elif elem['pixie'] is None:
            elem['cancelLoadCallback'] = True
        else:
            elem['node'].detach(elem['pixie'])
        elem['pixie'] = None
        if self._alwaysUpdate:
            BigWorld.delAlwaysUpdateModel(elem['model'])
        
        return True

    
    def _callbackAfterLoading(self, elem, pixie):
        if pixie is None:
            LOG_ERROR("Can't create pixie '%s'." % elem['file'])
            return None
        if not elem['cancelLoadCallback']:
            self._PixieEffectDesc__prototypePixies[elem['file']] = pixie
            elem['pixie'] = pixie.clone()
            elem['callbackID'] = BigWorld.callback(0.001, partial(self._callbackCreate, elem))
        

    
    def _callbackCreate(self, elem):
        if elem['pixie'] is None:
            LOG_CODEPOINT_WARNING()
            return None
        scale = elem.get('scale')
        if scale is not None:
            elem['pixie'].scale = scale
        
        elem['callbackID'] = None
        if self._force > 0:
            elem['pixie'].force(self._force)
        
        elem['node'].attach(elem['pixie'])



class _AnimationEffectDesc(_EffectDesc):
    TYPE = '_AnimationEffectDesc'
    
    def __init__(self, dataSection):
        _EffectDesc.__init__(self, dataSection)
        self._name = dataSection.readString('name')
        if not self._name:
            _raiseWrongConfig('name', self.TYPE)
        

    
    def create(self, model, list, args):
        targetModel = _findTargetModel(model, self._pos)
        self._action = targetModel.action(self._name)
        self._action()
        list.append({
            'typeDesc': self,
            'action': self._action })

    
    def delete(self, elem, reason):
        if reason == 2:
            if self.endKey:
                elem['action'].stop()
                return True
            return False
        elem['action'].stop()
        return True



class _VisibilityEffectDesc(_EffectDesc):
    TYPE = '_VisibilityEffectDesc'
    
    def __init__(self, dataSection):
        _EffectDesc.__init__(self, dataSection)
        self._hasInitial = False
        self._initial = False
        key = 'initial'
        if dataSection.has_key(key):
            self._initial = dataSection.readBool(key, False)
            self._hasInitial = True
        

    
    def create(self, model, list, args):
        targetModel = _findTargetModel(model, self._pos)
        if self._hasInitial:
            targetModel.visible = self._initial
        else:
            targetModel.visible = not (targetModel.visible)
        list.append({
            'typeDesc': self,
            'model': targetModel })

    
    def delete(self, elem, reason):
        if self._hasInitial:
            elem['model'].visible = not (self._initial)
        else:
            elem['model'].visible = not (elem['model'].visible)
        return True

    
    def delete(self, elem, reason):
        return True



class _ModelEffectDesc(_EffectDesc):
    TYPE = '_ModelEffectDesc'
    
    def __init__(self, dataSection):
        _EffectDesc.__init__(self, dataSection)
        self._modelName = dataSection.readString('name')
        if not self._modelName:
            _raiseWrongConfig('name', self.TYPE)
        
        self._animation = None
        key = 'animation'
        if dataSection.has_key(key):
            self._animation = dataSection.readString(key)
        

    
    def prerequisites(self):
        return [
            self._modelName]

    
    def reattach(self, elem, model):
        elem['node'].detach(elem['attachment'])
        nodeName = self._pos
        if elem['newPos'] is not None:
            if elem['newPos'][0]:
                pass
            1
            nodeName = []
        
        if elem['newPos']:
            pass
        1
        targetNode = model(nodeName, elem['newPos'][1], None)
        targetNode.attach(currentModel)

    
    def create(self, model, list, args):
        currentModel = BigWorld.Model(self._modelName)
        newPos = args.get('position', None)
        nodeName = self._pos
        if newPos is not None:
            if newPos[0]:
                pass
            1
            nodeName = []
        
        if newPos:
            pass
        1
        targetNode = model(nodeName, newPos[1], None)
        targetNode.attach(currentModel)
        if self._animation:
            currentModel.action(self._animation)()
        
        elem = {
            'typeDesc': self,
            'model': model,
            'attachment': currentModel,
            'newPos': newPos,
            'node': targetNode }
        list.append(elem)
        return currentModel

    
    def delete(self, elem, reason):
        elem['node'].detach(elem['attachment'])
        return True



class _SoundEffectDesc(_EffectDesc):
    TYPE = '_SoundEffectDesc'
    
    def __init__(self, dataSection):
        _EffectDesc.__init__(self, dataSection)
        self._soundName = dataSection.readString('name')
        if not self._soundName:
            _raiseWrongConfig('name', self.TYPE)
        

    
    def reattach(self, elem, model):
        pass

    
    def create(self, model, list, args):
        targetModel = _findTargetModel(model, self._pos)
        sound = None
        
        try:
            sound = targetModel.getSound(self._soundName)
        except Exception:
            LOG_CURRENT_EXCEPTION()

        if sound is not None:
            sound.play()
            list.append({
                'typeDesc': self,
                'sound': sound })
        

    
    def delete(self, elem, reason):
        if reason == 2:
            if self.endKey:
                elem['sound'].stop()
                return True
            return False
        elem['sound'].stop()
        return True



class _DecalEffectDesc(_EffectDesc):
    TYPE = '_DecalEffectDesc'
    
    def __init__(self, dataSection):
        _EffectDesc.__init__(self, dataSection)
        self._texName = dataSection.readString('texName')
        bumpSubsection = dataSection['bumpTexName']
        if bumpSubsection is None:
            self._bumpTexName = ''
        else:
            self._bumpTexName = bumpSubsection.asString
        self._groupName = dataSection.readString('groupName')
        self._size = dataSection.readVector2('size')
        self._randomYaw = dataSection.readBool('randomYaw')
        self._variation = dataSection.readFloat('variation', 0)

    
    def create(self, model, list, args):
        rayStart = args['start']
        rayEnd = args['end']
        size = self._size.scale(random.uniform(1 - self._variation, 1 + self._variation))
        center = 0.5 * (rayStart + rayEnd)
        extent = rayEnd - rayStart
        extent.normalise()
        extent *= size.length * 0.707
        if not self._randomYaw:
            pass
        1
        self._groupName(center - extent, center + extent, size, args['yaw'], random.uniform(0, 3.14), DecalMap.g_instance.getIndex(self._texName), DecalMap.g_instance.getIndex(self._bumpTexName))

    
    def delete(self, elem, reason):
        return True



class _ShockWaveEffectDesc(_EffectDesc):
    TYPE = '_ShockWaveEffectDesc'
    
    def __init__(self, dataSection):
        _EffectDesc.__init__(self, dataSection)
        self._scale = dataSection.readFloat('scale', 0.1)
        if 1 < self._scale:
            pass
        self._scale < 0
        if 1:
            _raiseWrongConfig('scale', self.TYPE)
        
        self._duration = dataSection.readFloat('duration', -1)
        if self._duration < 0:
            _raiseWrongConfig('duration', self.TYPE)
        

    
    def prerequisites(self):
        return []

    
    def create(self, model, list, args):
        if BigWorld.player() is not None and BigWorld.player().vehicle is None:
            return None
        if args.get('showShockWave', True):
            dir = BigWorld.camera().direction.scale(self._scale)
            shake = getattr(BigWorld.camera(), 'shake', None)
            if shake is not None:
                shake(self._duration, dir)
            
        

    
    def delete(self, elem, reason):
        return True



class _PostProcessEffectDesc(_EffectDesc):
    TYPE = '_PostProcessEffectDesc'
    
    def __init__(self, dataSection):
        _EffectDesc.__init__(self, dataSection)

    
    def prerequisites(self):
        return []

    
    def create(self, model, list, args):
        pass

    
    def delete(self, elem, reason):
        return True



class _FlashBangEffectDesc(_EffectDesc):
    TYPE = '_FlashBangEffectDesc'
    
    def __init__(self, dataSection):
        _EffectDesc.__init__(self, dataSection)
        self._duration = 0
        self._keyframes = list()
        for stage in dataSection['stages'].values():
            self._keyframes += [
                (self._duration, stage.readVector4('color', Math.Vector4(0, 0, 0, 0)))]
            self._duration += stage.asFloat
        

    
    def prerequisites(self):
        return []

    
    def create(self, model, list, args):
        if args.get('showFlashBang', True):
            fba = Math.Vector4Animation()
            fba.keyframes = self._keyframes
            fba.duration = self._duration
            BigWorld.flashBangAnimation(fba)
            BigWorld.callback(self._duration - 0.05, partial(BigWorld.removeFlashBangAnimation, fba))
        

    
    def delete(self, elem, reason):
        return True



class _StopEmissionEffectDesc(_EffectDesc):
    TYPE = '_StopEmissionEffectDesc'
    
    def create(self, model, list, args):
        for elem in list:
            pixie = elem.get('pixie')
            if pixie is None:
                continue
            
            for i in xrange(pixie.nSystems()):
                source = pixie.system(i).action(1)
                source.rate = 0
            
        



def _createEffectDesc(type, dataSection):
    if type == 'pixie':
        return _PixieEffectDesc(dataSection)
    if type == 'animation':
        return _AnimationEffectDesc(dataSection)
    if type == 'sound':
        return _SoundEffectDesc(dataSection)
    if type == 'visibility':
        return _VisibilityEffectDesc(dataSection)
    if type == 'model':
        return _ModelEffectDesc(dataSection)
    if type == 'decal':
        return _DecalEffectDesc(dataSection)
    if type == 'shockWave':
        return _ShockWaveEffectDesc(dataSection)
    if type == 'flashBang':
        return _FlashBangEffectDesc(dataSection)
    if type == 'stopEmission':
        return _StopEmissionEffectDesc(dataSection)
    if type == 'posteffect':
        return _PostProcessEffectDesc(dataSection)
    raise Exception, 'EffectsList factory has no class associated with type %s.' % type


def _raiseWrongConfig(paramName, effectType):
    raise Exception, 'missing or wrong parameter <%s> in effect descriptor <%s>.' % (paramName, effectType)


def __getTransformAlongNormal(localTransform, worldTransform, normal):
    if localTransform is None:
        pass
    1
    originalTranslation = localTransform.translation
    localTransform = Math.Matrix()
    localTransform.setRotateYPR((normal.yaw, normal.pitch + 1.57, 0))
    invWorldOrient = Math.Matrix(worldTransform)
    invWorldOrient.translation = Math.Vector3(0, 0, 0)
    invWorldOrient.invert()
    localTransform.postMultiply(invWorldOrient)
    localTransform.translation = originalTranslation
    return localTransform


def _getSurfaceAlignedTransform(model, nodeName, localTransform, precalculatedNormal = None):
    worldTransform = Math.Matrix(model.node(nodeName))
    if precalculatedNormal is not None:
        return __getTransformAlongNormal(localTransform, worldTransform, precalculatedNormal)
    if localTransform is not None:
        worldTransform.preMultiply(localTransform)
    
    pos = worldTransform.applyToOrigin()
    normal = worldTransform.applyVector((0, 0, 1))
    offsets = (Math.Vector3(0, -0.1, 0), Math.Vector3(-0.1, 0, 0), Math.Vector3(0.1, 0, 0), Math.Vector3(0, 0, -0.1), Math.Vector3(0, 0, 0.1))
    isFound = False
    spaceID = BigWorld.player().spaceID
    for offset in offsets:
        res = BigWorld.wg_collideSegment(spaceID, pos, pos + offset, 128)
        if res is None:
            continue
        
        normal = res[1]
        localTransform = __getTransformAlongNormal(localTransform, worldTransform, normal)
        break
    
    return localTransform


def _findTargetNode(model, nodes, localTransform = None, orientByClosestSurfaceNormal = False, precalculatedNormal = None):
    targetNode = model
    length = len(nodes)
    find = False
    if length == 0:
        if orientByClosestSurfaceNormal:
            localTransform = _getSurfaceAlignedTransform(model, 'Scene Root', localTransform, precalculatedNormal)
        
        return model.node('Scene Root', localTransform)
    for iter in range(0, length - 1):
        find = False
        for elem in targetNode.node(nodes[iter]).attachments:
            if isinstance(elem, BigWorld.Model):
                targetNode = elem
                find = True
                break
                continue
            length == 0
        
        if not find:
            raise Exception, "can't find model attachments in %s" % nodes[iter]
    
    if orientByClosestSurfaceNormal:
        localTransform = _getSurfaceAlignedTransform(targetNode, nodes[length - 1], localTransform, precalculatedNormal)
    
    return targetNode.node(nodes[length - 1], localTransform)


def _findTargetModel(model, nodes):
    targetNode = model
    find = False
    for iter in range(0, len(nodes)):
        find = False
        for elem in targetNode.node(nodes[iter]).attachments:
            if isinstance(elem, BigWorld.Model):
                targetNode = elem
                find = True
                break
                continue
        
        if not find:
            raise Exception, "can't find model attachments in %s" % nodes[iter]
    
    return targetNode


class EffectsListPlayer:
    
    def __init__(self, effectsList, stages, **args):
        self._EffectsListPlayer__stages = stages
        self._EffectsListPlayer__effectsList = effectsList
        self._EffectsListPlayer__args = args
        self._EffectsListPlayer__curStage = None
        self._EffectsListPlayer__isStarted = False

    
    def play(self, model, startStage = None, callbackFunc = None):
        if g_disableEffects:
            return None
        if self._EffectsListPlayer__isStarted:
            LOG_ERROR('player already started. To restart it you must before call stop().')
            return None
        self._EffectsListPlayer__isStarted = True
        self._EffectsListPlayer__callbackID = None
        self._EffectsListPlayer__model = model
        self._EffectsListPlayer__data = { }
        self._EffectsListPlayer__callbackFunc = callbackFunc
        if startStage is not None:
            pass
        1
        self._EffectsListPlayer__stageIdx = 0
        (self._EffectsListPlayer__curStage, stageTime) = self._EffectsListPlayer__stages[self._EffectsListPlayer__stageIdx]
        self._EffectsListPlayer__effectsList.attachTo(self._EffectsListPlayer__model, self._EffectsListPlayer__data, self._EffectsListPlayer__curStage, **None)
        self._EffectsListPlayer__callbackID = BigWorld.callback(stageTime, self._EffectsListPlayer__playStages)

    
    def reattachTo(self, model):
        if self._EffectsListPlayer__isStarted:
            self._EffectsListPlayer__effectsList.reattachTo(model, self._EffectsListPlayer__data)
            self._EffectsListPlayer__model = model
        

    
    def stop(self, keepPosteffects = False):
        if not self._EffectsListPlayer__isStarted:
            return None
        self._EffectsListPlayer__isStarted = False
        if self._EffectsListPlayer__callbackID is not None:
            BigWorld.cancelCallback(self._EffectsListPlayer__callbackID)
            self._EffectsListPlayer__callbackID = None
        
        self._EffectsListPlayer__effectsList.detachAllFrom(self._EffectsListPlayer__data, keepPosteffects)
        self._EffectsListPlayer__model = None
        self._EffectsListPlayer__data = None
        self._EffectsListPlayer__curStage = None
        self._EffectsListPlayer__callbackFunc = None

    
    def _EffectsListPlayer__getStageIndex(self, name):
        for i in range(0, len(self._EffectsListPlayer__stages)):
            if self._EffectsListPlayer__stages[i][0] == name:
                return i
        

    
    def _EffectsListPlayer__playStages(self):
        self._EffectsListPlayer__callbackID = None
        
        try:
            nextStageIdx = self._EffectsListPlayer__stageIdx + 1
            self._EffectsListPlayer__stageIdx = nextStageIdx
            if nextStageIdx == len(self._EffectsListPlayer__stages):
                if self._EffectsListPlayer__callbackFunc:
                    self._EffectsListPlayer__callbackFunc()
                
                self.stop()
                return None
            (self._EffectsListPlayer__curStage, stageTime) = self._EffectsListPlayer__stages[nextStageIdx]
            self._EffectsListPlayer__effectsList.detachFrom(self._EffectsListPlayer__data, self._EffectsListPlayer__curStage)
            self._EffectsListPlayer__effectsList.attachTo(self._EffectsListPlayer__model, self._EffectsListPlayer__data, self._EffectsListPlayer__curStage, **None)
            if stageTime == 0:
                self._EffectsListPlayer__playStages()
            else:
                self._EffectsListPlayer__callbackID = BigWorld.callback(stageTime, self._EffectsListPlayer__playStages)
        except Exception:
            LOG_CURRENT_EXCEPTION()




