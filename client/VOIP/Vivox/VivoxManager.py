# Source Generated with Decompyle++
# File: VivoxManager.pyc (Python 2.6)

import BigWorld
from VOIP import constants
from VOIP.ResponseHandler import ResponseHandler
from debug_utils import LOG_DEBUG, verify
import math

class VivoxManager(ResponseHandler):
    
    def __init__(self, channelsMgr):
        ResponseHandler.__init__(self, channelsMgr)
        self.channelsMgr.onCaptureDevicesUpdated += self._onCaptureDevicesUpdated

    
    def destroy(self):
        self.channelsMgr.onCaptureDevicesUpdated -= self._onCaptureDevicesUpdated
        ResponseHandler.destroy(self)

    
    def getVADProperties(self):
        cmd = {
            constants.KEY_COMMAND: constants.CMD_REQ_AUX_GET_VAD_PROPERTIES }
        BigWorld.VOIP.command(cmd)

    
    def setVADProperties(self, hangover, sensitivity):
        cmd = {
            constants.KEY_COMMAND: constants.CMD_REQ_AUX_SET_VAD_PROPERTIES,
            constants.KEY_VAD_HANGOVER: str(hangover),
            constants.KEY_VAD_SENSITIVITY: str(sensitivity) }
        BigWorld.VOIP.command(cmd)
        LOG_DEBUG('ResponseHandler::setVADProperties %d %d' % (hangover, sensitivity))

    
    def _VivoxManager__normalizeVoices(self):
        myOwnUri = self.channelsMgr.loginName
        
        def speaking(channelUser):
            if float(channelUser['energy']) > 0 and channelUser['uri'] != myOwnUri:
                pass
            return channelUser['talking']

        speakingChannelUsers = filter(speaking, self.channelUsers.values())
        for channelUser in speakingChannelUsers:
            if channelUser['talking']:
                volumeUpdateDelta = BigWorld.time() - channelUser['lastVolumeUpdateTime']
                if volumeUpdateDelta > 0.1:
                    currentEnergy = float(channelUser['energy'])
                    desiredVolume = ResponseHandler.NORMAL_VOLUME + math.log(1 / currentEnergy, ResponseHandler.LOGARITHM_BASE)
                    desiredVolume = round(desiredVolume)
                    self.setParticipantVolume(channelUser['uri'], desiredVolume)
                    channelUser['lastVolumeUpdateTime'] = BigWorld.time()
                
            volumeUpdateDelta > 0.1
        

    
    def _muteParticipantForMe(self, dbid, mute):
        verify(dbid in self.channelUsers)
        self.channelUsers[dbid]['muted'] = mute
        uri = self.channelUsers[dbid]['uri']
        cmd = { }
        cmd[constants.KEY_COMMAND] = constants.CMD_SET_PARTICIPANT_MUTE
        cmd[constants.KEY_PARTICIPANT_URI] = uri
        cmd[constants.KEY_STATE] = str(mute)
        BigWorld.VOIP.command(cmd)
        LOG_DEBUG('mute_for_me: %d, %s' % (dbid, str(mute)))
        self.onParticipantMute(dbid, mute)
        return True

    
    def _setMicMute(self, muted = True):
        cmd = {
            constants.KEY_COMMAND: 'mute_mic',
            constants.KEY_STATE: str(muted) }
        BigWorld.VOIP.command(cmd)
        LOG_DEBUG('mute_mic: %s' % str(muted))

    
    def setParticipantVolume(self, uri, volume):
        volumeToSet = int(volume)
        if volumeToSet > 100:
            volumeToSet = 100
        
        cmd = {
            constants.KEY_COMMAND: constants.CMD_SET_PARTICIPANT_VOLUME,
            constants.KEY_PARTICIPANT_URI: uri,
            constants.KEY_VOLUME: str(volumeToSet) }
        BigWorld.VOIP.command(cmd)

    
    def requestCaptureDevices(self):
        BigWorld.VOIP.wg_getCaptureDevices()

    
    def _onCaptureDevicesUpdated(self, data):
        captureDevicesCount = int(data[constants.KEY_COUNT])
        self.captureDevices = []
        for i in xrange(captureDevicesCount):
            self.captureDevices.append(str(data[constants.KEY_CAPTURE_DEVICES + '_' + str(i)]))
        
        self.currentCaptureDevice = str(data[constants.KEY_CURRENT_CAPTURE_DEVICE])
        self.OnCaptureDevicesUpdated()



