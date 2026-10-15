# Source Generated with Decompyle++
# File: ClientHangarSpace.pyc (Python 2.6)

import BigWorld
import Math
import ResMgr
import copy
from debug_utils import *
from functools import partial
from gui import g_tankActiveCamouflage
import items.vehicles as items
import math
import time
import VehicleStickers
from MemoryCriticalController import g_critMemHandler
from PlayerEvents import g_playerEvents
from helpers import getClientLanguage
from ConnectionManager import connectionManager
from ModelHitTester import ModelHitTester
_DEFAULT_HANGAR_SPACE_PATH = 'spaces/hangar'
_DEFAULT_HANGAR_PREM_SPACE_PATH = 'spaces/hangar_premium'
_SERVER_CMD_CHANGE_HANGAR = 'cmd_change_hangar'
_SERVER_CMD_CHANGE_HANGAR_PREM = 'cmd_change_hangar_prem'
_HANGAR_FAKESHADOWMAP_MODEL_NAME = 'gw.model'
_HANGAR_FAKESHADOWMAP_DEFAULT_TEX_NAME = 'content/Environment/envH_shadowPlane/GW_shad.dds'
_CFG = {
    'basic': {
        'def_space_path': _DEFAULT_HANGAR_SPACE_PATH,
        'nation_space_paths': { },
        'v_scale': 1,
        'v_start_angles': (0, 0, 0),
        'v_start_pos': Math.Vector3(50, 0, 50),
        'cam_start_dist': 9,
        'cam_start_angles': [
            -25,
            210],
        'cam_start_target_pos': Math.Vector3(50, 0, 50),
        'cam_dist_constr': [
            6,
            11],
        'cam_pitch_constr': [
            -70,
            -5],
        'cam_sens': 0.005,
        'cam_pivot_pos': Math.Vector3(0, 1, 0),
        'cam_fluency': 0.05,
        'emblems_alpha_damaged': 0.3,
        'emblems_alpha_undamaged': 0.9,
        'shadow_light_dir': (0.55, -1, -1.7),
        'preview_cam_start_dist': 8,
        'preview_cam_start_angles': [
            -25,
            140],
        'preview_cam_pivot_pos': Math.Vector3(-2, 1, 0),
        'preview_cam_start_target_pos': Math.Vector3(50, 0, 50) },
    'premium': {
        'def_space_path': _DEFAULT_HANGAR_PREM_SPACE_PATH,
        'nation_space_paths': {
            'usa': 'spaces/hangar_premium_AM' },
        'v_scale': 1,
        'v_start_angles': (180, 0, 0),
        'v_start_pos': Math.Vector3(50, 0, 50),
        'cam_start_dist': 14,
        'cam_start_angles': [
            -10,
            25],
        'cam_start_target_pos': Math.Vector3(50, 0, 50),
        'cam_dist_constr': [
            6,
            14],
        'cam_pitch_constr': [
            -70,
            -5],
        'cam_sens': 0.005,
        'cam_pivot_pos': Math.Vector3(0, 1, 0),
        'cam_fluency': 0.05,
        'emblems_alpha_damaged': 0.3,
        'emblems_alpha_undamaged': 0.9,
        'shadow_light_dir': (-0.3, -0.5, 0.7),
        'preview_cam_start_dist': 8,
        'preview_cam_start_angles': [
            -25,
            -40],
        'preview_cam_pivot_pos': Math.Vector3(-2, 1, 0),
        'preview_cam_start_target_pos': Math.Vector3(50, 0, 50) } }
_V_SCALE = None
_V_START_ANGLES = None
_V_START_POS = None
_CAM_START_DIST = None
_CAM_START_ANGLES = None
_CAM_START_TARGET_POS = None
_CAM_DIST_CONSTR = None
_CAM_PITCH_CONSTR = None
_CAM_SENS = None
_CAM_PIVOT_POS = None
_CAM_FLUENCY = None
_EMBLEMS_ALPHA_DAMAGED = None
_EMBLEMS_ALPHA_UNDAMAGED = None
_SHADOW_LIGHT_DIR = None
_PREVIEW_CAM_START_DIST = None
_PREVIEW_CAM_START_ANGLES = None
_PREVIEW_CAM_PIVOT_POS = None
_PREVIEW_CAM_START_TARGET_POS = None
_CAMOUFLAGE_MIN_INTENSITY = 1

