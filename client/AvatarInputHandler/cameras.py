# Source Generated with Decompyle++
# File: cameras.pyc (Python 2.6)

import BigWorld
import Math
import ResMgr
import math
import Settings
import weakref
import BattleReplay
from functools import partial
from debug_utils import *
from projectile_trajectory import getShotAngles
from gun_rotation_shared import calcPitchLimitsFromDesc

class ICamera:
    
    def create(self):
        pass

    
    def destroy(self):
        pass

    
    def enable(self, **args):
        pass

    
    def disable(self):
        pass

    
    def restoreDefaultsState(self):
        pass

    
    def getUserConfigValue(self, name):
        pass

    
    def setUserConfigValue(self, name, value):
        pass

    
    def update(self):
        pass

    
    def autoUpdate(self):
        pass



class ArcadeCamera:
    camera = property((lambda self: self._ArcadeCamera__cam))
    angles = property((lambda self: (self._ArcadeCamera__yaw, self._ArcadeCamera__pitch)))
    
    def __init__(self, dataSec):
        self._ArcadeCamera__readCfg(dataSec)
        self._ArcadeCamera__cam = BigWorld.CursorCamera()
        self._ArcadeCamera__camDist = 0
        self._ArcadeCamera__curSense = 0
        self._ArcadeCamera__curScrollSense = 0
        self._ArcadeCamera__pitch = 0
        self._ArcadeCamera__yaw = 0
        self._ArcadeCamera__cursorOffset = (0, 0)
        self._ArcadeCamera__postmortemMode = False
        self._ArcadeCamera__modelsToCollideWith = []
        self._ArcadeCamera__defaultPivotPos = Math.Vector3(0, 0, 0)
        self._ArcadeCamera__onChangeControlMode = None
        self._ArcadeCamera__autoUpdateCallbackId = None
        self._ArcadeCamera__cameraUpdateCallbackId = None

    
    def create(self, pivotPos, onChangeControlMode = None, postmortemMode = False):
        self._ArcadeCamera__onChangeControlMode = onChangeControlMode
        self._ArcadeCamera__postmortemMode = postmortemMode
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying:
            pass
        1
        vehicleID = BigWorld.player().playerVehicleID
        targetMat = BigWorld.entity(vehicleID).matrix
        self._ArcadeCamera__camDist = self._ArcadeCamera__cfg['startDist']
        self._ArcadeCamera__cam.pivotMaxDist = self._ArcadeCamera__camDist
        self._ArcadeCamera__cam.maxDistHalfLife = 0
        self._ArcadeCamera__cam.movementHalfLife = 0
        self._ArcadeCamera__cam.turningHalfLife = 0
        self._ArcadeCamera__cam.pivotPosition = pivotPos
        self._ArcadeCamera__defaultPivotPos = pivotPos
        self._ArcadeCamera__pitch = self._ArcadeCamera__cfg['startAngle']
        self._ArcadeCamera__yaw = Math.Matrix(targetMat).yaw
        matrix = Math.Matrix()
        matrix.setRotateYPR(self._ArcadeCamera__updateAngles(0, 0))
        self._ArcadeCamera__cam.source = matrix

    
    def destroy(self):
        self.disable()
        self._ArcadeCamera__onChangeControlMode = None
        self._ArcadeCamera__cam = None
        self._ArcadeCamera__writeUserPreferences()
        if self._ArcadeCamera__cameraUpdateCallbackId is not None:
            BigWorld.cancelCallback(self._ArcadeCamera__cameraUpdateCallbackId)
            self._ArcadeCamera__cameraUpdateCallbackId = None
        

    
    def addModelsToCollideWith(self, models):
        self._ArcadeCamera__modelsToCollideWith = self._ArcadeCamera__modelsToCollideWith + models
        if BigWorld.camera() == self._ArcadeCamera__cam:
            self._ArcadeCamera__cam.wg_setModelsToCollideWith(self._ArcadeCamera__modelsToCollideWith)
        

    
    def removeModelsToCollideWith(self, models):
        for model in models:
            if self._ArcadeCamera__modelsToCollideWith.count(model) > 0:
                self._ArcadeCamera__modelsToCollideWith.remove(model)
                continue
        
        if BigWorld.camera() == self._ArcadeCamera__cam:
            self._ArcadeCamera__cam.wg_setModelsToCollideWith(self._ArcadeCamera__modelsToCollideWith)
        

    
    def focusOnPos(self, preferredPos):
        self._ArcadeCamera__calcStartAngles(self._ArcadeCamera__cam.target, preferredPos)

    
    def enable(self, preferredPos = None, closesDist = False, postmortemParams = None):
        camSource = None
        camDist = None
        camTarget = BigWorld.player().getOwnVehicleMatrix()
        camTargetTransOnly = Math.WGTranslationOnlyMP()
        camTargetTransOnly.source = camTarget
        camTarget = camTargetTransOnly
        if not self._ArcadeCamera__postmortemMode:
            if preferredPos is not None:
                self._ArcadeCamera__calcStartAngles(camTarget, preferredPos)
            
            if closesDist:
                camDist = self._ArcadeCamera__cfg['distRange'][0]
            
        elif postmortemParams is not None:
            self._ArcadeCamera__yaw = postmortemParams[0][0]
            self._ArcadeCamera__pitch = postmortemParams[0][1]
            camDist = postmortemParams[1]
            camSource = Math.Matrix()
            camSource.setRotateYPR((self._ArcadeCamera__yaw, self._ArcadeCamera__pitch, 0))
        else:
            camDist = self._ArcadeCamera__cfg['distRange'][1]
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying:
            camTarget = BigWorld.entity(replayCtrl.playerVehicleID).matrix
            camDist = None
        
        if camDist is not None:
            self._ArcadeCamera__camDist = camDist
            self._ArcadeCamera__cam.pivotMaxDist = camDist
        
        if camSource is not None:
            self._ArcadeCamera__cam.source = camSource
        
        self._ArcadeCamera__cam.target = camTarget
        self._ArcadeCamera__cam.wg_setModelsToCollideWith(self._ArcadeCamera__modelsToCollideWith)
        BigWorld.camera(self._ArcadeCamera__cam)
        self._ArcadeCamera__cameraUpdate()

    
    def disable(self):
        self._ArcadeCamera__cam.wg_setModelsToCollideWith([])
        BigWorld.camera(None)
        if self._ArcadeCamera__autoUpdateCallbackId is not None:
            BigWorld.cancelCallback(self._ArcadeCamera__autoUpdateCallbackId)
            self._ArcadeCamera__autoUpdateCallbackId = None
        
        if self._ArcadeCamera__cameraUpdateCallbackId is not None:
            BigWorld.cancelCallback(self._ArcadeCamera__cameraUpdateCallbackId)
            self._ArcadeCamera__cameraUpdateCallbackId = None
        

    
    def update(self, dx, dy, dz, rotateMode = True, zoomMode = True):
        self._ArcadeCamera__curSense = self._ArcadeCamera__cfg['sensitivity']
        self._ArcadeCamera__curScrollSense = self._ArcadeCamera__cfg['scrollSensitivity']
        self._ArcadeCamera__update(dx, dy, dz, rotateMode, zoomMode, False)

    
    def autoUpdate(self, dx, dy, dz, rotateMode = True, zoomMode = True, onlyOnce = False):
        self._ArcadeCamera__curSense = self._ArcadeCamera__cfg['keySensitivity']
        self._ArcadeCamera__curScrollSense = self._ArcadeCamera__cfg['keySensitivity']
        if self._ArcadeCamera__autoUpdateCallbackId is not None:
            BigWorld.cancelCallback(self._ArcadeCamera__autoUpdateCallbackId)
            self._ArcadeCamera__autoUpdateCallbackId = None
        
        if onlyOnce:
            self._ArcadeCamera__update(dx, dy, dz, rotateMode, zoomMode, False)
        else:
            self._ArcadeCamera__autoUpdateCallbackId = BigWorld.callback(0.001, partial(self._ArcadeCamera__update, dx, dy, dz, rotateMode, zoomMode, True))

    
    def restoreDefaultsState(self):
        self._ArcadeCamera__camDist = self._ArcadeCamera__cfg['startDist']
        self._ArcadeCamera__cam.pivotMaxDist = self._ArcadeCamera__camDist
        self._ArcadeCamera__cam.maxDistHalfLife = 0.025
        self._ArcadeCamera__cam.movementHalfLife = 0
        self._ArcadeCamera__cam.turningHalfLife = 0.025
        self._ArcadeCamera__pitch = self._ArcadeCamera__cfg['startAngle']
        self._ArcadeCamera__yaw = Math.Matrix(self._ArcadeCamera__cam.target).yaw
        matrix = Math.Matrix()
        matrix.setRotateYPR(self._ArcadeCamera__updateAngles(0, 0))
        self._ArcadeCamera__cam.source = matrix

    
    def getUserConfigValue(self, name):
        return self._ArcadeCamera__userCfg.get(name)

    
    def setUserConfigValue(self, name, value):
        if name not in self._ArcadeCamera__userCfg:
            return None
        self._ArcadeCamera__userCfg[name] = value
        if name not in ('keySensitivity', 'sensitivity', 'scrollSensitivity'):
            self._ArcadeCamera__cfg[name] = self._ArcadeCamera__userCfg[name]
        else:
            self._ArcadeCamera__cfg[name] = self._ArcadeCamera__baseCfg[name] * self._ArcadeCamera__userCfg[name]

    
    def cursorOffset(self, offset):
        self._ArcadeCamera__cursorOffset = offset

    
    def setPivotPosition(self, position):
        self._ArcadeCamera__cam.pivotPosition = position
        self._ArcadeCamera__defaultPivotPos = position

    
    def getPivotPosition(self):
        return self._ArcadeCamera__defaultPivotPos

    
    def setCameraDistance(self, distance):
        distRange = self._ArcadeCamera__cfg['distRange']
        self._ArcadeCamera__camDist = distance
        self._ArcadeCamera__camDist = _clamp(distRange[0], distRange[1], self._ArcadeCamera__camDist)
        self._ArcadeCamera__cam.pivotMaxDist = self._ArcadeCamera__camDist

    
    def getCameraDistance(self):
        return self._ArcadeCamera__camDist

    
    def setYawPitch(self, yaw, pitch):
        anglesRange = self._ArcadeCamera__cfg['angleRange']
        self._ArcadeCamera__pitch = pitch
        self._ArcadeCamera__pitch = _clamp(anglesRange[0], anglesRange[1], self._ArcadeCamera__pitch)
        self._ArcadeCamera__yaw = yaw
        if self._ArcadeCamera__yaw > 2 * math.pi:
            self._ArcadeCamera__yaw -= 2 * math.pi
        elif self._ArcadeCamera__yaw < -2 * math.pi:
            self._ArcadeCamera__yaw += 2 * math.pi
        
        matrix = Math.Matrix()
        matrix.setRotateYPR((self._ArcadeCamera__yaw, self._ArcadeCamera__pitch, 0))
        self._ArcadeCamera__cam.source = matrix

    
    def getYawPitch(self):
        return (self._ArcadeCamera__yaw, self._ArcadeCamera__pitch)

    
    def _ArcadeCamera__calcStartAngles(self, targetMat, preferredPos):
        camDist = self._ArcadeCamera__camDist
        camPivotPos = self._ArcadeCamera__cam.pivotPosition
        posOnEntity = Math.Matrix(targetMat).applyPoint(Math.Vector3(0, camPivotPos[1], 0))
        yaw = (preferredPos - posOnEntity).yaw
        rotMat = Math.Matrix()
        rotMat.setRotateY(yaw)
        pivotPos = posOnEntity + rotMat.applyPoint(Math.Vector3(camPivotPos[0], 0, camPivotPos[2]))
        dir = preferredPos - pivotPos
        posDir = preferredPos - Math.Matrix(targetMat).applyToOrigin()
        pitch = -(posDir.pitch)
        
        try:
            pitch = self._ArcadeCamera__calcPitchAngle(camDist, dir)
            dist = self._ArcadeCamera__sceneCheck(yaw, pitch, pivotPos, camDist)
            if dist != 0:
                pitch = self._ArcadeCamera__calcPitchAngle(dist, dir)
        except:
            LOG_CURRENT_EXCEPTION()

        self._ArcadeCamera__pitch = pitch
        self._ArcadeCamera__yaw = yaw
        matrix = Math.Matrix()
        matrix.setRotateYPR(self._ArcadeCamera__updateAngles(0, 0))
        self._ArcadeCamera__cam.source = matrix

    
    def _ArcadeCamera__getRotateAngle(self, vec2f):
        fov = BigWorld.projection().fov
        near = BigWorld.projection().nearPlane
        yLength = near * math.tan(fov * 0.5)
        return math.atan2(yLength * vec2f[1], near)

    
    def _ArcadeCamera__sceneCheck(self, yaw, pitch, pivotPos, dist):
        dir = _vec3fFromYawPitch(yaw, -pitch)
        start = pivotPos - dir.scale(0.1)
        end = pivotPos - dir.scale(dist)
        colRes = BigWorld.wg_collideSegment(BigWorld.player().spaceID, start, end, 128)
        if colRes is not None:
            return Math.Vector3(colRes[0] - pivotPos).length
        return 0

    
    def _ArcadeCamera__calcPitchAngle(self, camDist, dir):
        alpha = self._ArcadeCamera__getRotateAngle(self._ArcadeCamera__cursorOffset)
        a = camDist
        b = dir.length
        A = 2 * a * math.cos(alpha)
        B = a * a - b * b
        D = A * A - 4 * B
        if D > 0:
            c1 = (A + math.sqrt(D)) * 0.5
            c2 = (A - math.sqrt(D)) * 0.5
            if c1 > c2:
                pass
            1
            c = c2
            beta = math.acos((a * a + b * b - c * c) / 2 * a * b)
            eta = math.pi - beta
            return -(dir.pitch) - eta
        return -(dir.pitch)

    
    def _ArcadeCamera__readCfg(self, dataSec):
        if dataSec is None:
            LOG_WARNING('Invalid section <arcadeMode/camera> in avatar_input_handler.xml')
        
        self._ArcadeCamera__baseCfg = dict()
        bcfg = self._ArcadeCamera__baseCfg
        bcfg['keySensitivity'] = readFloat(dataSec, 'keySensitivity', 0, 10, 0.01)
        bcfg['sensitivity'] = readFloat(dataSec, 'sensitivity', 0, 10, 0.01)
        bcfg['scrollSensitivity'] = readFloat(dataSec, 'scrollSensitivity', 0, 10, 0.01)
        bcfg['angleRange'] = readVec2(dataSec, 'angleRange', (0, 0), (180, 180), (10, 110))
        bcfg['distRange'] = readVec2(dataSec, 'distRange', (1, 1), (100, 100), (2, 20))
        bcfg['angleRange'][0] = math.radians(bcfg['angleRange'][0]) - math.pi * 0.5
        bcfg['angleRange'][1] = math.radians(bcfg['angleRange'][1]) - math.pi * 0.5
        ds = Settings.g_instance.userPrefs[Settings.KEY_CONTROL_MODE]
        if ds is not None:
            ds = ds['arcadeMode/camera']
        
        self._ArcadeCamera__userCfg = dict()
        ucfg = self._ArcadeCamera__userCfg
        ucfg['horzInvert'] = readBool(ds, 'horzInvert', False)
        ucfg['vertInvert'] = readBool(ds, 'vertInvert', False)
        ucfg['keySensitivity'] = readFloat(ds, 'keySensitivity', 0, 10, 1)
        ucfg['sensitivity'] = readFloat(ds, 'sensitivity', 0, 10, 1)
        ucfg['scrollSensitivity'] = readFloat(ds, 'scrollSensitivity', 0, 10, 1)
        ucfg['startDist'] = readFloat(ds, 'startDist', 2, 500, 10)
        ucfg['startAngle'] = readFloat(ds, 'startAngle', 5, 180, 60)
        ucfg['startAngle'] = math.radians(ucfg['startAngle']) - math.pi * 0.5
        self._ArcadeCamera__cfg = dict()
        cfg = self._ArcadeCamera__cfg
        cfg['keySensitivity'] = bcfg['keySensitivity']
        cfg['sensitivity'] = bcfg['sensitivity']
        cfg['scrollSensitivity'] = bcfg['scrollSensitivity']
        cfg['angleRange'] = bcfg['angleRange']
        cfg['distRange'] = bcfg['distRange']
        cfg['horzInvert'] = ucfg['horzInvert']
        cfg['vertInvert'] = ucfg['vertInvert']
        cfg['keySensitivity'] *= ucfg['keySensitivity']
        cfg['sensitivity'] *= ucfg['sensitivity']
        cfg['scrollSensitivity'] *= ucfg['scrollSensitivity']
        cfg['startDist'] = ucfg['startDist']
        cfg['startAngle'] = ucfg['startAngle']

    
    def _ArcadeCamera__writeUserPreferences(self):
        ds = Settings.g_instance.userPrefs
        if not ds.has_key(Settings.KEY_CONTROL_MODE):
            ds.write(Settings.KEY_CONTROL_MODE, '')
        
        ucfg = self._ArcadeCamera__userCfg
        ds = ds[Settings.KEY_CONTROL_MODE]
        ds.writeBool('arcadeMode/camera/horzInvert', ucfg['horzInvert'])
        ds.writeBool('arcadeMode/camera/vertInvert', ucfg['vertInvert'])
        ds.writeFloat('arcadeMode/camera/keySensitivity', ucfg['keySensitivity'])
        ds.writeFloat('arcadeMode/camera/sensitivity', ucfg['sensitivity'])
        ds.writeFloat('arcadeMode/camera/scrollSensitivity', ucfg['scrollSensitivity'])
        ds.writeFloat('arcadeMode/camera/startDist', ucfg['startDist'])
        ucfg['startAngle'] = math.degrees(ucfg['startAngle'] + math.pi * 0.5)
        ds.writeFloat('arcadeMode/camera/startAngle', ucfg['startAngle'])

    
    def calcYawPitchDelta(self, dx, dy):
        if self._ArcadeCamera__cfg['horzInvert']:
            pass
        1
        if self._ArcadeCamera__cfg['vertInvert']:
            pass
        1
        return (dy * self._ArcadeCamera__curSense, -1 * 1)

    
    def _ArcadeCamera__updateAngles(self, dx, dy):
        cfg = self._ArcadeCamera__cfg
        anglesRange = cfg['angleRange']
        offset = 0
        (yawDelta, pitchDelta) = self.calcYawPitchDelta(dx, dy)
        self._ArcadeCamera__pitch -= pitchDelta
        self._ArcadeCamera__pitch = _clamp(anglesRange[0] + offset, anglesRange[1] + offset, self._ArcadeCamera__pitch)
        self._ArcadeCamera__yaw += yawDelta
        if self._ArcadeCamera__yaw > 2 * math.pi:
            self._ArcadeCamera__yaw -= 2 * math.pi
        elif self._ArcadeCamera__yaw < -2 * math.pi:
            self._ArcadeCamera__yaw += 2 * math.pi
        
        return (self._ArcadeCamera__yaw, self._ArcadeCamera__pitch, 0)

    
    def _ArcadeCamera__update(self, dx, dy, dz, rotateMode = True, zoomMode = True, isCallback = False):
        if isCallback:
            self._ArcadeCamera__autoUpdateCallbackId = BigWorld.callback(0.001, partial(self._ArcadeCamera__update, dx, dy, dz, rotateMode, zoomMode, True))
        
        cfg = self._ArcadeCamera__cfg
        if zoomMode and dz != 0:
            distRange = cfg['distRange']
            prevCam = self._ArcadeCamera__camDist
            self._ArcadeCamera__camDist -= dz * float(self._ArcadeCamera__curScrollSense)
            self._ArcadeCamera__camDist = _clamp(distRange[0], distRange[1], self._ArcadeCamera__camDist)
            self._ArcadeCamera__userCfg['startDist'] = self._ArcadeCamera__camDist
            if prevCam == self._ArcadeCamera__camDist and self._ArcadeCamera__onChangeControlMode is not None:
                if _almostZero(self._ArcadeCamera__camDist - distRange[0]):
                    self._ArcadeCamera__onChangeControlMode()
                
            
            self._ArcadeCamera__cam.pivotMaxDist = self._ArcadeCamera__camDist
        
        if rotateMode:
            matrix = Math.Matrix()
            matrix.setRotateYPR(self._ArcadeCamera__updateAngles(dx, dy))
            self._ArcadeCamera__cam.source = matrix
        

    
    def _ArcadeCamera__cameraUpdate(self):
        self._ArcadeCamera__cameraUpdateCallbackId = BigWorld.callback(0, self._ArcadeCamera__cameraUpdate)
        if self._ArcadeCamera__cam.target is None:
            self._ArcadeCamera__cam.pivotPosition = self._ArcadeCamera__defaultPivotPos
            return None
        targetPosition = Math.Matrix(self._ArcadeCamera__cam.target).translation
        BOTTOM_SHIFT = Math.Vector3(0, 1, 0)
        collData = BigWorld.wg_collideSegment(BigWorld.player().spaceID, targetPosition + BOTTOM_SHIFT, targetPosition + Math.Vector3(0, self._ArcadeCamera__defaultPivotPos.y, 0), 7)
        if collData is not None:
            collPoint = collData[0]
            self._ArcadeCamera__cam.pivotPosition = collPoint - Math.Vector3(0, 0.3, 0) - targetPosition
        else:
            self._ArcadeCamera__cam.pivotPosition = self._ArcadeCamera__defaultPivotPos



