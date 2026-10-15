# Source Generated with Decompyle++
# File: LightManager.pyc (Python 2.6)

from debug_utils import *
import BigWorld
import LightEffect
from LightEffectsCache import LightEffectsCache
from Math import Vector4
import time
import copy
from ChatManager import chatManager
from chat_shared import CHAT_ACTIONS
import gui.SystemMessages as gui
g_instance = None

class LightManager:
    UPDATE_TIMEOUT = 0.5
    ALL_LIGHTS = 'All'
    LOCATIONS_MASKS = {
        'Zone_LeftSpeaker': 1,
        'Zone_RightSpeaker': 4,
        'Zone_Keyboard': 16,
        'Zone_Logo': 524288,
        ALL_LIGHTS: 0xFFFFFFFFL }
    
    def __init__(self):
        self._LightManager__isEnabled = False
        self._LightManager__lightObject = BigWorld.WGLightFx()
        self._LightManager__lights = { }
        self._LightManager__isEnabled = self._LightManager__lightObject.initialize()
        if not self._LightManager__isEnabled:
            LOG_DEBUG('LightFx is not enabled')
            return None
        self._LightManager__lightObject.reset()
        LightEffectsCache.load()
        for lightEffect in LightEffectsCache.allEffects().values():
            lightEffect.onStop += self._LightManager__onEffectStop
        
        numberOfDevices = self._LightManager__lightObject.getNumberOfDevices()
        for deviceIndex in range(numberOfDevices):
            numberOfLights = self._LightManager__lightObject.getNumberOfLights(deviceIndex)
            for lightIndex in range(numberOfLights):
                lightDescription = self._LightManager__lightObject.getLightDescription(deviceIndex, lightIndex)
                self._LightManager__lights[lightDescription] = (deviceIndex, lightIndex)
            
        
        self._LightManager__runningEffects = []
        self._LightManager__lastUpdateTime = None
        self._LightManager__periodicTimerID = None
        LightManager._chatActionsHandler = _ChatActionsHandler()
        self._LightManager__periodicUpdate()

    
    def start(self):
        if self.isEnabled():
            self.setStartupLights()
        

    
    def destroy(self):
        if not self._LightManager__isEnabled:
            return None
        if self._LightManager__periodicTimerID is not None:
            BigWorld.cancelCallback(self._LightManager__periodicTimerID)
        
        for lightEffect in LightEffectsCache.allEffects().values():
            lightEffect.destroy()
        
        LightManager._chatActionsHandler.destroy()

    
    def isEnabled(self):
        return self._LightManager__isEnabled

    
    def getLights(self):
        return self._LightManager__lights

    
    def setLightColor(self, lightDescription, color):
        self.setLightAction(lightDescription, color, LightEffect.ACTION_COLOR)

    
    def setLightPulse(self, lightDescription, color):
        self.setLightAction(lightDescription, color, LightEffect.ACTION_PULSE)

    
    def setLightActionByIndex(self, deviceIndex, lightIndex, color, action):
        if action == LightEffect.ACTION_COLOR:
            self._LightManager__lightObject.setLightColor(deviceIndex, lightIndex, color)
        elif action == LightEffect.ACTION_PULSE:
            self._LightManager__lightObject.setLightPulse(deviceIndex, lightIndex, color)
        

    
    def actionColorEx(self, mask, action, color):
        self._LightManager__lightObject.actionColorEx(mask, action, color, Vector4())

    
    def setLightAction(self, lightDescription, color, action):
        if not self.isEnabled():
            return None
        if LightManager.LOCATIONS_MASKS.has_key(lightDescription):
            self.actionColorEx(LightManager.LOCATIONS_MASKS[lightDescription], action, color)
        

    
    def startLightEffect(self, lightEffectName):
        if not self.isEnabled():
            return None
        lightEffect = LightEffectsCache.getEffect(lightEffectName)
        if not lightEffect.isRunning():
            self._LightManager__runningEffects.append(lightEffect)
            lightEffect.start()
        
        for oneLightAction in lightEffect.lightActions.values():
            self.setLightAction(oneLightAction.lightDescription, oneLightAction.color, oneLightAction.action)
        

    
    def stopLightEffect(self, lightEffectName):
        if not self.isEnabled():
            return None
        lightEffect = LightEffectsCache.getEffect(lightEffectName)
        if lightEffect.isRunning():
            lightEffect.stop()
        

    
    def _LightManager__onEffectStop(self, lightEffect):
        self._LightManager__runningEffects.remove(lightEffect)

    
    def turnOffAll(self):
        for lightEffect in self._LightManager__runningEffects[:]:
            self.stopLightEffect(lightEffect.name)
        

    
    def setStartupLights(self):
        self.turnOffAll()
        self.startLightEffect('Splash Screen')

    
    def _LightManager__periodicUpdate(self):
        self._LightManager__periodicTimerID = None
        blackLights = LightManager.LOCATIONS_MASKS.keys()
        blackLights.remove(LightManager.ALL_LIGHTS)
        if len(self._LightManager__runningEffects) > 0:
            lightEffect = self._LightManager__runningEffects[-1]
            for oneLightAction in lightEffect.lightActions.values():
                if oneLightAction.lightDescription in blackLights:
                    blackLights.remove(oneLightAction.lightDescription)
                
                if oneLightAction.lightDescription == LightManager.ALL_LIGHTS:
                    del blackLights[:]
                
                if oneLightAction.action == LightEffect.ACTION_COLOR:
                    self.setLightAction(oneLightAction.lightDescription, oneLightAction.color, oneLightAction.action)
                    continue
                del blackLights[:]
                break
            
        
        for lightDescription in blackLights:
            self.setLightAction(lightDescription, Vector4(), LightEffect.ACTION_COLOR)
        
        self._LightManager__lightObject.update()
        self._LightManager__lastUpdateTime = time.time()
        self._LightManager__periodicTimerID = BigWorld.callback(LightManager.UPDATE_TIMEOUT, self._LightManager__periodicUpdate)



