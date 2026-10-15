# Source Generated with Decompyle++
# File: SettingsInterface.pyc (Python 2.6)

import BigWorld
import SoundGroups
import ResMgr
import ArenaType
import sys
from gui import GUI_SETTINGS
from gui.GraphicsPresets import GraphicsPresets
from gui.GraphicsResolutions import g_graficsResolutions
from gui.Scaleform.utils.key_mapping import getScaleformKey, getBigworldKey, getBigworldNameFromKey
from messenger import g_settings as messenger_settings
from windows import UIInterface
from debug_utils import LOG_DEBUG, LOG_NOTE, LOG_CURRENT_EXCEPTION, LOG_ERROR
from account_helpers.AccountSettings import AccountSettings
from post_processing import g_postProcessing
from functools import partial
import CommandMapping
import Settings
from adisp import process
from gui.Scaleform import VoiceChatInterface
from gui.Scaleform.Waiting import Waiting
from Vibroeffects import VibroManager
from LogitechMonitor import LogitechMonitor

class SettingsInterface(UIInterface):
    KEYBOARD_MAPPING_COMMANDS = {
        'movement': {
            'forward': 'CMD_MOVE_FORWARD',
            'backward': 'CMD_MOVE_BACKWARD',
            'left': 'CMD_ROTATE_LEFT',
            'right': 'CMD_ROTATE_RIGHT',
            'auto_rotation': 'CMD_CM_VEHICLE_SWITCH_AUTOROTATION' },
        'cruis_control': {
            'forward': 'CMD_INCREMENT_CRUISE_MODE',
            'backward': 'CMD_DECREMENT_CRUISE_MODE',
            'stop_fire': 'CMD_STOP_UNTIL_FIRE' },
        'firing': {
            'fire': 'CMD_CM_SHOOT',
            'lock_target': 'CMD_CM_LOCK_TARGET',
            'lock_target_off': 'CMD_CM_LOCK_TARGET_OFF',
            'alternate_mode': 'CMD_CM_ALTERNATE_MODE',
            'reloadPartialClip': 'CMD_RELOAD_PARTIAL_CLIP' },
        'vehicle_other': {
            'showHUD': 'CMD_TOGGLE_GUI',
            'showRadialMenu': 'CMD_RADIAL_MENU_SHOW' },
        'equipment': {
            'item01': 'CMD_AMMO_CHOICE_1',
            'item02': 'CMD_AMMO_CHOICE_2',
            'item03': 'CMD_AMMO_CHOICE_3',
            'item04': 'CMD_AMMO_CHOICE_4',
            'item05': 'CMD_AMMO_CHOICE_5',
            'item06': 'CMD_AMMO_CHOICE_6',
            'item07': 'CMD_AMMO_CHOICE_7',
            'item08': 'CMD_AMMO_CHOICE_8' },
        'shortcuts': {
            'attack': 'CMD_CHAT_SHORTCUT_ATTACK',
            'to_base': 'CMD_CHAT_SHORTCUT_BACKTOBASE',
            'positive': 'CMD_CHAT_SHORTCUT_POSITIVE',
            'negative': 'CMD_CHAT_SHORTCUT_NEGATIVE',
            'help_me': 'CMD_CHAT_SHORTCUT_HELPME',
            'reload': 'CMD_CHAT_SHORTCUT_RELOAD' },
        'camera': {
            'camera_up': 'CMD_CM_CAMERA_ROTATE_UP',
            'camera_down': 'CMD_CM_CAMERA_ROTATE_DOWN',
            'camera_left': 'CMD_CM_CAMERA_ROTATE_LEFT',
            'camera_right': 'CMD_CM_CAMERA_ROTATE_RIGHT' },
        'voicechat': {
            'pushToTalk': 'CMD_VOICECHAT_MUTE' },
        'logitech_keyboard': {
            'switch_view': 'CMD_LOGITECH_SWITCH_VIEW' },
        'minimap': {
            'sizeUp': 'CMD_MINIMAP_SIZE_UP',
            'sizeDown': 'CMD_MINIMAP_SIZE_DOWN',
            'visible': 'CMD_MINIMAP_VISIBLE' } }
    KEYBOARD_MAPPING_BLOCKS = {
        'movement': ('forward', 'backward', 'left', 'right', 'auto_rotation'),
        'cruis_control': ('forward', 'backward', 'stop_fire'),
        'firing': ('fire', 'lock_target', 'lock_target_off', 'alternate_mode', 'reloadPartialClip'),
        'vehicle_other': ('showHUD', 'showRadialMenu'),
        'equipment': ('item01', 'item02', 'item03', 'item04', 'item05', 'item06', 'item07', 'item08'),
        'shortcuts': ('attack', 'to_base', 'negative', 'positive', 'help_me', 'reload'),
        'camera': ('camera_up', 'camera_down', 'camera_left', 'camera_right'),
        'voicechat': ('pushToTalk',),
        'logitech_keyboard': ('switch_view',),
        'minimap': ('sizeUp', 'sizeDown', 'visible') }
    KEYBOARD_MAPPING_BLOCKS_ORDER = ('movement', 'cruis_control', 'firing', 'vehicle_other', 'equipment', 'shortcuts', 'camera', 'voicechat', 'minimap', 'logitech_keyboard')
    POPULATE_UI = 'SettingsDialog.PopulateUI'
    APPLY_SETTINGS = 'SettingsDialog.ApplySettings'
    COMMIT_SETTINGS = 'SettingsDialog.CommitSettings'
    DELAY_SETTINGS = 'SettingsDialog.DelaySettings'
    AUTODETECT_QUALITY = 'SettingsDialog.AutodetectQuality'
    CURSOR_VALUES = {
        'mixing': 3,
        'gunTag': 6,
        'centralTag': 8,
        'net': 3,
        'reloader': 0,
        'condition': 0,
        'cassette': 0 }
    SNIPER_VALUES = {
        'snpMixing': 3,
        'snpGunTag': 6,
        'snpCentralTag': 8,
        'snpNet': 3,
        'snpReloader': 0,
        'snpCondition': 0,
        'snpCassette': 0 }
    MARKER_VALUES = {
        'Hp': 4,
        'Name': 3 }
    MARKER_TYPES = [
        'Base',
        'Alt']
    MOUSE_KEYS = {
        'ingame': {
            'arcadeSens': ('arcade', 'sensitivity'),
            'sniperSens': ('sniper', 'sensitivity'),
            'artSens': ('strategic', 'sensitivity'),
            'horInvert': ('arcade', 'horzInvert'),
            'vertInvert': ('arcade', 'vertInvert') },
        'lobby': {
            'arcadeSens': ('arcadeMode/camera', 'sensitivity', 'float'),
            'sniperSens': ('sniperMode/camera', 'sensitivity', 'float'),
            'artSens': ('strategicMode/camera', 'sensitivity', 'float'),
            'horInvert': ('arcadeMode/camera', 'horzInvert', 'bool'),
            'vertInvert': ('arcadeMode/camera', 'vertInvert', 'bool') },
        'default': {
            'arcadeSens': 1,
            'sniperSens': 1,
            'artSens': 1,
            'horInvert': False,
            'vertInvert': False } }
    GAMEPLAY_KEY_FORMAT = 'gameplay_{0:>s}'
    GAMEPLAY_PREFIX = 'gameplay_'
    
    def __init__(self, enableRedefineKeysMode = True):
        UIInterface.__init__(self)
        if not (GUI_SETTINGS.minimapSize) and self.KEYBOARD_MAPPING_BLOCKS.has_key('minimap'):
            del self.KEYBOARD_MAPPING_BLOCKS['minimap']
        
        self._SettingsInterface__enableRedefineKeysMode = enableRedefineKeysMode
        self.graphicsPresets = GraphicsPresets()
        self.resolutions = g_graficsResolutions
        self._SettingsInterface__currentSettings = None
        self._SettingsInterface__settingsUI = None
        if not (GUI_SETTINGS.voiceChat) and self.KEYBOARD_MAPPING_COMMANDS.has_key('voicechat'):
            if self.KEYBOARD_MAPPING_COMMANDS.has_key('voicechat'):
                del self.KEYBOARD_MAPPING_COMMANDS['voicechat']
            
            if self.KEYBOARD_MAPPING_BLOCKS.has_key('voicechat'):
                del self.KEYBOARD_MAPPING_BLOCKS['voicechat']
            
            self.KEYBOARD_MAPPING_BLOCKS_ORDER = list(self.KEYBOARD_MAPPING_BLOCKS_ORDER)
            del self.KEYBOARD_MAPPING_BLOCKS_ORDER[self.KEYBOARD_MAPPING_BLOCKS_ORDER.index('voicechat')]
            self.KEYBOARD_MAPPING_BLOCKS_ORDER = tuple(self.KEYBOARD_MAPPING_BLOCKS_ORDER)
        

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self.uiHolder.addExternalCallbacks({
            SettingsInterface.POPULATE_UI: self.onPopulateUI,
            SettingsInterface.APPLY_SETTINGS: self.onApplySettings,
            SettingsInterface.COMMIT_SETTINGS: self.onCommitSettings,
            SettingsInterface.DELAY_SETTINGS: self.onDelaySettings,
            SettingsInterface.AUTODETECT_QUALITY: self.onAutodetectSettings,
            'SettingsDialog.useRedifineKeysMode': self.onUseRedifineKeyMode,
            'SettingsDialog.processVivoxTest': self.onProcessVivoxTest,
            'SettingsDialog.voiceChatEnable': self.onVoiceChatEnable,
            'SettingsDialog.updateCaptureDevices': self.onUpdateCaptureDevices,
            'SettingsDialog.setVivoxMicVolume': self.onSetVivoxMicVolume,
            'SettingsDialog.killDialog': self.onDialogClose })
        VibroManager.g_instance.onConnect += self._SettingsInterface__vm_onConnect
        VibroManager.g_instance.onDisconnect += self._SettingsInterface__vm_onDisconnect
        g_guiResetters = g_guiResetters
        import game
        g_guiResetters.add(self.onRecreateDevice)
        BigWorld.wg_setAdapterOrdinalNotifyCallback(self.onRecreateDevice)

    
    def dispossessUI(self):
        if self._SettingsInterface__settingsUI:
            self._SettingsInterface__settingsUI.script = None
            self._SettingsInterface__settingsUI = None
        
        self.uiHolder.removeExternalCallbacks(SettingsInterface.POPULATE_UI, SettingsInterface.APPLY_SETTINGS, SettingsInterface.COMMIT_SETTINGS, SettingsInterface.DELAY_SETTINGS, SettingsInterface.AUTODETECT_QUALITY, 'SettingsDialog.useRedifineKeysMode', 'SettingsDialog.processVivoxTest', 'SettingsDialog.voiceChatEnable', 'SettingsDialog.updateCaptureDevices', 'SettingsDialog.setVivoxMicVolume', 'SettingsDialog.killDialog')
        VibroManager.g_instance.onConnect -= self._SettingsInterface__vm_onConnect
        VibroManager.g_instance.onDisconnect -= self._SettingsInterface__vm_onDisconnect
        g_guiResetters = g_guiResetters
        import game
        g_guiResetters.discard(self.onRecreateDevice)
        BigWorld.wg_setAdapterOrdinalNotifyCallback(None)
        UIInterface.dispossessUI(self)

    
    def _SettingsInterface__isReplayEnabled(self):
        prefs = Settings.g_instance.userPrefs
        
        try:
            return prefs['replayPrefs'].readBool('enabled', False)
        except:
            return False


    
    def _SettingsInterface__setReplayEnabled(self, isEnabled):
        prefs = Settings.g_instance.userPrefs
        
        try:
            prefs['replayPrefs'].writeBool('enabled', isEnabled)
            g_replayCtrl = g_replayCtrl
            import BattleReplay
            g_replayCtrl.enableAutoRecordingBattles(isEnabled)
        except:
            LOG_CURRENT_EXCEPTION()


    
    def onSetVivoxMicVolume(self, callbackId, value):
        import VOIP as VOIP
        if round(SoundGroups.g_instance.getVolume('micVivox') * 100) != value:
            SoundGroups.g_instance.setVolume('micVivox', value / 100)
            VOIP.getResponseHandler().setMicrophoneVolume(int(value))
        

    
    def onVoiceChatEnable(self, callbackId, isEnable):
        self._SettingsInterface__voiceChatEnable(isEnable)

    
    def _SettingsInterface__voiceChatEnable(self, isEnable):
        if isEnable is None:
            return None
        preveVoIP = Settings.g_instance.userPrefs.readBool(Settings.KEY_ENABLE_VOIP)
        import VOIP
        if preveVoIP != isEnable:
            VOIP.getResponseHandler().enable(isEnable)
            Settings.g_instance.userPrefs.writeBool(Settings.KEY_ENABLE_VOIP, bool(isEnable))
            g_windowsManager = g_windowsManager
            import gui.WindowsManager
            if g_windowsManager.battleWindow is not None and not isEnable:
                g_windowsManager.battleWindow.speakingPlayersReset()
            
            LOG_NOTE('Change state of voip: %s' % str(isEnable))
        

    
    def _SettingsInterface__changeCaptureDevice(self, captureDeviceIdx):
        if captureDeviceIdx is None or captureDeviceIdx == -1:
            return None
        import VOIP
        rh = VOIP.getResponseHandler()
        continue
        devices = [ device.decode(sys.getfilesystemencoding()).encode('utf-8') for device in rh.captureDevices ]
        if captureDeviceIdx < len(devices):
            newCaptureDevice = devices[captureDeviceIdx]
            previousDevice = Settings.g_instance.userPrefs.readString(Settings.KEY_VOIP_DEVICE)
            if previousDevice != newCaptureDevice:
                Settings.g_instance.userPrefs.writeString(Settings.KEY_VOIP_DEVICE, newCaptureDevice)
                LOG_NOTE('Change device of voip: %s' % str(newCaptureDevice))
            
        

    
    def onUseRedifineKeyMode(self, callbackId, isUse):
        if self._SettingsInterface__enableRedefineKeysMode:
            BigWorld.wg_setRedefineKeysMode(isUse)
        

    
    def onProcessVivoxTest(self, callbackId, isStart):
        LOG_DEBUG('Vivox test: %s' % str(isStart))
        import VOIP
        rh = VOIP.getResponseHandler()
        if isStart:
            pass
        1
        rh.leaveTestChannel()
        self.respond([
            callbackId,
            False])

    
    def _SettingsInterface__vm_onConnect(self):
        self.call('SettingsDialog.VibroManager.Connect')

    
    def _SettingsInterface__vm_onDisconnect(self):
        self.call('SettingsDialog.VibroManager.Disconnect')

    
    def _SettingsInterface__getVideoSettings(self):
        settings = { }
        settings['monitor'] = {
            'current': self.resolutions.monitorIndex,
            'real': self.resolutions.realMonitorIndex,
            'options': self.resolutions.monitorsList }
        settings['fullScreen'] = not (self.resolutions.isVideoWindowed)
        settings['windowSize'] = {
            'current': self.resolutions.windowSizeIndex,
            'options': self.resolutions.windowSizesList }
        settings['resolution'] = {
            'current': self.resolutions.videoModeIndex,
            'options': self.resolutions.videoModesList }
        return settings

    
    def _SettingsInterface__getSettings(self):
        settings = [
            self.graphicsPresets.getGraphicsPresetsData()]
        import VOIP
        rh = VOIP.getResponseHandler()
        mUserPref = messenger_settings.userPreferences
        vManager = VibroManager.g_instance
        vEffGroups = vManager.getGroupsSettings()
        vEffDefGroup = VibroManager.VibroManager.GroupSettings()
        vEffDefGroup.enabled = False
        vEffDefGroup.gain = 0
        cursorOld = AccountSettings.getSettings('cursor')
        arcade = dict()
        if cursorOld:
            
            try:
                for (key, data) in cursorOld:
                    AccountSettings.setSettings('arcade', False)
                    arcade[key] = {
                        'alpha': data[0],
                        'type': data[1] }
                    AccountSettings.setSettings('arcade', arcade)
            except Exception:
                arcade = AccountSettings.getSettings('arcade')
            

        arcade = AccountSettings.getSettings('arcade')
        markers = AccountSettings.getSettings('markers')
        sniper = AccountSettings.getSettings('sniper')
        if not rh.vivoxDomain == '':
            pass
        config = {
            'aspectRatio': {
                'current': self.resolutions.aspectRatioIndex,
                'options': self.resolutions.aspectRatiosList },
            'vertSync': self.resolutions.isVideoVSync,
            'tripleBuffered': self.resolutions.isTripleBuffered,
            'multisampling': {
                'current': self.resolutions.multisamplingTypeIndex,
                'options': self.resolutions.multisamplingTypesList },
            'customAA': {
                'current': self.resolutions.customAAModeIndex,
                'options': self.resolutions.customAAModesList },
            'gamma': self.resolutions.gamma,
            'masterVolume': round(SoundGroups.g_instance.getMasterVolume() * 100),
            'musicVolume': round(SoundGroups.g_instance.getVolume('music') * 100),
            'voiceVolume': round(SoundGroups.g_instance.getVolume('voice') * 100),
            'vehiclesVolume': round(SoundGroups.g_instance.getVolume('vehicles') * 100),
            'effectsVolume': round(SoundGroups.g_instance.getVolume('effects') * 100),
            'guiVolume': round(SoundGroups.g_instance.getVolume('gui') * 100),
            'ambientVolume': round(SoundGroups.g_instance.getVolume('ambient') * 100),
            'masterVivoxVolume': round(SoundGroups.g_instance.getVolume('masterVivox') * 100),
            'micVivoxVolume': round(SoundGroups.g_instance.getVolume('micVivox') * 100),
            'masterFadeVivoxVolume': round(SoundGroups.g_instance.getVolume('masterFadeVivox') * 100),
            'captureDevice': self._SettingsInterface__getCaptureDeviceSettings(),
            'voiceChatNotSupported': not (VoiceChatInterface.g_instance.ready),
            'datetimeIdx': mUserPref['datetimeIdx'],
            'enableOlFilter': mUserPref['enableOlFilter'],
            'enableSpamFilter': mUserPref['enableSpamFilter'],
            'enableStoreChatMws': mUserPref['enableStoreMws'],
            'enableStoreChatCws': mUserPref['enableStoreCws'],
            'invitesFromFriendsOnly': mUserPref['invitesFromFriendsOnly'],
            'showLangBar': Settings.g_instance.userPrefs.readBool(Settings.KEY_SHOW_LANGUAGE_BAR),
            'enableVoIP': Settings.g_instance.userPrefs.readBool(Settings.KEY_ENABLE_VOIP),
            'enablePostMortemEffect': g_postProcessing.getSetting('mortem_post_effect'),
            'nationalVoices': AccountSettings.getSettings('nationalVoices'),
            'isColorBlind': AccountSettings.getSettings('isColorBlind'),
            'useServerAim': AccountSettings.getSettings('useServerAim'),
            'minimapAlpha': AccountSettings.getSettings('minimapAlpha'),
            'vibroIsConnected': vManager.connect(),
            'vibroGain': vManager.getGain() * 100,
            'vibroEngine': vEffGroups.get('engine', vEffDefGroup).gain * 100,
            'vibroAcceleration': vEffGroups.get('acceleration', vEffDefGroup).gain * 100,
            'vibroShots': vEffGroups.get('shots', vEffDefGroup).gain * 100,
            'vibroHits': vEffGroups.get('hits', vEffDefGroup).gain * 100,
            'vibroCollisions': vEffGroups.get('collisions', vEffDefGroup).gain * 100,
            'vibroDamage': vEffGroups.get('damage', vEffDefGroup).gain * 100,
            'vibroGUI': vEffGroups.get('gui', vEffDefGroup).gain * 100,
            'ppShowLevels': AccountSettings.getSettings('players_panel')['showLevels'],
            'ppShowTypes': AccountSettings.getSettings('players_panel')['showTypes'],
            'replayEnabled': self._SettingsInterface__isReplayEnabled(),
            'arcade': {
                'values': arcade,
                'options': SettingsInterface.CURSOR_VALUES },
            'sniper': {
                'values': sniper,
                'options': SettingsInterface.SNIPER_VALUES },
            'markers': {
                'values': markers,
                'options': SettingsInterface.MARKER_VALUES,
                'types': SettingsInterface.MARKER_TYPES } }
        gameplayMask = AccountSettings.getSettings('gameplayMask')
        for name in ArenaType.g_gameplayNames:
            key = self.GAMEPLAY_KEY_FORMAT.format(name)
            bit = ArenaType.getVisibilityMask(ArenaType.getGameplayIDForName(name))
            config[key] = gameplayMask & bit > 0
        
        settings.append(config)
        if not LogitechMonitor.isPresentColor():
            if self.KEYBOARD_MAPPING_BLOCKS.has_key('logitech_keyboard'):
                del self.KEYBOARD_MAPPING_BLOCKS['logitech_keyboard']
            
        else:
            self.KEYBOARD_MAPPING_BLOCKS['logitech_keyboard'] = ('switch_view',)
        cmdMap = CommandMapping.g_instance
        defaults = cmdMap.getDefaults()
        keyboard = []
        for group_name in self.KEYBOARD_MAPPING_BLOCKS_ORDER:
            if group_name in self.KEYBOARD_MAPPING_BLOCKS.keys():
                group = {
                    'id': group_name,
                    'commands': [] }
                keyboard.append(group)
                for key_setting in self.KEYBOARD_MAPPING_BLOCKS[group_name]:
                    command = cmdMap.getCommand(self.KEYBOARD_MAPPING_COMMANDS[group_name][key_setting])
                    keyCode = cmdMap.get(self.KEYBOARD_MAPPING_COMMANDS[group_name][key_setting])
                    if defaults.has_key(command):
                        pass
                    1
                    defaultCode = 0
                    key = {
                        'id': key_setting,
                        'command': command,
                        'key': getScaleformKey(keyCode),
                        'keyDefault': getScaleformKey(defaultCode) }
                    group['commands'].append(key)
                
            defaults[command]
        
        settings.append(keyboard)
        mouse = { }
        player = BigWorld.player()
        if hasattr(player.inputHandler, 'ctrls'):
            for (key, path) in SettingsInterface.MOUSE_KEYS['ingame'].items():
                mouse[key] = {
                    'defaultValue': SettingsInterface.MOUSE_KEYS['default'][key],
                    'value': player.inputHandler.ctrls[path[0]].camera.getUserConfigValue(path[1]) }
            
        else:
            ds = Settings.g_instance.userPrefs[Settings.KEY_CONTROL_MODE]
            for (key, path) in SettingsInterface.MOUSE_KEYS['lobby'].items():
                default = SettingsInterface.MOUSE_KEYS['default'][key]
                value = default
                if ds is not None:
                    if path[2] == 'float':
                        value = ds[path[0]].readFloat(path[1], default)
                    elif path[2] == 'bool':
                        value = ds[path[0]].readBool(path[1], default)
                    else:
                        LOG_DEBUG('Unknown mouse settings type %s %s' % (key, path))
                
                mouse[key] = {
                    'defaultValue': default,
                    'value': value }
            
        settings.append(mouse)
        return settings

    
    def _SettingsInterface__getCaptureDeviceSettings(self):
        import VOIP
        rh = VOIP.getResponseHandler()
        continue
        devices = [ device.decode(sys.getfilesystemencoding()).encode('utf-8') for device in rh.captureDevices ]
        currentDeviceName = Settings.g_instance.userPrefs.readString(Settings.KEY_VOIP_DEVICE)
        currentCaptureDeviceIdx = -1
        
        try:
            currentCaptureDeviceIdx = devices.index(currentDeviceName)
        except:
            []
            
            try:
                currentCaptureDeviceIdx = rh.captureDevices.index(rh.currentCaptureDevice)


        settings = {
            'current': currentCaptureDeviceIdx,
            'options': devices }
        return settings

    
    def onUpdateCaptureDevices(self, callbackId):
        self._SettingsInterface__updateCaptureDevices()

    
    def __updateCaptureDevices(self):
        Waiting.show('__updateCaptureDevices')
        import VOIP
        yield VoiceChatInterface.g_instance.requestCaptureDevices()
        devices = None
        currentDeviceName = Settings.g_instance.userPrefs.readString(Settings.KEY_VOIP_DEVICE)
        currentCaptureDeviceIdx = -1
        
        try:
            currentCaptureDeviceIdx = devices.index(currentDeviceName)
        except:
            
            try:
                currentCaptureDeviceIdx = devices.index(VOIP.getResponseHandler().currentCaptureDevice)


        value = [
            currentCaptureDeviceIdx]
        continue
        _[1]([ d.decode(sys.getfilesystemencoding()).encode('utf-8') for d in devices ])
        Waiting.hide('__updateCaptureDevices')
        self.call('SettingsDialog.updateCaptureDevices', value)

    _SettingsInterface__updateCaptureDevices = process(__updateCaptureDevices)
    
    def onRecreateDevice(self):
        if self._SettingsInterface__settingsUI:
            if self._SettingsInterface__currentSettings and self._SettingsInterface__currentSettings != self._SettingsInterface__getVideoSettings():
                self._SettingsInterface__currentSettings = self._SettingsInterface__getVideoSettings()
                self._SettingsInterface__settingsUI.buildGraphicsData(self._SettingsInterface__getVideoSettings())
            
        

    
    def onAutodetectSettings(self, callbackID):
        presetIndex = BigWorld.autoDetectGraphicsSettings()
        self.call('SettingsDialog.setPreset', [
            presetIndex])

    
    def onPopulateUI(self, *args):
        self._SettingsInterface__currentSettings = self._SettingsInterface__getVideoSettings()
        VoiceChatInterface.g_instance.processFailedMessage()
        if self._SettingsInterface__settingsUI:
            self._SettingsInterface__settingsUI.script = None
            self._SettingsInterface__settingsUI = None
        
        settingsDialogName = args[1]
        self._SettingsInterface__settingsUI = self.uiHolder.getMember(settingsDialogName)
        if self._SettingsInterface__settingsUI:
            settings = self._SettingsInterface__getSettings()
            self._SettingsInterface__settingsUI.buildData(settings[0], settings[1], settings[2], settings[3])
            self._SettingsInterface__settingsUI.buildGraphicsData(self._SettingsInterface__getVideoSettings())
            self._SettingsInterface__settingsUI.script = self
        else:
            LOG_ERROR('settingsDialog is not found in flash by name {0}'.format(settingsDialogName))

    
    def onApplySettings(self, callbackId, settings):
        (monitorIndex, presetIndex, settingsList) = settings
        if monitorIndex != self.resolutions.realMonitorIndex:
            self.call('SettingsDialog.ApplySettings', [
                'restartNeeded'])
            return None
        applyPresets = self.graphicsPresets.checkApplyGraphicsPreset(int(presetIndex), settingsList)
        self.call('SettingsDialog.ApplySettings', [
            applyPresets])

    
    def onDelaySettings(self, *args):
        self.apply(False, *args)

    
    def onCommitSettings(self, *args):
        self.apply(True, *args)

    
    def apply(self, restartApproved, callbackId, settings):
        restartClient = False
        import VOIP
        ppSettings = dict(AccountSettings.getSettings('players_panel'))
        ppSettings['showLevels'] = settings['ppShowLevels']
        ppSettings['showTypes'] = settings['ppShowTypes']
        if settings['monitor'] != self.resolutions.realMonitorIndex:
            restartClient = True
        
        AccountSettings.setSettings('players_panel', ppSettings)
        self._SettingsInterface__setReplayEnabled(settings['replayEnabled'])
        AccountSettings.setSettings('nationalVoices', settings['nationalVoices'])
        AccountSettings.setSettings('isColorBlind', settings['isColorBlind'])
        AccountSettings.setSettings('useServerAim', settings['useServerAim'])
        AccountSettings.setSettings('minimapAlpha', settings['minimapAlpha'])
        AccountSettings.setSettings('arcade', settings['arcade'])
        AccountSettings.setSettings('sniper', settings['sniper'])
        AccountSettings.setSettings('markers', settings['markers'])
        Settings.g_instance.userPrefs.writeBool(Settings.KEY_SHOW_LANGUAGE_BAR, settings['showLangBar'])
        vManager = VibroManager.g_instance
        vManager.setGain(settings['vibroGain'] / 100)
        vEffGroups = vManager.getGroupsSettings()
        for (groupName, newValue) in [
            ('engine', settings['vibroEngine']),
            ('acceleration', settings['vibroAcceleration']),
            ('shots', settings['vibroShots']),
            ('hits', settings['vibroHits']),
            ('collisions', settings['vibroCollisions']),
            ('damage', settings['vibroDamage']),
            ('gui', settings['vibroGUI'])]:
            if groupName in vEffGroups:
                vEffGroups[groupName].gain = newValue / 100
                vEffGroups[groupName].enabled = newValue > 0
                continue
        
        vManager.setGroupsSettings(vEffGroups)
        self._SettingsInterface__voiceChatEnable(settings['enableVoIP'])
        self._SettingsInterface__changeCaptureDevice(settings[Settings.KEY_VOIP_DEVICE])
        g_postProcessing.setSetting('mortem_post_effect', settings['enablePostMortemEffect'])
        self.uiHolder.clearCommands()
        cmdMap = CommandMapping.g_instance
        keyboard = settings['controls']['keyboard']
        for i in xrange(len(self.KEYBOARD_MAPPING_BLOCKS)):
            group_name = keyboard[i]['id']
            for j in xrange(len(self.KEYBOARD_MAPPING_BLOCKS[group_name])):
                key_name = keyboard[i]['commands'][j]['id']
                key = 'KEY_NONE'
                if keyboard[i]['commands'][j]['key'] != 0:
                    key = getBigworldNameFromKey(getBigworldKey(keyboard[i]['commands'][j]['key']))
                
                cmdMap.remove(self.KEYBOARD_MAPPING_COMMANDS[group_name][key_name])
                cmdMap.add(self.KEYBOARD_MAPPING_COMMANDS[group_name][key_name], key)
            
        
        cmdMap.save()
        self.uiHolder.bindCommands()
        player = BigWorld.player()
        mouse = settings['controls']['mouse']
        if hasattr(player.inputHandler, 'ctrls'):
            player.inputHandler.ctrls['arcade'].camera.setUserConfigValue('sensitivity', mouse['arcadeSens']['value'])
            player.inputHandler.ctrls['sniper'].camera.setUserConfigValue('sensitivity', mouse['sniperSens']['value'])
            player.inputHandler.ctrls['strategic'].camera.setUserConfigValue('sensitivity', mouse['artSens']['value'])
            for mode in ('arcade', 'sniper', 'strategic'):
                player.inputHandler.ctrls[mode].camera.setUserConfigValue('horzInvert', bool(mouse['horInvert']['value']))
                player.inputHandler.ctrls[mode].camera.setUserConfigValue('vertInvert', bool(mouse['vertInvert']['value']))
            
        else:
            ds = Settings.g_instance.userPrefs[Settings.KEY_CONTROL_MODE]
            if ds:
                ds['arcadeMode/camera'].writeFloat('sensitivity', mouse['arcadeSens']['value'])
                ds['sniperMode/camera'].writeFloat('sensitivity', mouse['sniperSens']['value'])
                ds['strategicMode/camera'].writeFloat('sensitivity', mouse['artSens']['value'])
                for mode in ('arcadeMode', 'sniperMode', 'strategicMode'):
                    ds['%s/camera' % mode].writeBool('horzInvert', bool(mouse['horInvert']['value']))
                    ds['%s/camera' % mode].writeBool('vertInvert', bool(mouse['vertInvert']['value']))
                
            
        if not settings['fullScreen']:
            pass
        1
        settings['fullScreen'](settings['vertSync'], settings['tripleBuffered'], settings['windowSize'], settings['resolution'], settings['aspectRatio'], settings['multisampling'], settings['customAA'], settings['gamma'], settings['monitor'])
        if round(SoundGroups.g_instance.getVolume('masterVivox') * 100) != settings['masterVivoxVolume']:
            VOIP.getResponseHandler().setMasterVolume(settings['masterVivoxVolume'])
        
        if round(SoundGroups.g_instance.getVolume('micVivox') * 100) != settings['micVivoxVolume']:
            VOIP.getResponseHandler().setMicrophoneVolume(settings['micVivoxVolume'])
        
        SoundGroups.g_instance.setMasterVolume(float(settings['masterVolume']) / 100)
        SoundGroups.g_instance.setVolume('music', float(settings['musicVolume']) / 100)
        SoundGroups.g_instance.setVolume('voice', float(settings['voiceVolume']) / 100)
        SoundGroups.g_instance.setVolume('vehicles', float(settings['vehiclesVolume']) / 100)
        SoundGroups.g_instance.setVolume('effects', float(settings['effectsVolume']) / 100)
        SoundGroups.g_instance.setVolume('gui', float(settings['guiVolume']) / 100)
        SoundGroups.g_instance.setVolume('ambient', float(settings['ambientVolume']) / 100)
        SoundGroups.g_instance.setVolume('masterVivox', float(settings['masterVivoxVolume']) / 100)
        SoundGroups.g_instance.setVolume('micVivox', float(settings['micVivoxVolume']) / 100)
        SoundGroups.g_instance.setVolume('masterFadeVivox', float(settings['masterFadeVivoxVolume']) / 100)
        if len(VOIP.getResponseHandler().captureDevices):
            device = VOIP.getResponseHandler().captureDevices[0]
            if len(VOIP.getResponseHandler().captureDevices) > settings['captureDevice']:
                device = VOIP.getResponseHandler().captureDevices[settings['captureDevice']]
            
            VOIP.getResponseHandler().setCaptureDevice(device)
        
        messenger_settings.applyUserPreferences(datetimeIdx = settings['datetimeIdx'], enableOlFilter = settings['enableOlFilter'], enableSpamFilter = settings['enableSpamFilter'], enableStoreMws = settings['enableStoreChatMws'], enableStoreCws = settings['enableStoreChatCws'], invitesFromFriendsOnly = settings['invitesFromFriendsOnly'])
        gameplayKeys = (filter,)((lambda item: item.startswith(self.GAMEPLAY_PREFIX)), settings.keys())
        gameplayNames = set([
            'ctf'])
        prefixLen = len(self.GAMEPLAY_PREFIX)
        for key in gameplayKeys:
            if bool(settings[key]) is True:
                name = str(key[prefixLen:])
                if name in ArenaType.g_gameplayNames:
                    gameplayNames.add(name)
                else:
                    LOG_ERROR('Gameplay is not available', name)
            name in ArenaType.g_gameplayNames
        
        LOG_DEBUG('gameplayNames', gameplayNames)
        AccountSettings.setSettings('gameplayMask', ArenaType.getGameplaysMask(gameplayNames))
        qualitySettings = settings['quality']
        applyPresets = self.graphicsPresets.checkApplyGraphicsPreset(int(settings['graphicsQuality']), qualitySettings)
        if applyPresets:
            self.graphicsPresets.applyGraphicsPresets(int(settings['graphicsQuality']), qualitySettings)
            if applyPresets == 'restartNeeded':
                BigWorld.commitPendingGraphicsSettings()
                restartClient = True
            elif applyPresets == 'hasPendingSettings':
                BigWorld.commitPendingGraphicsSettings()
            
        
        g_postProcessing.refresh()
        SniperCamera = SniperCamera
        import AvatarInputHandler.cameras
        SniperCamera._USE_SWINGING = BigWorld.wg_isSniperModeSwingingEnabled()
        if hasattr(player.inputHandler, 'ctrl'):
            if player.inputHandler.ctrl == player.inputHandler.ctrls['sniper']:
                player.inputHandler.ctrl.recreateCamera()
            
        
        if restartClient:
            BigWorld.savePreferences()
            if restartApproved:
                BigWorld.callback(0.3, BigWorld.restartGame)
            else:
                BigWorld.callback(0, partial(BigWorld.changeVideoMode, -1, BigWorld.isVideoWindowed()))
        

    
    def onDialogClose(self, _):
        if self._SettingsInterface__settingsUI:
            self._SettingsInterface__settingsUI.script = None
            self._SettingsInterface__settingsUI = None
        