class StrategicCamera:
    camera = property((lambda self: self._StrategicCamera__cam))
    
    def __init__(self, dataSec):
        self._StrategicCamera__readCfg(dataSec)
        self._StrategicCamera__cam = BigWorld.CursorCamera()
        self._StrategicCamera__requiredHeight = 0
        self._StrategicCamera__totalMove = Math.Vector3(0, 0, 0)
        self._StrategicCamera__yaw = 0
        self._StrategicCamera__curSense = 0
        self._StrategicCamera__autoUpdateCallbackId = None
        self._StrategicCamera__onChangeControlMode = None

    
    def create(self, onChangeControlMode = None):
        self._StrategicCamera__onChangeControlMode = onChangeControlMode
        self._StrategicCamera__camDist = self._StrategicCamera__cfg['camDist']
        self._StrategicCamera__cam.pivotMaxDist = 0
        self._StrategicCamera__cam.maxDistHalfLife = 0.01
        self._StrategicCamera__cam.movementHalfLife = 0
        self._StrategicCamera__cam.turningHalfLife = 0.01
        self._StrategicCamera__cam.pivotPosition = Math.Vector3(0, self._StrategicCamera__camDist, 0)

    
    def destroy(self):
        self.disable()
        self._StrategicCamera__onChangeControlMode = None
        self._StrategicCamera__cam = None
        self._StrategicCamera__writeUserPreferences()

    
    def enable(self, targetPos, saveDist):
        vPos = BigWorld.player().getOwnVehiclePosition()
        dir = targetPos - vPos
        srcMat = Math.Matrix()
        srcMat.setRotateYPR((0, -(math.pi) * 0.499, 0))
        self._StrategicCamera__yaw = dir.yaw
        if not saveDist:
            self._StrategicCamera__camDist = self._StrategicCamera__cfg['camDist']
        
        self._StrategicCamera__totalMove = Math.Vector3(targetPos[0], 0, targetPos[2])
        self._StrategicCamera__cam.pivotPosition = Math.Vector3(0, targetPos[1] + self._StrategicCamera__camDist, 0)
        self._StrategicCamera__update(0, 0, 0, False)
        trgMat = Math.Matrix()
        trgMat.setTranslate(self._StrategicCamera__totalMove)
        self._StrategicCamera__cam.source = srcMat
        self._StrategicCamera__cam.target = trgMat
        BigWorld.camera(self._StrategicCamera__cam)
        BigWorld.player().positionControl.moveTo(self._StrategicCamera__totalMove)
        BigWorld.player().positionControl.followCamera(True)
        self._StrategicCamera__cam.sptHiding = False

    
    def disable(self):
        BigWorld.camera(None)
        BigWorld.player().positionControl.followCamera(False)
        if self._StrategicCamera__autoUpdateCallbackId is not None:
            BigWorld.cancelCallback(self._StrategicCamera__autoUpdateCallbackId)
            self._StrategicCamera__autoUpdateCallbackId = None
        
        self._StrategicCamera__cam.sptHiding = True

    
    def teleport(self, pos):
        self.moveToPosition(pos)

    
    def restoreDefaultsState(self):
        vPos = BigWorld.player().getOwnVehiclePosition()
        self._StrategicCamera__totalMove = Math.Vector3(vPos[0], 0, vPos[2])
        self._StrategicCamera__camDist = self._StrategicCamera__cfg['camDist']
        self._StrategicCamera__cam.pivotMaxDist = 0
        self._StrategicCamera__cam.maxDistHalfLife = 0.01
        self._StrategicCamera__cam.movementHalfLife = 0
        self._StrategicCamera__cam.turningHalfLife = 0.01
        self._StrategicCamera__cam.pivotPosition = Math.Vector3(0, vPos[1] + self._StrategicCamera__camDist, 0)
        trgMat = Math.Matrix()
        trgMat.setTranslate(self._StrategicCamera__totalMove)
        self._StrategicCamera__cam.target = trgMat
        BigWorld.player().positionControl.moveTo(self._StrategicCamera__totalMove)

    
    def getUserConfigValue(self, name):
        return self._StrategicCamera__userCfg.get(name)

    
    def setUserConfigValue(self, name, value):
        if name not in self._StrategicCamera__userCfg:
            return None
        self._StrategicCamera__userCfg[name] = value
        if name not in ('keySensitivity', 'sensitivity', 'scrollSensitivity'):
            self._StrategicCamera__cfg[name] = self._StrategicCamera__userCfg[name]
        else:
            self._StrategicCamera__cfg[name] = self._StrategicCamera__baseCfg[name] * self._StrategicCamera__userCfg[name]

    
    def update(self, dx, dy, dz):
        self._StrategicCamera__curSense = self._StrategicCamera__cfg['sensitivity']
        self._StrategicCamera__update(dx, dy, dz, False)

    
    def autoUpdate(self, dx, dy, dz, onlyOnce):
        self._StrategicCamera__curSense = self._StrategicCamera__cfg['keySensitivity']
        if self._StrategicCamera__autoUpdateCallbackId is not None:
            BigWorld.cancelCallback(self._StrategicCamera__autoUpdateCallbackId)
            self._StrategicCamera__autoUpdateCallbackId = None
        
        if onlyOnce:
            self._StrategicCamera__update(dx, dy, dz, False)
        else:
            self._StrategicCamera__autoUpdateCallbackId = BigWorld.callback(0.001, partial(self._StrategicCamera__update, dx, dy, dz, True))

    
    def moveToPosition(self, pos):
        self._StrategicCamera__totalMove = pos
        self.update(0, 0, 0)

    
    def _StrategicCamera__readCfg(self, dataSec):
        if not dataSec:
            LOG_WARNING('Invalid section <strategicMode/camera> in avatar_input_handler.xml')
        
        self._StrategicCamera__baseCfg = dict()
        bcfg = self._StrategicCamera__baseCfg
        bcfg['keySensitivity'] = readFloat(dataSec, 'keySensitivity', 0.005, 10, 0.025)
        bcfg['sensitivity'] = readFloat(dataSec, 'sensitivity', 0.005, 10, 0.025)
        bcfg['scrollSensitivity'] = readFloat(dataSec, 'scrollSensitivity', 0.005, 10, 0.025)
        bcfg['distRange'] = readVec2(dataSec, 'distRange', (1, 1), (100, 100), (2, 30))
        ds = Settings.g_instance.userPrefs[Settings.KEY_CONTROL_MODE]
        if ds is not None:
            ds = ds['strategicMode/camera']
        
        self._StrategicCamera__userCfg = dict()
        ucfg = self._StrategicCamera__userCfg
        ucfg['horzInvert'] = readBool(ds, 'horzInvert', False)
        ucfg['vertInvert'] = readBool(ds, 'vertInvert', False)
        ucfg['keySensitivity'] = readFloat(ds, 'keySensitivity', 0, 10, 1)
        ucfg['sensitivity'] = readFloat(ds, 'sensitivity', 0, 10, 1)
        ucfg['scrollSensitivity'] = readFloat(ds, 'scrollSensitivity', 0, 10, 1)
        ucfg['camDist'] = readFloat(ds, 'camDist', 40, 100, bcfg['distRange'][0])
        self._StrategicCamera__cfg = dict()
        cfg = self._StrategicCamera__cfg
        cfg['keySensitivity'] = bcfg['keySensitivity']
        cfg['sensitivity'] = bcfg['sensitivity']
        cfg['scrollSensitivity'] = bcfg['scrollSensitivity']
        cfg['distRange'] = bcfg['distRange']
        cfg['camDist'] = ucfg['camDist']
        cfg['keySensitivity'] *= ucfg['keySensitivity']
        cfg['sensitivity'] *= ucfg['sensitivity']
        cfg['scrollSensitivity'] *= ucfg['scrollSensitivity']
        cfg['horzInvert'] = ucfg['horzInvert']
        cfg['vertInvert'] = ucfg['vertInvert']

    
    def _StrategicCamera__writeUserPreferences(self):
        ds = Settings.g_instance.userPrefs
        if not ds.has_key(Settings.KEY_CONTROL_MODE):
            ds.write(Settings.KEY_CONTROL_MODE, '')
        
        ucfg = self._StrategicCamera__userCfg
        ds = ds[Settings.KEY_CONTROL_MODE]
        ds.writeFloat('strategicMode/camera/keySensitivity', ucfg['keySensitivity'])
        ds.writeFloat('strategicMode/camera/sensitivity', ucfg['sensitivity'])
        ds.writeFloat('strategicMode/camera/scrollSensitivity', ucfg['scrollSensitivity'])
        ds.writeFloat('strategicMode/camera/camDist', self._StrategicCamera__cfg['camDist'])

    
    def _StrategicCamera__updateDir(self, dx):
        delta = math.radians(dx * float(self._StrategicCamera__curSense))
        self._StrategicCamera__yaw += delta
        if self._StrategicCamera__yaw < 0:
            self._StrategicCamera__yaw = math.pi * 2 + self._StrategicCamera__yaw
        elif self._StrategicCamera__yaw > 2 * math.pi:
            self._StrategicCamera__yaw = 0
        
        rotMat = Math.Matrix()
        rotMat.setRotateY(self._StrategicCamera__yaw)
        return rotMat.applyVector(Math.Vector3(0, 0, 1))

    
    def _StrategicCamera__move(self, dx, dy):
        move_z = -dy * self._StrategicCamera__curSense
        move_x = dx * self._StrategicCamera__curSense
        dir = Math.Vector3(move_x, 0, move_z)
        matrix = Math.Matrix()
        matrix.setRotateY(Math.Matrix(self._StrategicCamera__cam.invViewMatrix).yaw)
        dir = matrix.applyVector(dir)
        length = dir.length
        dir.normalise()
        dir = dir.scale(length)
        destPos = self._StrategicCamera__totalMove + dir
        bb = BigWorld.player().arena.arenaType.boundingBox
        pos2D = _clampPoint2DInBox2D(bb[0], bb[1], Math.Vector2(destPos[0], destPos[2]))
        self._StrategicCamera__totalMove[0] = pos2D[0]
        self._StrategicCamera__totalMove[2] = pos2D[1]
        collPoint = BigWorld.wg_collideSegment(BigWorld.player().spaceID, self._StrategicCamera__totalMove + Math.Vector3(0, 1000, 0), self._StrategicCamera__totalMove + Math.Vector3(0, -250, 0), 3)
        if collPoint is not None:
            self._StrategicCamera__requiredHeight = collPoint[0][1]
        else:
            self._StrategicCamera__requiredHeight = 0
        matrix.setTranslate(self._StrategicCamera__totalMove)
        self._StrategicCamera__cam.target = matrix

    
    def _StrategicCamera__update(self, dx, dy, dz, isCallback = False):
        if isCallback:
            self._StrategicCamera__autoUpdateCallbackId = BigWorld.callback(0.001, partial(self._StrategicCamera__update, dx, dy, dz, True))
        
        self._StrategicCamera__move(dx, dy)
        distRange = self._StrategicCamera__cfg['distRange']
        self._StrategicCamera__camDist -= dz * float(self._StrategicCamera__curSense)
        self._StrategicCamera__camDist = _clamp(distRange[0], distRange[1], self._StrategicCamera__camDist)
        self._StrategicCamera__cfg['camDist'] = self._StrategicCamera__camDist
        self._StrategicCamera__cam.pivotPosition = Math.Vector3(0, self._StrategicCamera__camDist + self._StrategicCamera__requiredHeight, 0)
        if dz != 0 and self._StrategicCamera__onChangeControlMode is not None:
            if _almostZero(self._StrategicCamera__camDist - distRange[0]):
                self._StrategicCamera__onChangeControlMode()
            
        



