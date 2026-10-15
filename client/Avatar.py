# Source Generated with Decompyle++
# File: Avatar.pyc (Python 2.6)

import BigWorld
import Keys
import Math
import cPickle
import zlib
from functools import partial
import math
import random
import Vehicle
import ClientArena
import AvatarInputHandler
import ProjectileMover
import Settings
import VehicleGunRotator
import constants
import Event
import AreaDestructibles
import CommandMapping
import Weather
import MusicController
import SoundGroups
import AvatarPositionControl
import ResMgr
from debug_utils import LOG_ERROR, LOG_DEBUG
from OfflineMapCreator import g_offlineMapCreator
from gui.BattleContext import g_battleContext
from constants import ARENA_PERIOD, AIMING_MODE, VEHICLE_SETTING, DEVELOPMENT_INFO, SHOT_RESULT
from constants import SERVER_TICK_LENGTH, AUTO_AIM_LOSS_REASON, VEHICLE_MISC_STATUS
from constants import IS_DEVELOPMENT, SCOUT_EVENT_TYPE, DROWN_WARNING_LEVEL
from items import ITEM_TYPE_INDICES, getTypeOfCompactDescr, vehicles
from streamIDs import RangeStreamIDCallbacks, STREAM_ID_CHAT_MAX, STREAM_ID_CHAT_MIN, STREAM_ID_AVATAR_BATTLE_RESULS
from messenger.wrappers import ChatActionWrapper, ChatTargetedActionWrapper
from messenger.gui import MessengerDispatcher
from PlayerEvents import g_playerEvents
from ClientChat import ClientChat
from ChatManager import chatManager
from VehicleAppearance import StippleManager
from helpers import bound_effects
from helpers import DecalMap
from helpers import i18n
from gui import GameInfoPanel
from gui import PlayerBonusesPanel
from gui import IngameSoundNotifications
from gui.WindowsManager import g_windowsManager
from chat_shared import CHAT_ACTIONS, CHAT_COMMANDS
from debug_utils import *
from material_kinds import EFFECT_MATERIALS
from post_processing import g_postProcessing
from Vibroeffects.Controllers.ReloadController import ReloadController as VibroReloadController
from LightFx import LightManager
import AuxiliaryFx
from account_helpers.AccountSettings import AccountSettings
from account_helpers import BattleResultsCache
import physics_shared
import BattleReplay
import HornCooldown
import MapActivities
from physics_shared import computeBarrelLocalPoint
from AvatarInputHandler.control_modes import ArcadeControlMode
import VOIP
import material_kinds
import functools

class _CRUISE_CONTROL_MODE:
    NONE = 0
    FWD25 = 1
    FWD50 = 2
    FWD100 = 3
    BCKW50 = -1
    BCKW100 = -2

_SHOT_WAITING_MAX_TIMEOUT = 0.2
_SHOT_WAITING_MIN_TIMEOUT = 0.12

