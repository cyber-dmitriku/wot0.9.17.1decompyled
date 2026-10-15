# Source Generated with Decompyle++
# File: Minimap.pyc (Python 2.6)

import BigWorld
import Math
import ResMgr
from gui.BattleContext import g_battleContext, PLAYER_ENTITY_NAME
from gui.Scaleform.utils.sound import Sound
from gui import GUI_SETTINGS
from functools import partial
from weakref import proxy
from helpers.gui_utils import *
from debug_utils import *
import string
import CommandMapping
from items.vehicles import VEHICLE_CLASS_TAGS
from account_helpers.AccountSettings import AccountSettings

class VehicleLocation:
    AOI = 0
    FAR = 1
    AOI_TO_FAR = 2


class Minimap(object):
    _Minimap__MINIMAP_SIZE = (210, 210)
    _Minimap__MINIMAP_CELLS = (10, 10)
    _Minimap__AOI_ESTIMATE = 450
    _Minimap__AOI_TO_FAR_TIME = 5
    
    def __init__(self, parentUI):
        self.proxy = proxy(self)
        self._Minimap__cfg = dict()
        player = BigWorld.player()
        arena = player.arena
        arenaType = arena.arenaType
        self._Minimap__cfg['texture'] = arenaType.minimap
        self._Minimap__cfg['teamBasePositions'] = arenaType.teamBasePositions
        self._Minimap__cfg['teamSpawnPoints'] = arenaType.teamSpawnPoints
        self._Minimap__cfg['controlPoint'] = arenaType.controlPoint
        self._Minimap__points = {
            'base': { },
            'spawn': { } }
        self._Minimap__entries = { }
        self._Minimap__enemyEntries = { }
        self._Minimap__main = None
        self._Minimap__vehiclesWaitStart = []
        self._Minimap__isStarted = False
        self._Minimap__parentUI = parentUI
        self._Minimap__ownUI = None
        self._Minimap__ownEntry = dict()
        self._Minimap__aoiToFarCallbacks = dict()
        self._Minimap__deadCallbacks = dict()
        self._Minimap__sndAttention = Sound('/GUI/notifications_FX/minimap_attention')
        self._Minimap__isFirstEnemyMarked = False
        self._Minimap__checkEnemyLengthID = None
        self.zIndexManager = MinimapZIndexManager()
        self._Minimap__observedVehicleId = -1

    
    def __del__(self):
        LOG_DEBUG('Minimap deleted')

    
    def start(self):
        self._Minimap__ownUI = GUI.WGMinimapFlash(self._Minimap__parentUI.movie)
        self._Minimap__ownUI.wg_inputKeyMode = 2
        self._Minimap__parentUI.component.addChild(self._Minimap__ownUI, 'minimap')
        self._Minimap__ownUI.mapSize = Math.Vector2(self._Minimap__MINIMAP_SIZE)
        (bl, tr) = BigWorld.player().arena.arenaType.boundingBox
        self._Minimap__ownUI.setArenaBB(bl, tr)
        tex = BigWorld.PyTextureProvider(self._Minimap__cfg['texture'])
        self._Minimap__ownUI.setBackground(tex)
        self._Minimap__cameraHandle = None
        self._Minimap__resetCamera('arcade')
        BigWorld.player().inputHandler.onCameraChanged += self._Minimap__resetCamera
        BigWorld.player().inputHandler.onPostmortemVehicleChanged += self._Minimap__clearCamera
        self._Minimap__parentUI.addExternalCallbacks({
            'minimap.onClick': self._onMapClicked,
            'minimap.playAttantion': self._playAttention,
            'minimap.setSize': self.onSetSize,
            'minimap.lightPlayer': self.onLightPlayer })
        player = BigWorld.player()
        self._Minimap__playerTeam = player.team
        self._Minimap__playerVehicleID = player.playerVehicleID
        arena = player.arena
        arena.onPositionsUpdated += self._Minimap__onFarPosUpdated
        arena.onNewVehicleListReceived += self._Minimap__validateEntries
        arena.onVehicleKilled += self._Minimap__onVehicleKilled
        arena.onVehicleAdded += self._Minimap__onVehicleAdded
        arena.onTeamKiller += self._Minimap__onTeamKiller
        self._Minimap__marks = { }
        if not g_battleContext.isPlayerObserver():
            mp = BigWorld.player().getOwnVehicleMatrix()
            self._Minimap__ownEntry['handle'] = self._Minimap__ownUI.addEntry(mp, self.zIndexManager.getIndexByName('self'))
            self._Minimap__ownEntry['matrix'] = player.getOwnVehicleMatrix()
            self._Minimap__ownEntry['location'] = None
        
        self._Minimap__isStarted = True
        for id in self._Minimap__vehiclesWaitStart:
            self.notifyVehicleStart(id)
        
        self._Minimap__vehiclesWaitStart = []
        self._Minimap__mapSizeIndex = AccountSettings.getSettings('minimapSize')
        AccountSettings.onSettingsChanging += self.setupMinimapSettings
        self.setupMinimapSettings()
        self.setTeamPoints()
        g_repeatKeyHandlers = g_repeatKeyHandlers
        import game
        g_repeatKeyHandlers.add(self.handleRepeatKeyEvent)

    
    def setupMinimapSettings(self, name = None):
        if name == 'minimapSize' or name is None:
            self._Minimap__parentUI.call('minimap.setupSize', [
                AccountSettings.getSettings('minimapSize')])
        
        if name == 'minimapAlpha' or name is None:
            self._Minimap__parentUI.call('minimap.setupAlpha', [
                AccountSettings.getSettings('minimapAlpha')])
        

    
    def setTeamPoints(self):
        if self._Minimap__cfg['teamBasePositions'] and self._Minimap__cfg['teamSpawnPoints'] or self._Minimap__cfg['controlPoint']:
            arenaDesc = BigWorld.player().arena.arenaType
            (bottomLeft, upperRight) = arenaDesc.boundingBox
            viewpoint = (upperRight + bottomLeft) * 0.5
            viewpointTranslate = Math.Matrix()
            viewpointTranslate.setTranslate((viewpoint.x, 0, viewpoint.y))
            player = BigWorld.player()
            currentTeam = player.team
            for (team, teamSpawnPoints) in enumerate(self._Minimap__cfg['teamSpawnPoints'], 1):
                self._Minimap__points['spawn'][team] = { }
                for (spawn, spawnPoint) in enumerate(teamSpawnPoints, 1):
                    pos = (spawnPoint[0], 0, spawnPoint[1])
                    m = Math.Matrix()
                    m.setTranslate(Math.Matrix(viewpointTranslate).applyPoint(pos))
                    self._Minimap__points['spawn'][team][spawn] = self._Minimap__ownUI.addEntry(m, self.zIndexManager.getTeamPointIndex())
                    if team == currentTeam:
                        pass
                    1
                    if len(teamSpawnPoints) > 1:
                        pass
                    1
                    'init'('points', ('spawn', [
                        'blue',
                        'red',
                        spawn + 1,
                        1]))
                
            
            for (team, teamBasePoints) in enumerate(self._Minimap__cfg['teamBasePositions'], 1):
                self._Minimap__points['base'][team] = { }
                for (base, basePoint) in teamBasePoints.items():
                    pos = (basePoint[0], 0, basePoint[1])
                    m = Math.Matrix()
                    m.setTranslate(Math.Matrix(viewpointTranslate).applyPoint(pos))
                    self._Minimap__points['base'][team][base] = self._Minimap__ownUI.addEntry(m, self.zIndexManager.getTeamPointIndex())
                    if team == currentTeam:
                        pass
                    1
                    if len(teamBasePoints) > 1:
                        pass
                    1
                    'init'('points', ('base', [
                        'blue',
                        'red',
                        len(self._Minimap__points['base'][team]) + 1,
                        1]))
                
            
            if self._Minimap__cfg['controlPoint']:
                pos = (self._Minimap__cfg['controlPoint'][0], 0, self._Minimap__cfg['controlPoint'][1])
                m = Math.Matrix()
                m.setTranslate(Math.Matrix(viewpointTranslate).applyPoint(pos))
                self._Minimap__points['control'] = self._Minimap__ownUI.addEntry(m, self.zIndexManager.getTeamPointIndex())
                self._Minimap__ownUI.entryInvoke(self._Minimap__points['control'], ('init', [
                    'points',
                    'control',
                    'empty',
                    1]))
            
            self._Minimap__parentUI.call('minimap.entryInited', [])
        

    
    def onSetSize(self, calbackID, index):
        self._Minimap__mapSizeIndex = int(index)
        self._Minimap__parentUI.call('minimap.setupSize', [
            self._Minimap__mapSizeIndex])

    
    def onLightPlayer(self, calbackID, vehicleID, visibility):
        self._Minimap__callEntryFlash(vehicleID, 'lightPlayer', [
            visibility])

    
    def destroy(self):
        if not self._Minimap__isStarted:
            self._Minimap__vehiclesWaitStart = []
            return None
        while len(self._Minimap__aoiToFarCallbacks):
            (_, callbackID) = self._Minimap__aoiToFarCallbacks.popitem()
            if callbackID is not None:
                BigWorld.cancelCallback(callbackID)
                continue
        self._Minimap__isStarted = False
        self._Minimap__entries = { }
        self._Minimap__cameraHandle = None
        self._Minimap__marks = None
        setattr(self._Minimap__parentUI.component, 'minimap', None)
        AccountSettings.onSettingsChanging -= self.setupMinimapSettings
        AccountSettings.setSettings('minimapSize', self._Minimap__mapSizeIndex)
        self._Minimap__parentUI = None
        g_repeatKeyHandlers = g_repeatKeyHandlers
        import game
        g_repeatKeyHandlers.remove(self.handleRepeatKeyEvent)

    
    def prerequisites(self):
        return []

    
    def setVisible(self, visible):
        pass

    
    def notifyVehicleStop(self, vehicleId):
        if not self._Minimap__isStarted:
            if vehicleId in self._Minimap__vehiclesWaitStart:
                self._Minimap__vehiclesWaitStart.remove(vehicleId)
            
            return None
        if vehicleId == self._Minimap__playerVehicleID:
            return None
        info = BigWorld.player().arena.vehicles.get(vehicleId)
        if info is None or not info['isAlive']:
            return None
        entries = self._Minimap__entries
        if vehicleId in entries:
            location = entries[vehicleId]['location']
            if location == VehicleLocation.AOI:
                ownPos = Math.Matrix(BigWorld.camera().invViewMatrix).translation
                entryPos = Math.Matrix(entries[vehicleId]['matrix']).translation
                if abs(ownPos.x - entryPos.x) < self._Minimap__AOI_ESTIMATE:
                    pass
                inAoI = bool(abs(ownPos.z - entryPos.z) < self._Minimap__AOI_ESTIMATE)
                self._Minimap__delEntry(vehicleId)
                if not inAoI:
                    self._Minimap__addEntry(vehicleId, VehicleLocation.AOI_TO_FAR)
                
            else:
                LOG_DEBUG('notifyVehicleOnStop, unknown minimap entry location', location)
        

    
    def notifyVehicleStart(self, vehicleId):
        if not self._Minimap__isStarted:
            self._Minimap__vehiclesWaitStart.append(vehicleId)
            return None
        if vehicleId == self._Minimap__playerVehicleID:
            return None
        info = BigWorld.player().arena.vehicles.get(vehicleId)
        if info is None or not info['isAlive']:
            return None
        entries = self._Minimap__entries
        if vehicleId in entries:
            self._Minimap__delEntry(vehicleId)
        
        self._Minimap__addEntry(vehicleId, VehicleLocation.AOI)

    
    def _playAttention(self, _):
        self._Minimap__sndAttention.play()

    
    def markCell(self, cellIndexes, duration):
        if not self._Minimap__isStarted:
            return None
        if cellIndexes < 0:
            return None
        (columnCount, rowCount) = Minimap._Minimap__MINIMAP_CELLS
        column = cellIndexes / columnCount % columnCount
        row = cellIndexes % columnCount
        if self._Minimap__marks.has_key(cellIndexes):
            BigWorld.cancelCallback(self._Minimap__marks[cellIndexes][1])
            self._removeCellMark(cellIndexes)
        
        arenaDesc = BigWorld.player().arena.arenaType
        (bottomLeft, upperRight) = arenaDesc.boundingBox
        viewpoint = (upperRight + bottomLeft) * 0.5
        viewpointTranslate = Math.Matrix()
        viewpointTranslate.setTranslate((viewpoint.x, 0, viewpoint.y))
        spaceSize = upperRight - bottomLeft
        pos = (column * spaceSize[0] / columnCount - spaceSize[0] * 0.5, 0, -row * spaceSize[1] / rowCount + spaceSize[0] * 0.5)
        m = Math.Matrix()
        m.setTranslate(Math.Matrix(viewpointTranslate).applyPoint(pos))
        mark = self._Minimap__ownUI.addEntry(m, self.zIndexManager.getIndexByName('cell'))
        self._Minimap__ownUI.entryInvoke(mark, ('gotoAndStop', [
            'cellFlash']))
        self._playAttention(None)
        callbackID = BigWorld.callback(duration, partial(self._removeCellMark, cellIndexes))
        self._Minimap__marks[cellIndexes] = (mark, callbackID)

    
    def getCellName(self, cellIndexes):
        (columnCount, rowCount) = Minimap._Minimap__MINIMAP_CELLS
        column = cellIndexes / columnCount % columnCount
        row = cellIndexes % columnCount
        if row < 8:
            name = string.ascii_uppercase[row]
        else:
            name = string.ascii_uppercase[row + 1]
        name += str((column + 1) % 10)
        return name

    
    def _removeCellMark(self, cellIndexes):
        if self._Minimap__isStarted:
            mark = self._Minimap__marks[cellIndexes][0]
            del self._Minimap__marks[cellIndexes]
            self._Minimap__ownUI.delEntry(mark)
        

    
    def _onMapClicked(self, _, x, y, bHighlightCellNVehicleSpecific = True):
        localPos = (x - 0.5, y - 0.5)
        mapSize = Minimap._Minimap__MINIMAP_SIZE
        player = BigWorld.player()
        if bHighlightCellNVehicleSpecific:
            cellCount = Minimap._Minimap__MINIMAP_CELLS
            row = int(cellCount[0] * localPos[0] / mapSize[0])
            column = int(cellCount[1] * localPos[1] / mapSize[1])
            player.onMinimapCellClicked(row * int(cellCount[1]) + column)
        elif 'SPG' in player.vehicleTypeDescriptor.type.tags:
            arenaDesc = BigWorld.player().arena.arenaType
            (bottomLeft, upperRight) = arenaDesc.boundingBox
            spaceSize = upperRight - bottomLeft
            viewpoint = (upperRight + bottomLeft) * 0.5
            viewpointTranslate = Math.Matrix()
            viewpointTranslate.setTranslate((viewpoint.x, 0, viewpoint.y))
            pos = ((localPos[0] - mapSize[0] * 0.5) / mapSize[0], (localPos[1] - mapSize[1] * 0.5) / mapSize[1])
            worldPos = Math.Matrix(viewpointTranslate).applyPoint((pos[0] * spaceSize[0], 0, -pos[1] * spaceSize[1]))
            player.inputHandler.onMinimapClicked(worldPos)
        

    
    def _Minimap__onVehicleAdded(self, id):
        arena = BigWorld.player().arena
        if not arena.vehicles[id]['isAlive']:
            return None
        location = self._Minimap__detectLocation(id)
        if location is not None:
            self._Minimap__addEntry(id, location)
        

    
    def _Minimap__onTeamKiller(self, id):
        self._Minimap__callEntryFlash(id, 'setEntryName', [
            PLAYER_ENTITY_NAME.teamKiller.name()])

    
    def _Minimap__onVehicleRemoved(self, id):
        if self._Minimap__entries.has_key(id):
            self._Minimap__delEntry(id)
        

    
    def _Minimap__onVehicleKilled(self, victimId, killerID, reason):
        if self._Minimap__entries.has_key(victimId):
            entry = self._Minimap__delEntry(victimId)
            if GUI_SETTINGS.showMinimapDeath:
                self._Minimap__addDeadEntry(entry, victimId)
            
        

    
    def _Minimap__onFarPosUpdated(self):
        entries = self._Minimap__entries
        arena = BigWorld.player().arena
        vehicles = arena.vehicles
        for (id, pos) in arena.positions.iteritems():
            entry = entries.get(id)
            if entry is not None:
                location = entry['location']
                if location == VehicleLocation.FAR:
                    entry['matrix'].setTranslate(pos)
                elif location == VehicleLocation.AOI_TO_FAR:
                    self._Minimap__delEntry(id)
                    self._Minimap__addEntry(id, VehicleLocation.FAR)
                
            location == VehicleLocation.FAR
            if vehicles[id]['isAlive']:
                self._Minimap__addEntry(id, VehicleLocation.FAR)
                continue
        
        for id in set(entries).difference(set(arena.positions)):
            location = entries[id]['location']
            if location == VehicleLocation.FAR:
                self._Minimap__delEntry(id)
                continue
            if location == VehicleLocation.AOI_TO_FAR:
                self._Minimap__delEntry(id)
                continue
        

    
    def _Minimap__validateEntries(self):
        entrySet = set(self._Minimap__entries.iterkeys())
        vehiclesSet = set(BigWorld.player().arena.vehicles.iterkeys())
        playerOnlySet = set((self._Minimap__playerVehicleID,))
        for id in vehiclesSet.difference(entrySet) - playerOnlySet:
            self._Minimap__onVehicleAdded(id)
        
        for id in entrySet.difference(vehiclesSet) - playerOnlySet:
            self._Minimap__onVehicleRemoved(id)
        

    
    def _Minimap__detectLocation(self, id):
        vehicle = BigWorld.entities.get(id)
        if vehicle is not None and vehicle.isStarted:
            return VehicleLocation.AOI
        if BigWorld.player().arena.positions.has_key(id):
            return VehicleLocation.FAR
        return None

    
    def _Minimap__delEntry(self, id, inCallback = False):
        entry = self._Minimap__entries.get(id)
        if entry is None:
            return None
        self._Minimap__ownUI.delEntry(entry['handle'])
        if entry.get('location') == VehicleLocation.AOI_TO_FAR:
            callbackId = self._Minimap__aoiToFarCallbacks.pop(id, None)
            if callbackId is not None:
                BigWorld.cancelCallback(callbackId)
            
        
        if id in self._Minimap__enemyEntries:
            self._Minimap__enemyEntries.pop(id)
            if not len(self._Minimap__enemyEntries):
                if self._Minimap__checkEnemyLengthID:
                    BigWorld.cancelCallback(self._Minimap__checkEnemyLengthID)
                
                self._Minimap__checkEnemyLengthID = BigWorld.callback(5, self._Minimap__checkEnemyLength)
            
        
        
        try:
            callbackId = self._Minimap__deadCallbacks.pop(id)
            BigWorld.cancelCallback(callbackId)
        except KeyError:
            entry is None
        except:
            entry is None

        return self._Minimap__entries.pop(id)

    
    def _Minimap__addDeadEntry(self, entry, id):
        '''
\t\tadding death animation to minimap (WOTD-5884)
\t\t'''
        m = self._Minimap__getEntryMatrixByLocation(id, entry['location'])
        entry['handle'] = self._Minimap__ownUI.addEntry(m, self.zIndexManager.getDeadVehicleIndex(id))
        self._Minimap__entries[id] = entry
        if not GUI_SETTINGS.permanentMinimapDeath:
            self._Minimap__deadCallbacks[id] = BigWorld.callback(GUI_SETTINGS.minimapDeathDuration / 1000, partial(self._Minimap__delEntry, id))
        
        self._Minimap__callEntryFlash(id, 'setDead', [
            GUI_SETTINGS.permanentMinimapDeath])
        self._Minimap__callEntryFlash(id, 'init', [
            entry['markerType'],
            entry['entryName'],
            entry['vClass'],
            ''])
        self._Minimap__parentUI.call('minimap.entryInited', [])

    
    def _Minimap__checkEnemyLength(self):
        self._Minimap__checkEnemyLengthID = None
        self._Minimap__isFirstEnemyMarked = not (len(self._Minimap__enemyEntries) == 0)

    
    def _Minimap__getEntryMatrixByLocation(self, id, location):
        matrix = None
        if location == VehicleLocation.AOI:
            matrix = BigWorld.entities[id].matrix
        elif location == VehicleLocation.AOI_TO_FAR:
            matrix = Math.Matrix(BigWorld.entities[id].matrix)
        elif location == VehicleLocation.FAR:
            matrix = Math.Matrix()
            pos = BigWorld.player().arena.positions[id]
            matrix.setTranslate(pos)
        
        m = Math.WGTranslationOnlyMP()
        m.source = matrix
        return m

    
    def _Minimap__addEntry(self, id, location):
        if g_battleContext.isObserver(id):
            return None
        arena = BigWorld.player().arena
        entry = dict()
        m = self._Minimap__getEntryMatrixByLocation(id, location)
        if location == VehicleLocation.AOI_TO_FAR:
            self._Minimap__aoiToFarCallbacks[id] = BigWorld.callback(self._Minimap__AOI_TO_FAR_TIME, partial(self._Minimap__delEntry, id))
        
        entry['location'] = location
        entry['matrix'] = m.source
        entry['handle'] = self._Minimap__ownUI.addEntry(m, self.zIndexManager.getVehicleIndex(id))
        self._Minimap__entries[id] = entry
        entryVehicle = arena.vehicles[id]
        entityName = g_battleContext.getPlayerEntityName(id, entryVehicle)
        markerType = entityName.base
        entryName = entityName.name()
        markMarker = ''
        if not entityName.isFriend:
            if not (self._Minimap__isFirstEnemyMarked) and not len(self._Minimap__enemyEntries):
                self._Minimap__isFirstEnemyMarked = True
                markMarker = 'firstEnemy'
                BigWorld.player().soundNotifications.play('enemy_sighted_for_team')
            
            self._Minimap__enemyEntries[id] = entry
        
        if entryVehicle['vehicleType'] is not None:
            tags = set(entryVehicle['vehicleType'].type.tags & VEHICLE_CLASS_TAGS)
        else:
            LOG_ERROR('Try to show minimap marker without vehicle info.')
            return None
        if entryVehicle['vehicleType'] is not None(tags) > 0:
            pass
        1
        vClass = ''
        if GUI_SETTINGS.showMinimapSuperHeavy and entryVehicle['vehicleType'].type.level == 10 and vClass == 'heavyTank':
            vClass = 'super' + vClass
        
        self._Minimap__callEntryFlash(id, 'init', [
            markerType,
            entryName,
            vClass,
            markMarker])
        entry['markerType'] = markerType
        entry['entryName'] = entryName
        entry['vClass'] = vClass
        self._Minimap__parentUI.call('minimap.entryInited', [])

    
    def updateEntries(self):
        self._Minimap__parentUI.call('minimap.updatePoints', [])
        for id in self._Minimap__entries:
            self._Minimap__callEntryFlash(id, 'update')
        

    
    def _Minimap__callEntryFlash(self, id, methodName, args = None):
        if not self._Minimap__isStarted:
            return None
        if args is None:
            args = []
        
        if self._Minimap__entries.has_key(id):
            self._Minimap__ownUI.entryInvoke(self._Minimap__entries[id]['handle'], (methodName, args))
        elif id == BigWorld.player().playerVehicleID:
            if self._Minimap__ownEntry.has_key('handle'):
                self._Minimap__ownUI.entryInvoke(self._Minimap__ownEntry['handle'], (methodName, args))
            
        

    
    def _Minimap__resetVehicleIfObserved(self, id):
        if self._Minimap__observedVehicleId > 0 and id == self._Minimap__observedVehicleId:
            self._Minimap__callEntryFlash(self._Minimap__observedVehicleId, 'setPostmortem', [
                False])
            if self._Minimap__entries.has_key(self._Minimap__observedVehicleId):
                entry = self._Minimap__entries[self._Minimap__observedVehicleId]
                if entry.has_key('handle'):
                    mp1 = self._Minimap__getEntryMatrixByLocation(self._Minimap__observedVehicleId, entry['location'])
                    self._Minimap__ownUI.entrySetMatrix(entry['handle'], mp1)
                
            
            self._Minimap__observedVehicleId = -1
        

    
    def _Minimap__resetCamera(self, mode, vehicleId = None):
        if g_battleContext.isPlayerObserver():
            return None
        if self._Minimap__cameraHandle is not None:
            self._Minimap__ownUI.delEntry(self._Minimap__cameraHandle)
        
        if mode == 'strategic':
            m = Math.WGTranslationOnlyMP()
            m.source = BigWorld.camera().invViewMatrix
        elif mode == 'arcade' or mode == 'sniper':
            m = Math.WGCombinedMP()
            m.translationSrc = BigWorld.player().getOwnVehicleMatrix()
            m.rotationSrc = BigWorld.camera().invViewMatrix
        elif mode == 'postmortem':
            m = Math.WGCombinedMP()
            if vehicleId is not None:
                translationSrc = Math.WGTranslationOnlyMP()
                translationSrc.source = BigWorld.entities[vehicleId].matrix
            else:
                translationSrc = BigWorld.player().getOwnVehicleMatrix()
            m.translationSrc = translationSrc
            m.rotationSrc = BigWorld.camera().invViewMatrix
        else:
            m = BigWorld.camera().invViewMatrix
        if mode == 'strategic':
            pass
        1
        self._Minimap__cameraHandle = m(self.zIndexManager.getIndexByName, 'cameraStrategic'('cameraNormal'))
        if mode == 'strategic':
            pass
        1
        self._Minimap__cameraHandle('gotoAndStop', ('cursorStrategic', [
            'cursorNormal']))
        playerMarker = 'normal'
        if mode == 'strategic':
            playerMarker = 'strategic'
        
        if mode == 'postmortem':
            self._Minimap__resetVehicleIfObserved(self._Minimap__observedVehicleId)
            playerMarker = mode
            if vehicleId is not None and vehicleId != BigWorld.player().playerVehicleID:
                self._Minimap__observedVehicleId = vehicleId
                self._Minimap__callEntryFlash(vehicleId, 'setPostmortem', [
                    True])
                mp = BigWorld.player().getOwnVehicleMatrix()
                if self._Minimap__entries.has_key(vehicleId):
                    entry = self._Minimap__entries[vehicleId]
                    if entry.has_key('handle'):
                        mp1 = BigWorld.entities[vehicleId].matrix
                        self._Minimap__ownUI.entrySetMatrix(entry['handle'], mp1)
                    
                
            else:
                playerMarker += 'Camera'
                mp = Math.WGCombinedMP()
                mp.translationSrc = BigWorld.player().getOwnVehicleMatrix()
                mp.rotationSrc = BigWorld.camera().invViewMatrix
            if self._Minimap__ownEntry.has_key('handle'):
                self._Minimap__ownUI.entrySetMatrix(self._Minimap__ownEntry['handle'], mp)
            
        
        self._Minimap__callEntryFlash(BigWorld.player().playerVehicleID, 'init', [
            'player',
            playerMarker])
        self._Minimap__parentUI.call('minimap.entryInited', [])

    
    def _Minimap__clearCamera(self, vehicleId):
        if self._Minimap__cameraHandle is not None:
            self._Minimap__ownUI.delEntry(self._Minimap__cameraHandle)
            self._Minimap__cameraHandle = None
        

    
    def handleRepeatKeyEvent(self, event):
        if GUI_SETTINGS.minimapSize:
            convertKeyEvent = convertKeyEvent
            import game
            cmdMap = CommandMapping.g_instance
            (isDown, key, mods, isRepeat) = convertKeyEvent(event)
            if isRepeat and isDown and cmdMap.isFiredList((CommandMapping.CMD_MINIMAP_SIZE_DOWN, CommandMapping.CMD_MINIMAP_SIZE_UP), key):
                self.handleKey(key)
            
        

    
    def handleKey(self, key):
        if GUI_SETTINGS.minimapSize:
            cmdMap = CommandMapping.g_instance
            if cmdMap.isFired(CommandMapping.CMD_MINIMAP_SIZE_DOWN, key):
                self._Minimap__parentUI.call('minimap.sizeDown', [])
            elif cmdMap.isFired(CommandMapping.CMD_MINIMAP_SIZE_UP, key):
                self._Minimap__parentUI.call('minimap.sizeUp', [])
            elif cmdMap.isFired(CommandMapping.CMD_MINIMAP_VISIBLE, key):
                self._Minimap__parentUI.call('minimap.visible', [])
            
        

    
    def showActionMarker(self, vehicleID, newState):
        self._Minimap__callEntryFlash(vehicleID, 'showAction', [
            newState])