class SniperCamera:
    _USE_SWINGING = True
    _USE_ALIGN_TO_VEHICLE = True
    camera = property((lambda self: self._SniperCamera__cam))
    
    def __init__(self, dataSec):
        self._SniperCamera__readCfg(dataSec)
        self._SniperCamera__cam = BigWorld.FreeCamera()
        self._SniperCamera__angles = [
            0,
            0]
        self._SniperCamera__dxdydz = [
            0,
            0,
            0]
        self._SniperCamera__zoom = self._SniperCamera__cfg['zoom']
        self._SniperCamera__fov = BigWorld.projection().fov
        self._SniperCamera__curSense = 0
        self._SniperCamera__curScrollSense = 0
        self._SniperCamera__autoUpdate = False
        self._SniperCamera__autoUpdateCallbackId = None
        self._SniperCamera__waitVehicleCallbackId = None
        self._SniperCamera__onChangeControlMode = None
        self._SniperCamera__pitchCompensation = 0
        self._SniperCamera__pitchCompensationTimestamp = BigWorld.time()

    
    def create(self, onChangeControlMode = None):
        self._SniperCamera__onChangeControlMode = onChangeControlMode

    
    def destroy(self):
        self.disable()
        self._SniperCamera__onChangeControlMode = None
        self._SniperCamera__cam = None
        self._SniperCamera__writeUserPreferences()

    
    def enable(self, targetPos, saveZoom):
        player = BigWorld.player()
        if not saveZoom:
            self._SniperCamera__zoom = self._SniperCamera__cfg['zoom']
        
        self._SniperCamera__fov = BigWorld.projection().fov
        self._SniperCamera__dxdydz = [
            0,
            0,
            0]
        self._SniperCamera__applyFOV(self._SniperCamera__fov / self._SniperCamera__zoom)
        self._SniperCamera__setupCamera(targetPos)
        vehicle = BigWorld.entity(player.playerVehicleID)
        if vehicle is None:
            self._SniperCamera__whiteVehicleCallbackId = BigWorld.callback(0.1, self._SniperCamera__waitVehicle)
        else:
            self._SniperCamera__showVehicle(False)
        BigWorld.camera(self._SniperCamera__cam)
        self._SniperCamera__cameraUpdate()

    
    def disable(self):
        BigWorld.camera(None)
        if self._SniperCamera__autoUpdateCallbackId is not None:
            BigWorld.cancelCallback(self._SniperCamera__autoUpdateCallbackId)
            self._SniperCamera__autoUpdateCallbackId = None
        
        if self._SniperCamera__waitVehicleCallbackId is not None:
            BigWorld.cancelCallback(self._SniperCamera__waitVehicleCallbackId)
            self._SniperCamera__waitVehicleCallbackId = None
        
        self._SniperCamera__applyFOV(self._SniperCamera__fov)
        self._SniperCamera__showVehicle(True)

    
    def getUserConfigValue(self, name):
        return self._SniperCamera__userCfg.get(name)

    
    def setUserConfigValue(self, name, value):
        if name not in self._SniperCamera__userCfg:
            return None
        self._SniperCamera__userCfg[name] = value
        if name not in ('keySensitivity', 'sensitivity', 'scrollSensitivity'):
            self._SniperCamera__cfg[name] = self._SniperCamera__userCfg[name]
        else:
            self._SniperCamera__cfg[name] = self._SniperCamera__baseCfg[name] * self._SniperCamera__userCfg[name]

    
    def update(self, dx, dy, dz, autoUpdate = False):
        if autoUpdate:
            pass
        1
        self._SniperCamera__curSense = self._SniperCamera__cfg['sensitivity']
        if autoUpdate:
            pass
        1
        self._SniperCamera__curScrollSense = self._SniperCamera__cfg['scrollSensitivity']
        self._SniperCamera__curSense *= 1 / self._SniperCamera__zoom
        self._SniperCamera__dxdydz = [
            dx,
            dy,
            dz]
        self._SniperCamera__autoUpdate = autoUpdate

    
    def onRecreateDevice(self):
        curFov = BigWorld.projection().fov
        if curFov != self._SniperCamera__fov and curFov != self._SniperCamera__fov / self._SniperCamera__zoom:
            self._SniperCamera__fov = BigWorld.projection().fov
            self._SniperCamera__applyFOV(self._SniperCamera__fov / self._SniperCamera__zoom)
        

    
    def _SniperCamera__showVehicle(self, show):
        vehicle = BigWorld.entity(BigWorld.player().playerVehicleID)
        if vehicle is not None and vehicle.isStarted:
            va = vehicle.appearance
            va.changeVisibility('chassis', show, True)
            va.changeVisibility('hull', show, True)
            va.changeVisibility('turret', show, True)
            va.changeVisibility('gun', show, True)
            va.showStickers(show)
        

    
    def _SniperCamera__setupCamera(self, targetPos):
        player = BigWorld.player()
        desc = player.vehicleTypeDescriptor
        angles = self._SniperCamera__angles
        self._SniperCamera__yawLimits = desc.turret['yawLimits']
        (angles[0], angles[1]) = getShotAngles(desc, player.getOwnVehicleMatrix(), (0, 0), targetPos, False)
        self._SniperCamera__pitchLimits = calcPitchLimitsFromDesc(angles[0], desc.gun['pitchLimits'])
        gunOffs = desc.turret['gunPosition']
        self._SniperCamera__gunOffsetMat = Math.Matrix()
        self._SniperCamera__gunOffsetMat.setTranslate(gunOffs)
        calc = True
        if self._USE_SWINGING:
            vehicle = BigWorld.entity(player.playerVehicleID)
            if vehicle is not None and vehicle.isStarted:
                self._SniperCamera__turretJointMat = vehicle.appearance.modelsDesc['hull']['model'].node('HP_turretJoint')
                self._SniperCamera__chassisMat = vehicle.matrix
                calc = False
            
        
        if calc:
            turretOffs = desc.chassis['hullPosition'] + desc.hull['turretPositions'][0]
            turretOffsetMat = Math.Matrix()
            turretOffsetMat.setTranslate(turretOffs)
            self._SniperCamera__turretJointMat = Math.MatrixProduct()
            self._SniperCamera__turretJointMat.a = turretOffsetMat
            self._SniperCamera__turretJointMat.b = player.getOwnVehicleMatrix()
            self._SniperCamera__chassisMat = player.getOwnVehicleMatrix()
        
        invGunJointMat = Math.Matrix()
        invGunJointMat.set(self._SniperCamera__gunOffsetMat)
        invGunJointMat.postMultiply(self._SniperCamera__turretJointMat)
        invGunJointMat.invert()
        invTurretJointMat = Math.Matrix(self._SniperCamera__turretJointMat)
        invTurretJointMat.invert()
        gunYawRotateMat = Math.Matrix()
        gunYawRotateMat.setRotateY(angles[0])
        camPosMat = Math.Matrix()
        camPosMat.set(self._SniperCamera__gunOffsetMat)
        camPosMat.postMultiply(gunYawRotateMat)
        camPosMat.postMultiply(self._SniperCamera__turretJointMat)
        camDir = targetPos - camPosMat.applyToOrigin()
        angles[0] = invTurretJointMat.applyVector(camDir).yaw
        angles[1] = invGunJointMat.applyVector(camDir).pitch
        camMat = Math.Matrix()
        if self._USE_ALIGN_TO_VEHICLE:
            up = camPosMat.applyToAxis(1)
        else:
            up = Math.Vector3(0, 1, 0)
        camMat.lookAt(camPosMat.applyToOrigin(), camDir, up)
        self._SniperCamera__cam.set(camMat)

    
    def _SniperCamera__waitVehicle(self):
        vehicle = BigWorld.entity(BigWorld.player().playerVehicleID)
        if vehicle is not None and vehicle.isStarted:
            self._SniperCamera__waitVehicleCallbackId = None
        else:
            self._SniperCamera__waitVehicleCallbackId = BigWorld.callback(0.1, self._SniperCamera__waitVehicle)
            return None
        if vehicle.isStarted._USE_SWINGING:
            self._SniperCamera__turretJointMat = vehicle.appearance.modelsDesc['hull']['model'].node('HP_turretJoint')
            self._SniperCamera__chassisMat = vehicle.matrix
        
        self._SniperCamera__showVehicle(False)

    
    def _SniperCamera__rotate(self, dx, dy):
        cfg = self._SniperCamera__cfg
        angles = self._SniperCamera__angles
        if cfg['horzInvert']:
            pass
        1
        dx * self._SniperCamera__curSense += -1 * 1
        if cfg['vertInvert']:
            pass
        1
        dy * self._SniperCamera__curSense += -1 * 1
        if self._SniperCamera__yawLimits is not None:
            angles[0] = _clamp(self._SniperCamera__yawLimits[0], self._SniperCamera__yawLimits[1], angles[0])
        
        desc = BigWorld.player().vehicleTypeDescriptor
        self._SniperCamera__pitchLimits = calcPitchLimitsFromDesc(angles[0], desc.gun['pitchLimits'])
        chassisMatInv = Math.Matrix(self._SniperCamera__chassisMat)
        chassisMatInv.invert()
        turretJointMat = Math.Matrix(self._SniperCamera__turretJointMat)
        turretJointMat.postMultiply(chassisMatInv)
        pitchDelta = abs(turretJointMat.pitch)
        dTime = min(2, BigWorld.time() - self._SniperCamera__pitchCompensationTimestamp)
        self._SniperCamera__pitchCompensation = (dTime * pitchDelta + (2 - dTime) * self._SniperCamera__pitchCompensation) * 0.5
        self._SniperCamera__pitchCompensationTimestamp = BigWorld.time()
        pitchLimitsMin = self._SniperCamera__pitchLimits[0] - self._SniperCamera__pitchCompensation
        pitchLimitsMax = self._SniperCamera__pitchLimits[1] + self._SniperCamera__pitchCompensation
        angles[1] = _clamp(pitchLimitsMin, pitchLimitsMax, angles[1])

    
    def _SniperCamera__applyFOV(self, fov):
        BigWorld.projection().fov = fov

    
    def _SniperCamera__setupZoom(self, dz):
        if dz == 0:
            return None
        zooms = self._SniperCamera__cfg['zooms']
        prevZoom = self._SniperCamera__zoom
        if self._SniperCamera__zoom == zooms[0] and dz < 0 and self._SniperCamera__onChangeControlMode is not None:
            self._SniperCamera__onChangeControlMode()
        
        if dz > 0:
            for elem in zooms:
                if self._SniperCamera__zoom < elem:
                    self._SniperCamera__zoom = elem
                    self._SniperCamera__cfg['zoom'] = self._SniperCamera__zoom
                    break
                    continue
                dz == 0
            
        elif dz < 0:
            for i in range(len(zooms) - 1, -1, -1):
                if self._SniperCamera__zoom > zooms[i]:
                    self._SniperCamera__zoom = zooms[i]
                    self._SniperCamera__cfg['zoom'] = self._SniperCamera__zoom
                    break
                    continue
            
        
        if prevZoom != self._SniperCamera__zoom:
            self._SniperCamera__applyFOV(self._SniperCamera__fov / self._SniperCamera__zoom)
        

    
    def _SniperCamera__cameraUpdate(self):
        self._SniperCamera__autoUpdateCallbackId = BigWorld.callback(0, self._SniperCamera__cameraUpdate)
        ownVehicle = BigWorld.entity(BigWorld.player().playerVehicleID)
        if ownVehicle is not None and ownVehicle.isStarted and ownVehicle.appearance.isUnderwater():
            self._SniperCamera__onChangeControlMode()
            return None
        self._SniperCamera__setupZoom(self._SniperCamera__dxdydz[2])
        self._SniperCamera__rotate(self._SniperCamera__dxdydz[0], self._SniperCamera__dxdydz[1])
        yawRotateMat = Math.Matrix()
        yawRotateMat.setRotateY(self._SniperCamera__angles[0])
        pitchRotateMat = Math.Matrix()
        pitchRotateMat.setRotateX(self._SniperCamera__angles[1])
        camMat = Math.Matrix()
        camMat.set(pitchRotateMat)
        camMat.postMultiply(self._SniperCamera__gunOffsetMat)
        camMat.postMultiply(yawRotateMat)
        camMat.postMultiply(self._SniperCamera__turretJointMat)
        if not self._USE_ALIGN_TO_VEHICLE:
            pos = camMat.applyToOrigin()
            dir = camMat.applyToAxis(2)
            camMat.lookAt(pos, dir, (0, 1, 0))
        else:
            camMat.invert()
        self._SniperCamera__cam.set(camMat)
        if not self._SniperCamera__autoUpdate:
            self._SniperCamera__dxdydz = [
                0,
                0,
                0]
        

    
    def _SniperCamera__readCfg(self, dataSec):
        if not dataSec:
            LOG_WARNING('Invalid section <sniperMode/camera> in avatar_input_handler.xml')
        
        self._SniperCamera__baseCfg = dict()
        bcfg = self._SniperCamera__baseCfg
        bcfg['keySensitivity'] = readFloat(dataSec, 'keySensitivity', 0, 10, 0.005)
        bcfg['sensitivity'] = readFloat(dataSec, 'sensitivity', 0, 10, 0.005)
        bcfg['scrollSensitivity'] = readFloat(dataSec, 'scrollSensitivity', 0, 10, 0.005)
        zooms = readVec3(dataSec, 'zooms', (0, 0, 0), (10, 10, 10), (2, 4, 8))
        bcfg['zooms'] = [
            zooms.x,
            zooms.y,
            zooms.z]
        ds = Settings.g_instance.userPrefs[Settings.KEY_CONTROL_MODE]
        if ds is not None:
            ds = ds['sniperMode/camera']
        
        self._SniperCamera__userCfg = dict()
        ucfg = self._SniperCamera__userCfg
        ucfg['horzInvert'] = readBool(ds, 'horzInvert', False)
        ucfg['vertInvert'] = readBool(ds, 'vertInvert', False)
        ucfg['keySensitivity'] = readFloat(ds, 'keySensitivity', 0, 10, 1)
        ucfg['sensitivity'] = readFloat(ds, 'sensitivity', 0, 10, 1)
        ucfg['scrollSensitivity'] = readFloat(ds, 'scrollSensitivity', 0, 10, 1)
        ucfg['zoom'] = readFloat(ds, 'zoom', 0, 10, bcfg['zooms'][0])
        self._SniperCamera__cfg = dict()
        cfg = self._SniperCamera__cfg
        cfg['keySensitivity'] = bcfg['keySensitivity']
        cfg['sensitivity'] = bcfg['sensitivity']
        cfg['scrollSensitivity'] = bcfg['scrollSensitivity']
        cfg['zooms'] = bcfg['zooms']
        cfg['keySensitivity'] *= ucfg['keySensitivity']
        cfg['sensitivity'] *= ucfg['sensitivity']
        cfg['scrollSensitivity'] *= ucfg['scrollSensitivity']
        cfg['horzInvert'] = ucfg['horzInvert']
        cfg['vertInvert'] = ucfg['vertInvert']
        cfg['zoom'] = ucfg['zoom']

    
    def _SniperCamera__writeUserPreferences(self):
        ds = Settings.g_instance.userPrefs
        if not ds.has_key(Settings.KEY_CONTROL_MODE):
            ds.write(Settings.KEY_CONTROL_MODE, '')
        
        ucfg = self._SniperCamera__userCfg
        ds = ds[Settings.KEY_CONTROL_MODE]
        ds.writeBool('sniperMode/camera/horzInvert', ucfg['horzInvert'])
        ds.writeBool('sniperMode/camera/vertInvert', ucfg['vertInvert'])
        ds.writeFloat('sniperMode/camera/keySensitivity', ucfg['keySensitivity'])
        ds.writeFloat('sniperMode/camera/sensitivity', ucfg['sensitivity'])
        ds.writeFloat('sniperMode/camera/scrollSensitivity', ucfg['scrollSensitivity'])
        ds.writeFloat('sniperMode/camera/zoom', self._SniperCamera__cfg['zoom'])



