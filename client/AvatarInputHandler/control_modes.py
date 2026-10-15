# Source Generated with Decompyle++
# File: control_modes.pyc (Python 2.6)

import BigWorld
import Math
import Keys
import GUI
import math
import stat
import weakref
import string
import cameras
import aims
import CommandMapping
import constants
import BattleReplay
from post_processing import g_postProcessing
from constants import AIMING_MODE
from gui import DEPTH_OF_Binoculars
from gui import DEPTH_OF_GunMarker
from gui.Scaleform.Flash import Flash
from debug_utils import *
from ProjectileMover import collideDynamicAndStatic, collideDynamic
from PlayerEvents import g_playerEvents
from PostmortemDelay import PostmortemDelay
from account_helpers.AccountSettings import AccountSettings
import gun_rotation_shared
_ARCADE_CAM_PIVOT_POS = Math.Vector3(0, 4, 3)

class IControlMode:
    
    def prerequisites(self):
        return []

    
    def create(self):
        pass

    
    def destroy(self):
        pass

    
    def dumpState(self):
        pass

    
    def enable(self, **args):
        pass

    
    def disable(self):
        pass

    
    def handleKeyEvent(self, isDown, key, mods, event = None):
        pass

    
    def handleMouseEvent(self, dx, dy, dz):
        pass

    
    def showGunMarker(self, flag):
        pass

    
    def showGunMarker2(self, flag):
        pass

    
    def updateGunMarker(self, pos, dir, size, relaxTime, collData):
        pass

    
    def updateGunMarker2(self, pos, dir, size, relaxTime, collData):
        pass

    
    def setAimingMode(self, enable, mode):
        pass

    
    def getDesiredShotPoint(self):
        pass

    
    def updateShootingStatus(self, canShoot):
        pass

    
    def updateTrajectory(self):
        pass

    
    def onRecreateDevice(self):
        pass

    
    def getAim(self):
        pass

    
    def setReloading(self, duration, startTime):
        pass

    
    def setGUIVisible(self, isVisible):
        pass

    
    def selectPlayer(self, index):
        pass

    
    def onMinimapClicked(self, worldPos):
        pass

    
    def isSelfVehicle(self):
        return True

    
    def isManualBind(self):
        return False

    
    def getFixedAutorotation(self):
        pass



class DebugControlMode(IControlMode):
    
    def __init__(self, dataSection, avatarInputHandler):
        self._DebugControlMode__aih = weakref.proxy(avatarInputHandler)
        self._DebugControlMode__cam = cameras.FreeCamera()
        self._DebugControlMode__isCreated = False
        self._DebugControlMode__isEnabled = False
        self._DebugControlMode__prevModeName = None
        self._DebugControlMode__videoControl = None

    
    def prerequisites(self):
        return []

    
    def create(self):
        self._DebugControlMode__isCreated = True

    
    def destroy(self):
        self.disable()
        self._DebugControlMode__cam.destroy()
        self._DebugControlMode__cam = None
        self._DebugControlMode__isCreated = False

    
    def dumpState(self):
        return dumpStateEmpty()

    
    def enable(self, **args):
        ctrlState = args.get('ctrlState')
        self._DebugControlMode__prevModeName = args.get('prevModeName')
        camMatrix = args.get('camMatrix')
        self._DebugControlMode__cam.enable(camMatrix)
        BigWorld.setWatcher('Client Settings/Strafe Rate', 50)
        BigWorld.setWatcher('Client Settings/Camera Mass', 1)
        if not constants.IS_DEVELOPMENT:
            raise AssertionError
        import Cat as Cat
        Cat.Tasks.VideoEngineer.SetEnable(True)
        self._DebugControlMode__videoControl = Cat.Tasks.VideoEngineer.VideoControl(self._DebugControlMode__cam)
        self._DebugControlMode__videoControl.setEnable(True)
        self._DebugControlMode__isEnabled = True
        g_postProcessing.enable('debug')

    
    def disable(self):
        self._DebugControlMode__isEnabled = False
        if self._DebugControlMode__videoControl is not None:
            self._DebugControlMode__videoControl.setEnable(False)
            self._DebugControlMode__videoControl.destroy()
            self._DebugControlMode__videoControl = None
        
        self._DebugControlMode__cam.disable()
        g_postProcessing.disable()

    
    def handleKeyEvent(self, isDown, key, mods, event = None):
        if not self._DebugControlMode__isEnabled:
            raise AssertionError
        if BigWorld.isKeyDown(Keys.KEY_CAPSLOCK) and constants.IS_DEVELOPMENT and isDown and key == Keys.KEY_F1:
            self._DebugControlMode__aih.onControlModeChanged(self._DebugControlMode__prevModeName)
            return True
        if self._DebugControlMode__videoControl.handleKeyEvent(isDown, key, mods, event):
            return True
        return self._DebugControlMode__cam.handleKey(event)

    
    def handleMouseEvent(self, dx, dy, dz):
        if not self._DebugControlMode__isEnabled:
            raise AssertionError
        GUI.mcursor().position = (0, 0)
        return self._DebugControlMode__videoControl.handleMouseEvent(dx, dy, dz)

    
    def getDesiredShotPoint(self):
        if not self._DebugControlMode__isEnabled:
            raise AssertionError

    
    def updateShootingStatus(self, canShot):
        if not self._DebugControlMode__isEnabled:
            raise AssertionError

    
    def setCameraPosition(self, x, y, z):
        mat = Math.Matrix()
        mat.lookAt(Math.Vector3(x, y, z), (0, 0, 1), (0, 1, 0))
        self._DebugControlMode__cam.camera.set(mat)

    
    def getDebugVideoControl(self):
        return self._DebugControlMode__videoControl

    
    def isManualBind(self):
        return True



class CatControlMode(IControlMode):
    
    def __init__(self, dataSection, avatarInputHandler):
        self._CatControlMode__aih = weakref.proxy(avatarInputHandler)
        self._CatControlMode__cam = cameras.FreeCamera()
        self._CatControlMode__isCreated = False
        self._CatControlMode__isEnabled = False
        self._CatControlMode__shellingControl = None
        self._CatControlMode__sens = (3, 3, 3)

    
    def prerequisites(self):
        return []

    
    def create(self):
        self._CatControlMode__shellingControl = _ShellingControl(self._CatControlMode__cam)
        self._CatControlMode__isCreated = True

    
    def destroy(self):
        self.disable()
        self._CatControlMode__shellingControl.destroy()
        self._CatControlMode__shellingControl = None
        self._CatControlMode__cam.destroy()
        self._CatControlMode__cam = None
        self._CatControlMode__isCreated = False

    
    def dumpState(self):
        return dumpStateEmpty()

    
    def enable(self, **args):
        ctrlState = args.get('ctrlState')
        camMatrix = args.get('camMatrix')
        self._CatControlMode__cam.enable(camMatrix)
        BigWorld.setWatcher('Client Settings/Strafe Rate', 50)
        BigWorld.setWatcher('Client Settings/Camera Mass', 1)
        self._CatControlMode__shellingControl.setEnable(True)
        self._CatControlMode__isEnabled = True

    
    def disable(self):
        self._CatControlMode__shellingControl.setEnable(False)
        self._CatControlMode__cam.disable()
        self._CatControlMode__isEnabled = False

    
    def handleKeyEvent(self, isDown, key, mods, event = None):
        if not self._CatControlMode__isEnabled:
            raise AssertionError
        if BigWorld.isKeyDown(Keys.KEY_CAPSLOCK) and constants.IS_DEVELOPMENT and isDown and key == Keys.KEY_F2:
            self._CatControlMode__aih.onControlModeChanged('arcade')
        
        self._CatControlMode__shellingControl.handleKeyEvent(isDown, key, mods, event)
        return self._CatControlMode__cam.handleKey(event)

    
    def handleMouseEvent(self, dx, dy, dz):
        if not self._CatControlMode__isEnabled:
            raise AssertionError
        GUI.mcursor().position = (0, 0)
        return self._CatControlMode__cam.handleMouse(int(self._CatControlMode__sens[0] * dx), int(self._CatControlMode__sens[1] * dy), int(self._CatControlMode__sens[2] * dz))

    
    def onRecreateDevice(self):
        self._CatControlMode__shellingControl.recreate()

    
    def getEnabled(self):
        return bool(self._CatControlMode__isEnabled)

    
    def setCameraPosition(self, x, y, z):
        mat = Math.Matrix()
        mat.lookAt(Math.Vector3(x, y, z), (0, 0, 1), (0, 1, 0))
        self._CatControlMode__cam.camera.set(mat)

    
    def getCameraPosition(self):
        return tuple(self._CatControlMode__cam.camera.position)

    
    def setSensitivity(self, sens):
        self._CatControlMode__sens = tuple(sens)

    
    def getShellingControl(self):
        return self._CatControlMode__shellingControl

    
    def isManualBind(self):
        return True



