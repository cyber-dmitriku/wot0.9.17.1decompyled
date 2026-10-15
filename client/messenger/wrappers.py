# Source Generated with Decompyle++
# File: wrappers.pyc (Python 2.6)

import BigWorld
import constants
from collections import namedtuple
from chat_shared import CHAT_CHANNEL_BATTLE, CHAT_CHANNEL_BATTLE_TEAM, CHAT_CHANNEL_PREBATTLE, CHAT_CHANNEL_PRIVATE, CHAT_CHANNEL_SQUAD, CHAT_CHANNEL_TEAM, CHAT_CHANNEL_PREBATTLE_CLAN, CHAT_CHANNEL_TOURNAMENT, CHAT_CHANNEL_CLAN
from chat_shared import USERS_ROSTER_FRIEND, USERS_ROSTER_IGNORED, SYS_MESSAGE_IMPORTANCE, USERS_ROSTER_VOICE_MUTED
from items import vehicles
from helpers import time_utils
from messenger import LAZY_CHANNELS, passCensor
import time as _time
import types
from helpers import int2roman
_ChannelData = namedtuple('_ChannelData', ' '.join([
    'cid',
    'channelName',
    'ownerName',
    'isReadOnly',
    'isSystem',
    'isSecured',
    'greeting',
    'flags',
    'notifyFlags',
    'lazy',
    'channelNameCensored']))

class ChannelWrapper(_ChannelData):
    
    def __new__(cls, id = 0, channelName = 'Unknown', owner = -0x1L, ownerName = '', isReadOnly = False, isSystem = False, isSecured = False, greeting = '', flags = 0, notifyFlags = 0, **kwargs):
        lazy = 0
        if isSystem and channelName in LAZY_CHANNELS.INDICES:
            indiceIdx = LAZY_CHANNELS.INDICES.index(channelName)
            lazy = LAZY_CHANNELS.CLIENT_IDXS[indiceIdx]
        
        UsersManager = UsersManager
        import messenger.UsersManager
        if UsersManager.isCurrentPlayer(owner):
            pass
        1
        result = cls(id, channelName, ownerName, isReadOnly, isSystem, isSecured, greeting, flags, notifyFlags, lazy, channelName, passCensor(channelName))
        result.password = None
        result.joined = False
        result.joinedTime = None
        result.selected = False
        result.owner = owner
        result.hidden = False
        result.waitingDestroyedEvent = False
        return result

    
    def isPrebattle(self):
        return self.flags & CHAT_CHANNEL_PREBATTLE != 0

    isPrebattle = property(isPrebattle)
    
    def isBattleSession(self):
        if not self.flags & CHAT_CHANNEL_PREBATTLE_CLAN != 0:
            pass
        return self.flags & CHAT_CHANNEL_TOURNAMENT != 0

    isBattleSession = property(isBattleSession)
    
    def isBattle(self):
        return self.flags & CHAT_CHANNEL_BATTLE != 0

    isBattle = property(isBattle)
    
    def isBattleTeam(self):
        return self.flags & CHAT_CHANNEL_BATTLE_TEAM != 0

    isBattleTeam = property(isBattleTeam)
    
    def isPrivate(self):
        return self.flags & CHAT_CHANNEL_PRIVATE != 0

    isPrivate = property(isPrivate)
    
    def isSquad(self):
        return self.flags & CHAT_CHANNEL_SQUAD != 0

    isSquad = property(isSquad)
    
    def isCompany(self):
        return self.flags & CHAT_CHANNEL_TEAM != 0

    isCompany = property(isCompany)
    
    def isClan(self):
        return self.flags & CHAT_CHANNEL_CLAN != 0

    isClan = property(isClan)
    
    def update(self, other):
        other.password = self.password
        other.selected = self.selected
        other.joined = self.joined
        other.joinedTime = self.joinedTime
        return other

    
    def __eq__(self, other):
        return self.cid == other.cid

    
    def __hash__(self):
        return self.cid

    
    def __repr__(self):
        return 'ChannelWrapper(cid={0[0]!r:s}, channelName={0[1]!r:s}, owner={1!r:s}, ownerName={0[2]!r:s}, isReadOnly={0[3]!r:s}, isSystem={0[4]!r:s}, isSecured={0[5]!r:s}, greeting={0[6]!r:s}, flags={0[7]!r:s}, notifyFlags={0[8]!r:s}, lazy={0[9]!r:s}, joined={2!r:s}, joinedTime={3!r:s}, hidden={4!r:s})'.format(self, self.owner, self.joined, self.joinedTime, self.hidden)


_MemberData = namedtuple('_MemberData', 'uid nickName')