class PlayerAvatar(BigWorld.Entity, ClientChat):
    _PlayerAvatar__onStreamCompletePredef = {
        STREAM_ID_AVATAR_BATTLE_RESULS: 'receiveBattleResults' }
    isOnArena = property((lambda self: self._PlayerAvatar__isOnArena))
    isVehicleAlive = property((lambda self: self._PlayerAvatar__isVehicleAlive))
    isWaitingForShot = property((lambda self: self._PlayerAvatar__shotWaitingTimerID is not None))
    
    def __init__(self):
        ClientChat.__init__(self)
        self._PlayerAvatar__rangeStreamIDCallbacks = RangeStreamIDCallbacks()
        self._PlayerAvatar__rangeStreamIDCallbacks.addRangeCallback((STREAM_ID_CHAT_MIN, STREAM_ID_CHAT_MAX), '_ClientChat__receiveStreamedData')
        self._PlayerAvatar__prevArenaPeriod = -1

    
    def _PlayerAvatar__onAction(self, action):
        self.onChatShortcut(action)

    
    def onBecomePlayer(self):
        LOG_DEBUG('Avatar.onBecomePlayer()')
        BigWorld.camera(BigWorld.CursorCamera())
        g_hangarSpace = g_hangarSpace
        import gui.Scaleform.utils.HangarSpace
        if g_hangarSpace is not None:
            g_hangarSpace.destroy()
        
        chatManager.switchPlayerProxy(self)
        g_playerEvents.isPlayerEntityChanging = False
        self.arena = ClientArena.ClientArena(self.arenaUniqueID, self.arenaTypeID, self.arenaGuiType, self.arenaExtraData, self.weatherPresetID)
        self.vehicleTypeDescriptor = None
        self.terrainEffects = None
        self.hitTesters = set()
        self.onVehicleEnterWorld = Event.Event()
        self.onVehicleLeaveWorld = Event.Event()
        self.onGunShotChanged = Event.Event()
        self._PlayerAvatar__stepsTillInit = 4
        self._PlayerAvatar__isSpaceInitialized = False
        self._PlayerAvatar__isOnArena = False
        self._PlayerAvatar__isVehicleAlive = True
        self._PlayerAvatar__ownVehicleMProv = Math.WGAdaptiveMatrixProvider()
        m = Math.Matrix()
        m.setIdentity()
        self._PlayerAvatar__ownVehicleMProv.setStaticTransform(m)
        self._PlayerAvatar__lastVehicleSpeeds = (0, 0)
        self._PlayerAvatar__setOwnVehicleMatrixTimerID = None
        self._PlayerAvatar__aimingInfo = [
            0,
            0,
            1,
            0,
            0,
            0,
            1]
        self._PlayerAvatar__ammo = { }
        self._PlayerAvatar__currShellsIdx = None
        self._PlayerAvatar__nextShellsIdx = None
        self._PlayerAvatar__equipment = { }
        self._PlayerAvatar__equipmentFlags = { }
        self._PlayerAvatar__optionalDevices = { }
        self._PlayerAvatar__nextCSlotIdx = 0
        self._PlayerAvatar__fireInVehicle = False
        self._PlayerAvatar__burstShotResult = 0
        self._PlayerAvatar__isForcedGuiControlMode = False
        self._PlayerAvatar__cruiseControlMode = _CRUISE_CONTROL_MODE.NONE
        self._PlayerAvatar__stopUntilFire = False
        self._PlayerAvatar__stopUntilFireStartTime = -1
        self._PlayerAvatar__lastTimeOfKeyDown = -1
        self._PlayerAvatar__lastKeyDown = Keys.KEY_NONE
        self._PlayerAvatar__numSimilarKeyDowns = 0
        self._PlayerAvatar__stippleMgr = StippleManager()
        self._PlayerAvatar__autoAimVehID = 0
        self._PlayerAvatar__shotWaitingTimerID = None
        self._PlayerAvatar__gunReloadCommandWaitEndTime = 0
        self._PlayerAvatar__frags = set()
        self._PlayerAvatar__vehicleToVehicleCollisions = { }
        self._PlayerAvatar__deviceStates = { }
        self._PlayerAvatar__maySeeOtherVehicleDamage = False
        cdWnd = vehicles.HORN_COOLDOWN.WINDOW + vehicles.HORN_COOLDOWN.CLIENT_WINDOW_EXPANSION
        self._PlayerAvatar__hornCooldown = HornCooldown.HornCooldown(cdWnd, vehicles.HORN_COOLDOWN.MAX_SIGNALS)
        BigWorld.wg_setBatchingEnabled(self.arena.arenaType.batchingEnabled)
        g_playerEvents.onAvatarBecomePlayer()
        MusicController.g_musicController.stopAmbient()
        MusicController.g_musicController.play(MusicController.MUSIC_EVENT_COMBAT_LOADING)
        BigWorld.wg_prefetchSpaceZip(self.arena.arenaType.geometryName)
        self._PlayerAvatar__staticCollisionEffectID = None
        self._PlayerAvatar__drownWarningLevel = DROWN_WARNING_LEVEL.SAFE
        BigWorld.wg_clearDecals()

    
    def onBecomeNonPlayer(self):
        LOG_DEBUG('Avatar.onBecomeNonPlayer()')
        chatManager.switchPlayerProxy(None)
        g_playerEvents.onAvatarBecomeNonPlayer()
        self.onVehicleEnterWorld.clear()
        self.onVehicleEnterWorld = None
        self.onVehicleLeaveWorld.clear()
        self.onVehicleLeaveWorld = None
        self._PlayerAvatar__vehicleToVehicleCollisions = None

    
    def handleKeyEvent(self, event):
        return False

    
    def handleKey(self, isDown, key, mods):
        if not self.userSeesWorld():
            return False
        time = BigWorld.time()
        cmdMap = CommandMapping.g_instance
        
        try:
            isDoublePress = False
            if isDown:
                if self._PlayerAvatar__lastTimeOfKeyDown == -1:
                    self._PlayerAvatar__lastTimeOfKeyDown = 0
                
                if key == self._PlayerAvatar__lastKeyDown and time - self._PlayerAvatar__lastTimeOfKeyDown < 0.35:
                    self._PlayerAvatar__numSimilarKeyDowns = self._PlayerAvatar__numSimilarKeyDowns + 1
                    if self._PlayerAvatar__numSimilarKeyDowns == 2:
                        pass
                    1
                    isDoublePress = False
                else:
                    self._PlayerAvatar__numSimilarKeyDowns = 1
                self._PlayerAvatar__lastKeyDown = key
                self._PlayerAvatar__lastTimeOfKeyDown = time
            
            if BigWorld.isKeyDown(Keys.KEY_CAPSLOCK) and isDown and constants.IS_DEVELOPMENT:
                if key == Keys.KEY_ESCAPE:
                    self._PlayerAvatar__setVisibleGUI(not (self._PlayerAvatar__isGuiVisible))
                    return True
                if key == Keys.KEY_1:
                    self.base.setDevelopmentFeature('heal', 0)
                    return True
                if key == Keys.KEY_2:
                    self.base.setDevelopmentFeature('reload_gun', 0)
                    return True
                if key == Keys.KEY_3:
                    self.base.setDevelopmentFeature('start_fire', 0)
                    return True
                if key == Keys.KEY_4:
                    self.base.setDevelopmentFeature('explode', 0)
                    return True
                if key == Keys.KEY_5:
                    self.base.setDevelopmentFeature('break_left_track', 0)
                    return True
                if key == Keys.KEY_6:
                    self.base.setDevelopmentFeature('break_right_track', 0)
                    return True
                if key == Keys.KEY_7:
                    self.base.setDevelopmentFeature('destroy_self', True)
                
                if key == Keys.KEY_9:
                    BigWorld.setWatcher('Render/Spots/draw', BigWorld.getWatcher('Render/Spots/draw') == 'false')
                    return True
                if key == Keys.KEY_F:
                    vehicle = BigWorld.entity(self.playerVehicleID)
                    vehicle.filter.enableClientFilters = not (vehicle.filter.enableClientFilters)
                    return True
                if key == Keys.KEY_G:
                    self.moveVehicle(1, True)
                    return True
                if key == Keys.KEY_R:
                    self.base.setDevelopmentFeature('pickup', 0)
                    return True
                if key == Keys.KEY_T:
                    self.base.setDevelopmentFeature('log_tkill_ratings', 0)
                    return True
            
            if constants.IS_DEVELOPMENT and cmdMap.isFired(CommandMapping.CMD_SWITCH_SERVER_MARKER, key) and isDown:
                showServerMarker = not (self.gunRotator.showServerMarker)
                self.enableServerAim(showServerMarker)
                AccountSettings.setSettings('useServerAim', showServerMarker)
                return True
            if cmdMap.isFired(CommandMapping.CMD_TOGGLE_GUI, key) and isDown:
                self._PlayerAvatar__setVisibleGUI(not (self._PlayerAvatar__isGuiVisible))
            
            if constants.IS_DEVELOPMENT and isDown:
                if key == Keys.KEY_B and mods == 0:
                    g_windowsManager.showBotsMenu()
                    return True
                if key == Keys.KEY_H and mods != 0:
                    import Cat as Cat
                    Cat.Tasks.VehicleModels.VehicleModelsObject.switchVisualState()
                    return True
                if key == Keys.KEY_I and mods == 0:
                    import Cat as Cat
                    if Cat.Tasks.ScreenInfo.ScreenInfoObject.getVisible():
                        Cat.Tasks.ScreenInfo.ScreenInfoObject.setVisible(False)
                    else:
                        Cat.Tasks.ScreenInfo.ScreenInfoObject.setVisible(True)
                    return True
            
            if cmdMap.isFired(CommandMapping.CMD_INCREMENT_CRUISE_MODE, key) and isDown and not (self._PlayerAvatar__isForcedGuiControlMode):
                if self._PlayerAvatar__stopUntilFire:
                    self._PlayerAvatar__stopUntilFire = False
                    self._PlayerAvatar__cruiseControlMode = _CRUISE_CONTROL_MODE.NONE
                
                if isDoublePress:
                    newMode = _CRUISE_CONTROL_MODE.FWD100
                else:
                    newMode = self._PlayerAvatar__cruiseControlMode + 1
                    newMode = min(newMode, _CRUISE_CONTROL_MODE.FWD100)
                if newMode != self._PlayerAvatar__cruiseControlMode:
                    self._PlayerAvatar__cruiseControlMode = newMode
                    if not cmdMap.isActiveList((CommandMapping.CMD_MOVE_FORWARD, CommandMapping.CMD_MOVE_FORWARD_SPEC, CommandMapping.CMD_MOVE_BACKWARD)):
                        self.moveVehicle(self.makeVehicleMovementCommandByKeys(), isDown)
                    
                
                self._PlayerAvatar__updateCruiseControlPanel()
                return True
            if cmdMap.isFired(CommandMapping.CMD_DECREMENT_CRUISE_MODE, key) and isDown and not (self._PlayerAvatar__isForcedGuiControlMode):
                if self._PlayerAvatar__stopUntilFire:
                    self._PlayerAvatar__stopUntilFire = False
                    self._PlayerAvatar__cruiseControlMode = _CRUISE_CONTROL_MODE.NONE
                
                if isDoublePress:
                    newMode = _CRUISE_CONTROL_MODE.BCKW100
                else:
                    newMode = self._PlayerAvatar__cruiseControlMode - 1
                    newMode = max(newMode, _CRUISE_CONTROL_MODE.BCKW100)
                if newMode != self._PlayerAvatar__cruiseControlMode:
                    self._PlayerAvatar__cruiseControlMode = newMode
                    if not cmdMap.isActiveList((CommandMapping.CMD_MOVE_FORWARD, CommandMapping.CMD_MOVE_FORWARD_SPEC, CommandMapping.CMD_MOVE_BACKWARD)):
                        self.moveVehicle(self.makeVehicleMovementCommandByKeys(), isDown)
                    
                
                self._PlayerAvatar__updateCruiseControlPanel()
                return True
            if cmdMap.isFiredList((CommandMapping.CMD_MOVE_FORWARD, CommandMapping.CMD_MOVE_FORWARD_SPEC, CommandMapping.CMD_MOVE_BACKWARD), key) and isDown and not (self._PlayerAvatar__isForcedGuiControlMode):
                self._PlayerAvatar__cruiseControlMode = _CRUISE_CONTROL_MODE.NONE
                self._PlayerAvatar__updateCruiseControlPanel()
            
            if cmdMap.isFired(CommandMapping.CMD_STOP_UNTIL_FIRE, key) and isDown and not (self._PlayerAvatar__isForcedGuiControlMode):
                if not self._PlayerAvatar__stopUntilFire:
                    self._PlayerAvatar__stopUntilFire = True
                    self._PlayerAvatar__stopUntilFireStartTime = time
                else:
                    self._PlayerAvatar__stopUntilFire = False
                self.moveVehicle(self.makeVehicleMovementCommandByKeys(), isDown)
                self._PlayerAvatar__updateCruiseControlPanel()
            
            if cmdMap.isFiredList((CommandMapping.CMD_MOVE_FORWARD, CommandMapping.CMD_MOVE_FORWARD_SPEC, CommandMapping.CMD_MOVE_BACKWARD, CommandMapping.CMD_ROTATE_LEFT, CommandMapping.CMD_ROTATE_RIGHT), key):
                if self._PlayerAvatar__stopUntilFire and isDown and not (self._PlayerAvatar__isForcedGuiControlMode):
                    self._PlayerAvatar__stopUntilFire = False
                    self._PlayerAvatar__updateCruiseControlPanel()
                
                if not self._PlayerAvatar__isForcedGuiControlMode:
                    self.moveVehicle(self.makeVehicleMovementCommandByKeys(), isDown)
                
                return True
            if not (self._PlayerAvatar__isForcedGuiControlMode) and cmdMap.isFiredList(xrange(CommandMapping.CMD_AMMO_CHOICE_1, CommandMapping.CMD_AMMO_CHOICE_0 + 1), key) and isDown and mods == 0:
                g_windowsManager.battleWindow.consumablesPanel.handleKey(key)
                return True
            if cmdMap.isFiredList((CommandMapping.CMD_CHAT_SHORTCUT_ATTACK, CommandMapping.CMD_CHAT_SHORTCUT_BACKTOBASE, CommandMapping.CMD_CHAT_SHORTCUT_FOLLOWME, CommandMapping.CMD_CHAT_SHORTCUT_POSITIVE, CommandMapping.CMD_CHAT_SHORTCUT_NEGATIVE, CommandMapping.CMD_CHAT_SHORTCUT_HELPME, CommandMapping.CMD_CHAT_SHORTCUT_RELOAD, CommandMapping.CMD_RADIAL_MENU_SHOW), key) and self._PlayerAvatar__isVehicleAlive:
                g_windowsManager.battleWindow.radialMenu.handleKey(key, isDown, self.inputHandler.aim.offset())
                return True
            if cmdMap.isFired(CommandMapping.CMD_VEHICLE_MARKERS_SHOW_INFO, key):
                g_windowsManager.battleWindow.vMarkersManager.showExtendedInfo(isDown)
                return True
            if key == Keys.KEY_F12 and isDown and mods == 0:
                self._PlayerAvatar__dumpVehicleState()
                return True
            if key == Keys.KEY_F12 and isDown and mods == 2:
                self._PlayerAvatar__reportLag()
                return True
            if cmdMap.isFired(CommandMapping.CMD_USE_HORN, key) and isDown:
                self.useHorn(True)
                return True
            if self.isHornActive() and self.hornMode() != 'oneshot' and not cmdMap.isActive(CommandMapping.CMD_USE_HORN):
                self.useHorn(False)
                return True
            if cmdMap.isFired(CommandMapping.CMD_VOICECHAT_MUTE, key):
                LOG_DEBUG('onVoiceChatPTT', isDown)
                if VOIP.getResponseHandler().channelsMgr.currentChannel:
                    VOIP.getResponseHandler().setMicMute(not isDown)
                
            
            if cmdMap.isFired(CommandMapping.CMD_LOGITECH_SWITCH_VIEW, key) and isDown:
                LOG_DEBUG('LOGITECH SWICH VIEW', isDown)
                LogitechMonitor = LogitechMonitor
                import gui.Scaleform.LogitechMonitor
                LogitechMonitor.onChangeView()
            
            if cmdMap.isFiredList((CommandMapping.CMD_MINIMAP_SIZE_DOWN, CommandMapping.CMD_MINIMAP_SIZE_UP, CommandMapping.CMD_MINIMAP_VISIBLE), key) and isDown:
                g_windowsManager.battleWindow.minimap.handleKey(key)
                return True
            if cmdMap.isFired(CommandMapping.CMD_RELOAD_PARTIAL_CLIP, key) and isDown:
                self.onReloadPartialClipKeyDown()
                return True
        except Exception:
            self.userSeesWorld()
            LOG_CURRENT_EXCEPTION()
            return True

        return False

    
    def set_playerVehicleID(self, prev):
        LOG_DEBUG('Avatar.set_playerVehicleID()', self.playerVehicleID)
        BigWorld.wg_setEntityUnloadable(self.playerVehicleID, True)
        self._PlayerAvatar__onInitStepCompleted()
        ownVehicle = BigWorld.entity(self.playerVehicleID)
        if ownVehicle is not None and ownVehicle.inWorld and not (ownVehicle.isPlayer):
            ownVehicle.isPlayer = True
            self.vehicleTypeDescriptor = ownVehicle.typeDescriptor
            self._PlayerAvatar__onInitStepCompleted()
        

    
    def set_isGunLocked(self, prev):
        if self.isGunLocked:
            self.gunRotator.lock(True)
            if not isinstance(self.inputHandler.ctrl, ArcadeControlMode):
                self.inputHandler.onControlModeChanged('arcade', preferredPos = self.inputHandler.getDesiredShotPoint())
            
        else:
            self.gunRotator.lock(False)

    
    def set_isOwnVehicleContactingWorld(self, prev):
        pass

    
    def targetBlur(self, prevEntity):
        if not isinstance(prevEntity, Vehicle.Vehicle):
            return None
        if self.inputHandler.aim:
            self.inputHandler.aim.clearTarget()
        
        BigWorld.wgDelEdgeDetectEntity(prevEntity)
        if self._PlayerAvatar__maySeeOtherVehicleDamage:
            self.cell.monitorVehicleDamage(0)
            g_windowsManager.battleWindow.damageInfoPanel.hide()
        

    
    def targetFocus(self, entity):
        if not isinstance(entity, Vehicle.Vehicle):
            return None
        if self.inputHandler.aim:
            self.inputHandler.aim.setTarget(entity)
        
        if self._PlayerAvatar__isGuiVisible and entity.isAlive():
            if self.team == entity.publicInfo['team']:
                BigWorld.wgAddEdgeDetectEntity(entity, 2)
            else:
                BigWorld.wgAddEdgeDetectEntity(entity, 1)
            if self._PlayerAvatar__maySeeOtherVehicleDamage:
                self.cell.monitorVehicleDamage(entity.id)
            
        

    
    def reload(self):
        self._PlayerAvatar__reloadGUI()
        self.inputHandler.setReloading(0)

    
    def onEnterWorld(self, prereqs):
        LOG_DEBUG('Avatar.onEnterWorld()')
        list = []
        for p in set(self._PlayerAvatar__prereqs):
            
            try:
                list.append(prereqs[p])
            continue
            except Exception:
                e = None
                LOG_WARNING('Resource is not found', p)
                continue
            

        
        self._PlayerAvatar__prereqs = list
        self.gunRotator = VehicleGunRotator.VehicleGunRotator(self)
        self.positionControl = AvatarPositionControl.AvatarPositionControl(self)
        BigWorld.target.caps(1)
        self._PlayerAvatar__onInitStepCompleted()
        if self.playerVehicleID != 0:
            self.set_playerVehicleID(0)
        
        EdgeDetectColorController = EdgeDetectColorController
        import helpers
        EdgeDetectColorController.g_instance.updateColors()

    
    def onLeaveWorld(self):
        LOG_DEBUG('Avatar.onLeaveWorld()')
        MusicController.g_musicController.onLeaveArena()
        BigWorld.wg_setEntityUnloadable(self.playerVehicleID, False)
        BigWorld.worldDrawEnabled(False)
        BigWorld.wg_enableSpaceBoundFog(False)
        BigWorld.wg_setAmbientReverb('')
        BigWorld.target.clear()
        for v in BigWorld.entities.values():
            if isinstance(v, Vehicle.Vehicle) and v.isStarted:
                self.onVehicleLeaveWorld(v)
                v.stopVisual()
                continue
        
        if self._PlayerAvatar__setOwnVehicleMatrixTimerID is not None:
            BigWorld.cancelCallback(self._PlayerAvatar__setOwnVehicleMatrixTimerID)
            self._PlayerAvatar__setOwnVehicleMatrixTimerID = None
        
        if self._PlayerAvatar__shotWaitingTimerID is not None:
            BigWorld.cancelCallback(self._PlayerAvatar__shotWaitingTimerID)
            self._PlayerAvatar__shotWaitingTimerID = None
        
        
        try:
            self._PlayerAvatar__stippleMgr.destroy()
            self._PlayerAvatar__stippleMgr = None
        except Exception:
            LOG_CURRENT_EXCEPTION()

        
        try:
            self.gunRotator.destroy()
            self.gunRotator = None
        except Exception:
            LOG_CURRENT_EXCEPTION()

        if self._PlayerAvatar__stepsTillInit == 0:
            
            try:
                self._PlayerAvatar__destroyGUI()
                SoundGroups.g_instance.enableArenaSounds(False)
            except Exception:
                LOG_CURRENT_EXCEPTION()
            

        self._PlayerAvatar__stepsTillInit = None
        
        try:
            self._PlayerAvatar__projectileMover.destroy()
            self._PlayerAvatar__projectileMover = None
        except Exception:
            LOG_CURRENT_EXCEPTION()

        
        try:
            self.terrainEffects.destroy()
            self.terrainEffects = None
        except Exception:
            LOG_CURRENT_EXCEPTION()

        
        try:
            self.arena.destroy()
            self.arena = None
        except Exception:
            LOG_CURRENT_EXCEPTION()

        
        try:
            self.positionControl.destroy()
            self.positionControl = None
        except:
            LOG_CURRENT_EXCEPTION()

        
        try:
            for hitTester in self.hitTesters:
                hitTester.releaseBspModel()
        except Exception:
            LOG_CURRENT_EXCEPTION()

        
        try:
            vehicles.g_cache.clearPrereqs()
        except Exception:
            LOG_CURRENT_EXCEPTION()

        AreaDestructibles.clear()

    
    def onKickedFromServer(self, reason, isBan, expiryTime):
        LOG_MX('onKickedFromServer', reason, isBan, expiryTime)
        Disconnect = Disconnect
        import gui.Scaleform.Disconnect
        Disconnect.showKick(reason, isBan, expiryTime)

    
    def onAutoAimVehicleLost(self, lossReason):
        autoAimVehID = self._PlayerAvatar__autoAimVehID
        self._PlayerAvatar__autoAimVehID = 0
        self.inputHandler.setAimingMode(False, AIMING_MODE.TARGET_LOCK)
        self.gunRotator.clientMode = True
        if autoAimVehID and autoAimVehID not in self._PlayerAvatar__frags:
            self.soundNotifications.play('target_lost')
        

    
    def updateVehicleHealth(self, health, isCrewActive):
        rawHealth = health
        health = max(0, health)
        if health > 0:
            pass
        isAlive = isCrewActive
        wasAlive = self._PlayerAvatar__isVehicleAlive
        self._PlayerAvatar__isVehicleAlive = isAlive
        damagePanel = g_windowsManager.battleWindow.damagePanel
        damagePanel.updateHealth(health)
        if self.inputHandler.aim:
            self.inputHandler.aim.setHealth(health)
        
        if not isAlive and wasAlive:
            self.gunRotator.stop()
            if health > 0 and not isCrewActive:
                damagePanel.onCrewDeactivated()
                self.soundNotifications.play('crew_deactivated')
                self._PlayerAvatar__deviceStates = {
                    'crew': 'destroyed' }
            else:
                damagePanel.onVehicleDestroyed()
                self.soundNotifications.play('vehicle_destroyed')
                self._PlayerAvatar__deviceStates = {
                    'vehicle': 'destroyed' }
            battleWindow = g_windowsManager.battleWindow
            battleWindow.consumablesPanel.setDisabled(self._PlayerAvatar__currShellsIdx)
            g_windowsManager.showPostMortem()
            self.inputHandler.activatePostmortem()
            self._PlayerAvatar__cruiseControlMode = _CRUISE_CONTROL_MODE.NONE
            self._PlayerAvatar__updateCruiseControlPanel()
            self._PlayerAvatar__stopUntilFire = False
            if rawHealth <= 0:
                vehicle = BigWorld.entities.get(self.playerVehicleID)
                if vehicle is not None:
                    prevHealth = vehicle.health
                    vehicle.health = rawHealth
                    vehicle.set_health(prevHealth)
                
            
        

    
    def updateVehicleGunReloadTime(self, timeLeft):
        self._PlayerAvatar__gunReloadCommandWaitEndTime = 0
        if timeLeft == 0:
            self.soundNotifications.play('gun_reloaded')
            VibroReloadController()
        elif timeLeft < 0:
            timeLeft = -1
        
        self.inputHandler.setReloading(timeLeft)
        g_windowsManager.battleWindow.consumablesPanel.setCoolDownTime(self._PlayerAvatar__currShellsIdx, timeLeft)

    
    def updateVehicleAmmo(self, compactDescr, quantity, quantityInClip, timeRemaining):
        if not compactDescr:
            self._PlayerAvatar__processEmptyVehicleEquipment()
            return None
        itemTypeIdx = getTypeOfCompactDescr(compactDescr)
        processor = self._PlayerAvatar__updateConsumablesProcessors.get(itemTypeIdx)
        if processor:
            getattr(self, processor)(compactDescr, quantity, quantityInClip, timeRemaining)
        else:
            LOG_WARNING('Not supported item type index', itemTypeIdx)

    _PlayerAvatar__updateConsumablesProcessors = {
        ITEM_TYPE_INDICES['shell']: '_PlayerAvatar__processVehicleAmmo',
        ITEM_TYPE_INDICES['equipment']: '_PlayerAvatar__processVehicleEquipments' }
    
    def updateVehicleOptionalDeviceStatus(self, deviceID, isOn):
        self._PlayerAvatar__processVehicleOptionalDevices(deviceID, isOn)

    
    def updateVehicleMiscStatus(self, code, intArg, floatArg):
        STATUS = VEHICLE_MISC_STATUS
        if code == STATUS.DESTROYED_DEVICE_IS_REPAIRING:
            extraIndex = intArg & 255
            progress = (intArg & 65280) >> 8
            LOG_DEBUG_DEV('DESTROYED_DEVICE_IS_REPAIRING (%s): %s%%, %s sec' % (self.vehicleTypeDescriptor.extras[extraIndex].name, progress, floatArg))
        elif code == STATUS.OTHER_VEHICLE_DAMAGE_VISIBLE:
            prevVal = self._PlayerAvatar__maySeeOtherVehicleDamage
            newVal = bool(intArg)
            self._PlayerAvatar__maySeeOtherVehicleDamage = newVal
            if not prevVal and newVal:
                target = BigWorld.target()
                if target is not None and isinstance(target, Vehicle.Vehicle):
                    self.cell.monitorVehicleDamage(target.id)
                
            
        elif code == STATUS.VEHICLE_IS_OVERTURNED:
            self.updateVehicleDestroyTimer(code, floatArg)
        elif code == STATUS.IN_DEATH_ZONE:
            self.updateVehicleDestroyTimer(code, floatArg)
        elif code == STATUS.VEHICLE_DROWN_WARNING:
            self.updateVehicleDestroyTimer(code, floatArg, intArg)
        elif code == STATUS.IS_OBSERVED_BY_ENEMY:
            if g_windowsManager.battleWindow is not None:
                g_windowsManager.battleWindow.showSixthSenseIndicator(True)
            
        elif code == STATUS.LOADER_INTUITION_WAS_USED:
            self.soundNotifications.play('gun_intuition')
            if g_windowsManager.battleWindow is not None:
                g_windowsManager.battleWindow.vMsgsPanel.showMessage('LOADER_INTUITION_WAS_USED')
            
        elif code == STATUS.HORN_BANNED:
            self._PlayerAvatar__hornCooldown.ban(floatArg)
        

    
    def updateVehicleDestroyTimer(self, code, time, warnLvl = None):
        if g_windowsManager.battleWindow is not None:
            if warnLvl is None:
                if time > 0:
                    g_windowsManager.battleWindow.showVehicleTimer(code, time)
                else:
                    g_windowsManager.battleWindow.hideVehicleTimer(code)
            elif warnLvl == DROWN_WARNING_LEVEL.DANGER:
                g_windowsManager.battleWindow.showVehicleTimer(code, time, 'critical')
            elif warnLvl == DROWN_WARNING_LEVEL.CAUTION:
                g_windowsManager.battleWindow.showVehicleTimer(code, 0, 'warning')
            else:
                g_windowsManager.battleWindow.hideVehicleTimer(code)
        

    
    def updateVehicleSetting(self, code, value):
        consumablesPanel = g_windowsManager.battleWindow.consumablesPanel
        if code == VEHICLE_SETTING.CURRENT_SHELLS:
            idx = self._PlayerAvatar__findIndexInAmmo(value)
            if idx is None:
                LOG_CODEPOINT_WARNING(code, value)
                return None
            if idx == self._PlayerAvatar__currShellsIdx:
                return None
            consumablesPanel.setCurrentShell(idx)
            self._PlayerAvatar__currShellsIdx = idx
            shellDescr = vehicles.getDictDescr(value)
            for (shotIdx, descr) in enumerate(self.vehicleTypeDescriptor.gun['shots']):
                if descr['shell']['id'] == shellDescr['id']:
                    self.vehicleTypeDescriptor.activeGunShotIndex = shotIdx
                    vehicle = BigWorld.entity(self.playerVehicleID)
                    if vehicle is not None:
                        vehicle.typeDescriptor.activeGunShotIndex = shotIdx
                    
                    self.onGunShotChanged()
                    break
                    continue
                idx == self._PlayerAvatar__currShellsIdx
            
            aim = self.inputHandler.aim
            if aim is not None:
                aim.setAmmoStock(*self._PlayerAvatar__ammo[idx][1:3])
            
            return None
        if code == VEHICLE_SETTING.NEXT_SHELLS:
            idx = self._PlayerAvatar__findIndexInAmmo(value)
            if idx is None:
                LOG_CODEPOINT_WARNING(code, value)
                return None
            if idx == self._PlayerAvatar__nextShellsIdx:
                return None
            consumablesPanel.setNextShell(idx)
            self._PlayerAvatar__nextShellsIdx = idx
            return None
        LOG_CODEPOINT_WARNING(code, value)

    
    def updateTargetingInfo(self, turretYaw, gunPitch, maxTurretRotationSpeed, maxGunRotationSpeed, shotDispMultiplierFactor, gunShotDispersionFactorsTurretRotation, chassisShotDispersionFactorsMovement, chassisShotDispersionFactorsRotation, aimingTime):
        aimingInfo = self._PlayerAvatar__aimingInfo
        aimingInfo[2] = shotDispMultiplierFactor
        aimingInfo[3] = gunShotDispersionFactorsTurretRotation
        aimingInfo[4] = chassisShotDispersionFactorsMovement
        aimingInfo[5] = chassisShotDispersionFactorsRotation
        aimingInfo[6] = aimingTime
        self.gunRotator.update(turretYaw, gunPitch, maxTurretRotationSpeed, maxGunRotationSpeed)
        self.getOwnVehicleShotDispersionAngle(self.gunRotator.turretRotationSpeed)

    
    def updateGunMarker(self, shotPos, shotVec, dispersionAngle):
        self.gunRotator.setShotPosition(shotPos, shotVec, dispersionAngle)

    
    def showOwnVehicleHitDirection(self, hitDirYaw, isDamage):
        if self.inputHandler.aim is not None:
            self.inputHandler.aim.showHit(hitDirYaw, isDamage)
        

    
    def showOwnVehicleDamageInfo(self, damageIndex, extraIndex, entityID):
        damageCode = constants.DAMAGE_INFO_CODES[damageIndex]
        if extraIndex != 0:
            pass
        1
        extra = None
        self._PlayerAvatar__showDamageIconAndPlaySound(damageCode, extra)
        self._PlayerAvatar__showVehicleDamageMessage(damageCode, extra, entityID)

    
    def showOtherVehicleDamageInfo(self, vehicleID, damagedExtras, destroyedExtras):
        target = BigWorld.target()
        if target is None or not isinstance(target, Vehicle.Vehicle):
            if self._PlayerAvatar__maySeeOtherVehicleDamage and vehicleID != 0:
                self.cell.monitorVehicleDamage(0)
            
            return None
        if target.id == vehicleID:
            g_windowsManager.battleWindow.damageInfoPanel.show(vehicleID, damagedExtras, destroyedExtras)
            return None
        if self._PlayerAvatar__maySeeOtherVehicleDamage:
            self.cell.monitorVehicleDamage(target.id)
        
        g_windowsManager.battleWindow.damageInfoPanel.hide()

    
    def selectPlayer(self, vehId):
        if self._PlayerAvatar__isForcedGuiControlMode:
            vehicleDesc = self.arena.vehicles.get(vehId)
            if vehicleDesc['isAlive'] and vehicleDesc['team'] == self.team:
                self.inputHandler.selectPlayer(vehId)
            
        

    
    def showDevelopmentInfo(self, code, arg):
        params = cPickle.loads(arg)
        if code == DEVELOPMENT_INFO.BONUSES:
            if constants.IS_DEVELOPMENT:
                if self.playerBonusesPanel is not None:
                    self.playerBonusesPanel.setVisible(True)
                    self.playerBonusesPanel.setContent(params)
                
            
        elif code == DEVELOPMENT_INFO.VISIBILITY:
            if constants.IS_DEVELOPMENT:
                import Cat
                Cat.Tasks.VisibilityTest.VisibilityTestObject.setContent(params)
            
        else:
            LOG_MX('showDevelopmentInfo', code, params)

    
    def showTracer(self, shooterID, shotID, effectsIndex, refStartPoint, velocity, gravity):
        if not self.userSeesWorld():
            return None
        startPoint = refStartPoint
        shooter = BigWorld.entity(shooterID)
        if shooter is not None and shooter.isStarted:
            gunFirePos = Math.Matrix(shooter.appearance.modelsDesc['gun']['model'].node('HP_gunFire')).translation
            if gunFirePos.lengthSquared != 0:
                startPoint = gunFirePos
            
        
        effectsDescr = vehicles.g_cache.shotEffects[effectsIndex]
        isOwnShoot = self.playerVehicleID == shooterID
        self._PlayerAvatar__projectileMover.add(shotID, effectsDescr, gravity, refStartPoint, velocity, startPoint, isOwnShoot, BigWorld.camera().position)

    
    def stopTracer(self, shotID, endPoint):
        if self.userSeesWorld():
            self._PlayerAvatar__projectileMover.hide(shotID, endPoint)
        

    
    def explodeProjectile(self, shotID, effectsIndex, effectMaterialIndex, endPoint, velocityDir):
        if self.userSeesWorld():
            effectsDescr = vehicles.g_cache.shotEffects[effectsIndex]
            effectMaterial = EFFECT_MATERIALS[effectMaterialIndex]
            self._PlayerAvatar__projectileMover.explode(shotID, effectsDescr, effectMaterial, endPoint, velocityDir)
        

    
    def receiveHorn(self, vehicleID, hornID, start):
        vInfo = self.arena.vehicles.get(vehicleID, { })
        user = MessengerDispatcher.g_instance.users.getUser(vInfo.get('accountDBID', 0), vInfo.get('name'))
        if user.isIgnored() and start:
            return None
        vehicle = BigWorld.entities.get(vehicleID)
        if vehicle is not None:
            if start:
                vehicle.playHornSound(hornID)
            else:
                vehicle.stopHornSound()
        

    
    def useHorn(self, start):
        if not (self._PlayerAvatar__isVehicleAlive) or not (self._PlayerAvatar__isOnArena):
            return None
        if self.vehicleTypeDescriptor is None or self.vehicleTypeDescriptor.hornID is None:
            return None
        if start and not self._PlayerAvatar__hornCooldown.ask():
            g_windowsManager.battleWindow.vMsgsPanel.showMessage('HORN_IS_BLOCKED', max(1, self._PlayerAvatar__hornCooldown.banTime()))
            return None
        playerVehicle = BigWorld.entities.get(self.playerVehicleID)
        if playerVehicle is not None:
            if start:
                playerVehicle.playHornSound(playerVehicle.typeDescriptor.hornID)
            else:
                playerVehicle.stopHornSound()
        
        self.base.vehicle_useHorn(start)

    
    def isHornActive(self):
        playerVehicle = BigWorld.entities.get(self.playerVehicleID)
        if playerVehicle is not None:
            return playerVehicle.isHornActive()
        return False

    
    def hornMode(self):
        playerVehicle = BigWorld.entities.get(self.playerVehicleID)
        if playerVehicle is not None:
            return playerVehicle.hornMode
        return ''

    
    def onRoundFinished(self, winnerTeam, reason):
        LOG_MX('onRoundFinished', winnerTeam, reason)

    
    def onKickedFromArena(self, reasonCode):
        LOG_DEBUG('onKickedFromArena', reasonCode)
        g_playerEvents.onKickedFromArena(reasonCode)

    
    def onScoutEvent(self, eventType, reportedID):
        LOG_DEBUG('onScoutEvent, eventType = %s, reportedID = %s' % (eventType, reportedID))
        msgType = ''
        if eventType == SCOUT_EVENT_TYPE.SPOTTED:
            self.complexSoundNotifications.notifyEnemySpotted(reportedID == 0)
            msgType = 'ENEMY_SPOTTED'
        elif eventType == SCOUT_EVENT_TYPE.HIT_ASSIST:
            msgType = 'ENEMY_SPOTTED_HIT'
        elif eventType == SCOUT_EVENT_TYPE.KILL_ASSIST:
            self.soundNotifications.play('enemy_killed')
            msgType = 'ENEMY_SPOTTED_KILLED'
        
        additionalInfo = None
        extra = None
        if reportedID > 0:
            additionalInfo = {
                'entity': g_battleContext.getFullPlayerName(vID = reportedID) }
            extra = (('entity', reportedID),)
        else:
            msgType += '_PLURAL'
        g_windowsManager.battleWindow.pMsgsPanel.showMessage(msgType, additionalInfo, extra)

    
    def updateArena(self, updateType, argStr):
        self.arena.update(updateType, argStr)

    
    def updatePositions(self, indices, positions):
        self.arena.updatePositions(indices, positions)

    
    def makeDenunciation(self, violatorID, topicID, violatorKind):
        if self.denunciationsLeft <= 0:
            return None
        self.denunciationsLeft -= 1
        self.base.makeDenunciation(violatorID, topicID, violatorKind)

    
    def banUnbanUser(self, accountDBID, restrType, banPeriod, reason, isBan):
        reason = reason.encode('utf8')
        self.base.banUnbanUser(accountDBID, restrType, banPeriod, reason, isBan)

    
    def updateOwnVehiclePosition(self, position, direction, speed, rspeed):
        if self._PlayerAvatar__setOwnVehicleMatrixTimerID is not None:
            BigWorld.cancelCallback(self._PlayerAvatar__setOwnVehicleMatrixTimerID)
            self._PlayerAvatar__setOwnVehicleMatrixTimerID = None
        
        m = Math.Matrix()
        m.setRotateYPR(direction)
        m.translation = position
        self._PlayerAvatar__ownVehicleMProv.setStaticTransform(m)
        self._PlayerAvatar__lastVehicleSpeeds = (speed, rspeed)
        BigWorld.wg_setOutAoIEntityParams(self.playerVehicleID, position, direction)
        self._PlayerAvatar__ownVehicleMProv.target = None
        self._PlayerAvatar__setOwnVehicleMatrixTimerID = BigWorld.callback(SERVER_TICK_LENGTH, self._PlayerAvatar__setOwnVehicleMatrixCallback)

    
    def onStreamComplete(self, id, data):
        if BattleReplay.g_replayCtrl.isRecording:
            if id >= STREAM_ID_CHAT_MIN and id <= STREAM_ID_CHAT_MAX:
                BattleReplay.g_replayCtrl.cancelSaveCurrMessage()
            
        
        callback = self._PlayerAvatar__rangeStreamIDCallbacks.getCallbackForStreamID(id)
        if callback is not None:
            getattr(self, callback)(id, data)
            return None
        callback = self._PlayerAvatar__onStreamCompletePredef.get(id, None)
        if callback is not None:
            getattr(self, callback)(True, data)
            return None

    
    def onSpaceLoaded(self):
        LOG_DEBUG('onSpaceLoaded()')
        self._PlayerAvatar__onInitStepCompleted()

    
    def vehicle_onEnterWorld(self, vehicle):
        self._PlayerAvatar__stippleMgr.hideIfExistFor(vehicle)
        if vehicle.id != self.playerVehicleID:
            vehicle.targetCaps = [
                1]
        else:
            LOG_DEBUG('Avatar.vehicle_onEnterWorld(): own vehicle', vehicle.id)
            vehicle.isPlayer = True
            if self._PlayerAvatar__stepsTillInit != 0:
                self.vehicleTypeDescriptor = vehicle.typeDescriptor
                if isinstance(vehicle.filter, BigWorld.WGVehicleFilter2):
                    m = vehicle.filter.bodyMatrix
                else:
                    m = vehicle.matrix
                self._PlayerAvatar__ownVehicleMProv.setStaticTransform(Math.Matrix(m))
                self._PlayerAvatar__onInitStepCompleted()
            else:
                vehicle.typeDescriptor.activeGunShotIndex = self.vehicleTypeDescriptor.activeGunShotIndex
                if self.inputHandler.aim:
                    self.inputHandler.aim.resetVehicleMatrix()
                
        if self._PlayerAvatar__stepsTillInit == 0 and not (vehicle.isStarted):
            vehicle.startVisual()
            self.onVehicleEnterWorld(vehicle)
        

    
    def vehicle_onLeaveWorld(self, vehicle):
        if not vehicle.isStarted:
            return None
        self.onVehicleLeaveWorld(vehicle)
        vehicle.stopVisual()
        model = vehicle.model
        vehicle.model = None
        self._PlayerAvatar__stippleMgr.showFor(vehicle, model)

    
    def onMinimapCellClicked(self, cellIdx):
        if self._PlayerAvatar__isForcedGuiControlMode:
            channelID = chatManager.battleTeamChannelID
            if channelID != 0:
                ClientChat.sendChannelChatCommand(self, chatManager.battleTeamChannelID, CHAT_COMMANDS.ATTENTIONTOCELL, int16Arg = cellIdx)
            
        

    
    def onAmmoButtonPressed(self, idx):
        if not (self._PlayerAvatar__isOnArena) or not (self._PlayerAvatar__isVehicleAlive):
            return None
        if idx == self._PlayerAvatar__currShellsIdx and idx == self._PlayerAvatar__nextShellsIdx:
            return None
        if idx not in self._PlayerAvatar__ammo.keys():
            return None
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isRecording:
            replayCtrl.onAmmoButtonPressed(idx)
        
        (compactDescr, quantity, _) = self._PlayerAvatar__ammo[idx]
        if quantity <= 0:
            return None
        if idx == self._PlayerAvatar__nextShellsIdx:
            code = VEHICLE_SETTING.CURRENT_SHELLS
        else:
            code = VEHICLE_SETTING.NEXT_SHELLS
        self.updateVehicleSetting(code, compactDescr)
        self.base.vehicle_changeSetting(code, compactDescr)

    
    def onEquipmentButtonPressed(self, idx, deviceName = None):
        if not (self._PlayerAvatar__isOnArena) or not (self._PlayerAvatar__isVehicleAlive):
            return None
        if idx not in self._PlayerAvatar__equipment.keys():
            return None
        (compactDescr, quantity, time) = self._PlayerAvatar__equipment[idx]
        if quantity <= 0 and compactDescr == 0 or time > 0:
            return None
        artefact = vehicles.getDictDescr(compactDescr)
        if not (artefact.tags) or artefact.tags & frozenset(('fuel', 'stimulator')):
            return None
        consumablesPanel = g_windowsManager.battleWindow.consumablesPanel
        param = 0
        if artefact.tags & frozenset(('medkit', 'repairkit')):
            entitySuffix = 'Health'
            if deviceName is not None:
                extra = self.vehicleTypeDescriptor.extrasDict[deviceName + entitySuffix]
                param = (extra.index << 16) + artefact.id[1]
            elif artefact.repairAll:
                if len(self._PlayerAvatar__deviceStates) > 0:
                    param = 65536 + artefact.id[1]
                elif 'medkit' in artefact.tags:
                    pass
                
                artefact.tags & frozenset(('fuel', 'stimulator'))('repairkitAllDevicesAreNotDamaged')
                return None
            else:
                vTypeDescr = self.vehicleTypeDescriptor.type
                if 'medkit' in artefact.tags:
                    tagName = 'medkit'
                    enumRoles = {
                        'gunner': 1,
                        'loader': 1,
                        'radioman': 1 }
                    tankmen = []
                    for roles in vTypeDescr.crewRoles:
                        mainRole = roles[0]
                        if mainRole in enumRoles.keys():
                            tankmen.append(mainRole + str(enumRoles[mainRole]))
                            enumRoles[mainRole] += 1
                            continue
                        tankmen.append(mainRole)
                    
                    entityStates = dict.fromkeys(tankmen)
                else:
                    tagName = 'repairkit'
                    entityStates = dict.fromkeys((tuple,)((lambda .0: for device in .0:
device.name[:-len(entitySuffix)])(vTypeDescr.devices)))
                for eName in entityStates.keys():
                    state = self._PlayerAvatar__deviceStates.get(eName, None)
                    entityStates[eName] = state
                
                consumablesPanel.expandEquipmentSlot(idx, tagName, entityStates)
                return None
        deviceName is not None
        if artefact.tags & frozenset(('extinguisher',)):
            if not self._PlayerAvatar__fireInVehicle:
                self._PlayerAvatar__showPlayerError('extinguisherDoesNotActivated', args = {
                    'name': artefact.userString })
                return None
            flag = self._PlayerAvatar__equipmentFlags.get(idx)
            if flag == 1:
                self._PlayerAvatar__showPlayerError('equipmentAlreadyActivated', args = {
                    'name': artefact.userString })
                return None
            param = 65536 + artefact.id[1]
            self._PlayerAvatar__equipmentFlags[idx] = 1
        
        if artefact.tags & frozenset(('trigger',)):
            flag = self._PlayerAvatar__equipmentFlags.get(idx, 0)
            flag ^= 1
            param = (flag << 16) + artefact.id[1]
            self._PlayerAvatar__equipmentFlags[idx] = flag
        
        self.base.vehicle_changeSetting(VEHICLE_SETTING.ACTIVATE_EQUIPMENT, param)

    
    def onDamageIconButtonPressed(self, tag, deviceName):
        for (compactDescr, _, _) in self._PlayerAvatar__equipment.iteritems():
            if compactDescr == 0:
                continue
            
            eDescr = vehicles.getDictDescr(compactDescr)
            if eDescr.tags & frozenset((tag,)):
                self.onEquipmentButtonPressed(idx, deviceName = deviceName)
                return None
        

    
    def onReloadPartialClipKeyDown(self):
        (clipCapacity, _) = self.vehicleTypeDescriptor.gun['clip']
        if clipCapacity > 1 and self._PlayerAvatar__currShellsIdx < len(self._PlayerAvatar__ammo):
            (_, quantity, quantityInClip) = self._PlayerAvatar__ammo[self._PlayerAvatar__currShellsIdx]
            if quantity != 0 and quantityInClip < clipCapacity:
                self.base.vehicle_changeSetting(VEHICLE_SETTING.RELOAD_PARTIAL_CLIP, 0)
            
        

    
    def prerequisites(self):
        if hasattr(self, '_PlayerAvatar__prereqs'):
            return ()
        SoundGroups.g_instance.enableArenaSounds(False)
        self._PlayerAvatar__prereqs = []
        self._PlayerAvatar__fakeModelName = Settings.g_instance.scriptConfig.readString(Settings.KEY_FAKE_MODEL)
        if self._PlayerAvatar__fakeModelName:
            self._PlayerAvatar__prereqs.append(self._PlayerAvatar__fakeModelName)
        else:
            LOG_ERROR("The '%s' is missing or empty in '%s'" % (Settings.KEY_FAKE_MODEL, Settings.g_instance.scriptConfig.name))
        self.terrainEffects = bound_effects.StaticSceneBoundEffects()
        self._PlayerAvatar__projectileMover = ProjectileMover.ProjectileMover()
        self._PlayerAvatar__prereqs += self._PlayerAvatar__initGUI()
        self._PlayerAvatar__prereqs += g_postProcessing.prerequisites()
        return self._PlayerAvatar__prereqs

    
    def initSpace(self):
        if not self._PlayerAvatar__isSpaceInitialized:
            self._PlayerAvatar__applyTimeAndWeatherSettings()
            self._PlayerAvatar__isSpaceInitialized = True
        

    
    def userSeesWorld(self):
        return self._PlayerAvatar__stepsTillInit == 0

    
    def newFakeModel(self):
        return BigWorld.Model(self._PlayerAvatar__fakeModelName)

    
    def leaveArena(self):
        LOG_DEBUG('Avatar.leaveArena')
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isRecording or replayCtrl.isPlaying:
            replayCtrl.stop()
        
        g_playerEvents.isPlayerEntityChanging = True
        g_playerEvents.onPlayerEntityChanging()
        self._PlayerAvatar__setIsOnArena(False)
        self.base.leaveArena()

    
    def setForcedGuiControlMode(self, value, stopVehicle = True, enableAiming = True):
        if self._PlayerAvatar__stepsTillInit == 0:
            if self._PlayerAvatar__isForcedGuiControlMode ^ value:
                self._PlayerAvatar__doSetForcedGuiControlMode(value, enableAiming)
                if not value:
                    flags = self.makeVehicleMovementCommandByKeys()
                    self.moveVehicle(flags, False)
                
            
            if value and stopVehicle:
                self.moveVehicle(0, False)
            
        
        self._PlayerAvatar__isForcedGuiControlMode = value

    
    def enableOwnVehicleAutorotation(self, enable):
        battleWindow = g_windowsManager.battleWindow
        if battleWindow is not None:
            battleWindow.damagePanel.onVehicleAutorotationEnabled(enable)
        
        self.base.vehicle_changeSetting(VEHICLE_SETTING.AUTOROTATION_ENABLED, enable)

    
    def enableServerAim(self, enable):
        self.base.setDevelopmentFeature('server_marker', enable)

    
    def getOwnVehiclePosition(self):
        return Math.Matrix(self._PlayerAvatar__ownVehicleMProv).translation

    
    def getOwnVehicleMatrix(self):
        return self._PlayerAvatar__ownVehicleMProv

    
    def getOwnVehicleSpeeds(self, getInstantaneous = False):
        if self._PlayerAvatar__ownVehicleMProv.target is None:
            return self._PlayerAvatar__lastVehicleSpeeds
        vehicle = BigWorld.entity(self.playerVehicleID)
        if vehicle is None or not (vehicle.isStarted):
            return self._PlayerAvatar__lastVehicleSpeeds
        speedInfo = vehicle.filter.speedInfo.value
        if getInstantaneous:
            speed = speedInfo[2]
            rspeed = speedInfo[3]
        else:
            speed = speedInfo[0]
            rspeed = speedInfo[1]
        (fwdSpeedLimit, bckwdSpeedLimit) = vehicle.typeDescriptor.physics['speedLimits']
        MAX_SPEED_MULTIPLIER = 1.5
        fwdSpeedLimit *= MAX_SPEED_MULTIPLIER
        bckwdSpeedLimit *= MAX_SPEED_MULTIPLIER
        if speed > fwdSpeedLimit:
            speed = fwdSpeedLimit
        elif speed < -bckwdSpeedLimit:
            speed = -bckwdSpeedLimit
        
        rspeedLimit = vehicle.typeDescriptor.physics['rotationSpeedLimit']
        if rspeed > rspeedLimit:
            rspeed = rspeedLimit
        elif rspeed < -rspeedLimit:
            rspeed = -rspeedLimit
        
        return (speed, rspeed)

    
    def getOwnVehicleShotDispersionAngle(self, turretRotationSpeed, withShot = 0):
        descr = self.vehicleTypeDescriptor
        (aimingStartTime, aimingStartFactor, multFactor, gunShotDispersionFactorsTurretRotation, chassisShotDispersionFactorsMovement, chassisShotDispersionFactorsRotation, aimingTime) = self._PlayerAvatar__aimingInfo
        (vehicleSpeed, vehicleRSpeed) = self.getOwnVehicleSpeeds(True)
        vehicleMovementFactor = vehicleSpeed * chassisShotDispersionFactorsMovement
        vehicleMovementFactor *= vehicleMovementFactor
        vehicleRotationFactor = vehicleRSpeed * chassisShotDispersionFactorsRotation
        vehicleRotationFactor *= vehicleRotationFactor
        turretRotationFactor = turretRotationSpeed * gunShotDispersionFactorsTurretRotation
        turretRotationFactor *= turretRotationFactor
        if withShot == 0:
            shotFactor = 0
        elif withShot == 1:
            shotFactor = descr.gun['shotDispersionFactors']['afterShot']
        else:
            shotFactor = descr.gun['shotDispersionFactors']['afterShotInBurst']
        shotFactor *= shotFactor
        idealFactor = vehicleMovementFactor + vehicleRotationFactor + turretRotationFactor + shotFactor
        idealFactor *= descr.miscAttrs['additiveShotDispersionFactor'] ** 2
        idealFactor = multFactor * math.sqrt(1 + idealFactor)
        currTime = BigWorld.time()
        aimingFactor = aimingStartFactor * math.exp((aimingStartTime - currTime) / aimingTime)
        aim = self.inputHandler.aim
        isGunReload = False
        if aim is not None:
            isGunReload = aim.isGunReload()
        
        if aimingFactor < idealFactor:
            aimingFactor = idealFactor
            self._PlayerAvatar__aimingInfo[0] = currTime
            self._PlayerAvatar__aimingInfo[1] = aimingFactor
            if abs(idealFactor - multFactor) < 0.001:
                self.complexSoundNotifications.setAimingEnded(True, isGunReload)
            elif idealFactor / multFactor > 1.1:
                self.complexSoundNotifications.setAimingEnded(False, isGunReload)
            
        elif aimingFactor / multFactor > 1.1:
            self.complexSoundNotifications.setAimingEnded(False, isGunReload)
        
        return descr.gun['shotDispersionAngle'] * aimingFactor

    
    def shoot(self):
        if not self._PlayerAvatar__isOnArena:
            return None
        for (deviceName, stateName) in self._PlayerAvatar__deviceStates.iteritems():
            msgName = self._PlayerAvatar__cantShootCriticals.get(deviceName + '_' + stateName)
            if msgName is not None:
                self._PlayerAvatar__showPlayerError(msgName)
                return None
        
        if self._PlayerAvatar__currShellsIdx is None:
            return None
        if self._PlayerAvatar__ammo[self._PlayerAvatar__currShellsIdx][1] == 0:
            self._PlayerAvatar__showPlayerError(self._PlayerAvatar__cantShootCriticals['no_ammo'])
            return None
        if self.inputHandler.aim and self.inputHandler.aim.isGunReload():
            self._PlayerAvatar__showPlayerError(self._PlayerAvatar__cantShootCriticals['gun_reload'])
            return None
        if self._PlayerAvatar__gunReloadCommandWaitEndTime > BigWorld.time():
            return None
        if self._PlayerAvatar__shotWaitingTimerID is not None:
            return None
        if self.isGunLocked:
            return None
        if self._PlayerAvatar__isOwnBarrelUnderWater():
            self._PlayerAvatar__showPlayerError(self._PlayerAvatar__cantShootCriticals['under_water'])
            return None
        self.base.vehicle_shoot()
        self._PlayerAvatar__startWaitingForShot()
        self._PlayerAvatar__burstShotResult = 0
        if self._PlayerAvatar__stopUntilFire:
            self._PlayerAvatar__stopUntilFire = False
            if BigWorld.time() - self._PlayerAvatar__stopUntilFireStartTime > 60:
                self._PlayerAvatar__cruiseControlMode = _CRUISE_CONTROL_MODE.NONE
            
            self._PlayerAvatar__updateCruiseControlPanel()
            self.moveVehicle(self.makeVehicleMovementCommandByKeys(), True)
        

    _PlayerAvatar__cantShootCriticals = {
        'gun_destroyed': 'cantShootGunDamaged',
        'vehicle_destroyed': 'cantShootVehicleDestroyed',
        'crew_destroyed': 'cantShootCrewInactive',
        'no_ammo': 'cantShootNoAmmo',
        'gun_reload': 'cantShootGunReloading',
        'under_water': 'cantShootUnderWater' }
    
    def playShotResultNotification(self, result, target):
        if result is not None:
            if target.publicInfo.team != self.team:
                severity = self._PlayerAvatar__shotResultSeveritiesForEnemy[result]
            elif result < SHOT_RESULT.MIN_HIT:
                severity = 0
            else:
                severity = 4
                g_windowsManager.battleWindow.pMsgsPanel.showMessage('ALLY_HIT', {
                    'entity': g_battleContext.getFullPlayerName(vID = target.id) }, extra = (('entity', target.id),))
            if severity > self._PlayerAvatar__burstShotResult:
                self._PlayerAvatar__burstShotResult = severity
            
        
        if result is None or self.vehicleTypeDescriptor.gun['burst'][0] == 1:
            severity = self._PlayerAvatar__burstShotResult
            self._PlayerAvatar__burstShotResult = 0
            play = self.soundNotifications.play
            if severity == 1:
                if target is None:
                    pass
                1
                'armor_ricochet_by_player'(None, target.id)
            elif severity == 2:
                if target is None:
                    pass
                1
                'armor_not_pierced_by_player'(None, target.id)
            elif severity == 3:
                if target is None:
                    pass
                1
                'armor_pierced_crit_by_player'(None, target.id)
            elif severity == 5:
                if target is None:
                    pass
                1
                'damage_by_near_explosion_by_player'(None, target.id)
            elif severity == 6:
                if target is None:
                    pass
                1
                'armor_pierced_by_player'(None, target.id)
            elif severity == 7:
                if target is None:
                    pass
                1
                'armor_pierced_crit_by_player'(None, target.id)
            
        

    _PlayerAvatar__shotResultSeveritiesForEnemy = (1, 2, 3, 6, 7, 5)
    
    def playStartedFire(self, target):
        if self.team != target.publicInfo.team:
            self.soundNotifications.play('enemy_fire_started_by_player', target.id)
        

    
    def addBotToArena(self, vehicleTypeName, team):
        compactDescr = vehicles.VehicleDescr(typeName = vehicleTypeName).makeCompactDescr()
        self.base.addBotToArena(compactDescr, team, self.name)

    
    def controlAnotherVehicle(self, vehicleID, callback = None):
        BigWorld.entity(self.playerVehicleID).isPlayer = False
        self.base.controlAnotherVehicle(vehicleID, 1)
        if vehicleID not in BigWorld.entities.keys():
            BigWorld.callback(0.1, partial(self._PlayerAvatar__controlAnotherVehicleWait, vehicleID, callback, 50))
            return None
        BigWorld.callback(1, partial(self._PlayerAvatar__controlAnotherVehicleAfteraction, vehicleID, callback))

    
    def autoAim(self, target):
        if target is None:
            vehID = 0
        elif not isinstance(target, Vehicle.Vehicle):
            vehID = 0
        elif target.publicInfo['team'] == self.team:
            vehID = 0
        elif not target.isAlive():
            vehID = 0
        else:
            vehID = target.id
        if self._PlayerAvatar__autoAimVehID != vehID:
            self._PlayerAvatar__autoAimVehID = vehID
            self.cell.autoAim(vehID)
            if vehID != 0:
                self.inputHandler.setAimingMode(True, AIMING_MODE.TARGET_LOCK)
                self.gunRotator.clientMode = False
                self.soundNotifications.play('target_captured')
            else:
                self.inputHandler.setAimingMode(False, AIMING_MODE.TARGET_LOCK)
                self.gunRotator.clientMode = True
                self.soundNotifications.play('target_unlocked')
        

    
    def handleVehicleCollidedVehicle(self, vehA, vehB, hitPt, time):
        if self._PlayerAvatar__vehicleToVehicleCollisions is None:
            return None
        lastCollisionTime = 0
        key = (vehA, vehB)
        if not self._PlayerAvatar__vehicleToVehicleCollisions.has_key(key):
            key = (vehB, vehA)
        
        if self._PlayerAvatar__vehicleToVehicleCollisions.has_key(key):
            lastCollisionTime = self._PlayerAvatar__vehicleToVehicleCollisions[key]
        
        if time - lastCollisionTime < 0.2:
            return None
        self._PlayerAvatar__vehicleToVehicleCollisions[key] = time
        vehA.showVehicleCollisionEffect(hitPt)

    
    def cancelWaitingForShot(self):
        if self._PlayerAvatar__shotWaitingTimerID is not None:
            BigWorld.cancelCallback(self._PlayerAvatar__shotWaitingTimerID)
            self._PlayerAvatar__shotWaitingTimerID = None
            self.inputHandler.setAimingMode(False, AIMING_MODE.SHOOTING)
            self.gunRotator.targetLastShotPoint = False
        

    
    def moveVehicleByCurrentKeys(self, isKeyDown, forceFlags = 204, forceMask = 0):
        moveFlags = self.makeVehicleMovementCommandByKeys(forceFlags, forceMask)
        self.moveVehicle(moveFlags, isKeyDown)

    
    def receiveBattleResults(self, isSuccess, data):
        LOG_MX('receiveBattleResults', isSuccess)
        if not isSuccess:
            return None
        
        try:
            results = cPickle.loads(zlib.decompress(data))
            BattleResultsCache.save(self.name, results)
            g_playerEvents.onBattleResultsReceived(True, self._PlayerAvatar__convertBattleResultsToOldStyle(results))
            self.base.confirmBattleResultsReceiving()
        except:
            LOG_CURRENT_EXCEPTION()


    
    def _PlayerAvatar__convertBattleResultsToOldStyle(self, results):
        from battle_results_shared import *
        ACHIEVEMENT_INDICES = ACHIEVEMENT_INDICES
        import arena_achievements
        (arenaUniqueID, private, pickled) = results
        oldStyle = { }
        for rec in ('repair', 'credits', 'xp', 'damageDealt', 'shots', 'hits', 'shotsReceived', 'damageReceived', 'capturePoints', 'droppedCapturePoints', 'killerID'):
            oldStyle[rec] = private[VEH_FULL_RESULTS_INDICES[rec]]
        
        (common, players, vehicles) = cPickle.loads(pickled)
        for rec in ('arenaCreateTime', 'arenaTypeID'):
            oldStyle[rec] = common[COMMON_RESULTS_INDICES[rec]]
        
        heroVehicleIDs = []
        achieveIndices = []
        for (vehID, vehRes) in vehicles.iteritems():
            for achieveName in ('warrior', 'invader', 'sniper', 'defender', 'steelwall', 'supporter', 'scout', 'evileye'):
                if ACHIEVEMENT_INDICES[achieveName] in vehRes[VEH_PUBLIC_RESULTS_INDICES['achievements']]:
                    heroVehicleIDs.append(vehID)
                    achieveIndices.append(ACHIEVEMENT_INDICES[achieveName])
                    continue
            
        
        oldStyle['heroVehicleIDs'] = heroVehicleIDs
        oldStyle['achieveIndices'] = achieveIndices
        if common[COMMON_RESULTS_INDICES['winnerTeam']] == private[VEH_FULL_RESULTS_INDICES['team']]:
            oldStyle['isWinner'] = 1
        elif common[COMMON_RESULTS_INDICES['winnerTeam']] == 0:
            oldStyle['isWinner'] = 0
        else:
            oldStyle['isWinner'] = -1
        oldStyle['factors'] = {
            'dailyXPFactor10': private[VEH_FULL_RESULTS_INDICES['dailyXPFactor10']],
            'aogasFactor10': private[VEH_FULL_RESULTS_INDICES['aogasFactor10']] }
        details = private[VEH_FULL_RESULTS_INDICES['details']]
        asDict = VehicleInteractionDetails.fromPacked(details).toDict()
        continue
        oldStyle['killed'] = _[1]
        continue
        oldStyle['spotted'] = _[2]
        continue
        oldStyle['damaged'] = _[3]
        return oldStyle

    
    def _PlayerAvatar__onInitStepCompleted(self):
        LOG_DEBUG('Avatar.__onInitStepCompleted()', self._PlayerAvatar__stepsTillInit)
        if constants.IS_CAT_LOADED:
            if self._PlayerAvatar__stepsTillInit == 0:
                return None
        
        if not self._PlayerAvatar__stepsTillInit > 0:
            raise AssertionError
        self._PlayerAvatar__stepsTillInit -= 1
        if self._PlayerAvatar__stepsTillInit != 0:
            return None
        self.initSpace()
        self._PlayerAvatar__startGUI()
        DecalMap.g_instance.initGroups(1)
        if self._PlayerAvatar__isForcedGuiControlMode:
            self._PlayerAvatar__doSetForcedGuiControlMode(True, True)
        
        self._PlayerAvatar__setOwnVehicleMatrixCallback()
        for v in BigWorld.entities.values():
            if v.inWorld and isinstance(v, Vehicle.Vehicle) and not (v.isStarted):
                v.startVisual()
                self.onVehicleEnterWorld(v)
                continue
            self._PlayerAvatar__stepsTillInit != 0
        
        SoundGroups.g_instance.enableArenaSounds(True)
        SoundGroups.g_instance.applyPreferences()
        MusicController.g_musicController.onEnterArena()
        BigWorld.wg_setUmbraEnabled(self.arena.arenaType.umbraEnabled)
        BigWorld.wg_enableTreeHiding(False)
        BigWorld.wg_enableSpaceBoundFog(True, _boundingBoxAsVector4(self.arena.arenaType.boundingBox), 0.5)
        BigWorld.worldDrawEnabled(True)
        BigWorld.wg_setAmbientReverb(self.arena.arenaType.defaultReverbPreset)
        BigWorld.wg_setWaterTexScale(self.arena.arenaType.waterTexScale)
        BigWorld.wg_setWaterFreqX(self.arena.arenaType.waterFreqX)
        BigWorld.wg_setWaterFreqZ(self.arena.arenaType.waterFreqZ)
        BattleReplay.g_replayCtrl.onClientReady()
        self.base.setClientReady()
        if self.arena.period == ARENA_PERIOD.BATTLE:
            self._PlayerAvatar__setIsOnArena(True)
        
        self.arena.onPeriodChange += self._PlayerAvatar__onArenaPeriodChange
        ownVehicle = BigWorld.entity(self.playerVehicleID)
        if ownVehicle is not None:
            self.updateVehicleHealth(ownVehicle.health, ownVehicle.isCrewActive)
        
        self.cell.autoAim(0)
        g_playerEvents.onAvatarReady()

    
    def bbfog(self, enable, distance):
        BigWorld.wg_enableSpaceBoundFog(enable, _boundingBoxAsVector4(self.arena.arenaType.boundingBox), distance)

    
    def _PlayerAvatar__initGUIConfig(self):
        up = Settings.g_instance.userPrefs
        out = dict()
        out['showFPS'] = True
        out['showPlayerBonuses'] = True
        if up.has_key('showFPS'):
            out['showFPS'] = up.readBool('showFPS')
        else:
            up.writeBool('showFPS', True)
        return out

    
    def _PlayerAvatar__initGUI(self):
        prereqs = []
        self.guiConfig = self._PlayerAvatar__initGUIConfig()
        if not g_offlineMapCreator.Active():
            self.inputHandler = AvatarInputHandler.AvatarInputHandler()
            prereqs += self.inputHandler.prerequisites()
        
        self.gameInfoPanel = None
        if self.guiConfig['showFPS']:
            self.gameInfoPanel = GameInfoPanel.GameInfoPanel()
            prereqs += self.gameInfoPanel.prerequisites()
        
        self.playerBonusesPanel = None
        if self.guiConfig['showPlayerBonuses']:
            self.playerBonusesPanel = PlayerBonusesPanel.PlayerBonusesPanel()
            prereqs += self.playerBonusesPanel.prerequisites()
        
        self.soundNotifications = IngameSoundNotifications.IngameSoundNotifications()
        self.complexSoundNotifications = IngameSoundNotifications.ComplexSoundNotifications(self.soundNotifications)
        return prereqs

    
    def _PlayerAvatar__startGUI(self):
        self.inputHandler.start()
        self.inputHandler.setReloading(-1)
        if self.gameInfoPanel is not None:
            self.gameInfoPanel.start()
        
        if self.playerBonusesPanel is not None:
            self.playerBonusesPanel.start()
            self.playerBonusesPanel.setVisible(False)
        
        self._PlayerAvatar__isGuiVisible = True
        self.arena.onVehicleKilled += self._PlayerAvatar__onArenaVehicleKilled
        MessengerDispatcher.g_instance.onBattleConnect()
        g_battleContext.init()
        battleWindow = g_windowsManager.startBattle()
        self.soundNotifications.start()
        self.subscribeChatAction(self._PlayerAvatar__onUserChatCommand, CHAT_ACTIONS.userChatCommand)

    
    def _PlayerAvatar__destroyGUI(self):
        g_battleContext.fini()
        g_windowsManager.destroyBattle()
        if self.gameInfoPanel is not None:
            self.gameInfoPanel.destroy()
            self.gameInfoPanel = None
        
        if self.playerBonusesPanel is not None:
            self.playerBonusesPanel.destroy()
            self.playerBonusesPanel = None
        
        self.arena.onVehicleKilled -= self._PlayerAvatar__onArenaVehicleKilled
        self.unsubscribeChatAction(self._PlayerAvatar__onUserChatCommand, CHAT_ACTIONS.userChatCommand)
        self.complexSoundNotifications.destroy()
        self.complexSoundNotifications = None
        self.soundNotifications.destroy()
        self.soundNotifications = None
        self.inputHandler.stop()
        self.inputHandler = None

    
    def _PlayerAvatar__reloadGUI(self):
        self._PlayerAvatar__destroyGUI()
        self._PlayerAvatar__initGUI()
        self._PlayerAvatar__startGUI()
        self.setForcedGuiControlMode(True)
        self.setForcedGuiControlMode(False)
        print 'GUI reloaded'

    
    def _PlayerAvatar__setVisibleGUI(self, bool):
        self._PlayerAvatar__isGuiVisible = bool
        Battle = Battle
        import gui.Scaleform.Battle
        if isinstance(g_windowsManager.window, Battle):
            g_windowsManager.window.showAll(bool)
        
        self.inputHandler.setGUIVisible(bool)

    
    def isGuiVisible(self):
        return self._PlayerAvatar__isGuiVisible

    isGuiVisible = property(isGuiVisible)
    
    def _PlayerAvatar__doSetForcedGuiControlMode(self, value, enableAiming):
        self.inputHandler.detachCursor(value, enableAiming)

    
    def makeVehicleMovementCommandByKeys(self, forceFlags = 204, forceMask = 0):
        cmdMap = CommandMapping.g_instance
        flags = 0
        if self._PlayerAvatar__stopUntilFire:
            return flags
        if cmdMap.isActiveList((CommandMapping.CMD_MOVE_FORWARD, CommandMapping.CMD_MOVE_FORWARD_SPEC)):
            flags = 1
        elif cmdMap.isActive(CommandMapping.CMD_MOVE_BACKWARD):
            flags = 2
        elif self._PlayerAvatar__cruiseControlMode >= _CRUISE_CONTROL_MODE.FWD25:
            flags = 1
        elif self._PlayerAvatar__cruiseControlMode <= _CRUISE_CONTROL_MODE.BCKW50:
            flags = 2
        
        if not self._PlayerAvatar__cruiseControlMode == _CRUISE_CONTROL_MODE.FWD50:
            pass
        isOn = self._PlayerAvatar__cruiseControlMode == _CRUISE_CONTROL_MODE.BCKW50
        if isOn:
            flags |= 16
        elif self._PlayerAvatar__cruiseControlMode == _CRUISE_CONTROL_MODE.FWD25:
            flags |= 32
        
        if cmdMap.isActive(CommandMapping.CMD_ROTATE_LEFT):
            flags |= 4
        
        if cmdMap.isActive(CommandMapping.CMD_ROTATE_RIGHT):
            flags |= 8
        
        flags |= forceMask & forceFlags
        flags &= ~forceMask | forceFlags
        return flags

    
    def moveVehicle(self, flags, isKeyDown):
        if not self._PlayerAvatar__isOnArena:
            return None
        cantMove = False
        if self.inputHandler.ctrl.isSelfVehicle():
            for (deviceName, stateName) in self._PlayerAvatar__deviceStates.iteritems():
                msgName = self._PlayerAvatar__cantMoveCriticals.get(deviceName + '_' + stateName)
                if msgName is not None:
                    cantMove = True
                    if isKeyDown:
                        self._PlayerAvatar__showPlayerError(msgName)
                    
                    break
                    continue
            
        
        if not cantMove:
            vehicle = BigWorld.entity(self.playerVehicleID)
            if vehicle is not None and vehicle.isStarted:
                vehicle.showPlayerMovementCommand(flags)
                if flags & 4:
                    pass
                1
                if flags & 8:
                    pass
                1
                rotationDir = 0
                if flags & 2:
                    pass
                1
                if flags & 1:
                    pass
                1
                movementDir = 0
                vehicle.filter.notifyInputKeysDown(movementDir, rotationDir)
                if isKeyDown:
                    self.inputHandler.setAutorotation(True)
                
            
        
        self.base.vehicle_moveWith(flags)

    _PlayerAvatar__cantMoveCriticals = {
        'engine_destroyed': 'cantMoveEngineDamaged',
        'leftTrack_destroyed': 'cantMoveChassisDamaged',
        'rightTrack_destroyed': 'cantMoveChassisDamaged',
        'vehicle_destroyed': 'cantMoveVehicleDestroyed',
        'crew_destroyed': 'cantMoveCrewInactive' }
    
    def _PlayerAvatar__setIsOnArena(self, onArena):
        if self._PlayerAvatar__isOnArena == onArena:
            return None
        self._PlayerAvatar__isOnArena = onArena
        if not onArena:
            self.gunRotator.stop()
        else:
            self.gunRotator.start()
            if not self._PlayerAvatar__isForcedGuiControlMode:
                self.moveVehicle(self.makeVehicleMovementCommandByKeys(), False)
            

    
    def _PlayerAvatar__showPlayerError(self, msgName, args = None):
        g_windowsManager.battleWindow.vErrorsPanel.showMessage(msgName, args)

    
    def _PlayerAvatar__showDamageIconAndPlaySound(self, damageCode, extra):
        damagePanel = g_windowsManager.battleWindow.damagePanel
        consumablesPanel = g_windowsManager.battleWindow.consumablesPanel
        deviceName = None
        deviceState = None
        soundType = None
        if damageCode in self._PlayerAvatar__damageInfoFire:
            extra = self.vehicleTypeDescriptor.extrasDict['fire']
            self._PlayerAvatar__fireInVehicle = damageCode != 'FIRE_STOPPED'
            if self._PlayerAvatar__fireInVehicle:
                pass
            1
            soundType = 'fixed'
            damagePanel.onFireInVehicle(self._PlayerAvatar__fireInVehicle)
        elif damageCode in self._PlayerAvatar__damageInfoCriticals:
            deviceName = extra.name[:-len('Health')]
            if damageCode == 'DEVICE_REPAIRED_TO_CRITICAL':
                deviceState = 'repaired'
                if 'functionalCanMove' in extra.sounds:
                    tracksToCheck = [
                        'leftTrack',
                        'rightTrack']
                    if deviceName in tracksToCheck:
                        tracksToCheck.remove(deviceName)
                    
                    canMove = True
                    for trackName in tracksToCheck:
                        if trackName in self._PlayerAvatar__deviceStates and self._PlayerAvatar__deviceStates[trackName] == 'destroyed':
                            canMove = False
                            break
                            continue
                    
                    if canMove:
                        pass
                    1
                    soundType = 'functional'
                else:
                    soundType = 'functional'
            else:
                deviceState = 'critical'
                soundType = 'critical'
            self._PlayerAvatar__deviceStates[deviceName] = 'critical'
        elif damageCode in self._PlayerAvatar__damageInfoDestructions:
            deviceName = extra.name[:-len('Health')]
            deviceState = 'destroyed'
            soundType = 'destroyed'
            self._PlayerAvatar__deviceStates[deviceName] = 'destroyed'
            vehicle = self.vehicle
            if vehicle is not None:
                vehicle.appearance.executeCriticalHitVibrations(vehicle, extra.name)
            
        elif damageCode in self._PlayerAvatar__damageInfoHealings:
            deviceName = extra.name[:-len('Health')]
            deviceState = 'normal'
            soundType = 'fixed'
            self._PlayerAvatar__deviceStates.pop(deviceName, None)
        
        if deviceState is not None:
            damagePanel.updateState(deviceName, deviceState)
            consumablesPanel.updateExpandedEquipmentSlot(deviceName, deviceState)
        
        if soundType is not None:
            sound = extra.sounds.get(soundType)
            if sound is not None:
                self.soundNotifications.play(sound)
            
        

    _PlayerAvatar__damageInfoCriticals = ('DEVICE_CRITICAL', 'DEVICE_REPAIRED_TO_CRITICAL', 'DEVICE_CRITICAL_AT_SHOT', 'DEVICE_CRITICAL_AT_RAMMING', 'DEVICE_CRITICAL_AT_FIRE', 'ENGINE_CRITICAL_AT_UNLIMITED_RPM')
    _PlayerAvatar__damageInfoDestructions = ('DEVICE_DESTROYED', 'DEVICE_DESTROYED_AT_SHOT', 'DEVICE_DESTROYED_AT_RAMMING', 'DEVICE_DESTROYED_AT_FIRE', 'TANKMAN_HIT', 'TANKMAN_HIT_AT_SHOT', 'ENGINE_DESTROYED_AT_UNLIMITED_RPM')
    _PlayerAvatar__damageInfoHealings = ('DEVICE_REPAIRED', 'TANKMAN_RESTORED', 'FIRE_STOPPED')
    _PlayerAvatar__damageInfoFire = ('FIRE', 'DEVICE_STARTED_FIRE_AT_SHOT', 'DEVICE_STARTED_FIRE_AT_RAMMING', 'FIRE_STOPPED')
    
    def _PlayerAvatar__showVehicleDamageMessage(self, damageCode, extra, entityID):
        if damageCode in self._PlayerAvatar__damageInfoNoMessage:
            return None
        names = {
            'device': '',
            'entity': '' }
        if extra is not None:
            names['device'] = extra.deviceUserString
        
        if entityID:
            vehicleInfo = self.arena.vehicles.get(entityID)
            if vehicleInfo is None:
                LOG_CODEPOINT_WARNING()
                return None
            names['entity'] = g_battleContext.getFullPlayerName(vehicleInfo)
        
        g_windowsManager.battleWindow.vMsgsPanel.showMessage(damageCode, names)

    _PlayerAvatar__damageInfoNoMessage = ('DEVICE_CRITICAL', 'DEVICE_DESTROYED', 'TANKMAN_HIT', 'FIRE')
    
    def _PlayerAvatar__setOwnVehicleMatrixCallback(self):
        self._PlayerAvatar__setOwnVehicleMatrixTimerID = None
        if not self._PlayerAvatar__ownVehicleMProv.target is None:
            raise AssertionError
        vehicle = self.vehicle
        if vehicle is not None and not (vehicle.isDestroyed) and vehicle.isStarted and vehicle.id == self.playerVehicleID:
            if isinstance(vehicle.filter, BigWorld.WGVehicleFilter2):
                self._PlayerAvatar__ownVehicleMProv.target = vehicle.filter.bodyMatrix
            else:
                self._PlayerAvatar__ownVehicleMProv.target = vehicle.matrix
            return None
        self._PlayerAvatar__setOwnVehicleMatrixTimerID = BigWorld.callback(SERVER_TICK_LENGTH, self._PlayerAvatar__setOwnVehicleMatrixCallback)
        self.positionControl.onFollowCameraTick()

    
    def _PlayerAvatar__onArenaVehicleKilled(self, targetID, attackerID, reason):
        if targetID == self.playerVehicleID:
            self.inputHandler.setKillerVehicleID(attackerID)
            if g_windowsManager.battleWindow is not None:
                g_windowsManager.battleWindow.hideVehicleTimer('ALL')
            
            return None
        playerMessagesPanel = g_windowsManager.battleWindow.pMsgsPanel
        if attackerID == self.playerVehicleID:
            targetInfo = self.arena.vehicles.get(targetID)
            if targetInfo is None:
                LOG_CODEPOINT_WARNING()
                return None
            self._PlayerAvatar__frags.add(targetID)
            if targetInfo['team'] != self.team:
                msg = 'player_frag'
                self.soundNotifications.cancel('armor_pierced_by_player', False)
                self.soundNotifications.play('enemy_killed_by_player')
            else:
                msg = 'player_friendly_fire_frag'
                self.soundNotifications.play('ally_killed_by_player')
            playerMessagesPanel.showMessage(msg, {
                'target': g_battleContext.getFullPlayerName(targetInfo) }, extra = (('target', targetID),))
            return None
        targetInfo = self.arena.vehicles.get(targetID)
        attackerInfo = self.arena.vehicles.get(attackerID)
        if targetInfo is None or attackerInfo is None:
            LOG_CODEPOINT_WARNING()
            return None
        targetTeam = targetInfo['team']
        attackerTeam = attackerInfo['team']
        if targetID == attackerID:
            if not g_battleContext.isObserver(targetID):
                if targetTeam == self.team:
                    pass
                1
                msg = 'enemy_suicide'
                playerMessagesPanel.showMessage(msg, {
                    'entity': g_battleContext.getFullPlayerName(targetInfo) }, extra = (('entity', targetID),))
            
            return None
        if attackerTeam == self.team:
            if attackerTeam != targetTeam:
                msg = 'ally_frag'
            else:
                msg = 'ally_friendly_fire_frag'
        elif attackerTeam != targetTeam:
            pass
        
        msg = 'enemy_friendly_fire_frag'
        playerMessagesPanel.showMessage(msg, {
            'target': g_battleContext.getFullPlayerName(targetInfo, showClan = False),
            'attacker': g_battleContext.getFullPlayerName(attackerInfo, showClan = False) }, extra = (('target', targetID), ('attacker', attackerID)))

    
    def _PlayerAvatar__onArenaPeriodChange(self, period, periodEndTime, periodLength, periodAdditionalInfo):
        self._PlayerAvatar__setIsOnArena(period == ARENA_PERIOD.BATTLE)
        if period == ARENA_PERIOD.PREBATTLE and period > self._PlayerAvatar__prevArenaPeriod:
            LightManager.GameLights.startTicks()
            if AuxiliaryFx.g_instance is not None:
                AuxiliaryFx.g_instance.execEffect('startTicksEffect')
            
        
        if period == ARENA_PERIOD.BATTLE and period > self._PlayerAvatar__prevArenaPeriod:
            self.soundNotifications.play('start_battle')
            LightManager.GameLights.roundStarted()
            BigWorld.WGWindowsNotifier.onBattleBeginning()
            if AuxiliaryFx.g_instance is not None:
                AuxiliaryFx.g_instance.execEffect('roundStartedEffect')
            
        
        self._PlayerAvatar__prevArenaPeriod = period

    
    def _PlayerAvatar__onUserChatCommand(self, commandData):
        messenger = MessengerDispatcher.g_instance
        user = messenger.users.getUser(commandData['originator'], commandData['originatorNickName'])
        if not (user.himself) and user.isIgnored():
            LOG_DEBUG('chat command is ignored', dict(commandData))
            return None
        cmd = CHAT_COMMANDS[commandData['data'][0]]
        if cmd == CHAT_COMMANDS.ATTENTIONTOCELL:
            cellIdx = commandData['data'][2]
            g_windowsManager.battleWindow.minimap.markCell(cellIdx, 3)
            cellName = g_windowsManager.battleWindow.minimap.getCellName(cellIdx)
            commandData['data'] = i18n.makeString(cmd.msgText, cellName)
            messenger.currentWindow.addChannelMessage(ChatActionWrapper(**None))
            return None
        self._PlayerAvatar__processUserChatCommand(commandData, cmd, user)

    
    def _PlayerAvatar__processUserChatCommand(self, commandData, cmd, user):
        PUBLIC_ADR_CMDS = [
            CHAT_COMMANDS.ATTACKENEMY,
            CHAT_COMMANDS.SUPPORTMEWITHFIRE,
            CHAT_COMMANDS.POSITIVE,
            CHAT_COMMANDS.NEGATIVE,
            CHAT_COMMANDS.RELOADINGGUN,
            CHAT_COMMANDS.HELPME]
        PRIVATE_ADR_CMDS = [
            CHAT_COMMANDS.TURNBACK,
            CHAT_COMMANDS.FOLLOWME,
            CHAT_COMMANDS.HELPMEEX,
            CHAT_COMMANDS.STOP]
        TARGETED_CMDS = [
            CHAT_COMMANDS.ATTACKENEMY,
            CHAT_COMMANDS.TURNBACK,
            CHAT_COMMANDS.FOLLOWME,
            CHAT_COMMANDS.HELPMEEX,
            CHAT_COMMANDS.SUPPORTMEWITHFIRE,
            CHAT_COMMANDS.STOP]
        TARGET_TOO_CMDS = [
            CHAT_COMMANDS.ATTACKENEMY,
            CHAT_COMMANDS.SUPPORTMEWITHFIRE]
        vehID = commandData['data'][1]
        isTargeted = cmd in TARGETED_CMDS
        currentIsTarget = vehID == self.playerVehicleID
        canShowTarget = cmd in TARGET_TOO_CMDS
        vmManager = g_windowsManager.battleWindow.vMarkersManager
        if cmd in PRIVATE_ADR_CMDS:
            self._PlayerAvatar__onSenderPrivateUserChatCmd(commandData, cmd, user, vmManager, isTargeted, currentIsTarget)
        else:
            self._PlayerAvatar__playChatSound(cmd)
            if cmd in PUBLIC_ADR_CMDS:
                self._PlayerAvatar__onSenderPublicUserChatCmd(commandData, cmd, user, vmManager, isTargeted, currentIsTarget, canShowTarget)
            else:
                self._PlayerAvatar__onDefaultChat(commandData, cmd, user, vmManager)

    
    def _PlayerAvatar__onSenderPrivateUserChatCmd(self, commandData, cmd, user, vmManager, isTargeted, currentIsTarget):
        (vehicle, senderVehicleId) = self._PlayerAvatar__findNonPlayerVehicleByName(user.uid)
        if currentIsTarget or senderVehicleId == self.playerVehicleID:
            self._PlayerAvatar__playChatSound(cmd)
            vehID = commandData['data'][1]
            self._PlayerAvatar__addChannelMessages(commandData, cmd.msgText, vehID, isTargeted, currentIsTarget)
            if vehicle is None:
                vehicle = BigWorld.entity(self.playerVehicleID)
            
            if vehicle and 'SPG' in vehicle.typeDescriptor.type.tags:
                pass
            1
            spgMod = ''
            self._PlayerAvatar__showVehicleMarkerForVehId(vmManager, senderVehicleId, cmd.vehMarker + spgMod)
            markerName = cmd.get('vehMarker')
            if markerName is not None:
                (vehicle, senderVehicleId) = self._PlayerAvatar__findNonPlayerVehicleByName(user.uid)
                if senderVehicleId:
                    g_windowsManager.battleWindow.minimap.showActionMarker(senderVehicleId, markerName)
                
            
        

    
    def _PlayerAvatar__onSenderPublicUserChatCmd(self, commandData, cmd, user, vmManager, isTargeted, currentIsTarget, canShowTarget):
        vehID = commandData['data'][1]
        self._PlayerAvatar__addChannelMessages(commandData, cmd.msgText, vehID, isTargeted, currentIsTarget)
        (vehicle, senderVehicleId) = self._PlayerAvatar__findNonPlayerVehicleByName(user.uid)
        if vehicle is None:
            vehicle = BigWorld.entity(self.playerVehicleID)
        
        if vehicle and 'SPG' in vehicle.typeDescriptor.type.tags:
            pass
        1
        spgMod = ''
        if canShowTarget:
            g_windowsManager.battleWindow.minimap.showActionMarker(vehID, cmd.vehMarker + spgMod)
            g_windowsManager.battleWindow.minimap.showActionMarker(senderVehicleId, 'attackSender' + spgMod)
        elif senderVehicleId:
            g_windowsManager.battleWindow.minimap.showActionMarker(senderVehicleId, cmd.vehMarker + spgMod)
        
        if canShowTarget:
            self._PlayerAvatar__showVehicleMarkerForVehId(vmManager, senderVehicleId, 'attackSender' + spgMod)
            self._PlayerAvatar__showVehicleMarkerForVehId(vmManager, vehID, cmd.vehMarker + spgMod)
        else:
            self._PlayerAvatar__showVehicleMarkerForVehId(vmManager, senderVehicleId, cmd.vehMarker + spgMod)

    
    def _PlayerAvatar__onDefaultChat(self, commandData, cmd, user, vmManager):
        messenger = MessengerDispatcher.g_instance
        commandData['data'] = i18n.makeString(cmd.msgText)
        messenger.currentWindow.addChannelMessage(ChatActionWrapper(**None))
        markerName = cmd.get('vehMarker')
        if markerName is not None:
            (vehicle, vehicleId) = self._PlayerAvatar__findNonPlayerVehicleByName(user.uid)
            if vehicle is not None:
                vmManager.showActionMarker(vehicle.marker, markerName)
            
            if vehicleId:
                g_windowsManager.battleWindow.minimap.showActionMarker(vehicleId, markerName)
            
        

    
    def _PlayerAvatar__showVehicleMarkerForVehId(self, vmManager, vehId, markerName):
        if vehId != self.playerVehicleID:
            vehicle = BigWorld.entity(vehId)
            if vehicle is not None and vehicle.isStarted:
                vmManager.showActionMarker(vehicle.marker, markerName)
            
        

    
    def _PlayerAvatar__addChannelMessages(self, commandData, msgText, vehID, isTargeted, currentIsTarget):
        vehInfo = self.arena.vehicles.get(vehID)
        messenger = MessengerDispatcher.g_instance
        if isTargeted:
            if currentIsTarget:
                commandData['data'] = {
                    'text': i18n.makeString(msgText),
                    'target': g_battleContext.getFullPlayerName(vData = vehInfo) }
                messenger.currentWindow.addChannelMessage(ChatTargetedActionWrapper(**None), currentIsTarget)
            else:
                commandData['data'] = i18n.makeString(msgText, g_battleContext.getFullPlayerName(vData = vehInfo))
                messenger.currentWindow.addChannelMessage(ChatActionWrapper(**None), currentIsTarget)
        else:
            commandData['data'] = i18n.makeString(msgText)
            messenger.currentWindow.addChannelMessage(ChatActionWrapper(**None))

    
    def _PlayerAvatar__playChatSound(self, cmd):
        DENIED_SND_CMDS = [
            CHAT_COMMANDS.ATTENTIONTOCELL]
        if cmd not in DENIED_SND_CMDS:
            self.soundNotifications.play('chat_shortcut_common_fx')
        

    
    def _PlayerAvatar__findNonPlayerVehicleByName(self, accDBID):
        result = (None, None)
        vehID = g_battleContext.getVehIDByAccDBID(accDBID)
        if vehID:
            vehicle = BigWorld.entities.get(vehID)
            if vehicle is not None:
                if not (vehicle.isStarted) or vehicle.isPlayer:
                    vehicle = None
                
            result = (vehicle, vehID)
        
        return result

    
    def onChatShortcut(self, cmdName):
        if not self._PlayerAvatar__isVehicleAlive:
            return None
        channelID = chatManager.battleTeamChannelID
        if channelID != 0:
            ClientChat.sendChannelChatCommand(self, chatManager.battleTeamChannelID, getattr(CHAT_COMMANDS, cmdName))
        

    
    def onChatShortcutTarget(self, cmdName, targetId):
        if not self._PlayerAvatar__isVehicleAlive:
            return None
        if targetId is None:
            return None
        channelID = chatManager.battleTeamChannelID
        if channelID != 0:
            ClientChat.sendChannelChatCommand(self, chatManager.battleTeamChannelID, getattr(CHAT_COMMANDS, cmdName), int64Arg = targetId)
        

    
    def _PlayerAvatar__startWaitingForShot(self):
        if self._PlayerAvatar__shotWaitingTimerID is not None:
            BigWorld.cancelCallback(self._PlayerAvatar__shotWaitingTimerID)
            self._PlayerAvatar__shotWaitingTimerID = None
        
        timeout = BigWorld.LatencyInfo().value[3] * 0.5
        timeout = min(_SHOT_WAITING_MAX_TIMEOUT, timeout)
        timeout = max(_SHOT_WAITING_MIN_TIMEOUT, timeout)
        self._PlayerAvatar__shotWaitingTimerID = BigWorld.callback(timeout, self._PlayerAvatar__showTimedOutShooting)
        self.inputHandler.setAimingMode(True, AIMING_MODE.SHOOTING)
        self.gunRotator.targetLastShotPoint = True
        self._PlayerAvatar__gunReloadCommandWaitEndTime = BigWorld.time() + 2

    
    def _PlayerAvatar__showTimedOutShooting(self):
        self._PlayerAvatar__shotWaitingTimerID = None
        self.inputHandler.setAimingMode(False, AIMING_MODE.SHOOTING)
        self.gunRotator.targetLastShotPoint = False
        
        try:
            vehicle = BigWorld.entity(self.playerVehicleID)
            if vehicle is not None and vehicle.isStarted:
                gunDescr = vehicle.typeDescriptor.gun
                burstCount = gunDescr['burst'][0]
                if self._PlayerAvatar__currShellsIdx is not None:
                    (totalShots, shotsInClip) = self._PlayerAvatar__ammo[self._PlayerAvatar__currShellsIdx][1:3]
                    if burstCount > totalShots:
                        pass
                    totalShots > 0
                    if 1:
                        burstCount = totalShots
                    
                    if gunDescr['clip'][0] > 1:
                        if burstCount > shotsInClip:
                            pass
                        shotsInClip > 0
                        if 1:
                            burstCount = shotsInClip
                        
                    1
                
                vehicle.showShooting(burstCount, True)
        except Exception:
            LOG_CURRENT_EXCEPTION()


    
    def _PlayerAvatar__findIndexInAmmo(self, compactDescr):
        for (value, _, _) in self._PlayerAvatar__ammo.iteritems():
            if compactDescr == value:
                return idx
        

    
    def _PlayerAvatar__findIndexInEquipment(self, compactDescr):
        for (value, _, _) in self._PlayerAvatar__equipment.iteritems():
            if compactDescr == value:
                return idx
        

    
    def _PlayerAvatar__controlAnotherVehicleWait(self, vehicleID, callback, waitCallsLeft):
        if vehicleID in BigWorld.entities.keys():
            BigWorld.callback(1, partial(self._PlayerAvatar__controlAnotherVehicleAfteraction, vehicleID, callback))
        elif waitCallsLeft <= 1:
            if callback is not None:
                callback()
            
            return None
        BigWorld.callback(0.1, partial(self._PlayerAvatar__controlAnotherVehicleWait, vehicleID, callback, waitCallsLeft - 1))

    
    def _PlayerAvatar__controlAnotherVehicleAfteraction(self, vehicleID, callback):
        vehicle = BigWorld.entity(vehicleID)
        if vehicle is None:
            return None
        vehicle.isPlayer = True
        self._PlayerAvatar__isVehicleAlive = True
        self.playerVehicleID = vehicleID
        self.vehicleTypeDescriptor = vehicle.typeDescriptor
        self.base.controlAnotherVehicle(vehicleID, 2)
        self.gunRotator.clientMode = False
        self.gunRotator.start()
        self.base.setDevelopmentFeature('server_marker', True)
        self.base.setDevelopmentFeature('heal', 0)
        self.base.setDevelopmentFeature('stop_bot', 0)
        self.inputHandler.setKillerVehicleID(None)
        self.inputHandler.onControlModeChanged('arcade')
        if callback is not None:
            callback()
        

    
    def _PlayerAvatar__dumpVehicleState(self):
        matrix = Math.Matrix(self.getOwnVehicleMatrix())
        LOG_NOTE('Arena type: ', self.arena.arenaType.geometryName)
        LOG_NOTE('Vehicle position: ', matrix.translation)
        LOG_NOTE('Vehicle direction (y, p, r): ', (matrix.yaw, matrix.pitch, matrix.roll))
        LOG_NOTE('Vehicle speeds: ', self.getOwnVehicleSpeeds())
        if self.vehicleTypeDescriptor is not None:
            LOG_NOTE('Vehicle type: ', self.vehicleTypeDescriptor.type.name)
            LOG_NOTE('Vehicle turret: ', self.vehicleTypeDescriptor.turret['name'])
            LOG_NOTE('Vehicle gun: ', self.vehicleTypeDescriptor.gun['name'])
        
        LOG_NOTE('Shot point: ', self.gunRotator._VehicleGunRotator__lastShotPoint)

    
    def _PlayerAvatar__reportLag(self):
        msg = 'LAG REPORT\n'
        import time
        t = time.gmtime()
        msg += '\ttime: %d/%0d/%0d %0d:%0d:%0d UTC\n' % t[:6]
        msg += '\tAvatar.id: %d\n' % self.id
        ping = BigWorld.LatencyInfo().value[3] - 0.5 * constants.SERVER_TICK_LENGTH
        ping = max(1, ping * 1000)
        msg += '\tping: %d\n' % ping
        msg += '\tFPS: %d\n' % BigWorld.getFPS()[1]
        numVehs = 0
        numAreaDestrs = 0
        for e in BigWorld.entities.values():
            if type(e) is Vehicle.Vehicle:
                numVehs += 1
                continue
            if type(e) == AreaDestructibles.AreaDestructibles:
                numAreaDestrs += 1
                continue
        
        msg += '\tnum Vehicle: %d\n\tnum AreaDestructibles: %d\n' % (numVehs, numAreaDestrs)
        msg += '\tarena: %s\n' % self.arena.arenaType.geometryName
        msg += '\tposition: ' + str(self.position)
        LOG_NOTE(msg)
        self.base.setDevelopmentFeature('log_lag', True)

    
    def _PlayerAvatar__updateCruiseControlPanel(self):
        damagePanel = g_windowsManager.battleWindow.damagePanel
        if self._PlayerAvatar__stopUntilFire or not (self._PlayerAvatar__isVehicleAlive):
            damagePanel.setCruiseMode(_CRUISE_CONTROL_MODE.NONE)
        else:
            damagePanel.setCruiseMode(self._PlayerAvatar__cruiseControlMode)

    
    def _PlayerAvatar__applyTimeAndWeatherSettings(self, overridePresetID = None):
        presets = self.arena.arenaType.weatherPresets
        weather = Weather.weather()
        if len(presets) == 0 or presets[0].get('name') is None:
            weather.summon('Clear', immediate = True)
            return None
        
        try:
            if overridePresetID is not None:
                pass
            1
            presetID = self.weatherPresetID
            preset = presets[presetID]
            weather.summon(preset['name'], immediate = True)
            hour = preset.get('hour')
            if hour is not None:
                BigWorld.wg_setHourOfDay(float(hour))
            
            fogDensity = preset.get('fogDensity')
            if fogDensity is None:
                fogDensity = weather.getFog()[3]
            else:
                fogDensity = float(fogDensity)
            fogColor = preset.get('fogColor')
            if fogColor is None:
                fogColor = weather.getFog()
            else:
                fogColor = fogColor.split()
                fogColor = (float(fogColor[0]), float(fogColor[1]), float(fogColor[2]))
            weather.fog((fogColor[0], fogColor[1], fogColor[2], fogDensity))
            rain = preset.get('rain')
            if rain is not None:
                weather.rain(rain)
            
            ambientLight = preset.get('ambientLight')
            if ambientLight is not None:
                ambientLight = ambientLight.split()
                if len(ambientLight) == 1:
                    weather.ambient(Math.Vector4(float(ambientLight[0])))
                elif len(ambientLight) >= 3:
                    weather.ambient(Math.Vector4(float(ambientLight[0]), float(ambientLight[1]), float(ambientLight[2]), 1))
                
            
            sunLight = preset.get('sunLight')
            if sunLight is not None:
                sunLight = sunLight.split()
                if len(sunLight) == 1:
                    weather.sun(Math.Vector4(float(sunLight[0])))
                elif len(sunLight) >= 3:
                    weather.sun(Math.Vector4(float(sunLight[0]), float(sunLight[1]), float(sunLight[2]), 1))
                
        except Exception:
            presets[0].get('name') is None
            LOG_CURRENT_EXCEPTION()
            LOG_DEBUG("Weather system's ID was:", self.weatherPresetID)
        except:
            presets[0].get('name') is None


    
    def _PlayerAvatar__processVehicleAmmo(self, compactDescr, quantity, quantityInClip, _):
        consumablesPanel = g_windowsManager.battleWindow.consumablesPanel
        aim = self.inputHandler.aim
        idx = self._PlayerAvatar__findIndexInAmmo(compactDescr)
        if idx is not None:
            prevAmmo = self._PlayerAvatar__ammo.get(idx)
            self._PlayerAvatar__ammo[idx] = (compactDescr, quantity, quantityInClip)
            consumablesPanel.setShellQuantityInSlot(idx, quantity, quantityInClip)
            if idx == self._PlayerAvatar__currShellsIdx:
                if prevAmmo is None:
                    pass
                1
                if quantityInClip > 0 and prevAmmo[2] == 0:
                    pass
                isCassetteReload = quantity == prevAmmo[1]
                if not isCassetteReload:
                    self.getOwnVehicleShotDispersionAngle(self.gunRotator.turretRotationSpeed, 1)
                
                if aim is not None:
                    aim.setAmmoStock(quantity, quantityInClip, clipReloaded = isCassetteReload)
                
            
            return None
        idx = self._PlayerAvatar__nextCSlotIdx
        self._PlayerAvatar__nextCSlotIdx += 1
        self._PlayerAvatar__ammo[idx] = (compactDescr, quantity, quantityInClip)
        shellDescr = vehicles.getDictDescr(compactDescr)
        for (_, shotDescr) in enumerate(self.vehicleTypeDescriptor.gun['shots']):
            if shotDescr['shell']['id'] == shellDescr['id']:
                break
                continue
            idx is not None
        
        (clipCapacity, _) = self.vehicleTypeDescriptor.gun['clip']
        (burst, _) = self.vehicleTypeDescriptor.gun['burst']
        if aim is not None:
            aim.setClipParams(clipCapacity, burst)
        
        consumablesPanel.addShellSlot(idx, quantity, quantityInClip, clipCapacity, shellDescr, shotDescr['piercingPower'])

    
    def _PlayerAvatar__processVehicleEquipments(self, compactDescr, quantity, _, timeRemaining):
        consumablesPanel = g_windowsManager.battleWindow.consumablesPanel
        idx = self._PlayerAvatar__findIndexInEquipment(compactDescr)
        if idx is not None:
            self._PlayerAvatar__equipment[idx] = (compactDescr, quantity, timeRemaining)
            if not timeRemaining and quantity > 0 and idx in self._PlayerAvatar__equipmentFlags:
                self._PlayerAvatar__equipmentFlags[idx] = 0
            
            consumablesPanel.setItemQuantityInSlot(idx, quantity)
            consumablesPanel.setCoolDownTime(idx, timeRemaining)
            return None
        self._PlayerAvatar__nextCSlotIdx = consumablesPanel.checkEquipmentSlotIdx(self._PlayerAvatar__nextCSlotIdx)
        idx = self._PlayerAvatar__nextCSlotIdx
        self._PlayerAvatar__nextCSlotIdx += 1
        self._PlayerAvatar__equipment[idx] = (compactDescr, quantity, timeRemaining)
        eDescr = vehicles.getDictDescr(compactDescr)
        consumablesPanel.addEquipmentSlot(idx, quantity, eDescr)
        if timeRemaining:
            consumablesPanel.setCoolDownTime(idx, timeRemaining)
            if eDescr.tags & frozenset(('trigger', 'extinguisher')):
                self._PlayerAvatar__equipmentFlags[idx] = 1
            
        

    
    def _PlayerAvatar__processEmptyVehicleEquipment(self):
        consumablesPanel = g_windowsManager.battleWindow.consumablesPanel
        self._PlayerAvatar__nextCSlotIdx = consumablesPanel.checkEquipmentSlotIdx(self._PlayerAvatar__nextCSlotIdx)
        idx = self._PlayerAvatar__nextCSlotIdx
        self._PlayerAvatar__nextCSlotIdx += 1
        self._PlayerAvatar__equipment[idx] = (0, 0, 0)
        consumablesPanel.addEmptyEquipmentSlot(idx)

    
    def _PlayerAvatar__processVehicleOptionalDevices(self, deviceID, isOn):
        consumablesPanel = g_windowsManager.battleWindow.consumablesPanel
        idx = self._PlayerAvatar__optionalDevices.get(deviceID)
        if idx is None:
            idx = self._PlayerAvatar__nextCSlotIdx
            self._PlayerAvatar__nextCSlotIdx += 1
            self._PlayerAvatar__optionalDevices[deviceID] = idx
            consumablesPanel.addOptionalDevice(idx, vehicles.g_cache.optionalDevices()[deviceID])
        
        consumablesPanel.setOptionalDeviceState(idx, isOn)

    
    def _PlayerAvatar__isOwnBarrelUnderWater(self):
        if self.vehicle is None:
            return None
        turretYaw = Math.Matrix(self.gunRotator.turretMatrix).yaw
        gunPitch = Math.Matrix(self.gunRotator.gunMatrix).pitch
        lp = computeBarrelLocalPoint(self.vehicleTypeDescriptor, turretYaw, gunPitch)
        wp = Math.Matrix(self.vehicle.matrix).applyPoint(lp)
        up = Math.Vector3((0, 0.1, 0))
        return BigWorld.wg_collideWater(wp, wp + up, False) != -1



def preload(alist):
    ds = ResMgr.openSection('precache.xml')
    if ds is not None:
        for sec in ds.values():
            alist.append(sec.asString)
        
    


def _boundingBoxAsVector4(bb):
    return Math.Vector4(bb[0][0], bb[0][1], bb[1][0], bb[1][1])

Avatar = PlayerAvatar

