# Source Generated with Decompyle++
# File: ingame_help.pyc (Python 2.6)

from account_helpers.AccountSettings import AccountSettings
import BigWorld
import ResMgr
import CommandMapping
import constants
from debug_utils import LOG_DEBUG, LOG_ERROR
from gui import VERSION_FILE_PATH
from gui.Scaleform.windows import UIInterface

class IngameHelp(object):
    _IngameHelp__viewCmds = ('CMD_MOVE_FORWARD', 'CMD_MOVE_BACKWARD', 'CMD_ROTATE_LEFT', 'CMD_ROTATE_RIGHT', 'CMD_INCREMENT_CRUISE_MODE', 'CMD_DECREMENT_CRUISE_MODE', 'CMD_CM_VEHICLE_SWITCH_AUTOROTATION', 'CMD_RELOAD_PARTIAL_CLIP', 'CMD_CM_SHOOT', 'CMD_CM_LOCK_TARGET', 'CMD_CM_LOCK_TARGET_OFF', 'CMD_CM_ALTERNATE_MODE', 'CMD_VEHICLE_MARKERS_SHOW_INFO', 'CMD_RADIAL_MENU_SHOW', 'CMD_CHAT_SHORTCUT_ATTACK', 'CMD_VOICECHAT_MUTE', 'CMD_MINIMAP_VISIBLE', 'CMD_TOGGLE_GUI')
    _IngameHelp__viewCmdMapping = []
    _IngameHelp__version = -1
    
    def __init__(self, parentUI):
        self.buildCmdMapping()
        self._IngameHelp__ui = parentUI

    
    def __del__(self):
        LOG_DEBUG('IngameHelp deleted')

    
    def start(self):
        if self._IngameHelp__ui:
            self._IngameHelp__ui.addExternalCallbacks({
                'battle.ingameHelp.getCommandMapping': self.onGetCommandMapping })
        

    
    def destroy(self):
        if self._IngameHelp__ui:
            self._IngameHelp__ui.removeExternalCallbacks('battle.ingameHelp.getCommandMapping')
        
        self._IngameHelp__ui = None

    
    def isRequiredToShow(self):
        playerHelpVersion = int(AccountSettings.getSettings('ingameHelpVersion'))
        if constants.IS_SHOW_INGAME_HELP_FIRST_TIME and self._IngameHelp__version is not -1:
            pass
        return playerHelpVersion is not self._IngameHelp__version

    
    def buildCmdMapping(self):
        cmdMap = CommandMapping.g_instance
        self._IngameHelp__viewCmdMapping = []
        for command in self._IngameHelp__viewCmds:
            key = cmdMap.get(command)
            self._IngameHelp__viewCmdMapping.append(command)
            if key is not None:
                pass
            1
            BigWorld.keyToString(key)('NONE')
        

    
    def onGetCommandMapping(self, responceId, *args):
        args = [
            responceId]
        args.extend(self._IngameHelp__viewCmdMapping)
        self._IngameHelp__ui.respond(args)

    
    def _readVersion(cls):
        dSection = ResMgr.openSection(VERSION_FILE_PATH)
        if dSection is None:
            LOG_ERROR('Can not open file:', VERSION_FILE_PATH)
            IngameHelp._IngameHelp__version = -1
            return None
        IngameHelp._IngameHelp__version = dSection.readInt('ingameHelpVersion', -1)

    _readVersion = classmethod(_readVersion)
    
    def _writeVersionForCurrentPlayer(cls):
        AccountSettings.setSettings('ingameHelpVersion', IngameHelp._IngameHelp__version)

    _writeVersionForCurrentPlayer = classmethod(_writeVersionForCurrentPlayer)


class IngameHelpLobbyDelegator(UIInterface):
    
    def __init__(self):
        super(IngameHelpLobbyDelegator, self).__init__()

    
    def populateUI(self, proxy):
        super(IngameHelpLobbyDelegator, self).populateUI(proxy)
        self.uiHolder.addExternalCallbacks({
            'common.ingameHelp.close': self.onClose })
        self._IngameHelpLobbyDelegator__callback = None
        self._IngameHelpLobbyDelegator__ingameHelp = IngameHelp(proxy)
        self._IngameHelpLobbyDelegator__ingameHelp.start()
        self._IngameHelpLobbyDelegator__ingameHelp._readVersion()

    
    def dispossessUI(self):
        self._IngameHelpLobbyDelegator__ingameHelp.destroy()
        self._IngameHelpLobbyDelegator__ingameHelp = None
        self._IngameHelpLobbyDelegator__callback = None
        self.uiHolder.removeExternalCallbacks('common.ingameHelp.close')
        super(IngameHelpLobbyDelegator, self).dispossessUI()

    
    def isRequiredToShow(self):
        return self._IngameHelpLobbyDelegator__ingameHelp.isRequiredToShow()

    
    def showIngameHelp(self, callback = None):
        self._IngameHelpLobbyDelegator__ingameHelp.buildCmdMapping()
        self._IngameHelpLobbyDelegator__ingameHelp._writeVersionForCurrentPlayer()
        self._IngameHelpLobbyDelegator__callback = callback
        self.uiHolder.call('common.ingameHelp.show')

    
    def closeIngameHelp(self):
        if self._IngameHelpLobbyDelegator__callback is not None:
            self._IngameHelpLobbyDelegator__callback()
            self._IngameHelpLobbyDelegator__callback = None
        

    
    def onClose(self, _):
        self.closeIngameHelp()



