# Source Generated with Decompyle++
# File: battle_page_interfaces.pyc (Python 2.6)

from debug_utils import LOG_DEBUG, LOG_WARNING
from gui.BattleContext import g_battleContext
from helpers import i18n
from messenger import MESSENGER_I18N_FILE, BATTLE_TARGET_MESSAGE_FORMAT
from messenger import BATTLE_MESSAGE_FORMAT, BATTLE_CHANNELS, g_settings
from messenger.UsersManager import UsersManager
from messenger.gui.interfaces import MessengerPageInterface
_pColorSchemes = g_settings.getBattlePlayerHexCS()
_msgColorSchemes = g_settings.getBattleMsgHexCS()
_recvColorSchemes = g_settings.getBattleRecvHexCS()
_lastReceiver = BATTLE_CHANNELS.TEAM[1]

class _BasePageInterface(MessengerPageInterface):
    _teamCID = 0
    
    def __init__(self, channelID, initFlag, receiver):
        super(_BasePageInterface, self).__init__()
        self._cid = channelID
        self._initFlag = initFlag
        self._receiver = receiver

    
    def __del__(self):
        LOG_DEBUG('Deleted: %s' % self)

    
    def format(self, message, playerIsTarget = False, system = False):
        (playerColor, msgColor, targetColor) = self.getColors(message)
        if playerIsTarget:
            targetFormattedText = BATTLE_TARGET_MESSAGE_FORMAT % (targetColor, message.data['target'], msgColor)
            message.data = message.data['text'] % targetFormattedText
        
        return BATTLE_MESSAGE_FORMAT % (playerColor, unicode(self.getFullPlayerName(message), 'utf-8', errors = 'ignore'), msgColor, message.data)

    
    def getFullPlayerName(self, message):
        return g_battleContext.getFullPlayerName(accID = message.originator)

    
    def addMessage(self, message, format = True, playerIsTarget = False, system = False):
        if format:
            return self.format(message, playerIsTarget, system)
        return message.data

    
    def getColors(self, message):
        return (_msgColorSchemes['unknown'],) * 3

    
    def getRecvConfig(self):
        config = [
            '',
            0,
            0,
            False]
        receivers = g_settings.battleSettings['receivers']
        if self._receiver in receivers:
            color = 'FFFFFF'
            if self._receiver in _recvColorSchemes:
                color = _recvColorSchemes[self._receiver]
            else:
                LOG_WARNING('Color for receiver label not found', self._receiver, _recvColorSchemes)
            config = receivers[self._receiver][:]
            config[0] = config[0] % color
            config.append(self._receiver == _lastReceiver)
        
        return config

    
    def setCurrent(self):
        global _lastReceiver
        _lastReceiver = self._receiver



class TeamPageInterface(_BasePageInterface):
    
    def __init__(self, channelID):
        super(TeamPageInterface, self).__init__(channelID, BATTLE_CHANNELS.TEAM[0], BATTLE_CHANNELS.TEAM[1])
        _BasePageInterface._teamCID = channelID

    
    def __del__(self):
        self._teamCID = 0
        super(TeamPageInterface, self).__del__()

    
    def getColors(self, message):
        cid = message.channel
        uid = message.originator
        msgColor = _msgColorSchemes['team']
        playerColor = _pColorSchemes['teammate']
        targetColor = _pColorSchemes['himselfTgt']
        if UsersManager.isCurrentPlayer(uid):
            playerColor = _pColorSchemes['himself']
        elif g_battleContext.isTeamKiller(accID = uid):
            playerColor = _pColorSchemes['teamkiller']
        elif g_battleContext.isSquadMan(accID = uid):
            playerColor = _pColorSchemes['squadman']
        
        return (playerColor, msgColor, targetColor)



class CommonPageInterface(_BasePageInterface):
    _CommonPageInterface__i18n_ally = i18n.makeString('#{0:>s}:battle/unknown/ally'.format(MESSENGER_I18N_FILE))
    _CommonPageInterface__i18n_enemy = i18n.makeString('#{0:>s}:battle/unknown/enemy'.format(MESSENGER_I18N_FILE))
    
    def __init__(self, channelID):
        super(CommonPageInterface, self).__init__(channelID, BATTLE_CHANNELS.COMMON[0], BATTLE_CHANNELS.COMMON[1])

    
    def getFullPlayerName(self, message):
        fullName = g_battleContext.getFullPlayerName(accID = message.originator)
        if not len(fullName):
            if self.channels.hasExistMember(self._teamCID, message.originator):
                fullName = self._CommonPageInterface__i18n_ally
            else:
                fullName = self._CommonPageInterface__i18n_enemy
        
        return fullName

    
    def getColors(self, message):
        cid = message.channel
        uid = message.originator
        msgColor = _msgColorSchemes['common']
        playerColor = _msgColorSchemes['unknown']
        targetColor = _pColorSchemes['himselfTgt']
        if UsersManager.isCurrentPlayer(uid):
            playerColor = _pColorSchemes['himself']
        elif self.channels.hasExistMember(self._teamCID, uid):
            if g_battleContext.isTeamKiller(accID = uid):
                playerColor = _pColorSchemes['teamkiller']
            elif g_battleContext.isSquadMan(accID = uid):
                playerColor = _pColorSchemes['squadman']
            else:
                playerColor = _pColorSchemes['teammate']
        elif self.channels.hasExistMember(self._cid, uid):
            playerColor = _pColorSchemes['enemy']
        
        return (playerColor, msgColor, targetColor)



class SquadPageInterface(_BasePageInterface):
    
    def __init__(self, channelID):
        super(SquadPageInterface, self).__init__(channelID, BATTLE_CHANNELS.SQUAD[0], BATTLE_CHANNELS.SQUAD[1])

    
    def getFullPlayerName(self, message):
        return g_battleContext.getFullPlayerName(accID = message.originator, pName = message.originatorNickName)

    
    def getColors(self, message):
        cid = message.channel
        uid = message.originator
        msgColor = _msgColorSchemes['squad']
        playerColor = _pColorSchemes['squadman']
        targetColor = _pColorSchemes['himselfTgt']
        if UsersManager.isCurrentPlayer(uid):
            playerColor = _pColorSchemes['himself']
        elif g_battleContext.isTeamKiller(accID = uid):
            playerColor = _pColorSchemes['teamkiller']
        
        return (playerColor, msgColor, targetColor)



def create(channel):
    page = None
    if channel.isBattle:
        if channel.isBattleTeam:
            pass
        1
        clazz = CommonPageInterface
        page = clazz(channel.cid)
    elif channel.isSquad:
        page = SquadPageInterface(channel.cid)
    
    return page


def updateColors(**kwargs):
    global _pColorSchemes, _msgColorSchemes, _recvColorSchemes
    _pColorSchemes = g_settings.getBattlePlayerHexCS(**None)
    _msgColorSchemes = g_settings.getBattleMsgHexCS(**None)
    _recvColorSchemes = g_settings.getBattleRecvHexCS(**None)


def addDefMessage(message):
    playerColor = _msgColorSchemes['unknown']
    msgColor = _msgColorSchemes['unknown']
    return BATTLE_MESSAGE_FORMAT % (playerColor, unicode(g_battleContext.getFullPlayerName(accID = message.originator), 'utf-8', errors = 'ignore'), msgColor, message.data)


def storeReceiver4NextBattles():
    global _lastReceiver
    if _lastReceiver != BATTLE_CHANNELS.SQUAD[1]:
        _lastReceiver = BATTLE_CHANNELS.TEAM[1]
    


