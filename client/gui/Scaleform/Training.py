# Source Generated with Decompyle++
# File: Training.pyc (Python 2.6)

from CurrentVehicle import g_currentVehicle
from PlayerEvents import g_playerEvents
from account_helpers.AccountPrebattle import AccountPrebattle
from adisp import process
from debug_utils import LOG_WARNING, LOG_ERROR, LOG_DEBUG
from gui import SystemMessages, GUI_SETTINGS
from gui.BattleContext import g_battleContext
from gui.Scaleform import ColorSchemeManager, VoiceChatInterface
from gui.Scaleform.Waiting import Waiting
from gui.Scaleform.utils.functions import getArenaSubTypeName, getArenaFullName
from gui.Scaleform.utils.gui_items import Vehicle
from gui.Scaleform.windows import UIInterface
from helpers import int2roman
from helpers.i18n import makeString
from messenger import passCensor
from messenger.gui import MessengerDispatcher
from messenger.gui.Scalefrom.search_interfaces import PrebattleSearchUsersInterface
from messenger.gui.Scalefrom.users_interfaces import PrebattleUsersRosterInterface
import ArenaType
import BigWorld
import MusicController
import constants
from MinimapLobby import MinimapLobby
from account_helpers.AccountSettings import AccountSettings
from external_strings_utils import truncate_utf8
_ICONS_MASK = '../maps/icons/map/%(subtype)s%(unicName)s.png'
_UPDATE_LIST_TIMEOUT = 5
_ROOM_LIFETIME = 60 * 60
_UNASSIGNED_ROSTER_MASK = 16

