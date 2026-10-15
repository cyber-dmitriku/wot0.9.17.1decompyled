# Source Generated with Decompyle++
# File: BattleReplay.pyc (Python 2.6)

import BigWorld
import ResMgr
import Math
import os
import datetime
import Account
import Avatar
import Vehicle
import ArenaType
import Settings
import CommandMapping
import SoundGroups
import constants
import json
import cPickle
import copy
import AreaDestructibles
from gui.Scaleform.utils import functions
from gui.Scaleform.Battle import Battle
import gui.SystemMessages as gui
import gui.Scaleform.CursorDelegator as gui
import Keys
from helpers import EffectsList
from debug_utils import *
from ConnectionManager import connectionManager
from PlayerEvents import g_playerEvents
from gui import VERSION_FILE_PATH
from helpers import i18n
from gui.WindowsManager import g_windowsManager
from messenger.gui import MessengerDispatcher
from PlayerEvents import g_playerEvents
AUTO_RECORD_TEMP_FILENAME = 'temp.wotreplay'
g_replayCtrl = None
REPLAY_TIME_MARK_CLIENT_READY = 0x80000000L
REPLAY_TIME_MARK_REPLAY_FINISHED = 0x80000001L
REPLAY_TIME_MARK_CURRENT_TIME = 0x80000002L