class _TargetPointCalculator:
    _TargetPointCalculator__STATE_WAIT_FOR_MOUSE_MOVE = 0
    _TargetPointCalculator__STATE_MOUSE_TRACK = 1
    _TargetPointCalculator__STATE_SMART_TRACK = 2
    MIN_DIST = 50
    TERRAIN_MIN_ANGLE = math.pi / 6
    _TargetPointCalculator__TMP_MIN_DIST = MIN_DIST
    
    def enableSmartTrack(enable):
        if enable and _TargetPointCalculator.MIN_DIST == 0:
            _TargetPointCalculator.MIN_DIST = _TargetPointCalculator._TargetPointCalculator__TMP_MIN_DIST
        elif not enable and _TargetPointCalculator.MIN_DIST > 0:
            _TargetPointCalculator._TargetPointCalculator__TMP_MIN_DIST = _TargetPointCalculator.MIN_DIST
            _TargetPointCalculator.MIN_DIST = 0
        

    enableSmartTrack = staticmethod(enableSmartTrack)
    
    def setMinSmartTrackDistance(distance):
        _TargetPointCalculator.MIN_DIST = distance
        _TargetPointCalculator._TargetPointCalculator__TMP_MIN_DIST = distance

    setMinSmartTrackDistance = staticmethod(setMinSmartTrackDistance)
    
    def setTerrainMinAngleDegrees(degs):
        _TargetPointCalculator.TERRAIN_MIN_ANGLE = math.radians(degs)

    setTerrainMinAngleDegrees = staticmethod(setTerrainMinAngleDegrees)
    
    def __init__(self, arcadeCamera, aim):
        self._TargetPointCalculator__arcadeCamera = arcadeCamera
        self._TargetPointCalculator__aim = aim
        self._TargetPointCalculator__smartTrackYaw = 0
        self._TargetPointCalculator__smartTrackPitch = 0
        self._TargetPointCalculator__state = _TargetPointCalculator._TargetPointCalculator__STATE_WAIT_FOR_MOUSE_MOVE
        self.getTargetPoint = self._TargetPointCalculator__getTargetPointFromCamera
        self._TargetPointCalculator__tickCallbackId = None
        self._TargetPointCalculator__pitchDelta = 0
        self._TargetPointCalculator__yawDelta = 0
        self._TargetPointCalculator__turretJointMat = None

    
    def _TargetPointCalculator__isMouseTrack(self):
        return self._TargetPointCalculator__state in (_TargetPointCalculator._TargetPointCalculator__STATE_WAIT_FOR_MOUSE_MOVE, _TargetPointCalculator._TargetPointCalculator__STATE_MOUSE_TRACK)

    
    def destroy(self):
        if self._TargetPointCalculator__tickCallbackId is not None:
            BigWorld.cancelCallback(self._TargetPointCalculator__tickCallbackId)
        

    
    def enable(self, preferredPos, camYaw):
        if self._TargetPointCalculator__tickCallbackId is None:
            self._TargetPointCalculator__tickCallbackId = BigWorld.callback(0, self._TargetPointCalculator__tick)
        
        (turretStartPoint, gunStartPoint) = self._TargetPointCalculator__getTurretStartPoints(camYaw)
        if turretStartPoint is None:
            return None
        dirAtPrefPos = preferredPos - turretStartPoint
        dirLen = dirAtPrefPos.length
        if dirLen == 0:
            return None
        dirAtPrefPos /= dirLen
        self._TargetPointCalculator__smartTrackYaw = dirAtPrefPos.yaw
        self._TargetPointCalculator__smartTrackPitch = (preferredPos - gunStartPoint).pitch
        m = Math.Matrix()
        m.setRotateYPR((self._TargetPointCalculator__smartTrackYaw, self._TargetPointCalculator__smartTrackPitch, 0))
        m.translation = gunStartPoint
        prevState = self._TargetPointCalculator__state
        self._TargetPointCalculator__updateMode(preferredDirStartPos = (dirAtPrefPos, gunStartPoint))
        if self._TargetPointCalculator__state == _TargetPointCalculator._TargetPointCalculator__STATE_SMART_TRACK:
            if prevState != self._TargetPointCalculator__state:
                self._TargetPointCalculator__pitchDelta = 0
            
            cameraLookDir = preferredPos - Math.Matrix(self._TargetPointCalculator__arcadeCamera.camera.target).translation
            camYaw = cameraLookDir.yaw
            self._TargetPointCalculator__yawDelta = self._TargetPointCalculator__smartTrackYaw - camYaw
            (aimViewDir, _) = cameras.getWorldRayAndPoint(*self._TargetPointCalculator__aim.offset())
            (cameraViewDir, _) = cameras.getWorldRayAndPoint(0, 0)
            cameraAimToPitchDiff = cameraViewDir.pitch - aimViewDir.pitch
            resultCamPitch = -((self._TargetPointCalculator__smartTrackPitch - self._TargetPointCalculator__pitchDelta) + cameraAimToPitchDiff)
            self._TargetPointCalculator__arcadeCamera.setYawPitch(camYaw, resultCamPitch)
        
        self._TargetPointCalculator__updateDirections(preferredPos)

    
    def disable(self):
        if self._TargetPointCalculator__tickCallbackId is not None:
            BigWorld.cancelCallback(self._TargetPointCalculator__tickCallbackId)
            self._TargetPointCalculator__tickCallbackId = None
        

    
    def _TargetPointCalculator__tick(self):
        self._TargetPointCalculator__tickCallbackId = None
        self._TargetPointCalculator__tickCallbackId = BigWorld.callback(0, self._TargetPointCalculator__tick)
        
        try:
            self._TargetPointCalculator__turretJointMat = self._TargetPointCalculator__getTurretJointMat()
            if self._TargetPointCalculator__turretJointMat is not None:
                self._TargetPointCalculator__updateMode()
                self._TargetPointCalculator__updateDirections(self.getTargetPoint())
        except:
            LOG_CURRENT_EXCEPTION()


    
    def handleMouseEvent(self, dx, dy, dz):
        self._TargetPointCalculator__updateMode()
        if self._TargetPointCalculator__isMouseTrack():
            if dx != 0 or dy != 0:
                self._TargetPointCalculator__arcadeCamera.update(dx, dy, 0)
            
            if dz != 0:
                preferredPos = self._TargetPointCalculator__getTargetPointFromCamera()
                self._TargetPointCalculator__arcadeCamera.update(0, 0, cameras._clamp(-1, 1, dz))
                self._TargetPointCalculator__arcadeCamera.focusOnPos(preferredPos)
            
        else:
            self._TargetPointCalculator__trackableMouseUpdate(dx, dy, dz)
        self._TargetPointCalculator__updateDirections(self.getTargetPoint())

    
    def _TargetPointCalculator__updateDirections(self, targetPoint):
        if targetPoint is None:
            return None
        if self._TargetPointCalculator__isMouseTrack():
            (turretStartPoint, gunStartPoint) = self._TargetPointCalculator__getTurretStartPoints()
            if turretStartPoint is None:
                return None
            turretLookDir = targetPoint - turretStartPoint
            gunLookDir = targetPoint - gunStartPoint
            self._TargetPointCalculator__smartTrackYaw = turretLookDir.yaw
            self._TargetPointCalculator__smartTrackPitch = gunLookDir.pitch
        else:
            self._TargetPointCalculator__cameraUpdate(targetPoint)

    
    def _TargetPointCalculator__cameraUpdate(self, targetPoint):
        pass

    
    def _TargetPointCalculator__trackableMouseUpdate(self, dx, dy, dz):
        self._TargetPointCalculator__arcadeCamera.update(dx, dy, cameras._clamp(-1, 1, dz))
        (viewDir, _) = cameras.getWorldRayAndPoint(*self._TargetPointCalculator__aim.offset())
        self._TargetPointCalculator__smartTrackYaw = viewDir.yaw + self._TargetPointCalculator__yawDelta
        self._TargetPointCalculator__smartTrackPitch = viewDir.pitch + self._TargetPointCalculator__pitchDelta
        (minPitch, maxPitch) = self._TargetPointCalculator__getMinMaxPitch()
        self._TargetPointCalculator__smartTrackPitch = min(maxPitch, max(minPitch, self._TargetPointCalculator__smartTrackPitch))

    
    def _TargetPointCalculator__getMinMaxPitch(self):
        player = BigWorld.player()
        desc = player.vehicleTypeDescriptor
        if desc is None:
            return (0, 0)
        return gun_rotation_shared.calcPitchLimitsFromDesc(self._TargetPointCalculator__smartTrackYaw, desc.gun['pitchLimits'])

    
    def _TargetPointCalculator__calcYawPitch(self, targetPoint, startPoint):
        dir = targetPoint - startPoint
        return (dir.yaw, dir.pitch)

    
    def _TargetPointCalculator__testMouseTargetPoint(self, dir, start):
        (minPitch, maxPitch) = self._TargetPointCalculator__getMinMaxPitch()
        if minPitch <= self._TargetPointCalculator__smartTrackPitch:
            pass
        self._TargetPointCalculator__smartTrackPitch <= maxPitch
        pitchInBorders = 1
        dir.normalise()
        end = start + dir.scale(10000)
        testResTerrain = BigWorld.wg_collideSegment(BigWorld.player().spaceID, start, end, 128, (lambda matKind, collFlags, itemId, chunkId: collFlags & 8))
        if testResTerrain:
            pass
        terrainSuitsForCheck = testResTerrain[1].dot(Math.Vector3(0, 1, 0)) <= math.cos(_TargetPointCalculator.TERRAIN_MIN_ANGLE)
        testResNonTerrain = BigWorld.wg_collideSegment(BigWorld.player().spaceID, start, end, 136)
        testResDynamic = collideDynamic(start, end, (BigWorld.player().playerVehicleID,), False)
        closestPoint = None
        closestDist = 1000000
        enableSmartTrack = False
        if testResTerrain:
            closestPoint = testResTerrain[0]
            closestDist = (testResTerrain[0] - start).length
        
        if terrainSuitsForCheck:
            if closestDist <= _TargetPointCalculator.MIN_DIST:
                pass
            enableSmartTrack = pitchInBorders
        
        if testResNonTerrain is not None:
            dist = (testResNonTerrain[0] - start).length
            if dist < closestDist:
                closestPoint = testResNonTerrain[0]
                closestDist = dist
                if closestDist <= _TargetPointCalculator.MIN_DIST:
                    pass
                enableSmartTrack = pitchInBorders
            
        
        if closestPoint is None and testResDynamic is None:
            return (_shootInSkyPoint(start, dir), False)
        if testResDynamic is not None:
            dynDist = testResDynamic[1]
            if dynDist <= closestDist:
                dir = end - start
                dir.normalise()
                return (start + dir * dynDist, False)
        
        if not enableSmartTrack:
            camPos = self._TargetPointCalculator__arcadeCamera.camera.position
            viewDir = closestPoint - camPos
            enableSmartTrack = self._TargetPointCalculator__isLookOnBridge(viewDir, closestPoint)
        
        return (closestPoint, enableSmartTrack)

    
    def _TargetPointCalculator__isLookOnBridge(self, viewDir, targetPoint):
        dirFromTurretPos = targetPoint - self._TargetPointCalculator__getTurretJointMat().translation
        (turretPos, gunStartToLookOnTarget) = self._TargetPointCalculator__getTurretStartPoints(dirFromTurretPos.yaw)
        dirFromSniperPos = targetPoint - gunStartToLookOnTarget
        viewDir = Math.Vector3(viewDir)
        viewDir.y = 0
        viewDir.normalise()
        dirFromSniperPos.y = 0
        dirFromSniperPos.normalise()
        dirFromTurretPos.y = 0
        dirFromTurretPos.normalise()
        if not viewDir.dot(dirFromSniperPos) < 0:
            pass
        return viewDir.dot(dirFromTurretPos) < 0

    
    def _TargetPointCalculator__updateMode(self, preferredDirStartPos = None):
        if self._TargetPointCalculator__state == _TargetPointCalculator._TargetPointCalculator__STATE_WAIT_FOR_MOUSE_MOVE:
            self._TargetPointCalculator__updateDirections(self.getTargetPoint())
            self._TargetPointCalculator__state = _TargetPointCalculator._TargetPointCalculator__STATE_MOUSE_TRACK
        
        if preferredDirStartPos is None:
            (dir, start) = cameras.getWorldRayAndPoint(*self._TargetPointCalculator__aim.offset())
        else:
            dir = preferredDirStartPos[0]
            start = preferredDirStartPos[1]
        (mouseTargetPoint, enableSmartTrack) = self._TargetPointCalculator__testMouseTargetPoint(dir, start)
        if mouseTargetPoint is None:
            return None
        camPos = self._TargetPointCalculator__arcadeCamera.camera.position
        viewDir = mouseTargetPoint - camPos
        if not enableSmartTrack and not (self._TargetPointCalculator__state == _TargetPointCalculator._TargetPointCalculator__STATE_MOUSE_TRACK):
            self._TargetPointCalculator__state = _TargetPointCalculator._TargetPointCalculator__STATE_MOUSE_TRACK
            self.getTargetPoint = self._TargetPointCalculator__getTargetPointFromCamera
        elif enableSmartTrack and self._TargetPointCalculator__state == _TargetPointCalculator._TargetPointCalculator__STATE_MOUSE_TRACK:
            self._TargetPointCalculator__enterSmartTrackMode(viewDir)
        

    
    def _TargetPointCalculator__getMaxYawDelta(self):
        turretMat = self._TargetPointCalculator__getTurretJointMat()
        if turretMat is None or _TargetPointCalculator.MIN_DIST <= 0:
            return 0
        camTargetPos = Math.Matrix(self._TargetPointCalculator__arcadeCamera.camera.target).translation
        shiftVec = camTargetPos - turretMat.translation
        shiftVec.y = 0
        shift = shiftVec.length
        return math.atan(shift / _TargetPointCalculator.MIN_DIST)

    
    def _TargetPointCalculator__enterSmartTrackMode(self, viewDir):
        self._TargetPointCalculator__state = _TargetPointCalculator._TargetPointCalculator__STATE_SMART_TRACK
        self.getTargetPoint = self._TargetPointCalculator__getTargetPointFromTurret
        self._TargetPointCalculator__pitchDelta = self._TargetPointCalculator__smartTrackPitch - viewDir.pitch
        self._TargetPointCalculator__yawDelta = self._TargetPointCalculator__smartTrackYaw - viewDir.yaw
        maxYawDelta = self._TargetPointCalculator__getMaxYawDelta()
        self._TargetPointCalculator__yawDelta = _clamp(-maxYawDelta, maxYawDelta, self._TargetPointCalculator__yawDelta)

    
    def _TargetPointCalculator__isOnLeftSideOfSymmetry(self, vec2d):
        symmetryAxis = self._TargetPointCalculator__getTurretJointMat().translation - self._TargetPointCalculator__arcadeCamera.camera.position
        symmetryAxis = Math.Vector2(symmetryAxis.x, symmetryAxis.z)
        return symmetryAxis.cross2D(vec2d) <= 0

    
    def _TargetPointCalculator__getTurretJointMat(self):
        player = BigWorld.player()
        vehicle = BigWorld.entity(player.playerVehicleID)
        if vehicle is not None and vehicle.isStarted:
            turretOffs = vehicle.typeDescriptor.chassis['hullPosition'] + vehicle.typeDescriptor.hull['turretPositions'][0]
            turretOffsetMat = Math.Matrix()
            turretOffsetMat.setTranslate(turretOffs)
            turretJointMat = Math.Matrix(player.getOwnVehicleMatrix())
            turretJointMat.preMultiply(turretOffsetMat)
            return turretJointMat
        return None

    
    def _TargetPointCalculator__getTurretStartPoints(self, predefinedYaw = None):
        player = BigWorld.player()
        vehicle = BigWorld.entity(player.playerVehicleID)
        if vehicle is not None and vehicle.isStarted:
            gunOffs = vehicle.typeDescriptor.turret['gunPosition']
            posMat = Math.Matrix()
            posMat.setTranslate(gunOffs)
            turretJointMat = self._TargetPointCalculator__getTurretJointMat()
            rotateMat = Math.Matrix()
            if predefinedYaw is None:
                pass
            1
            calculatorYaw = predefinedYaw
            rotateMat.setRotateYPR((calculatorYaw - turretJointMat.yaw, 0, 0))
            posMat.postMultiply(rotateMat)
            posMat.postMultiply(turretJointMat)
            return (turretJointMat.translation, posMat.translation)
        return (None, None)

    
    def _TargetPointCalculator__getTargetPointFromTurret(self):
        (turretTranslation, gunTranslation) = self._TargetPointCalculator__getTurretStartPoints()
        if turretTranslation is None:
            return None
        dirMat = Math.Matrix()
        dirMat.setRotateYPR((self._TargetPointCalculator__smartTrackYaw, self._TargetPointCalculator__smartTrackPitch, 0))
        dir = dirMat.applyToAxis(2)
        return _getShotPointOnDir(gunTranslation, dir)

    
    def _TargetPointCalculator__getTargetPointFromCamera(self):
        return _getDesiredShotPoint(self._TargetPointCalculator__aim.offset())



