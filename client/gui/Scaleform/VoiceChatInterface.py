# Source Generated with Decompyle++
# File: VoiceChatInterface.pyc (Python 2.6)

import BigWorld
import Settings
import constants
import Event
from adisp import process, async
from enumerations import Enumeration
from windows import UIInterface
from debug_utils import LOG_ERROR, LOG_DEBUG, LOG_NOTE
from chat_shared import CHAT_ACTIONS
from ChatManager import chatManager
from gui import GUI_SETTINGS
VC_STATES = Enumeration('Voice chat states enumeration', [
    'NotInitialized',
    'Initialized',
    'Failed'])

class _VoiceChatInterface(UIInterface):
    onVoiceChatInitFailed = Event.Event()
    onVoiceChatInitSucceded = Event.Event()
    onPlayerSpeaking = Event.Event()
    
    def __init__(self):
        UIInterface.__init__(self)
        self._VoiceChatInterface__initializationTimoutCallback = None
        self._VoiceChatInterface__state = VC_STATES.NotInitialized
        self._VoiceChatInterface__failedEventRaised = False

    
    def reset(self):
        self._VoiceChatInterface__failedEventRaised = False

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        chatManager.subscribeChatAction(self.processFailedMessage, CHAT_ACTIONS.VOIPSettings)

    
    def processFailedMessage(self, *args):
        if not (self._VoiceChatInterface__failedEventRaised) and self._VoiceChatInterface__state != VC_STATES.Initialized and GUI_SETTINGS.voiceChat:
            self._VoiceChatInterface__failedEventRaised = True
            self.onVoiceChatInitFailed()
        

    
    def getPlayerDBID(self):
        import Avatar as Avatar
        import Account as Account
        if type(BigWorld.player()) is Account.PlayerAccount:
            return BigWorld.player().databaseID
        if type(BigWorld.player()) is Avatar.PlayerAvatar and hasattr(BigWorld.player(), 'playerVehicleID'):
            return BigWorld.player().arena.vehicles[BigWorld.player().playerVehicleID].get('accountDBID', None)

    
    def dispossessUI(self):
        chatManager.unsubscribeChatAction(self.processFailedMessage, CHAT_ACTIONS.VOIPSettings)
        UIInterface.dispossessUI(self)

    
    def setPlayerSpeaking(self, accountDBID, isSpeak):
        if not GUI_SETTINGS.voiceChat:
            return None
        self.onPlayerSpeaking(accountDBID, isSpeak)
        g_windowsManager = g_windowsManager
        import gui.WindowsManager
        if g_windowsManager.battleWindow is None:
            self.call('common.speakingPlayersResponse', [
                accountDBID,
                isSpeak,
                accountDBID == self.getPlayerDBID()])
        

    
    def isPlayerSpeaking(self, accountDBID):
        if GUI_SETTINGS.voiceChat:
            import VOIP as VOIP
            return VOIP.getResponseHandler().isParticipantTalking(accountDBID)
        return False

    
    def state(self):
        return self._VoiceChatInterface__state

    state = property(state)
    
    def ready(self):
        return self._VoiceChatInterface__state == VC_STATES.Initialized

    ready = property(ready)
    
    def initialize(self, domain, callback):
        import VOIP
        rh = VOIP.getResponseHandler()
        if domain == '':
            LOG_ERROR('Initialize. Vivox is not supported')
            self._VoiceChatInterface__state = VC_STATES.Failed
            callback(False)
            return None
        if self._VoiceChatInterface__state == VC_STATES.Initialized:
            callback(True)
            return None
        
        def _VoiceChatInterface__response(data):
            rh.channelsMgr.onInitialized -= _VoiceChatInterface__response
            if data is not None:
                pass
            1
            self._VoiceChatInterface__state = VC_STATES.Failed
            if self._VoiceChatInterface__state == VC_STATES.Initialized and self._VoiceChatInterface__failedEventRaised:
                self._VoiceChatInterface__failedEventRaised = False
                self.onVoiceChatInitSucceded()
            
            if self._VoiceChatInterface__initializationTimoutCallback is not None:
                BigWorld.cancelCallback(self._VoiceChatInterface__initializationTimoutCallback)
                self._VoiceChatInterface__initializationTimoutCallback = None
            
            callback(data is not None)

        
        def _VoiceChatInterface__initTimoutCallback():
            if self._VoiceChatInterface__initializationTimoutCallback is not None:
                BigWorld.cancelCallback(self._VoiceChatInterface__initializationTimoutCallback)
                self._VoiceChatInterface__initializationTimoutCallback = None
            

        rh.enable(Settings.g_instance.userPrefs.readBool(Settings.KEY_ENABLE_VOIP))
        rh.channelsMgr.onInitialized += _VoiceChatInterface__response
        self._VoiceChatInterface__initializationTimoutCallback = BigWorld.callback(constants.VOICE_CHAT_INIT_TIMEOUT, _VoiceChatInterface__initTimoutCallback)
        rh.initialize(domain)

    initialize = async(initialize)
    
    def requestCaptureDevices(self, callback):
        import VOIP
        ChannelsMgr = ChannelsMgr
        import VOIP.ChannelsMgr
        if VOIP.getResponseHandler().vivoxDomain == '':
            LOG_ERROR('RequestCaptureDevices. Vivox is not supported')
            callback([])
            return None
        if self._VoiceChatInterface__state != VC_STATES.Initialized:
            LOG_ERROR('RequestCaptureDevices. Vivox has not been initialized')
            callback([])
            return None
        
        def _VoiceChatInterface__response():
            VOIP.getResponseHandler().OnCaptureDevicesUpdated -= _VoiceChatInterface__response
            callback(VOIP.getResponseHandler().captureDevices)

        VOIP.getResponseHandler().OnCaptureDevicesUpdated += _VoiceChatInterface__response
        VOIP.getResponseHandler().requestCaptureDevices()

    requestCaptureDevices = async(requestCaptureDevices)

g_instance = _VoiceChatInterface()

