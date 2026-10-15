# Source Generated with Decompyle++
# File: AOGAS.pyc (Python 2.6)

import BigWorld
from ConnectionManager import connectionManager
from constants import AOGAS_TIME, ACCOUNT_ATTR
from debug_utils import LOG_ERROR, LOG_DEBUG
from enumerations import AttributeEnumItem, Enumeration
import Event
from helpers import time_utils
from PlayerEvents import g_playerEvents
import time
import weakref
TIME_MODIFER = 3600
AOGAS_FORCE_START_NOTIFY = False
_DEFAULT_AOGAS_NOTIFY_TIMEOUT = 5
AOGAS_NOTIFY_MSG = Enumeration('Notification message for Anti-online game addiction system', [
    ('AOND_1', {
        'timeout': _DEFAULT_AOGAS_NOTIFY_TIMEOUT }),
    ('AOND_2', {
        'timeout': _DEFAULT_AOGAS_NOTIFY_TIMEOUT }),
    ('AOND_3', {
        'timeout': _DEFAULT_AOGAS_NOTIFY_TIMEOUT }),
    ('AOND_MORE_3', {
        'timeout': _DEFAULT_AOGAS_NOTIFY_TIMEOUT }),
    ('AOND_MORE_5', {
        'timeout': _DEFAULT_AOGAS_NOTIFY_TIMEOUT }),
    ('RESET', {
        'timeout': _DEFAULT_AOGAS_NOTIFY_TIMEOUT })], instance = AttributeEnumItem)

class AOGAS_NOTIFY_TIME(object):
    AOND_1 = 1 * TIME_MODIFER - 600
    AOND_2 = 2 * TIME_MODIFER - 600
    AOND_3 = AOGAS_TIME.REDUCED_GAIN
    AOND_5 = AOGAS_TIME.NO_GAIN


class AOGAS_NOTIFY_PERIOD(object):
    AOND_START = 5 * TIME_MODIFER / 6
    AOND_2_3 = 1 * TIME_MODIFER
    AOND_3_5 = 0.5 * TIME_MODIFER
    AOND_END = 0.25 * TIME_MODIFER


