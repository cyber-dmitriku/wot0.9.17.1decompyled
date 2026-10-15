# Source Generated with Decompyle++
# File: ConnectionManager.pyc (Python 2.6)

from constants import CLIENT_INACTIVITY_TIMEOUT
import json
import hashlib
import BigWorld
from Event import Event
from Singleton import Singleton
from enumerations import Enumeration
from debug_utils import *
from predefined_hosts import g_preDefinedHosts
from functools import partial
import constants
CONNECTION_STATUS = Enumeration('Connection status', ('disconnected', 'connected', 'connectionInProgress'))

def getHardwareID():
    import ResMgr as ResMgr
    import Settings as Settings
    up = Settings.g_instance.userPrefs
    loginInfo = None
    if up.has_key(Settings.KEY_LOGIN_INFO):
        loginInfo = up[Settings.KEY_LOGIN_INFO]
    else:
        loginInfo = up.write(Settings.KEY_LOGIN_INFO, '')
    prevSalt = loginInfo.readString('salt', '')
    newSalt = BigWorld.wg_cpsalt(prevSalt)
    loginInfo.writeString('salt', newSalt)
    return newSalt


def md5hex(concealed_value):
    m = hashlib.md5()
    m.update(concealed_value)
    return m.hexdigest()


class AUTH_METHODS:
    BASIC = 'basic'
    EBANK = 'ebank'
    TOKEN2 = 'token2'


class ConnectionManager(Singleton):
    
    def instance():
        return ConnectionManager()

    instance = staticmethod(instance)
    
    def _singleton_init(self):
        self._ConnectionManager__host = g_preDefinedHosts._makeHostItem('', '')
        self.searchServersCallbacks = Event()
        self.connectionStatusCallbacks = Event()
        self.connectionStatusCallbacks += self._ConnectionManager__connectionStatusCallback
        self._ConnectionManager__connectionStatus = CONNECTION_STATUS.disconnected
        self.onConnected = Event()
        self.onDisconnected = Event()
        self._ConnectionManager__rawStatus = ''
        self._ConnectionManager__loginName = None
        BigWorld.serverDiscovery.changeNotifier = self._searchServersHandler

    
    def startSearchServers(self):
        if constants.IS_DEVELOPMENT:
            BigWorld.serverDiscovery.searching = 1
        

    
    def stopSearchServers(self):
        if constants.IS_DEVELOPMENT:
            BigWorld.serverDiscovery.searching = 0
        

    
    def _searchServersHandler(self):
        
        def _serverDottedHost(ip):
            return '%d.%d.%d.%d' % (ip >> 24 & 255, ip >> 16 & 255, ip >> 8 & 255, ip >> 0 & 255)

        
        def _serverNetName(details):
            name = _serverDottedHost(details.ip)
            if details.port:
                name += ':%d' % details.port
                return name

        
        def _serverNiceName(details):
            name = details.hostName
            if not name:
                name = _serverNetName(details)
            elif details.port:
                name += ':%d' % details.port
            
            if details.ownerName:
                name += ' (' + details.ownerName + ')'
            
            return name

        continue
        servers = [ (_serverNiceName(server), server.serverString) for server in BigWorld.serverDiscovery.servers ]
        self.searchServersCallbacks(servers)

    
    def connect(self, url, login, password, publicKeyPath = None, nickName = None, token2 = ''):
        self.disconnect()
        LOG_DEBUG('login: %s; pass: %s; name: %s; token: %s' % (login, password, nickName, token2))
        if len(login) > 0 and url is not None:
            self._ConnectionManager__setConnectionStatus(CONNECTION_STATUS.connectionInProgress)
            if constants.IS_VIETNAM:
                pass
            1
            authMethod = AUTH_METHODS.BASIC
            dct = {
                'login': login,
                'auth_method': authMethod,
                'session': md5hex(getHardwareID()) }
            if nickName is not None:
                dct['nickname'] = nickName
                dct['auto_registration'] = 'true'
            
            if token2:
                dct['token2'] = token2
                dct['auth_method'] = AUTH_METHODS.TOKEN2
            
            
            class LoginInfo:
                pass

            loginInfo = LoginInfo()
            loginInfo.username = json.dumps(dct).encode('utf8')
            loginInfo.password = password
            loginInfo.inactivityTimeout = CLIENT_INACTIVITY_TIMEOUT
            if publicKeyPath is not None:
                loginInfo.publicKeyPath = publicKeyPath
            
            if constants.IS_DEVELOPMENT and login[0] == '@':
                
                try:
                    loginInfo.username = login[1:]
                except Exception:
                    loginInfo.username = login
                

            BigWorld.connect(url, loginInfo, partial(self.connectionWatcher, nickName is not None))
            self._ConnectionManager__setConnectionStatus(CONNECTION_STATUS.connectionInProgress)
            self._ConnectionManager__loginName = login
            if g_preDefinedHosts.predefined(url):
                host = g_preDefinedHosts.byUrl(url)
                self._ConnectionManager__host = host
            else:
                for server in BigWorld.serverDiscovery.servers:
                    if server.serverString == url:
                        self._ConnectionManager__host = self._ConnectionManager__host._replace(name = server.ownerName)
                        break
                        continue
                
        

    
    def disconnect(self):
        if not self.isDisconnected():
            BigWorld.disconnect()
        

    
    def serverUserName(self):
        return self._ConnectionManager__host.name

    serverUserName = property(serverUserName)
    
    def peripheryID(self):
        return self._ConnectionManager__host.peripheryID

    peripheryID = property(peripheryID)
    
    def areaID(self):
        if not self.isDisconnected():
            return self._ConnectionManager__host.areaID

    areaID = property(areaID)
    
    def loginName(self):
        if not self.isDisconnected():
            return self._ConnectionManager__loginName

    loginName = property(loginName)
    
    def connectionWatcher(self, isAutoRegister, stage, status, serverMsg):
        self.connectionStatusCallbacks(stage, status, serverMsg, isAutoRegister)

    
    def _ConnectionManager__connectionStatusCallback(self, stage, status, serverMsg, isAutoRegister):
        LOG_MX('__connectionStatusCallback', stage, status, serverMsg)
        self._ConnectionManager__rawStatus = status
        if stage == 0:
            pass
        1
        if stage == 1:
            if status != 'LOGGED_ON':
                self._ConnectionManager__setConnectionStatus(CONNECTION_STATUS.disconnected)
            
        elif stage == 2:
            self._ConnectionManager__setConnectionStatus(CONNECTION_STATUS.connected)
            self.onConnected()
        elif stage == 6:
            self._ConnectionManager__setConnectionStatus(CONNECTION_STATUS.disconnected)
            self.onDisconnected()
        else:
            LOG_UNEXPECTED('stage:%d, status:%s, serverMsg:%s' % (stage, status, serverMsg))

    
    def _ConnectionManager__setConnectionStatus(self, status):
        self._ConnectionManager__connectionStatus = status

    
    def isDisconnected(self):
        return self._ConnectionManager__connectionStatus != CONNECTION_STATUS.connected

    
    def isUpdateClientSoftwareNeeded(self):
        return self._ConnectionManager__rawStatus in ('LOGIN_BAD_PROTOCOL_VERSION', 'LOGIN_REJECTED_BAD_DIGEST')



def _getClientUpdateUrl():
    import ResMgr
    import Settings
    updateUrl = Settings.g_instance.scriptConfig.readString(Settings.KEY_UPDATE_URL)
    return updateUrl

connectionManager = ConnectionManager.instance()

