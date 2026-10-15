# Source Generated with Decompyle++
# File: m_settings.pyc (Python 2.6)

from chat_shared import CHAT_MEMBER_GROUP, USERS_ROSTER_FRIEND, USERS_ROSTER_IGNORED
import Event
from helpers.html import translation as html_translation, templates
from messenger import BATTLE_DEFAULT_MESSAGE_LIFE_TIME, DEFAULT_MESSAGE_DATETIME_FORMAT_INDEX, LOBBY_MESSAGE_FORMAT, SCH_DEFAULT_POP_UP_MSG_LIFE_TIME, SCH_DEFAULT_POP_UP_MSG_STACK_LENGTH, BATTLE_CHANNELS
import Math
import ResMgr
import Settings

class _MessageTemplate(templates.Template):
    
    def __init__(self, source, data):
        super(_MessageTemplate, self).__init__({
            'message': source })
        self.data = data

    
    def format(self, ctx = None, data = None):
        vo = self.data.copy()
        if data is not None:
            vo.update(data)
        
        vo['message'] = super(_MessageTemplate, self).format(ctx = ctx, sourceKey = 'message')
        return vo



class _MessageTemplates(templates.XMLCollection):
    
    def __missing__(self, key):
        self[key] = _MessageTemplate(key, { })
        value = _MessageTemplate(key, { })
        return value

    
    def _make(self, source):
        data = {
            'type': source.readString('type'),
            'icon': source.readString('icon'),
            'defaultIcon': source.readString('defaultIcon'),
            'filters': [] }
        message = html_translation(source.readString('message'))
        filtersSec = source['filters']
        if filtersSec is None:
            filtersSec = { }
        
        for (key1, filterSec) in filtersSec.items():
            data['filters'].append({
                'name': filterSec.readString('name'),
                'color': filterSec.readString('color') })
        
        return _MessageTemplate(message, data)



