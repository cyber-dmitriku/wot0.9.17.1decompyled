# Source Generated with Decompyle++
# File: __init__.pyc (Python 2.6)

import BigWorld
import Math
import ResMgr
import game
import GUI
from Event import Event
from debug_utils import *
from gui.Scaleform.CursorDelegator import g_cursorDelegator
from post_processing.post_effect_controllers import g_postProcessingEvents
import control_modes
import constants
import cameras
import BattleReplay
from constants import ARENA_PERIOD, AIMING_MODE
_INPUT_HANDLER_CFG = 'gui/avatar_input_handler.xml'
_CTRLS_FIRST = 'arcade'
_CTRLS_DESC_MAP = {
    'arcade': ('ArcadeControlMode', 'arcadeMode', False),
    'strategic': ('StrategicControlMode', 'strategicMode', False),
    'sniper': ('SniperControlMode', 'sniperMode', False),
    'postmortem': ('PostMortemControlMode', 'postMortemMode', False),
    'debug': ('DebugControlMode', None, True),
    'cat': ('CatControlMode', None, True) }

class AvatarInputHandler(object):
    aim = property((lambda self: self._AvatarInputHandler__curCtrl.getAim()))
    ctrl = property((lambda self: self._AvatarInputHandler__curCtrl))
    ctrls = property((lambda self: self._AvatarInputHandler__ctrls))
    isSPG = property((lambda self: self._AvatarInputHandler__isSPG))
    isATSPG = property((lambda self: self._AvatarInputHandler__isATSPG))
    
    def __init__(self):
        sec = self._readCfg()
        self.onCameraChanged = Event()
        self.onPostmortemVehicleChanged = Event()
        self._AvatarInputHandler__isArenaStarted = False
        self._AvatarInputHandler__isStarted = False
        self._AvatarInputHandler__targeting = _Targeting()
        self._AvatarInputHandler__ctrls = dict()
        self._AvatarInputHandler__killerVehicleID = None
        self._AvatarInputHandler__isAutorotation = True
        self._AvatarInputHandler__prevModeAutorotation = None
        self._AvatarInputHandler__isSPG = False
        self._AvatarInputHandler__isATSPG = False
        self._AvatarInputHandler__setupCtrls(sec)
        self._AvatarInputHandler__curCtrl = self._AvatarInputHandler__ctrls[_CTRLS_FIRST]
        self._AvatarInputHandler__detachCount = 0

    
    def prerequisites(self):
        out = []
        for ctrl in self._AvatarInputHandler__ctrls.itervalues():
            out += ctrl.prerequisites()
        
        return out

    
    def handleKeyEvent(self, event):
        cursorDetached = self._AvatarInputHandler__detachCount < 0
        (isDown, key, mods, isRepeat) = game.convertKeyEvent(event)
        if isRepeat:
            return False
        if self._AvatarInputHandler__isStarted and cursorDetached:
            return BigWorld.player().handleKey(isDown, key, mods)
        if not (self._AvatarInputHandler__isStarted) or cursorDetached:
            return False
        if self._AvatarInputHandler__curCtrl.handleKeyEvent(isDown, key, mods, event):
            return True
        return BigWorld.player().handleKey(isDown, key, mods)

    
    def handleMouseEvent(self, dx, dy, dz):
        if not (self._AvatarInputHandler__isStarted) or self._AvatarInputHandler__detachCount < 0:
            return False
        return self._AvatarInputHandler__curCtrl.handleMouseEvent(dx, dy, dz)

    
    def detachCursor(self, isDetached, enableAiming):
        if not self._AvatarInputHandler__isStarted:
            return None
        if isDetached:
            pass
        1
        -1 += 1
        if not self._AvatarInputHandler__detachCount <= 0:
            raise AssertionError
        if self._AvatarInputHandler__detachCount == -1 and isDetached:
            self._AvatarInputHandler__targeting.enable(False)
            g_cursorDelegator.activateCursor()
            if enableAiming:
                self.setAimingMode(False, AIMING_MODE.USER_DISABLED)
            
        elif not self._AvatarInputHandler__detachCount:
            self._AvatarInputHandler__targeting.enable(True)
            g_cursorDelegator.detachCursor()
        

    
    def updateShootingStatus(self, canShoot):
        if self._AvatarInputHandler__detachCount < 0:
            return None
        return self._AvatarInputHandler__curCtrl.updateShootingStatus(canShoot)

    
    def getDesiredShotPoint(self):
        if self._AvatarInputHandler__detachCount < 0:
            return None
        g_postProcessingEvents.onFocalPlaneChanged()
        return self._AvatarInputHandler__curCtrl.getDesiredShotPoint()

    
    def showGunMarker(self, flag):
        self._AvatarInputHandler__curCtrl.showGunMarker(flag)

    
    def showGunMarker2(self, flag):
        self._AvatarInputHandler__curCtrl.showGunMarker2(flag)

    
    def updateGunMarker(self, pos, dir, size, relaxTime, collData):
        aim = self._AvatarInputHandler__curCtrl.getAim()
        if aim is not None:
            aim.updateMarkerPos(pos, relaxTime)
        
        self._AvatarInputHandler__curCtrl.updateGunMarker(pos, dir, size, relaxTime, collData)

    
    def updateGunMarker2(self, pos, dir, size, relaxTime, collData):
        self._AvatarInputHandler__curCtrl.updateGunMarker2(pos, dir, size, relaxTime, collData)

    
    def setAimingMode(self, enable, mode):
        self._AvatarInputHandler__curCtrl.setAimingMode(enable, mode)

    
    def setAutorotation(self, bValue):
        if self._AvatarInputHandler__curCtrl.getFixedAutorotation() is not None:
            return None
        if not BigWorld.player().isOnArena:
            return None
        if self._AvatarInputHandler__isAutorotation != bValue:
            self._AvatarInputHandler__isAutorotation = bValue
            BigWorld.player().enableOwnVehicleAutorotation(self._AvatarInputHandler__isAutorotation)
        

    
    def getAutorotation(self):
        return self._AvatarInputHandler__isAutorotation

    
    def switchAutorotation(self):
        if self._AvatarInputHandler__curCtrl.getFixedAutorotation() is not None:
            return None
        if not BigWorld.player().isOnArena:
            return None
        self._AvatarInputHandler__isAutorotation = not (self._AvatarInputHandler__isAutorotation)
        BigWorld.player().enableOwnVehicleAutorotation(self._AvatarInputHandler__isAutorotation)

    
    def activatePostmortem(self):
        
        try:
            params = self._AvatarInputHandler__curCtrl.postmortemCamParams
        except:
            params = None

        self.onControlModeChanged('postmortem', postmortemParams = params, bPostmortemDelay = True)

    
    def setKillerVehicleID(self, killerVehicleID):
        self._AvatarInputHandler__killerVehicleID = killerVehicleID

    
    def getKillerVehicleID(self):
        return self._AvatarInputHandler__killerVehicleID

    
    def start(self):
        game.g_guiResetters.add(self._AvatarInputHandler__onRecreateDevice)
        import aims as aims
        aims.clearState()
        ownVehicle = BigWorld.entity(BigWorld.player().playerVehicleID)
        vehTypeDesc = ownVehicle.typeDescriptor.type
        self._AvatarInputHandler__isSPG = 'SPG' in vehTypeDesc.tags
        self._AvatarInputHandler__isATSPG = 'AT-SPG' in vehTypeDesc.tags
        for control in self._AvatarInputHandler__ctrls.itervalues():
            control.create()
        
        g_cursorDelegator.detachCursor()
        if not self._AvatarInputHandler__curCtrl.isManualBind():
            BigWorld.player().positionControl.bindToVehicle(True)
        
        self._AvatarInputHandler__curCtrl.enable(ctrlState = control_modes.dumpStateEmpty())
        self.onCameraChanged('arcade')
        tmp = self._AvatarInputHandler__curCtrl.getFixedAutorotation()
        if tmp is not None:
            self._AvatarInputHandler__isAutorotation = tmp
            self._AvatarInputHandler__prevModeAutorotation = True
        else:
            self._AvatarInputHandler__isAutorotation = True
            self._AvatarInputHandler__prevModeAutorotation = None
        BigWorld.player().enableOwnVehicleAutorotation(self._AvatarInputHandler__isAutorotation)
        self._AvatarInputHandler__targeting.enable(True)
        self._AvatarInputHandler__isStarted = True
        self._AvatarInputHandler__isGUIVisible = True
        self._AvatarInputHandler__killerVehicleID = None
        arena = BigWorld.player().arena
        arena.onPeriodChange += self._AvatarInputHandler__onArenaStarted
        self._AvatarInputHandler__onArenaStarted(arena.period)

    
    def stop(self):
        self._AvatarInputHandler__isStarted = False
        for control in self._AvatarInputHandler__ctrls.itervalues():
            control.destroy()
        
        BigWorld.player().positionControl.bindToVehicle(False)
        self.onCameraChanged = None
        self._AvatarInputHandler__targeting.enable(False)
        self._AvatarInputHandler__killerVehicleID = None
        game.g_guiResetters.remove(self._AvatarInputHandler__onRecreateDevice)
        BigWorld.player().arena.onPeriodChange -= self._AvatarInputHandler__onArenaStarted

    
    def onControlModeChanged(self, eMode, **args):
        if not (self._AvatarInputHandler__isArenaStarted) and eMode != 'postmortem':
            return None
        player = BigWorld.player()
        ctrl = BattleReplay.g_replayCtrl
        if ctrl.isRecording:
            ctrl.setControlMode(eMode)
        
        ctrlState = self._AvatarInputHandler__curCtrl.dumpState()
        self._AvatarInputHandler__curCtrl.disable()
        prevCtrl = self._AvatarInputHandler__curCtrl
        self._AvatarInputHandler__curCtrl = self._AvatarInputHandler__ctrls[eMode]
        if player is not None:
            if not prevCtrl.isManualBind() and self._AvatarInputHandler__curCtrl.isManualBind():
                player.positionControl.bindToVehicle(False)
            
            if prevCtrl.isManualBind() and not self._AvatarInputHandler__curCtrl.isManualBind():
                player.positionControl.bindToVehicle(True)
            
            if not prevCtrl.isManualBind() and not self._AvatarInputHandler__curCtrl.isManualBind():
                if prevCtrl is self._AvatarInputHandler__curCtrl:
                    player.positionControl.bindToVehicle(False)
                    player.positionControl.bindToVehicle(True)
                
            
        
        if player is not None:
            curFixed = self._AvatarInputHandler__curCtrl.getFixedAutorotation()
            if curFixed is not None:
                if prevCtrl.getFixedAutorotation() is None:
                    self._AvatarInputHandler__prevModeAutorotation = self._AvatarInputHandler__isAutorotation
                
                if self._AvatarInputHandler__isAutorotation != curFixed:
                    self._AvatarInputHandler__isAutorotation = curFixed
                    BigWorld.player().enableOwnVehicleAutorotation(self._AvatarInputHandler__isAutorotation)
                
            elif prevCtrl.getFixedAutorotation() is not None:
                if self._AvatarInputHandler__prevModeAutorotation is None:
                    self._AvatarInputHandler__prevModeAutorotation = True
                
                if self._AvatarInputHandler__isAutorotation != self._AvatarInputHandler__prevModeAutorotation:
                    self._AvatarInputHandler__isAutorotation = self._AvatarInputHandler__prevModeAutorotation
                    BigWorld.player().enableOwnVehicleAutorotation(self._AvatarInputHandler__isAutorotation)
                
                self._AvatarInputHandler__prevModeAutorotation = None
            
        
        cameras.SniperCamera._USE_SWINGING = BigWorld.wg_isSniperModeSwingingEnabled()
        self._AvatarInputHandler__targeting.onRecreateDevice()
        aim = self.aim
        if aim is not None:
            pass
        1
        GUI.mcursor().position = (0, 0)
        self._AvatarInputHandler__curCtrl.setGUIVisible(self._AvatarInputHandler__isGUIVisible)
        self._AvatarInputHandler__curCtrl.enable(ctrlState = ctrlState, **None)
        self.onCameraChanged(eMode)

    
    def getTargeting(self):
        return self._AvatarInputHandler__targeting

    
    def setGUIVisible(self, isVisible):
        self._AvatarInputHandler__isGUIVisible = isVisible
        self._AvatarInputHandler__curCtrl.setGUIVisible(isVisible)

    
    def selectPlayer(self, vehId):
        self._AvatarInputHandler__curCtrl.selectPlayer(vehId)

    
    def onMinimapClicked(self, worldPos):
        self._AvatarInputHandler__curCtrl.onMinimapClicked(worldPos)

    
    def setReloading(self, duration, startTime = None):
        self._AvatarInputHandler__curCtrl.setReloading(duration, startTime)
        if self.aim is not None:
            self.aim.setReloading(duration, startTime)
        

    
    def _readCfg(self):
        sec = ResMgr.openSection(_INPUT_HANDLER_CFG)
        if sec is None:
            LOG_ERROR('can not open <%s>.' % _INPUT_HANDLER_CFG)
            return None
        self._AvatarInputHandler__checkSections(sec)
        return sec

    
    def _AvatarInputHandler__setupCtrls(self, section):
        for (name, desc) in _CTRLS_DESC_MAP.items():
            if (not desc[2] or desc[2]) and constants.IS_DEVELOPMENT:
                if name not in self._AvatarInputHandler__ctrls:
                    if desc[1]:
                        pass
                    1
                    self._AvatarInputHandler__ctrls[name] = section[desc[1]](None, self)
                
            name not in self._AvatarInputHandler__ctrls
        

    
    def _AvatarInputHandler__checkSections(self, section):
        for (name, desc) in _CTRLS_DESC_MAP.items():
            if (desc[1] is None or desc[2]) and not (constants.IS_DEVELOPMENT):
                continue
            
            if not section.has_key(desc[1]):
                LOG_ERROR('Invalid section <%s> in <%s>.' % (desc[1], _INPUT_HANDLER_CFG))
                continue
        

    
    def _AvatarInputHandler__onArenaStarted(self, period, *args):
        if period == ARENA_PERIOD.BATTLE:
            pass
        1
        self._AvatarInputHandler__isArenaStarted = False
        if self._AvatarInputHandler__isGUIVisible:
            pass
        show = self._AvatarInputHandler__isArenaStarted
        if show:
            pass
        self._AvatarInputHandler__curCtrl.showGunMarker2(control_modes.useServerAim())
        self._AvatarInputHandler__curCtrl.showGunMarker(show)

    
    def _AvatarInputHandler__onRecreateDevice(self):
        self._AvatarInputHandler__curCtrl.onRecreateDevice()
        self._AvatarInputHandler__targeting.onRecreateDevice()



class _Targeting:
    
    def __init__(self):
        target = BigWorld.target
        target.selectionFovDegrees = 1
        target.deselectionFovDegrees = 80
        target.maxDistance = 710
        target.skeletonCheckEnabled = True
        BigWorld.target.isEnabled = False
        self._Targeting__mouseMatProv = BigWorld.MouseTargettingMatrix()

    
    def isEnabled(self):
        return BigWorld.target.isEnabled

    
    def getTargetEntity(self):
        return BigWorld.target.entity

    
    def enable(self, flag):
        if flag and not (BigWorld.target.isEnabled):
            BigWorld.target.isEnabled = True
            BigWorld.target.source = self._Targeting__mouseMatProv
        elif not flag:
            BigWorld.target.isEnabled = False
            BigWorld.target.clear()
            BigWorld.target.source = None
        

    
    def onRecreateDevice(self):
        if BigWorld.target.isEnabled:
            BigWorld.target.clear()
        