class _AOGASController(object):
    
    def __init__(self):
        self.onNotifyAccount = Event.Event()
        self._AOGASController__isNotifyAccount = False
        self._AOGASController__lastNotifyMessages = []
        self._AOGASController__aogasStartedAt = 0
        self._AOGASController__isAogasEnabled = True
        self._AOGASController__notificator = _AOGASNotificator(self, '_AOGASController__notifyAccount')

    
    def init(self):
        g_playerEvents.onAccountShowGUI += self._AOGASController__onAccountShowGUI
        g_playerEvents.onAvatarBecomePlayer += self._AOGASController__onAvatarBecomePlayer
        connectionManager.onDisconnected += self._AOGASController__onDisconnected

    
    def destroy(self):
        g_playerEvents.onAccountShowGUI -= self._AOGASController__onAccountShowGUI
        g_playerEvents.onAvatarBecomePlayer -= self._AOGASController__onAvatarBecomePlayer
        connectionManager.onDisconnected -= self._AOGASController__onDisconnected
        self._AOGASController__notificator.stop()
        self.onNotifyAccount.clear()

    
    def enableNotifyAccount(self):
        LOG_DEBUG('enableNotifyAccount ', self._AOGASController__lastNotifyMessages)
        self._AOGASController__isNotifyAccount = True
        for message in self._AOGASController__lastNotifyMessages:
            self.onNotifyAccount(message)
        
        self._AOGASController__lastNotifyMessages = []

    
    def disableNotifyAccount(self):
        LOG_DEBUG('disableNotifyAccount')
        self._AOGASController__isNotifyAccount = False

    
    def _AOGASController__notifyAccount(self, message, collect = False):
        if self._AOGASController__isNotifyAccount:
            self.onNotifyAccount(message)
        elif collect:
            self._AOGASController__lastNotifyMessages.append(message)
        else:
            self._AOGASController__lastNotifyMessages = [
                message]

    
    def _AOGASController__onAccountShowGUI(self, ctx):
        serverTime = ctx.get('aogasStartedAt')
        if serverTime is not None:
            self._AOGASController__aogasStartedAt = time_utils.makeLocalServerTime(serverTime)
        else:
            self._AOGASController__aogasStartedAt = time.time()
        self._AOGASController__isAogasEnabled = ctx.get('isAogasEnabled', True)
        if not self._AOGASController__notificator.isStarted():
            self._AOGASController__requestRequiredInfo()
        

    
    def _AOGASController__onAvatarBecomePlayer(self):
        self.disableNotifyAccount()

    
    def _AOGASController__onDisconnected(self):
        self._AOGASController__notificator.stop()
        self._AOGASController__isNotifyAccount = False
        self._AOGASController__lastNotifyMessages = []

    
    def _AOGASController__requestRequiredInfo(self):
        BigWorld.player().stats.get('attrs', self._AOGASController__receiveAccountAttrs)

    
    def _AOGASController__receiveAccountAttrs(self, resultID, attrs):
        if resultID < 0:
            LOG_ERROR('Server return error: ', resultID, attrs)
            return None
        if self._AOGASController__isAogasEnabled or ACCOUNT_ATTR.AOGAS & attrs != 0 or AOGAS_FORCE_START_NOTIFY:
            BigWorld.player().stats.get('accOnline', self._AOGASController__receiveAccOnline)
        elif self._AOGASController__notificator.isStarted():
            self._AOGASController__notificator.stop()
        

    
    def _AOGASController__receiveAccOnline(self, resultID, accOnline):
        if resultID < 0:
            LOG_ERROR('Server return error: ', resultID, accOnline)
            return None
        if not accOnline:
            self._AOGASController__notifyAccount(AOGAS_NOTIFY_MSG.RESET)
        
        delta = round(time.time() - self._AOGASController__aogasStartedAt)
        AOND = delta + accOnline
        LOG_DEBUG('Calculate AOND (seconds,seconds,seconds) : ', AOND, delta, accOnline)
        self._AOGASController__notificator.start(AOND)