class ArcadeControlMode(IControlMode):
    postmortemCamParams = property((lambda self: (self._ArcadeControlMode__cam.angles, self._ArcadeControlMode__cam.camera.pivotMaxDist)))
    camera = property((lambda self: self._ArcadeControlMode__cam))
    
    def __init__(self, dataSection, avatarInputHandler):
        self._ArcadeControlMode__aih = weakref.proxy(avatarInputHandler)
        self._ArcadeControlMode__gunMarker = _SuperGunMarker(mode = 'arcade')
        self._ArcadeControlMode__aim = aims.createAim(dataSection.readString('aim'))
        self._ArcadeControlMode__cam = cameras.ArcadeCamera(dataSection['camera'])
        self._ArcadeControlMode__mouseVehicleRotator = _MouseVehicleRotator()
        self._ArcadeControlMode__aimingMode = 0
        self._ArcadeControlMode__canShot = False
        self._ArcadeControlMode__isEnabled = False
        self._ArcadeControlMode__isArenaStarted = False
        self._ArcadeControlMode__sightOffset = list(self._ArcadeControlMode__aim.offset())
        self._ArcadeControlMode__targetPointCalculator = _TargetPointCalculator(self._ArcadeControlMode__cam, self._ArcadeControlMode__aim)

    
    def prerequisites(self):
        out = []
        out += self._ArcadeControlMode__gunMarker.prerequisites()
        out += self._ArcadeControlMode__aim.prerequisites()
        return out

    
    def create(self):
        self._ArcadeControlMode__aim.create()
        self._ArcadeControlMode__gunMarker.create()
        self._ArcadeControlMode__cam.create(_ARCADE_CAM_PIVOT_POS, self.onChangeControlModeByScroll)
        self._ArcadeControlMode__cam.cursorOffset(self._ArcadeControlMode__sightOffset)
        self.disable()

    
    def destroy(self):
        self.disable()
        self._ArcadeControlMode__aim.destroy()
        self._ArcadeControlMode__gunMarker.destroy()
        self._ArcadeControlMode__cam.destroy()
        self._ArcadeControlMode__mouseVehicleRotator.destroy()
        self._ArcadeControlMode__targetPointCalculator.destroy()
        self._ArcadeControlMode__aih = None
        self._ArcadeControlMode__mouseVehicleRotator = None
        self._ArcadeControlMode__targetPointCalculator = None

    
    def dumpState(self):
        return {
            'gunMarker': self._ArcadeControlMode__gunMarker.dumpState() }

    
    def enable(self, **args):
        ctrlState = args.get('ctrlState')
        self._ArcadeControlMode__aimingMode = args.get('aimingMode', self._ArcadeControlMode__aimingMode)
        self._ArcadeControlMode__cam.enable(args.get('preferredPos'), args.get('closesDist', False))
        self._ArcadeControlMode__targetPointCalculator.enable(args.get('preferredPos', Math.Vector3(0, 0, 0)), self._ArcadeControlMode__cam.angles[0])
        self._ArcadeControlMode__gunMarker.enable(ctrlState.get('gunMarker'))
        self._ArcadeControlMode__aim.enable()
        self._ArcadeControlMode__isEnabled = True
        arena = BigWorld.player().arena
        if arena is not None:
            arena.onPeriodChange += self._ArcadeControlMode__onArenaStarted
            self._ArcadeControlMode__onArenaStarted(arena.period)
        
        g_postProcessing.enable('arcade')

    
    def disable(self):
        self._ArcadeControlMode__isEnabled = False
        self._ArcadeControlMode__cam.disable()
        self._ArcadeControlMode__gunMarker.disable()
        self._ArcadeControlMode__aim.disable()
        arena = BigWorld.player().arena
        if arena is not None:
            arena.onPeriodChange -= self._ArcadeControlMode__onArenaStarted
        
        g_postProcessing.disable()
        self._ArcadeControlMode__targetPointCalculator.disable()

    
    def handleKeyEvent(self, isDown, key, mods, event = None):
        if not self._ArcadeControlMode__isEnabled:
            raise AssertionError
        cmdMap = CommandMapping.g_instance
        if BigWorld.isKeyDown(Keys.KEY_CAPSLOCK) and constants.IS_DEVELOPMENT and isDown and key == Keys.KEY_F1:
            self._ArcadeControlMode__aih.onControlModeChanged('debug', prevModeName = 'arcade', camMatrix = self._ArcadeControlMode__cam.camera.matrix)
            return True
        if BigWorld.isKeyDown(Keys.KEY_CAPSLOCK) and constants.IS_DEVELOPMENT and isDown and key == Keys.KEY_F2:
            self._ArcadeControlMode__aih.onControlModeChanged('cat', camMatrix = self._ArcadeControlMode__cam.camera.matrix)
            return True
        isFiredFreeCamera = cmdMap.isFired(CommandMapping.CMD_CM_FREE_CAMERA, key)
        if cmdMap.isFired(CommandMapping.CMD_CM_LOCK_TARGET, key):
            pass
        isFiredLockTarget = isDown
        if isFiredFreeCamera or isFiredLockTarget:
            if isFiredFreeCamera:
                self.setAimingMode(isDown, AIMING_MODE.USER_DISABLED)
            
            if isFiredLockTarget:
                BigWorld.player().autoAim(BigWorld.target())
            
        
        if cmdMap.isFired(CommandMapping.CMD_CM_SHOOT, key) and isDown:
            BigWorld.player().shoot()
            return True
        if cmdMap.isFired(CommandMapping.CMD_CM_LOCK_TARGET_OFF, key) and isDown:
            BigWorld.player().autoAim(None)
            return True
        if cmdMap.isFired(CommandMapping.CMD_CM_VEHICLE_SWITCH_AUTOROTATION, key) and isDown:
            self._ArcadeControlMode__aih.switchAutorotation()
            return True
        if cmdMap.isFiredList((CommandMapping.CMD_CM_CAMERA_ROTATE_LEFT, CommandMapping.CMD_CM_CAMERA_ROTATE_RIGHT, CommandMapping.CMD_CM_CAMERA_ROTATE_UP, CommandMapping.CMD_CM_CAMERA_ROTATE_DOWN, CommandMapping.CMD_CM_INCREASE_ZOOM, CommandMapping.CMD_CM_DECREASE_ZOOM), key):
            dx = 0
            dy = 0
            dz = 0
            if cmdMap.isActive(CommandMapping.CMD_CM_CAMERA_ROTATE_LEFT):
                dx = -1
            
            if cmdMap.isActive(CommandMapping.CMD_CM_CAMERA_ROTATE_RIGHT):
                dx = 1
            
            if cmdMap.isActive(CommandMapping.CMD_CM_CAMERA_ROTATE_UP):
                dy = -1
            
            if cmdMap.isActive(CommandMapping.CMD_CM_CAMERA_ROTATE_DOWN):
                dy = 1
            
            if cmdMap.isActive(CommandMapping.CMD_CM_INCREASE_ZOOM):
                dz = 1
            
            if cmdMap.isActive(CommandMapping.CMD_CM_DECREASE_ZOOM):
                dz = -1
            
            if dx == dy and dy == dz:
                pass
            dz == 0
            if 1:
                pass
            1
            dx(dy, dz, True, True, True, False)
            return True
        if cmdMap.isFired(CommandMapping.CMD_CM_ALTERNATE_MODE, key) and isDown:
            self._ArcadeControlMode__activateAlternateMode()
            return True
        if cmdMap.isFired(CommandMapping.CMD_CM_CAMERA_RESTORE_DEFAULT, key) and isDown:
            self._ArcadeControlMode__cam.restoreDefaultsState()
            return True
        return False

    
    def handleMouseEvent(self, dx, dy, dz):
        if not self._ArcadeControlMode__isEnabled:
            raise AssertionError
        GUI.mcursor().position = self._ArcadeControlMode__aim.offset()
        self._ArcadeControlMode__targetPointCalculator.handleMouseEvent(dx, dy, dz)
        self._ArcadeControlMode__mouseVehicleRotator.handleMouse(dx)
        return True

    
    def setReloading(self, duration, startTime):
        self._ArcadeControlMode__gunMarker.setReloading(duration, startTime)

    
    def onMinimapClicked(self, worldPos):
        if self._ArcadeControlMode__aih.isSPG:
            self._ArcadeControlMode__activateAlternateMode(worldPos)
        

    
    def showGunMarker(self, flag):
        if not self._ArcadeControlMode__isEnabled:
            raise AssertionError
        self._ArcadeControlMode__gunMarker.show(flag)

    
    def showGunMarker2(self, flag):
        if not self._ArcadeControlMode__isEnabled:
            raise AssertionError
        self._ArcadeControlMode__gunMarker.show2(flag)

    
    def updateGunMarker(self, pos, dir, size, relaxTime, collData):
        if not self._ArcadeControlMode__isEnabled:
            raise AssertionError
        self._ArcadeControlMode__gunMarker.update(pos, dir, size, relaxTime, collData)

    
    def updateGunMarker2(self, pos, dir, size, relaxTime, collData):
        if not self._ArcadeControlMode__isEnabled:
            raise AssertionError
        self._ArcadeControlMode__gunMarker.update2(pos, dir, size, relaxTime, collData)

    
    def setAimingMode(self, enable, mode):
        if enable:
            self._ArcadeControlMode__aimingMode |= mode
        else:
            self._ArcadeControlMode__aimingMode &= -1 - mode

    
    def getDesiredShotPoint(self):
        if not self._ArcadeControlMode__isEnabled:
            raise AssertionError
        if self._ArcadeControlMode__aimingMode == 0:
            return self._ArcadeControlMode__targetPointCalculator.getTargetPoint()

    
    def updateShootingStatus(self, canShot):
        if not self._ArcadeControlMode__isEnabled:
            raise AssertionError
        self._ArcadeControlMode__canShot = canShot

    
    def onChangeControlModeByScroll(self):
        self._ArcadeControlMode__activateAlternateMode(pos = None, bByScroll = True)

    
    def onRecreateDevice(self):
        self._ArcadeControlMode__gunMarker.onRecreateDevice()
        self._ArcadeControlMode__aim.onRecreateDevice()

    
    def getAim(self):
        return self._ArcadeControlMode__aim

    
    def _ArcadeControlMode__onArenaStarted(self, period, *args):
        if period == constants.ARENA_PERIOD.BATTLE:
            pass
        1
        self._ArcadeControlMode__isArenaStarted = False

    
    def setGUIVisible(self, isVisible):
        self._ArcadeControlMode__aim.setVisible(isVisible)
        self._ArcadeControlMode__gunMarker.setGUIVisible(isVisible, valueUpdate = not (self._ArcadeControlMode__isArenaStarted))

    
    def _ArcadeControlMode__activateAlternateMode(self, pos = None, bByScroll = False):
        ownVehicle = BigWorld.entity(BigWorld.player().playerVehicleID)
        if ownVehicle is not None and ownVehicle.isStarted and ownVehicle.appearance.isUnderwater():
            return None
        if self._ArcadeControlMode__aih.isSPG and not bByScroll:
            self._ArcadeControlMode__cam.autoUpdate(0, 0, 0, False, False, True)
            if pos is None:
                pos = _getDesiredShotPoint(self._ArcadeControlMode__aim.offset(), False)
                if pos is None:
                    pos = Math.Matrix(self._ArcadeControlMode__gunMarker.matrixProvider()).applyToOrigin()
                
            
            self._ArcadeControlMode__aih.onControlModeChanged('strategic', preferredPos = pos, aimingMode = self._ArcadeControlMode__aimingMode, saveDist = True)
            return None
        if not self._ArcadeControlMode__aih.isSPG:
            self._ArcadeControlMode__cam.autoUpdate(0, 0, 0, False, False, True)
            self._ArcadeControlMode__aih.onControlModeChanged('sniper', preferredPos = self._ArcadeControlMode__targetPointCalculator.getTargetPoint(), aimingMode = self._ArcadeControlMode__aimingMode, saveZoom = True)
            return None



