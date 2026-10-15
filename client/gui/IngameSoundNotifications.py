# Source Generated with Decompyle++
# File: IngameSoundNotifications.pyc (Python 2.6)

import BigWorld
import ResMgr
import BattleReplay
from functools import partial
from debug_utils import *
from Vehicle import Vehicle

class IngameSoundNotifications(object):
    _IngameSoundNotifications__CFG_SECTION_PATH = 'gui/sound_notifications.xml'
    
    def __init__(self):
        self._IngameSoundNotifications__readConfig()
        self._IngameSoundNotifications__isEnabled = False

    
    def start(self):
        self._IngameSoundNotifications__soundQueues = {
            'fx': [],
            'voice': [] }
        self._IngameSoundNotifications__enabledSoundCategories = set(('fx', 'voice'))
        self._IngameSoundNotifications__isEnabled = True
        self._IngameSoundNotifications__activeEvents = {
            'fx': None,
            'voice': None }
        self._IngameSoundNotifications__lastTimePlayed = { }

    
    def destroy(self):
        for event in self._IngameSoundNotifications__activeEvents.itervalues():
            if event is not None:
                event['sound'].stop()
                continue
        
        self._IngameSoundNotifications__activeEvents = None
        self._IngameSoundNotifications__soundQueues = None
        self._IngameSoundNotifications__isEnabled = False

    
    def cancel(self, eventName, continuePlaying = True):
        for category in ('fx', 'voice'):
            eventDesc = self._IngameSoundNotifications__events[eventName].get(category, None)
            if eventDesc is not None:
                activeEvent = self._IngameSoundNotifications__activeEvents[category]
                soundPath = eventDesc['sound']
                if activeEvent is not None and activeEvent['soundPath'] == soundPath:
                    activeEvent['sound'].stop()
                    self._IngameSoundNotifications__activeEvents[category] = None
                    if continuePlaying:
                        self._IngameSoundNotifications__playFirstFromQueue(category)
                    
                
                if soundPath in self._IngameSoundNotifications__soundQueues[category]:
                    self._IngameSoundNotifications__soundQueues[category].remove(soundPath)
                
            soundPath in self._IngameSoundNotifications__soundQueues[category]
        

    
    def play(self, eventName, vehicleIdToBind = None):
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.isTimeWarpInProgress:
            return None
        if not (self._IngameSoundNotifications__isEnabled) or BigWorld.isWindowVisible() == False:
            return None
        event = self._IngameSoundNotifications__events.get(eventName, None)
        if event is None:
            LOG_WARNING("Couldn't find %s event" % eventName)
            return None
        queues = self._IngameSoundNotifications__soundQueues
        enabledCategories = self._IngameSoundNotifications__enabledSoundCategories
        time = BigWorld.time()
        for (category, soundDesc) in event.iteritems():
            if category in enabledCategories and soundDesc['sound'] != '':
                rules = soundDesc['playRules']
                idToBind = vehicleIdToBind
                if idToBind is None and soundDesc['shouldBindToPlayer']:
                    if BigWorld.player().vehicle is not None:
                        idToBind = BigWorld.player().vehicle.id
                    
                
                queueItem = (soundDesc['sound'], time + soundDesc['timeout'], soundDesc['minTimeBetweenEvents'], idToBind)
                if rules == 0:
                    
                    try:
                        BigWorld.playSound(soundDesc['sound'])
                    continue
                    BigWorld.isWindowVisible() == False
                    continue

                    continue
                elif rules == 1:
                    self._IngameSoundNotifications__clearQueue(category)
                    queues[category].append(queueItem)
                elif rules == 2:
                    queues[category].insert(0, queueItem)
                elif rules == 3:
                    queues[category].append(queueItem)
                
                if self._IngameSoundNotifications__activeEvents[category] is None:
                    self._IngameSoundNotifications__playFirstFromQueue(category)
                
            self._IngameSoundNotifications__activeEvents[category] is None
        

    
    def enable(self, isEnabled):
        self._IngameSoundNotifications__isEnabled = isEnabled
        if not isEnabled:
            for category in ('fx', 'voice'):
                self._IngameSoundNotifications__clearQueue(category)
            
        

    
    def enableFX(self, isEnabled):
        self.enableCategory('fx', isEnabled)

    
    def enableVoices(self, isEnabled):
        self.enableCategory('voice', isEnabled)

    
    def enableCategory(self, category, isEnabled):
        if isEnabled:
            self._IngameSoundNotifications__enabledSoundCategories.add(category)
        else:
            self._IngameSoundNotifications__enabledSoundCategories.remove(category)
            self._IngameSoundNotifications__clearQueue(category)

    
    def _IngameSoundNotifications__clearQueue(self, category):
        if self._IngameSoundNotifications__activeEvents[category] is not None:
            self._IngameSoundNotifications__activeEvents[category]['sound'].stop()
            self._IngameSoundNotifications__activeEvents[category] = None
        
        self._IngameSoundNotifications__soundQueues[category] = []

    
    def _IngameSoundNotifications__onSoundEnd(self, category, sound):
        if sound.state.find('playing') != -1:
            None((None, BigWorld.callback, 0.01), (lambda : self._IngameSoundNotifications__onSoundEnd(category, sound)))
        else:
            self._IngameSoundNotifications__activeEvents[category] = None
            BigWorld.callback(0.01, partial(self._IngameSoundNotifications__playFirstFromQueue, category))

    
    def _IngameSoundNotifications__playFirstFromQueue(self, category):
        if not self._IngameSoundNotifications__isEnabled:
            return None
        queue = self._IngameSoundNotifications__soundQueues[category]
        succes = False
        time = BigWorld.time()
        while not succes and len(queue) > 0:
            (soundPath, timeout, minTimeBetweenEvents, vehicleIdToBind) = queue[0]
            del queue[0]
            if vehicleIdToBind is not None:
                vehicles = BigWorld.player().arena.vehicles
                vehicleInfo = vehicles.get(vehicleIdToBind)
                if vehicleInfo is None or not vehicleInfo['isAlive']:
                    continue
                
            
            if time > timeout:
                continue
            
            lastPlayed = self._IngameSoundNotifications__lastTimePlayed.get(soundPath)
            if lastPlayed is not None and time - lastPlayed < minTimeBetweenEvents:
                continue
            
            succes = True
            
            try:
                sound = BigWorld.playSound(soundPath)
                if sound is None:
                    succes = False
                else:
                    self._IngameSoundNotifications__lastTimePlayed[soundPath] = time
            except:
                succes = False

            if not succes:
                LOG_ERROR('Failed to load sound %s' % soundPath)
                continue
        if succes:
            if sound.duration == 0:
                LOG_WARNING('Sound notification %s has zero duration and was skipped' % soundPath)
                BigWorld.callback(0.01, partial(self._IngameSoundNotifications__playFirstFromQueue, category))
            else:
                sound.setCallback('EVENTFINISHED', partial(self._IngameSoundNotifications__onSoundEnd, category))
                self._IngameSoundNotifications__activeEvents[category] = {
                    'sound': sound,
                    'soundPath': soundPath }
        

    
    def _IngameSoundNotifications__readConfig(self):
        sec = ResMgr.openSection(self._IngameSoundNotifications__CFG_SECTION_PATH)
        events = { }
        for eventSec in sec.values():
            event = { }
            events[eventSec.name] = { }
            for category in ('fx', 'voice'):
                soundSec = eventSec[category]
                if soundSec is not None:
                    event[category] = {
                        'sound': soundSec.readString('sound'),
                        'playRules': soundSec.readInt('playRules'),
                        'timeout': soundSec.readFloat('timeout', 3),
                        'minTimeBetweenEvents': soundSec.readFloat('minTimeBetweenEvents', 0),
                        'shouldBindToPlayer': soundSec.readBool('shouldBindToPlayer', False) }
                    continue
            
        
        self._IngameSoundNotifications__events = events



