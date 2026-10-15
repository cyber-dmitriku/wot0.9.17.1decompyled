# Source Generated with Decompyle++
# File: AreaDestructibles.pyc (Python 2.6)

import BigWorld
from debug_utils import *
from math import floor
import Math
import math
import game
import random
import ResMgr
import constants
from DestructiblesCache import *
from time import clock
from functools import partial
from helpers import bound_effects
from constants import DESTRUCTIBLE_MATKIND
import re
import physics_shared
g_cache = None
g_destructiblesManager = None
g_destructiblesAnimator = None
DESTRUCTIBLE_HIDING_DELAY = 0.2
_TREE_EFFECTS_SCALE_RATIO = 0.7
_DAMAGE_TYPE_TREE = 0
_DAMAGE_TYPE_COLUMN = 1
_DAMAGE_TYPE_FRAGILE = 2
_DAMAGE_TYPE_MODULE = 3
_MAX_PITCH_TO_CHECK_TERRAIN = math.radians(87)

def init():
    global g_cache, g_destructiblesManager, g_destructiblesAnimator
    g_cache = ClientDestructiblesCache()
    g_destructiblesManager = DestructiblesManager()
    g_destructiblesAnimator = _DestructiblesAnimator()


def clear():
    g_destructiblesManager.clear()
    g_destructiblesAnimator.clear()


class ClientDestructiblesCache(DestructiblesCache):
    
    def getDestructibleDesc(self, spaceID, chunkID, destrIndex):
        filename = BigWorld.wg_getDestructibleFilename(spaceID, chunkID, destrIndex)
        return self.getDescByFilename(filename)