class StrategicControlMode(IControlMode):
    camera = property((lambda self: self._StrategicControlMode__cam))
    
    def __init__(self, dataSection, avatarInputHandler):
        self._StrategicControlMode__aih = weakref.proxy(avatarInputHandler)
        self._StrategicControlMode__trajectoryDrawer = BigWorld.wg_trajectory_drawer()
        self._StrategicControlMode__gunMarker = _SuperGunMarker(mode = 'strategic', isStrategic = True)
        self._StrategicControlMode__aim = aims.createAim(dataSection.readString('aim'))
        self._StrategicControlMode__cam = cameras.StrategicCamera(dataSection['camera'])
        self._StrategicControlMode__canShoot = False
        self._StrategicControlMode__isEnabled = False
        self._StrategicControlMode__aimingMode = 0
        self._StrategicControlMode__trajectoryDrawerClbk = None
        self._StrategicControlMode__updateInterval = 0.1

    
    def prerequisites(self):
        out = []
        out += self._StrategicControlMode__gunMarker.prerequisites()
        out += self._StrategicControlMode__aim.prerequisites()
        return out

    
    def create(self):
        self._StrategicControlMode__aim.create()
        self._StrategicControlMode__gunMarker.create()
        self._StrategicControlMode__cam.create(None)
        self._StrategicControlMode__initTrajectoryDrawer()
        self.disable()

    
    def destroy(self):
        self.disable()
        self._StrategicControlMode__aim.destroy()
        self._StrategicControlMode__gunMarker.destroy()
        self._StrategicControlMode__cam.destroy()
        self._StrategicControlMode__delTrajectoryDrawer()
        self._StrategicControlMode__aih = None

    
    def dumpState(self):
        return {
            'gunMarker': self._StrategicControlMode__gunMarker.dumpState() }

    
    def enable(self, **args):
        ctrlState = args.get('ctrlState')
        self._StrategicControlMode__aimingMode = args.get('aimingMode', self._StrategicControlMode__aimingMode)
        self._StrategicControlMode__cam.enable(args['preferredPos'], args['saveDist'])
        self._StrategicControlMode__aim.enable()
        self._StrategicControlMode__gunMarker.enable(ctrlState.get('gunMarker', None))
        self._StrategicControlMode__trajectoryDrawer.visible = True
        self._StrategicControlMode__isEnabled = True
        BigWorld.player().autoAim(None)
        self._StrategicControlMode__updateTrajectoryDrawer()
        vehicle = BigWorld.entities.get(BigWorld.player().playerVehicleID)
        if vehicle is not None:
            if isinstance(vehicle.filter, BigWorld.WGVehicleFilter) or isinstance(vehicle.filter, BigWorld.WGVehicleFilter2):
                vehicle.filter.allowLagReporting = False
            
        g_postProcessing.enable('strategic')

    
    def disable(self):
        self._StrategicControlMode__isEnabled = False
        self._StrategicControlMode__cam.disable()
        self._StrategicControlMode__gunMarker.disable()
        self._StrategicControlMode__aim.disable()
        self._StrategicControlMode__trajectoryDrawer.visible = False
        vehicle = BigWorld.entities.get(BigWorld.player().playerVehicleID)
        if vehicle is not None:
            if isinstance(vehicle.filter, BigWorld.WGVehicleFilter) or isinstance(vehicle.filter, BigWorld.WGVehicleFilter2):
                vehicle.filter.allowLagReporting = True
            
        if self._StrategicControlMode__trajectoryDrawerClbk is not None:
            BigWorld.cancelCallback(self._StrategicControlMode__trajectoryDrawerClbk)
            self._StrategicControlMode__trajectoryDrawerClbk = None
        
        g_postProcessing.disable()

    
    def handleKeyEvent(self, isDown, key, mods, event = None):
        if not self._StrategicControlMode__isEnabled:
            raise AssertionError
        cmdMap = CommandMapping.g_instance
        if cmdMap.isFired(CommandMapping.CMD_CM_SHOOT, key) and isDown:
            BigWorld.player().shoot()
            return True
        if cmdMap.isFired(CommandMapping.CMD_CM_VEHICLE_SWITCH_AUTOROTATION, key) and isDown:
            self._StrategicControlMode__aih.switchAutorotation()
            return True
        if cmdMap.isFired(CommandMapping.CMD_CM_ALTERNATE_MODE, key) and isDown:
            pos = _getDesiredShotPoint(self._StrategicControlMode__aim.offset(), False, True)
            if pos is None:
                pos = Math.Matrix(self._StrategicControlMode__gunMarker.matrixProvider()).applyToOrigin()
            
            dir = pos - BigWorld.player().getOwnVehiclePosition()
            self._StrategicControlMode__aih.onControlModeChanged('arcade', preferredPos = pos, yaw = dir.yaw, aimingMode = self._StrategicControlMode__aimingMode, closesDist = False)
            return True
        if cmdMap.isFired(CommandMapping.CMD_CM_FREE_CAMERA, key):
            self.setAimingMode(isDown, AIMING_MODE.USER_DISABLED)
            return True
        if cmdMap.isFiredList((CommandMapping.CMD_CM_CAMERA_ROTATE_LEFT, CommandMapping.CMD_CM_CAMERA_ROTATE_RIGHT, CommandMapping.CMD_CM_CAMERA_ROTATE_UP, CommandMapping.CMD_CM_CAMERA_ROTATE_DOWN, CommandMapping.CMD_CM_INCREASE_ZOOM, CommandMapping.CMD_CM_DECREASE_ZOOM), key):
            dx = 0
            dy = 0
            dz = 0
            if cmdMap.isActive(CommandMapping.CMD_CM_CAMERA_ROTATE_LEFT):
                dx = -1
            
            if cmdMap.isActive(CommandMapping.CMD_CM_CAMERA_ROTATE_RIGHT):
                dx = 1
            
            if cmdMap.isActive(CommandMapping.CMD_CM_CAMERA_ROTATE_UP):
                dy = -1
            
            if cmdMap.isActive(CommandMapping.CMD_CM_CAMERA_ROTATE_DOWN):
                dy = 1
            
            if cmdMap.isActive(CommandMapping.CMD_CM_INCREASE_ZOOM):
                dz = 1
            
            if cmdMap.isActive(CommandMapping.CMD_CM_DECREASE_ZOOM):
                dz = -1
            
            if dx == dy and dy == dz:
                pass
            dz == 0
            if 1:
                pass
            1
            dx(dy, dz, True, False)
            return True
        if cmdMap.isFired(CommandMapping.CMD_CM_CAMERA_RESTORE_DEFAULT, key) and isDown:
            self._StrategicControlMode__cam.autoUpdate(0, 0, 0, True)
            self._StrategicControlMode__cam.restoreDefaultsState()
            return True
        return False

    
    def handleMouseEvent(self, dx, dy, dz):
        if not self._StrategicControlMode__isEnabled:
            raise AssertionError
        GUI.mcursor().position = self._StrategicControlMode__aim.offset()
        self._StrategicControlMode__cam.update(dx, dy, dz)
        return True

    
    def setReloading(self, duration, startTime):
        self._StrategicControlMode__gunMarker.setReloading(duration, startTime)

    
    def onMinimapClicked(self, worldPos):
        self._StrategicControlMode__cam.teleport(worldPos)

    
    def showGunMarker(self, flag):
        if not self._StrategicControlMode__isEnabled:
            raise AssertionError
        self._StrategicControlMode__gunMarker.show(flag)

    
    def showGunMarker2(self, flag):
        if not self._StrategicControlMode__isEnabled:
            raise AssertionError
        self._StrategicControlMode__gunMarker.show2(flag)

    
    def updateGunMarker(self, pos, dir, size, relaxTime, collData):
        if not self._StrategicControlMode__isEnabled:
            raise AssertionError
        self._StrategicControlMode__gunMarker.update(pos, dir, size, relaxTime, collData)

    
    def updateGunMarker2(self, pos, dir, size, relaxTime, collData):
        if not self._StrategicControlMode__isEnabled:
            raise AssertionError
        self._StrategicControlMode__gunMarker.update2(pos, dir, size, relaxTime, collData)

    
    def setAimingMode(self, enable, mode):
        if enable:
            self._StrategicControlMode__aimingMode |= mode
        else:
            self._StrategicControlMode__aimingMode &= -1 - mode

    
    def getDesiredShotPoint(self):
        if not self._StrategicControlMode__isEnabled:
            raise AssertionError
        if self._StrategicControlMode__aimingMode == 0:
            return _getDesiredShotPoint(self._StrategicControlMode__aim.offset(), True, True)

    
    def updateShootingStatus(self, canShoot):
        if not self._StrategicControlMode__isEnabled:
            raise AssertionError
        self._StrategicControlMode__canShoot = canShoot

    
    def onRecreateDevice(self):
        self._StrategicControlMode__gunMarker.onRecreateDevice()
        self._StrategicControlMode__aim.onRecreateDevice()

    
    def getAim(self):
        return self._StrategicControlMode__aim

    
    def setGUIVisible(self, isVisible):
        self._StrategicControlMode__aim.setVisible(isVisible)
        self._StrategicControlMode__gunMarker.setGUIVisible(isVisible)

    
    def isManualBind(self):
        return True

    
    def _StrategicControlMode__updateTrajectoryDrawer(self):
        self._StrategicControlMode__trajectoryDrawerClbk = BigWorld.callback(self._StrategicControlMode__updateInterval, self._StrategicControlMode__updateTrajectoryDrawer)
        
        try:
            R = _getDesiredShotPoint(self._StrategicControlMode__aim.offset(), True, True)
            if R is None:
                return None
            (r0, v0, g0) = BigWorld.player().gunRotator.getShotParams(R)
            self._StrategicControlMode__trajectoryDrawer.update(R, r0, v0, self._StrategicControlMode__updateInterval)
        except:
            LOG_CURRENT_EXCEPTION()


    
    def _StrategicControlMode__onGunShotChanged(self):
        shotDescr = BigWorld.player().vehicleTypeDescriptor.shot
        self._StrategicControlMode__trajectoryDrawer.setParams(shotDescr['maxDistance'], Math.Vector3(0, -shotDescr['gravity'], 0), self._StrategicControlMode__aim.offset())

    
    def _StrategicControlMode__initTrajectoryDrawer(self):
        BigWorld.player().onGunShotChanged += self._StrategicControlMode__onGunShotChanged
        self._StrategicControlMode__trajectoryDrawer.setColors(Math.Vector4(0, 255, 0, 255), Math.Vector4(255, 0, 0, 255), Math.Vector4(128, 128, 128, 255))
        self._StrategicControlMode__onGunShotChanged()

    
    def _StrategicControlMode__delTrajectoryDrawer(self):
        BigWorld.player().onGunShotChanged -= self._StrategicControlMode__onGunShotChanged
        self._StrategicControlMode__trajectoryDrawer = None



class SniperControlMode(IControlMode):
    camera = property((lambda self: self._SniperControlMode__cam))
    
    def __init__(self, dataSection, avatarInputHandler):
        self._SniperControlMode__aih = weakref.proxy(avatarInputHandler)
        self._SniperControlMode__gunMarker = _SuperGunMarker('sniper')
        self._SniperControlMode__aim = aims.createAim(dataSection.readString('aim'))
        self._SniperControlMode__cam = cameras.SniperCamera(dataSection['camera'])
        self._SniperControlMode__binoculars = _Binoculars()
        self._SniperControlMode__isEnabled = False
        self._SniperControlMode__aimingMode = 0
        self._SniperControlMode__canShoot = False

    
    def prerequisites(self):
        out = []
        out += self._SniperControlMode__gunMarker.prerequisites()
        out += self._SniperControlMode__aim.prerequisites()
        return out

    
    def create(self):
        self._SniperControlMode__aim.create()
        self._SniperControlMode__gunMarker.create()
        self._SniperControlMode__cam.create(self.onChangeControlModeByScroll)
        self.disable()

    
    def destroy(self):
        self.disable(True)
        self._SniperControlMode__aim.destroy()
        self._SniperControlMode__gunMarker.destroy()
        self._SniperControlMode__cam.destroy()
        self._SniperControlMode__binoculars.disable()
        self._SniperControlMode__aih = None

    
    def dumpState(self):
        return {
            'gunMarker': self._SniperControlMode__gunMarker.dumpState() }

    
    def enable(self, **args):
        ctrlState = args.get('ctrlState')
        self._SniperControlMode__aimingMode = args.get('aimingMode', self._SniperControlMode__aimingMode)
        self._SniperControlMode__cam.enable(args['preferredPos'], args['saveZoom'])
        self._SniperControlMode__aim.enable()
        self._SniperControlMode__gunMarker.enable(ctrlState.get('gunMarker', None))
        self._SniperControlMode__binoculars.enable()
        self._SniperControlMode__isEnabled = True
        BigWorld.wg_enableTreeHiding(True)
        BigWorld.wg_setTreeHidingRadius(15, 10)
        g_postProcessing.enable('sniper')

    
    def disable(self, isDestroy = False):
        self._SniperControlMode__isEnabled = False
        self._SniperControlMode__aim.disable()
        self._SniperControlMode__gunMarker.disable()
        self._SniperControlMode__binoculars.disable()
        self._SniperControlMode__cam.disable()
        BigWorld.wg_enableTreeHiding(False)
        g_postProcessing.disable()

    
    def handleKeyEvent(self, isDown, key, mods, event = None):
        if not self._SniperControlMode__isEnabled:
            raise AssertionError
        cmdMap = CommandMapping.g_instance
        isFiredFreeCamera = cmdMap.isFired(CommandMapping.CMD_CM_FREE_CAMERA, key)
        if cmdMap.isFired(CommandMapping.CMD_CM_LOCK_TARGET, key):
            pass
        isFiredLockTarget = isDown
        if isFiredFreeCamera or isFiredLockTarget:
            if isFiredFreeCamera:
                self.setAimingMode(isDown, AIMING_MODE.USER_DISABLED)
            
            if isFiredLockTarget:
                BigWorld.player().autoAim(BigWorld.target())
            
        
        if cmdMap.isFired(CommandMapping.CMD_CM_SHOOT, key) and isDown:
            BigWorld.player().shoot()
            return True
        if cmdMap.isFired(CommandMapping.CMD_CM_LOCK_TARGET_OFF, key) and isDown:
            BigWorld.player().autoAim(None)
            return True
        if cmdMap.isFired(CommandMapping.CMD_CM_ALTERNATE_MODE, key) and isDown:
            self._SniperControlMode__aih.onControlModeChanged('arcade', preferredPos = _getDesiredShotPoint(self._SniperControlMode__aim.offset(), False), yaw = self._SniperControlMode__cam.camera.direction.yaw, aimingMode = self._SniperControlMode__aimingMode, closesDist = False)
            return True
        if cmdMap.isFiredList((CommandMapping.CMD_CM_CAMERA_ROTATE_LEFT, CommandMapping.CMD_CM_CAMERA_ROTATE_RIGHT, CommandMapping.CMD_CM_CAMERA_ROTATE_UP, CommandMapping.CMD_CM_CAMERA_ROTATE_DOWN, CommandMapping.CMD_CM_INCREASE_ZOOM, CommandMapping.CMD_CM_DECREASE_ZOOM), key):
            dx = 0
            dy = 0
            dz = 0
            if cmdMap.isActive(CommandMapping.CMD_CM_CAMERA_ROTATE_LEFT):
                dx = -1
            
            if cmdMap.isActive(CommandMapping.CMD_CM_CAMERA_ROTATE_RIGHT):
                dx = 1
            
            if cmdMap.isActive(CommandMapping.CMD_CM_CAMERA_ROTATE_UP):
                dy = -1
            
            if cmdMap.isActive(CommandMapping.CMD_CM_CAMERA_ROTATE_DOWN):
                dy = 1
            
            if cmdMap.isActive(CommandMapping.CMD_CM_INCREASE_ZOOM):
                dz = 1
            
            if cmdMap.isActive(CommandMapping.CMD_CM_DECREASE_ZOOM):
                dz = -1
            
            if dx == dy:
                pass
            dy == 0
            if 1:
                pass
            1
            dx(dy, dz, False, True)
            return True
        return False

    
    def handleMouseEvent(self, dx, dy, dz):
        if not self._SniperControlMode__isEnabled:
            raise AssertionError
        GUI.mcursor().position = self._SniperControlMode__aim.offset()
        self._SniperControlMode__cam.update(dx, dy, dz)
        return True

    
    def setReloading(self, duration, startTime):
        self._SniperControlMode__gunMarker.setReloading(duration, startTime)

    
    def showGunMarker(self, flag):
        if not self._SniperControlMode__isEnabled:
            raise AssertionError
        self._SniperControlMode__gunMarker.show(flag)

    
    def showGunMarker2(self, flag):
        if not self._SniperControlMode__isEnabled:
            raise AssertionError
        self._SniperControlMode__gunMarker.show2(flag)

    
    def updateGunMarker(self, pos, dir, size, relaxTime, collData):
        if not self._SniperControlMode__isEnabled:
            raise AssertionError
        self._SniperControlMode__gunMarker.update(pos, dir, size, relaxTime, collData)

    
    def updateGunMarker2(self, pos, dir, size, relaxTime, collData):
        if not self._SniperControlMode__isEnabled:
            raise AssertionError
        self._SniperControlMode__gunMarker.update2(pos, dir, size, relaxTime, collData)

    
    def setAimingMode(self, enable, mode):
        if enable:
            self._SniperControlMode__aimingMode |= mode
        else:
            self._SniperControlMode__aimingMode &= -1 - mode

    
    def getDesiredShotPoint(self):
        if not self._SniperControlMode__isEnabled:
            raise AssertionError
        if self._SniperControlMode__aimingMode == 0:
            return _getDesiredShotPoint(self._SniperControlMode__aim.offset(), False)

    
    def updateShootingStatus(self, canShoot):
        if not self._SniperControlMode__isEnabled:
            raise AssertionError
        self._SniperControlMode__canShoot = canShoot

    
    def onRecreateDevice(self):
        self._SniperControlMode__gunMarker.onRecreateDevice()
        self._SniperControlMode__aim.onRecreateDevice()
        self._SniperControlMode__binoculars.onRecreateDevice()
        self._SniperControlMode__cam.onRecreateDevice()

    
    def getAim(self):
        return self._SniperControlMode__aim

    
    def setGUIVisible(self, isVisible):
        self._SniperControlMode__aim.setVisible(isVisible)
        self._SniperControlMode__gunMarker.setGUIVisible(isVisible)

    
    def getFixedAutorotation(self):
        return False

    
    def onChangeControlModeByScroll(self):
        if not self._SniperControlMode__isEnabled:
            raise AssertionError
        self._SniperControlMode__aih.onControlModeChanged('arcade', preferredPos = _getDesiredShotPoint(self._SniperControlMode__aim.offset(), False), yaw = self._SniperControlMode__cam.camera.direction.yaw, aimingMode = self._SniperControlMode__aimingMode, closesDist = True)

    
    def recreateCamera(self):
        preferredPos = _getDesiredShotPoint(self._SniperControlMode__aim.offset(), False)
        self._SniperControlMode__cam.disable()
        self._SniperControlMode__cam.enable(preferredPos, True)