class ComplexSoundNotifications(object):
    
    def __init__(self, ingameSoundNotifications):
        self._ComplexSoundNotifications__isAimingEnded = False
        self._ComplexSoundNotifications__ingameSoundNotifications = ingameSoundNotifications

    
    def destroy(self):
        pass

    
    def setAimingEnded(self, isEnded, isReloading):
        if not (self._ComplexSoundNotifications__isAimingEnded) and isEnded and not isReloading:
            self._ComplexSoundNotifications__ingameSoundNotifications.play('sight_convergence')
        
        self._ComplexSoundNotifications__isAimingEnded = isEnded

    
    def notifyEnemySpotted(self, isPlural):
        self._ComplexSoundNotifications__ingameSoundNotifications.cancel('enemy_sighted_for_team', True)
        if isPlural:
            self._ComplexSoundNotifications__ingameSoundNotifications.play('enemies_sighted')
        else:
            self._ComplexSoundNotifications__ingameSoundNotifications.play('enemy_sighted')



class __SightNotifications(object):
    NOTIFICATION_DELAY = 2
    ENEMY_SIGHTED_SOUND = ''
    ENEMIES_SIGHTED_SOUND = ''
    SIGHTED_ENEMY_KILLED_SOUND = ''
    SIGHTED_ENEMIES_KILLED_SOUND = ''
    
    def __init__(self, ingameSoundNotifications):
        self._SightNotifications__ingameSoundNotifications = ingameSoundNotifications
        self._SightNotifications__enemySightedCallbackId = None
        self._SightNotifications__isOneSighted = True
        self._SightNotifications__sightedEnemyKilledCallbackId = None
        self._SightNotifications__isOneKilled = True

    
    def destroy(self):
        if self._SightNotifications__enemySightedCallbackId is not None:
            BigWorld.cancelCallback(self._SightNotifications__enemySightedCallbackId)
        
        if self._SightNotifications__sightedEnemyKilledCallbackId is not None:
            BigWorld.cancelCallback(self._SightNotifications__sightedEnemyKilledCallbackId)
        

    
    def _SightNotifications__playEnemySighted(self):
        self._SightNotifications__enemySightedCallbackId = None
        if self._SightNotifications__isOneSighted:
            self._SightNotifications__ingameSoundNotifications.play(SightNotifications.ENEMY_SIGHTED_SOUND)
        else:
            self._SightNotifications__ingameSoundNotifications.play(SightNotifications.ENEMIES_SIGHTED_SOUND)

    
    def notifyEnemySighted(self):
        if self._SightNotifications__enemySightedCallbackId is None:
            self._SightNotifications__enemySightedCallbackId = BigWorld.callback(SightNotifications.NOTIFICATION_DELAY, self._SightNotifications__playEnemySighted)
            self._SightNotifications__isOneSighted = True
        else:
            self._SightNotifications__isOneSighted = False

    
    def _SightNotifications__playSightedEnemyKilled(self):
        self._SightNotifications__sightedEnemyKilledCallbackId = None
        if self._SightNotifications____isOneKilled:
            self._SightNotifications__ingameSoundNotifications.play(SightNotifications.ENEMY_SIGHTED_SOUND)
        else:
            self._SightNotifications__ingameSoundNotifications.play(SightNotifications.ENEMIES_SIGHTED_SOUND)

    
    def notifySightedEnemyKilled(self):
        if self._SightNotifications__sightedEnemyKilledCallbackId is None:
            self._SightNotifications__sightedEnemyKilledCallbackId = BigWorld.callback(SightNotifications.NOTIFICATION_DELAY, self._SightNotifications__playSightedEnemyKilled)
            self._SightNotifications____isOneKilled = True
        else:
            self._SightNotifications____isOneKilled = False



