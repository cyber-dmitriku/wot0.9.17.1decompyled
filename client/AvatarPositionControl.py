# Source Generated with Decompyle++
# File: AvatarPositionControl.pyc (Python 2.6)

import BigWorld
import constants
import weakref
import BattleReplay
from debug_utils import *
import time

class AvatarPositionControl:
    FOLLOW_CAMERA_MAX_DEVIATION = 10
    
    def __init__(self, avatar):
        self._AvatarPositionControl__avatar = weakref.proxy(avatar)
        self._AvatarPositionControl__bFollowCamera = False

    
    def destroy(self):
        self._AvatarPositionControl__avatar = None

    
    def bindToVehicle(self, bValue = True, vehicleID = None):
        if bValue:
            if vehicleID is None:
                vehicleID = self._AvatarPositionControl__avatar.playerVehicleID
            
            self._AvatarPositionControl__doBind(vehicleID)
        else:
            self._AvatarPositionControl__doUnbind()

    
    def followCamera(self, bValue = True):
        self._AvatarPositionControl__bFollowCamera = bValue
        if bValue:
            self.onFollowCameraTick()
        

    
    def moveTo(self, pos):
        self._AvatarPositionControl__avatar.cell.moveTo(pos)

    
    def getFollowCamera(self):
        return self._AvatarPositionControl__bFollowCamera

    
    def onFollowCameraTick(self):
        if not self._AvatarPositionControl__bFollowCamera:
            return None
        cam = BigWorld.camera()
        if cam is None:
            return None
        if BigWorld.camera().position.flatDistTo(self._AvatarPositionControl__avatar.position) >= self.FOLLOW_CAMERA_MAX_DEVIATION:
            self.moveTo(BigWorld.camera().position)
        

    
    def _AvatarPositionControl__doBind(self, vehicleID):
        pos = self._AvatarPositionControl__avatar.arena.positions.get(vehicleID)
        if pos is None and vehicleID == self._AvatarPositionControl__avatar.playerVehicleID:
            pos = self._AvatarPositionControl__avatar.getOwnVehiclePosition()
        
        if pos is None:
            pos = self._AvatarPositionControl__avatar.position
        
        self._AvatarPositionControl__avatar.cell.bindToVehicle(vehicleID, pos)
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isRecording:
            replayCtrl.setPlayerVehicleID(vehicleID)
        

    
    def _AvatarPositionControl__doUnbind(self):
        self._AvatarPositionControl__avatar.cell.bindToVehicle(0, self._AvatarPositionControl__avatar.position)
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isRecording:
            replayCtrl.setPlayerVehicleID(0)
        