class PostMortemControlMode(IControlMode):
    POSTMORTEM_DELAY_ENABLED = True
    _PostMortemControlMode__CAM_FLUENCY = 0
    camera = property((lambda self: self._PostMortemControlMode__cam))
    
    def __init__(self, dataSection, avatarInputHandler):
        self._PostMortemControlMode__aih = weakref.proxy(avatarInputHandler)
        self._PostMortemControlMode__aim = aims.createAim('postmortem')
        self._PostMortemControlMode__cam = cameras.ArcadeCamera(dataSection['camera'])
        self._PostMortemControlMode__vIDs = list()
        self._PostMortemControlMode__curIndex = -1
        self._PostMortemControlMode__curVehicleID = None
        self._PostMortemControlMode__selfVehicleID = None
        self._PostMortemControlMode__isEnabled = False
        self._PostMortemControlMode__cbIDWaitForCameraTarget = None
        self._PostMortemControlMode__postmortemDelay = None
        self._PostMortemControlMode__isObserverMode = False

    
    def prerequisites(self):
        return self._PostMortemControlMode__aim.prerequisites()

    
    def create(self):
        self._PostMortemControlMode__aim.create()
        self._PostMortemControlMode__cam.create(_ARCADE_CAM_PIVOT_POS, None, True)

    
    def destroy(self):
        self.disable()
        self._PostMortemControlMode__aim.destroy()
        self._PostMortemControlMode__cam = None

    
    def dumpState(self):
        return dumpStateEmpty()

    
    def enable(self, **args):
        ctrlState = args.get('ctrlState')
        player = BigWorld.player()
        if player:
            self._PostMortemControlMode__selfVehicleID = player.playerVehicleID
            self._PostMortemControlMode__isObserverMode = 'observer' in player.vehicleTypeDescriptor.type.tags
        
        self._PostMortemControlMode__cam.enable(None, False, args.get('postmortemParams'))
        self._PostMortemControlMode__aim.enable()
        self._PostMortemControlMode__connectToArena()
        _setCameraFluency(self._PostMortemControlMode__cam.camera, self._PostMortemControlMode__CAM_FLUENCY)
        self._PostMortemControlMode__isEnabled = True
        if self._PostMortemControlMode__isObserverMode:
            self._PostMortemControlMode__switchToVehicle(-1)
            return None
        if self.POSTMORTEM_DELAY_ENABLED and bool(args.get('bPostmortemDelay')):
            self._PostMortemControlMode__postmortemDelay = PostmortemDelay(self._PostMortemControlMode__cam, self._PostMortemControlMode__onPostmortemDelayStop)
            self._PostMortemControlMode__postmortemDelay.start()
        else:
            self._PostMortemControlMode__switchToVehicle(None)
        g_postProcessing.enable('postmortem')

    
    def disable(self):
        self._PostMortemControlMode__destroyPostmortemDelay()
        self._PostMortemControlMode__waitForCameraTargetCancel()
        self._PostMortemControlMode__isEnabled = False
        self._PostMortemControlMode__aim.disable()
        self._PostMortemControlMode__disconnectFromArena()
        self._PostMortemControlMode__cam.disable()
        self._PostMortemControlMode__curIndex = -1
        self._PostMortemControlMode__curVehicleID = None
        self._PostMortemControlMode__selfVehicleID = None
        g_postProcessing.disable()

    
    def handleKeyEvent(self, isDown, key, mods, event = None):
        if not self._PostMortemControlMode__isEnabled:
            raise AssertionError
        cmdMap = CommandMapping.g_instance
        if BigWorld.isKeyDown(Keys.KEY_CAPSLOCK) and constants.IS_DEVELOPMENT and isDown and key == Keys.KEY_F1:
            self._PostMortemControlMode__aih.onControlModeChanged('debug', prevModeName = 'postmortem', camMatrix = self._PostMortemControlMode__cam.camera.matrix)
            return True
        if cmdMap.isFired(CommandMapping.CMD_CM_POSTMORTEM_NEXT_VEHICLE, key) and isDown:
            self._PostMortemControlMode__switchToVehicle(-1, True)
            return True
        if cmdMap.isFired(CommandMapping.CMD_CM_POSTMORTEM_SELF_VEHICLE, key) and isDown:
            self._PostMortemControlMode__switchToVehicle(-1, False)
            return True

    
    def handleMouseEvent(self, dx, dy, dz):
        if not self._PostMortemControlMode__isEnabled:
            raise AssertionError
        if self._PostMortemControlMode__postmortemDelay is not None:
            return True
        GUI.mcursor().position = self._PostMortemControlMode__aim.offset()
        self._PostMortemControlMode__cam.update(dx, dy, _clamp(-1, 1, dz))
        return True

    
    def onRecreateDevice(self):
        self._PostMortemControlMode__aim.onRecreateDevice()

    
    def selectPlayer(self, vehId):
        self._PostMortemControlMode__switchToVehicle(vehId, False)

    
    def getAim(self):
        return self._PostMortemControlMode__aim

    
    def setGUIVisible(self, isVisible):
        self._PostMortemControlMode__aim.setVisible(isVisible)

    
    def isManualBind(self):
        return True

    
    def _PostMortemControlMode__destroyPostmortemDelay(self):
        if self._PostMortemControlMode__postmortemDelay is not None:
            self._PostMortemControlMode__postmortemDelay.destroy()
            self._PostMortemControlMode__postmortemDelay = None
        

    
    def _PostMortemControlMode__onPostmortemDelayStop(self):
        self._PostMortemControlMode__destroyPostmortemDelay()
        self._PostMortemControlMode__switchToVehicle(None)

    
    def _PostMortemControlMode__switchToVehicle(self, toId = None, toPrevious = False):
        if self._PostMortemControlMode__postmortemDelay is not None:
            return None
        player = BigWorld.player()
        replayCtrl = BattleReplay.g_replayCtrl
        self._PostMortemControlMode__waitForCameraTargetCancel()
        if toId == None and not (self._PostMortemControlMode__isObserverMode):
            self._PostMortemControlMode__curIndex = self._PostMortemControlMode__vIDs.index(player.playerVehicleID)
        elif toId >= 0:
            if toId in self._PostMortemControlMode__vIDs:
                self._PostMortemControlMode__curIndex = self._PostMortemControlMode__vIDs.index(toId)
            else:
                self._PostMortemControlMode__curIndex = 0
        elif toPrevious:
            self._PostMortemControlMode__curIndex -= 1
            if self._PostMortemControlMode__curIndex < 0:
                self._PostMortemControlMode__curIndex = len(self._PostMortemControlMode__vIDs) - 1
            
        else:
            self._PostMortemControlMode__curIndex += 1
            if self._PostMortemControlMode__curIndex >= len(self._PostMortemControlMode__vIDs):
                self._PostMortemControlMode__curIndex = 0
            
        if self._PostMortemControlMode__isObserverMode and len(self._PostMortemControlMode__vIDs) > 0 and self._PostMortemControlMode__vIDs[self._PostMortemControlMode__curIndex] == player.playerVehicleID:
            if toPrevious:
                pass
            1
            -1 += 1
            if self._PostMortemControlMode__curIndex < 0:
                self._PostMortemControlMode__curIndex = len(self._PostMortemControlMode__vIDs) - 1
            elif self._PostMortemControlMode__curIndex >= len(self._PostMortemControlMode__vIDs):
                self._PostMortemControlMode__curIndex = 0
            
        
        if replayCtrl.isPlaying:
            self._PostMortemControlMode__curVehicleID = replayCtrl.playerVehicleID
        else:
            newVehicleID = None
            if len(self._PostMortemControlMode__vIDs) == 0:
                newVehicleID = player.playerVehicleID
            else:
                newVehicleID = self._PostMortemControlMode__vIDs[self._PostMortemControlMode__curIndex]
            if self._PostMortemControlMode__isObserverMode:
                if self._PostMortemControlMode__curVehicleID != player.playerVehicleID and newVehicleID == player.playerVehicleID:
                    return None
            
            self._PostMortemControlMode__curVehicleID = newVehicleID
        player.positionControl.bindToVehicle(True, self._PostMortemControlMode__curVehicleID)
        self._PostMortemControlMode__aim.changeVehicle(self._PostMortemControlMode__curVehicleID)
        self._PostMortemControlMode__aih.onPostmortemVehicleChanged(self._PostMortemControlMode__curVehicleID)
        if self._PostMortemControlMode__isObserverMode:
            if self._PostMortemControlMode__cam.camera.target is None:
                self._PostMortemControlMode__cam.camera.target = player.getOwnVehicleMatrix()
            
        
        if self._PostMortemControlMode__curVehicleID != player.playerVehicleID and BigWorld.entity(self._PostMortemControlMode__curVehicleID) is None and not (replayCtrl.isPlaying) and not (self._PostMortemControlMode__isObserverMode) and player.arena.positions.get(self._PostMortemControlMode__curVehicleID) is None:
            self._PostMortemControlMode__switchToVehicle(-1, toPrevious)
            return None
        self._PostMortemControlMode__cbIDWaitForCameraTarget = BigWorld.callback(0.001, self._PostMortemControlMode__waitForCameraTarget)
        if not replayCtrl.isPlaying:
            self._PostMortemControlMode__cam.camera.target = Math.Matrix(self._PostMortemControlMode__cam.camera.target)
        

    
    def _PostMortemControlMode__onVehicleAdded(self, vehicleID):
        player = BigWorld.player()
        vDesc = player.arena.vehicles[vehicleID]
        if vDesc['team'] == player.team and vDesc['isAlive']:
            self._PostMortemControlMode__updateVIDsList()
        

    
    def _PostMortemControlMode__onVehicleKilled(self, victimID, killerID, reason):
        player = BigWorld.player()
        vDesc = player.arena.vehicles[victimID]
        if vDesc['team'] == player.team and not vDesc['isAlive']:
            self._PostMortemControlMode__delAndAdjustIDs(victimID)
        

    
    def _PostMortemControlMode__onPeriodChange(self, period, *args):
        if period != constants.ARENA_PERIOD.AFTERBATTLE:
            return None
        if self._PostMortemControlMode__isObserverMode:
            return None
        self._PostMortemControlMode__vIDs = list()
        self._PostMortemControlMode__vIDs.append(BigWorld.player().playerVehicleID)
        self._PostMortemControlMode__switchToVehicle(None)

    
    def _PostMortemControlMode__onVehicleLeaveWorld(self, vehicle):
        if vehicle.id == self._PostMortemControlMode__curVehicleID:
            self._PostMortemControlMode__switchToVehicle(None)
        

    
    def _playerComparator(self, x1, x2):
        if x1[0] < x2[0]:
            return 1
        if x1[0] > x2[0]:
            return -1
        if x1[1] < x2[1]:
            return 1
        if x1[1] > x2[1]:
            return -1
        if x1[2] < x2[2]:
            return -1
        if x1[2] > x2[2]:
            return 1
        if x1[3] < x2[3]:
            return -1
        if x1[3] > x2[3]:
            return 1

    
    def _PostMortemControlMode__updateVIDsList(self):
        player = BigWorld.player()
        vehicles = player.arena.vehicles
        self._PostMortemControlMode__vIDs = list()
        data = []
        for (id, desc) in vehicles.items():
            if (desc['team'] == player.team or desc['isAlive'] or id == player.playerVehicleID) and not desc['isAlive']:
                vehicleType = desc['vehicleType']
                if 'observer' not in vehicleType.type.tags:
                    data.append((desc['isAlive'], vehicleType.balanceWeight, vehicleType.type.shortUserString, desc['name'], id))
                
            'observer' not in vehicleType.type.tags
        
        data = sorted(data, cmp = self._playerComparator)
        for item in data:
            self._PostMortemControlMode__vIDs.append(item[4])
        

    
    def _PostMortemControlMode__connectToArena(self):
        player = BigWorld.player()
        player.arena.onVehicleAdded += self._PostMortemControlMode__onVehicleAdded
        player.arena.onVehicleKilled += self._PostMortemControlMode__onVehicleKilled
        player.arena.onPeriodChange += self._PostMortemControlMode__onPeriodChange
        player.onVehicleLeaveWorld += self._PostMortemControlMode__onVehicleLeaveWorld
        self._PostMortemControlMode__updateVIDsList()

    
    def _PostMortemControlMode__disconnectFromArena(self):
        player = BigWorld.player()
        player.arena.onVehicleAdded -= self._PostMortemControlMode__onVehicleAdded
        player.arena.onVehicleKilled -= self._PostMortemControlMode__onVehicleKilled
        player.arena.onPeriodChange -= self._PostMortemControlMode__onPeriodChange
        player.onVehicleLeaveWorld -= self._PostMortemControlMode__onVehicleLeaveWorld

    
    def _PostMortemControlMode__delAndAdjustIDs(self, id):
        if id == BigWorld.player().playerVehicleID:
            return None
        index = self._PostMortemControlMode__vIDs.index(id)
        del self._PostMortemControlMode__vIDs[index]
        if index <= self._PostMortemControlMode__curIndex:
            self._PostMortemControlMode__curIndex -= 1
        

    
    def _PostMortemControlMode__prepareNextVehicle(self, curNextIndex):
        player = BigWorld.player()
        curVPos = player.position
        nextIndex = curNextIndex
        curLen = 0
        for index in range(curNextIndex, len(self._PostMortemControlMode__vIDs)):
            v = BigWorld.entity(self._PostMortemControlMode__vIDs[index])
            p = player.arena.positions.get(self._PostMortemControlMode__vIDs[index], None)
            if v is not None or p is not None:
                if v is not None:
                    pass
                1
                pos = p
                tmpLen = curVPos.flatDistTo(pos)
                if tmpLen < curLen or curLen == 0:
                    curLen = tmpLen
                    nextIndex = index
                
            curLen == 0
        
        _swap(self._PostMortemControlMode__vIDs, curNextIndex, nextIndex)

    
    def _PostMortemControlMode__waitForCameraTarget(self):
        self._PostMortemControlMode__cbIDWaitForCameraTarget = None
        targetMProv = self._PostMortemControlMode__cam.camera.target
        targetPos = Math.Matrix(targetMProv).translation
        groundPos = Math.Vector3(targetPos)
        colRes = BigWorld.wg_collideSegment(BigWorld.player().spaceID, (groundPos.x, 1000, groundPos.z), (groundPos.x, -1000, groundPos.z), 128)
        if colRes is None:
            self._PostMortemControlMode__cbIDWaitForCameraTarget = BigWorld.callback(0.1, self._PostMortemControlMode__waitForCameraTarget)
            return None
        groundPos.y = colRes[0].y
        vehicle = BigWorld.entity(self._PostMortemControlMode__curVehicleID)
        if vehicle is None:
            targetMProv = Math.Matrix()
            targetMProv.setTranslate(groundPos)
            self._PostMortemControlMode__cam.camera.target = targetMProv
            self._PostMortemControlMode__cbIDWaitForCameraTarget = BigWorld.callback(0.1, self._PostMortemControlMode__waitForCameraTarget)
            return None
        camTargetTransOnly = Math.WGTranslationOnlyMP()
        camTargetTransOnly.source = vehicle.matrix
        self._PostMortemControlMode__cam.camera.target = camTargetTransOnly
        self._PostMortemControlMode__aih.onCameraChanged('postmortem', self._PostMortemControlMode__curVehicleID)

    
    def _PostMortemControlMode__waitForCameraTargetCancel(self):
        if self._PostMortemControlMode__cbIDWaitForCameraTarget is not None:
            BigWorld.cancelCallback(self._PostMortemControlMode__cbIDWaitForCameraTarget)
            self._PostMortemControlMode__cbIDWaitForCameraTarget = None
        

    
    def isSelfVehicle(self):
        return self._PostMortemControlMode__curVehicleID == self._PostMortemControlMode__selfVehicleID