class DestructiblesManager:
    
    def __init__(self):
        self._DestructiblesManager__spaceID = None
        self._DestructiblesManager__loadedChunkIDs = { }
        self._DestructiblesManager__savedLoadedChunkIDs = None
        self._DestructiblesManager__destructiblesWaitDestroy = { }
        self._DestructiblesManager__effectsResourceRefs = { }
        self._DestructiblesManager__structuresEffects = { }
        self._DestructiblesManager__lifetimeEffects = { }
        self.forceNoAnimation = False
        self._DestructiblesManager__damagedModules = set()
        self._DestructiblesManager__destrInitialMatrices = { }
        self._DestructiblesManager__ctrls = { }

    
    def clear(self):
        self._DestructiblesManager__spaceID = None
        self._DestructiblesManager__loadedChunkIDs = { }
        self._DestructiblesManager__destructiblesWaitDestroy = { }
        self._DestructiblesManager__effectsResourceRefs = { }
        self._DestructiblesManager__structuresEffects = { }
        self._DestructiblesManager__lifetimeEffects = { }
        self._DestructiblesManager__damagedModules = set()
        self._DestructiblesManager__destrInitialMatrices = { }
        self._DestructiblesManager__ctrls = { }

    
    def startSpace(self, spaceID):
        self.clear()
        self._DestructiblesManager__spaceID = spaceID

    
    def getSpaceID(self):
        return self._DestructiblesManager__spaceID

    
    def getController(self, chunkID):
        return self._DestructiblesManager__ctrls.get(chunkID)

    
    def onChunkLoad(self, chunkID, numDestructibles):
        if numDestructibles > 256:
            self._DestructiblesManager__logErrorTooMuchDestructibles(chunkID)
        
        if self._DestructiblesManager__spaceID is None:
            LOG_ERROR('Notification about chunk load came when no space started')
            return None
        destrFilenames = BigWorld.wg_getChunkDestrFilenames(self._DestructiblesManager__spaceID, chunkID)
        if destrFilenames is None:
            LOG_ERROR("Can't get destructibles filenames list for space %s, chunk %s" % (self._DestructiblesManager__spaceID, chunkID))
            return None
        for destrIndex in xrange(numDestructibles):
            self._DestructiblesManager__setDestructibleInitialState(chunkID, destrIndex)
        
        self._DestructiblesManager__loadedChunkIDs[chunkID] = numDestructibles
        chunkEntries = self._DestructiblesManager__destructiblesWaitDestroy.get(chunkID)
        if chunkEntries is not None:
            for (dmgType, destrData, isNeedAnimation) in chunkEntries:
                self._DestructiblesManager__destroyDestructible(chunkID, dmgType, destrData, isNeedAnimation)
            
            del self._DestructiblesManager__destructiblesWaitDestroy[chunkID]
        
        consideredNames = set()
        prereqs = set()
        for fname in destrFilenames:
            if fname not in consideredNames:
                consideredNames.add(fname)
                desc = g_cache.getDescByFilename(fname)
                if desc is not None:
                    effLists = _extractEffectLists(desc)
                    for effList in effLists:
                        prereqs.update(effList.prerequisites())
                    
                
            desc is not None
        
        if prereqs:
            BigWorld.loadResourceListBG(list(prereqs), partial(self._DestructiblesManager__onResourceLoad, self._DestructiblesManager__spaceID, chunkID))
        

    
    def onChunkLoose(self, chunkID):
        if self._DestructiblesManager__loadedChunkIDs.has_key(chunkID):
            del self._DestructiblesManager__loadedChunkIDs[chunkID]
        
        if self._DestructiblesManager__effectsResourceRefs.has_key(chunkID):
            del self._DestructiblesManager__effectsResourceRefs[chunkID]
        

    
    def isChunkLoaded(self, chunkID):
        return self._DestructiblesManager__loadedChunkIDs.has_key(chunkID)

    
    def orderDestructibleDestroy(self, chunkID, dmgType, destrData, isNeedAnimation):
        if self.forceNoAnimation:
            isNeedAnimation = False
        
        if self._DestructiblesManager__loadedChunkIDs.has_key(chunkID):
            self._DestructiblesManager__destroyDestructible(chunkID, dmgType, destrData, isNeedAnimation)
        else:
            entry = (dmgType, destrData, isNeedAnimation)
            self._DestructiblesManager__destructiblesWaitDestroy.setdefault(chunkID, []).append(entry)

    
    def onBeforeReplayRewind(self):
        self._DestructiblesManager__savedLoadedChunkIDs = self._DestructiblesManager__loadedChunkIDs
        self._DestructiblesManager__savedSpaceID = self._DestructiblesManager__spaceID
        for (chunkID, destrIndex) in self._DestructiblesManager__destrInitialMatrices.iteritems():
            m = None
            BigWorld.wg_setDestructibleMatrix(self._DestructiblesManager__spaceID, chunkID, destrIndex, m)
        

    
    def onAfterReplayRewind(self):
        if self._DestructiblesManager__savedLoadedChunkIDs is None:
            return None
        g_destructiblesAnimator.clear()
        self._DestructiblesManager__spaceID = self._DestructiblesManager__savedSpaceID
        for (chunkID, numDestructibles) in self._DestructiblesManager__savedLoadedChunkIDs.iteritems():
            self.onChunkLoad(chunkID, numDestructibles)
        
        self._DestructiblesManager__savedSpaceID = None
        self._DestructiblesManager__savedLoadedChunkIDs = None

    
    def _addController(self, chunkID, ctrl):
        self._DestructiblesManager__ctrls[chunkID] = ctrl

    
    def _delController(self, chunkID):
        if self._DestructiblesManager__ctrls.has_key(chunkID):
            del self._DestructiblesManager__ctrls[chunkID]
        

    
    def _DestructiblesManager__logErrorTooMuchDestructibles(self, chunkID):
        (x, y) = chunkIndexesFromChunkID(chunkID)
        player = BigWorld.player()
        if player is None:
            LOG_ERROR('Number of destructibles more than 256, chunk: %i %i' % (x, y))
        elif x >= 0:
            xh = hex(x)[2:]
            xh = '0000'[:4 - len(xh)] + xh
        else:
            xh = hex(65535 + x + 1)[2:]
        if y >= 0:
            yh = hex(y)[2:]
            yh = '0000'[:4 - len(yh)] + yh
        else:
            yh = hex(65535 + y + 1)[2:]
        arenaTypeID = player.arenaTypeID
        LOG_ERROR('Number of destructibles more than 256, arena: %s, chunk: %s' % (arenaTypeID, xh + yh + 'o'))

    
    def _DestructiblesManager__onResourceLoad(self, spaceID, chunkID, resourceRefs):
        if spaceID == self._DestructiblesManager__spaceID:
            self._DestructiblesManager__effectsResourceRefs[chunkID] = resourceRefs
        

    
    def _DestructiblesManager__destroyDestructible(self, chunkID, dmgType, destData, isNeedAnimation):
        if self.forceNoAnimation:
            isNeedAnimation = False
        
        if dmgType == _DAMAGE_TYPE_COLUMN:
            (destrIndex, fallDirYaw, fallSpeed) = decodeFallenColumn(destData)
            (pitchConstr, collisionFlags) = BigWorld.wg_getDestructibleFallPitchConstr(self._DestructiblesManager__spaceID, chunkID, destrIndex, fallDirYaw)
            if pitchConstr is None:
                pitchConstr = math.pi / 2
            
            self._DestructiblesManager__dropDestructible(chunkID, destrIndex, fallDirYaw, pitchConstr, fallSpeed, isNeedAnimation, collisionFlags)
        
        if dmgType == _DAMAGE_TYPE_TREE:
            (destrIndex, fallDirYaw, pitchConstr, fallSpeed) = decodeFallenTree(destData)
            (_, collisionFlags) = BigWorld.wg_getDestructibleFallPitchConstr(self._DestructiblesManager__spaceID, chunkID, destrIndex, fallDirYaw)
            self._DestructiblesManager__dropDestructible(chunkID, destrIndex, fallDirYaw, pitchConstr, fallSpeed, isNeedAnimation, collisionFlags)
        elif dmgType == _DAMAGE_TYPE_FRAGILE:
            self._DestructiblesManager__destroyFragile(chunkID, destData, isNeedAnimation)
        elif dmgType == _DAMAGE_TYPE_MODULE:
            (destrIndex, matKind, isShotDamage) = decodeDestructibleModule(destData)
            self._DestructiblesManager__destroyModule(chunkID, destrIndex, matKind, isNeedAnimation, isShotDamage)
        

    
    def _DestructiblesManager__setDestructibleInitialState(self, chunkID, destrIndex):
        filename = BigWorld.wg_getDestructibleFilename(self._DestructiblesManager__spaceID, chunkID, destrIndex)
        if filename is None:
            return None
        filename = re.sub('/lod./', '/lod0/', filename)
        desc = g_cache.getDescByFilename(filename)
        if desc is None:
            return None
        type = desc['type']
        if type == DESTR_TYPE_FRAGILE or type == DESTR_TYPE_STRUCTURE:
            fashion = _getOrCreateFashion(self._DestructiblesManager__spaceID, chunkID, destrIndex)
            fashion.isDestroyed = False
        
        if type == DESTR_TYPE_STRUCTURE:
            for (moduleKind, moduleDesc) in desc['modules'].iteritems():
                self._DestructiblesManager__startLifetimeEffect(chunkID, destrIndex, moduleKind, moduleDesc, desc['filename'])
            
        else:
            self._DestructiblesManager__startLifetimeEffect(chunkID, destrIndex, 0, desc, desc['filename'])

    
    def _DestructiblesManager__destroyFragile(self, chunkID, destrIndex, isNeedAnimation):
        self._DestructiblesManager__stopLifetimeEffect(chunkID, destrIndex, 0)
        BigWorld.callback(DESTRUCTIBLE_HIDING_DELAY, partial(self._DestructiblesManager__setDestructibleState, self._DestructiblesManager__spaceID, chunkID, destrIndex, True))
        desc = g_cache.getDestructibleDesc(self._DestructiblesManager__spaceID, chunkID, destrIndex)
        if desc is None:
            LOG_ERROR('Destructible descriptor is not available, chunkID: %i, destrIndex: %i' % (chunkID, destrIndex))
            return None
        self._DestructiblesManager__launchEffect(chunkID, destrIndex, desc, 'decayEffect', desc['filename'])
        if isNeedAnimation:
            self._DestructiblesManager__launchEffect(chunkID, destrIndex, desc, 'effect', desc['filename'])
        

    
    def _DestructiblesManager__destroyModule(self, chunkID, destrIndex, matKind, isNeedAnimation, isShotDamage):
        if self._DestructiblesManager__isModuleDamaged(chunkID, destrIndex, matKind):
            return None
        self._DestructiblesManager__stopLifetimeEffect(chunkID, destrIndex, matKind)
        desc = g_cache.getDestructibleDesc(self._DestructiblesManager__spaceID, chunkID, destrIndex)
        if desc is None:
            LOG_ERROR('Destructible descriptor is not available, chunkID: %i, destrIndex: %i' % (chunkID, destrIndex))
            return None
        destroyDepends = desc['destroyDepends'].get(matKind, [])
        kindsToHide = [
            matKind]
        kindsToHide += destroyDepends
        for kind in destroyDepends:
            dependModuleDesc = desc['modules'][kind]
            kindsToHide.append(dependModuleDesc['destroyedMat'])
        
        moduleDesc = desc['modules'][matKind]
        destroyedMat = moduleDesc['destroyedMat']
        BigWorld.callback(DESTRUCTIBLE_HIDING_DELAY, partial(self._DestructiblesManager__setDestructibleMaterialsVisible, self._DestructiblesManager__spaceID, chunkID, destrIndex, [
            destroyedMat], kindsToHide))
        if isShotDamage:
            unregisterCallback = partial(self._DestructiblesManager__unregisterModuleEffect, self._DestructiblesManager__spaceID, chunkID, destrIndex, matKind)
            decayEffectID = self._DestructiblesManager__launchEffect(chunkID, destrIndex, moduleDesc, 'decayEffect', desc['filename'], unregisterCallback)
            if decayEffectID is not None:
                self._DestructiblesManager__registerModuleEffect(chunkID, destrIndex, matKind, decayEffectID)
            
        
        damagedDepands = []
        undamagedDepands = []
        for kind in destroyDepends:
            if self._DestructiblesManager__isModuleDamaged(chunkID, destrIndex, kind):
                damagedDepands.append(kind)
                continue
            desc is None
            undamagedDepands.append(kind)
        
        for kind in damagedDepands:
            staticEffectID = self._DestructiblesManager__getModuleEffectID(chunkID, destrIndex, kind)
            if staticEffectID is not None:
                self._DestructiblesManager__unregisterModuleEffect(self._DestructiblesManager__spaceID, chunkID, destrIndex, kind)
                player = BigWorld.player()
                if player is not None:
                    player.terrainEffects.stop(staticEffectID)
                
            player is not None
        
        if isNeedAnimation:
            if isShotDamage:
                coreEffectType = 'hitEffect'
            else:
                coreEffectType = 'ramEffect'
            self._DestructiblesManager__launchEffect(chunkID, destrIndex, moduleDesc, coreEffectType, desc['filename'])
            for kind in undamagedDepands:
                self._DestructiblesManager__launchEffect(chunkID, destrIndex, moduleDesc, 'ramEffect', desc['filename'])
            
        
        damagedKinds = [
            matKind]
        damagedKinds += destroyDepends
        self._DestructiblesManager__registerDamagedModules(chunkID, destrIndex, damagedKinds)
        allUndamagedKinds = self._DestructiblesManager__getUndamagedKinds(chunkID, destrIndex)
        allDamagedKinds = self._DestructiblesManager__getDamagedKinds(chunkID, destrIndex)
        if len(allUndamagedKinds) == 2 and len(allDamagedKinds) >= 6:
            for kind in allUndamagedKinds:
                depends = desc['destroyDepends'].get(kind, [])
                for dependKind in depends:
                    if dependKind in allUndamagedKinds:
                        self._DestructiblesManager__destroyModule(chunkID, destrIndex, dependKind, isNeedAnimation, False)
                        return None
                
            
        
        if len(allUndamagedKinds) == 1 and len(allDamagedKinds) >= 7:
            kind = allUndamagedKinds[0]
            depends = desc['destroyDepends'].get(kind, [])
            kindsToHide = []
            for dependKind in depends:
                dependModuleDesc = desc['modules'][dependKind]
                kindsToHide.append(dependModuleDesc['destroyedMat'])
                self._DestructiblesManager__stopLifetimeEffect(chunkID, destrIndex, kind)
                staticEffectID = self._DestructiblesManager__getModuleEffectID(chunkID, destrIndex, kind)
                if staticEffectID is not None:
                    self._DestructiblesManager__unregisterModuleEffect(self._DestructiblesManager__spaceID, chunkID, destrIndex, kind)
                    player = BigWorld.player()
                    if player is not None:
                        player.terrainEffects.stop(staticEffectID)
                    
                player is not None
            
            BigWorld.callback(DESTRUCTIBLE_HIDING_DELAY, partial(self._DestructiblesManager__setDestructibleMaterialsVisible, self._DestructiblesManager__spaceID, chunkID, destrIndex, [], kindsToHide))
        

    
    def _DestructiblesManager__getDamagedKinds(self, chunkID, destrIndex):
        desc = g_cache.getDestructibleDesc(self._DestructiblesManager__spaceID, chunkID, destrIndex)
        if desc is None:
            LOG_ERROR('Destructible descriptor is not available, chunkID: %i, destrIndex: %i' % (chunkID, destrIndex))
            return None
        damagedKinds = []
        for kind in desc['modules'].iterkeys():
            if self._DestructiblesManager__isModuleDamaged(chunkID, destrIndex, kind):
                damagedKinds.append(kind)
                continue
            desc is None
        
        return damagedKinds

    
    def _DestructiblesManager__getUndamagedKinds(self, chunkID, destrIndex):
        desc = g_cache.getDestructibleDesc(self._DestructiblesManager__spaceID, chunkID, destrIndex)
        if desc is None:
            LOG_ERROR('Destructible descriptor is not available, chunkID: %i, destrIndex: %i' % (chunkID, destrIndex))
            return None
        undamagedKinds = []
        for kind in desc['modules'].iterkeys():
            if not self._DestructiblesManager__isModuleDamaged(chunkID, destrIndex, kind):
                undamagedKinds.append(kind)
                continue
            desc is None
        
        return undamagedKinds

    
    def _DestructiblesManager__launchEffect(self, chunkID, destrIndex, desc, effectType, modelFile, callbackOnStop = None):
        effectVars = desc.get(effectType)
        if effectVars is None:
            return None
        type = desc.get('type')
        if type == DESTR_TYPE_TREE or type == DESTR_TYPE_FALLING_ATOM:
            chunkMatrix = BigWorld.wg_getChunkMatrix(self._DestructiblesManager__spaceID, chunkID)
            destrMatrix = BigWorld.wg_getDestructibleMatrix(self._DestructiblesManager__spaceID, chunkID, destrIndex)
            dir = destrMatrix.applyVector((0, 0, 1))
            pos = chunkMatrix.translation + destrMatrix.translation
            if type == DESTR_TYPE_TREE:
                treeScale = destrMatrix.applyVector((0, 1, 0)).length
                scale = 1 + (treeScale - 1) * _TREE_EFFECTS_SCALE_RATIO
            else:
                scale = desc['effectScale']
        else:
            hpMatrix = BigWorld.wg_getHardPointMatrix(self._DestructiblesManager__spaceID, chunkID, destrIndex, desc['effectHP'])
            if hpMatrix is None:
                LOG_ERROR("Can't find hardpoint %s in model %s" % (desc['effectHP'], modelFile))
                return None
            dir = hpMatrix.applyVector((0, 0, 1))
            pos = hpMatrix.translation
            scale = desc['effectScale']
        player = BigWorld.player()
        if player is None:
            return None
        effectStuff = random.choice(effectVars)
        (stages, effectList) = effectStuff
        effectID = player.terrainEffects.addNew(pos, effectList, stages, callbackOnStop, dir = dir, scale = scale)
        return effectID

    
    def _DestructiblesManager__startLifetimeEffect(self, chunkID, destrIndex, moduleKind, desc, modelFile):
        chance = desc.get('lifetimeEffectChance')
        if chance is None or random.random() > chance:
            return None
        lifetimeEffectID = self._DestructiblesManager__launchEffect(chunkID, destrIndex, desc, 'lifetimeEffect', modelFile)
        if lifetimeEffectID is not None:
            code = _encodeModule(chunkID, destrIndex, moduleKind)
            self._DestructiblesManager__lifetimeEffects[code] = lifetimeEffectID
        

    
    def _DestructiblesManager__stopLifetimeEffect(self, chunkID, destrIndex, moduleKind):
        code = _encodeModule(chunkID, destrIndex, moduleKind)
        lifetimeEffectID = self._DestructiblesManager__lifetimeEffects.get(code)
        if lifetimeEffectID is None:
            return None
        del self._DestructiblesManager__lifetimeEffects[code]
        player = BigWorld.player()
        if player is not None:
            player.terrainEffects.stop(lifetimeEffectID)
        

    
    def _DestructiblesManager__registerDamagedModules(self, chunkID, structureIndex, moduleKinds):
        for kind in moduleKinds:
            code = _encodeModule(chunkID, structureIndex, kind)
            self._DestructiblesManager__damagedModules.add(code)
        

    
    def _DestructiblesManager__isModuleDamaged(self, chunkID, structureIndex, moduleKind):
        code = _encodeModule(chunkID, structureIndex, moduleKind)
        return code in self._DestructiblesManager__damagedModules

    
    def _DestructiblesManager__getModuleEffectID(self, chunkID, structureIndex, moduleKind):
        code = _encodeModule(chunkID, structureIndex, moduleKind)
        return self._DestructiblesManager__structuresEffects.get(code)

    
    def _DestructiblesManager__registerModuleEffect(self, chunkID, structureIndex, moduleKind, effectID):
        code = _encodeModule(chunkID, structureIndex, moduleKind)
        self._DestructiblesManager__structuresEffects[code] = effectID

    
    def _DestructiblesManager__unregisterModuleEffect(self, spaceID, chunkID, structureIndex, moduleKind):
        if spaceID != self._DestructiblesManager__spaceID:
            return None
        code = _encodeModule(chunkID, structureIndex, moduleKind)
        if self._DestructiblesManager__structuresEffects.has_key(code):
            del self._DestructiblesManager__structuresEffects[code]
        

    
    def _DestructiblesManager__setDestructibleMaterialsVisible(self, spaceID, chunkID, destrIndex, kindsToShow, kindsToHide):
        if spaceID != self._DestructiblesManager__spaceID:
            return None
        fashion = _getOrCreateFashion(spaceID, chunkID, destrIndex)
        for kind in kindsToShow:
            fashion.setMaterialKindVisible(kind, True)
            if kind >= DESTRUCTIBLE_MATKIND.DAMAGED_MIN and kind <= DESTRUCTIBLE_MATKIND.DAMAGED_MAX:
                fashion.setEnableDrawMergedModel(False)
                continue
            spaceID != self._DestructiblesManager__spaceID
        
        for kind in kindsToHide:
            fashion.setMaterialKindVisible(kind, False)
            if kind >= DESTRUCTIBLE_MATKIND.NORMAL_MIN and kind <= DESTRUCTIBLE_MATKIND.NORMAL_MAX:
                fashion.setEnableDrawMergedModel(False)
                continue
        

    
    def _DestructiblesManager__setDestructibleState(self, spaceID, chunkID, destrIndex, isDestroyed):
        if spaceID != self._DestructiblesManager__spaceID:
            return None
        fashion = _getOrCreateFashion(spaceID, chunkID, destrIndex)
        fashion.isDestroyed = isDestroyed
        fashion.setEnableDrawMergedModel(not isDestroyed)

    
    def _DestructiblesManager__dropDestructible(self, chunkID, destrIndex, fallDirYaw, pitchConstr, fallSpeed, isAnimate, obstacleCollisionFlags):
        self._DestructiblesManager__stopLifetimeEffect(chunkID, destrIndex, 0)
        if isAnimate:
            self._DestructiblesManager__launchFallEffect(chunkID, destrIndex, 'fractureEffect', fallDirYaw)
            if obstacleCollisionFlags & 8 or pitchConstr > _MAX_PITCH_TO_CHECK_TERRAIN:
                touchdownCallback = partial(self._DestructiblesManager__launchFallEffect, chunkID, destrIndex, 'touchdownEffect', fallDirYaw)
            else:
                touchdownCallback = None
        else:
            touchdownCallback = None
        fashion = _getOrCreateFashion(self._DestructiblesManager__spaceID, chunkID, destrIndex)
        fashion.enableModelCompound = False
        initialMatrix = self._DestructiblesManager__getDestrInitialMatrix(chunkID, destrIndex)
        g_destructiblesAnimator.showFall(self._DestructiblesManager__spaceID, chunkID, destrIndex, fallDirYaw, pitchConstr, fallSpeed, isAnimate, initialMatrix, touchdownCallback)

    
    def _DestructiblesManager__launchFallEffect(self, chunkID, destrIndex, effectName, fallDirYaw):
        player = BigWorld.player()
        if player is None:
            return None
        desc = g_cache.getDestructibleDesc(self._DestructiblesManager__spaceID, chunkID, destrIndex)
        if desc is None:
            LOG_ERROR('Destructible descriptor is not available, chunkID: %i, destrIndex: %i' % (chunkID, destrIndex))
            return None
        effectVars = desc.get(effectName)
        if effectVars is None:
            return None
        effectStuff = random.choice(effectVars)
        (stages, effectList) = effectStuff
        chunkMatrix = BigWorld.wg_getChunkMatrix(self._DestructiblesManager__spaceID, chunkID)
        destrMatrix = BigWorld.wg_getDestructibleMatrix(self._DestructiblesManager__spaceID, chunkID, destrIndex)
        pos = chunkMatrix.translation + destrMatrix.translation
        dir = Math.Vector3(math.sin(fallDirYaw), 0, math.cos(fallDirYaw))
        if desc['type'] == DESTR_TYPE_TREE:
            treeScale = destrMatrix.applyVector((0, 1, 0)).length
            scale = 1 + (treeScale - 1) * _TREE_EFFECTS_SCALE_RATIO
        else:
            scale = desc['effectScale']
        player.terrainEffects.addNew(pos, effectList, stages, None, dir = dir, scale = scale)

    
    def _DestructiblesManager__getDestrInitialMatrix(self, chunkID, destrIndex):
        return self._DestructiblesManager__destrInitialMatrices.setdefault((chunkID, destrIndex), BigWorld.wg_getDestructibleMatrix(self._DestructiblesManager__spaceID, chunkID, destrIndex))



