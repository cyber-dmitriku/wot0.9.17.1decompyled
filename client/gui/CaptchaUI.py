# Source Generated with Decompyle++
# File: CaptchaUI.pyc (Python 2.6)

from abc import ABCMeta, abstractmethod
import AccountCommands
import BigWorld
from account_helpers.captcha import CAPTCHA_API_CLASS
from constants import JOIN_FAILURE
from debug_utils import LOG_ERROR, LOG_WARNING
from helpers import i18n
from PlayerEvents import g_playerEvents
from gui.ClientUpdateManager import g_clientUpdateManager

class CaptchaUI(object):
    __metaclass__ = ABCMeta
    _callback = None
    _api = CAPTCHA_API_CLASS()
    _battlesTillCaptcha = 99
    _captchaTriesLeft = 3
    _CLIENT_ERROR_CODES = {
        'enqueue-failure': i18n.makeString('#captcha:error-codes/enqueue-failure'),
        'response-is-empty': i18n.makeString('#captcha:error-codes/response-is-empty'),
        'challenge-is-empty': i18n.makeString('#captcha:error-codes/challenge-is-empty') }
    
    def showCaptcha(self, callback = None):
        pass

    showCaptcha = abstractmethod(showCaptcha)
    
    def closeCaptcha(self):
        pass

    closeCaptcha = abstractmethod(closeCaptcha)
    
    def reloadCaptcha(self):
        pass

    reloadCaptcha = abstractmethod(reloadCaptcha)
    
    def setCaptchaVerified(self):
        pass

    setCaptchaVerified = abstractmethod(setCaptchaVerified)
    
    def setCaptchaServerError(self, errorCode):
        pass

    setCaptchaServerError = abstractmethod(setCaptchaServerError)
    
    def setCaptchaClientError(self, errorTest):
        pass

    setCaptchaClientError = abstractmethod(setCaptchaClientError)
    
    def isCaptchaRequired(self):
        return self._battlesTillCaptcha <= 0

    
    def getPublicKey(self):
        settings = BigWorld.player().serverSettings
        if settings.has_key('captchaKey'):
            return settings['captchaKey']

    
    def getCaptchaRegex(self):
        return BigWorld.player().serverSettings.get('reCaptchaParser', '')

    
    def verify(self, challenge, response):
        BigWorld.player().challengeCaptcha(challenge, response, self._CaptchaUI__pc_onCaptchaChecked)

    
    def tryBattlesTillCaptchaReset(self):
        if self._captchaTriesLeft > 1:
            LOG_WARNING('Client try battlesTillCaptcha reset')
            BigWorld.player().challengeCaptcha('', '', (lambda resultID, errorCode: pass))
        

    
    def startListening(self):
        BigWorld.player().stats.get('battlesTillCaptcha', self._CaptchaUI__pc_onReceiveBattlesTillCaptcha)
        BigWorld.player().stats.get('captchaTriesLeft', self._CaptchaUI__pc_onReceiveCaptchaTriesLeft)
        g_playerEvents.onEnqueueFailure += self._CaptchaUI__pe_onEnqueueFailure
        g_clientUpdateManager.addCallbacks({
            'stats.battlesTillCaptcha': self.onBattlesTillCaptcha,
            'stats.captchaTriesLeft': self.onCaptchaTriesLeft })

    
    def stopListening(self):
        g_clientUpdateManager.removeObjectCallbacks(self)
        g_playerEvents.onEnqueueFailure -= self._CaptchaUI__pe_onEnqueueFailure

    
    def _CaptchaUI__pe_onEnqueueFailure(self, errorCode, errorStr):
        if errorCode != JOIN_FAILURE.CAPTCHA:
            return None
        self.showCaptcha()
        self.setCaptchaClientError(self._CLIENT_ERROR_CODES['enqueue-failure'])

    
    def onBattlesTillCaptcha(self, value):
        self._battlesTillCaptcha = value

    
    def onCaptchaTriesLeft(self, value):
        self._captchaTriesLeft = value

    
    def _CaptchaUI__pc_onReceiveBattlesTillCaptcha(self, resultID, value):
        if resultID < 0:
            LOG_ERROR('Server return error: ', resultID, value)
            return None
        self._battlesTillCaptcha = value

    
    def _CaptchaUI__pc_onReceiveCaptchaTriesLeft(self, resultID, value):
        if resultID < 0:
            LOG_ERROR('Server return error: ', resultID, value)
            return None
        self._captchaTriesLeft = value

    
    def _CaptchaUI__pc_onCaptchaChecked(self, resultID, errorCode):
        if resultID == AccountCommands.RES_SUCCESS:
            self.setCaptchaVerified()
        elif self._captchaTriesLeft > 0:
            self.reloadCaptcha()
        
        self.setCaptchaServerError(errorCode)