class _ShellingControl:
    _ShellingControl__TARGET_MODEL_FILE_NAME = 'cat/models/position_gizmo.model'
    _ShellingControl__TARGET_POINTER_FILE_NAME = 'cat/target_pointer.dds'
    
    def __init__(self, camera):
        self._ShellingControl__bEnable = False
        self._ShellingControl__shellingObject = None
        self._ShellingControl__camera = camera
        self._ShellingControl__targetPointer = self._ShellingControl__createTargetPointer()
        self._ShellingControl__targetModel = self._ShellingControl__createTargetModel()
        self._ShellingControl__targetModelVisible = False
        self._ShellingControl__targetModelAutoUpdateCallbackID = None
        self._ShellingControl__targetModelAutoUpdateOnGetMatrix = None

    
    def destroy(self):
        self.setEnable(False)
        if self._ShellingControl__shellingObject is not None:
            self._ShellingControl__shellingObject.deselectTarget()
            self.installShellingObject(None)
        
        self._ShellingControl__createTargetPointer(bDelete = True)
        self._ShellingControl__targetModelVisible = None
        self._ShellingControl__createTargetModel(bDelete = True)
        self._ShellingControl__camera = None

    
    def setEnable(self, value):
        if self._ShellingControl__bEnable == value:
            return None
        if value:
            self._ShellingControl__showTargetPointer_directly(True)
            self._ShellingControl__showTargetModel_directly(self._ShellingControl__targetModelVisible)
        else:
            self._ShellingControl__showTargetPointer_directly(False)
            self._ShellingControl__showTargetModel_directly(False)
        self._ShellingControl__bEnable = value

    
    def installShellingObject(self, shellingObject):
        if shellingObject is not None:
            self.installShellingObject(None)
            self._ShellingControl__shellingObject = shellingObject
            self._ShellingControl__shellingObject._setCamera(self._ShellingControl__camera.camera)
        elif self._ShellingControl__shellingObject is not None:
            self._ShellingControl__shellingObject._setCamera(None)
            self._ShellingControl__shellingObject = None
        

    
    def getShellingObjectInstalled(self):
        return self._ShellingControl__shellingObject is not None

    
    def getShellingObject(self):
        return self._ShellingControl__shellingObject

    
    def showTargetPointer(self, value):
        self._ShellingControl__showTargetPointer_directly(value)

    
    def showTargetModel(self, value):
        self._ShellingControl__targetModelVisible = value
        if self._ShellingControl__bEnable:
            self._ShellingControl__showTargetModel_directly(value)
        

    
    def setTargetModelMatrix(self, worldMatrix):
        self._ShellingControl__targetModel.motors[0].signal = Math.Matrix(worldMatrix)

    
    def setTargetModelAutoUpdate(self, onGetMatrix = None):
        if self._ShellingControl__targetModelAutoUpdateCallbackID is not None:
            BigWorld.cancelCallback(self._ShellingControl__targetModelAutoUpdateCallbackID)
            self._ShellingControl__targetModelAutoUpdateCallbackID = None
        
        self._ShellingControl__targetModelAutoUpdateOnGetMatrix = onGetMatrix
        if self._ShellingControl__targetModelAutoUpdateOnGetMatrix is not None:
            self._ShellingControl__targetModelAutoUpdateCallbackID = BigWorld.callback(0.001, self._ShellingControl__targetModelAutoUpdateCallbackFunc)
        

    
    def recreate(self):
        isVisible = self._ShellingControl__targetPointer.visible
        self._ShellingControl__createTargetPointer(bDelete = True)
        self._ShellingControl__targetPointer = self._ShellingControl__createTargetPointer()
        self._ShellingControl__targetPointer.visible = isVisible
        isVisible = self._ShellingControl__targetModel.visible
        self._ShellingControl__createTargetModel(bDelete = True)
        self._ShellingControl__targetModel = self._ShellingControl__createTargetModel()
        self._ShellingControl__targetModel.visible = isVisible

    
    def handleKeyEvent(self, isDown, key, mods, event = None):
        if self._ShellingControl__shellingObject is not None:
            if key == Keys.KEY_LEFTMOUSE and isDown:
                self._ShellingControl__shellingObject.shoot()
                return True
            if key == Keys.KEY_RIGHTMOUSE and isDown:
                self._ShellingControl__shellingObject.selectTarget()
                return True
            if key == Keys.KEY_MIDDLEMOUSE and isDown:
                self._ShellingControl__shellingObject.deselectTarget()
                return True
        
        return False

    
    def _ShellingControl__targetModelAutoUpdateCallbackFunc(self):
        self._ShellingControl__targetModelAutoUpdateCallbackID = None
        nextCallbackInterval = 0.001
        
        try:
            newMatrix = self._ShellingControl__targetModelAutoUpdateOnGetMatrix()
            if newMatrix is not None:
                self._ShellingControl__targetModel.motors[0].signal = Math.Matrix(newMatrix)
            else:
                nextCallbackInterval = 2
        except:
            nextCallbackInterval = 2
            LOG_DEBUG('<_targetModelAutoUpdateCallbackFunc>: target model is not updated')

        self._ShellingControl__targetModelAutoUpdateCallbackID = BigWorld.callback(nextCallbackInterval, self._ShellingControl__targetModelAutoUpdateCallbackFunc)

    
    def _ShellingControl__createTargetPointer(self, bDelete = False):
        result = None
        if not bDelete:
            result = GUI.Simple(_ShellingControl._ShellingControl__TARGET_POINTER_FILE_NAME)
            result.position[2] = 0.7
            result.size = (2, 2)
            result.materialFX = 'BLEND_INVERSE_COLOUR'
            result.filterType = 'LINEAR'
            result.visible = False
            GUI.addRoot(result)
        elif self._ShellingControl__targetPointer is not None:
            GUI.delRoot(self._ShellingControl__targetPointer)
            self._ShellingControl__targetPointer = None
        
        return result

    
    def _ShellingControl__createTargetModel(self, bDelete = False):
        result = None
        if not bDelete:
            result = BigWorld.Model(_ShellingControl._ShellingControl__TARGET_MODEL_FILE_NAME)
            result.addMotor(BigWorld.Servo(Math.Matrix()))
            result.visible = False
            BigWorld.addModel(result)
        elif self._ShellingControl__targetModel is not None:
            self.setTargetModelAutoUpdate(None)
            BigWorld.delModel(self._ShellingControl__targetModel)
            self._ShellingControl__targetModel = None
        
        return result

    
    def _ShellingControl__showTargetPointer_directly(self, value):
        self._ShellingControl__targetPointer.visible = value

    
    def _ShellingControl__showTargetModel_directly(self, value):
        self._ShellingControl__targetModel.visible = value



class _Binoculars(Flash):
    _SWF_FILE_NAME = 'ScopeShadow.swf'
    
    def __init__(self):
        Flash.__init__(self, self._SWF_FILE_NAME)
        self.component.wg_inputKeyMode = 2
        self.component.position.z = DEPTH_OF_Binoculars
        self.movie.backgroundAlpha = 0

    
    def enable(self):
        self.onRecreateDevice()
        self.active(True)

    
    def disable(self):
        self.active(False)

    
    def onRecreateDevice(self):
        scrRes = GUI.screenResolution()
        self.call('onRecreateDevice', [
            scrRes[0],
            scrRes[1]])



class _SuperGunMarker:
    
    def __init__(self, mode = 'arcade', isStrategic = False):
        self._SuperGunMarker__show2 = useServerAim()
        if not constants.IS_DEVELOPMENT:
            pass
        self._SuperGunMarker__show1 = not (self._SuperGunMarker__show2)
        self._SuperGunMarker__isGuiVisible = True
        if isStrategic:
            self._SuperGunMarker__gm1 = _SPGFlashGunMarker()
        else:
            self._SuperGunMarker__gm1 = _FlashGunMarker(mode)
        if isStrategic:
            self._SuperGunMarker__gm2 = _SPGFlashGunMarker(True)
        else:
            self._SuperGunMarker__gm2 = _FlashGunMarker(mode)

    
    def prerequisites(self):
        return self._SuperGunMarker__gm1.prerequisites() + self._SuperGunMarker__gm2.prerequisites()

    
    def create(self):
        self._SuperGunMarker__gm1.create()
        self._SuperGunMarker__gm2.create()

    
    def destroy(self):
        self._SuperGunMarker__gm1.destroy()
        self._SuperGunMarker__gm2.destroy()

    
    def enable(self, state):
        if state is not None:
            self._SuperGunMarker__show1 = state.get('show1', False)
            self._SuperGunMarker__show2 = state.get('show2', False)
        
        self._SuperGunMarker__gm1.enable(state)
        self._SuperGunMarker__gm2.enable(state)
        self.show(self._SuperGunMarker__show1)
        self.show2(self._SuperGunMarker__show2)
        self.onRecreateDevice()

    
    def disable(self):
        self._SuperGunMarker__gm1.disable()
        self._SuperGunMarker__gm2.disable()

    
    def dumpState(self):
        out = self._SuperGunMarker__gm1.dumpState()
        out['pos2'] = self._SuperGunMarker__gm2.getPosition()
        out['show1'] = self._SuperGunMarker__show1
        out['show2'] = self._SuperGunMarker__show2
        return out

    
    def matrixProvider(self):
        return self._SuperGunMarker__gm1.matrixProvider

    
    def setReloading(self, duration, startTime = None):
        self._SuperGunMarker__gm1.setReloading(duration, startTime)
        self._SuperGunMarker__gm2.setReloading(duration, startTime)

    
    def show(self, flag):
        self._SuperGunMarker__show1 = flag
        if flag:
            pass
        self._SuperGunMarker__gm1.show(self._SuperGunMarker__isGuiVisible)

    
    def show2(self, flag):
        show2Prev = self._SuperGunMarker__show2
        if flag:
            pass
        self._SuperGunMarker__show2 = self._SuperGunMarker__isGuiVisible
        if self._SuperGunMarker__show2 and show2Prev != self._SuperGunMarker__show2:
            self._SuperGunMarker__gm2.setPosition(self._SuperGunMarker__gm1.getPosition())
        
        self._SuperGunMarker__gm2.show(self._SuperGunMarker__show2)
        if not constants.IS_DEVELOPMENT:
            self.show(not flag)
        

    
    def setGUIVisible(self, isVisible, valueUpdate = False):
        self._SuperGunMarker__isGuiVisible = isVisible
        if not valueUpdate:
            serverAim = useServerAim()
            if not constants.IS_DEVELOPMENT:
                pass
            self.show(not serverAim)
            self.show2(serverAim)
        

    
    def update(self, pos, dir, size, relaxTime, collData):
        self._SuperGunMarker__gm1.update(pos, dir, size, relaxTime, collData)

    
    def update2(self, pos, dir, size, relaxTime, collData):
        self._SuperGunMarker__gm2.update(pos, dir, size, relaxTime, collData)

    
    def onRecreateDevice(self):
        self._SuperGunMarker__gm1.onRecreateDevice()
        self._SuperGunMarker__gm2.onRecreateDevice()

    
    def setPosition(self, pos):
        self._SuperGunMarker__gm1.setPosition(pos)

    
    def setPosition2(self, pos):
        self._SuperGunMarker__gm2.setPosition(pos)

    
    def getPosition(self):
        return self._SuperGunMarker__gm1.getPosition()

    
    def getPosition2(self):
        return self._SuperGunMarker__gm2.getPosition()



