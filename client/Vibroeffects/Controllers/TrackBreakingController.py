# Source Generated with Decompyle++
# File: TrackBreakingController.pyc (Python 2.6)

import BigWorld
import Math
from Math import Matrix
from debug_utils import *
import math
import copy
from Vibroeffects.Controllers.OnceController import OnceController

class TrackBreakingController:
    _TrackBreakingController__MIN_MOVEMENT_SPEED = 1
    _TrackBreakingController__wasLeftTrackBroken = None
    _TrackBreakingController__wasRightTrackBroken = None
    _TrackBreakingController__ANGLES_VIBRATIONS = [
        [
            math.pi / 4,
            'crit_track_front_right_veff'],
        [
            math.pi / 2 + math.pi / 4,
            'crit_track_front_left_veff'],
        [
            math.pi + math.pi / 4,
            'crit_track_rear_left_veff'],
        [
            math.pi * 3 / 2 + math.pi / 4,
            'crit_track_rear_right_veff']]
    
    def _TrackBreakingController__break(self, vehicleSpeed):
        if vehicleSpeed < TrackBreakingController._TrackBreakingController__MIN_MOVEMENT_SPEED:
            OnceController('crit_track_veff')
        else:
            OnceController('move_track_veff')

    
    def _TrackBreakingController__breakWithDirection(self, vehicle, isLeftTrackBroken):
        directionMatrix = Math.Matrix(BigWorld.camera().source)
        directionMatrix.setElement(3, 0, 0)
        directionMatrix.setElement(3, 1, 0)
        directionMatrix.setElement(3, 2, 0)
        cameraDirection = directionMatrix.applyToAxis(0)
        cameraDirection.y = 0
        vehicleMatrix = Math.Matrix(vehicle.matrix)
        vehicleMatrix.setElement(3, 0, 0)
        vehicleMatrix.setElement(3, 1, 0)
        vehicleMatrix.setElement(3, 2, 0)
        vehicleMatrix.invert()
        cameraDirection = vehicleMatrix.applyVector(cameraDirection)
        brokenTrackAngle = 0
        if isLeftTrackBroken:
            brokenTrackAngle = math.pi
        
        dirAngleRelative = math.atan2(cameraDirection.z, cameraDirection.x)
        minDirDelta = math.pi * 2
        vibrationToPlay = ''
        for angleVibration in TrackBreakingController._TrackBreakingController__ANGLES_VIBRATIONS:
            curAngle = angleVibration[0]
            curAngle += dirAngleRelative
            if curAngle > math.pi * 2:
                curAngle -= math.pi * 2
            
            if curAngle < 0:
                curAngle += math.pi * 2
            
            curDirDelta = abs(curAngle - brokenTrackAngle)
            if curDirDelta > math.pi:
                curDirDelta = math.pi * 2 - curDirDelta
            
            if curDirDelta < minDirDelta:
                minDirDelta = curDirDelta
                vibrationToPlay = angleVibration[1]
                continue
        
        OnceController(vibrationToPlay)

    
    def update(self, vehicle, isLeftTrackBroken, isRightTrackBroken):
        if self._TrackBreakingController__wasLeftTrackBroken == False and isLeftTrackBroken:
            self._TrackBreakingController__breakWithDirection(vehicle, True)
        elif self._TrackBreakingController__wasRightTrackBroken == False and isRightTrackBroken:
            self._TrackBreakingController__breakWithDirection(vehicle, False)
        
        self._TrackBreakingController__wasLeftTrackBroken = isLeftTrackBroken
        self._TrackBreakingController__wasRightTrackBroken = isRightTrackBroken



