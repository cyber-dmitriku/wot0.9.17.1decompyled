# Source Generated with Decompyle++
# File: OfflineMapCreator.pyc (Python 2.6)

import BigWorld
import Math
import Keys
import GUI
from debug_utils import *
from functools import partial
import items.vehicles as items
import math
import AccountSyncData
import Account
from account_helpers import Inventory, Stats, Shop
import constants
import ResMgr
_CFG = {
    'basic': {
        'v_scale': 1.3,
        'v_start_angles': Math.Vector3(0, 0, 0),
        'v_start_pos': Math.Vector3(50, 0, 50),
        'cam_start_dist': 9,
        'cam_start_angles': [
            -25,
            110],
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
        'shadow_light_dir': (0.55, -1, -1.7) } }
_SPACE_NAME = None
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

class OfflineMapCreator:
    
    def __init__(self):
        self._OfflineMapCreator__spaceId = None
        self._OfflineMapCreator__accountID = None
        self._OfflineMapCreator__cam = None
        self._OfflineMapCreator__waitCallback = None
        self._OfflineMapCreator__loadingStatus = 0
        self._OfflineMapCreator__destroyFunc = None
        self._OfflineMapCreator__spaceMappingId = None
        self._OfflineMapCreator__vEntityId = None
        self._OfflineMapCreator__isActive = False
        self._loadListArenaNames()
        self._OfflineMapCreator__arenaTypeID = 0

    
    def create(self, mapName):
        
        try:
            LOG_DEBUG('OfflineMapCreator.Create( %s )' % mapName)
            g_windowsManager = g_windowsManager
            import gui.WindowsManager
            g_windowsManager.showBattle()
            cfgType = 'basic'
            self._OfflineMapCreator__loadCfg(cfgType, mapName)
            BigWorld.worldDrawEnabled(False)
            BigWorld.setWatcher('Visibility/GUI', False)
            self._OfflineMapCreator__spaceId = BigWorld.createSpace()
            self._OfflineMapCreator__spaceMappingId = BigWorld.addSpaceGeometryMapping(self._OfflineMapCreator__spaceId, None, 'spaces/' + mapName)
            self._OfflineMapCreator__isActive = True
            self._OfflineMapCreator__arenaTypeID = self._arenaTypeIDByArenaName.get(mapName)
            self._OfflineMapCreator__accountID = BigWorld.createEntity('Account', self._OfflineMapCreator__spaceId, 0, _V_START_POS, (_V_START_ANGLES[2], _V_START_ANGLES[1], _V_START_ANGLES[0]), dict())
            self._OfflineMapCreator__spaceMappingId = BigWorld.addSpaceGeometryMapping(self._OfflineMapCreator__spaceId, None, 'spaces/' + mapName)
            self._OfflineMapCreator__vEntityId = BigWorld.createEntity('Avatar', self._OfflineMapCreator__spaceId, 0, _V_START_POS, (_V_START_ANGLES[2], _V_START_ANGLES[1], _V_START_ANGLES[0]), dict())
            BigWorld.player(BigWorld.entities[self._OfflineMapCreator__vEntityId])
            self._OfflineMapCreator__setupCamera()
            BigWorld.worldDrawEnabled(True)
        except:
            LOG_DEBUG('OfflineMapCreator.Create( %s ): FAILED with: ' % mapName)
            LOG_CURRENT_EXCEPTION()
            self.cancel()


    
    def destroy(self):
        
        try:
            LOG_DEBUG('OfflineMapCreator.destroy()')
            self._OfflineMapCreator__isActive = False
            BigWorld.worldDrawEnabled(False)
            BigWorld.setWatcher('Visibility/GUI', True)
            self._OfflineMapCreator__spaceMappingId = 0
            BigWorld.cameraSpaceID(0)
            BigWorld.camera(None)
            self._OfflineMapCreator__cam = None
            BigWorld.clearEntitiesAndSpaces()
            BigWorld.releaseSpace(self._OfflineMapCreator__spaceId)
            self._OfflineMapCreator__spaceId = 0
            self._OfflineMapCreator__arenaTypeID = 0
            accountId = 0
            self._OfflineMapCreator__vEntityId = 0
            BigWorld.worldDrawEnabled(True)
        except:
            LOG_DEBUG('OfflineMapCreator.destroy(): FAILED with: ')
            LOG_CURRENT_EXCEPTION()
            self.cancel()


    
    def reset(self):
        LOG_DEBUG('OfflineMapCreator.reset()')
        self.destroy()
        self._OfflineMapCreator__isActive = True

    
    def cancel(self):
        self._OfflineMapCreator__spaceId = 0
        self._OfflineMapCreator__spaceMappingId = 0
        self._OfflineMapCreator__vEntityId = 0
        self._OfflineMapCreator__isActive = False
        BigWorld.setWatcher('Visibility/GUI', True)
        BigWorld.worldDrawEnabled(True)

    
    def _clamp(self, minVal, maxVal, val):
        tmpVal = val
        tmpVal = max(minVal, val)
        tmpVal = min(maxVal, tmpVal)
        return tmpVal

    
    def Active(self):
        return self._OfflineMapCreator__isActive

    
    def SetActive(self, _active):
        self._OfflineMapCreator__isActive = _active

    
    def arenaId(self):
        return self._OfflineMapCreator__arenaTypeID

    
    def _loadListArenaNames(self):
        self._arenaTypeIDByArenaName = { }
        ds = ResMgr.openSection(constants.ARENA_TYPE_XML_PATH + '_list_.xml')
        if ds is not None:
            for sec in ds.values():
                _OfflineMapCreator__arenaTypeID = sec.readInt('id')
                arenaName = sec.readString('name')
                self._arenaTypeIDByArenaName[arenaName] = _OfflineMapCreator__arenaTypeID
            
        

    
    def _OfflineMapCreator__setupCamera(self):
        self._OfflineMapCreator__cam = BigWorld.CursorCamera()
        self._OfflineMapCreator__cam.spaceID = self._OfflineMapCreator__spaceId
        self._OfflineMapCreator__cam.pivotMaxDist = _CAM_START_DIST
        self._OfflineMapCreator__cam.maxDistHalfLife = _CAM_FLUENCY
        self._OfflineMapCreator__cam.turningHalfLife = _CAM_FLUENCY
        self._OfflineMapCreator__cam.movementHalfLife = 0
        self._OfflineMapCreator__cam.pivotPosition = _CAM_PIVOT_POS
        mat = Math.Matrix()
        mat.setRotateYPR((math.radians(_CAM_START_ANGLES[1]), math.radians(_CAM_START_ANGLES[0]), 0))
        self._OfflineMapCreator__cam.source = mat
        mat = Math.Matrix()
        mat.setTranslate(_CAM_START_TARGET_POS)
        self._OfflineMapCreator__cam.target = mat
        LOG_DEBUG('camera')
        BigWorld.camera(self._OfflineMapCreator__cam)

    
    def _OfflineMapCreator__loadCfg(self, type, mapName):
        global _SPACE_NAME, _V_SCALE, _V_START_ANGLES, _V_START_POS, _CAM_START_DIST, _CAM_START_ANGLES, _CAM_START_TARGET_POS, _CAM_DIST_CONSTR, _CAM_PITCH_CONSTR, _CAM_SENS, _CAM_PIVOT_POS, _CAM_FLUENCY, _EMBLEMS_ALPHA_DAMAGED, _EMBLEMS_ALPHA_UNDAMAGED, _SHADOW_LIGHT_DIR
        cfg = _CFG[type]
        _SPACE_NAME = mapName
        _V_SCALE = cfg['v_scale']
        _V_START_ANGLES = cfg['v_start_angles']
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


g_offlineMapCreator = OfflineMapCreator()

