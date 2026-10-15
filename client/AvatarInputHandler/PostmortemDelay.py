# Source Generated with Decompyle++
# File: PostmortemDelay.pyc (Python 2.6)

import BigWorld
import Math
import cameras
import constants
from PlayerEvents import g_playerEvents
from constants import ARENA_PERIOD
from debug_utils import *
import math

class PostmortemDelay:
    FADE_DELAY_TIME = 2
    KILLER_VISION_TIME = 5
    KILLER_VEHICLE_CAMERA_DISTANCE = 15
    KILLER_VEHICLE_CAMERA_PIVOT_POSITION = Math.Vector3(0, 1.5, 3)
    KILLER_VEHICLE_PITCH_OFFSET = -0.3
    
    def __init__(self, arcadeCamera, onStop):
        if not isinstance(arcadeCamera, cameras.ArcadeCamera):
            raise AssertionError
        self._PostmortemDelay__killerVehicleID = None
        self._PostmortemDelay__bActive = False
        self._PostmortemDelay__bChoiceWindowActive = False
        self._PostmortemDelay__bFadeScreenActive = False
        self._PostmortemDelay__bKillerVisionActive = False
        self._PostmortemDelay__savedPivotPosition = None
        self._PostmortemDelay__savedCameraDistance = None
        self._PostmortemDelay__savedYawPitch = None
        self._PostmortemDelay__arcadeCamera = arcadeCamera
        self._PostmortemDelay__onStop = onStop
        self._PostmortemDelay__cbIDWait = None
        BigWorld.player().onVehicleLeaveWorld += self._PostmortemDelay__onVehicleLeaveWorld
        g_playerEvents.onArenaPeriodChange += self._PostmortemDelay__onRoundFinished

    
    def destroy(self):
        self.stop()
        self._PostmortemDelay__arcadeCamera = None
        self._PostmortemDelay__onStop = None
        BigWorld.player().onVehicleLeaveWorld -= self._PostmortemDelay__onVehicleLeaveWorld
        g_playerEvents.onArenaPeriodChange -= self._PostmortemDelay__onRoundFinished

    
    def start(self):
        if self._PostmortemDelay__bActive:
            return None
        self._PostmortemDelay__bActive = True
        self._PostmortemDelay__fadeScreen()
        self._PostmortemDelay__moveCameraTo(BigWorld.player().playerVehicleID)
        self._PostmortemDelay__cbIDWait = BigWorld.callback(self.FADE_DELAY_TIME, self._PostmortemDelay__onFadeDelay)

    
    def stop(self):
        if not self._PostmortemDelay__bActive:
            return None
        self._PostmortemDelay__cancelWait()
        self._PostmortemDelay__showChoiceWindow(False)
        self._PostmortemDelay__fadeScreen(bFade = False)
        self._PostmortemDelay__bKillerVisionActive = False
        self._PostmortemDelay__moveCameraTo(BigWorld.player().playerVehicleID)
        self._PostmortemDelay__killerVehicleID = None
        self._PostmortemDelay__savedPivotPosition = None
        self._PostmortemDelay__savedCameraDistance = None
        self._PostmortemDelay__savedYawPitch = None
        self._PostmortemDelay__bActive = False
        
        try:
            self._PostmortemDelay__onStop()
        except:
            LOG_CURRENT_EXCEPTION()


    
    def _PostmortemDelay__fadeScreen(self, bFade = True):
        if self._PostmortemDelay__bFadeScreenActive == bFade:
            return None
        self._PostmortemDelay__bFadeScreenActive = bFade
        if bFade:
            pass
        1

    
    def _PostmortemDelay__showChoiceWindow(self, bShow = True):
        if self._PostmortemDelay__bChoiceWindowActive == bShow:
            return None
        self._PostmortemDelay__bChoiceWindowActive = bShow
        if bShow:
            self._PostmortemDelay__onContinueBattle()
        

    
    def _PostmortemDelay__moveCameraTo(self, vehicleID, sourceVehicleID = None):
        vehicle = BigWorld.entity(vehicleID)
        if vehicle is None:
            if vehicleID == BigWorld.player().playerVehicleID:
                self._PostmortemDelay__setCameraSettings(targetMP = BigWorld.player().getOwnVehicleMatrix(), pivotPosition = self._PostmortemDelay__savedPivotPosition, cameraDistance = self._PostmortemDelay__savedCameraDistance, yawPitch = self._PostmortemDelay__savedYawPitch)
                return True
            return False
        self._PostmortemDelay__setCameraSettings(targetMP = vehicle.matrix, pivotPosition = self._PostmortemDelay__savedPivotPosition, cameraDistance = self._PostmortemDelay__savedCameraDistance, yawPitch = self._PostmortemDelay__savedYawPitch)
        if sourceVehicleID is not None:
            sourceVehicle = BigWorld.entity(sourceVehicleID)
            if sourceVehicle is not None:
                self._PostmortemDelay__savedPivotPosition = self._PostmortemDelay__arcadeCamera.getPivotPosition()
                self._PostmortemDelay__savedCameraDistance = self._PostmortemDelay__arcadeCamera.getCameraDistance()
                self._PostmortemDelay__savedYawPitch = self._PostmortemDelay__arcadeCamera.getYawPitch()
                dir = Math.Matrix(vehicle.matrix).translation - Math.Matrix(sourceVehicle.matrix).translation
                yaw = dir.yaw
                pitch = dir.pitch + self.KILLER_VEHICLE_PITCH_OFFSET
                if pitch > math.pi * 0.5:
                    pitch = math.pi * 0.5
                
                if pitch < -(math.pi) * 0.5:
                    pitch = -(math.pi) * 0.5
                
                self._PostmortemDelay__setCameraSettings(pivotPosition = Math.Vector3(self.KILLER_VEHICLE_CAMERA_PIVOT_POSITION), cameraDistance = self.KILLER_VEHICLE_CAMERA_DISTANCE, yawPitch = (yaw, pitch))
            
        
        return True

    
    def _PostmortemDelay__setCameraSettings(self, targetMP = None, pivotPosition = None, cameraDistance = None, yawPitch = None):
        if targetMP is not None:
            camTargetTransOnly = Math.WGTranslationOnlyMP()
            camTargetTransOnly.source = targetMP
            self._PostmortemDelay__arcadeCamera.camera.target = camTargetTransOnly
        
        if pivotPosition is not None:
            self._PostmortemDelay__arcadeCamera.setPivotPosition(pivotPosition)
        
        if cameraDistance is not None:
            self._PostmortemDelay__arcadeCamera.setCameraDistance(cameraDistance)
        
        if yawPitch is not None:
            self._PostmortemDelay__arcadeCamera.setYawPitch(yawPitch[0], yawPitch[1])
        

    
    def _PostmortemDelay__onFadeDelay(self):
        self._PostmortemDelay__cbIDWait = None
        if self._PostmortemDelay__killerVehicleID is None:
            self._PostmortemDelay__killerVehicleID = BigWorld.player().inputHandler.getKillerVehicleID()
        
        if self._PostmortemDelay__killerVehicleID is None:
            self.stop()
            return None
        self._PostmortemDelay__startKillerVision()

    
    def _PostmortemDelay__startKillerVision(self):
        if not self._PostmortemDelay__moveCameraTo(self._PostmortemDelay__killerVehicleID, BigWorld.player().playerVehicleID):
            LOG_DEBUG("<PostmortemDelay>: can't move camera to killer vehicle")
            self._PostmortemDelay__showChoiceWindow()
            return None
        self._PostmortemDelay__bKillerVisionActive = True
        self._PostmortemDelay__cbIDWait = BigWorld.callback(self.KILLER_VISION_TIME, self._PostmortemDelay__onKillerVisionFinished)

    
    def _PostmortemDelay__onKillerVisionFinished(self):
        self._PostmortemDelay__cbIDWait = None
        self._PostmortemDelay__bKillerVisionActive = False
        self._PostmortemDelay__moveCameraTo(BigWorld.player().playerVehicleID)
        self._PostmortemDelay__showChoiceWindow()

    
    def _PostmortemDelay__onContinueBattle(self):
        self.stop()

    
    def _PostmortemDelay__onVehicleLeaveWorld(self, vehicle):
        if not self._PostmortemDelay__bActive:
            return None
        if vehicle.id == self._PostmortemDelay__killerVehicleID:
            if self._PostmortemDelay__bKillerVisionActive:
                self._PostmortemDelay__arcadeCamera.camera.target = Math.Matrix(self._PostmortemDelay__arcadeCamera.camera.target)
            
        

    
    def _PostmortemDelay__onRoundFinished(self, period, *args):
        if period != ARENA_PERIOD.AFTERBATTLE:
            return None
        self.stop()

    
    def _PostmortemDelay__cancelWait(self):
        if self._PostmortemDelay__cbIDWait is not None:
            BigWorld.cancelCallback(self._PostmortemDelay__cbIDWait)
            self._PostmortemDelay__cbIDWait = None
        



