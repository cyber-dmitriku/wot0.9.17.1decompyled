# Source Generated with Decompyle++
# File: VehicleGunRotator.pyc (Python 2.6)

import BigWorld
import Math
import weakref
from constants import SERVER_TICK_LENGTH, SHELL_TRAJECTORY_EPSILON_CLIENT
from projectile_trajectory import getShotAngles
from ProjectileMover import collideDynamicAndStatic
from debug_utils import *
from math import pi, sin, cos, atan, atan2, sqrt, fmod
from projectile_trajectory import computeProjectileTrajectory
import BattleReplay
from gun_rotation_shared import calcPitchLimitsFromDesc
from account_helpers.AccountSettings import AccountSettings

class VehicleGunRotator(object):
    _VehicleGunRotator__INSUFFICIENT_TIME_DIFF = 0.02
    _VehicleGunRotator__MAX_TIME_DIFF = 0.2
    _VehicleGunRotator__ROTATION_TICK_LENGTH = SERVER_TICK_LENGTH
    
    def __init__(self, avatar):
        self._VehicleGunRotator__avatar = weakref.proxy(avatar)
        self._VehicleGunRotator__isStarted = False
        self._VehicleGunRotator__prevSentShotPoint = None
        self._VehicleGunRotator__targetLastShotPoint = False
        self._VehicleGunRotator__lastShotPoint = Math.Vector3(0, 0, 0)
        self._VehicleGunRotator__shotPointSourceFunctor = self._VehicleGunRotator__shotPointSourceFunctor_Default
        self._VehicleGunRotator__maxTurretRotationSpeed = None
        self._VehicleGunRotator__maxGunRotationSpeed = None
        self._VehicleGunRotator__turretYaw = 0
        self._VehicleGunRotator__gunPitch = 0
        self._VehicleGunRotator__turretRotationSpeed = 0
        self._VehicleGunRotator__dispersionAngle = 0
        self._VehicleGunRotator__markerInfo = (Math.Vector3(0, 0, 0), Math.Vector3(0, 1, 0), 1)
        self._VehicleGunRotator__clientMode = True
        self._VehicleGunRotator__showServerMarker = False
        self._VehicleGunRotator__time = None
        self._VehicleGunRotator__timerID = None
        self._VehicleGunRotator__turretMatrixAnimator = _MatrixAnimator(self._VehicleGunRotator__avatar)
        self._VehicleGunRotator__gunMatrixAnimator = _MatrixAnimator(self._VehicleGunRotator__avatar)
        self._VehicleGunRotator__isLocked = False
        self.estimatedTurretRotationTime = 0

    
    def destroy(self):
        self.stop()
        self._VehicleGunRotator__turretMatrixAnimator.destroy(self._VehicleGunRotator__avatar)
        self._VehicleGunRotator__gunMatrixAnimator.destroy(self._VehicleGunRotator__avatar)
        self._VehicleGunRotator__avatar = None

    
    def start(self):
        if self._VehicleGunRotator__isStarted:
            return None
        if self._VehicleGunRotator__maxTurretRotationSpeed is None:
            return None
        if not (self._VehicleGunRotator__avatar.isOnArena) or not (self._VehicleGunRotator__avatar.isVehicleAlive):
            return None
        self.showServerMarker = AccountSettings.getSettings('useServerAim')
        AccountSettings.onSettingsChanging += self.applySettings
        self._VehicleGunRotator__isStarted = True
        self._VehicleGunRotator__updateGunMarker()
        self._VehicleGunRotator__timerID = BigWorld.callback(self._VehicleGunRotator__ROTATION_TICK_LENGTH, self._VehicleGunRotator__onTick)
        if self._VehicleGunRotator__clientMode:
            self._VehicleGunRotator__time = BigWorld.time()
            if self._VehicleGunRotator__showServerMarker:
                self._VehicleGunRotator__avatar.inputHandler.showGunMarker2(True)
            
        

    
    def applySettings(self, type):
        if type == 'useServerAim':
            self.showServerMarker = AccountSettings.getSettings('useServerAim')
        

    
    def stop(self):
        if not self._VehicleGunRotator__isStarted:
            return None
        if self._VehicleGunRotator__timerID is not None:
            BigWorld.cancelCallback(self._VehicleGunRotator__timerID)
            self._VehicleGunRotator__timerID = None
        
        if self._VehicleGunRotator__avatar.inputHandler is None:
            return None
        if self._VehicleGunRotator__clientMode and self._VehicleGunRotator__showServerMarker:
            self._VehicleGunRotator__avatar.inputHandler.showGunMarker2(False)
        
        AccountSettings.onSettingsChanging -= self.applySettings
        self._VehicleGunRotator__isStarted = False

    
    def lock(self, isLocked):
        self._VehicleGunRotator__isLocked = isLocked

    
    def update(self, turretYaw, gunPitch, maxTurretRotationSpeed, maxGunRotationSpeed):
        if self._VehicleGunRotator__timerID is None or maxTurretRotationSpeed < self._VehicleGunRotator__maxTurretRotationSpeed:
            self._VehicleGunRotator__turretYaw = turretYaw
            self._VehicleGunRotator__gunPitch = gunPitch
            self._VehicleGunRotator__updateTurretMatrix(turretYaw, 0)
            self._VehicleGunRotator__updateGunMatrix(gunPitch, 0)
        
        self._VehicleGunRotator__maxTurretRotationSpeed = maxTurretRotationSpeed
        self._VehicleGunRotator__maxGunRotationSpeed = maxGunRotationSpeed
        self._VehicleGunRotator__turretRotationSpeed = 0
        self._VehicleGunRotator__dispersionAngle = self._VehicleGunRotator__avatar.getOwnVehicleShotDispersionAngle(0)
        self.start()

    
    def setShotPosition(self, shotPos, shotVec, dispersionAngle):
        if self._VehicleGunRotator__clientMode and not (self._VehicleGunRotator__showServerMarker):
            return None
        self._VehicleGunRotator__dispersionAngle = dispersionAngle
        (markerPos, markerDir, markerSize, collData) = self._VehicleGunRotator__getGunMarkerPosition(shotPos, shotVec, dispersionAngle)
        if self._VehicleGunRotator__clientMode and self._VehicleGunRotator__showServerMarker:
            self._VehicleGunRotator__avatar.inputHandler.updateGunMarker2(markerPos, markerDir, markerSize, SERVER_TICK_LENGTH, collData)
        
        if not self._VehicleGunRotator__clientMode:
            self._VehicleGunRotator__lastShotPoint = markerPos
            self._VehicleGunRotator__avatar.inputHandler.updateGunMarker(markerPos, markerDir, markerSize, SERVER_TICK_LENGTH, collData)
            (self._VehicleGunRotator__turretYaw, self._VehicleGunRotator__gunPitch) = getShotAngles(self._VehicleGunRotator__avatar.vehicleTypeDescriptor, self._VehicleGunRotator__avatar.getOwnVehicleMatrix(), (self._VehicleGunRotator__turretYaw, self._VehicleGunRotator__gunPitch), markerPos, True)
            self._VehicleGunRotator__updateTurretMatrix(self._VehicleGunRotator__turretYaw, SERVER_TICK_LENGTH)
            self._VehicleGunRotator__updateGunMatrix(self._VehicleGunRotator__gunPitch, SERVER_TICK_LENGTH)
            self._VehicleGunRotator__markerInfo = (markerPos, markerDir, markerSize)
        

    
    def getShotParams(self, targetPoint):
        descr = self._VehicleGunRotator__avatar.vehicleTypeDescriptor
        (shotTurretYaw, shotGunPitch) = getShotAngles(descr, self._VehicleGunRotator__avatar.getOwnVehicleMatrix(), (self._VehicleGunRotator__turretYaw, self._VehicleGunRotator__gunPitch), targetPoint)
        gunPitchLimits = calcPitchLimitsFromDesc(shotTurretYaw, descr.gun['pitchLimits'])
        closestLimit = self._VehicleGunRotator__isOutOfLimits(shotGunPitch, gunPitchLimits)
        if closestLimit is not None:
            shotGunPitch = closestLimit
        
        (pos, vel) = self._VehicleGunRotator__getShotPosition(shotTurretYaw, shotGunPitch)
        grav = Math.Vector3(0, -descr.shot['gravity'], 0)
        return (pos, vel, grav)

    
    def _VehicleGunRotator__set_clientMode(self, value):
        if self._VehicleGunRotator__clientMode == value:
            return None
        self._VehicleGunRotator__clientMode = value
        if not self._VehicleGunRotator__isStarted:
            return None
        if self._VehicleGunRotator__clientMode:
            self._VehicleGunRotator__time = BigWorld.time()
        
        if self._VehicleGunRotator__showServerMarker:
            self._VehicleGunRotator__avatar.inputHandler.showGunMarker2(self._VehicleGunRotator__clientMode)
        

    clientMode = property((lambda self: self._VehicleGunRotator__clientMode), _VehicleGunRotator__set_clientMode)
    
    def _VehicleGunRotator__set_showServerMarker(self, value):
        if self._VehicleGunRotator__showServerMarker == value:
            return None
        self._VehicleGunRotator__showServerMarker = value
        BigWorld.player().enableServerAim(self.showServerMarker)
        if not self._VehicleGunRotator__isStarted:
            return None
        if self._VehicleGunRotator__clientMode:
            self._VehicleGunRotator__avatar.inputHandler.showGunMarker2(self._VehicleGunRotator__showServerMarker)
        

    showServerMarker = property((lambda self: self._VehicleGunRotator__showServerMarker), _VehicleGunRotator__set_showServerMarker)
    
    def _VehicleGunRotator__set_targetLastShotPoint(self, value):
        self._VehicleGunRotator__targetLastShotPoint = value

    targetLastShotPoint = property((lambda self: self._VehicleGunRotator__targetLastShotPoint), _VehicleGunRotator__set_targetLastShotPoint)
    
    def _VehicleGunRotator__set_shotPointSourceFunctor(self, value):
        if value is not None:
            self._VehicleGunRotator__shotPointSourceFunctor = value
        else:
            self._VehicleGunRotator__shotPointSourceFunctor = self._VehicleGunRotator__shotPointSourceFunctor_Default

    shotPointSourceFunctor = property((lambda self: self._VehicleGunRotator__shotPointSourceFunctor), _VehicleGunRotator__set_shotPointSourceFunctor)
    
    def _VehicleGunRotator__shotPointSourceFunctor_Default(self):
        pt = self._VehicleGunRotator__avatar.inputHandler.getDesiredShotPoint()
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.isClientReady:
            pt = replayCtrl.getGunRotatorTargetPoint()
        elif replayCtrl.isRecording:
            if pt is not None:
                replayCtrl.setGunRotatorTargetPoint(pt)
            
        
        return pt

    turretMatrix = property((lambda self: self._VehicleGunRotator__turretMatrixAnimator.matrix))
    gunMatrix = property((lambda self: self._VehicleGunRotator__gunMatrixAnimator.matrix))
    turretRotationSpeed = property((lambda self: self._VehicleGunRotator__turretRotationSpeed))
    dispersionAngle = property((lambda self: self._VehicleGunRotator__dispersionAngle))
    markerInfo = property((lambda self: self._VehicleGunRotator__markerInfo))
    
    def _VehicleGunRotator__onTick(self):
        self._VehicleGunRotator__timerID = BigWorld.callback(self._VehicleGunRotator__ROTATION_TICK_LENGTH, self._VehicleGunRotator__onTick)
        replayCtrl = BattleReplay.g_replayCtrl
        if not (self._VehicleGunRotator__clientMode) and not (replayCtrl.isPlaying):
            return None
        shotPoint = self._VehicleGunRotator__shotPointSourceFunctor()
        if shotPoint is None and self._VehicleGunRotator__targetLastShotPoint:
            shotPoint = self._VehicleGunRotator__lastShotPoint
        
        self._VehicleGunRotator__updateShotPointOnServer(shotPoint)
        timeDiff = self._VehicleGunRotator__getTimeDiff()
        if timeDiff is None:
            return None
        self._VehicleGunRotator__time = BigWorld.time()
        self._VehicleGunRotator__rotate(shotPoint, timeDiff)
        self._VehicleGunRotator__updateGunMarker()

    
    def _VehicleGunRotator__getTimeDiff(self):
        timeDiff = BigWorld.time() - self._VehicleGunRotator__time
        if timeDiff < self._VehicleGunRotator__INSUFFICIENT_TIME_DIFF:
            return None
        if timeDiff > self._VehicleGunRotator__MAX_TIME_DIFF:
            timeDiff = self._VehicleGunRotator__MAX_TIME_DIFF
        
        return timeDiff

    
    def _VehicleGunRotator__updateShotPointOnServer(self, shotPoint):
        if shotPoint == self._VehicleGunRotator__prevSentShotPoint:
            return None
        self._VehicleGunRotator__prevSentShotPoint = shotPoint
        if shotPoint is None:
            self._VehicleGunRotator__avatar.base.vehicle_stopTrackingWithGun(self._VehicleGunRotator__turretYaw, self._VehicleGunRotator__gunPitch)
        else:
            vehicle = BigWorld.entity(self._VehicleGunRotator__avatar.playerVehicleID)
            if vehicle is not None:
                vehicle.cell.trackPointWithGun(shotPoint)
            else:
                self._VehicleGunRotator__avatar.base.vehicle_trackPointWithGun(shotPoint)

    
    def _VehicleGunRotator__rotate(self, shotPoint, timeDiff):
        self._VehicleGunRotator__turretRotationSpeed = 0
        if shotPoint is None:
            self._VehicleGunRotator__dispersionAngle = self._VehicleGunRotator__avatar.getOwnVehicleShotDispersionAngle(0)
            return None
        if self._VehicleGunRotator__isLocked:
            return None
        avatar = self._VehicleGunRotator__avatar
        descr = avatar.vehicleTypeDescriptor
        turretYawLimits = descr.turret['yawLimits']
        maxTurretRotationSpeed = self._VehicleGunRotator__maxTurretRotationSpeed
        prevTurretYaw = self._VehicleGunRotator__turretYaw
        (shotTurretYaw, shotGunPitch) = getShotAngles(descr, avatar.getOwnVehicleMatrix(), (prevTurretYaw, self._VehicleGunRotator__gunPitch), shotPoint)
        self._VehicleGunRotator__turretYaw = self._VehicleGunRotator__getNextTurretYaw(prevTurretYaw, shotTurretYaw, maxTurretRotationSpeed * timeDiff, turretYawLimits)
        turretYaw = self._VehicleGunRotator__getNextTurretYaw(prevTurretYaw, shotTurretYaw, maxTurretRotationSpeed * timeDiff, turretYawLimits)
        if maxTurretRotationSpeed != 0:
            self.estimatedTurretRotationTime = abs(turretYaw - shotTurretYaw) / maxTurretRotationSpeed
        else:
            self.estimatedTurretRotationTime = 0
        gunPitchLimits = calcPitchLimitsFromDesc(turretYaw, descr.gun['pitchLimits'])
        self._VehicleGunRotator__gunPitch = self._VehicleGunRotator__getNextGunPitch(self._VehicleGunRotator__gunPitch, shotGunPitch, self._VehicleGunRotator__maxGunRotationSpeed * timeDiff, gunPitchLimits)
        self._VehicleGunRotator__updateTurretMatrix(turretYaw, self._VehicleGunRotator__ROTATION_TICK_LENGTH)
        self._VehicleGunRotator__updateGunMatrix(self._VehicleGunRotator__gunPitch, self._VehicleGunRotator__ROTATION_TICK_LENGTH)
        diff = abs(turretYaw - prevTurretYaw)
        if diff > pi:
            diff = 2 * pi - diff
        
        self._VehicleGunRotator__turretRotationSpeed = diff / timeDiff
        self._VehicleGunRotator__dispersionAngle = avatar.getOwnVehicleShotDispersionAngle(self._VehicleGunRotator__turretRotationSpeed)

    
    def _VehicleGunRotator__updateGunMarker(self):
        (shotPos, shotVec) = self._VehicleGunRotator__getCurShotPosition()
        (markerPos, markerDir, markerSize, collData) = self._VehicleGunRotator__getGunMarkerPosition(shotPos, shotVec, self._VehicleGunRotator__dispersionAngle)
        if not self._VehicleGunRotator__targetLastShotPoint:
            self._VehicleGunRotator__lastShotPoint = markerPos
        
        self._VehicleGunRotator__avatar.inputHandler.updateGunMarker(markerPos, markerDir, markerSize, self._VehicleGunRotator__ROTATION_TICK_LENGTH, collData)
        self._VehicleGunRotator__markerInfo = (markerPos, markerDir, markerSize)

    
    def _VehicleGunRotator__getNextTurretYaw(self, curAngle, shotAngle, speedLimit, angleLimits):
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying:
            turretYaw = replayCtrl.getTurretYaw()
            if turretYaw > -100000:
                return turretYaw
        
        if curAngle == shotAngle:
            return curAngle
        (shortWayDiff, longWayDiff) = self._VehicleGunRotator__getRotationWays(curAngle, shotAngle)
        if speedLimit < 1e-05:
            return curAngle
        closestLimit = self._VehicleGunRotator__isOutOfLimits(curAngle, angleLimits)
        if closestLimit is not None:
            return closestLimit
        shortWayDiffLimited = self._VehicleGunRotator__applyTurretYawLimits(shortWayDiff, curAngle, angleLimits)
        if shortWayDiffLimited == shortWayDiff:
            return self._VehicleGunRotator__getTurretYawWithSpeedLimit(curAngle, shortWayDiff, speedLimit)
        longWayDiffLimited = self._VehicleGunRotator__applyTurretYawLimits(longWayDiff, curAngle, angleLimits)
        if longWayDiffLimited == longWayDiff:
            return self._VehicleGunRotator__getTurretYawWithSpeedLimit(curAngle, longWayDiff, speedLimit)
        return self._VehicleGunRotator__getTurretYawWithSpeedLimit(curAngle, shortWayDiffLimited, speedLimit)

    
    def _VehicleGunRotator__getRotationWays(self, curAngle, shotAngle):
        shotDiff1 = shotAngle - curAngle
        if shotDiff1 < 0:
            shotDiff2 = 2 * pi + shotDiff1
        else:
            shotDiff2 = -2 * pi + shotDiff1
        if abs(shotDiff1) <= pi:
            return (shotDiff1, shotDiff2)
        return (shotDiff2, shotDiff1)

    
    def _VehicleGunRotator__isOutOfLimits(self, angle, limits):
        if limits is None:
            return None
        if abs(limits[1] - angle) < 1e-05 or abs(limits[0] - angle) < 1e-05:
            return None
        dpi = 2 * pi
        minDiff = fmod((limits[0] - angle) + dpi, dpi)
        maxDiff = fmod((limits[1] - angle) + dpi, dpi)
        if minDiff > maxDiff:
            return None
        if minDiff < dpi - maxDiff:
            return limits[0]
        return limits[1]

    
    def _VehicleGunRotator__applyTurretYawLimits(self, diff, angle, limits):
        if limits is None:
            return diff
        dpi = 2 * pi
        if diff > 0:
            if abs(limits[1] - angle) < 1e-05:
                return 0
            maxDiff = fmod((limits[1] - angle) + dpi, dpi)
            return min(maxDiff, diff)
        if abs(limits[0] - angle) < 1e-05:
            return 0
        maxDiff = fmod(limits[0] - angle - dpi, dpi)
        return max(maxDiff, diff)

    
    def _VehicleGunRotator__getTurretYawWithSpeedLimit(self, angle, diff, limit):
        dpi = 2 * pi
        if diff > 0:
            return fmod(pi + angle + min(diff, limit), dpi) - pi
        return fmod(-pi + angle + max(diff, -limit), dpi) + pi

    
    def _VehicleGunRotator__getNextGunPitch(self, curAngle, shotAngle, speedLimit, angleLimits):
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying:
            gunPitch = replayCtrl.getGunPitch()
            if gunPitch > -100000:
                return gunPitch
        
        if curAngle == shotAngle:
            return curAngle
        shotDiff = shotAngle - curAngle
        if angleLimits is not None:
            if shotAngle < angleLimits[0]:
                shotDiff = angleLimits[0] - curAngle
            elif shotAngle > angleLimits[1]:
                shotDiff = angleLimits[1] - curAngle
            
        
        if shotDiff > 0:
            return curAngle + min(shotDiff, speedLimit)
        return curAngle + max(shotDiff, -speedLimit)

    
    def _VehicleGunRotator__getShotPosition(self, turretYaw, gunPitch):
        descr = self._VehicleGunRotator__avatar.vehicleTypeDescriptor
        turretOffs = descr.hull['turretPositions'][0] + descr.chassis['hullPosition']
        gunOffs = descr.turret['gunPosition']
        shotSpeed = descr.shot['speed']
        turretWorldMatrix = Math.Matrix()
        turretWorldMatrix.setRotateY(turretYaw)
        turretWorldMatrix.translation = turretOffs
        turretWorldMatrix.postMultiply(Math.Matrix(self._VehicleGunRotator__avatar.getOwnVehicleMatrix()))
        position = turretWorldMatrix.applyPoint(gunOffs)
        gunWorldMatrix = Math.Matrix()
        gunWorldMatrix.setRotateX(gunPitch)
        gunWorldMatrix.postMultiply(turretWorldMatrix)
        vector = gunWorldMatrix.applyVector(Math.Vector3(0, 0, shotSpeed))
        return (position, vector)

    
    def _VehicleGunRotator__getCurShotPosition(self):
        return self._VehicleGunRotator__getShotPosition(self._VehicleGunRotator__turretYaw, self._VehicleGunRotator__gunPitch)

    
    def _VehicleGunRotator__getGunMarkerPosition(self, shotPos, shotVec, dispersionAngle):
        shotDescr = self._VehicleGunRotator__avatar.vehicleTypeDescriptor.shot
        gravity = Math.Vector3(0, -shotDescr['gravity'], 0)
        maxDist = shotDescr['maxDistance']
        prevPos = shotPos
        prevVelocity = shotVec
        dt = 0
        maxDistCheckFlag = False
        while True:
            dt += SERVER_TICK_LENGTH
            checkPoints = computeProjectileTrajectory(prevPos, prevVelocity, gravity, SERVER_TICK_LENGTH, SHELL_TRAJECTORY_EPSILON_CLIENT)
            prevCheckPoint = prevPos
            bBreak = False
            for curCheckPoint in checkPoints:
                testRes = collideDynamicAndStatic(prevCheckPoint, curCheckPoint, (self._VehicleGunRotator__avatar.playerVehicleID,))
                if testRes is not None:
                    collData = testRes[1]
                    dir = testRes[0] - prevCheckPoint
                    endPos = testRes[0]
                    bBreak = True
                    break
                
                pos = self._VehicleGunRotator__avatar.arena.collideWithSpaceBB(prevCheckPoint, curCheckPoint)
                if pos is not None:
                    collData = None
                    maxDistCheckFlag = True
                    dir = pos - prevCheckPoint
                    endPos = pos
                    bBreak = True
                    break
                
                prevCheckPoint = curCheckPoint
            
            if bBreak:
                break
            
            prevPos = shotPos + shotVec.scale(dt) + gravity.scale(dt * dt * 0.5)
            prevVelocity = shotVec + gravity.scale(dt)
        dir.normalise()
        distance = (endPos - shotPos).length
        markerDiameter = 2 * distance * dispersionAngle
        if maxDistCheckFlag:
            if endPos.distTo(shotPos) >= maxDist:
                dir = endPos - shotPos
                dir.normalise()
                endPos = shotPos + dir.scale(maxDist)
                distance = maxDist
                markerDiameter = 2 * distance * dispersionAngle
            
        
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.isClientReady:
            (markerDiameter, endPos, dir) = replayCtrl.getGunMarkerParams(endPos, dir)
        elif replayCtrl.isRecording:
            replayCtrl.setGunMarkerParams(markerDiameter, endPos, dir)
        
        return (endPos, dir, markerDiameter, collData)

    
    def _VehicleGunRotator__updateTurretMatrix(self, yaw, time):
        m = Math.Matrix()
        m.setRotateY(yaw)
        self._VehicleGunRotator__turretMatrixAnimator.update(m, time)
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isRecording:
            replayCtrl.setTurretYaw(yaw)
        

    
    def _VehicleGunRotator__updateGunMatrix(self, pitch, time):
        m = Math.Matrix()
        m.setRotateX(pitch)
        self._VehicleGunRotator__gunMatrixAnimator.update(m, time)
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isRecording:
            replayCtrl.setGunPitch(pitch)
        



class _MatrixAnimator(object):
    
    def __init__(self, avatar):
        m = Math.Matrix()
        m.setIdentity()
        self._MatrixAnimator__animMat = Math.MatrixAnimation()
        self._MatrixAnimator__animMat.keyframes = ((0, m),)

    
    def destroy(self, avatar):
        self._MatrixAnimator__animMat = None

    matrix = property((lambda self: self._MatrixAnimator__animMat))
    
    def update(self, matrix, time):
        self._MatrixAnimator__animMat.keyframes = ((0, Math.Matrix(self._MatrixAnimator__animMat)), (time, matrix))
        self._MatrixAnimator__animMat.time = 0