class Training(UIInterface):
    
    def __init__(self):
        UIInterface.__init__(self)
        self._Training__searchUsers = PrebattleSearchUsersInterface(prefix = 'Prebattle.Training.SearchUsers')
        self._Training__contacts = PrebattleUsersRosterInterface(prefix = 'Prebattle.Training')
        self._Training__roomsList = TrainingRooms()
        self._Training__createRoom = CreateTrainingRoom()
        self._Training__roomInfo = TrainingRoom()
        self._Training__selectedRoom = None

    
    def __del__(self):
        LOG_DEBUG('TrainingHandler deleted')

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self._Training__searchUsers.populateUI(proxy)
        self._Training__contacts.populateUI(proxy)
        self._Training__roomsList.populateUI(proxy)
        self._Training__roomInfo.populateUI(proxy)
        self._Training__createRoom.populateUI(proxy)
        g_playerEvents.onPrebattleJoined += self._Training__onPrebattleJoined
        g_playerEvents.onPrebattleJoinFailure += self._Training__joinPrebattleError
        g_playerEvents.onPrebattleLeft += self._Training__onKickedFromRoom
        g_playerEvents.onKickedFromPrebattle += self._Training__onKickedFromRoom
        g_playerEvents.onArenaCreated += self._Training__startArena
        g_playerEvents.onArenaJoinFailure += self._Training__joinArenaError
        g_playerEvents.onKickedFromArena += self._Training__kickArenaError
        forseClose = True
        if AccountPrebattle.isTraining():
            forseClose = False
            self._Training__onRoomJoin()
        else:
            self._Training__roomsList.show()
        self.uiHolder.movie.backgroundAlpha = 0
        self.uiHolder.movie.wg_inputKeyMode = 1
        self.uiHolder.addExternalCallbacks({
            'training.join': self._Training__joinRoom,
            'training.start': self._Training__startRoom,
            'training.close': self._Training__closeRoom })
        if not self.uiHolder.commandsBinded:
            self.uiHolder.bindCommands()
        
        self.uiHolder.updateAccountInfo()
        Waiting.hide('loadPage')
        MusicController.g_musicController.play(MusicController.MUSIC_EVENT_LOBBY)
        MusicController.g_musicController.play(MusicController.AMBIENT_EVENT_LOBBY)
        self._Training__showBattleResults()

    
    def _Training__showBattleResults(self):
        if GUI_SETTINGS.battleStatsInHangar and g_battleContext.lastArenaUniqueID:
            self.uiHolder.battleResults.onBattleResultsShow(None, g_battleContext.lastArenaUniqueID)
            g_battleContext.lastArenaUniqueID = None
        

    
    def dispossessUI(self):
        self._Training__searchUsers.dispossessUI()
        self._Training__contacts.dispossessUI()
        self._Training__roomsList.dispossessUI()
        self._Training__createRoom.dispossessUI()
        self._Training__roomInfo.dispossessUI()
        self.uiHolder.removeExternalCallbacks('training.join', 'training.start', 'training.close')
        UIInterface.dispossessUI(self)
        g_playerEvents.onPrebattleJoined -= self._Training__onPrebattleJoined
        g_playerEvents.onPrebattleJoinFailure -= self._Training__joinPrebattleError
        g_playerEvents.onPrebattleLeft -= self._Training__onKickedFromRoom
        g_playerEvents.onKickedFromPrebattle -= self._Training__onKickedFromRoom
        g_playerEvents.onArenaCreated -= self._Training__startArena
        g_playerEvents.onArenaJoinFailure -= self._Training__joinArenaError
        g_playerEvents.onKickedFromArena -= self._Training__kickArenaError
        self._Training__suspend()

    
    def _Training__joinRoom(self, callbackId, roomId):
        '''
\t\tJoin to room with current vehicle
\t\t'''
        if self._Training__selectedRoom != roomId and roomId is not None:
            
            def joinFunc():
                Waiting.show('trainingJoin')
                BigWorld.player().prb_join(roomId)

            if self.uiHolder.captcha.isCaptchaRequired():
                self.uiHolder.captcha.showCaptcha(joinFunc)
            else:
                joinFunc()
        
        self._Training__selectedRoom = roomId

    
    def _Training__startRoom(self, callbackId):
        '''
\t\tStart room
\t\t'''
        if self.uiHolder.captcha.isCaptchaRequired():
            self.uiHolder.captcha.showCaptcha(self._Training__setTeamReady)
        else:
            self._Training__setTeamReady()

    
    def _Training__setTeamReady(self):
        BigWorld.player().prb_teamReady(1, True, (lambda code: pass))
        BigWorld.player().prb_teamReady(2, True, (lambda code: pass))
        self.call('training.disableStart', [
            True])

    
    def _Training__startArena(self):
        pass

    
    def _Training__kickArenaError(self, code):
        self._Training__errorArena(code, 'kick')

    
    def _Training__joinPrebattleError(self, code):
        Waiting.hide('trainingCreateMap')
        Waiting.hide('trainingJoin')

    
    def _Training__joinArenaError(self, code, errorStr = ''):
        Waiting.hide('trainingCreateMap')
        Waiting.hide('trainingJoin')
        self._Training__errorArena(code, 'join')

    
    def _Training__errorArena(self, errorCode, messageType):
        self._Training__onKickedFromRoom()
        if messageType == 'join':
            pass
        1
        error = constants.KICK_REASON_NAMES[errorCode]
        message = '#system_messages:arena_start_errors/%s/%s' % (messageType, error)
        SystemMessages.pushI18nMessage(message, type = SystemMessages.SM_TYPE.Error)

    
    def _Training__closeRoom(self, callbackId):
        '''
\t\tExit from room. If player is owner close room.
\t\t'''
        BigWorld.player().prb_leave((lambda : pass))
        self._Training__selectedRoom = None

    
    def _Training__onPrebattleJoined(self):
        BigWorld.player().prebattle.onSettingsReceived += self._Training__onPrebattleSettingsReceived
        BigWorld.player().prebattle.onRosterReceived += self._Training__onPrebattleRosterReceived

    
    def _Training__onPrebattleSettingsReceived(self):
        BigWorld.player().prebattle.onSettingsReceived -= self._Training__onPrebattleSettingsReceived
        if AccountPrebattle.isTraining():
            self._Training__onRoomJoin()
        

    
    def _Training__onPrebattleRosterReceived(self):
        BigWorld.player().prebattle.onRosterReceived -= self._Training__onPrebattleRosterReceived
        if AccountPrebattle.isTraining():
            self._Training__onRoomJoin()
        

    
    def _Training__onRoomJoin(self):
        if AccountPrebattle.get().settings and AccountPrebattle.get().rosters:
            if not AccountPrebattle.isTraining():
                self.uiHolder.movie.invoke(('loadHangar',))
                return None
            if not AccountPrebattle.isMemberReady():
                if not g_currentVehicle.isReadyToFight():
                    message = '#system_messages:arena_start_errors/join/no_readyVehicle'
                    SystemMessages.pushI18nMessage(message, type = SystemMessages.SM_TYPE.Error)
                    self.uiHolder.movie.invoke(('loadHangar',))
                    return None
                if self.uiHolder.captcha.isCaptchaRequired():
                    (self.uiHolder.captcha.showCaptcha,)((lambda : BigWorld.player().prb_ready(g_currentVehicle.vehicle.inventoryId, self._Training__onReady)))
                else:
                    BigWorld.player().prb_ready(g_currentVehicle.vehicle.inventoryId, self._Training__onReady)
                return None
            self._Training__onReady()
        

    
    def _Training__onReady(self, code = None):
        self._Training__roomsList.hide()
        self._Training__createRoom.hide()
        Waiting.hide('trainingCreateMap')
        Waiting.hide('trainingJoin')
        self._Training__roomInfo.show()
        self._Training__selectedRoom = None

    
    def _Training__onKickedFromRoom(self, *args):
        '''
\t\tPlayer was kicked from room or leave it themself.
\t\t'''
        self._Training__selectedRoom = None
        self._Training__roomsList.show()
        self._Training__roomInfo.hide()

    
    def _Training__suspend(self):
        if AccountPrebattle.isTraining():
            BigWorld.player().prb_notReady(constants.PREBATTLE_ACCOUNT_STATE.NOT_READY, (lambda code: pass))
        



