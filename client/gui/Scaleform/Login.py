# Source Generated with Decompyle++
# File: Login.pyc (Python 2.6)

import BigWorld
import ResMgr
import Settings
import MusicController
from account_helpers import pwd_token
from adisp import process
import constants
import sys
from ConnectionManager import connectionManager
from debug_utils import LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_ERROR
from gui.BattleContext import g_battleContext
from gui.Scaleform import SCALEFORM_WALLPAPER_PATH
from helpers import i18n
from account_helpers.SteamAccount import g_steamAccount
from helpers.obfuscators import PasswordObfuscator
from helpers.links import openRegistrationWebsite, openMigrationWebsite
from helpers.time_utils import makeLocalServerTime
from gui import VERSION_FILE_PATH, GUI_SETTINGS
from gui.Scaleform.Disconnect import Disconnect
from gui.Scaleform.EULA import EULAInterface
from gui.Scaleform.Waiting import Waiting
from constants import IS_DEVELOPMENT
from external_strings_utils import isAccountLoginValid, isPasswordValid, _LOGIN_NAME_MIN_LENGTH, isAccountNameValid, _ACCOUNT_NAME_MIN_LENGTH_REG, _PASSWORD_MAX_LENGTH
from gui.Scaleform.windows import UIInterface
import random
import json
from PlayerEvents import g_playerEvents
from predefined_hosts import g_preDefinedHosts, AUTO_LOGIN_QUERY_URL, AUTO_LOGIN_QUERY_TIMEOUT