def _extractEffectLists(desc):
    type = desc['type']
    effectLists = []
    if type == DESTR_TYPE_TREE or type == DESTR_TYPE_FALLING_ATOM:
        effTypes = ('fractureEffect', 'touchdownEffect')
        effDescs = [
            desc]
    elif type == DESTR_TYPE_STRUCTURE:
        effTypes = ('ramEffect', 'hitEffect', 'decayEffect')
        effDescs = desc['modules'].itervalues()
    else:
        effTypes = ('effect', 'decayEffect')
        effDescs = [
            desc]
    for effDesc in effDescs:
        for effType in effTypes:
            vars = effDesc.get(effType)
            if vars is not None:
                for stuff in vars:
                    effectLists.append(stuff[1])
                
        
    
    return effectLists


def _encodeModule(chunkID, structureIndex, moduleKind):
    return chunkID << 16 | structureIndex << 8 | moduleKind


def _getOrCreateFashion(spaceID, chunkID, destrIndex):
    fashion = BigWorld.wg_getChunkModelFashion(spaceID, chunkID, destrIndex)
    if fashion is None:
        fashion = BigWorld.WGMaterialDisabler()
        BigWorld.wg_setChunkModelFashion(spaceID, chunkID, destrIndex, fashion)
    
    return fashion