class FreeCamera:
    camera = property((lambda self: self._FreeCamera__cam))
    
    def __init__(self):
        self._FreeCamera__cam = BigWorld.FreeCamera()

    
    def create(self):
        pass

    
    def destroy(self):
        self._FreeCamera__cam = None

    
    def enable(self, camMat = None):
        if camMat is not None:
            self._FreeCamera__cam.set(camMat)
        
        BigWorld.camera(self._FreeCamera__cam)

    
    def disable(self):
        BigWorld.camera(None)

    
    def setWorldMatrix(self, matrix):
        matrix = Math.Matrix(matrix)
        matrix.invert()
        self._FreeCamera__cam.set(matrix)

    
    def getWorldMatrix(self):
        return Math.Matrix(self._FreeCamera__cam.invViewMatrix)

    
    def handleKey(self, event):
        return self._FreeCamera__cam.handleKeyEvent(event)

    
    def handleMouse(self, dx, dy, dz):
        return self._FreeCamera__cam.handleMouseEvent(BigWorld.MouseEvent(dx, dy, dz, (0, 0)))



def readBool(dataSec, name, defaultVal):
    if dataSec is None:
        return defaultVal
    return dataSec.readBool(name, defaultVal)


def readFloat(dataSec, name, minVal, maxVal, defaultVal):
    if dataSec is None:
        return defaultVal
    value = dataSec.readFloat(name, defaultVal)
    value = _clamp(minVal, maxVal, value)
    return value