class ClientHangarSpace:
    
    def __init__(self):
        self._ClientHangarSpace__spaceId = None
        self._ClientHangarSpace__cam = None
        self._ClientHangarSpace__waitCallback = None
        self._ClientHangarSpace__loadingStatus = 0
        self._ClientHangarSpace__destroyFunc = None
        self._ClientHangarSpace__spaceMappingId = None
        self._ClientHangarSpace__onLoadedCallback = None
        self._ClientHangarSpace__boundingRadius = None
        self._ClientHangarSpace__vAppearance = None
        self._ClientHangarSpace__vEntityId = None
        self._ClientHangarSpace__selectedEmblemInfo = None

    
    def create(self, isPremium, spacePath, onSpaceLoadedCallback = None):
        BigWorld.drawSkySunAndMoon(False)
        type = self.getSpaceType(isPremium)
        self._ClientHangarSpace__selectHangarType(type)
        LOG_DEBUG('load hangar: hangar type = <{0:>s}>, space = <{1:>s}>'.format(type, spacePath))
        BigWorld.worldDrawEnabled(False)
        self._ClientHangarSpace__onLoadedCallback = onSpaceLoadedCallback
        self._ClientHangarSpace__spaceId = BigWorld.createSpace()
        
        try:
            self._ClientHangarSpace__spaceMappingId = BigWorld.addSpaceGeometryMapping(self._ClientHangarSpace__spaceId, None, spacePath)
        except ValueError:
            BigWorld.releaseSpace(self._ClientHangarSpace__spaceId)
            self._ClientHangarSpace__spaceMappingId = None
            self._ClientHangarSpace__spaceId = None
            LOG_CURRENT_EXCEPTION()
            return None

        self._ClientHangarSpace__vEntityId = BigWorld.createEntity('OfflineEntity', self._ClientHangarSpace__spaceId, 0, _V_START_POS, (_V_START_ANGLES[2], _V_START_ANGLES[1], _V_START_ANGLES[0]), dict())
        self._ClientHangarSpace__vAppearance = _VehicleAppearance(self._ClientHangarSpace__spaceId, self._ClientHangarSpace__vEntityId)
        self._ClientHangarSpace__setupCamera()
        self._ClientHangarSpace__waitCallback = BigWorld.callback(0.1, self._ClientHangarSpace__waitLoadingSpace)

    
    def getCamera(self):
        return self._ClientHangarSpace__cam

    
    def recreateVehicle(self, vDesc, vState, onVehicleLoadedCallback = None):
        if self._ClientHangarSpace__vAppearance is None:
            LOG_ERROR('ClientHangarSpace.recreateVehicle failed because hangar space has not been loaded correctly.')
            return None
        self._ClientHangarSpace__vAppearance.recreate(vDesc, vState, onVehicleLoadedCallback)
        self._ClientHangarSpace__boundingRadius = _calculateBoundingRadius(vDesc, _V_SCALE)
        dz = 0
        if self._ClientHangarSpace__cam.targetMaxDist > self._ClientHangarSpace__cam.pivotMaxDist:
            dz = (self._ClientHangarSpace__cam.pivotMaxDist - _CAM_START_DIST) / _CAM_SENS
        
        self.updateCameraByMouseMove(0, 0, dz)

    
    def removeVehicle(self):
        self._ClientHangarSpace__boundingRadius = None
        self._ClientHangarSpace__vAppearance.destroy()
        self._ClientHangarSpace__vAppearance = _VehicleAppearance(self._ClientHangarSpace__spaceId, self._ClientHangarSpace__vEntityId)
        BigWorld.entity(self._ClientHangarSpace__vEntityId).model = None
        self._ClientHangarSpace__selectedEmblemInfo = None

    
    def moveVehicleTo(self, position):
        
        try:
            vehicle = BigWorld.entity(self._ClientHangarSpace__vEntityId)
            vehicle.model.motors[0].signal = _createMatrix(_V_SCALE, _V_START_ANGLES, position)
        except Exception:
            LOG_CURRENT_EXCEPTION()


    
    def updateVehicleCamouflage(self, camouflageID = None):
        self._ClientHangarSpace__vAppearance.updateCamouflage(camouflageID = camouflageID)

    
    def updateVehicleSticker(self, model):
        self._ClientHangarSpace__vAppearance.updateVehicleSticker(model[0], model[1])

    
    def destroy(self):
        if self._ClientHangarSpace__waitCallback is not None and not self.spaceLoaded():
            self._ClientHangarSpace__destroyFunc = self._ClientHangarSpace__destroy
            return None
        self._ClientHangarSpace__destroy()

    
    def handleMouseEvent(self, dx, dy, dz):
        if not self.spaceLoaded():
            return False
        self.updateCameraByMouseMove(dx, dy, dz)

    
    def getCameraLocation(self):
        sourceMat = Math.Matrix(self._ClientHangarSpace__cam.source)
        targetMat = Math.Matrix(self._ClientHangarSpace__cam.target)
        return {
            'targetPos': targetMat.translation,
            'pivotPos': self._ClientHangarSpace__cam.pivotPosition,
            'yaw': sourceMat.yaw,
            'pitch': sourceMat.pitch,
            'dist': self._ClientHangarSpace__cam.pivotMaxDist }

    
    def setCameraLocation(self, targetPos = None, pivotPos = None, yaw = None, pitch = None, dist = None, ignoreConstraints = False):
        sourceMat = Math.Matrix(self._ClientHangarSpace__cam.source)
        if yaw is None:
            yaw = sourceMat.yaw
        
        if pitch is None:
            pitch = sourceMat.pitch
        
        if dist is None:
            dist = self._ClientHangarSpace__cam.pivotMaxDist
        
        if not ignoreConstraints:
            if yaw > 2 * math.pi:
                yaw -= 2 * math.pi
            elif yaw < -2 * math.pi:
                yaw += 2 * math.pi
            
            pitch = _clamp(math.radians(_CAM_PITCH_CONSTR[0]), math.radians(_CAM_PITCH_CONSTR[1]), pitch)
            dist = _clamp(_CAM_DIST_CONSTR[0], _CAM_DIST_CONSTR[1], dist)
            if self._ClientHangarSpace__boundingRadius is not None:
                if dist > self._ClientHangarSpace__boundingRadius + 1:
                    pass
                1
                dist = self._ClientHangarSpace__boundingRadius + 1
            
        
        mat = Math.Matrix()
        pitch = _clamp((-(math.pi) / 2) * 0.99, (math.pi / 2) * 0.99, pitch)
        mat.setRotateYPR((yaw, pitch, 0))
        self._ClientHangarSpace__cam.source = mat
        self._ClientHangarSpace__cam.pivotMaxDist = dist
        if targetPos is not None:
            self._ClientHangarSpace__cam.target.setTranslate(targetPos)
        
        if pivotPos is not None:
            self._ClientHangarSpace__cam.pivotPosition = pivotPos
        

    
    def locateCameraToPreview(self):
        self.setCameraLocation(targetPos = _PREVIEW_CAM_START_TARGET_POS, pivotPos = _PREVIEW_CAM_PIVOT_POS, yaw = math.radians(_PREVIEW_CAM_START_ANGLES[1]), pitch = math.radians(_PREVIEW_CAM_START_ANGLES[0]), dist = _PREVIEW_CAM_START_DIST)

    
    def locateCameraOnEmblem(self, onHull, emblemType, emblemIdx, relativeSize = 0.5):
        self._ClientHangarSpace__selectedEmblemInfo = (onHull, emblemType, emblemIdx, relativeSize)
        targetPosDirEmblem = self._ClientHangarSpace__vAppearance.getEmblemPos(onHull, emblemType, emblemIdx)
        if targetPosDirEmblem is None:
            return False
        dir = targetPosDirEmblem[1]
        emblemDesc = targetPosDirEmblem[2]
        emblemSize = emblemDesc[3]
        halfF = emblemSize / 2 * relativeSize
        dist = halfF / math.tan(BigWorld.projection().fov / 2)
        self.setCameraLocation(targetPosDirEmblem[0], Math.Vector3(0, 0, 0), dir.yaw, -(dir.pitch), dist, True)
        return True

    
    def clearSelectedEmblemInfo(self):
        self._ClientHangarSpace__selectedEmblemInfo = None

    
    def updateCameraByMouseMove(self, dx, dy, dz):
        sourceMat = Math.Matrix(self._ClientHangarSpace__cam.source)
        yaw = sourceMat.yaw
        pitch = sourceMat.pitch
        dist = self._ClientHangarSpace__cam.pivotMaxDist
        yaw += dx * _CAM_SENS
        pitch -= dy * _CAM_SENS
        dist -= dz * _CAM_SENS
        if yaw > 2 * math.pi:
            yaw -= 2 * math.pi
        elif yaw < -2 * math.pi:
            yaw += 2 * math.pi
        
        pitch = _clamp(math.radians(_CAM_PITCH_CONSTR[0]), math.radians(_CAM_PITCH_CONSTR[1]), pitch)
        prevDist = dist
        dist = _clamp(_CAM_DIST_CONSTR[0], _CAM_DIST_CONSTR[1], dist)
        if self._ClientHangarSpace__boundingRadius is not None:
            if dist > self._ClientHangarSpace__boundingRadius + 1:
                pass
            1
            dist = self._ClientHangarSpace__boundingRadius + 1
        
        if dist > prevDist and dz > 0:
            if self._ClientHangarSpace__selectedEmblemInfo is not None:
                self.locateCameraOnEmblem(*self._ClientHangarSpace__selectedEmblemInfo)
                return None
        
        mat = Math.Matrix()
        mat.setRotateYPR((yaw, pitch, 0))
        self._ClientHangarSpace__cam.source = mat
        self._ClientHangarSpace__cam.pivotMaxDist = dist

    
    def spaceLoaded(self):
        return not (self._ClientHangarSpace__loadingStatus < 1)

    
    def spaceLoading(self):
        return self._ClientHangarSpace__waitCallback is not None

    
    def getSpaceType(self, isPremium):
        if isPremium:
            return 'premium'
        return 'basic'

    
    def getDefSpacePath(self, isPremium):
        return _CFG[self.getSpaceType(isPremium)]['def_space_path']

    
    def getNationSpacePath(self, isPremium, nationName):
        cfg = _CFG[self.getSpaceType(isPremium)]
        return cfg['nation_space_paths'].get(nationName, cfg['def_space_path'])

    
    def _ClientHangarSpace__destroy(self):
        LOG_DEBUG('Hangar successfully destroyed.')
        if self._ClientHangarSpace__cam == BigWorld.camera():
            self._ClientHangarSpace__cam.spaceID = 0
            BigWorld.camera(None)
            BigWorld.worldDrawEnabled(False)
        
        self._ClientHangarSpace__cam = None
        self._ClientHangarSpace__loadingStatus = 0
        if self._ClientHangarSpace__vAppearance is not None:
            self._ClientHangarSpace__vAppearance.destroy()
            self._ClientHangarSpace__vAppearance = None
        
        self._ClientHangarSpace__onLoadedCallback = None
        self._ClientHangarSpace__boundingRadius = None
        if self._ClientHangarSpace__vEntityId is None:
            pass
        1
        entity = BigWorld.entity(self._ClientHangarSpace__vEntityId)
        BigWorld.drawSkySunAndMoon(True)
        BigWorld.SetDrawInflux(False)
        if self._ClientHangarSpace__spaceId is not None and BigWorld.isClientSpace(self._ClientHangarSpace__spaceId):
            if self._ClientHangarSpace__spaceMappingId is not None:
                BigWorld.delSpaceGeometryMapping(self._ClientHangarSpace__spaceId, self._ClientHangarSpace__spaceMappingId)
            
            BigWorld.clearSpace(self._ClientHangarSpace__spaceId)
            BigWorld.releaseSpace(self._ClientHangarSpace__spaceId)
        
        self._ClientHangarSpace__spaceMappingId = None
        self._ClientHangarSpace__spaceId = None
        if entity is None or not (entity.inWorld):
            return None
        BigWorld.destroyEntity(self._ClientHangarSpace__vEntityId)
        self._ClientHangarSpace__vEntityId = None

    
    def _ClientHangarSpace__setupCamera(self):
        self._ClientHangarSpace__cam = BigWorld.CursorCamera()
        self._ClientHangarSpace__cam.spaceID = self._ClientHangarSpace__spaceId
        self._ClientHangarSpace__cam.pivotMaxDist = _CAM_START_DIST
        self._ClientHangarSpace__cam.pivotMinDist = 0
        self._ClientHangarSpace__cam.maxDistHalfLife = _CAM_FLUENCY
        self._ClientHangarSpace__cam.turningHalfLife = _CAM_FLUENCY
        self._ClientHangarSpace__cam.movementHalfLife = 0
        self._ClientHangarSpace__cam.pivotPosition = _CAM_PIVOT_POS
        mat = Math.Matrix()
        mat.setRotateYPR((math.radians(_CAM_START_ANGLES[1]), math.radians(_CAM_START_ANGLES[0]), 0))
        self._ClientHangarSpace__cam.source = mat
        mat = Math.Matrix()
        mat.setTranslate(_CAM_START_TARGET_POS)
        self._ClientHangarSpace__cam.target = mat
        BigWorld.camera(self._ClientHangarSpace__cam)

    
    def _ClientHangarSpace__waitLoadingSpace(self):
        self._ClientHangarSpace__waitCallback = None
        self._ClientHangarSpace__loadingStatus = BigWorld.spaceLoadStatus()
        if not BigWorld.worldDrawEnabled():
            BigWorld.worldDrawEnabled(True)
        
        if self._ClientHangarSpace__loadingStatus < 1:
            self._ClientHangarSpace__waitCallback = BigWorld.callback(0.1, self._ClientHangarSpace__waitLoadingSpace)
        else:
            g_critMemHandler.restore()
            if self._ClientHangarSpace__onLoadedCallback is not None:
                self._ClientHangarSpace__onLoadedCallback()
                self._ClientHangarSpace__onLoadedCallback = None
            
            if self._ClientHangarSpace__destroyFunc:
                self._ClientHangarSpace__destroyFunc()
                self._ClientHangarSpace__destroyFunc = None
            

    
    def _ClientHangarSpace__selectHangarType(self, type):
        global _V_SCALE, _V_START_ANGLES, _V_START_POS, _CAM_START_DIST, _CAM_START_ANGLES, _CAM_START_TARGET_POS, _CAM_DIST_CONSTR, _CAM_PITCH_CONSTR, _CAM_SENS, _CAM_PIVOT_POS, _CAM_FLUENCY, _EMBLEMS_ALPHA_DAMAGED, _EMBLEMS_ALPHA_UNDAMAGED, _SHADOW_LIGHT_DIR, _PREVIEW_CAM_START_DIST, _PREVIEW_CAM_START_ANGLES, _PREVIEW_CAM_PIVOT_POS, _PREVIEW_CAM_START_TARGET_POS
        cfg = _CFG[type]
        _V_SCALE = cfg['v_scale']
        _V_START_ANGLES = _degToRadVec3(cfg['v_start_angles'])
        _V_START_POS = cfg['v_start_pos']
        _CAM_START_DIST = cfg['cam_start_dist']
        _CAM_START_ANGLES = cfg['cam_start_angles']
        _CAM_START_TARGET_POS = cfg['cam_start_target_pos']
        _CAM_DIST_CONSTR = cfg['cam_dist_constr']
        _CAM_PITCH_CONSTR = cfg['cam_pitch_constr']
        _CAM_SENS = cfg['cam_sens']
        _CAM_PIVOT_POS = cfg['cam_pivot_pos']
        _CAM_FLUENCY = cfg['cam_fluency']
        _EMBLEMS_ALPHA_DAMAGED = cfg['emblems_alpha_damaged']
        _EMBLEMS_ALPHA_UNDAMAGED = cfg['emblems_alpha_undamaged']
        _SHADOW_LIGHT_DIR = cfg['shadow_light_dir']
        _PREVIEW_CAM_START_DIST = cfg['preview_cam_start_dist']
        _PREVIEW_CAM_START_ANGLES = cfg['preview_cam_start_angles']
        _PREVIEW_CAM_PIVOT_POS = cfg['preview_cam_pivot_pos']
        _PREVIEW_CAM_START_TARGET_POS = cfg['preview_cam_start_target_pos']



