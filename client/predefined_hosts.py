# Source Generated with Decompyle++
# File: predefined_hosts.pyc (Python 2.6)

import BigWorld
import ResMgr
import base64
import pickle
import random
import time
import threading
from collections import namedtuple
import constants
from debug_utils import LOG_CURRENT_EXCEPTION, LOG_DEBUG, LOG_WARNING
import Settings
from helpers import i18n
from urllib import urlencode
import urllib2
if not constants.IS_DEVELOPMENT:
    pass
AUTO_LOGIN_QUERY_ENABLED = not (constants.IS_CHINA)
AUTO_LOGIN_QUERY_URL = 'auto.login.app:0000'
AUTO_LOGIN_QUERY_TIMEOUT = 5
STORED_AS_RECOMMEND_DELTA = 15 * 60

class HOST_AVAILABILITY(object):
    NOT_AVAILABLE = -1
    NOT_RECOMMENDED = 0
    RECOMMENDED = 1


class AUTO_LOGIN_QUERY_STATE(object):
    DEFAULT = 0
    START = 1
    PING_PERFORMED = 2
    CSIS_RESPONSE_RECEIVED = 4
    COMPLETED = START | PING_PERFORMED | CSIS_RESPONSE_RECEIVED

_csisQueryMutex = threading.Lock()

def _CSISResponseParser(out):
    result = { }
    root = ResMgr.DataSection().createSectionFromString(out)
    itemsSec = None
    if root is not None:
        itemsSec = root['items']
    
    if itemsSec is not None:
        for (_, subSec) in itemsSec.items():
            type = subSec.readString('type')
            name = subSec.readInt('name')
            if type == 'periphery' and name:
                result[name] = subSec.readInt('availability', HOST_AVAILABILITY.NOT_AVAILABLE)
                continue
        
    
    return result


class _CSISRequestWorker(threading.Thread):
    
    def __init__(self, url, callback, params = None):
        super(_CSISRequestWorker, self).__init__()
        self._CSISRequestWorker__url = url
        self._CSISRequestWorker__callback = callback
        self._CSISRequestWorker__params = params

    
    def _makeUrl(self):
        url = self._CSISRequestWorker__url
        if self._CSISRequestWorker__params is not None and len(self._CSISRequestWorker__params):
            data = urlencode(map((lambda param: ('periphery', param)), self._CSISRequestWorker__params))
            url = '{0:>s}?{1:>s}'.format(self._CSISRequestWorker__url, data)
        
        return url

    
    def run(self):
        if self._CSISRequestWorker__callback is None:
            return None
        response = { }
        info = None
        
        try:
            url = self._makeUrl()
            LOG_DEBUG('CSIS url', url)
            req = urllib2.Request(url = url)
            urllib2.build_opener(urllib2.HTTPHandler())
            info = urllib2.urlopen(req)
            if info.code == 200 and info.headers.type == 'text/xml':
                response = _CSISResponseParser(info.read())
        except IOError:
            self._CSISRequestWorker__callback is None
            LOG_CURRENT_EXCEPTION()
        except:
            self._CSISRequestWorker__callback is None
        finally:
            if info is not None:
                info.close()
            

        _csisQueryMutex.acquire()
        
        try:
            self._CSISRequestWorker__callback(response)
        finally:
            self._CSISRequestWorker__callback = None
            _csisQueryMutex.release()




class _LoginAppUrlIterator(list):
    
    def __init__(self, *args):
        list.__init__(self, *args)
        self.cursor = 0
        if len(self) > 0:
            pass
        1
        self.primary = None
        self._LoginAppUrlIterator__lock = False
        random.shuffle(self)

    
    def end(self):
        return self.cursor >= len(self)

    
    def suspend(self):
        if self.cursor > 0 and not (self._LoginAppUrlIterator__lock):
            self.cursor -= 1
        
        self._LoginAppUrlIterator__lock = True

    
    def resume(self):
        self._LoginAppUrlIterator__lock = False

    
    def next(self):
        value = self[self.cursor]
        if not self._LoginAppUrlIterator__lock:
            self.cursor += 1
        
        return value


_HostItem = namedtuple('HostItem', ' '.join([
    'name',
    'url',
    'urlIterator',
    'keyPath',
    'areaID',
    'peripheryID']))