class TrainingRooms(UIInterface):
    
    def __init__(self):
        self._TrainingRooms__callbackId = None
        UIInterface.__init__(self)

    
    def __del__(self):
        LOG_DEBUG('TrainingRoomsHandler deleted')

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        g_playerEvents.onPrebattlesListReceived += self._TrainingRooms__update

    
    def dispossessUI(self):
        g_playerEvents.onPrebattlesListReceived -= self._TrainingRooms__update
        self.hide()
        UIInterface.dispossessUI(self)

    
    def show(self):
        self.uiHolder.call('training.showList', [])
        self._TrainingRooms__request()

    
    def hide(self):
        self._TrainingRooms__stopRequest()

    
    def _TrainingRooms__stopRequest(self):
        if self._TrainingRooms__callbackId:
            BigWorld.cancelCallback(self._TrainingRooms__callbackId)
            self._TrainingRooms__callbackId = None
        

    
    def _TrainingRooms__request(self):
        '''
\t\tTrainings list requests from server
\t\t'''
        if hasattr(BigWorld.player(), 'requestPrebattles'):
            self._TrainingRooms__callbackId = BigWorld.callback(_UPDATE_LIST_TIMEOUT, self._TrainingRooms__request)
            BigWorld.player().requestPrebattles(constants.PREBATTLE_TYPE.TRAINING, constants.PREBATTLE_CACHE_KEY.CREATE_TIME, False, 0, 50)
        

    
    def _TrainingRooms__update(self, type, count, trainings):
        '''
\t\tPopulate list of rooms recived from server
\t\tIf player was suspended and room exists autojoin to room
\t\tOwner always autojoin ot room (check by name)
\t\t'''
        if type == constants.PREBATTLE_TYPE.TRAINING:
            list = []
            for (time, id, info) in trainings:
                list.append(id)
                list.append(passCensor(info.get(constants.PREBATTLE_CACHE_KEY.COMMENT, '')))
                list.append(info[constants.PREBATTLE_CACHE_KEY.ROUND_LENGTH] / 60)
                arena = ArenaType.g_cache[info[constants.PREBATTLE_CACHE_KEY.ARENA_TYPE_ID]]
                (list.append(getArenaFullName(info[constants.PREBATTLE_CACHE_KEY.ARENA_TYPE_ID])),)
                list.append(info[constants.PREBATTLE_CACHE_KEY.PLAYER_COUNT])
                list.append(arena.maxPlayersInTeam)
                clan = info.get(constants.PREBATTLE_CACHE_KEY.CREATOR_CLAN_ABBREV, '')
                creator = info.get(constants.PREBATTLE_CACHE_KEY.CREATOR, '')
                if clan:
                    creator += '[%s]' % clan
                
                list.append(creator)
                list.append(_ICONS_MASK % {
                    'subtype': 'small/',
                    'unicName': arena.geometryName })
                list.append(not info[constants.PREBATTLE_CACHE_KEY.IS_OPENED])
            
            self.uiHolder.call('training.updateList', list)
        