class _VehicleAppearance:
    _VehicleAppearance__ROOT_NODE_NAME = 'V'
    
    def __init__(self, spaceId, vEntityId):
        self._VehicleAppearance__isLoaded = False
        self._VehicleAppearance__curBuildInd = 0
        self._VehicleAppearance__vDesc = None
        self._VehicleAppearance__spaceId = spaceId
        self._VehicleAppearance__vEntityId = vEntityId
        self._VehicleAppearance__onLoadedCallback = None
        self._VehicleAppearance__emblemsAlpha = _EMBLEMS_ALPHA_UNDAMAGED
        self._VehicleAppearance__models = ()
        self._VehicleAppearance__stickers = []
        self._VehicleAppearance__isVehicleDestroyed = False
        self._VehicleAppearance__smCb = None

    
    def recreate(self, vDesc, vState, onVehicleLoadedCallback = None):
        self._VehicleAppearance__onLoadedCallback = onVehicleLoadedCallback
        self._VehicleAppearance__isLoaded = False
        self._VehicleAppearance__startBuild(vDesc, vState)

    
    def destroy(self):
        self._VehicleAppearance__onLoadedCallback = None
        self._VehicleAppearance__vDesc = None
        self._VehicleAppearance__isLoaded = False
        self._VehicleAppearance__curBuildInd = 0
        self._VehicleAppearance__vEntityId = None
        if self._VehicleAppearance__smCb is not None:
            BigWorld.cancelCallback(self._VehicleAppearance__smCb)
            self._VehicleAppearance__smCb = None
        

    
    def isLoaded(self):
        return self._VehicleAppearance__isLoaded

    
    def _VehicleAppearance__startBuild(self, vDesc, vState):
        self._VehicleAppearance__curBuildInd += 1
        self._VehicleAppearance__vDesc = vDesc
        self._VehicleAppearance__resources = { }
        self._VehicleAppearance__stickers = []
        self._VehicleAppearance__componentIDs = {
            'chassis': vDesc.chassis['models'][vState],
            'hull': vDesc.hull['models'][vState],
            'turret': vDesc.turret['models'][vState],
            'gun': vDesc.gun['models'][vState],
            'camouflageExclusionMask': vDesc.type.camouflageExclusionMask }
        customization = items.vehicles.g_cache.customization(vDesc.type.id[0])
        if vDesc.camouflage is not None and customization is not None:
            camouflageId = vDesc.camouflage[0]
            camouflageDesc = customization['camouflages'].get(camouflageId)
            if camouflageDesc is not None:
                self._VehicleAppearance__componentIDs['camouflageTexture'] = camouflageDesc['texture']
            
        
        if vState == 'undamaged':
            self._VehicleAppearance__emblemsAlpha = _EMBLEMS_ALPHA_UNDAMAGED
            self._VehicleAppearance__isVehicleDestroyed = False
        else:
            self._VehicleAppearance__emblemsAlpha = _EMBLEMS_ALPHA_DAMAGED
            self._VehicleAppearance__isVehicleDestroyed = True
        resources = self._VehicleAppearance__componentIDs.values()
        BigWorld.loadResourceListBG(tuple(resources), partial(self._VehicleAppearance__onResourcesLoaded, self._VehicleAppearance__curBuildInd))

    
    def _VehicleAppearance__onResourcesLoaded(self, buildInd, resourceRefs):
        if buildInd != self._VehicleAppearance__curBuildInd:
            return None
        failedIDs = resourceRefs.failedIDs
        resources = self._VehicleAppearance__resources
        succesLoaded = True
        for (resID, resource) in resourceRefs.items():
            if resID not in failedIDs:
                resources[resID] = resource
                continue
            buildInd != self._VehicleAppearance__curBuildInd
            LOG_ERROR('Could not load %s' % resID)
            succesLoaded = False
        
        if succesLoaded:
            self._VehicleAppearance__setupModel(buildInd)
        

    
    def _VehicleAppearance__assembleModel(self):
        resources = self._VehicleAppearance__resources
        compIDs = self._VehicleAppearance__componentIDs
        chassis = resources[compIDs['chassis']]
        hull = resources[compIDs['hull']]
        turret = resources[compIDs['turret']]
        gun = resources[compIDs['gun']]
        self._VehicleAppearance__models = (chassis, hull, turret, gun)
        chassis.node(self._VehicleAppearance__ROOT_NODE_NAME).attach(hull)
        hull.node('HP_turretJoint').attach(turret)
        turret.node('HP_gunJoint').attach(gun)
        self._VehicleAppearance__setupEmblems(self._VehicleAppearance__vDesc)
        for (sticker, alpha) in self._VehicleAppearance__stickers:
            sticker.setAlphas(0, 0)
        
        for model in self._VehicleAppearance__models:
            model.visible = False
            model.visibleAttachments = True
        
        return chassis

    
    def _VehicleAppearance__setupHangarShadowMap(self):
        if BigWorld.spaceLoadStatus() < 1:
            self._VehicleAppearance__smCb = BigWorld.callback(0, self._VehicleAppearance__setupHangarShadowMap)
            return None
        self._VehicleAppearance__smCb = None
        vehiclePath = self._VehicleAppearance__vDesc.chassis['models']['undamaged']
        vehiclePath = vehiclePath[:vehiclePath.rfind('/normal')]
        dsVehicle = ResMgr.openSection(vehiclePath)
        shadowMapTexFileName = _HANGAR_FAKESHADOWMAP_DEFAULT_TEX_NAME
        if dsVehicle is not None:
            for (fileName, _) in dsVehicle.items():
                if fileName.lower().find('_hangarshadowmap.dds') != -1:
                    shadowMapTexFileName = vehiclePath + '/' + fileName
                    continue
                BigWorld.spaceLoadStatus() < 1
            
        
        BigWorld.wg_setChunkModelTexture(BigWorld.camera().spaceID, 0, 0, _HANGAR_FAKESHADOWMAP_MODEL_NAME, 'diffuseMap', shadowMapTexFileName)

    
    def _VehicleAppearance__setupEmblems(self, vDesc):
        for (vehicleStickers, _) in self._VehicleAppearance__stickers:
            vehicleStickers.detachStickers()
        
        chassis = self._VehicleAppearance__models[0]
        hull = self._VehicleAppearance__models[1]
        turret = self._VehicleAppearance__models[2]
        gun = self._VehicleAppearance__models[3]
        emblemAlpha = self._VehicleAppearance__emblemsAlpha * vDesc.type.emblemsAlpha
        if vDesc.turret['showEmblemsOnGun']:
            pass
        1
        emblemPositions = (gun, (turret, hull.node('HP_turretJoint'), vDesc.turret['emblemSlots']))
        for (targetModel, parentNode, slots) in emblemPositions:
            sticker = VehicleStickers.VehicleStickers(vDesc, slots, targetModel == hull, self._VehicleAppearance__resources)
            sticker.setAlphas(emblemAlpha, emblemAlpha)
            sticker.attachStickers(targetModel, parentNode, self._VehicleAppearance__isVehicleDestroyed)
            self._VehicleAppearance__stickers.append((sticker, emblemAlpha))
        
        BigWorld.player().stats.get('clanDBID', self._VehicleAppearance__onClanDBIDRetrieved)

    
    def updateVehicleSticker(self, playerEmblems, playerInscriptions):
        initialEmblems = copy.copy(self._VehicleAppearance__vDesc.playerEmblems)
        initialInscriptions = copy.copy(self._VehicleAppearance__vDesc.playerInscriptions)
        for (emblemId, startTime, duration) in enumerate(playerEmblems):
            self._VehicleAppearance__vDesc.setPlayerEmblem(idx, emblemId, startTime, duration)
        
        for (inscriptionId, startTime, duration, color) in enumerate(playerInscriptions):
            self._VehicleAppearance__vDesc.setPlayerInscription(idx, inscriptionId, startTime, duration, color)
        
        self._VehicleAppearance__setupEmblems(self._VehicleAppearance__vDesc)
        self._VehicleAppearance__vDesc.playerEmblems = initialEmblems
        self._VehicleAppearance__vDesc.playerInscriptions = initialInscriptions

    
    def _VehicleAppearance__onClanDBIDRetrieved(self, _, clanID):
        for (sticker, _) in self._VehicleAppearance__stickers:
            sticker.setClanID(clanID)
        

    
    def _VehicleAppearance__setupModel(self, buildIdx):
        model = self._VehicleAppearance__assembleModel()
        model.addMotor(BigWorld.Servo(_createMatrix(_V_SCALE, _V_START_ANGLES, _V_START_POS)))
        BigWorld.addModel(model)
        BigWorld.callback(0, partial(self._VehicleAppearance__doFinalSetup, buildIdx, model, True))

    
    def _VehicleAppearance__doFinalSetup(self, buildIdx, model, delModel):
        if delModel:
            BigWorld.delModel(model)
        
        if model.attached:
            BigWorld.callback(0, partial(self._VehicleAppearance__doFinalSetup, buildIdx, model, False))
            return None
        if buildIdx != self._VehicleAppearance__curBuildInd:
            return None
        entity = BigWorld.entity(self._VehicleAppearance__vEntityId)
        if entity:
            for m in self._VehicleAppearance__models:
                m.visible = True
                m.visibleAttachments = True
            
            for (sticker, alpha) in self._VehicleAppearance__stickers:
                sticker.setAlphas(alpha, alpha)
            
            entity.model = model
            entity.model.delMotor(entity.model.motors[0])
            entity.model.addMotor(BigWorld.Servo(_createMatrix(_V_SCALE, _V_START_ANGLES, _V_START_POS)))
            if self._VehicleAppearance__onLoadedCallback is not None:
                self._VehicleAppearance__onLoadedCallback()
                self._VehicleAppearance__onLoadedCallback = None
            
            self.updateCamouflage()
            if self._VehicleAppearance__smCb is None:
                self._VehicleAppearance__setupHangarShadowMap()
            
        
        if self._VehicleAppearance__vDesc is not None and 'observer' in self._VehicleAppearance__vDesc.type.tags:
            model.visible = False
            model.visibleAttachments = False
        

    
    def getEmblemPos(self, onHull, emblemType, emblemIdx):
        model = None
        emblemsDesc = None
        hitTester = ModelHitTester()
        worldMat = None
        chassis = self._VehicleAppearance__models[0]
        if onHull:
            model = self._VehicleAppearance__models[1]
            hitTester.bspModelName = self._VehicleAppearance__vDesc.hull['models']['undamaged']
            emblemsDesc = self._VehicleAppearance__vDesc.hull['emblemSlots']
            worldMat = Math.Matrix(model.matrix)
        elif self._VehicleAppearance__vDesc.turret['showEmblemsOnGun']:
            model = self._VehicleAppearance__models[3]
            hitTester.bspModelName = self._VehicleAppearance__vDesc.gun['models']['undamaged']
        else:
            model = self._VehicleAppearance__models[2]
            hitTester.bspModelName = self._VehicleAppearance__vDesc.turret['models']['undamaged']
        emblemsDesc = self._VehicleAppearance__vDesc.turret['emblemSlots']
        worldMat = Math.Matrix(model.matrix)
        if model is None:
            return None
        continue
        desiredEmblems = _[1]
        if emblemIdx >= len(desiredEmblems):
            return None
        emblem = desiredEmblems[emblemIdx]
        dir = emblem[1] - emblem[0]
        dir.normalise()
        startPos = emblem[0] - dir * 5
        endPos = emblem[1] + dir * 5
        hitTester.loadBspModel()
        collideRes = hitTester.localHitTest(startPos, endPos)
        hitTester.releaseBspModel()
        if collideRes is not None:
            collideRes = sorted(collideRes, (lambda t1, t2: cmp(t1[0], t2[0])))
            distanceFromStart = collideRes[0][0]
            normal = collideRes[0][1]
            hitPos = startPos + dir * distanceFromStart
            hitPos = worldMat.applyPoint(hitPos)
            dir = -worldMat.applyVector(normal)
            dir.normalise()
            if abs(dir.pitch - math.pi / 2) < 0.0001:
                upVecWorld = worldMat.applyVector(emblem[2])
                upVecWorld.normalise()
                dir += upVecWorld * 0.001
            
            return (hitPos, dir, emblem)
        return None

    
    def updateCamouflage(self, camouflageID = None):
        texture = ''
        colors = [
            0,
            0,
            0,
            0]
        weights = Math.Vector4(1, 0, 0, 0)
        camouflagePresent = True
        vDesc = self._VehicleAppearance__vDesc
        if vDesc is None:
            return None
        if camouflageID is None and vDesc.camouflages is not None:
            camouflageID = vDesc.camouflages[g_tankActiveCamouflage.get(vDesc.type.compactDescr, 0)][0]
        
        customization = items.vehicles.g_cache.customization(vDesc.type.id[0])
        defaultTiling = None
        if camouflageID is not None and customization is not None:
            camouflage = customization['camouflages'].get(camouflageID)
            if camouflage is not None:
                camouflagePresent = True
                texture = camouflage['texture']
                colors = camouflage['colors']
                weights = Math.Vector4((colors[0] >> 24) / 255, (colors[1] >> 24) / 255, (colors[2] >> 24) / 255, (colors[3] >> 24) / 255)
                defaultTiling = camouflage['tiling'].get(vDesc.type.compactDescr)
            
        
        if self._VehicleAppearance__isVehicleDestroyed:
            weights *= 0.1
        
        if vDesc.camouflage is not None:
            (_, camStartTime, camNumDays) = vDesc.camouflage
            if camNumDays > 0:
                timeAmount = (time.time() - camStartTime) / camNumDays * 86400
                if timeAmount > 1:
                    weights *= _CAMOUFLAGE_MIN_INTENSITY
                elif timeAmount > 0:
                    weights *= (1 - timeAmount) * (1 - _CAMOUFLAGE_MIN_INTENSITY) + _CAMOUFLAGE_MIN_INTENSITY
                
            
        
        for model in self._VehicleAppearance__models:
            exclusionMap = vDesc.type.camouflageExclusionMask
            tiling = defaultTiling
            if tiling is None:
                tiling = vDesc.type.camouflageTiling
            
            tgDesc = None
            if model == self._VehicleAppearance__models[2]:
                tgDesc = vDesc.turret
            elif model == self._VehicleAppearance__models[3]:
                tgDesc = vDesc.gun
            
            if tgDesc is not None:
                coeff = tgDesc.get('camouflageTiling')
                if coeff is not None:
                    if tiling is not None:
                        tiling = (tiling[0] * coeff[0], tiling[1] * coeff[1], tiling[2] * coeff[2], tiling[3] * coeff[3])
                    else:
                        tiling = coeff
                
                if tgDesc.has_key('camouflageExclusionMask'):
                    exclusionMap = tgDesc['camouflageExclusionMask']
                
            
            if not camouflagePresent and exclusionMap == '' or texture == '':
                if hasattr(model, 'wg_fashion'):
                    delattr(model, 'wg_fashion')
                
            hasattr(model, 'wg_fashion')
            if not hasattr(model, 'wg_fashion'):
                if model == self._VehicleAppearance__models[0]:
                    tracksCfg = vDesc.chassis['tracks']
                    fashion = BigWorld.WGVehicleFashion()
                    fashion.setTracks(tracksCfg['leftMaterial'], tracksCfg['rightMaterial'], tracksCfg['textureScale'])
                    model.wg_fashion = fashion
                else:
                    model.wg_fashion = BigWorld.WGBaseFashion()
            
            model.wg_fashion.setCamouflage(texture, exclusionMap, tiling, colors[0], colors[1], colors[2], colors[3], weights)
        