class _PreDefinedHostList(object):
    
    def __init__(self):
        super(_PreDefinedHostList, self).__init__()
        self._hosts = []
        self._urlMap = { }
        self._nameMap = { }
        self._peripheryMap = { }
        self._isDataLoaded = False
        self._PreDefinedHostList__pingResult = { }
        self._PreDefinedHostList__csisUrl = ''
        self._PreDefinedHostList__csisResponse = { }
        self._PreDefinedHostList__queryCallback = None
        self._PreDefinedHostList__queryState = AUTO_LOGIN_QUERY_STATE.DEFAULT
        self._PreDefinedHostList__recommended = []
        self._PreDefinedHostList__setPingCallback = False
        
        try:
            BigWorld.Pinger.setOnPingCallback(self._PreDefinedHostList__onPingPerformed)
            self._PreDefinedHostList__setPingCallback = True
        except AttributeError:
            LOG_CURRENT_EXCEPTION()


    
    def fini(self):
        self._hosts = []
        self._urlMap.clear()
        self._nameMap.clear()
        self._peripheryMap.clear()
        self._isDataLoaded = False
        self._PreDefinedHostList__pingResult.clear()
        self._PreDefinedHostList__csisResponse.clear()
        self._PreDefinedHostList__csisUrl = ''
        self._PreDefinedHostList__queryCallback = None
        self._PreDefinedHostList__queryState = AUTO_LOGIN_QUERY_STATE.DEFAULT
        self._PreDefinedHostList__setPingCallback = False
        
        try:
            BigWorld.Pinger.clearOnPingCallback()
        except AttributeError:
            LOG_CURRENT_EXCEPTION()


    
    def _makeHostItem(self, name, url, urlIterator = None, keyPath = None, areaID = None, peripheryID = 0):
        return _HostItem(name, url, urlIterator, keyPath, areaID, peripheryID)

    
    def _PreDefinedHostList__ping(self):
        if not self._PreDefinedHostList__setPingCallback:
            self._PreDefinedHostList__onPingPerformed([])
            return None
        
        try:
            peripheries = map((lambda host: host.url), self.peripheries())
            LOG_DEBUG('Ping starting', peripheries)
            BigWorld.Pinger.ping(peripheries)
        except (AttributeError, TypeError):
            LOG_CURRENT_EXCEPTION()
            self._PreDefinedHostList__onPingPerformed([])


    
    def _PreDefinedHostList__onPingPerformed(self, result):
        LOG_DEBUG('Ping performed', result)
        
        try:
            self._PreDefinedHostList__pingResult = dict(result)
            self._PreDefinedHostList__autoLoginQueryCompleted(AUTO_LOGIN_QUERY_STATE.PING_PERFORMED)
        except Exception:
            LOG_CURRENT_EXCEPTION()
            self._PreDefinedHostList__pingResult = { }


    
    def _PreDefinedHostList__sendCSISQuery(self):
        if len(self._PreDefinedHostList__csisUrl):
            peripheries = map((lambda host: host.peripheryID), self.peripheries())
            LOG_DEBUG('CSIS query sending', peripheries)
            _CSISRequestWorker(self._PreDefinedHostList__csisUrl, self._PreDefinedHostList__receiveCSISResponse, peripheries).start()
        else:
            LOG_DEBUG('CSIS url is not defined - ignore')
            self._PreDefinedHostList__csisResponse = { }
            self._PreDefinedHostList__autoLoginQueryCompleted(AUTO_LOGIN_QUERY_STATE.CSIS_RESPONSE_RECEIVED)

    
    def _PreDefinedHostList__receiveCSISResponse(self, response):
        LOG_DEBUG('CSIS query received', response)
        self._PreDefinedHostList__csisResponse = response
        self._PreDefinedHostList__autoLoginQueryCompleted(AUTO_LOGIN_QUERY_STATE.CSIS_RESPONSE_RECEIVED)

    
    def _PreDefinedHostList__autoLoginQueryCompleted(self, state):
        if not self._PreDefinedHostList__queryState & state:
            self._PreDefinedHostList__queryState |= state
        
        if self._PreDefinedHostList__queryState == AUTO_LOGIN_QUERY_STATE.COMPLETED:
            host = self._determineRecommendHost()
            LOG_DEBUG('Recommended host', host)
            self._PreDefinedHostList__queryState = AUTO_LOGIN_QUERY_STATE.DEFAULT
            self._PreDefinedHostList__queryCallback(host)
            self._PreDefinedHostList__queryCallback = None
        

    
    def _PreDefinedHostList__filterRecommendedByPing(self, recommended):
        result = recommended
        filtered = filter((lambda item: item[1] > -1), recommended)
        if len(filtered):
            minPingTime = min(filtered, key = (lambda item: item[1]))[1]
            maxPingTime = 1.2 * minPingTime
            result = (filter,)((lambda item: item[1] < maxPingTime), filtered)
        
        return result

    
    def _PreDefinedHostList__choiceFromRecommended(self):
        recommended = random.choice(self._PreDefinedHostList__recommended)
        self._PreDefinedHostList__recommended = (filter,)((lambda item: item != recommended), self._PreDefinedHostList__recommended)
        return recommended[0]

    
    def _determineRecommendHost(self):
        defAvail = HOST_AVAILABILITY.NOT_AVAILABLE
        pResGetter = self._PreDefinedHostList__pingResult.get
        csisResGetter = self._PreDefinedHostList__csisResponse.get
        queryResult = (None, None, map)((lambda host: (host, pResGetter(host.url, -1), csisResGetter(host.peripheryID, defAvail))), self.peripheries())
        self._PreDefinedHostList__recommended = filter((lambda item: item[2] == HOST_AVAILABILITY.RECOMMENDED), queryResult)
        if not len(self._PreDefinedHostList__recommended):
            self._PreDefinedHostList__recommended = filter((lambda item: item[2] == HOST_AVAILABILITY.NOT_RECOMMENDED), queryResult)
        
        recommendLen = len(self._PreDefinedHostList__recommended)
        if not recommendLen:
            if len(queryResult) > 1:
                LOG_DEBUG('List of recommended is empty. Gets host by ping')
                self._PreDefinedHostList__recommended = self._PreDefinedHostList__filterRecommendedByPing(queryResult)
                LOG_DEBUG('Recommended by ping', self._PreDefinedHostList__recommended)
                result = self._PreDefinedHostList__choiceFromRecommended()
            else:
                LOG_DEBUG('Gets first as recommended')
                result = self.first()
        else:
            LOG_DEBUG('Recommended by CSIS', self._PreDefinedHostList__recommended)
            if recommendLen > 1:
                self._PreDefinedHostList__recommended = self._PreDefinedHostList__filterRecommendedByPing(self._PreDefinedHostList__recommended)
                LOG_DEBUG('Recommended by ping', self._PreDefinedHostList__recommended)
            
            result = self._PreDefinedHostList__choiceFromRecommended()
        return result

    
    def autoLoginQuery(self, callback):
        if callback is None:
            LOG_WARNING('Callback is not defined.')
            return None
        if self._PreDefinedHostList__queryState != AUTO_LOGIN_QUERY_STATE.DEFAULT:
            LOG_WARNING('Auto login query in process.')
            return None
        if len(self._hosts) < 2:
            callback(self.first())
            return None
        (peripheryID, expired) = self.readPeripheryTL()
        if peripheryID > 0 and expired > 0:
            if expired > time.time():
                host = self.periphery(peripheryID)
                if host is not None:
                    LOG_DEBUG('Recommended host taken from cache', host)
                    callback(host)
                    return None
            
        
        if len(self._PreDefinedHostList__recommended):
            LOG_DEBUG('Gets recommended from previous query', self._PreDefinedHostList__recommended)
            host = self._PreDefinedHostList__choiceFromRecommended()
            LOG_DEBUG('Recommended host', host)
            callback(host)
            return None
        self._PreDefinedHostList__queryState = AUTO_LOGIN_QUERY_STATE.START
        self._PreDefinedHostList__csisResponse.clear()
        self._PreDefinedHostList__queryCallback = callback
        self._PreDefinedHostList__ping()
        self._PreDefinedHostList__sendCSISQuery()

    
    def resetQueryResult(self):
        self._PreDefinedHostList__recommended = []
        self._PreDefinedHostList__pingResult.clear()
        self._PreDefinedHostList__csisResponse.clear()

    
    def savePeripheryTL(self, peripheryID, delta = STORED_AS_RECOMMEND_DELTA):
        if not AUTO_LOGIN_QUERY_ENABLED or not peripheryID:
            return None
        
        try:
            loginSec = Settings.g_instance.userPrefs[Settings.KEY_LOGIN_INFO]
            if loginSec is not None:
                value = base64.b64encode(pickle.dumps((peripheryID, time.time() + delta)))
                loginSec.writeString('peripheryLifeTime', value)
                Settings.g_instance.save()
        except Exception:
            not peripheryID
            LOG_CURRENT_EXCEPTION()
        except:
            not peripheryID


    
    def readPeripheryTL(self):
        if not AUTO_LOGIN_QUERY_ENABLED:
            return (0, 0)
        result = (0, 0)
        
        try:
            loginSec = Settings.g_instance.userPrefs[Settings.KEY_LOGIN_INFO]
            if loginSec is not None:
                value = loginSec.readString('peripheryLifeTime')
                if len(value):
                    value = pickle.loads(base64.b64decode(value))
                    if len(value) > 1:
                        result = value
                    
                
        except Exception:
            result = ('', 0)
            LOG_CURRENT_EXCEPTION()

        return result

    
    def clearPeripheryTL(self):
        if not AUTO_LOGIN_QUERY_ENABLED:
            return None
        
        try:
            loginSec = Settings.g_instance.userPrefs[Settings.KEY_LOGIN_INFO]
            if loginSec is not None:
                loginSec.writeString('peripheryLifeTime', '')
                Settings.g_instance.save()
        except Exception:
            LOG_CURRENT_EXCEPTION()


    
    def readScriptConfig(self, dataSection):
        if self._isDataLoaded or dataSection is None:
            return None
        self._PreDefinedHostList__csisUrl = dataSection.readString('csisUrl')
        self._hosts = []
        self._urlMap.clear()
        self._nameMap.clear()
        self._peripheryMap.clear()
        loginSection = dataSection['login']
        if loginSection is None:
            return None
        for (name, subSec) in loginSection.items():
            name = subSec.readString('name')
            urls = _LoginAppUrlIterator(subSec.readStrings('url'))
            host = urls.primary
            if host is not None:
                if not len(name):
                    name = host
                
                keyPath = subSec.readString('public_key_path')
                if not len(keyPath):
                    keyPath = None
                
                areaID = subSec.readString('game_area_id')
                if not len(areaID):
                    areaID = None
                
                if len(urls) > 1:
                    pass
                1
                app = name(host, 'urlIterator', urls = None, keyPath = keyPath, areaID = areaID, peripheryID = subSec.readInt('periphery_id', 0))
                idx = len(self._hosts)
                self._urlMap[app.url] = idx
                self._nameMap[app.name] = idx
                if app.peripheryID:
                    self._peripheryMap[app.peripheryID] = idx
                
                self._hosts.append(app)
                continue
        
        self._isDataLoaded = True

    
    def predefined(self, url):
        return url in self._urlMap

    
    def first(self):
        if len(self._hosts):
            return self._hosts[0]
        return self._makeHostItem('', '')

    
    def byUrl(self, url):
        result = self._makeHostItem('', url)
        index = self._urlMap.get(url, -1)
        if index > -1:
            result = self._hosts[index]
        
        return result

    
    def byName(self, name):
        result = self._makeHostItem(name, '')
        index = self._nameMap.get(name, -1)
        if index > -1:
            result = self._hosts[index]
        
        return result

    
    def hosts(self):
        return self._hosts[:]

    
    def shortList(self):
        result = map((lambda item: (item.url, item.name)), self._hosts)
        if AUTO_LOGIN_QUERY_ENABLED and len(result) > 1 and len(self.peripheries()) > 1:
            result.insert(0, (AUTO_LOGIN_QUERY_URL, i18n.makeString('#menu:login/auto')))
        
        return result

    
    def urlIterator(self, primary):
        result = None
        index = self._urlMap.get(primary, -1)
        if index > -1:
            result = self._hosts[index].urlIterator
        
        return result

    
    def periphery(self, peripheryID):
        result = None
        index = self._peripheryMap.get(peripheryID, -1)
        if index > -1:
            result = self._hosts[index]
        
        return result

    
    def peripheries(self):
        return filter((lambda app: app.peripheryID), self._hosts)


g_preDefinedHosts = _PreDefinedHostList()