class MinimapZIndexManager(object):
    _DEAD_VEHICLE_RANGE = (50, 99)
    _VEHICLE_RANGE = (101, 150)
    _FIXED_INDEXES = {
        'cameraNormal': 100,
        'self': 151,
        'cameraStrategic': 152,
        'cell': 153 }
    
    def __init__(self):
        self._MinimapZIndexManager__indexes = { }
        self._MinimapZIndexManager__indexesDead = { }
        self._MinimapZIndexManager__lastPointIndex = 0
        self._MinimapZIndexManager__lastVehIndex = MinimapZIndexManager._VEHICLE_RANGE[0]
        self._MinimapZIndexManager__lastDeadVehIndex = MinimapZIndexManager._DEAD_VEHICLE_RANGE[0]

    
    def getTeamPointIndex(self):
        self._MinimapZIndexManager__lastPointIndex += 1
        return self._MinimapZIndexManager__lastPointIndex

    
    def getVehicleIndex(self, id):
        if not self._MinimapZIndexManager__indexes.has_key(id):
            self._MinimapZIndexManager__indexes[id] = self._MinimapZIndexManager__lastVehIndex
            self._MinimapZIndexManager__lastVehIndex += 1
        
        return self._MinimapZIndexManager__indexes[id]

    
    def getDeadVehicleIndex(self, id):
        if not self._MinimapZIndexManager__indexesDead.has_key(id):
            self._MinimapZIndexManager__indexesDead[id] = self._MinimapZIndexManager__lastDeadVehIndex
            self._MinimapZIndexManager__lastDeadVehIndex += 1
        
        return self._MinimapZIndexManager__indexesDead[id]

    
    def getIndexByName(self, name):
        return MinimapZIndexManager._FIXED_INDEXES[name]