class _ClientHangarSpacePathOverride:
    
    def __init__(self):
        g_playerEvents.onEventNotificationsChanged += self._ClientHangarSpacePathOverride__onEventNotificationsChanged
        connectionManager.onDisconnected += self._ClientHangarSpacePathOverride__onDisconnected

    
    def destroy(self):
        g_playerEvents.onEventNotificationsChanged -= self._ClientHangarSpacePathOverride__onEventNotificationsChanged
        connectionManager.onDisconnected -= self._ClientHangarSpacePathOverride__onDisconnected

    
    def _ClientHangarSpacePathOverride__changeHangarPath(self, isPremium, path):
        if isPremium:
            pass
        1
        'premium'['basic']['def_space_path'] = _CFG

    
    def _ClientHangarSpacePathOverride__onDisconnected(self):
        self._ClientHangarSpacePathOverride__changeHangarPath(False, _DEFAULT_HANGAR_SPACE_PATH)
        self._ClientHangarSpacePathOverride__changeHangarPath(True, _DEFAULT_HANGAR_PREM_SPACE_PATH)

    
    def _ClientHangarSpacePathOverride__onEventNotificationsChanged(self, notificationsDiff):
        g_hangarSpace = g_hangarSpace
        import gui.Scaleform.utils.HangarSpace
        isPremium = g_hangarSpace.isPremium
        hasChanged = False
        for notification in notificationsDiff['removed']:
            if notification['type'] == _SERVER_CMD_CHANGE_HANGAR:
                self._ClientHangarSpacePathOverride__changeHangarPath(False, _DEFAULT_HANGAR_SPACE_PATH)
                if not isPremium:
                    hasChanged = True
                
            if notification['type'] == _SERVER_CMD_CHANGE_HANGAR_PREM:
                self._ClientHangarSpacePathOverride__changeHangarPath(True, _DEFAULT_HANGAR_PREM_SPACE_PATH)
                if isPremium:
                    hasChanged = True
                
        
        for notification in notificationsDiff['added']:
            if not notification.has_key('data') or notification['data'] == '':
                continue
            
            if notification['type'] == _SERVER_CMD_CHANGE_HANGAR:
                self._ClientHangarSpacePathOverride__changeHangarPath(False, notification['data'])
                if not isPremium:
                    hasChanged = True
                
            if notification['type'] == _SERVER_CMD_CHANGE_HANGAR_PREM:
                self._ClientHangarSpacePathOverride__changeHangarPath(True, notification['data'])
                if isPremium:
                    hasChanged = True
                
        
        if hasChanged:
            g_hangarSpace.refreshSpace(isPremium)
        


g_clientHangarSpaceOverride = _ClientHangarSpacePathOverride()

def _createMatrix(scale, angles, pos):
    mat = Math.Matrix()
    mat.setScale((scale, scale, scale))
    mat2 = Math.Matrix()
    mat2.setTranslate(pos)
    mat3 = Math.Matrix()
    mat3.setRotateYPR(angles)
    mat.preMultiply(mat3)
    mat.postMultiply(mat2)
    return mat


def _clamp(minVal, maxVal, val):
    tmpVal = max(minVal, val)
    tmpVal = min(maxVal, tmpVal)
    return tmpVal


def _calculateBoundingRadius(vehDescr, scale):
    hitTester = vehDescr.type.hull['hitTester']
    hitTester.loadBspModel()
    boundingRadius = hitTester.bbox[2] * scale
    hitTester.releaseBspModel()
    return boundingRadius


def _degToRadVec3(inVec):
    outVec = Math.Vector3()
    for i in range(0, 3):
        outVec[i] = math.radians(inVec[i])
    
    return outVec