class _SPGFlashGunMarker(Flash):
    _FLASH_CLASS = 'WGSPGCrosshairFlash'
    _SWF_FILE_NAME = 'crosshair_strategic.swf'
    _SWF_SIZE = (620, 620)
    
    def __init__(self, isDebug = False):
        Flash.__init__(self, self._SWF_FILE_NAME, self._FLASH_CLASS)
        self.component.wg_inputKeyMode = 2
        self.component.position.z = DEPTH_OF_GunMarker
        self.component.focus = False
        self.component.moveFocus = False
        self.component.heightMode = 'PIXEL'
        self.component.widthMode = 'PIXEL'
        self.movie.backgroundAlpha = 0
        self.flashSize = self._SWF_SIZE
        self._SPGFlashGunMarker__animMat = None
        if isDebug:
            self.call('Crosshair.setAsDebug', [
                isDebug])
        

    
    def prerequisites(self):
        return []

    
    def dumpState(self):
        return {
            'reload': dict(self._SPGFlashGunMarker__reload),
            'pos1': self.getPosition(),
            'size': 0 }

    
    def create(self):
        self.component.wg_maxTime = 5
        self.component.wg_serverTickLength = 0.1
        self.component.wg_sizeScaleRate = 10
        self.component.wg_sizeConstraints = Math.Vector2(50, 100)
        self.component.wg_usePyCollDetect = False
        self.component.wg_setRelaxTime(0.1)
        self.active(True)
        self._SPGFlashGunMarker__reload = {
            'start_time': 0,
            'duration': 0,
            'isReloading': False }
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.replayContainsGunReloads:
            self._SPGFlashGunMarker__cbIdSetReloading = BigWorld.callback(0, self.setReloadingFromReplay)
        else:
            self._SPGFlashGunMarker__cbIdSetReloading = None
        self.onRecreateDevice()

    
    def destroy(self):
        if self._SPGFlashGunMarker__cbIdSetReloading is not None:
            BigWorld.cancelCallback(self._SPGFlashGunMarker__cbIdSetReloading)
            self._SPGFlashGunMarker__cbIdSetReloading = None
        
        self.active(False)

    
    def enable(self, state):
        if state is not None:
            rs = state['reload']
            self.setReloading(rs['duration'], rs['startTime'], rs['isReloading'], correction = rs.get('correction'))
            self.setPosition(state['pos1'])
        

    
    def disable(self):
        self.show(False)

    
    def matrixProvider(self):
        return self._SPGFlashGunMarker__animMat

    
    def show(self, flag):
        self.component.visible = flag

    
    def setReloading(self, duration, startTime = None, isReloading = True, correction = None):
        rs = self._SPGFlashGunMarker__reload
        rs['isReloading'] = isReloading
        if startTime is None:
            pass
        1
        rs['startTime'] = startTime
        rs['duration'] = duration
        rs['correction'] = correction
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.replayContainsGunReloads:
            return None
        if startTime is None:
            pass
        1
        startTime = BigWorld.time() - startTime
        self.call('Crosshair.setReloading', [
            duration,
            startTime,
            isReloading])

    
    def setReloadingAsPercent(self, percent):
        self.call('Crosshair.setReloadingAsPercent', [
            percent])

    
    def setReloadingFromReplay(self):
        self.setReloadingAsPercent(100 * BattleReplay.g_replayCtrl.getGunReloadAmountLeft())
        self._SPGFlashGunMarker__cbIdSetReloading = BigWorld.callback(0, self.setReloadingFromReplay)

    
    def update(self, pos, dir, size, relaxTime, collData):
        m = Math.Matrix()
        m.setTranslate(pos)
        self._SPGFlashGunMarker__setupMatrixAnimation()
        self._SPGFlashGunMarker__animMat.keyframes = ((0, Math.Matrix(self._SPGFlashGunMarker__animMat)), (relaxTime, m))
        self._SPGFlashGunMarker__animMat.time = 0
        self._SPGFlashGunMarker__spgUpdate(size)

    
    def onRecreateDevice(self):
        self.component.size = GUI.screenResolution()

    
    def setPosition(self, pos):
        m = Math.Matrix()
        m.setTranslate(pos)
        self._SPGFlashGunMarker__setupMatrixAnimation()
        self._SPGFlashGunMarker__animMat.keyframes = ((0, m), (0, m))
        self._SPGFlashGunMarker__animMat.time = 0

    
    def getPosition(self):
        if self._SPGFlashGunMarker__animMat is None:
            return Math.Vector3(0, 0, 0)
        return Math.Matrix(self._SPGFlashGunMarker__animMat).translation

    
    def _SPGFlashGunMarker__setupMatrixAnimation(self):
        if self._SPGFlashGunMarker__animMat is not None:
            return None
        self._SPGFlashGunMarker__animMat = Math.MatrixAnimation()

    
    def _SPGFlashGunMarker__spgUpdate(self, size):
        gunRotator = BigWorld.player().gunRotator
        shotDesc = BigWorld.player().vehicleTypeDescriptor.shot
        
        try:
            dispersionAngle = gunRotator.dispersionAngle
            (pos3d, vel3d) = gunRotator._VehicleGunRotator__getCurShotPosition()
            gravity3d = Math.Vector3(0, -shotDesc['gravity'], 0)
            self.component.wg_update(pos3d, vel3d, gravity3d, dispersionAngle, size)
        except:
            LOG_CURRENT_EXCEPTION()




class _FlashGunMarker(Flash):
    _FLASH_CLASS = 'WGCrosshairFlash'
    _SWF_FILE_NAME = 'crosshair_sniper.swf'
    _SWF_SIZE = (620, 620)
    _colorsByPiercing = {
        'default': {
            'not_pierced': 'red',
            'little_pierced': 'orange',
            'great_pierced': 'green' },
        'color_blind': {
            'not_pierced': 'purple',
            'little_pierced': 'yellow',
            'great_pierced': 'green' } }
    
    def __init__(self, mode):
        Flash.__init__(self, self._SWF_FILE_NAME, self._FLASH_CLASS)
        self.component.wg_inputKeyMode = 2
        self.component.position.z = DEPTH_OF_GunMarker
        self.component.focus = False
        self.component.moveFocus = False
        self.component.heightMode = 'PIXEL'
        self.component.widthMode = 'PIXEL'
        self.movie.backgroundAlpha = 0
        self.flashSize = self._SWF_SIZE
        self.mode = mode
        self._FlashGunMarker__curSize = 0
        self._FlashGunMarker__animMat = None

    
    def prerequisites(self):
        return []

    
    def dumpState(self):
        return {
            'reload': dict(self._FlashGunMarker__reload),
            'pos1': self.getPosition(),
            'size': self._FlashGunMarker__curSize }

    
    def create(self):
        if AccountSettings.getSettings('isColorBlind'):
            pass
        1
        type = 'default'
        self._curColors = self._colorsByPiercing[type]
        AccountSettings.onSettingsChanging += self.applySettings
        self.component.wg_sizeConstraint = (10, 300)
        self.component.wg_setStartSize(10)
        self.active(True)
        self._FlashGunMarker__reload = {
            'start_time': 0,
            'duration': 0,
            'isReloading': False }
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.replayContainsGunReloads:
            self._FlashGunMarker__cbIdSetReloading = BigWorld.callback(0, self.setReloadingFromReplay)
        else:
            self._FlashGunMarker__cbIdSetReloading = None
        self.onRecreateDevice()

    
    def applySettings(self, type):
        if type == 'arcade':
            settings = dict(AccountSettings.getSettings('arcade'))
            current = settings['gunTag']
            self.call('Crosshair.setGunTag', [
                current['alpha'],
                current['type']])
            current = settings['mixing']
            self.call('Crosshair.setMixing', [
                current['alpha'],
                current['type']])
        
        if type == 'sniper':
            settings = dict(AccountSettings.getSettings('sniper'))
            current = settings['snpGunTag']
            self.call('Crosshair.setGunTag', [
                current['alpha'],
                current['type']])
            current = settings['snpMixing']
            self.call('Crosshair.setMixing', [
                current['alpha'],
                current['type']])
        
        if type == 'isColorBlind':
            if AccountSettings.getSettings('isColorBlind'):
                pass
            1
            type = 'default'
            self._curColors = self._colorsByPiercing[type]
        

    
    def destroy(self):
        AccountSettings.onSettingsChanging -= self.applySettings
        self.active(False)
        if self._FlashGunMarker__cbIdSetReloading is not None:
            BigWorld.cancelCallback(self._FlashGunMarker__cbIdSetReloading)
            self._FlashGunMarker__cbIdSetReloading = None
        
        self._FlashGunMarker__animMat = None

    
    def enable(self, state):
        self.applySettings(self.mode)
        if state is not None:
            rs = state['reload']
            self.setReloading(rs['duration'], rs['startTime'], rs['isReloading'], correction = rs.get('correction'), switched = True)
            self.setPosition(state['pos1'])
            self.component.wg_updateSize(state['size'], 0)
        

    
    def disable(self):
        self.show(False)

    
    def matrixProvider(self):
        return self._FlashGunMarker__animMat

    
    def show(self, flag):
        self.component.visible = flag

    
    def setReloading(self, duration, startTime = None, isReloading = True, correction = None, switched = False):
        rs = self._FlashGunMarker__reload
        _isReloading = rs.get('isReloading', False)
        _startTime = rs.get('startTime', 0)
        _duration = rs.get('duration', 0)
        isReloading = duration > 0
        rs['isReloading'] = isReloading
        rs['correction'] = None
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying:
            pass
        allowFlashCall = not (replayCtrl.replayContainsGunReloads)
        if not switched and _isReloading and duration > 0 and _duration > 0:
            current = BigWorld.time()
            rs['correction'] = {
                'timeRemaining': duration,
                'startTime': current,
                'startPosition': (current - _startTime) / _duration }
            if allowFlashCall:
                self.call('Crosshair.correctReloadingTime', [
                    duration])
            
        elif startTime is None:
            pass
        
        rs['startTime'] = startTime
        rs['duration'] = duration
        if correction is not None:
            params = self._getCorrectionReloadingParams(correction)
            if params is not None:
                rs['correction'] = correction
                if allowFlashCall:
                    self.call('Crosshair.setReloading', params)
                
            
        elif startTime is None:
            pass
        
        startTime = BigWorld.time() - startTime
        if allowFlashCall:
            self.call('Crosshair.setReloading', [
                duration,
                startTime,
                isReloading])
        

    
    def setReloadingFromReplay(self):
        self._setReloadingAsPercent(100 * BattleReplay.g_replayCtrl.getGunReloadAmountLeft())
        self._FlashGunMarker__cbIdSetReloading = BigWorld.callback(0, self.setReloadingFromReplay)

    
    def _setReloadingAsPercent(self, percent):
        self.call('Crosshair.setReloadingAsPercent', [
            percent])

    
    def update(self, pos, dir, size, relaxTime, collData):
        m = Math.Matrix()
        m.setTranslate(pos)
        self._FlashGunMarker__setupMatrixAnimation()
        self._FlashGunMarker__animMat.keyframes = ((0, Math.Matrix(self._FlashGunMarker__animMat)), (relaxTime, m))
        self._FlashGunMarker__animMat.time = 0
        self._FlashGunMarker__curSize = _calcScale(m, size) * GUI.screenResolution()[0] * 0.5
        if collData is None or collData[0].publicInfo['team'] == BigWorld.player().team:
            self.call('Crosshair.setMarkerType', [
                'normal'])
        else:
            self._changeColor(pos, collData[2])
        self.component.wg_updateSize(self._FlashGunMarker__curSize, relaxTime)

    
    def onRecreateDevice(self):
        self.component.size = GUI.screenResolution()

    
    def setPosition(self, pos):
        m = Math.Matrix()
        m.setTranslate(pos)
        self._FlashGunMarker__setupMatrixAnimation()
        self._FlashGunMarker__animMat.keyframes = ((0, m), (0, m))
        self._FlashGunMarker__animMat.time = 0

    
    def getPosition(self):
        if self._FlashGunMarker__animMat is None:
            return Math.Vector3(0, 0, 0)
        return Math.Matrix(self._FlashGunMarker__animMat).translation

    
    def _FlashGunMarker__setupMatrixAnimation(self):
        if self._FlashGunMarker__animMat is not None:
            return None
        self._FlashGunMarker__animMat = Math.MatrixAnimation()
        self.component.wg_positionMatProv = self._FlashGunMarker__animMat

    
    def _changeColor(self, hitPoint, armor):
        vDesc = BigWorld.player().vehicleTypeDescriptor
        ppDesc = vDesc.shot['piercingPower']
        maxDist = vDesc.shot['maxDistance']
        dist = (hitPoint - BigWorld.player().getOwnVehiclePosition()).length
        if dist <= 100:
            piercingPower = ppDesc[0]
        elif maxDist > dist:
            (p100, p500) = ppDesc
            piercingPower = p100 + (p500 - p100) * (dist - 100) / 400
            if piercingPower < 0:
                piercingPower = 0
            
        else:
            piercingPower = 0
        piercingPercent = 1000
        if piercingPower > 0:
            piercingPercent = 100 + ((armor - piercingPower) / piercingPower) * 100
        
        type = 'great_pierced'
        if piercingPercent > 150:
            type = 'not_pierced'
        elif 90 < piercingPercent:
            pass
        elif piercingPercent > 150:
            type = 'little_pierced'
        
        self.call('Crosshair.setMarkerType', [
            self._curColors[type]])

    
    def _getCorrectionReloadingParams(self, correction):
        cTimeRemaining = correction.get('timeRemaining', 0)
        cStartTime = correction.get('startTime', 0)
        cStartPosition = correction.get('startPosition', 0)
        if not cTimeRemaining > 0:
            LOG_WARNING('timeRemaining - invalid value ', cTimeRemaining)
            return None
        delta = BigWorld.time() - cStartTime
        currentPosition = cStartPosition + (delta / cTimeRemaining) * (1 - cStartPosition)
        return [
            cTimeRemaining - delta,
            cStartTime,
            True,
            currentPosition * 100]



