# Source Generated with Decompyle++
# File: MusicController.pyc (Python 2.6)

import account_helpers
import struct
import BigWorld
import ResMgr
import FMOD
import items
import ClientArena
import Avatar
import Account
import constants
from constants import ARENA_PERIOD
from items import _xml
from PlayerEvents import g_playerEvents
from ConnectionManager import connectionManager
MUSIC_EVENT_NONE = 0
MUSIC_EVENT_LOGIN = 1
MUSIC_EVENT_LOBBY = 2
MUSIC_EVENT_COMBAT = 3
MUSIC_EVENT_COMBAT_LOADING = 4
MUSIC_EVENT_COMBAT_VICTORY = 5
MUSIC_EVENT_COMBAT_LOSE = 6
MUSIC_EVENT_COMBAT_DRAW = 7
AMBIENT_EVENT_NONE = 1000
AMBIENT_EVENT_LOBBY = 1001
AMBIENT_EVENT_SHOP = 1002
AMBIENT_EVENT_STATISTICS = 1003
AMBIENT_EVENT_COMBAT = 1004
_CMD_SERVER_CHANGE_HANGAR_AMBIENT = 'cmd_change_hangar_ambient'
g_musicController = None

def init():
    global g_musicController
    g_musicController = MusicController()


class MusicController(object):
    
    def __init__(self):
        self._MusicController__sndEventAmbient = None
        self._MusicController__eventAmbientId = None
        self._MusicController__sndEventMusic = None
        self._MusicController__eventMusicId = None
        self._MusicController__isOnArena = False
        self._MusicController__isPremiumAccount = False
        self._MusicController__updatedByNotification = False
        self._MusicController__soundEvents = {
            MUSIC_EVENT_NONE: None,
            AMBIENT_EVENT_NONE: None }
        self._loadConfig()
        g_playerEvents.onEventNotificationsChanged += self._MusicController__onEventNotificationsChanged
        connectionManager.onDisconnected += self._MusicController__onDisconnected

    
    def destroy(self):
        g_playerEvents.onEventNotificationsChanged -= self._MusicController__onEventNotificationsChanged
        connectionManager.onDisconnected -= self._MusicController__onDisconnected

    
    def __del__(self):
        self.stop()
        self._MusicController__soundEvents.clear()

    
    def _MusicController__reloadConfig(self):
        self._loadConfig()
        if self._MusicController__eventAmbientId is not None:
            self.play(self._MusicController__eventAmbientId)
        
        if self._MusicController__eventMusicId is not None:
            self.play(self._MusicController__eventMusicId)
        

    
    def _MusicController__onEventNotificationsChanged(self, notificationsDiff):
        for notification in notificationsDiff['removed']:
            if notification['type'] == _CMD_SERVER_CHANGE_HANGAR_AMBIENT:
                self._MusicController__reloadConfig()
                self._MusicController__updatedByNotification = False
                continue
        
        for notification in notificationsDiff['added']:
            if notification['type'] == _CMD_SERVER_CHANGE_HANGAR_AMBIENT:
                ambientEventName = notification['data']
                sound = FMOD.getSound(ambientEventName)
                if sound is not None:
                    sound.stop()
                
                self._MusicController__soundEvents[AMBIENT_EVENT_LOBBY] = [
                    sound,
                    sound]
                self._MusicController__soundEvents[AMBIENT_EVENT_SHOP] = [
                    sound,
                    sound]
                self._MusicController__soundEvents[AMBIENT_EVENT_STATISTICS] = [
                    sound,
                    sound]
                if self._MusicController__eventAmbientId is not None:
                    self.play(self._MusicController__eventAmbientId)
                
                if self._MusicController__eventMusicId is not None:
                    self.play(self._MusicController__eventMusicId)
                
                self._MusicController__updatedByNotification = True
                continue
        

    
    def _MusicController__onDisconnected(self):
        if self._MusicController__updatedByNotification:
            self._MusicController__reloadConfig()
        

    
    def _loadConfig(self):
        eventNames = { }
        xmlPath = 'gui/music_events.xml'
        section = ResMgr.openSection(xmlPath)
        if section is None:
            _xml.raiseWrongXml(None, xmlPath, 'can not open or read')
        
        for i in section.items():
            s = i[1]
            if i[0] == 'music':
                eventNames[MUSIC_EVENT_LOGIN] = s.readString('login')
                eventNames[MUSIC_EVENT_LOBBY] = (s.readString('lobby'), s.readString('lobby_premium'))
                eventNames[MUSIC_EVENT_COMBAT_VICTORY] = s.readString('combat_victory')
                eventNames[MUSIC_EVENT_COMBAT_LOSE] = s.readString('combat_lose')
                eventNames[MUSIC_EVENT_COMBAT_DRAW] = s.readString('combat_draw')
                continue
            if i[0] == 'ambient':
                eventNames[AMBIENT_EVENT_LOBBY] = (s.readString('lobby'), s.readString('lobby_premium'))
                eventNames[AMBIENT_EVENT_SHOP] = (s.readString('shop'), s.readString('shop_premium'))
                eventNames[AMBIENT_EVENT_STATISTICS] = (s.readString('rating'), s.readString('rating_premium'))
                continue
        
        soundsByName = { }
        for (eventId, eventNames) in eventNames.items():
            lstEvents = []
            if not isinstance(eventNames, tuple):
                eventNames = (eventNames,)
            
            for eventName in eventNames:
                sound = soundsByName.get(eventName)
                if sound is None:
                    if eventName != '':
                        pass
                    1
                    sound = None
                
                soundsByName[eventName] = sound
                lstEvents.append(sound)
                if sound is not None:
                    sound.stop()
                    continue
            
            self._MusicController__soundEvents[eventId] = lstEvents
        

    
    def play(self, eventId):
        soundEvent = None
        if eventId == MUSIC_EVENT_COMBAT and eventId == AMBIENT_EVENT_COMBAT or eventId == MUSIC_EVENT_COMBAT_LOADING:
            soundEvent = self._getArenaSoundEvent(eventId)
        else:
            soundEvent = self._MusicController__soundEvents.get(eventId)
            if soundEvent is not None:
                if isinstance(soundEvent, list):
                    isPremium = self._MusicController__isPremiumAccount
                    if isPremium and len(soundEvent) > 1:
                        pass
                    1
                    idx = 0
                    if isPremium and len(soundEvent) > 1:
                        pass
                    1
                    soundEvent = 1[0]
                
            
        isMusicTrack = eventId < AMBIENT_EVENT_NONE
        if isMusicTrack:
            pass
        1
        prevSoundEvent = self._MusicController__sndEventAmbient
        if prevSoundEvent == soundEvent:
            return None
        if prevSoundEvent is not None:
            prevSoundEvent.stop()
        
        if soundEvent is not None:
            soundEvent.play()
        
        if isMusicTrack:
            self._MusicController__sndEventMusic = soundEvent
            self._MusicController__eventMusicId = eventId
        else:
            self._MusicController__sndEventAmbient = soundEvent
            self._MusicController__eventAmbientId = eventId

    
    def stopMusic(self):
        if self._MusicController__sndEventMusic is not None:
            self._MusicController__sndEventMusic.stop()
            self._MusicController__sndEventMusic = None
            self._MusicController__eventMusicId = None
        

    
    def stopAmbient(self):
        if self._MusicController__sndEventAmbient is not None:
            self._MusicController__sndEventAmbient.stop()
            self._MusicController__sndEventAmbient = None
            self._MusicController__eventAmbientId = None
        

    
    def stop(self):
        self.stopAmbient()
        self.stopMusic()

    
    def onEnterArena(self):
        BigWorld.player().arena.onPeriodChange += self._onArenaStateChanged
        self._MusicController__isOnArena = True
        self._onArenaStateChanged()

    
    def onLeaveArena(self):
        self._MusicController__isOnArena = False
        BigWorld.player().arena.onPeriodChange -= self._onArenaStateChanged

    
    def setAccountAttrs(self, accAttrs):
        self._MusicController__isPremiumAccount = account_helpers.isPremiumAccount(accAttrs)

    
    def _onArenaStateChanged(self, *args):
        arena = BigWorld.player().arena
        period = arena.period
        if period == ARENA_PERIOD.BATTLE and self._MusicController__isOnArena:
            self.play(MUSIC_EVENT_COMBAT)
            self.play(AMBIENT_EVENT_COMBAT)
        elif period == ARENA_PERIOD.AFTERBATTLE:
            self.stopAmbient()
            winnerTeam = arena.periodAdditionalInfo[0]
            if winnerTeam == BigWorld.player().team:
                self.play(MUSIC_EVENT_COMBAT_VICTORY)
            elif winnerTeam == 0:
                self.play(MUSIC_EVENT_COMBAT_DRAW)
            else:
                self.play(MUSIC_EVENT_COMBAT_LOSE)
        

    
    def _getArenaSoundEvent(self, eventId):
        player = BigWorld.player()
        soundEvent = None
        soundEventName = None
        if not isinstance(player, Avatar.PlayerAvatar):
            return None
        if player.arena is None:
            return None
        arenaType = player.arena.arenaType
        if eventId == MUSIC_EVENT_COMBAT:
            soundEventName = arenaType.music
        elif eventId == MUSIC_EVENT_COMBAT_LOADING:
            soundEventName = arenaType.loadingMusic
        elif eventId == AMBIENT_EVENT_COMBAT:
            soundEventName = arenaType.ambientSound
        
        if soundEventName is not None:
            soundEvent = FMOD.getSound(soundEventName)
            if soundEvent is not None:
                soundEvent.stop()
            
        
        return soundEvent