class AreaDestructibles(BigWorld.Entity):
    
    def __init__(self):
        pass

    
    def onEnterWorld(self, prereqs):
        if g_destructiblesManager.getSpaceID() != self.spaceID:
            g_destructiblesManager.startSpace(self.spaceID)
        
        chunkID = chunkIDFromPosition(self.position)
        self._AreaDestructibles__chunkID = chunkID
        g_destructiblesManager._addController(chunkID, self)
        self._AreaDestructibles__prevFallenColumns = frozenset(self.fallenColumns)
        for fallData in self.fallenColumns:
            g_destructiblesManager.orderDestructibleDestroy(chunkID, _DAMAGE_TYPE_COLUMN, fallData, False)
        
        self._AreaDestructibles__prevFallenTrees = frozenset(self.fallenTrees)
        for fallData in self.fallenTrees:
            g_destructiblesManager.orderDestructibleDestroy(chunkID, _DAMAGE_TYPE_TREE, fallData, False)
        
        self._AreaDestructibles__prevDestroyedFragiles = frozenset(self.destroyedFragiles)
        for fragileData in self.destroyedFragiles:
            g_destructiblesManager.orderDestructibleDestroy(chunkID, _DAMAGE_TYPE_FRAGILE, fragileData, False)
        
        self._AreaDestructibles__prevDestroyedModules = frozenset(self.destroyedModules)
        for moduleData in self.destroyedModules:
            g_destructiblesManager.orderDestructibleDestroy(chunkID, _DAMAGE_TYPE_MODULE, moduleData, False)
        

    
    def onLeaveWorld(self):
        g_destructiblesManager._delController(self._AreaDestructibles__chunkID)

    
    def isDestructibleBroken(self, itemIndex, matKind, destrType):
        if destrType == DESTR_TYPE_FRAGILE:
            for fragileData in self.destroyedFragiles:
                if fragileData == itemIndex:
                    return True
            
        elif destrType == DESTR_TYPE_STRUCTURE:
            for moduleData in self.destroyedModules:
                (itemIndex_, matKind_, _) = decodeDestructibleModule(moduleData)
                if itemIndex_ == itemIndex and matKind_ == matKind:
                    return True
            
        elif destrType == DESTR_TYPE_TREE:
            for fallData in self.fallenTrees:
                (itemIndex_, _, _, _) = decodeFallenTree(fallData)
                if itemIndex_ == itemIndex:
                    return True
            
        else:
            for fallData in self.fallenColumns:
                (itemIndex_, _, _) = decodeFallenColumn(fallData)
                if itemIndex_ == itemIndex:
                    return True
            
        return False

    
    def set_fallenTrees(self, prev):
        prev = self._AreaDestructibles__prevFallenTrees
        curr = frozenset(self.fallenTrees)
        self._AreaDestructibles__prevFallenTrees = curr
        for fallData in curr.difference(prev):
            g_destructiblesManager.orderDestructibleDestroy(self._AreaDestructibles__chunkID, _DAMAGE_TYPE_TREE, fallData, True)
        

    
    def set_fallenColumns(self, prev):
        prev = self._AreaDestructibles__prevFallenColumns
        curr = frozenset(self.fallenColumns)
        self._AreaDestructibles__prevFallenColumns = curr
        for fallData in curr.difference(prev):
            g_destructiblesManager.orderDestructibleDestroy(self._AreaDestructibles__chunkID, _DAMAGE_TYPE_COLUMN, fallData, True)
        

    
    def set_destroyedFragiles(self, prev):
        prev = self._AreaDestructibles__prevDestroyedFragiles
        curr = frozenset(self.destroyedFragiles)
        self._AreaDestructibles__prevDestroyedFragiles = curr
        for fragileData in curr.difference(prev):
            g_destructiblesManager.orderDestructibleDestroy(self._AreaDestructibles__chunkID, _DAMAGE_TYPE_FRAGILE, fragileData, True)
        

    
    def set_destroyedModules(self, prev):
        prev = self._AreaDestructibles__prevDestroyedModules
        curr = frozenset(self.destroyedModules)
        self._AreaDestructibles__prevDestroyedModules = curr
        for moduleData in curr.difference(prev):
            g_destructiblesManager.orderDestructibleDestroy(self._AreaDestructibles__chunkID, _DAMAGE_TYPE_MODULE, moduleData, True)
        