def readVec2(dataSec, name, minVal, maxVal, defaultVal):
    if dataSec is None:
        return Math.Vector2(defaultVal)
    value = dataSec.readVector2(name, Math.Vector2(defaultVal))
    for i in xrange(2):
        value[i] = _clamp(minVal[i], maxVal[i], value[i])
    
    return value


def readVec3(dataSec, name, minVal, maxVal, defaultVal):
    if dataSec is None:
        return Math.Vector3(defaultVal)
    value = dataSec.readVector3(name, Math.Vector3(defaultVal))
    for i in xrange(3):
        value[i] = _clamp(minVal[i], maxVal[i], value[i])
    
    return value


def getScreenAspectRatio():
    if BigWorld.isVideoWindowed():
        size = BigWorld.screenSize()
        return size[0] / size[1]
    return BigWorld.getFullScreenAspectRatio()


def getWorldRayAndPoint(x, y):
    fov = BigWorld.projection().fov
    near = BigWorld.projection().nearPlane
    aspect = getScreenAspectRatio()
    yLength = near * math.tan(fov * 0.5)
    xLength = yLength * aspect
    point = Math.Vector3(xLength * x, yLength * y, near)
    inv = Math.Matrix(BigWorld.camera().invViewMatrix)
    ray = inv.applyVector(point)
    wPoint = inv.applyPoint(point)
    return (ray, wPoint)


def _clampPoint2DInBox2D(bottomLeft, upperRight, point):
    retPoint = Math.Vector2(0, 0)
    retPoint[0] = max(bottomLeft[0], point[0])
    retPoint[0] = min(retPoint[0], upperRight[0])
    retPoint[1] = max(bottomLeft[1], point[1])
    retPoint[1] = min(retPoint[1], upperRight[1])
    return retPoint


def _almostZero(val, epsilon = 0.0004):
    if -epsilon < val:
        return val < epsilon
    -epsilon < val
    return val


def _clamp(minVal, maxVal, val):
    tmpVal = val
    tmpVal = max(minVal, val)
    tmpVal = min(maxVal, tmpVal)
    return tmpVal


def _vec3fFromYawPitch(yaw, pitch):
    cosPitch = math.cos(+pitch)
    sinPitch = math.sin(-pitch)
    cosYaw = math.cos(yaw)
    sinYaw = math.sin(yaw)
    return Math.Vector3(cosPitch * sinYaw, sinPitch, cosPitch * cosYaw)