class GameLights:
    
    def startTicks():
        g_instance.startLightEffect('Ticks')

    startTicks = staticmethod(startTicks)
    
    def roundStarted():
        g_instance.stopLightEffect('Ticks')
        g_instance.startLightEffect('Round Started')

    roundStarted = staticmethod(roundStarted)
    INVITATION_EFFECT = 'Invitation'
    CHAT_CHANNEL_OPENED_EFFECT = 'Chat Channel'
    
    def systemMessage():
        g_instance.startLightEffect('System Message')

    systemMessage = staticmethod(systemMessage)

from LightFx.LightManager import GameLights
from messenger.gui import MessengerDispatcher
from PlayerEvents import g_playerEvents
from ConnectionManager import connectionManager as g_connectionManager
_chatActionsHandler = None

class _ChatActionsHandler:
    
    def __init__(self):
        g_playerEvents.onAccountBecomePlayer += self._ChatActionsHandler__subscribe
        g_connectionManager.onDisconnected += self._ChatActionsHandler__onDisconnected

    
    def _ChatActionsHandler__subscribe(self):
        messengerDispatcher = MessengerDispatcher.g_instance
        messengerDispatcher.invites.onReceivedInviteListModified += self._ChatActionsHandler__onReceivedInviteListModified
        messengerDispatcher.invites.onReceivedInviteListInited += self._ChatActionsHandler__onReceivedInviteListModified
        messengerDispatcher.serviceChannel.onReceiveServerMessage += self._ChatActionsHandler__onSysMessage
        messengerDispatcher.serviceChannel.onReceiveClientMessage += self._ChatActionsHandler__onSysMessage
        messengerDispatcher.channels.onJoinedToChannel += self._ChatActionsHandler__onChatEnter

    
    def destroy(self):
        messengerDispatcher = MessengerDispatcher.g_instance
        messengerDispatcher.invites.onReceivedInviteListModified -= self._ChatActionsHandler__onReceivedInviteListModified
        messengerDispatcher.invites.onReceivedInviteListInited -= self._ChatActionsHandler__onReceivedInviteListModified
        messengerDispatcher.serviceChannel.onReceiveServerMessage -= self._ChatActionsHandler__onSysMessage
        messengerDispatcher.serviceChannel.onReceiveClientMessage -= self._ChatActionsHandler__onSysMessage
        messengerDispatcher.channels.onJoinedToChannel -= self._ChatActionsHandler__onChatEnter

    
    def _ChatActionsHandler__onDisconnected(self):
        g_instance.setStartupLights()

    
    def _ChatActionsHandler__onReceivedInviteListModified(self, *args):
        if MessengerDispatcher.g_instance.invites.getUnreadCount():
            g_instance.startLightEffect(GameLights.INVITATION_EFFECT)
        else:
            g_instance.stopLightEffect(GameLights.INVITATION_EFFECT)

    
    def _ChatActionsHandler__onSysMessage(self, formatted, isPriority, notify, auxData):
        gameGreetingName = gui.SystemMessages.SM_TYPE.GameGreeting.name()
        if gameGreetingName not in auxData:
            GameLights.systemMessage()
        

    
    def _ChatActionsHandler__onChatEnter(self, channel):
        isCurrentPlayer = MessengerDispatcher.g_instance.users.isCurrentPlayer(channel.owner)
        if not isCurrentPlayer and channel.isPrivate:
            g_instance.startLightEffect(GameLights.CHAT_CHANNEL_OPENED_EFFECT)
        