class _DestructiblesAnimator:
    _DestructiblesAnimator__UPDATE_INTERVAL = 0.016666
    _DestructiblesAnimator__MAX_PHYS_UPDATE_DELAY = 0.02
    _DestructiblesAnimator__INIT_SPEED_NORMALISER = 0.45
    _DestructiblesAnimator__STOP_SIMULATION_EPSILON = math.pi / 500
    _DestructiblesAnimator__MAX_SIMULATION_DURATION = 8
    
    def __init__(self):
        self._DestructiblesAnimator__updateCallbackID = None
        self._DestructiblesAnimator__isUpdating = False
        self._DestructiblesAnimator__bodies = []

    
    def __del__(self):
        self.clear()

    
    def clear(self):
        self._DestructiblesAnimator__stopUpdate()
        self._DestructiblesAnimator__bodies = []

    
    def showFall(self, spaceID, chunkID, destrIndex, fallDirYaw, pitchConstr, discreteInitSpeed, isNeedAnimation, initialMatrix, touchdownCallback = None):
        desc = g_cache.getDestructibleDesc(spaceID, chunkID, destrIndex)
        if desc is None:
            LOG_ERROR('Destructible descriptor is not available, chunkID: %i, destrIndex: %i' % (chunkID, destrIndex))
            return None
        destrMatrix = Math.Matrix(initialMatrix)
        scale = destrMatrix.applyVector((0, 1, 0)).length
        height = desc['height'] * scale
        mass = desc['mass'] * scale * scale * scale
        stiffness = desc['springStiffnes'] * scale * scale
        pitch = 0
        pitchSpeed = (discreteInitSpeed + 1) * self._DestructiblesAnimator__INIT_SPEED_NORMALISER
        inertiaMoment = mass * height * height / 3
        translation = destrMatrix.translation
        destrMatrix.translation = Math.Vector3(0, 0, 0)
        invFallYawRot = Math.Matrix()
        invFallYawRot.setRotateY(-fallDirYaw)
        destrMatrix.postMultiply(invFallYawRot)
        fallYawRot = Math.Matrix()
        fallYawRot.setRotateY(fallDirYaw)
        body = {
            'pitch': pitch,
            'pitchSpeed': pitchSpeed,
            'inertiaMoment': inertiaMoment,
            'mass': mass,
            'height': height,
            'springAngle': desc['springAngle'],
            'springStiffnes': stiffness,
            'springResist': desc['springResist'] * scale * scale,
            'airResist': desc['airResist'] * scale * scale,
            'pitchConstr': pitchConstr,
            'preRot': destrMatrix,
            'postRot': fallYawRot,
            'translation': translation,
            'chunkID': chunkID,
            'spaceID': spaceID,
            'destrIndex': destrIndex,
            'simulationTime': 0,
            'buryDepth': desc['buryDepth'] * scale }
        if touchdownCallback is not None:
            body['touchdownCallback'] = touchdownCallback
        
        if isNeedAnimation:
            self._DestructiblesAnimator__bodies.append(body)
            self._DestructiblesAnimator__startUpdate()
        else:
            weight = physics_shared.G * mass
            angStiffness = 0.5 * height * stiffness
            approxPitch = pitchConstr - 0.5 * desc['springAngle']
            body['pitch'] = BigWorld.wg_solveDestructibleFallPitch(weight, angStiffness, pitchConstr - desc['springAngle'], approxPitch)
            self._DestructiblesAnimator__positionBodyModel(body)

    
    def _DestructiblesAnimator__detectPitchConstraint(self, spaceID, chunkID, root, fallDir, scanOffs, scanRange, destrIndex):
        testsCount = min(15, max(5, int(scanRange / 0.7)))
        rootUp = root + (0, 100, 0)
        rootDown = root - (0, 100, 0)
        fallNormal = Math.Vector3(fallDir)
        fallNormal.normalise()
        cb = partial(_fallCollideCallback, destrIndex, chunkID)
        rootTestRes = BigWorld.wg_collideSegment(spaceID, rootUp, rootDown, 128, cb)
        if rootTestRes is None:
            return math.pi * 0.5
        rootPoint = rootTestRes[0]
        minPitch = math.pi
        sumPitch = 0
        scanStep = scanRange / (testsCount - 1)
        succsessTestCnt = 0
        for i in xrange(testsCount):
            fallVector = fallNormal * (scanOffs + i * scanStep)
            res = BigWorld.wg_collideSegment(spaceID, rootUp + fallVector, rootDown + fallVector, 128, cb)
            if res is not None:
                p = res[0]
                pitch = math.pi * 0.5 + (p - rootPoint).pitch
                sumPitch += pitch
                succsessTestCnt += 1
                if pitch < minPitch:
                    minPitch = pitch
                
            pitch < minPitch
        
        return minPitch * 0.8 + sumPitch * 0.2 / succsessTestCnt

    
    def _DestructiblesAnimator__moveBody(self, body, dt):
        pitch = body['pitch']
        if pitch < 0:
            body['pitchSpeed'] = 0
            body['pitch'] = 0
            pitch = 0
        
        pitchConstr = body['pitchConstr']
        if pitch > pitchConstr:
            body['pitchSpeed'] = 0
            body['pitch'] = pitchConstr
            pitch = pitchConstr
        
        height = body['height']
        mp = height * height * 0.25
        torque = 0.5 * height * physics_shared.G * body['mass'] * math.sin(pitch)
        torque -= body['pitchSpeed'] * body['airResist'] * mp
        if pitch + body['springAngle'] > pitchConstr:
            touchdownCallback = body.get('touchdownCallback')
            if touchdownCallback is not None:
                touchdownCallback()
                del body['touchdownCallback']
            
            anglePen = pitch + body['springAngle'] - pitchConstr
            torque -= anglePen * body['springStiffnes'] * mp
            torque -= body['pitchSpeed'] * body['springResist'] * mp
        
        body['pitchSpeed'] += dt * torque / body['inertiaMoment']
        body['simulationTime'] += dt
        if abs(body['pitchSpeed']) + abs(torque) < self._DestructiblesAnimator__STOP_SIMULATION_EPSILON or body['simulationTime'] > self._DestructiblesAnimator__MAX_SIMULATION_DURATION:
            return False
        body['pitch'] += dt * body['pitchSpeed']
        return True

    
    def _DestructiblesAnimator__positionBodyModel(self, body):
        m = Math.Matrix()
        m.setRotateX(body['pitch'])
        m.preMultiply(body['preRot'])
        m.postMultiply(body['postRot'])
        m.translation = body['translation'] - (0, body['buryDepth'] * math.sin(body['pitch']), 0)
        spaceID = body['spaceID']
        BigWorld.wg_setDestructibleMatrix(spaceID, body['chunkID'], body['destrIndex'], m)

    
    def _DestructiblesAnimator__update(self, dt):
        removedBodies = []
        cnt = int(math.ceil(dt / self._DestructiblesAnimator__MAX_PHYS_UPDATE_DELAY))
        step = dt / cnt
        for body in self._DestructiblesAnimator__bodies:
            for i in xrange(cnt):
                if not self._DestructiblesAnimator__moveBody(body, step):
                    removedBodies.append(body)
                    break
                    continue
            
        
        for body in removedBodies:
            self._DestructiblesAnimator__bodies.remove(body)
        
        if len(self._DestructiblesAnimator__bodies) == 0:
            self._DestructiblesAnimator__stopUpdate()
        
        for body in self._DestructiblesAnimator__bodies:
            self._DestructiblesAnimator__positionBodyModel(body)
        

    
    def _DestructiblesAnimator__startUpdate(self):
        if not self._DestructiblesAnimator__isUpdating:
            self._DestructiblesAnimator__isUpdating = True
            self._DestructiblesAnimator__lastUpdateTime = clock() - self._DestructiblesAnimator__UPDATE_INTERVAL
            self._DestructiblesAnimator__updateCallback()
        

    
    def _DestructiblesAnimator__stopUpdate(self):
        self._DestructiblesAnimator__isUpdating = False
        if self._DestructiblesAnimator__updateCallbackID is not None:
            BigWorld.cancelCallback(self._DestructiblesAnimator__updateCallbackID)
            self._DestructiblesAnimator__updateCallbackID = None
        

    
    def _DestructiblesAnimator__updateCallback(self):
        self._DestructiblesAnimator__updateCallbackID = None
        curTime = clock()
        self._DestructiblesAnimator__update(curTime - self._DestructiblesAnimator__lastUpdateTime)
        self._DestructiblesAnimator__lastUpdateTime = curTime
        if self._DestructiblesAnimator__isUpdating:
            self._DestructiblesAnimator__updateCallbackID = BigWorld.callback(self._DestructiblesAnimator__UPDATE_INTERVAL, self._DestructiblesAnimator__updateCallback)
        



def _fallCollideCallback(curItemIndex, curChunkID, matKind, collFlags, itemIndex, chunkID):
    if not curChunkID != chunkID:
        pass
    return curItemIndex != itemIndex


