# Source Generated with Decompyle++
# File: RadialMenu.pyc (Python 2.6)

import Avatar
import BigWorld
import Keys
import GUI
import Vehicle
from GuiBinding import FlashBind
from debug_utils import LOG_ERROR, LOG_DEBUG
from gui.Scaleform.utils.key_mapping import getScaleformKey, BW_TO_SCALEFORM
from weakref import proxy
from windows import UIInterface
import CommandMapping

class RadialMenu(UIInterface):
    DEFAULT_CUT = 'default'
    ALLY_CUT = 'ally'
    ENEMY_CUT = 'enemy'
    ENEMY_SPG_CUT = 'enemy_spg'
    SELECT_EFFECT_SND = 'effects.select_radial_button'
    INDEX_REFERENCES = (3, 1, 5, 4, 0, 2)
    ALL_SHORTCUTS = {
        DEFAULT_CUT: {
            'labels': [
                'attack',
                'backToBase',
                'negative',
                'positive',
                'helpMe',
                'reloadingGun'],
            'commands': [
                'ATTACK',
                'BACKTOBASE',
                'NEGATIVE',
                'POSITIVE',
                'HELPME',
                'RELOADINGGUN'],
            'icons': [
                'Attack',
                'Backtobase',
                'No',
                'Yes',
                'Helpme',
                'Reload'] },
        ALLY_CUT: {
            'labels': [
                'followMe',
                'toBack',
                'negative',
                'positive',
                'helpMeEx',
                'stop'],
            'commands': [
                'FOLLOWME',
                'TURNBACK',
                'NEGATIVE',
                'POSITIVE',
                'HELPMEEX',
                'STOP'],
            'icons': [
                'Followme',
                'Turnback',
                'No',
                'Yes',
                'Helpmeex',
                'Stop'] },
        ENEMY_CUT: {
            'labels': [
                'supportMeWithFire',
                'backToBase',
                'negative',
                'positive',
                'helpMe',
                'reloadingGun'],
            'commands': [
                'SUPPORTMEWITHFIRE',
                'BACKTOBASE',
                'NEGATIVE',
                'POSITIVE',
                'HELPME',
                'RELOADINGGUN'],
            'icons': [
                'Support',
                'Backtobase',
                'No',
                'Yes',
                'Helpme',
                'Reload'] },
        ENEMY_SPG_CUT: {
            'labels': [
                'attackEnemy',
                'backToBase',
                'negative',
                'positive',
                'helpMe',
                'reloadingGun'],
            'commands': [
                'ATTACKENEMY',
                'BACKTOBASE',
                'NEGATIVE',
                'POSITIVE',
                'HELPME',
                'RELOADINGGUN'],
            'icons': [
                'AttackSPG',
                'Backtobase',
                'No',
                'Yes',
                'Helpme',
                'Reload'] } }
    DENIED_KEYB_CMDS = [
        'ATTACK']
    TARGET_ACTIONS = [
        'FOLLOWME',
        'TURNBACK',
        'HELPMEEX',
        'SUPPORTMEWITHFIRE',
        'ATTACKENEMY',
        'STOP']
    
    def __init__(self, parentUI):
        UIInterface.__init__(self)
        self.proxy = proxy(self)
        self.GUICtrl = None
        self._RadialMenu__parentUI = parentUI
        self._RadialMenu__settings = None
        self._RadialMenu__currentTarget = None
        self._RadialMenu__currentVehicleDesc = None
        self._RadialMenu__showed = False

    
    def populateUI(self, proxy):
        for state in self.ALL_SHORTCUTS:
            self.GUICtrl.setState(state)
            list = self._RadialMenu__getDataForFlash(state)
            self.GUICtrl.buildData(list)
        

    populateUI = FlashBind('RadialMenu')(populateUI)
    
    def setSettings(self, settings):
        self._RadialMenu__settings = settings
        SHCTS_SECTION = 'shortcuts'
        self.KEYB_MAPPINGS = self._RadialMenu__settings.KEYBOARD_MAPPING_BLOCKS[SHCTS_SECTION]
        self.KEYB_CMDS_MAPPINGS = self._RadialMenu__settings.KEYBOARD_MAPPING_COMMANDS[SHCTS_SECTION]

    
    def handleKey(self, key, isDown, offset):
        cmdMap = CommandMapping.g_instance
        if cmdMap.isFired(CommandMapping.CMD_RADIAL_MENU_SHOW, key):
            if isDown:
                if self._RadialMenu__currentVehicleDesc is None:
                    self._RadialMenu__currentVehicleDesc = self._RadialMenu__getCurrentVehicleDesc()
                
                if self._RadialMenu__currentVehicleDesc is not None:
                    self._RadialMenu__currentTarget = BigWorld.target()
                    mouseUsedForShow = getScaleformKey(key) <= BW_TO_SCALEFORM[Keys.KEY_MOUSE7]
                    self._RadialMenu__onMenuShow(offset, mouseUsedForShow)
                
            else:
                self._RadialMenu__onMenuHide()
            return None
        if isDown:
            if not self._RadialMenu__ingameMenuIsVisible():
                if self._RadialMenu__currentVehicleDesc is None:
                    self._RadialMenu__currentVehicleDesc = self._RadialMenu__getCurrentVehicleDesc()
                
                if not self._RadialMenu__showed:
                    self._RadialMenu__currentTarget = BigWorld.target()
                
                for command in self.KEYB_MAPPINGS:
                    shortcut = self.KEYB_CMDS_MAPPINGS[command]
                    if cmdMap.isFired(getattr(CommandMapping, shortcut), key):
                        action = self._RadialMenu__getMappedCommand(command)
                        if action not in self.DENIED_KEYB_CMDS:
                            self.onAction(action)
                        
                    action not in self.DENIED_KEYB_CMDS
                
            
        

    
    def _RadialMenu__getDataForFlash(self, crosshairType):
        if crosshairType != '':
            CMD_LOCALE_PFX = '#ingame_help:chatShortcuts/'
            need_shortcuts = self.ALL_SHORTCUTS[crosshairType]
            flashData = []
            for (i, shortcut_key) in enumerate(self.KEYB_MAPPINGS):
                index = self.INDEX_REFERENCES[i]
                title = need_shortcuts['labels'][index]
                action = need_shortcuts['commands'][index]
                icon = need_shortcuts['icons'][index]
                data = {
                    'title': CMD_LOCALE_PFX + title,
                    'action': action,
                    'icon': icon }
                flashData.append(data)
            
            return flashData
        LOG_ERROR('Unknown vehicle type under crosshair target')

    
    def _RadialMenu__getKeysList(self, crosshairType):
        if crosshairType != '':
            keys = []
            need_shortcuts = self.ALL_SHORTCUTS[crosshairType]
            for (i, shortcut_key) in enumerate(self.KEYB_MAPPINGS):
                index = self.INDEX_REFERENCES[i]
                action = need_shortcuts['commands'][index]
                if action not in self.DENIED_KEYB_CMDS:
                    shortcut = self.KEYB_CMDS_MAPPINGS[self.KEYB_MAPPINGS[index]]
                    keyCode = getScaleformKey(CommandMapping.g_instance.get(shortcut))
                    keys.append(keyCode)
                    continue
                keys.append(0)
            
            return keys
        LOG_ERROR('Unknown vehicle type under crosshair target')

    
    def _RadialMenu__getMappedCommand(self, shortcut):
        crosshairType = self._RadialMenu__getCrosshairType()
        index = self._RadialMenu__settings.KEYBOARD_MAPPING_BLOCKS['shortcuts'].index(shortcut)
        return self.ALL_SHORTCUTS[crosshairType]['commands'][index]

    
    def _RadialMenu__getCrosshairType(self):
        player = BigWorld.player()
        outcome = self.DEFAULT_CUT
        if self._RadialMenu__isTargetCorrect(player):
            if self._RadialMenu__currentTarget.publicInfo.team == player.team:
                outcome = self.ALLY_CUT
            elif 'SPG' in self._RadialMenu__currentVehicleDesc['vehicleType'].type.tags:
                outcome = self.ENEMY_SPG_CUT
            else:
                outcome = self.ENEMY_CUT
        
        return outcome

    
    def _RadialMenu__isTargetCorrect(self, player):
        if self._RadialMenu__currentTarget is not None and isinstance(self._RadialMenu__currentTarget, Vehicle.Vehicle):
            if self._RadialMenu__currentTarget.isAlive():
                if player is not None and type(player) == Avatar.PlayerAvatar:
                    return True
            
        
        return False

    
    def _RadialMenu__getCurrentVehicleDesc(self):
        player = BigWorld.player()
        vehicles = player.arena.vehicles
        for (id, desc) in vehicles.items():
            if id == player.playerVehicleID:
                return desc
        

    
    def _RadialMenu__getFireKeyCode(self):
        fireKey = self._RadialMenu__settings.KEYBOARD_MAPPING_COMMANDS['firing']['fire']
        return getScaleformKey(fireKey)

    
    def _RadialMenu__playSound(self, soundName):
        if self.uiHolder.soundManager is not None:
            self.uiHolder.soundManager.playSound(soundName)
        

    
    def onSelectButton(self):
        self._RadialMenu__playSound(self.SELECT_EFFECT_SND)

    
    def onAction(self, action):
        player = BigWorld.player()
        if action in self.TARGET_ACTIONS:
            player.onChatShortcutTarget(action, self._RadialMenu__currentTarget.id)
        else:
            player.onChatShortcut(action)

    
    def _RadialMenu__onMenuShow(self, offset, mouseUsedForShow):
        if not self._RadialMenu__ingameMenuIsVisible():
            crosshairType = self._RadialMenu__getCrosshairType()
            keys = self._RadialMenu__getKeysList(crosshairType)
            self.GUICtrl.setFireKeyCode(self._RadialMenu__getFireKeyCode())
            self.GUICtrl.setState(crosshairType)
            self.GUICtrl.updateKeys(keys)
            (screenWidth, screenHeight) = GUI.screenResolution()
            (mouseLeft, mouseTop) = offset
            x = round((screenWidth / 2) * mouseLeft)
            y = -round((screenHeight / 2) * mouseTop)
            offset = (x, y)
            self._RadialMenu__showed = True
            self.GUICtrl.show(offset, mouseUsedForShow)
        

    
    def _RadialMenu__ingameMenuIsVisible(self):
        battle = self.uiHolder.getMember('_level0')
        return battle.ingameMenusWasShowed()

    
    def _RadialMenu__onMenuHide(self):
        self._RadialMenu__showed = False
        self.GUICtrl.hide()

    
    def destroy(self):
        pass