class _GunMarker:
    
    def __init__(self, dataSection):
        self._readCfg(dataSection)
        self._GunMarker__mover = None
        self._GunMarker__gui = None
        self._GunMarker__model = None
        self._GunMarker__animMat = None

    
    def prerequisites(self):
        return [
            self._GunMarker__cfg['texture']]

    
    def create(self):
        cfg = self._GunMarker__cfg
        sr = GUI.screenResolution()
        self._GunMarker__gui = GUI.Window('')
        self._GunMarker__gui.heightMode = 'PIXEL'
        self._GunMarker__gui.widthMode = 'PIXEL'
        self._GunMarker__gui.width = sr[0]
        self._GunMarker__gui.height = sr[1]
        self._GunMarker__gui.position[2] = DEPTH_OF_GunMarker
        self._GunMarker__gui.visible = False
        mover = GUI.MatrixShader()
        mover.target = None
        mover.eta = 0
        mover.blend = True
        self._GunMarker__gui.addShader(mover, 'mover')
        elems = cfg['elems']
        self._createGui(elems['top'], 'top')
        self._createGui(elems['right'], 'right')
        self._createGui(elems['bottom'], 'bottom')
        self._createGui(elems['left'], 'left')
        center = GUI.Simple(cfg['texture'])
        center.mapping = _buildTexCoord(elems['center'][0], cfg['size'])
        center.heightMode = 'PIXEL'
        center.widthMode = 'PIXEL'
        center.materialFX = 'BLEND'
        center.size = elems['center'][1]
        self._GunMarker__gui.addChild(center, 'center')
        GUI.addRoot(self._GunMarker__gui)

    
    def destroy(self):
        GUI.delRoot(self._GunMarker__gui)
        self._GunMarker__animMat = None

    
    def matrixProvider(self):
        return self._GunMarker__animMat

    
    def show(self, flag):
        self._GunMarker__gui.visible = flag

    
    def update(self, pos, dir, size, relaxTime, collData):
        m = Math.Matrix()
        m.setTranslate(pos)
        self._GunMarker__setupMatrixAnimation(relaxTime)
        self._GunMarker__animMat.keyframes = ((0, Math.Matrix(self._GunMarker__animMat)), (relaxTime, m))
        self._GunMarker__animMat.time = 0
        sr = GUI.screenResolution()
        aspect = sr[0] / float(sr[1])
        scale = _calcScale(m, size)
        self._transformGui(Math.Vector3(0, scale * aspect, 0), relaxTime, 'top')
        self._transformGui(Math.Vector3(scale, 0, 0), relaxTime, 'right')
        self._transformGui(Math.Vector3(0, -scale * aspect, 0), relaxTime, 'bottom')
        self._transformGui(Math.Vector3(-scale, 0, 0), relaxTime, 'left')

    
    def onRecreateDevice(self):
        sr = GUI.screenResolution()
        self._GunMarker__gui.width = sr[0]
        self._GunMarker__gui.height = sr[1]

    
    def setPosition(self, pos):
        m = Math.Matrix()
        m.setTranslate(pos)
        self._GunMarker__setupMatrixAnimation(0)
        self._GunMarker__animMat.keyframes = ((0, m), (0, m))
        self._GunMarker__animMat.time = 0

    
    def getPosition(self):
        if self._GunMarker__animMat is None:
            return Math.Vector3(0, 0, 0)
        return Math.Matrix(self._GunMarker__animMat).translation

    
    def _createGui(self, elemDesc, name):
        mover = GUI.MatrixShader()
        mover.blend = True
        mover.eta = 0
        gui = GUI.Simple(self._GunMarker__cfg['texture'])
        gui.mapping = _buildTexCoord(elemDesc[0], self._GunMarker__cfg['size'])
        gui.verticalPositionMode = 'CLIP'
        gui.horizontalPositionMode = 'CLIP'
        gui.heightMode = 'PIXEL'
        gui.widthMode = 'PIXEL'
        gui.materialFX = 'BLEND'
        gui.size = elemDesc[1]
        gui.addShader(mover, 'mover')
        self._GunMarker__gui.addChild(gui, name)

    
    def _transformGui(self, translate, relaxTime, name):
        mat = Math.Matrix()
        mat.setTranslate(translate)
        mov = getattr(self._GunMarker__gui, name).mover
        mov.target = mat
        mov.eta = relaxTime

    
    def _readCfg(self, dataSection):
        self._GunMarker__cfg = dict()
        self._GunMarker__cfg['texture'] = dataSection.readString('texture')
        self._GunMarker__cfg['size'] = dataSection.readVector2('size')
        self._GunMarker__cfg['elems'] = dict()
        self._GunMarker__readElem(dataSection['elems/top'], 'top')
        self._GunMarker__readElem(dataSection['elems/right'], 'right')
        self._GunMarker__readElem(dataSection['elems/bottom'], 'bottom')
        self._GunMarker__readElem(dataSection['elems/left'], 'left')
        self._GunMarker__readElem(dataSection['elems/center'], 'center')

    
    def _GunMarker__readElem(self, dataSection, name):
        mapping = dataSection.readVector4('mapping', Math.Vector4(0, 0, 0, 0))
        size = dataSection.readVector2('size', Math.Vector2(0, 0))
        self._GunMarker__cfg['elems'][name] = (mapping, size)

    
    def _GunMarker__setupMatrixAnimation(self, relaxTime):
        if self._GunMarker__animMat is not None:
            return None
        self._GunMarker__animMat = Math.MatrixAnimation()
        _wtcMat = GUI.WorldToClipMP()
        _wtcMat.target = self._GunMarker__animMat
        _wtcMat.onlyFront = True
        self._GunMarker__gui.mover.target = _wtcMat
        self._GunMarker__gui.mover.eta = relaxTime



class _MouseVehicleRotator:
    ROTATION_ACTIVITY_INTERVAL = 0.2
    
    def __init__(self):
        self._MouseVehicleRotator__rotationState = 0
        self._MouseVehicleRotator__cbIDActivity = None

    
    def destroy(self):
        self.unforceRotation(isDestroy = True)

    
    def handleMouse(self, dx):
        import Avatar as Avatar
        player = BigWorld.player()
        if not isinstance(player, Avatar.PlayerAvatar):
            return None
        cmdMap = CommandMapping.g_instance
        if not cmdMap.isActive(CommandMapping.CMD_MOVE_FORWARD_SPEC):
            return None
        if dx * self._MouseVehicleRotator__rotationState > 0:
            return None
        self._MouseVehicleRotator__rotationState = _clamp(-1, 1, dx)
        bStartRotation = dx != 0
        if self._MouseVehicleRotator__cbIDActivity is not None:
            BigWorld.cancelCallback(self._MouseVehicleRotator__cbIDActivity)
            self._MouseVehicleRotator__cbIDActivity = None
        
        if bStartRotation:
            self._MouseVehicleRotator__cbIDActivity = BigWorld.callback(self.ROTATION_ACTIVITY_INTERVAL, self._MouseVehicleRotator__cbActivity)
        
        if bStartRotation:
            forceMask = 12
            if dx < 0:
                forceFlags = 4
            
            if dx > 0:
                forceFlags = 8
            
        else:
            forceMask = 0
            forceFlags = 204
        BigWorld.player().moveVehicleByCurrentKeys(bStartRotation, forceFlags, forceMask)

    
    def unforceRotation(self, isDestroy = False):
        self._MouseVehicleRotator__rotationState = 0
        if self._MouseVehicleRotator__cbIDActivity is not None:
            BigWorld.cancelCallback(self._MouseVehicleRotator__cbIDActivity)
            self._MouseVehicleRotator__cbIDActivity = None
        
        if not isDestroy:
            import Avatar
            player = BigWorld.player()
            if not isinstance(player, Avatar.PlayerAvatar):
                return None
            player.moveVehicleByCurrentKeys(False)
        

    
    def _MouseVehicleRotator__cbActivity(self):
        self._MouseVehicleRotator__cbIDActivity = None
        self.unforceRotation()



def getFocalPoint():
    (dir, start) = cameras.getWorldRayAndPoint(0, 0)
    end = start + dir.scale(100000)
    point = collideDynamicAndStatic(start, end, (BigWorld.player().playerVehicleID,), 0)
    if point is not None:
        return point[0]
    return _shootInSkyPoint(start, dir)


def useServerAim():
    return AccountSettings.getSettings('useServerAim')


def dumpStateEmpty():
    return {
        'gunMarkerPosition': None,
        'gunMarkerPosition2': None,
        'aimState': None }


def collideStaticOnly(startPoint, endPoint):
    res = None
    testRes = BigWorld.wg_collideSegment(BigWorld.player().spaceID, startPoint, endPoint, 128)
    if testRes is not None:
        res = (testRes[0], None)
    
    return res


def collideStaticOnlyRichInfo(startPoint, endPoint):
    testRes = BigWorld.wg_collideSegment(BigWorld.player().spaceID, startPoint, endPoint, 128)
    if testRes is not None:
        return testRes


def _getShotPointOnDir(start, dir):
    point = collideDynamicAndStatic(start, start + dir.scale(10000), (BigWorld.player().playerVehicleID,))
    if point is not None:
        return point[0]
    return _shootInSkyPoint(start, dir)


def _getDesiredShotPoint(mousePos = None, onlyOnGround = False, isStrategicMode = False):
    if mousePos is not None:
        (dir, start) = cameras.getWorldRayAndPoint(mousePos[0], mousePos[1])
        end = start + dir.scale(100000)
        if isStrategicMode:
            point1 = collideStaticOnly(start, end)
            point2 = collideDynamicAndStatic(start, end, (BigWorld.player().playerVehicleID,), skipGun = isStrategicMode)
            if point1 is None or point2 is None:
                point = None
            else:
                dir = Math.Vector3(point2[0]) - Math.Vector3(point1[0])
                point = (Math.Vector3(point1[0]) + dir.scale(0.5), None)
        else:
            point = collideDynamicAndStatic(start, end, (BigWorld.player().playerVehicleID,), skipGun = isStrategicMode)
    else:
        mp = (GUI.mcursor().position.x, GUI.mcursor().position.y)
        if abs(mp[0]) < 0.995 and abs(mp[1]) < 0.995:
            (dir, start) = cameras.getWorldRayAndPoint(mp[0], mp[1])
            end = start + dir.scale(100000)
            point = collideDynamicAndStatic(start, end, (BigWorld.player().playerVehicleID,), skipGun = isStrategicMode)
        else:
            return None
        if abs(mp[1]) < 0.995 is not None:
            return point[0]
        if not onlyOnGround:
            return _shootInSkyPoint(start, dir)
        return None
    return mousePos is not None


def _shootInSkyPoint(startPos, dir):
    dirFromCam = dir
    start = startPos
    dirFromCam.normalise()
    vehicle = BigWorld.entity(BigWorld.player().playerVehicleID)
    if vehicle is not None and vehicle.isStarted:
        shotPos = Math.Vector3(vehicle.appearance.modelsDesc['gun']['model'].position)
        shotDesc = vehicle.typeDescriptor.shot
    else:
        type = BigWorld.player().arena.vehicles[BigWorld.player().playerVehicleID]['vehicleType']
        shotPos = BigWorld.player().getOwnVehiclePosition()
        shotPos += type.hull['turretPositions'][0] + type.turret['gunPosition']
        shotDesc = type.shot
    dirAtCam = shotPos - start
    dirAtCam.normalise()
    cosAngle = dirAtCam.dot(dirFromCam)
    a = shotDesc['maxDistance']
    b = shotPos.distTo(start)
    
    try:
        dist = b * cosAngle + math.sqrt(b * b * (cosAngle * cosAngle - 1) + a * a)
    except:
        dist = shotDesc['maxDistance']
        LOG_CODEPOINT_WARNING()

    finalPoint = start + dirFromCam.scale(dist)
    intersecPoint = BigWorld.player().arena.collideWithSpaceBB(start, finalPoint)
    if intersecPoint is not None:
        finalPoint = intersecPoint
    
    return finalPoint


def _clamp(minVal, maxVal, val):
    tmpVal = val
    tmpVal = max(minVal, val)
    tmpVal = min(maxVal, tmpVal)
    return tmpVal


def _sign(val):
    if val > 0:
        return 1
    if val < 0:
        return -1
    return 0


def _buildTexCoord(vec4, textureSize):
    out = ((vec4[0] / textureSize[0], vec4[1] / textureSize[1]), (vec4[0] / textureSize[0], vec4[3] / textureSize[1]), (vec4[2] / textureSize[0], vec4[3] / textureSize[1]), (vec4[2] / textureSize[0], vec4[1] / textureSize[1]))
    return out


def _setCameraFluency(cam, value):
    cam.maxDistHalfLife = value
    cam.turningHalfLife = value
    cam.movementHalfLife = value


def _swap(data, index1, index2):
    if index1 == index2:
        return None
    tmp = data[index1]
    data[index1] = data[index2]
    data[index2] = tmp


def _calcScale(worldMat, size):
    sr = GUI.screenResolution()
    aspect = sr[0] / sr[1]
    proj = BigWorld.projection()
    wtcMat = Math.Matrix()
    wtcMat.perspectiveProjection(proj.fov, aspect, proj.nearPlane, proj.farPlane)
    wtcMat.preMultiply(BigWorld.camera().matrix)
    wtcMat.preMultiply(worldMat)
    pointMat = Math.Matrix()
    pointMat.set(BigWorld.camera().matrix)
    transl = Math.Matrix()
    transl.setTranslate(Math.Vector3(size, 0, 0))
    pointMat.postMultiply(transl)
    pointMat.postMultiply(BigWorld.camera().invViewMatrix)
    p = pointMat.applyToOrigin()
    pV4 = wtcMat.applyV4Point(Math.Vector4(p[0], p[1], p[2], 1))
    oV4 = wtcMat.applyV4Point(Math.Vector4(0, 0, 0, 1))
    pV3 = Math.Vector3(pV4[0], pV4[1], pV4[2]).scale(1 / pV4[3])
    oV3 = Math.Vector3(oV4[0], oV4[1], oV4[2]).scale(1 / oV4[3])
    return math.fabs(pV3[0] - oV3[0]) + math.fabs(pV3[1] - oV3[1])