class MemberWrapper(_MemberData):
    
    def __new__(cls, id = -0x1L, nickName = 'Unknown', status = 0):
        result = _MemberData.__new__(cls, long(id), unicode(nickName, 'utf-8', errors = 'ignore'))
        result.status = int(status)
        return result

    
    def tuple(self):
        return (self.uid, self.nickName, self.status)

    
    def __eq__(self, other):
        return self.uid == other.uid

    
    def __hash__(self):
        return self.uid

    
    def __repr__(self):
        return 'MemberWrapper(uid=%r, nickName=%s, status=%d)' % (self.uid, self.nickName, self.status)


_SquadPlayerData = namedtuple('_SquadPlayerData', ' '.join([
    'accId',
    'name',
    'dbID',
    'time',
    'clanAbbrev']))

class SquadPlayerWrapper(_SquadPlayerData):
    
    def __new__(cls, id = -0x1L, name = 'Unknown', dbID = -0x1L, state = 0, time = 0, vehCompDescr = '', clanAbbrev = '', **kwargs):
        result = _SquadPlayerData.__new__(cls, id, name, dbID, time, clanAbbrev)
        result.state = state
        result.roles = 0
        result.vehCompDescr = vehCompDescr
        return result

    
    def vUserString(self):
        if self.vehCompDescr and len(self.vehCompDescr) > 0:
            return vehicles.VehicleDescr(compactDescr = self.vehCompDescr).type.shortUserString
        return ''

    vUserString = property(vUserString)
    
    def isCommander(self):
        if self.roles is not None:
            return self.roles & constants.PREBATTLE_ROLE.SQUAD_CREATOR != 0
        return False

    isCommander = property(isCommander)
    
    def displayName(self):
        if self.clanAbbrev:
            return '%s[%s]' % (self.name, self.clanAbbrev)
        return self.name

    displayName = property(displayName)
    
    def __repr__(self):
        return 'SquadPlayerWrapper(accId=%r, name=%s, dbID= %d, state=%d, roles=%d, time=%f, vehCompDescr=%s, displayName=%s)' % (self.accId, self.name, self.dbID, self.state, self.roles, self.time, self.vehCompDescr, self.displayName)


_TeamPlayerData = namedtuple('_TeamPlayerData', ' '.join([
    'accId',
    'name',
    'dbID',
    'time',
    'clanAbbrev',
    'clanDBID']))

class TeamPlayerWrapper(_TeamPlayerData):
    
    def __new__(cls, id = -0x1L, name = 'Unknown', dbID = -0x1L, state = 0, time = 0, vehCompDescr = '', clanAbbrev = '', clanDBID = 0, **kwargs):
        result = _TeamPlayerData.__new__(cls, id, name, dbID, time, clanAbbrev, clanDBID)
        result.state = state
        result.roles = 0
        result.vehCompDescr = vehCompDescr
        return result

    
    def vUserString(self):
        if self.vehCompDescr and len(self.vehCompDescr) > 0:
            return vehicles.VehicleDescr(compactDescr = self.vehCompDescr).type.shortUserString
        return ''

    vUserString = property(vUserString)
    
    def _TeamPlayerWrapper__checkVehicleType(self, typeStrID):
        if self.vehCompDescr and len(self.vehCompDescr) > 0:
            return typeStrID in vehicles.VEHICLE_CLASS_TAGS.intersection(vehicles.VehicleDescr(compactDescr = self.vehCompDescr).type.tags)
        return False

    
    def isVehicleSPG(self):
        return self._TeamPlayerWrapper__checkVehicleType('SPG')

    isVehicleSPG = property(isVehicleSPG)
    
    def isVehicleATSPG(self):
        return self._TeamPlayerWrapper__checkVehicleType('AT-SPG')

    isVehicleATSPG = property(isVehicleATSPG)
    
    def isVehicleLightTank(self):
        return self._TeamPlayerWrapper__checkVehicleType('lightTank')

    isVehicleLightTank = property(isVehicleLightTank)
    
    def isVehicleMediumTank(self):
        return self._TeamPlayerWrapper__checkVehicleType('mediumTank')

    isVehicleMediumTank = property(isVehicleMediumTank)
    
    def isVehicleHeavyTank(self):
        return self._TeamPlayerWrapper__checkVehicleType('heavyTank')

    isVehicleHeavyTank = property(isVehicleHeavyTank)
    
    def vLevel(self):
        if self.vehCompDescr and len(self.vehCompDescr) > 0:
            return vehicles.VehicleDescr(compactDescr = self.vehCompDescr).level
        return 0

    vLevel = property(vLevel)
    
    def displayName(self):
        if self.clanAbbrev:
            return '%s[%s]' % (self.name, self.clanAbbrev)
        return self.name

    displayName = property(displayName)
    
    def vRomanLevel(self):
        return int2roman(self.vLevel)

    vRomanLevel = property(vRomanLevel)
    
    def isComm