class _AOGASNotificator(object):
    
    def __init__(self, scope, function):
        self._AOGASNotificator__scope = weakref.ref(scope)
        self._AOGASNotificator__function = function
        self._AOGASNotificator__started = False
        self._AOGASNotificator__AOND = 0
        self._AOGASNotificator__callbackID = None

    
    def start(self, AOND):
        if self._AOGASNotificator__started:
            return None
        self._AOGASNotificator__started = True
        self._AOGASNotificator__AOND = AOND
        notificated = False
        if AOND > AOGAS_NOTIFY_TIME.AOND_1:
            prevAOND = self._AOGASNotificator__getPrevNotifyTime(AOND)
            self._AOGASNotificator__doNotify(self._AOGASNotificator__getNotifyMessages(prevAOND))
            notificated = prevAOND == AOND
        
        if notificated:
            notifyPeriod = self._AOGASNotificator__getNotifyPeriod(self._AOGASNotificator__AOND)
            LOG_DEBUG('start (seconds,seconds) ', self._AOGASNotificator__AOND, notifyPeriod)
            self._AOGASNotificator__callbackID = self._AOGASNotificator__started((BigWorld.callback, notifyPeriod), (lambda : self._AOGASNotificator__notify(notifyPeriod)))
        else:
            notifyTime = self._AOGASNotificator__getNextNotifyTime(AOND)
            nextNotifyDelay = abs(notifyTime - AOND)
            LOG_DEBUG('start (seconds,seconds,seconds) ', self._AOGASNotificator__AOND, notifyTime, nextNotifyDelay)
            self._AOGASNotificator__callbackID = self._AOGASNotificator__started((BigWorld.callback, nextNotifyDelay), (lambda : self._AOGASNotificator__notify(nextNotifyDelay)))

    
    def stop(self):
        self._AOGASNotificator__started = False
        if self._AOGASNotificator__callbackID is not None:
            BigWorld.cancelCallback(self._AOGASNotificator__callbackID)
            self._AOGASNotificator__callbackID = None
        

    
    def isStarted(self):
        return self._AOGASNotificator__started

    
    def _AOGASNotificator__getNotifyPeriod(self, AOND):
        if AOND < AOGAS_NOTIFY_TIME.AOND_1:
            notifyPeriod = AOGAS_NOTIFY_PERIOD.AOND_START
        elif AOND < AOGAS_NOTIFY_TIME.AOND_3:
            notifyPeriod = AOGAS_NOTIFY_PERIOD.AOND_2_3
        elif AOND < AOGAS_NOTIFY_TIME.AOND_5:
            notifyPeriod = AOGAS_NOTIFY_PERIOD.AOND_3_5
        else:
            notifyPeriod = AOGAS_NOTIFY_PERIOD.AOND_END
        return notifyPeriod

    
    def _AOGASNotificator__getNextNotifyTime(self, AOND):
        notifyTime = 0
        while notifyTime < AOND:
            notifyPeriod = self._AOGASNotificator__getNotifyPeriod(notifyTime)
            notifyTime += notifyPeriod
        return notifyTime

    
    def _AOGASNotificator__getPrevNotifyTime(self, AOND):
        notifyTime = 0
        notifyPeriod = 0
        while notifyTime < AOND:
            notifyPeriod = self._AOGASNotificator__getNotifyPeriod(notifyTime)
            notifyTime += notifyPeriod
        return notifyTime - notifyPeriod

    
    def _AOGASNotificator__getNotifyMessages(self, AOND):
        if AOND == AOGAS_NOTIFY_TIME.AOND_1:
            messages = (AOGAS_NOTIFY_MSG.AOND_1,)
        elif AOND == AOGAS_NOTIFY_TIME.AOND_2:
            messages = (AOGAS_NOTIFY_MSG.AOND_2,)
        elif AOND == AOGAS_NOTIFY_TIME.AOND_3:
            messages = (AOGAS_NOTIFY_MSG.AOND_3, AOGAS_NOTIFY_MSG.AOND_MORE_3)
        elif AOND < AOGAS_NOTIFY_TIME.AOND_5:
            messages = (AOGAS_NOTIFY_MSG.AOND_MORE_3,)
        else:
            messages = (AOGAS_NOTIFY_MSG.AOND_MORE_5,)
        return messages

    
    def _AOGASNotificator__doNotify(self, messages):
        notifyHandler = getattr(self._AOGASNotificator__scope(), self._AOGASNotificator__function, None)
        if notifyHandler is not None:
            collect = len(messages) > 1
            for message in messages:
                notifyHandler(message, collect)
                LOG_DEBUG('notify (seconds, message)', self._AOGASNotificator__AOND, message)
            
        else:
            LOG_ERROR('Not found notify handler ', self._AOGASNotificator__scope(), self._AOGASNotificator__function)

    
    def _AOGASNotificator__notify(self, notifyPeriod):
        self._AOGASNotificator__AOND += notifyPeriod
        self._AOGASNotificator__doNotify(self._AOGASNotificator__getNotifyMessages(self._AOGASNotificator__AOND))
        notifyPeriod = self._AOGASNotificator__getNotifyPeriod(self._AOGASNotificator__AOND)
        self._AOGASNotificator__callbackID = None((BigWorld.callback, notifyPeriod), (lambda : self._AOGASNotificator__notify(notifyPeriod)))


g_controller = None

def init():
    global g_controller
    g_controller = _AOGASController()
    g_controller.init()


def fini():
    global g_controller
    if g_controller is not None:
        g_controller.destroy()
        g_controller = None
    


