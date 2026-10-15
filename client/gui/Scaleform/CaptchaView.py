# Source Generated with Decompyle++
# File: CaptchaView.pyc (Python 2.6)

from gui import SystemMessages
from helpers import i18n
import BigWorld
from debug_utils import LOG_CURRENT_EXCEPTION, LOG_DEBUG
from gui.CaptchaUI import CaptchaUI
from gui.Scaleform.windows import UIInterface
from gui.Scaleform.Waiting import Waiting
import time
import threading
CAPTCHA_IMAGE_NAME = 'captcha-cache-%s'
CAPTCHA_IMAGE_URL = 'img://' + CAPTCHA_IMAGE_NAME
CAPTCHA_TRIES_LEFT_NOTIFY_THESHOLD = 1

class CaptchaImageWorker(threading.Thread):
    
    def __init__(self, sharedObj, callbackName):
        super(CaptchaImageWorker, self).__init__()
        self.sharedObj = sharedObj
        self.callbackName = callbackName

    
    def __del__(self):
        LOG_DEBUG('CaptchaImageWorker deleted')

    
    def run(self):
        if self.sharedObj is None:
            return None
        (binaryData, challenge) = self.sharedObj._api.getImageSource(self.sharedObj.getPublicKey(), self.sharedObj.getCaptchaRegex())
        if binaryData is None and len(binaryData) == 0 or len(challenge) == 0:
            getattr(self.sharedObj, self.callbackName)(None)
            self.sharedObj = None
            return None
        
        try:
            imageID = CAPTCHA_IMAGE_NAME % self.sharedObj.generateImageID()
            BigWorld.wg_addTempScaleformTexture(imageID, binaryData)
        except AttributeError:
            len(challenge) == 0
            self.sharedObj is None
            LOG_CURRENT_EXCEPTION()
            challenge = None
        except:
            len(challenge) == 0

        getattr(self.sharedObj, self.callbackName)(challenge)
        self.sharedObj = None



class CaptchaView(CaptchaUI, UIInterface):
    _challenge = None
    _CaptchaView__callback = None
    _CaptchaView__imageID = 0
    _CaptchaView__tryReset = False
    
    def generateImageID(self):
        self._CaptchaView__imageID = int(time.time())
        return self._CaptchaView__imageID

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self.startListening()
        self.uiHolder.addExternalCallbacks({
            'CAPTCHA.ReloadImage': self.onReloadImage,
            'CAPTCHA.HandleClose': self.onHandleClose,
            'CAPTCHA.VerifyResponse': self.onVerifyResponse })

    
    def dispossessUI(self):
        self.stopListening()
        self.uiHolder.removeExternalCallbacks('CAPTCHA.ReloadImage', 'CAPTCHA.HandleClose', 'CAPTCHA.VerifyResponse')
        UIInterface.dispossessUI(self)
        self._CaptchaView__clearData()

    
    def _CaptchaView__setCaptchaImageSource(self):
        (width, height) = self._api._IMAGE_SIZE
        self.uiHolder.call('CAPTCHA.SetImageUrl', [
            CAPTCHA_IMAGE_URL % self._CaptchaView__imageID,
            width,
            height])

    
    def _CaptchaView__clearData(self):
        self._challenge = None
        self._CaptchaView__callback = None

    
    def showCaptcha(self, callback = None):
        if self.getPublicKey() is None:
            SystemMessages.pushI18nMessage('#captcha:error-codes/public-key-empty', type = SystemMessages.SM_TYPE.Error)
            return None
        Waiting.show('requestCaptcha')
        self._CaptchaView__callback = callback
        self.uiHolder.call('common.showCaptcha')
        CaptchaImageWorker(self, '_CaptchaView__afterImageCreate').start()

    
    def _CaptchaView__afterImageCreate(self, challenge):
        if challenge is not None:
            self._challenge = challenge
            self._CaptchaView__tryReset = False
            self._CaptchaView__setCaptchaImageSource()
            if self._captchaTriesLeft <= CAPTCHA_TRIES_LEFT_NOTIFY_THESHOLD:
                if self._captchaTriesLeft > 0:
                    pass
                1
                errorText = '#captcha:notification/remains-to-attempt'(self._captchaTriesLeft, 0)
                self.uiHolder.call('CAPTCHA.SetErrorMessage', [
                    errorText])
            
        else:
            self.closeCaptcha()
            SystemMessages.pushI18nMessage('#captcha:error-codes/image-internal-error', type = SystemMessages.SM_TYPE.Error)
            if not self._CaptchaView__tryReset:
                self._CaptchaView__tryReset = True
                self.tryBattlesTillCaptchaReset()
            
        Waiting.close()

    
    def closeCaptcha(self):
        self.uiHolder.call('common.closeCaptcha')
        self._CaptchaView__clearData()

    
    def reloadCaptcha(self):
        if self.getPublicKey() is None:
            SystemMessages.pushI18nMessage('#captcha:error-codes/public-key-empty', type = SystemMessages.SM_TYPE.Error)
            return None
        Waiting.show('reloadCaptcha')
        CaptchaImageWorker(self, '_CaptchaView__afterImageReload').start()

    
    def _CaptchaView__afterImageReload(self, challenge):
        if challenge is not None:
            self._challenge = challenge
            self._CaptchaView__setCaptchaImageSource()
        else:
            self.closeCaptcha()
            SystemMessages.pushI18nMessage('#captcha:error-codes/image-internal-error', type = SystemMessages.SM_TYPE.Error)
        Waiting.hide('reloadCaptcha')

    
    def setCaptchaVerified(self):
        Waiting.hide('verifyCaptcha')
        if self._CaptchaView__callback is not None:
            self._CaptchaView__callback()
        
        self.closeCaptcha()

    
    def setCaptchaServerError(self, errorCode):
        if Waiting.isVisible():
            Waiting.hide('verifyCaptcha')
        
        errorText = self._api.getI18nServerErrorText(errorCode)
        if errorCode == self._api._RESPONSE_IS_INCORRECT_CODE:
            triesLeftString = i18n.makeString('#captcha:notification/remains-to-attempt', self._captchaTriesLeft)
            errorText = '{0:>s} {1:>s}'.format(errorText, triesLeftString)
        
        self.uiHolder.call('CAPTCHA.SetErrorMessage', [
            errorText])

    
    def setCaptchaClientError(self, errorText):
        self.uiHolder.call('CAPTCHA.SetErrorMessage', [
            errorText])

    
    def onReloadImage(self, _):
        self.reloadCaptcha()

    
    def onHandleClose(self, _):
        self._CaptchaView__clearData()
        self.uiHolder.movie.invoke(('loadHangar',))

    
    def onVerifyResponse(self, _, response):
        response = response.strip()
        if self._challenge is None:
            self.setCaptchaClientError(self._CLIENT_ERROR_CODES['challenge-is-empty'])
            return None
        if not len(response):
            self.setCaptchaClientError(self._CLIENT_ERROR_CODES['challenge-is-empty'])
            return None
        Waiting.show('verifyCaptcha')
        self.verify(self._challenge, response)