class MessengerSettings(object):
    _MessengerSettings__lobbyMFormats = { }
    _MessengerSettings__lobbyUserColorScheme = {
        'himself': (False, True, {
            'offline': None,
            'online': '' }),
        'user': (True, True, {
            'offline': '',
            'online': '' }),
        'friend': (True, True, {
            'offline': '',
            'online': '' }),
        'ignored': (True, False, {
            'offline': '',
            'online': None }) }
    _MessengerSettings__userRosterKayPairs = {
        USERS_ROSTER_FRIEND: 'friend',
        USERS_ROSTER_IGNORED: 'ignored' }
    _MessengerSettings__defUserPropsGetters = {
        'datetimeIdx': ('readInt', xrange(0, 4)),
        'enableOlFilter': ('readBool', None),
        'enableSpamFilter': ('readBool', None),
        'enableStoreMws': ('readBool', None),
        'enableStoreCws': ('readBool', None),
        'invitesFromFriendsOnly': ('readBool', None) }
    _MessengerSettings__user = {
        'datetimeIdx': DEFAULT_MESSAGE_DATETIME_FORMAT_INDEX,
        'enableOlFilter': True,
        'enableSpamFilter': False,
        'enableStoreMws': True,
        'enableStoreCws': True,
        'windowsPersistens': {
            'management': { },
            'channels': { } },
        'invitesFromFriendsOnly': False }
    _MessengerSettings__lobby = {
        'popUpMessageLifeTime': SCH_DEFAULT_POP_UP_MSG_LIFE_TIME,
        'popUpMessageAlphaSpeed': 0,
        'popUpMessageStackLength': SCH_DEFAULT_POP_UP_MSG_STACK_LENGTH,
        'inviteLinkFormat': '%(id)d %(message)s',
        'inviteNoteFormat': '%(note)s',
        'forseDestroyPrebattleChannel': False }
    _MessengerSettings__battle = {
        'messageLifeTime': BATTLE_DEFAULT_MESSAGE_LIFE_TIME,
        'messageAlphaSpeed': 0,
        'inactiveStateAlpha': 100,
        'hintText': '',
        'toolTipText': '',
        'receivers': { } }
    _MessengerSettings__battleMsgColorScheme = {
        'team': {
            'default': Math.Vector3(0, 255, 0) },
        'common': {
            'default': Math.Vector3(255, 255, 255) },
        'squad': {
            'default': Math.Vector3(255, 255, 0) },
        'unknown': {
            'default': Math.Vector3(42, 42, 42) } }
    _MessengerSettings__battlePlayerColorScheme = {
        'himself': {
            'default': Math.Vector3(255, 255, 0) },
        'teammate': {
            'default': Math.Vector3(0, 255, 0) },
        'enemy': {
            'default': Math.Vector3(255, 0, 0) },
        'unknown': {
            'default': Math.Vector3(42, 42, 42) },
        'teamkiller': {
            'default': Math.Vector3(0, 235, 0) },
        'squadman': {
            'default': Math.Vector3(255, 235, 0) },
        'himselfTgt': {
            'default': Math.Vector3(255, 244, 181) } }
    _MessengerSettings__battleRecvColorScheme = dict(map((lambda name: (name, {
'default': Math.Vector3(255, 255, 255) })), BATTLE_CHANNELS.NAMES))
    _MessengerSettings__debug = {
        'dumpWaitingToDestroyChannels': False }
    _MessengerSettings__protocols = { }
    coloringForBadWordFormat = '<font color="#00FFFF">%s</font>'
    
    def __init__(self, resourceId):
        self._MessengerSettings__resourceId = resourceId
        self.htmlTemplates = templates.XMLCollection(self._MessengerSettings__resourceId, 'htmlTemplatesSimple')
        self.msgTemplates = _MessageTemplates(self._MessengerSettings__resourceId, 'htmlTemplates')
        self.onApplyUserPreferences = Event.Event()

    
    def getColorSchemeTag(self, roster):
        tag = 'user'
        if bool(roster & USERS_ROSTER_FRIEND):
            tag = self._MessengerSettings__userRosterKayPairs[USERS_ROSTER_FRIEND]
        elif bool(roster & USERS_ROSTER_IGNORED):
            tag = self._MessengerSettings__userRosterKayPairs[USERS_ROSTER_IGNORED]
        
        return tag

    
    def lobbySettings(self):
        return self._MessengerSettings__lobby.copy()

    lobbySettings = property(lobbySettings)
    
    def battleSettings(self):
        return self._MessengerSettings__battle.copy()

    battleSettings = property(battleSettings)
    
    def debugSettings(self):
        return self._MessengerSettings__debug.copy()

    debugSettings = property(debugSettings)
    
    def userPreferences(self):
        return self._MessengerSettings__user.copy()

    userPreferences = property(userPreferences)
    
    def supportedProtocols(self):
        return self._MessengerSettings__protocols.copy()

    supportedProtocols = property(supportedProtocols)
    
    def getLobbyMsgFormat(self, message, user):
        if user.himself:
            key = 'himself'
        elif user.breaker:
            key = 'breaker'
        else:
            groupIdx = message.group
            if CHAT_MEMBER_GROUP.member.index() == groupIdx:
                key = self.getColorSchemeTag(user.roster)
            else:
                key = CHAT_MEMBER_GROUP[groupIdx].name()
        return self._MessengerSettings__lobbyMFormats.get(key, LOBBY_MESSAGE_FORMAT)

    
    def getLobbyUserCS(self, roster, himself = False):
        if himself:
            pass
        1
        key = self.getColorSchemeTag(roster)
        scheme = self._MessengerSettings__lobbyUserColorScheme[key][2]
        return [
            scheme['offline'],
            scheme['online']]

    
    def _formatToHex(self, colorScheme, group):
        if group in colorScheme:
            pass
        1
        sub = group['default']
        return '%02X%02X%02X' % sub.tuple()

    
    def _MessengerSettings__getHexCS(self, colorSchemes, isColorBlind = False):
        group = 'default'
        if isColorBlind:
            group = 'colorBlind'
        
        return None((dict, map)((lambda item: (item[0], self._formatToHex(item[1], group))), colorSchemes.iteritems()))

    
    def getBattlePlayerHexCS(self, isColorBlind = False):
        return self._MessengerSettings__getHexCS(self._MessengerSettings__battlePlayerColorScheme, isColorBlind = isColorBlind)

    
    def getBattleMsgHexCS(self, isColorBlind = False):
        return self._MessengerSettings__getHexCS(self._MessengerSettings__battleMsgColorScheme, isColorBlind = isColorBlind)

    
    def getBattleRecvHexCS(self, isColorBlind = False):
        return self._MessengerSettings__getHexCS(self._MessengerSettings__battleRecvColorScheme, isColorBlind = isColorBlind)

    
    def read(self):
        self.readUserPreference()
        self.readXML()

    
    def readUserPreference(self):
        userPrefs = Settings.g_instance.userPrefs
        if not userPrefs.has_key(Settings.KEY_MESSENGER_PREFERENCES):
            userPrefs.write(Settings.KEY_MESSENGER_PREFERENCES, '')
            self.saveUserPreferences()
        else:
            ds = userPrefs[Settings.KEY_MESSENGER_PREFERENCES]
            if ds.has_key('showJoinLeaveMessages'):
                ds.deleteSection('showJoinLeaveMessages')
            
            self._MessengerSettings__user['datetimeIdx'] = ds.readInt('datetimeIdx', self._MessengerSettings__user['datetimeIdx'])
            self._MessengerSettings__user['enableOlFilter'] = ds.readBool('enableOlFilter', self._MessengerSettings__user['enableOlFilter'])
            self._MessengerSettings__user['enableSpamFilter'] = ds.readBool('enableSpamFilter', self._MessengerSettings__user['enableSpamFilter'])
            self._MessengerSettings__user['invitesFromFriendsOnly'] = ds.readBool('invitesFromFriendsOnly', self._MessengerSettings__user['invitesFromFriendsOnly'])
            self._MessengerSettings__user['enableStoreMws'] = ds.readBool('enableStoreMws', self._MessengerSettings__user['enableStoreMws'])
            self._MessengerSettings__user['enableStoreCws'] = ds.readBool('enableStoreCws', self._MessengerSettings__user['enableStoreCws'])
            if ds.has_key('windows'):
                pass
            1
            wSection = { }
            if wSection.has_key('management'):
                pass
            1
            mSection = { }
            for (windowName, pSection) in mSection.items():
                if pSection.has_key('name'):
                    pass
                1
                windowName = None
                if pSection.has_key('persistent'):
                    pass
                1
                persistent = None
                if len(windowName) > 0 and persistent != Math.Vector4(-1, -1, -1, -1):
                    self._MessengerSettings__user['windowsPersistens']['management'][windowName] = persistent
                    continue
                pSection.readVector4('persistent', (-1, -1, -1, -1))
            
            if wSection.has_key('channels'):
                pass
            1
            chSection = { }
            for (_, pSection) in chSection.items():
                if pSection.has_key('cid'):
                    pass
                1
                channelId = None
                if pSection.has_key('persistent'):
                    pass
                1
                persistent = None
                if channelId != 0x0L and persistent != Math.Vector4(-1, -1, -1, -1):
                    self._MessengerSettings__user['windowsPersistens']['channels'][channelId] = persistent
                    continue
                pSection.readVector4('persistent', (-1, -1, -1, -1))
            

    
    def _MessengerSettings__readProtocolsXmlSettings(self, protocols):
        for (name, section) in protocols.items():
            self._MessengerSettings__protocols[name] = section.asString
        

    
    def _MessengerSettings__readLobbyXmlSettings(self, lobby):
        propsSec = lobby['defUserProps']
        if propsSec:
            pass
        1
        tags = { }
        for (getter, all) in self._MessengerSettings__defUserPropsGetters.iteritems():
            if key in tags:
                value = getattr(propsSec, getter)(key)
                if all is None or value in all:
                    self._MessengerSettings__user[key] = value
                
            value in all
        
        colorScheme = lobby['colorScheme']
        if colorScheme:
            messageBodyColor = '%02X%02X%02X' % colorScheme.readVector3('messageBody', Math.Vector3(0, 0, 0)).tuple()
            self._MessengerSettings__lobbyMFormats = { }
            if colorScheme.has_key('group'):
                pass
            1
            gSection = { }
            for (group, cSection) in gSection.items():
                userNameColor = '%02X%02X%02X' % cSection.asVector3.tuple()
                self._MessengerSettings__lobbyMFormats[group] = '<font color="#%s">' % userNameColor + '%s</font>' + ' <font color="#%s">' % userNameColor + '%s</font>' + ' <font color="#%s">' % messageBodyColor + '%s</font>'
            
            if colorScheme.has_key('userRoster'):
                pass
            1
            urSection = { }
            for (showOffline, showOnline, _) in self._MessengerSettings__lobbyUserColorScheme.iteritems():
                if urSection.has_key(userType):
                    pass
                1
                uSection = { }
                if showOnline:
                    if uSection.has_key('online'):
                        pass
                    1
                    onlineColor = (0, 0, 0)
                    self._MessengerSettings__lobbyUserColorScheme[userType][2]['online'] = (int(onlineColor[0]) << 16) + (int(onlineColor[1]) << 8) + (int(onlineColor[2]) << 0)
                    onlineColor = '%02X%02X%02X' % onlineColor
                    self._MessengerSettings__lobbyMFormats[userType] = '<font color="#%s">' % onlineColor + '%s</font>' + ' <font color="#%s">' % onlineColor + '%s</font>' + ' <font color="#%s">' % messageBodyColor + '%s</font>'
                
                if showOffline:
                    if uSection.has_key('offline'):
                        pass
                    1
                    offlineColor = (0, 0, 0)
                    self._MessengerSettings__lobbyUserColorScheme[userType][2]['offline'] = (int(offlineColor[0]) << 16) + (int(offlineColor[1]) << 8) + (int(offlineColor[2]) << 0)
                    continue
                uSection['offline'].asVector3.tuple()
            
            badWordColor = '%02X%02X%02X' % colorScheme.readVector3('badWord', Math.Vector3(0, 0, 0)).tuple()
            self.coloringForBadWordFormat = '<font color="#' + badWordColor + '">%s</font>'
            breakerColor = '%02X%02X%02X' % colorScheme.readVector3('breaker', Math.Vector3(0, 0, 0)).tuple()
            self._MessengerSettings__lobbyMFormats['breaker'] = '<font color="#%s">' % breakerColor + '%s</font>' + ' <font color="#%s">' % messageBodyColor + '%s</font>' + ' <font color="#%s">' % messageBodyColor + '%s</font>'
        
        serviceChannel = lobby['serviceChannel']
        if serviceChannel:
            self._MessengerSettings__lobby['popUpMessageLifeTime'] = serviceChannel.readFloat('lifeTime', SCH_DEFAULT_POP_UP_MSG_LIFE_TIME)
            self._MessengerSettings__lobby['popUpMessageAlphaSpeed'] = serviceChannel.readFloat('alphaSpeed', 0)
            self._MessengerSettings__lobby['popUpMessageStackLength'] = serviceChannel.readInt('stackLength', SCH_DEFAULT_POP_UP_MSG_STACK_LENGTH)
        
        invites = lobby['invites']
        if invites:
            self._MessengerSettings__lobby['inviteLinkFormat'] = invites.readString('linkFormat', '%(id)d %(message)s')
            self._MessengerSettings__lobby['inviteNoteFormat'] = invites.readString('noteFormat', '%(note)s')
        
        prebattle = lobby['prebattle']
        if prebattle:
            self._MessengerSettings__lobby['forseDestroyPrebattleChannel'] = prebattle.readBool('forseDestroyChannel')
        

    
    def _MessengerSettings__readBattlePlayerCSItem(self, csSection):
        result = {
            'default': Math.Vector3(0, 0, 0) }
        items = csSection.items()
        if len(items):
            result.update(dict((lambda .0: for (key, section) in .0:
(key, section.asVector3))(items)))
        else:
            result = {
                'default': csSection.asVector3 }
        return result

    
    def _MessengerSettings__updateBattlePlayerCSGroups(self, section, csData):
        if section is None:
            return None
        for key in csData.keys():
            sub = section[key]
            if sub is not None:
                csData[key] = self._MessengerSettings__readBattlePlayerCSItem(sub)
                continue
            section is None
        

    
    def _MessengerSettings__readBattleXmlSettings(self, battle):
        self._MessengerSettings__battle['messageLifeTime'] = battle.readFloat('lifeTime')
        self._MessengerSettings__battle['messageAlphaSpeed'] = battle.readFloat('alphaSpeed')
        self._MessengerSettings__battle['inactiveStateAlpha'] = battle.readInt('inactiveStateAlpha', 100)
        self._MessengerSettings__battle['hintText'] = html_translation(battle.readString('hintText'))
        self._MessengerSettings__battle['toolTipText'] = html_translation(battle.readString('toolTipText'))
        subSec = battle['colorScheme']
        if subSec:
            self._MessengerSettings__updateBattlePlayerCSGroups(subSec['player'], self._MessengerSettings__battlePlayerColorScheme)
            self._MessengerSettings__updateBattlePlayerCSGroups(subSec['messageBody'], self._MessengerSettings__battleMsgColorScheme)
            self._MessengerSettings__updateBattlePlayerCSGroups(subSec['receiverLabel'], self._MessengerSettings__battleRecvColorScheme)
        
        subSec = battle['receivers']
        if subSec:
            receivers = { }
            for data in BATTLE_CHANNELS.ALL:
                name = data[1]
                recvSec = subSec[name]
                if recvSec:
                    receivers[name] = [
                        html_translation(recvSec.readString('label')),
                        recvSec.readInt('modifier'),
                        recvSec.readInt('order')]
                    continue
                receivers[name] = [
                    data[2],
                    0,
                    0]
            
            self._MessengerSettings__battle['receivers'] = receivers
        

    
    def _MessengerSettings__readDebugXmlSettings(self, debug):
        self._MessengerSettings__debug['dumpWaitingToDestroyChannels'] = debug.readBool('dumpWaitingToDestroyChannels')

    
    def readXML(self):
        section = ResMgr.openSection(self._MessengerSettings__resourceId)
        if section is None:
            return None
        protocols = section['protocols']
        if protocols:
            self._MessengerSettings__readProtocolsXmlSettings(protocols)
        
        lobby = section['lobby']
        if lobby:
            self._MessengerSettings__readLobbyXmlSettings(lobby)
        
        battle = section['battle']
        if battle:
            self._MessengerSettings__readBattleXmlSettings(battle)
        
        debug = section['debug']
        if debug:
            self._MessengerSettings__readDebugXmlSettings(debug)
        
        self.htmlTemplates.load(section = section)
        self.msgTemplates.load(section = section)

    
    def saveUserPreferences(self):
        ds = Settings.g_instance.userPrefs[Settings.KEY_MESSENGER_PREFERENCES]
        ds.writeInt('datetimeIdx', self._MessengerSettings__user['datetimeIdx'])
        ds.writeBool('enableOlFilter', self._MessengerSettings__user['enableOlFilter'])
        ds.writeBool('enableSpamFilter', self._MessengerSettings__user['enableSpamFilter'])
        ds.writeBool('enableStoreMws', self._MessengerSettings__user['enableStoreMws'])
        ds.writeBool('enableStoreCws', self._MessengerSettings__user['enableStoreCws'])
        ds.writeBool('invitesFromFriendsOnly', self._MessengerSettings__user['invitesFromFriendsOnly'])
        if not self._MessengerSettings__user['enableStoreMws']:
            self._MessengerSettings__user['windowsPersistens']['management'] = { }
        
        if not self._MessengerSettings__user['enableStoreCws']:
            self._MessengerSettings__user['windowsPersistens']['channels'] = { }
        

    
    def saveWindowPersistens(self):
        ds = Settings.g_instance.userPrefs[Settings.KEY_MESSENGER_PREFERENCES]
        ds.deleteSection('windows')
        wSection = ds.createSection('windows')
        mSection = wSection.createSection('management')
        management = self._MessengerSettings__user['windowsPersistens']['management']
        for (windowName, persistent) in management.iteritems():
            section = mSection.createSection('window')
            section.writeString('name', windowName)
            section.writeVector4('persistent', persistent)
        
        chSection = wSection.createSection('channels')
        channels = self._MessengerSettings__user['windowsPersistens']['channels']
        for (channelId, persistent) in channels.iteritems():
            section = chSection.createSection('channel')
            section.writeInt64('cid', channelId)
            section.writeVector4('persistent', persistent)
        
        Settings.g_instance.save()

    
    def applyWindowPersistens(self, management, channels):
        if self._MessengerSettings__user['enableStoreMws']:
            self._MessengerSettings__user['windowsPersistens']['management'] = management
        
        if self._MessengerSettings__user['enableStoreCws']:
            self._MessengerSettings__user['windowsPersistens']['channels'] = channels
        
        self.saveWindowPersistens()

    
    def applyUserPreferences(self, **kwargs):
        self._MessengerSettings__user.update(kwargs)
        self.saveUserPreferences()
        self.onApplyUserPreferences()



