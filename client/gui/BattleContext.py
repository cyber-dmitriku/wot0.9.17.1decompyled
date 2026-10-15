# Source Generated with Decompyle++
# File: BattleContext.pyc (Python 2.6)

import BigWorld
import Settings
import constants
from enumerations import AttributeEnumItem, Enumeration
PLAYER_ENTITY_NAME = Enumeration('Player entity name in battle', [
    ('ally', {
        'isFriend': True,
        'base': 'ally' }),
    ('teamKiller', {
        'isFriend': True,
        'base': 'ally' }),
    ('squadman', {
        'isFriend': True,
        'base': 'ally' }),
    ('enemy', {
        'isFriend': False,
        'base': 'enemy' })], instance = AttributeEnumItem)

class _BattleContext(object):
    _BattleContext__playerFullNameFormats = {
        1: '{0:>s} ({2:>s})',
        16: '{0:>s}[{1:>s}]',
        17: '{0:>s}[{1:>s}] ({2:>s})' }
    
    def __init__(self):
        super(_BattleContext, self).__init__()
        self._BattleContext__playersVIDs = { }
        self._BattleContext__squadID = None
        self._BattleContext__squadManVIDs = set()
        self._BattleContext__teamKillerVIDs = set()
        self._BattleContext__observerVIDs = set()
        self._BattleContext__isShowVehShortName = True
        self.lastArenaUniqueID = None

    
    def init(self):
        prefs = Settings.g_instance.userPrefs
        if prefs is not None:
            self._BattleContext__isShowVehShortName = prefs.readBool('showVehShortName', True)
        
        player = BigWorld.player()
        if not player:
            return None
        arena = getattr(player, 'arena', None)
        if arena is None:
            return None
        playerVehID = getattr(player, 'playerVehicleID', None)
        prebattleID = arena.vehicles.get(playerVehID, { }).get('prebattleID')
        if arena.guiType == constants.ARENA_GUI_TYPE.RANDOM and prebattleID > 0:
            self._BattleContext__squadID = prebattleID
        
        self._BattleContext__findRequiredData()
        arena.onNewVehicleListReceived += self._BattleContext__arena_onNewVehicleListReceived
        arena.onVehicleAdded += self._BattleContext__arena_onVehicleAdded
        arena.onTeamKiller += self._BattleContext__arena_onTeamKiller

    
    def fini(self):
        self._BattleContext__playersVIDs.clear()
        self._BattleContext__squadManVIDs.clear()
        self._BattleContext__teamKillerVIDs.clear()
        self._BattleContext__observerVIDs.clear()
        self._BattleContext__squadID = None
        arena = getattr(BigWorld.player(), 'arena', None)
        if arena is None:
            arena.onNewVehicleListReceived -= self._BattleContext__arena_onNewVehicleListReceived
            arena.onVehicleAdded -= self._BattleContext__arena_onVehicleAdded
            arena.onTeamKiller -= self._BattleContext__arena_onTeamKiller
        

    
    def getVehIDByAccDBID(self, accDBID):
        return self._BattleContext__playersVIDs.get(accDBID, 0)

    
    def getFullPlayerName(self, vData = None, vID = None, accID = None, pName = None, showVehShortName = True, showClan = True):
        key = 0
        vehShortName = ''
        if vData is None:
            arena = getattr(BigWorld.player(), 'arena', None)
            if vID is None:
                vID = self._BattleContext__playersVIDs.get(accID, 0)
            
            if arena:
                pass
            1
            vData = { }
        
        if showVehShortName and self._BattleContext__isShowVehShortName:
            vehType = vData.get('vehicleType')
            if vehType is not None:
                vehShortName = vehType.type.shortUserString
                key |= 1
            
        
        if pName is None:
            pName = vData.get('name', '')
        
        clanAbbrev = ''
        if showClan:
            clanAbbrev = vData.get('clanAbbrev', '')
            if clanAbbrev is not None and len(clanAbbrev) > 0:
                key |= 16
            
        
        if key == 0:
            return pName
        return self._BattleContext__playerFullNameFormats.get(key, '{0:>s}').format(pName, clanAbbrev, vehShortName)

    
    def isSquadMan(self, vID = None, accID = None):
        if vID is None:
            vID = self._BattleContext__playersVIDs.get(accID)
        
        if self._BattleContext__squadID:
            pass
        return vID in self._BattleContext__squadManVIDs

    
    def isTeamKiller(self, vID = None, accID = None):
        if vID is None:
            vID = self._BattleContext__playersVIDs.get(accID)
        
        return vID in self._BattleContext__teamKillerVIDs

    
    def isObserver(self, vID):
        return vID in self._BattleContext__observerVIDs

    
    def isPlayerObserver(self):
        return getattr(BigWorld.player(), 'playerVehicleID', -1) in self._BattleContext__observerVIDs

    
    def getPlayerEntityName(self, vID, vData):
        entityName = PLAYER_ENTITY_NAME.enemy
        if BigWorld.player().team == vData.get('team'):
            if self.isTeamKiller(vID = vID):
                entityName = PLAYER_ENTITY_NAME.teamKiller
            elif self.isSquadMan(vID = vID):
                entityName = PLAYER_ENTITY_NAME.squadman
            else:
                entityName = PLAYER_ENTITY_NAME.ally
        
        return entityName

    
    def _BattleContext__findRequiredData(self):
        self._BattleContext__playersVIDs.clear()
        self._BattleContext__squadManVIDs.clear()
        self._BattleContext__teamKillerVIDs.clear()
        arena = BigWorld.player().arena
        for (vID, vData) in arena.vehicles.iteritems():
            self._BattleContext__addVehicleData(vID, vData)
        

    
    def _BattleContext__addVehicleData(self, vID, vData):
        accDBID = vData.get('accountDBID', 0)
        if accDBID > 0:
            self._BattleContext__playersVIDs[accDBID] = vID
        
        if self._BattleContext__squadID and self._BattleContext__squadID == vData.get('prebattleID'):
            self._BattleContext__squadManVIDs.add(vID)
        
        if vData.get('isTeamKiller', False) and BigWorld.player().team == vData.get('team'):
            self._BattleContext__teamKillerVIDs.add(vID)
        
        vDesc = vData.get('vehicleType')
        if vDesc is not None and 'observer' in vDesc.type.tags:
            self._BattleContext__observerVIDs.add(vID)
        

    
    def _BattleContext__arena_onNewVehicleListReceived(self):
        self._BattleContext__findRequiredData()

    
    def _BattleContext__arena_onVehicleAdded(self, vID):
        self._BattleContext__addVehicleData(vID, BigWorld.player().arena.vehicles.get(vID, { }))

    
    def _BattleContext__arena_onTeamKiller(self, vID):
        vData = BigWorld.player().arena.vehicles.get(vID, { })
        if vData.get('isTeamKiller', False) and BigWorld.player().team == vData.get('team'):
            self._BattleContext__teamKillerVIDs.add(vID)
        


g_battleContext = _BattleContext()