class TrainingRoom(UIInterface):
    
    def __init__(self):
        self._TrainingRoom__trainingInfo = { }
        self.minimap = None
        UIInterface.__init__(self)

    
    def __del__(self):
        LOG_DEBUG('TrainingRoomHandler deleted')

    
    def prebattle(self):
        if hasattr(BigWorld.player(), 'prebattle'):
            return BigWorld.player().prebattle

    prebattle = property(prebattle)
    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self.uiHolder.addExternalCallbacks({
            'training.populateInfo': self._TrainingRoom__updateInfo,
            'training.populateSettings': self._TrainingRoom__updateSettings,
            'training.changeTeam': self._TrainingRoom__changeTeam,
            'training.selectUseCommonVoiceChat': self._TrainingRoom__selectUseCommonVoiceChat,
            'training.swapTeams': self._TrainingRoom__swapTeams,
            'Prebattle.Training.Invitations.Send': self._TrainingRoom__sendInvitation,
            'Prebattle.Training.Invitations.ShowError': self._TrainingRoom__showInvitationError })
        AccountSettings.onSettingsChanging += self._TrainingRoom__accs_onSettingsChanged
        self.colorManager = ColorSchemeManager._ColorSchemeManager()
        self.colorManager.populateUI(proxy)
        self.minimap = MinimapLobby(proxy, MinimapLobby.IN_ROOM_SCOPE)
        self.minimap.start()
        MessengerDispatcher.g_instance.users.onUsersRosterUpdate += self.onUsersRosterUpdated
        MessengerDispatcher.g_instance.users.onUsersRosterReceived += self._TrainingRoom__updatePlayersList

    
    def dispossessUI(self):
        MessengerDispatcher.g_instance.users.onUsersRosterReceived -= self._TrainingRoom__updatePlayersList
        MessengerDispatcher.g_instance.users.onUsersRosterUpdate -= self.onUsersRosterUpdated
        self.minimap.destroy()
        self.minimap = None
        if self.colorManager:
            self.colorManager.dispossessUI()
        
        self.uiHolder.removeExternalCallbacks('training.populateInfo', 'training.populateSettings', 'training.changeTeam', 'training.selectUseCommonVoiceChat', 'training.swapTeams', 'Prebattle.Training.Invitations.Send', 'Prebattle.Training.Invitations.ShowError')
        AccountSettings.onSettingsChanging -= self._TrainingRoom__accs_onSettingsChanged
        self.hide()
        UIInterface.dispossessUI(self)

    
    def onUsersRosterUpdated(self, action, user):
        self._TrainingRoom__updatePlayersList()

    
    def show(self):
        if self.prebattle:
            self.prebattle.onSettingsReceived += self._TrainingRoom__reciveSettingsInfo
            self.prebattle.onSettingUpdated += self._TrainingRoom__reciveSettingsInfo
            self.prebattle.onRosterReceived += self._TrainingRoom__recivePlayersList
            self.prebattle.onPlayerAdded += self._TrainingRoom__recivePlayersList
            self.prebattle.onPlayerRemoved += self._TrainingRoom__recivePlayersList
            self.prebattle.onPlayerStateChanged += self._TrainingRoom__recivePlayersList
            self.prebattle.onPlayerRosterChanged += self._TrainingRoom__recivePlayersList
            if self.prebattle.settings and self.uiHolder:
                self._TrainingRoom__reciveInfo()
            
        

    
    def hide(self):
        if self.uiHolder is not None:
            self.uiHolder.call('Prebattle.Training.Invitations.CloseWindow')
        
        self._TrainingRoom__trainingInfo = { }
        if self.prebattle:
            self.prebattle.onSettingsReceived -= self._TrainingRoom__reciveSettingsInfo
            self.prebattle.onSettingUpdated -= self._TrainingRoom__reciveSettingsInfo
            self.prebattle.onRosterReceived -= self
