# Source Generated with Decompyle++
# File: ResponseHandler.pyc (Python 2.6)

import BigWorld
import Event
import math
from Account import PlayerAccount
import Avatar
import constants
import Vivox
import Helpers
from debug_utils import LOG_DEBUG, verify, LOG_ERROR
import SoundGroups
from wotdecorators import noexcept
from chat_shared import CHAT_ACTIONS, CHAT_COMMANDS, CHAT_RESPONSES, USERS_ROSTER_VOICE_MUTED
from ChatManager import chatManager
from gui.WindowsManager import g_windowsManager
import ChannelsMgr
from gui.Scaleform import VoiceChatInterface
import FMOD

class ResponseHandler:
    MAX_VOLUME = 100
    NORMAL_VOLUME = 50
    DEFAULT_PARTICIPANT_VOLUME = 50
    LOGARITHM_BASE = 2 ** (1 / 6)
    
    def __init__(self, channelsMgr):
        self.channelsMgr = channelsMgr
        self.vivoxDomain = ''
        self.testChannel = ''
        self.mainChannel = [
            '',
            '']
        self.inTesting = False
        self._ResponseHandler__activateMicByVoice = False
        self._ResponseHandler__enableVoiceNormalization = False
        self.usersRoster = { }
        self.channelUsers = { }
        self.channelID = -1
        self.captureDevices = []
        self.currentCaptureDevice = ''
        self.OnCaptureDevicesUpdated = Event.Event()
        self.onParticipantMute = Event.Event()
        self.channelsMgr.onParticipantAdded += self._onParticipantAdded
        self.channelsMgr.onParticipantRemoved += self._onParticipantRemoved
        self.channelsMgr.onParticipantUpdated += self._onParticipantUpdated
        self.channelsMgr.onJoinedChannel += self._onJoinedChannel
        self.channelsMgr.onLeftChannel += self.onLeftChannel
        self.channelsMgr.onLogined += self.onLogined
        self.channelsMgr.onStateChanged += self.onStateChanged

    
    def destroy(self):
        self.channelsMgr.onParticipantAdded -= self._onParticipantAdded
        self.channelsMgr.onParticipantRemoved -= self._onParticipantRemoved
        self.channelsMgr.onParticipantUpdated -= self._onParticipantUpdated
        self.channelsMgr.onJoinedChannel -= self._onJoinedChannel
        self.channelsMgr.onLeftChannel -= self.onLeftChannel
        self.channelsMgr.onLogined -= self.onLogined
        self.channelsMgr.onStateChanged -= self.onStateChanged
        self.channelsMgr.destroy()

    
    def onConnected(self):
        chatManager.subscribeChatAction(self._ResponseHandler__onEnterChatChannel, CHAT_ACTIONS.VOIPSettings)
        chatManager.subscribeChatAction(self._ResponseHandler__onLeftChatChannel, CHAT_ACTIONS.channelDestroyed)
        chatManager.subscribeChatAction(self._ResponseHandler__onLeftChatChannel, CHAT_ACTIONS.selfLeave)
        chatManager.subscribeChatAction(self._ResponseHandler__onUserCredentials, CHAT_ACTIONS.VOIPCredentials)
        chatManager.subscribeChatAction(self._ResponseHandler__onRequestUsersRoster, CHAT_ACTIONS.requestUsersRoster)
        chatManager.subscribeChatAction(self._ResponseHandler__onChatActionSetMuted, CHAT_ACTIONS.setMuted)
        chatManager.subscribeChatAction(self._ResponseHandler__onChatActionUnsetMuted, CHAT_ACTIONS.unsetMuted)
        chatManager.subscribeChatAction(self._ResponseHandler__onChatResponseMutedError, CHAT_RESPONSES.setMutedError)
        chatManager.subscribeChatAction(self._ResponseHandler__onChatResponseMutedError, CHAT_RESPONSES.unsetMutedError)
        self.channelsMgr.onConnected()

    
    def unsubscribeChatActions(self):
        chatManager.unsubscribeChatAction(self._ResponseHandler__onEnterChatChannel, CHAT_ACTIONS.VOIPSettings)
        chatManager.unsubscribeChatAction(self._ResponseHandler__onLeftChatChannel, CHAT_ACTIONS.channelDestroyed)
        chatManager.unsubscribeChatAction(self._ResponseHandler__onLeftChatChannel, CHAT_ACTIONS.selfLeave)
        chatManager.unsubscribeChatAction(self._ResponseHandler__onUserCredentials, CHAT_ACTIONS.VOIPCredentials)
        chatManager.unsubscribeChatAction(self._ResponseHandler__onRequestUsersRoster, CHAT_ACTIONS.requestUsersRoster)
        chatManager.unsubscribeChatAction(self._ResponseHandler__onChatActionSetMuted, CHAT_ACTIONS.setMuted)
        chatManager.unsubscribeChatAction(self._ResponseHandler__onChatActionUnsetMuted, CHAT_ACTIONS.unsetMuted)
        chatManager.unsubscribeChatAction(self._ResponseHandler__onChatResponseMutedError, CHAT_RESPONSES.setMutedError)
        chatManager.unsubscribeChatAction(self._ResponseHandler__onChatResponseMutedError, CHAT_RESPONSES.unsetMutedError)

    
    def initialize(self, domain):
        if not domain:
            return None
        if self.vivoxDomain:
            verify(domain == self.vivoxDomain)
            return None
        self.vivoxDomain = domain
        self.testChannel = 'sip:confctl-2@' + domain.partition('www.')[2]
        self.channelsMgr.initialize(domain)

    
    def initialized(self):
        return self.channelsMgr.initialized

    
    def _ResponseHandler__onUserCredentials(self, data):
        LOG_DEBUG('__onUserCredentials', data['data'][0], data['data'][1])
        self.channelsMgr.login(data['data'][0], data['data'][1])
        BigWorld.player().requestUsersRoster(USERS_ROSTER_VOICE_MUTED)

    
    def _ResponseHandler__onEnterChatChannel(self, data):
        if data['data']['URL'] == '' or data['data']['password'] == '':
            return None
        self.channelID = data['channel']
        credentials = [
            data['data']['URL'],
            data['data']['password']]
        if self.inTesting:
            self.mainChannel = credentials
        else:
            self._ResponseHandler__enterChannel(credentials[0], credentials[1])

    
    def _ResponseHandler__onLeftChatChannel(self, data):
        if self.channelID == data['channel']:
            if self.inTesting:
                verify(self.mainChannel[0])
                self.mainChannel = [
                    '',
                    '']
            else:
                self.channelID = -1
                verify(not self.mainChannel[0])
                self._ResponseHandler__leaveChannel()
        

    
    def _ResponseHandler__enterChannel(self, name, password):
        if not self.channelsMgr.user[0] and self.channelsMgr.enabled:
            BigWorld.player().requestVOIPCredentials()
        
        self.channelsMgr.enterChannel(name, password)

    
    def _ResponseHandler__leaveChannel(self):
        self.channelsMgr.leaveChannel()

    
    def logout(self):
        self.usersRoster.clear()
        self.channelsMgr.logout()

    
    def enable(self, enabled):
        self.channelsMgr.enable(enabled)

    
    def setMicMute(self, muted = True):
        if muted and self._ResponseHandler__activateMicByVoice:
            return None
        self._setMicMute(muted)

    
    def _setMicMute(self, muted = True):
        pass

    
    def setVoiceActivation(self, enabled):
        self._ResponseHandler__activateMicByVoice = enabled
        self.setMicMute(not enabled)

    
    def setMasterVolume(self, attenuation):
        BigWorld.VOIP.setMasterVolume(attenuation, { })

    
    def setMicrophoneVolume(self, attenuation):
        BigWorld.VOIP.setMicrophoneVolume(attenuation, { })

    
    def setVolume(self):
        self.setMasterVolume(int(round(SoundGroups.g_instance.getVolume('masterVivox') * 100)))
        self.setMicrophoneVolume(int(round(SoundGroups.g_instance.getVolume('micVivox') * 100)))

    
    def getVADProperties(self):
        LOG_DEBUG('ResponseHandler::getVADProperties is not implemented!')

    
    def setVADProperties(self, hangover, sensitivity):
        LOG_DEBUG('ResponseHandler::setVADProperties is not implemented!')

    
    def enterTestChannel(self):
        verify(not (self.inTesting))
        if self.inTesting:
            return None
        self.inTesting = True
        self.mainChannel = self.channelsMgr.channel
        self._ResponseHandler__enterChannel(self.testChannel, '')

    
    def leaveTestChannel(self):
        verify(self.inTesting)
        if not self.inTesting:
            return None
        self.inTesting = False
        if self.mainChannel[0]:
            self._ResponseHandler__enterChannel(self.mainChannel[0], self.mainChannel[1])
        else:
            self._ResponseHandler__leaveChannel()
        self.mainChannel = [
            '',
            '']

    
    def muteParticipantForMe(self, dbid, mute, name = ''):
        if dbid not in self.channelUsers:
            LOG_DEBUG("mute_for_me: User not found in participant's list")
            return False
        p = BigWorld.player()
        if mute:
            pass
        1
        p.unsetMuted(dbid)
        self._muteParticipantForMe(dbid, mute)

    
    def _muteParticipantForMe(self, dbid, mute):
        LOG_DEBUG('ResponseHandler::_muteParticipantForMe is not implemented!')
        return False

    
    def _ResponseHandler__onChatActionSetMuted(self, data):
        self._ResponseHandler__onChatActionMute(data['data'][0], True)

    
    def _ResponseHandler__onChatActionUnsetMuted(self, data):
        self._ResponseHandler__onChatActionMute(data['data'], False)

    
    def _ResponseHandler__onChatActionMute(self, dbid, muted):
        LOG_DEBUG('__onChatActionMute', dbid, muted)
        self.usersRoster[dbid] = muted
        if dbid in self.channelUsers and self.channelUsers[dbid]['muted'] != muted:
            self._muteParticipantForMe(dbid, muted)
        

    
    def _ResponseHandler__onChatResponseMutedError(self, data):
        LOG_ERROR('__onChatResponseMutedError', data.items())
        if False:
            pass
        verify(data)

    
    def _ResponseHandler__onRequestUsersRoster(self, data):
        for (dbid, name, flags) in data['data']:
            muted = bool(flags & USERS_ROSTER_VOICE_MUTED)
            self.usersRoster[dbid] = muted
            if muted and dbid in self.channelUsers:
                self._muteParticipantForMe(dbid, True)
                continue
        

    
    def requestCaptureDevices(self):
        pass

    
    def setCaptureDevice(self, deviceName):
        BigWorld.VOIP.wg_setCaptureDevice(deviceName)
        self.requestCaptureDevices()

    
    def setParticipantVolume(self, uri, volume):
        LOG_DEBUG('ResponseHandler::setParticipantVolume is not implemented')

    
    def isCommander(self, dbid):
        if isinstance(BigWorld.player(), PlayerAccount) and hasattr(BigWorld.player(), 'prebattle') and BigWorld.player().prebattle is not None:
            creatorName = BigWorld.player().prebattle.settings['creator']
            for roster in BigWorld.player().prebattle.rosters.values():
                for accData in roster.values():
                    if accData['dbID'] == dbid:
                        return accData['name'] == creatorName
                
            
        elif isinstance(BigWorld.player(), Avatar.PlayerAvatar):
            vehicles = BigWorld.player().arena.vehicles
            for vehicleData in vehicles.values():
                if vehicleData['accountDBID'] == dbid:
                    return vehicleData['isPrebattleCreator']
            
        
        return False

    
    def _ResponseHandler__muffleIfCommanderTalk(self, dbid, isTalking):
        if isTalking:
            pass
        1
        desiredVolume = 50
        if self.isCommander(dbid):
            for (userDBID, channelUser) in self.channelUsers.items():
                if userDBID != dbid:
                    self.setParticipantVolume(channelUser['uri'], desiredVolume)
                    continue
                44
            
        

    
    def isParticipantTalking(self, dbid):
        outcome = self.channelUsers.get(dbid, { }).get('talking', False)
        return outcome

    
    def setPlayerTalking(self, dbid, talking):
        VoiceChatInterface.g_instance.setPlayerSpeaking(dbid, talking)
        if g_windowsManager.battleWindow is not None:
            g_windowsManager.battleWindow.setPlayerSpeaking(dbid, talking)
        

    
    def muffleMasterVolume(self):
        masterVolume = SoundGroups.g_instance.getMasterVolume() * SoundGroups.g_instance.getVolume('masterFadeVivox')
        FMOD.setMasterVolume(masterVolume)

    
    def restoreMasterVolume(self):
        FMOD.setMasterVolume(SoundGroups.g_instance.getMasterVolume())

    
    def isAnyoneTalking(self):
        for info in self.channelUsers.values():
            if info['talking']:
                return True
        
        return False

    
    def _onParticipantAdded(self, data):
        uri = data[constants.KEY_PARTICIPANT_URI]
        (dbid, _) = self.extractDBIDFromURI(uri)
        if dbid == -1:
            return None
        self.channelUsers[dbid] = {
            'talking': False,
            'uri': uri,
            'muted': False,
            'lastVolumeUpdateTime': BigWorld.time(),
            'energy': 0,
            'volume': 0 }
        if self.usersRoster.get(dbid, False):
            self._muteParticipantForMe(dbid, True)
        

    
    def _onParticipantUpdated(self, data):
        uri = data[constants.KEY_PARTICIPANT_URI]
        (dbid, participantLogin) = self.extractDBIDFromURI(uri)
        if dbid == -1:
            return None
        talking = int(data[constants.KEY_IS_SPEAKING])
        channelUser = self.channelUsers[dbid]
        if dbid in self.channelUsers:
            if channelUser['talking'] != talking:
                channelUser['talking'] = talking
                if self.isAnyoneTalking():
                    pass
                1
                self.restoreMasterVolume()
                if participantLogin != self.channelsMgr.user[0]:
                    self._ResponseHandler__muffleIfCommanderTalk(dbid, talking)
                
            
        
        self.setPlayerTalking(dbid, talking)
        channelUser['energy'] = data[constants.KEY_ENERGY]
        channelUser['volume'] = data[constants.KEY_VOLUME]

    
    def _onParticipantRemoved(self, data):
        uri = data[constants.KEY_PARTICIPANT_URI]
        (dbid, _) = self.extractDBIDFromURI(uri)
        if dbid in self.channelUsers:
            del self.channelUsers[dbid]
        
        self.setPlayerTalking(dbid, False)

    
    def _onJoinedChannel(self, data):
        self.setVolume()
        verify(not (self.channelUsers))

    
    def onLeftChannel(self, data):
        for dbid in self.channelUsers.keys():
            self.setPlayerTalking(dbid, False)
        
        self.channelUsers.clear()
        self.restoreMasterVolume()

    
    def onLogined(self):
        BigWorld.player().logVivoxLogin()

    
    def onStateChanged(self, old, new):
        if new == self.channelsMgr.STATE_JOINING_CHANNEL:
            if self.channelsMgr.channel[0] != self.testChannel:
                pass
            muteMic = not (self._ResponseHandler__activateMicByVoice)
            self.setMicMute(muteMic)
        

    
    def extractDBIDFromURI(self, uri):
        
        try:
            domain = self.vivoxDomain.partition('www.')[2]
            login = uri.partition('sip:')[2].rpartition('@' + domain)[0]
            s = login[login.find('.') + 1:]
            return (int(s), login)
        except:
            return -1