class Login(UIInterface):
    IS_FIRST_RUN = True
    _Login__APPLICATION_CLOSE_DELAY_DEFAULT = 15
    DEFAULT_PASS_LENGTH = 10
    
    def __init__(self):
        self._Login__user = ''
        self._Login__host = ''
        self._Login__pass = ''
        self._Login__token2 = ''
        self._Login__passLength = 0
        self._Login__rememberPwd = False
        self._Login__closeCallbackId = None
        self._Login__eula = EULAInterface()
        self._Login__loginQueue = False
        self._Login__kickedFromServer = False
        self._Login__capsLockState = None
        self._Login__showLoginWallpaperNode = 'showLoginWallpaper'
        UIInterface.__init__(self)

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self.uiHolder.movie.backgroundAlpha = 1
        self.uiHolder.addExternalCallbacks({
            'login.Login': self.onLogin,
            'login.Register': self.onRegister,
            'login.SetRememberPassword': self.onSetRememberPassword,
            'login.ExitFromAutoLogin': self.onExitFromAutoLogin,
            'login.EULAClose': self.steamLogin,
            'login.ConfirmUpdate': self.doUpdate,
            'login.tryCreateAnAccount': self.onTryCreateAnAccount })
        self._Login__loadUserConfig()
        g_preDefinedHosts.readScriptConfig(Settings.g_instance.scriptConfig)
        connectionManager.connectionStatusCallbacks += self._Login__handleConnectionStatus
        connectionManager.onConnected += self._Login__onConnected
        connectionManager.searchServersCallbacks += self._Login__serversFind
        connectionManager.startSearchServers()
        connectionManager.onDisconnected -= Disconnect.show
        Disconnect.hide()
        self.setOptions(g_preDefinedHosts.shortList())
        self._Login__loadVersion()
        g_playerEvents.onLoginQueueNumberReceived += self.onQueue
        g_playerEvents.onAccountBecomePlayer += self._Login__pe_onAccountBecomePlayer
        g_playerEvents.onKickWhileLoginReceived += self.handleKickWhileLogin
        Waiting.hide('loadPage')
        Waiting.close()
        MusicController.g_musicController.stopAmbient()
        MusicController.g_musicController.play(MusicController.MUSIC_EVENT_LOGIN)
        self._Login__eula.populateUI(proxy)
        self.uiHolder.call('login.ShowLicense', [
            self._Login__eula.isShowLicense()])
        self.uiHolder.call('login.isSteam', [
            g_steamAccount.isValid])
        if not self._Login__eula.isShowLicense():
            self.steamLogin()
        
        self._Login__loadRandomBgImage()
        if constants.IS_DEVELOPMENT:
            
            try:
                tmp_fil = open('GUIUnitTest.ut', 'r')
                if tmp_fil.readline().strip() != '':
                    tmp_fil.close()
                    sys.path.append('../../gui_unit_test/scripts')
                    import GUIUnitTest as GUIUnitTest
                else:
                    tmp_fil.close()
            except IOError:
                pass
            

        self._Login__capsLockCallback = BigWorld.callback(0.1, self._Login__checkCapsLockState)
        self._displayRoot = self.uiHolder.getMember('contentHolder.main')
        if self._displayRoot is not None:
            self._displayRoot.resync()
            self._displayRoot.script = self
        
        g_battleContext.lastArenaUniqueID = None

    
    def dispossessUI(self):
        if self._displayRoot is not None:
            self._displayRoot.script = None
            self._displayRoot = None
        
        if self._Login__capsLockCallback is not None:
            BigWorld.cancelCallback(self._Login__capsLockCallback)
            self._Login__capsLockCallback = None
        
        connectionManager.connectionStatusCallbacks -= self._Login__handleConnectionStatus
        connectionManager.onConnected -= self._Login__onConnected
        connectionManager.stopSearchServers()
        connectionManager.searchServersCallbacks -= self._Login__serversFind
        connectionManager.onDisconnected += Disconnect.show
        g_playerEvents.onLoginQueueNumberReceived -= self.onQueue
        g_playerEvents.onAccountBecomePlayer -= self._Login__pe_onAccountBecomePlayer
        g_playerEvents.onKickWhileLoginReceived -= self.handleKickWhileLogin
        self.uiHolder.removeExternalCallbacks('login.Login', 'login.Register', 'login.SetRememberPassword', 'login.ExitFromAutoLogin', 'login.EULAClose', 'login.ConfirmUpdate', 'login.tryCreateAnAccount')
        self._Login__eula.dispossessUI()
        UIInterface.dispossessUI(self)

    
    def _Login__loadVersion(self):
        sec = ResMgr.openSection(VERSION_FILE_PATH)
        version = i18n.makeString(sec.readString('appname')) + ' ' + sec.readString('version')
        self.call('Login.SetVersion', [
            version])

    
    def isToken(self):
        return len(self._Login__token2) > 0

    
    def resetToken(self):
        LOG_DEBUG('Token has been invalidated')
        self._Login__passLength = 0
        self._Login__token2 = ''

    
    def _Login__loadUserConfig(self):
        ds = self._Login__getUserLoginSection()
        isRememberPwd = GUI_SETTINGS.rememberPassVisible
        password = ''
        self._Login__rememberPwd = False
        if isRememberPwd:
            self._Login__rememberPwd = ds.readBool('rememberPwd', False)
        
        if ds:
            if GUI_SETTINGS.clearLoginValue:
                ds.writeString('user', '')
                ds.writeString('login', '')
            
            self._Login__user = self._Login__getUserLoginName(ds)
            self._Login__host = ds.readString('host')
            decrypt = getattr(BigWorld, 'wg_ucpdata', None)
            if 'password' in ds.keys():
                password = ds.readString('password')
                decrypt = PasswordObfuscator().unobfuscate
            else:
                password = ds.readString('pwd')
            if not isRememberPwd:
                self._Login__rememberPwd = False
                password = ''
            elif len(password) > 0 and 'rememberPwd' not in ds.keys():
                self._Login__rememberPwd = True
            else:
                self._Login__rememberPwd = ds.readBool('rememberPwd', False)
            if self._Login__rememberPwd and decrypt is not None:
                
                try:
                    password = decrypt(password)
                except (TypeError, AttributeError):
                    LOG_CURRENT_EXCEPTION()
                

            if 'token2' in ds.keys():
                token2 = ds.readString('token2')
                if len(token2):
                    separatorPos = token2.find(':')
                    if separatorPos > 0:
                        
                        try:
                            self._Login__passLength = int(token2[:separatorPos])
                        except Exception:
                            self._Login__passLength = self.DEFAULT_PASS_LENGTH

                        self._Login__passLength = min(self._Login__passLength, _PASSWORD_MAX_LENGTH)
                        self._Login__token2 = token2[separatorPos + 1:]
                        password = '*' * self._Login__passLength
                    else:
                        self._Login__token2 = ''
                
            
        
        self.call('login.setDefaultValues', [
            self._Login__user,
            password,
            self._Login__rememberPwd,
            isRememberPwd])

    
    def _Login__getUserLoginSection(self):
        up = Settings.g_instance.userPrefs
        if up.has_key(Settings.KEY_LOGIN_INFO):
            return up[Settings.KEY_LOGIN_INFO]
        return up.write(Settings.KEY_LOGIN_INFO, '')

    
    def _Login__getUserLoginName(self, loginInfoSection):
        userLogin = ''
        if 'user' in loginInfoSection.keys():
            userLogin = loginInfoSection.readString('user', '')
        elif 'login' in loginInfoSection.keys():
            userLogin = BigWorld.wg_ucpdata(loginInfoSection.readString('login', ''))
        
        return userLogin

    
    def _Login__saveUserConfig(self, user, rememberPwd, host):
        li = self._Login__getUserLoginSection()
        if not g_steamAccount.isValid:
            if not GUI_SETTINGS.clearLoginValue:
                pass
            1
            'login'(BigWorld.wg_cpdata(user), '')
            if 'user' in li.keys():
                li.deleteSection('user')
            
            if GUI_SETTINGS.rememberPassVisible:
                pass
            1
            'rememberPwd'(rememberPwd, False)
        
        li.writeString('host', host)
        self._Login__saveUserToken(self._Login__passLength, self._Login__token2)
        Settings.g_instance.save()

    
    def _Login__saveUserToken(self, passwordLength, token2):
        ds = Settings.g_instance.userPrefs[Settings.KEY_LOGIN_INFO]
        if GUI_SETTINGS.rememberPassVisible:
            pass
        rememberPwd = ds.readBool('rememberPwd', False)
        li = self._Login__getUserLoginSection()
        if len(token2):
            token2 = '%d:%s' % (passwordLength, token2)
        
        if 'pwd' in li.keys():
            li.deleteSection('pwd')
        
        if rememberPwd:
            pass
        1
        'token2'(token2, '')
        Settings.g_instance.save()

    
    def showCreateAnAccountDialog(self):
        self.call('login.ShowCreateAnAccount', [
            '#dialogs:createAnAccount/title',
            '#dialogs:createAnAccount/message',
            '#dialogs:createAnAccount/submit'])

    
    def _Login__createAnAccountResponse(self, succcess, errorMsg):
        self.call('login.CreateAnAccountResponce', [
            succcess,
            errorMsg])

    
    def onTryCreateAnAccount(self, cid, nickname):
        LOG_DEBUG('CREATE ACCOUNT: %s' % str(nickname))
        if len(nickname) < _ACCOUNT_NAME_MIN_LENGTH_REG:
            return self._Login__createAnAccountResponse(False, i18n.makeString('#menu:login/status/invalid_login_length') % {
                'count': _ACCOUNT_NAME_MIN_LENGTH_REG })
        if not isAccountNameValid(nickname):
            return self._Login__createAnAccountResponse(False, '#menu:login/status/invalid_nickname')
        host = g_preDefinedHosts.byUrl(self._Login__host)
        password = pwd_token.generate(self._Login__pass)
        urls = host.urlIterator
        if urls is not None:
            if urls.end():
                urls.cursor = 0
            
            host = urls.next()
            LOG_DEBUG('Gets next LoginApp url:', host)
        
        LOG_DEBUG('Try create an account: url=%s; login=%s; password=%s; nickName=%s' % (host.url, self._Login__user, password, nickname))
        connectionManager.connect(host.url, self._Login__user, password, host.keyPath, nickName = nickname, token2 = '')

    
    def _Login__checkCapsLockState(self):
        if self._Login__capsLockState != BigWorld.wg_isCapsLockOn():
            self._Login__capsLockState = BigWorld.wg_isCapsLockOn()
            self._Login__setCapsLockState(self._Login__capsLockState)
        
        self._Login__capsLockCallback = BigWorld.callback(0.1, self._Login__checkCapsLockState)

    
    def _Login__setCapsLockState(self, isActive):
        self.call('login.setCapsLockState', [
            isActive])

    
    def _Login__serversFind(self, servers = None):
        list = g_preDefinedHosts.shortList()
        if servers is not None:
            for (name, key) in servers:
                if not g_preDefinedHosts.predefined(key):
                    list.append((key, name))
                    continue
            
        
        self.setOptions(list)

    
    def _Login__handleConnectionStatus(self, stage, status, serverMsg, isAutoRegister):
        if stage == 1:
            handlerFunc = None
            if status == 'LOGGED_ON':
                handlerFunc = self._Login__logOnSuccess[status]
            elif isAutoRegister:
                handlerFunc = self._Login__logAutoRegisterHandlers.get(status, self._Login__logOnFailedDefaultHandler)
            else:
                handlerFunc = self._Login__logOnFailedHandlers.get(status, self._Login__logOnFailedDefaultHandler)
                if status != 'LOGIN_REJECTED_LOGIN_QUEUE':
                    self._Login__clearAutoLoginTimer()
                
                if status != 'LOGIN_REJECTED_RATE_LIMITED':
                    self._Login__resetLgTimeout()
                
                self.cancelQueue(showWaiting = False)
                g_preDefinedHosts.clearPeripheryTL()
            
            try:
                getattr(self, handlerFunc)(status, serverMsg)
            except:
                LOG_ERROR('Handle logon status error: status = %r, message = %r' % (status, serverMsg))
                LOG_CURRENT_EXCEPTION()
                Waiting.hide('login')

            if connectionManager.isUpdateClientSoftwareNeeded():
                self._Login__handleUpdateClientSoftwareNeeded()
            elif status != 'LOGGED_ON':
                connectionManager.disconnect()
            
        elif stage == 6:
            if not self._Login__kickedFromServer:
                self.cancelQueue(showWaiting = False)
            
            self._Login__setStatus(i18n.convert(i18n.makeString('#menu:login/status/disconnected')))
            connectionManager.disconnect()
        

    
    def _Login__onConnected(self):
        g_preDefinedHosts.resetQueryResult()
        self._Login__loginQueue = False
        LOG_DEBUG('onConnected')
        
        def iCallback():
            BigWorld.disconnect()
            BigWorld.clearEntitiesAndSpaces()
            g_windowsManager = g_windowsManager
            import gui.WindowsManager
            g_windowsManager.showLogin()
            Waiting.close()

        Waiting.show('enter', interruptCallback = iCallback)

    
    def _Login__handleUpdateClientSoftwareNeeded(self):
        self.call('login.updateNeeded', [])

    
    def doUpdate(self, _):
        if not BigWorld.wg_quitAndStartLauncher():
            self._Login__setStatus(i18n.convert(i18n.makeString('#menu:login/status/launchernotfound')))
        

    
    def _Login__handleMigrationNeeded(self):
        if not IS_DEVELOPMENT:
            self._Login__closeCallbackId = BigWorld.callback(self._Login__getApplicationCloseDelay(), BigWorld.quit)
            
            try:
                openMigrationWebsite(self._Login__user)
            except Exception:
                LOG_CURRENT_EXCEPTION()
            


    
    def _Login__getApplicationCloseDelay(self):
        prefs = Settings.g_instance.userPrefs
        if prefs is None:
            delay = Login._Login__APPLICATION_CLOSE_DELAY_DEFAULT
        elif not prefs.has_key(Settings.APPLICATION_CLOSE_DELAY):
            prefs.writeInt(Settings.APPLICATION_CLOSE_DELAY, Login._Login__APPLICATION_CLOSE_DELAY_DEFAULT)
        
        delay = prefs.readInt(Settings.APPLICATION_CLOSE_DELAY)
        return delay

    
    def setOptions(self, optionsList):
        options = [
            0]
        for (key, name) in enumerate(optionsList):
            if key == self._Login__host:
                options[0] = i
            
            options.append(name)
            options.append(key)
        
        self.call('login.setServersList', options)

    
    def _Login__setStatus(self, status):
        self.call('login.setErrorMessage', [
            status])
        Waiting.close()

    _Login__isAutoLoginTimerSet = False
    _Login__isAutoLoginShow = False
    _Login__autoLoginTimerID = None
    
    def _Login__setAutoLoginTimer(self, time):
        if self._Login__isAutoLoginTimerSet:
            return None
        self._Login__isAutoLoginTimerSet = True
        LOG_DEBUG('__setAutoLoginTimer', time)
        self._Login__isAutoLoginShow = True
        if time > 0:
            self._Login__autoLoginTimerID = BigWorld.callback(time, self._Login__doAutoLogin)
        else:
            self._Login__doAutoLogin()

    
    def _Login__clearAutoLoginTimer(self, clearInFlash = True):
        if self._Login__isAutoLoginTimerSet:
            LOG_DEBUG('__clearAutoLoginTimer')
            if self._Login__autoLoginTimerID is not None:
                BigWorld.cancelCallback(self._Login__autoLoginTimerID)
                self._Login__autoLoginTimerID = None
            
            self._Login__isAutoLoginTimerSet = False
        
        if self._Login__isAutoLoginShow:
            urls = g_preDefinedHosts.urlIterator(self._Login__host)
            if urls is not None:
                urls.resume()
            
            self._Login__minOrderInQueue = 0xFFFFFFFFFFFFFFFFL
            if clearInFlash:
                self.call('login.clearAutoLogin')
            
            self._Login__isAutoLoginShow = False
        

    
    def _Login__doAutoLogin(self):
        LOG_DEBUG('__doAutoLogin')
        self._Login__isAutoLoginTimerSet = False
        self._Login__autoLoginTimerID = None
        self.call('login.doAutoLogin', [])

    
    def onExitFromAutoLogin(self, *args):
        self._Login__clearAutoLoginTimer(clearInFlash = False)
        self._Login__resetLgTimeout()
        g_preDefinedHosts.resetQueryResult()

    _Login__lg_Timeout = 0
    _Login__lg_maxTimeout = 20
    _Login__lg_increment = 5
    
    def _Login__getLgNextTimeout(self):
        self._Login__lg_Timeout = min(self._Login__lg_maxTimeout, self._Login__lg_Timeout + self._Login__lg_increment)
        return self._Login__lg_Timeout

    
    def _Login__resetLgTimeout(self):
        self._Login__lg_Timeout = 0

    _Login__logOnFailedHandlers = {
        'LOGIN_REJECTED_BAN': 'handleLoginRejectedBan',
        'LOGIN_CUSTOM_DEFINED_ERROR': 'handleLoginRejectedBan',
        'LOGIN_REJECTED_RATE_LIMITED': 'handleLoginRejectedRateLimited',
        'LOGIN_REJECTED_USERS_LIMIT': 'handleLoginRejectedUsersLimited',
        'LOGIN_REJECTED_LOGINS_NOT_ALLOWED': 'handleLoginAppFailed',
        'LOGIN_REJECTED_BASEAPP_TIMEOUT': 'handleLoginAppFailed',
        'CONNECTION_FAILED': 'handleLoginAppFailed',
        'DNS_LOOKUP_FAILED': 'handleLoginAppFailed',
        'LOGIN_REJECTED_NOT_REGISTERED': 'handleNotRegistered',
        'LOGIN_REJECTED_ACTIVATING': 'handleActivating',
        'LOGIN_REJECTED_INVALID_PASSWORD': 'handleInvalidPassword' }
    _Login__logAutoRegisterHandlers = {
        'LOGIN_REJECTED_INVALID_PASSWORD': 'handleAutoRegisterInvalidPass',
        'LOGIN_REJECTED_UNABLE_TO_PARSE_JSON': 'handleAutoRegisterJSONParsingFailed',
        'LOGIN_REJECTED_ACTIVATING': 'handleAutoRegisterActivating' }
    _Login__logOnSuccess = {
        'LOGGED_ON': 'handleLogOnSuccess' }
    _Login__logOnFailedDefaultHandler = 'handleLogOnFailed'
    _Login__minOrderInQueue = 0xFFFFFFFFFFFFFFFFL
    
    def handleLogOnFailed(self, status, _):
        errorMessage = i18n.makeString('#menu:login/status/' + status)
        self._Login__setStatus(errorMessage)

    
    def handleInvalidPassword(self, status, message):
        errorMessage = i18n.makeString('#menu:login/status/' + status)
        if len(self._Login__token2):
            self.resetToken()
            self.call('login.setDefaultValues', [
                self._Login__user,
                '',
                self._Login__rememberPwd,
                GUI_SETTINGS.rememberPassVisible])
            errorMessage = i18n.makeString('#menu:login/status/SESSION_END')
        
        self._Login__setStatus(errorMessage)

    
    def handleLogOnSuccess(self, status, message):
        
        try:
            LOG_DEBUG('handleLogOnSuccess', message)
            if not len(message):
                return None
            msg_dict = json.loads(message)
            if not isinstance(msg_dict, dict):
                raise Exception, ''
            isinstance(msg_dict, dict)
        except Exception:
            self.handleLoginCustomDefinedError(status, message)
            LOG_CURRENT_EXCEPTION()
            return None

        self._Login__saveUserToken(self._Login__passLength, str(msg_dict.get('token2', '')))

    
    def handleAutoRegisterInvalidPass(self, status, message):
        self._Login__createAnAccountResponse(False, '#menu:login/status/LOGIN_REJECTED_NICKNAME_ALREADY_EXIST')
        Waiting.close()

    
    def handleAutoRegisterJSONParsingFailed(self, status, message):
        self._Login__createAnAccountResponse(False, '#menu:login/status/LOGIN_REJECTED_UNABLE_TO_PARSE_JSON')
        Waiting.close()

    
    def handleActivating(self, status, message):
        message = i18n.makeString('#waiting:message/auto_login_activating')
        self.call('login.setAutoLogin', [
            '#waiting:titles/registering',
            message,
            '#waiting:buttons/exit'])
        self._Login__setAutoLoginTimer(self._Login__getLgNextTimeout())

    
    def handleAutoRegisterActivating(self, status, message):
        self._Login__createAnAccountResponse(True, '')
        Waiting.hide('login')
        self.handleActivating(status, message)

    
    def handleNotRegistered(self, status, message):
        if constants.IS_VIETNAM:
            self.showCreateAnAccountDialog()
        
        Waiting.close()

    
    def handleLoginRejectedBan(self, status, message):
        
        try:
            LOG_DEBUG('handleLoginRejectedBan', message)
            msg_dict = json.loads(message)
            if not isinstance(msg_dict, dict):
                self.handleLoginCustomDefinedError(status, message)
                return None
            self._Login__token2 = msg_dict.get('token2', '')
            self._Login__saveUserToken(self._Login__passLength, self._Login__token2)
            json_dict = msg_dict.get('bans')
            msg_dict = json.loads(json_dict)
        except Exception:
            LOG_CURRENT_EXCEPTION()
            self.handleLoginCustomDefinedError(status, message)
            return None

        if isinstance(msg_dict, dict):
            expiryTime = int(msg_dict.get('expiryTime', 0))
            reason = msg_dict.get('reason', '').encode('utf-8')
        
        if reason == '#ban_reason:china_migration':
            self._Login__handleMigrationNeeded()
        
        if reason.startswith('#'):
            reason = i18n.makeString(reason)
        
        if expiryTime > 0:
            expiryTime = makeLocalServerTime(expiryTime)
            expiryTime = BigWorld.wg_getLongDateFormat(expiryTime) + ' ' + BigWorld.wg_getLongTimeFormat(expiryTime)
            errorMessage = i18n.makeString('#menu:login/status/LOGIN_REJECTED_BAN', time = expiryTime, reason = reason)
        else:
            errorMessage = i18n.makeString('#menu:login/status/LOGIN_REJECTED_BAN_UNLIMITED', reason = reason)
        self._Login__setStatus(errorMessage)

    
    def onQueue(self, queueNumber):
        if not self._Login__loginQueue:
            Waiting.close()
            self._Login__loginQueue = True
        
        message = i18n.makeString('#waiting:message/queue', connectionManager.serverUserName, BigWorld.wg_getIntegralFormat(queueNumber))
        self.call('login.setLoginQueue', [
            '#waiting:titles/queue',
            message,
            '#waiting:buttons/exitQueue'])

    
    def cancelQueue(self, showWaiting = True, logged = False):
        if self._Login__loginQueue:
            if showWaiting:
                Waiting.show('enter')
            
            self._Login__loginQueue = False
        
        self.call('login.cancelLoginQueue', [
            logged])

    
    def _Login__pe_onAccountBecomePlayer(self):
        self.cancelQueue(logged = True)

    
    def handleLoginCustomDefinedError(self, _, message):
        errorMessage = i18n.makeString('#menu:login/status/LOGIN_CUSTOM_DEFINED_ERROR', message)
        self._Login__setStatus(errorMessage)

    
    def handleLoginRejectedRateLimited(self, status, message):
        errorMessage = i18n.makeString('#menu:login/status/LOGIN_REJECTED_RATE_LIMITED')
        self._Login__setStatus(errorMessage)
        urls = g_preDefinedHosts.urlIterator(self._Login__host)
        if urls is not None and urls.end():
            urls.cursor = 0
        
        message = i18n.makeString('#waiting:message/autoLogin', connectionManager.serverUserName)
        self.call('login.setAutoLogin', [
            '#waiting:titles/queue',
            message,
            '#waiting:buttons/exitQueue'])
        self._Login__setAutoLoginTimer(self._Login__getLgNextTimeout())

    
    def handleKickWhileLogin(self, peripheryID):
        g_preDefinedHosts.savePeripheryTL(peripheryID)
        self._Login__kickedFromServer = True
        if peripheryID:
            pass
        1
        messageType = 'checkout_error'
        errorMessage = i18n.makeString('#system_messages:%s' % messageType)
        self._Login__setStatus(errorMessage)
        urls = g_preDefinedHosts.urlIterator(self._Login__host)
        if urls is not None and urls.end():
            urls.cursor = 0
        
        message = i18n.makeString('#waiting:message/%s' % messageType, connectionManager.serverUserName)
        self.call('login.setAutoLogin', [
            '#waiting:titles/%s' % messageType,
            message,
            '#waiting:buttons/cease'])
        self._Login__setAutoLoginTimer(self._Login__getLgNextTimeout())

    
    def handleLoginRejectedUsersLimited(self, status, message):
        errorMessage = i18n.makeString('#menu:login/status/LOGIN_REJECTED_USERS_LIMIT')
        self._Login__setStatus(errorMessage)

    
    def _Login__loginToNextLoginApp(self):
        urls = g_preDefinedHosts.urlIterator(self._Login__host)
        result = False
        if urls is not None:
            result = not urls.end()
            if result:
                Waiting.hide('login')
                self._Login__setAutoLoginTimer(0)
            else:
                urls.cursor = 0
        
        return result

    
    def handleLoginAppFailed(self, status, message):
        if self.handleAutoLoginQueryFailed(status):
            return None
        if not self._Login__loginToNextLoginApp():
            self.handleLogOnFailed(status, message)
        

    
    def handleAutoLoginQueryFailed(self, status):
        result = False
        if AUTO_LOGIN_QUERY_URL == self._Login__host:
            result = True
            Waiting.hide('login')
            self.call('login.setAutoLogin', [
                '#waiting:titles/auto_login_query_failed',
                i18n.makeString('#waiting:message/auto_login_query_failed', server = connectionManager.serverUserName, reason = i18n.makeString('#menu:login/status/{0:>s}'.format(status))),
                '#waiting:buttons/cease'])
            self._Login__setAutoLoginTimer(AUTO_LOGIN_QUERY_TIMEOUT)
        
        return result

    
    def steamLogin(self, callbackId = None):
        if Login.IS_FIRST_RUN and g_steamAccount.isValid:
            Login.IS_FIRST_RUN = False
            self._Login__loadUserConfig()
            host = self._Login__host
            if not g_preDefinedHosts.predefined(host):
                host = g_preDefinedHosts.first().url
            
            self.onLogin(0, '', '', host)
        

    
    def _Login__loadRandomBgImage(self):
        wallpapperSettings = self._Login__readUserPreferenceLogin()
        wallpaperFiles = self._Login__getWallpapersList()
        BG_IMAGES_PATH = '../maps/login/%s.png'
        if wallpapperSettings['show'] and len(wallpaperFiles) > 0:
            if len(wallpaperFiles) == 1:
                newfile = wallpaperFiles[0]
            else:
                newfile = ''
                while True:
                    newfile = random.choice(wallpaperFiles)
                    if newfile != wallpapperSettings['filename']:
                        break
                        continue
            self._Login__saveUserPreferencesLogin(newfile)
            bgImage = BG_IMAGES_PATH % newfile
        else:
            bgImage = BG_IMAGES_PATH % '__login_bg'
            wallpapperSettings['show'] = False
        self.uiHolder.call('login.showWallpaper', [
            wallpapperSettings['show'],
            bgImage])

    
    def _Login__getWallpapersList(self):
        result = []
        ds = ResMgr.openSection(SCALEFORM_WALLPAPER_PATH)
        for filename in ds.keys():
            if filename[-4:] == '.png' and filename[0:2] != '__':
                result.append(filename[0:-4])
                continue
        
        return result

    
    def _Login__readUserPreferenceLogin(self):
        result = {
            'show': True,
            'filename': '' }
        userPrefs = Settings.g_instance.userPrefs
        ds = None
        if not userPrefs.has_key(Settings.KEY_LOGINPAGE_PREFERENCES):
            userPrefs.write(Settings.KEY_LOGINPAGE_PREFERENCES, '')
            self._Login__saveUserPreferencesLogin(result['filename'])
        else:
            ds = userPrefs[Settings.KEY_LOGINPAGE_PREFERENCES]
            result['filename'] = ds.readString('lastLoginBgImage', '')
        if ds is None:
            ds = userPrefs[Settings.KEY_LOGINPAGE_PREFERENCES]
        
        if not ds.has_key(self._Login__showLoginWallpaperNode):
            self._Login__createNodeShowWallpaper()
        
        result['show'] = ds.readBool(self._Login__showLoginWallpaperNode, True)
        return result

    
    def _Login__saveUserPreferencesLogin(self, filename):
        ds = Settings.g_instance.userPrefs[Settings.KEY_LOGINPAGE_PREFERENCES]
        ds.writeString('lastLoginBgImage', filename)

    
    def _Login__createNodeShowWallpaper(self):
        ds = Settings.g_instance.userPrefs[Settings.KEY_LOGINPAGE_PREFERENCES]
        ds.writeBool(self._Login__showLoginWallpaperNode, True)

    
    def onLogin(self, _, user, password, host):
        self._Login__kickedFromServer = False
        if self._Login__closeCallbackId:
            BigWorld.cancelCallback(self._Login__closeCallbackId)
            self._Login__closeCallbackId = None
        
        if g_steamAccount.isValid:
            (user, password) = g_steamAccount.getCredentials()
        else:
            user = user.lower().strip()
            if len(user) < _LOGIN_NAME_MIN_LENGTH:
                self._Login__setStatus(i18n.makeString('#menu:login/status/invalid_login_length') % {
                    'count': _LOGIN_NAME_MIN_LENGTH })
                return None
            if not isAccountLoginValid(user) and not IS_DEVELOPMENT:
                self._Login__setStatus(i18n.makeString('#menu:login/status/invalid_login'))
                return None
            password = password.strip()
            if not isPasswordValid(password) and not IS_DEVELOPMENT and not len(self._Login__token2):
                self._Login__setStatus(i18n.makeString('#menu:login/status/invalid_password'))
                return None
        Waiting.show('login')
        self._Login__host = host
        self._Login__user = user
        self._Login__passLength = len(password)
        if constants.IS_VIETNAM:
            self._Login__pass = password
        
        self._Login__saveUserConfig(user, self._Login__rememberPwd, self._Login__host)
        password = pwd_token.generate(password)
        if len(self._Login__token2):
            password = ''
        
        if AUTO_LOGIN_QUERY_URL == host:
            (not IS_DEVELOPMENT, not len(self._Login__token2), g_preDefinedHosts.autoLoginQuery)((lambda host: connectionManager.connect(host.url, user, password, host.keyPath, nickName = None, token2 = self._Login__token2)))
            return None
        host = g_preDefinedHosts.byUrl(host)
        urls = host.urlIterator
        if urls is not None:
            if urls.end():
                urls.cursor = 0
            
            host = urls.next()
            LOG_DEBUG('Gets next LoginApp url:', host)
        
        connectionManager.connect(host.url, user, password, host.keyPath, nickName = None, token2 = self._Login__token2)

    
    def onRegister(self, _):
        openRegistrationWebsite()

    
    def onSetRememberPassword(self, _, remember):
        self._Login__rememberPwd = bool(remember)