class BattleReplay:
    isPlaying = property((lambda self: self._BattleReplay__replayCtrl.isPlaying))
    isRecording = property((lambda self: self._BattleReplay__replayCtrl.isRecording))
    isClientReady = property((lambda self: self._BattleReplay__replayCtrl.isClientReady))
    isControllingCamera = property((lambda self: self._BattleReplay__replayCtrl.isControllingCamera))
    isOffline = property((lambda self: self._BattleReplay__replayCtrl.isOfflinePlaybackMode))
    isTimeWarpInProgress = property((lambda self: if not self._BattleReplay__replayCtrl.isTimeWarpInProgress:
passself._BattleReplay__timeWarpCleanupCb is not None))
    playerVehicleID = property((lambda self: self._BattleReplay__replayCtrl.playerVehicleID))
    fps = property((lambda self: self._BattleReplay__replayCtrl.fps))
    ping = property((lambda self: self._BattleReplay__replayCtrl.ping))
    isLaggingNow = property((lambda self: self._BattleReplay__replayCtrl.isLaggingNow))
    playbackSpeed = property((lambda self: self._BattleReplay__replayCtrl.playbackSpeed))
    replayContainsGunReloads = property((lambda self: self._BattleReplay__replayCtrl.replayContainsGunReloads))
    
    def __init__(self):
        userPrefs = Settings.g_instance.userPrefs
        if not userPrefs.has_key(Settings.KEY_REPLAY_PREFERENCES):
            userPrefs.write(Settings.KEY_REPLAY_PREFERENCES, '')
            userPrefs[Settings.KEY_REPLAY_PREFERENCES].writeBool('enabled', False)
        
        self._BattleReplay__settings = userPrefs[Settings.KEY_REPLAY_PREFERENCES]
        self._BattleReplay__fileName = None
        self._BattleReplay__replayCtrl = BigWorld.WGReplayController()
        self._BattleReplay__replayCtrl.replayFinishedCallback = self.onReplayFinished
        self._BattleReplay__replayCtrl.controlModeChangedCallback = self.onControlModeChanged
        self._BattleReplay__replayCtrl.ammoButtonPressedCallback = self.onAmmoButtonPressed
        self._BattleReplay__replayCtrl.playerVehicleIDChangedCallback = self.onPlayerVehicleIDChanged
        self._BattleReplay__replayCtrl.clientVersionDiffersCallback = self.onClientVersionDiffers
        self._BattleReplay__replayCtrl.battleChatMessageCallback = self.onBattleChatMessage
        self._BattleReplay__isAutoRecordingEnabled = False
        self._BattleReplay__quitAfterStop = False
        self._BattleReplay__isPlayingPlayList = False
        self._BattleReplay__playList = []
        g_playerEvents.onBattleResultsReceived += self._BattleReplay__onBattleResultsReceived
        g_playerEvents.onAccountBecomePlayer += self._BattleReplay__onAccountBecomePlayer
        self._BattleReplay__playerDatabaseID = 0
        if isinstance(BigWorld.player(), Account.PlayerAccount):
            self._BattleReplay__playerDatabaseID = BigWorld.player().databaseID
        
        self._BattleReplay__playbackSpeedModifiers = (0, 0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8, 16)
        self._BattleReplay__playbackSpeedModifiersStr = ('0', '1/16', '1/8', '1/4', '1/2', '1', '2', '4', '8', '16')
        self._BattleReplay__playbackSpeedIdx = self._BattleReplay__playbackSpeedModifiers.index(1)
        self._BattleReplay__gunWasLockedBeforePause = False
        self._BattleReplay__replayDir = './replays'
        sec = ResMgr.openSection(VERSION_FILE_PATH)
        version = i18n.makeString(sec.readString('appname')) + ' ' + sec.readString('version')
        self._BattleReplay__replayCtrl.clientVersion = version
        if self._BattleReplay__settings.readBool('enabled'):
            self.enableAutoRecordingBattles(True)
        
        self.fastForwardStep = 20
        self._BattleReplay__timeWarpCleanupCb = None
        self._BattleReplay__enableTimeWarp = False

    
    def destroy(self):
        self.stop()
        g_playerEvents.onBattleResultsReceived -= self._BattleReplay__onBattleResultsReceived
        g_playerEvents.onAccountBecomePlayer -= self._BattleReplay__onAccountBecomePlayer
        self.enableAutoRecordingBattles(False)
        self._BattleReplay__replayCtrl.replayFinishedCallback = None
        self._BattleReplay__replayCtrl.controlModeChangedCallback = None
        self._BattleReplay__replayCtrl.clientVersionDiffersCallback = None
        self._BattleReplay__replayCtrl.playerVehicleIDChangedCallback = None
        self._BattleReplay__replayCtrl.battleChatMessageCallback = None
        self._BattleReplay__replayCtrl.ammoButtonPressedCallback = None
        self._BattleReplay__replayCtrl = None
        if self._BattleReplay__timeWarpCleanupCb is not None:
            BigWorld.cancelCallback(self._BattleReplay__timeWarpCleanupCb)
            self._BattleReplay__timeWarpCleanupCb = None
        

    
    def record(self, fileName = None):
        if self.isPlaying:
            return False
        if self.isRecording:
            return self._BattleReplay__fileName == fileName
        if fileName is None:
            
            try:
                fileName = os.path.join(self._BattleReplay__replayDir, AUTO_RECORD_TEMP_FILENAME)
                if not os.path.isdir(self._BattleReplay__replayDir):
                    os.makedirs(self._BattleReplay__replayDir)
            LOG_CURRENT_EXCEPTION()
            return None

        
        if self._BattleReplay__replayCtrl.startRecording(fileName):
            self._BattleReplay__fileName = fileName
            return True
        return False

    
    def play(self, fileName = None):
        if self.isRecording:
            self.stop()
        elif self.isPlaying:
            return self._BattleReplay__fileName == fileName
        if fileName is not None and fileName.rfind('.wotreplaylist') != -1:
            self._BattleReplay__playList = []
            self._BattleReplay__isPlayingPlayList = True
            
            try:
                f = open(fileName)
                s = f.read()
                f.close()
                self._BattleReplay__playList = s.replace('\r\n', '\n').replace('\r', '\n').split('\n')
                fileName = None

        
        if fileName is None:
            if len(self._BattleReplay__playList) == 0:
                return False
            fileName = self._BattleReplay__playList[0]
            self._BattleReplay__playList.pop(0)
            self._BattleReplay__quitAfterStop = len(self._BattleReplay__playList) == 0
        
        if self._BattleReplay__replayCtrl.startPlayback(fileName):
            self._BattleReplay__fileName = fileName
            self._BattleReplay__playbackSpeedIdx = self._BattleReplay__playbackSpeedModifiers.index(1)
            self._BattleReplay__savedPlaybackSpeedIdx = self._BattleReplay__playbackSpeedIdx
            return True
        return False

    
    def stop(self, rewindToTime = None):
        if not (self.isPlaying) and not (self.isRecording):
            return False
        wasPlaying = self.isPlaying
        isOffline = self._BattleReplay__replayCtrl.isOfflinePlaybackMode
        self._BattleReplay__replayCtrl.stop()
        self._BattleReplay__fileName = None
        if wasPlaying:
            if not isOffline:
                connectionManager.onDisconnected += self._BattleReplay__showLoginPage
            
            BigWorld.clearEntitiesAndSpaces()
            BigWorld.disconnect()
            if self._BattleReplay__quitAfterStop:
                BigWorld.quit()
            elif isOffline:
                self._BattleReplay__showLoginPage()
            
        

    
    def autoStartBattleReplay(self):
        fileName = self._BattleReplay__replayCtrl.getAutoStartFileName()
        if fileName != '':
            self._BattleReplay__quitAfterStop = True
            return self.play(fileName)
        return False

    
    def handleKeyEvent(self, isDown, key, mods, isRepeat, event):
        if not self.isPlaying and self.isClientReady:
            return False
        cmdMap = CommandMapping.g_instance
        player = BigWorld.player()
        if not isinstance(player, Avatar.PlayerAvatar):
            return None
        currReplayTime = self._BattleReplay__replayCtrl.getTimeMark(REPLAY_TIME_MARK_CURRENT_TIME)
        isCursorVisible = gui.Scaleform.CursorDelegator.g_cursorDelegator._CursorDelegator__activated
        if mods == 2:
            pass
        1
        fastForwardStep = 2 * 1
        if (key == Keys.KEY_LEFTMOUSE or cmdMap.isFired(CommandMapping.CMD_CM_SHOOT, key)) and isDown and not isCursorVisible:
            if self.isControllingCamera:
                self.onControlModeChanged()
                self._BattleReplay__replayCtrl.isControllingCamera = False
                self._BattleReplay__showInfoMessage('replayFreeCameraActivated')
            else:
                self._BattleReplay__replayCtrl.isControllingCamera = True
                self.onControlModeChanged()
                self._BattleReplay__showInfoMessage('replaySavedCameraActivated')
            return True
        if cmdMap.isFired(CommandMapping.CMD_CM_ALTERNATE_MODE, key) and isDown:
            if self.isControllingCamera:
                return True
        
        if key == Keys.KEY_SPACE and isDown:
            if self._BattleReplay__playbackSpeedIdx > 0:
                self.setPlaybackSpeedIdx(0)
            elif self._BattleReplay__savedPlaybackSpeedIdx != 0:
                pass
            
            not isCursorVisible(self._BattleReplay__playbackSpeedModifiers.index(1))
            return True
        if key == Keys.KEY_DOWNARROW and isDown:
            if self._BattleReplay__playbackSpeedIdx > 0:
                self.setPlaybackSpeedIdx(self._BattleReplay__playbackSpeedIdx - 1)
            
            return True
        if key == Keys.KEY_UPARROW and isDown:
            if self._BattleReplay__playbackSpeedIdx < len(self._BattleReplay__playbackSpeedModifiers) - 1:
                self.setPlaybackSpeedIdx(self._BattleReplay__playbackSpeedIdx + 1)
            
            return True
        if key == Keys.KEY_RIGHTARROW and isDown:
            self._BattleReplay__timeWarp(currReplayTime + fastForwardStep)
            return True
        if key == Keys.KEY_LEFTARROW:
            self._BattleReplay__timeWarp(currReplayTime - fastForwardStep)
            return True
        if key == Keys.KEY_HOME and isDown:
            self._BattleReplay__timeWarp(0)
            return True
        if key == Keys.KEY_END and isDown:
            self._BattleReplay__timeWarp(self._BattleReplay__replayCtrl.getTimeMark(REPLAY_TIME_MARK_REPLAY_FINISHED))
            return True
        if cmdMap.isFiredList(xrange(CommandMapping.CMD_AMMO_CHOICE_1, CommandMapping.CMD_AMMO_CHOICE_0 + 1), key) and isDown:
            return True
        if cmdMap.isFiredList((CommandMapping.CMD_CM_LOCK_TARGET, CommandMapping.CMD_CM_LOCK_TARGET_OFF, CommandMapping.CMD_USE_HORN, CommandMapping.CMD_STOP_UNTIL_FIRE, CommandMapping.CMD_INCREMENT_CRUISE_MODE, CommandMapping.CMD_DECREMENT_CRUISE_MODE, CommandMapping.CMD_MOVE_FORWARD, CommandMapping.CMD_MOVE_FORWARD_SPEC, CommandMapping.CMD_MOVE_BACKWARD, CommandMapping.CMD_CM_POSTMORTEM_NEXT_VEHICLE, CommandMapping.CMD_CM_POSTMORTEM_SELF_VEHICLE), key) and isDown and not isCursorVisible:
            return True
        if (key == Keys.KEY_RETURN or key == Keys.KEY_NUMPADENTER) and isDown:
            return True
        return False

    
    def handleMouseEvent(self, dx, dy, dz):
        if not self.isPlaying and self.isClientReady:
            return False
        player = BigWorld.player()
        if not isinstance(player, Avatar.PlayerAvatar):
            return False
        if self.isControllingCamera:
            if dz != 0:
                return True
        
        return False

    
    def setGunRotatorTargetPoint(self, value):
        self._BattleReplay__replayCtrl.gunRotatorTargetPoint = value

    
    def getGunRotatorTargetPoint(self):
        return self._BattleReplay__replayCtrl.gunRotatorTargetPoint

    
    def setGunMarkerParams(self, diameter, pos, dir):
        self._BattleReplay__replayCtrl.gunMarkerDiameter = diameter
        self._BattleReplay__replayCtrl.gunMarkerPosition = pos
        self._BattleReplay__replayCtrl.gunMarkerDirection = dir

    
    def getGunMarkerParams(self, defaultPos, defaultDir):
        diameter = self._BattleReplay__replayCtrl.gunMarkerDiameter
        dir = self._BattleReplay__replayCtrl.gunMarkerDirection
        pos = self._BattleReplay__replayCtrl.gunMarkerPosition
        if dir == Math.Vector3(0, 0, 0):
            pos = defaultPos
            dir = defaultDir
        
        return (diameter, pos, dir)

    
    def setTurretYaw(self, value):
        self._BattleReplay__replayCtrl.turretYaw = value

    
    def getTurretYaw(self):
        return self._BattleReplay__replayCtrl.turretYaw

    
    def setGunPitch(self, value):
        self._BattleReplay__replayCtrl.gunPitch = value

    
    def getGunPitch(self):
        return self._BattleReplay__replayCtrl.gunPitch

    
    def getGunReloadAmountLeft(self):
        return self._BattleReplay__replayCtrl.getGunReloadAmountLeft()

    
    def setGunReloadTime(self, startTime, duration):
        self._BattleReplay__replayCtrl.setGunReloadTime(startTime, duration)

    
    def getConsumableSlotCooldownAmount(self, idx):
        return self._BattleReplay__replayCtrl.getConsumableSlotCooldownAmount(idx)

    
    def setConsumableSlotCooldown(self, idx, cooldown, addToExistingCooldown):
        self._BattleReplay__replayCtrl.setConsumableSlotCooldown(idx, cooldown, addToExistingCooldown)

    
    def setArenaPeriod(self, value):
        self._BattleReplay__replayCtrl.arenaPeriod = value

    
    def getArenaPeriod(self):
        return self._BattleReplay__replayCtrl.arenaPeriod

    
    def setArenaLength(self, value):
        self._BattleReplay__replayCtrl.arenaLength = value

    
    def getArenaLength(self):
        return self._BattleReplay__replayCtrl.arenaLength

    
    def setPlayerVehicleID(self, vehicleID):
        if vehicleID == 0 and isinstance(BigWorld.player(), Avatar.PlayerAvatar):
            vehicleID = BigWorld.player().playerVehicleID
        
        self._BattleReplay__replayCtrl.playerVehicleID = vehicleID

    
    def setPlaybackSpeedIdx(self, value):
        self._BattleReplay__savedPlaybackSpeedIdx = self._BattleReplay__playbackSpeedIdx
        self._BattleReplay__playbackSpeedIdx = value
        oldSpeed = self._BattleReplay__playbackSpeedModifiers[self._BattleReplay__savedPlaybackSpeedIdx]
        if not oldSpeed == 0:
            pass
        oldQuiet = oldSpeed > 4
        newSpeed = self._BattleReplay__playbackSpeedModifiers[self._BattleReplay__playbackSpeedIdx]
        if not newSpeed == 0:
            pass
        newQuiet = newSpeed > 4
        if oldQuiet != newQuiet:
            SoundGroups.g_instance.enableArenaSounds(not newQuiet)
        
        player = BigWorld.player()
        if newSpeed == 0:
            self._BattleReplay__gunWasLockedBeforePause = player.gunRotator._VehicleGunRotator__isLocked
            player.gunRotator.lock(True)
            self._BattleReplay__showInfoMessage('replayPaused')
        else:
            player.gunRotator.lock(self._BattleReplay__gunWasLockedBeforePause)
            newSpeedStr = self._BattleReplay__playbackSpeedModifiersStr[self._BattleReplay__playbackSpeedIdx]
            self._BattleReplay__showInfoMessage('replaySpeedChange', {
                'speed': newSpeedStr })
        self._BattleReplay__replayCtrl.playbackSpeed = newSpeed
        if newSpeed == 0:
            BigWorld.callback(0, self._BattleReplay__updateAim)
        

    
    def getPlaybackSpeedIdx(self):
        ret = self._BattleReplay__playbackSpeedModifiers.index(self._BattleReplay__replayCtrl.playbackSpeed)
        if ret == -1:
            return self._BattleReplay__playbackSpeedModifiers.index(1)
        return ret

    
    def setControlMode(self, value):
        self._BattleReplay__replayCtrl.controlMode = value

    
    def getControlMode(self):
        return self._BattleReplay__replayCtrl.controlMode

    
    def onClientReady(self):
        if not self.isPlaying or self.isRecording:
            return None
        self._BattleReplay__replayCtrl.playerVehicleID = BigWorld.player().playerVehicleID
        self._BattleReplay__replayCtrl.onClientReady()
        if self.isRecording:
            player = BigWorld.player()
            arena = player.arena
            arenaName = arena.arenaType.geometry
            i = arenaName.find('/')
            if i != -1:
                arenaName = arenaName[i + 1:]
            
            now = datetime.datetime.now()
            now = '%02d.%02d.%04d %02d:%02d:%02d' % (now.day, now.month, now.year, now.hour, now.minute, now.second)
            vehicleName = BigWorld.entities[player.playerVehicleID].typeDescriptor.name
            vehicleName = vehicleName.replace(':', '-')
            vehicles = self._BattleReplay__getArenaVehiclesInfo()
            gameplayID = player.arenaTypeID >> 16
            if not ArenaType.getGameplayName(gameplayID):
                pass
            arenaInfo = {
                'dateTime': now,
                'playerName': player.name,
                'playerID': self._BattleReplay__playerDatabaseID,
                'playerVehicle': vehicleName,
                'mapName': arenaName,
                'mapDisplayName': arena.arenaType.name,
                'gameplayID': gameplayID,
                'vehicles': vehicles }
            self._BattleReplay__replayCtrl.recMapName = arenaName
            self._BattleReplay__replayCtrl.recPlayerVehicleName = vehicleName
            self._BattleReplay__replayCtrl.setArenaInfoStr(json.dumps(arenaInfo))
        else:
            self._BattleReplay__showInfoMessage('replayControlsHelp1')
            self._BattleReplay__showInfoMessage('replayControlsHelp2')
            self._BattleReplay__showInfoMessage('replayControlsHelp3')

    
    def _BattleReplay__getArenaVehiclesInfo(self):
        vehicles = { }
        for (k, v) in BigWorld.player().arena.vehicles.iteritems():
            vehicle = copy.copy(v)
            vehicle['vehicleType'] = v['vehicleType'].name
            del vehicle['accountDBID']
            del vehicle['prebattleID']
            del vehicle['clanDBID']
            del vehicle['isPrebattleCreator']
            del vehicle['isAvatarReady']
            vehicles[k] = vehicle
        
        return vehicles

    
    def onBattleSwfLoaded(self):
        if self.isPlaying:
            self._BattleReplay__replayCtrl.onBattleSwfLoaded()
        

    
    def onCommonSwfLoaded(self):
        self._BattleReplay__enableTimeWarp = False

    
    def onCommonSwfUnloaded(self):
        self._BattleReplay__enableTimeWarp = True

    
    def onReplayFinished(self):
        if self._BattleReplay__isPlayingPlayList:
            self.stop()
            BigWorld.callback(1, self.play)
            return None
        period = self._BattleReplay__replayCtrl.arenaPeriod
        player = BigWorld.player()
        if isinstance(player, Avatar.PlayerAvatar):
            if player.arena.period == constants.ARENA_PERIOD.AFTERBATTLE:
                period = constants.ARENA_PERIOD.AFTERBATTLE
            
        
        if period != constants.ARENA_PERIOD.AFTERBATTLE:
            functions.showInformationDialog('replayStopped', self.stop, ns = 'battle')
        

    
    def onControlModeChanged(self):
        player = BigWorld.player()
        if not (self.isPlaying) or not isinstance(player, Avatar.PlayerAvatar):
            return None
        if not self.isControllingCamera:
            return None
        player.inputHandler.onControlModeChanged(self.getControlMode(), camMatrix = BigWorld.camera().matrix, preferredPos = self.getGunRotatorTargetPoint(), saveZoom = False, saveDist = False)

    
    def onPlayerVehicleIDChanged(self):
        player = BigWorld.player()
        if self.isPlaying and hasattr(player, 'positionControl'):
            player.positionControl.bindToVehicle(self._BattleReplay__replayCtrl.playerVehicleID)
            self.onControlModeChanged()
        

    
    def onAmmoButtonPressed(self, idx):
        player = BigWorld.player()
        if not isinstance(player, Avatar.PlayerAvatar):
            return None
        if self.isPlaying:
            player.onAmmoButtonPressed(idx)
        elif self.isRecording:
            self._BattleReplay__replayCtrl.onAmmoButtonPressed(idx)
        

    
    def onBattleChatMessage(self, messageText, isCurrentPlayer, targetIsCurrentPlayer = False):
        if self.isRecording:
            self._BattleReplay__replayCtrl.onBattleChatMessage(messageText, isCurrentPlayer)
        elif self.isPlaying and not (self.isTimeWarpInProgress):
            MessengerDispatcher.g_instance.battleMessenger.addFormattedMessage(messageText, isCurrentPlayer, targetIsCurrentPlayer)
        

    
    def setFpsPingLag(self, fps, ping, isLaggingNow):
        if self.isPlaying:
            return None
        self._BattleReplay__replayCtrl.fps = fps
        self._BattleReplay__replayCtrl.ping = ping
        self._BattleReplay__replayCtrl.isLaggingNow = isLaggingNow

    
    def onClientVersionDiffers(self):
        g_windowsManager.showLogin()
        functions.showConfirmDialog('replayNotification', self._BattleReplay__onClientVersionConfirmDlgClosed)

    
    def _BattleReplay__onClientVersionConfirmDlgClosed(self, result):
        if result:
            self._BattleReplay__replayCtrl.isWaitingForVersionConfirm = False
        else:
            self.stop()

    
    def registerWotReplayFileExtension(self):
        self._BattleReplay__replayCtrl.registerWotReplayFileExtension()

    
    def enableAutoRecordingBattles(self, enable):
        if self._BattleReplay__isAutoRecordingEnabled == enable:
            return None
        self._BattleReplay__isAutoRecordingEnabled = enable
        if enable:
            g_playerEvents.onAccountBecomePlayer += self._BattleReplay__startAutoRecord
            if isinstance(BigWorld.player(), Account.PlayerAccount):
                self._BattleReplay__startAutoRecord()
            
        else:
            g_playerEvents.onAccountBecomePlayer -= self._BattleReplay__startAutoRecord
            if self.isRecording:
                self.stop()
            

    
    def cancelSaveCurrMessage(self):
        self._BattleReplay__replayCtrl.cancelSaveCurrMessage()

    
    def _BattleReplay__showInfoMessage(self, msg, args = None):
        if not self.isTimeWarpInProgress:
            g_windowsManager.battleWindow.vMsgsPanel.showMessage(msg, args)
        

    
    def _BattleReplay__startAutoRecord(self):
        if self.isPlaying:
            return None
        if self.isRecording:
            BigWorld.callback(0.1, self._BattleReplay__startAutoRecord)
            return None
        self.record()

    
    def _BattleReplay__showLoginPage(self):
        Disconnect = Disconnect
        import gui.Scaleform.Disconnect
        Disconnect.hide()
        g_windowsManager.showLogin()
        connectionManager.onDisconnected -= self._BattleReplay__showLoginPage

    
    def _BattleReplay__updateAim(self):
        if self.getPlaybackSpeedIdx() == 0:
            player = BigWorld.player()
            if isinstance(player, Avatar.PlayerAvatar):
                player.inputHandler.aim._update()
                BigWorld.callback(0, self._BattleReplay__updateAim)
            
        

    
    def _BattleReplay__onBattleResultsReceived(self, isPlayerVehicle, results):
        if isPlayerVehicle:
            results = cPickle.loads(cPickle.dumps(results))
            results = (results, self._BattleReplay__getArenaVehiclesInfo(), BigWorld.player().arena.statistics)
            self._BattleReplay__replayCtrl.setArenaStatisticsStr(json.dumps(results))
        

    
    def _BattleReplay__onAccountBecomePlayer(self):
        player = BigWorld.player()
        if not isinstance(player, Account.PlayerAccount):
            return None
        if player.databaseID is None:
            BigWorld.callback(0.1, self._BattleReplay__onAccountBecomePlayer)
        else:
            self._BattleReplay__playerDatabaseID = player.databaseID

    
    def _BattleReplay__timeWarp(self, time):
        if not (self.isPlaying) or not (self._BattleReplay__enableTimeWarp):
            return None
        EffectsList.g_disableEffects = True
        AreaDestructibles.g_destructiblesManager.forceNoAnimation = True
        if time < self._BattleReplay__replayCtrl.getTimeMark(REPLAY_TIME_MARK_CURRENT_TIME):
            AreaDestructibles.g_destructiblesManager.onBeforeReplayRewind()
        
        if not self._BattleReplay__replayCtrl.beginTimeWarp(time):
            return None
        if self._BattleReplay__timeWarpCleanupCb is None:
            self._BattleReplay__timeWarpCleanupCb = BigWorld.callback(0, self._BattleReplay__cleanupAfterTimeWarp)
            self._BattleReplay__timeWarpCleanupTime = BigWorld.time() + 0.5
        

    
    def _BattleReplay__cleanupAfterTimeWarp(self):
        BigWorld.wg_clearDecals()
        if self._BattleReplay__replayCtrl.isTimeWarpInProgress:
            self._BattleReplay__timeWarpCleanupTime = BigWorld.time() + 0.5
        
        self._BattleReplay__timeWarpCleanupCb = None
        if BigWorld.time() < self._BattleReplay__timeWarpCleanupTime:
            self._BattleReplay__timeWarpCleanupCb = BigWorld.callback(0, self._BattleReplay__cleanupAfterTimeWarp)
        else:
            AreaDestructibles.g_destructiblesManager.onAfterReplayRewind()
            AreaDestructibles.g_destructiblesManager.forceNoAnimation = False
            EffectsList.g_disableEffects = False



