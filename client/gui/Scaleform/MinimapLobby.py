# Source Generated with Decompyle++
# File: MinimapLobby.pyc (Python 2.6)

import Math
import BigWorld
import ArenaType

class MinimapLobby(object):
    CREATE_SCOPE = 'createRoom'
    IN_ROOM_SCOPE = 'inRoom'
    MINIMAP_SIZE = 300
    
    def __init__(self, parentUI, scope):
        self._MinimapLobby__parentUI = parentUI
        self._MinimapLobby__playerTeam = 1
        self._MinimapLobby__arenaTypeID = None
        self._MinimapLobby__cfg = dict()
        self._MinimapLobby__scope = scope

    
    def start(self):
        self._MinimapLobby__parentUI.addExternalCallbacks({
            'minimap.{0:>s}.onChange'.format(self._MinimapLobby__scope): self.onChange })

    
    def destroy(self):
        self._MinimapLobby__parentUI.removeExternalCallbacks('minimap.{0:>s}.onChange'.format(self._MinimapLobby__scope))
        self._MinimapLobby__parentUI = None

    
    def onChange(self, callbackID, arenaTypeID):
        self.setArena(arenaTypeID)

    
    def swapTeams(self, team):
        doBuild = False
        if not team:
            team = 1
        
        if team is not self._MinimapLobby__playerTeam:
            self._MinimapLobby__playerTeam = team
            doBuild = True
        
        if doBuild and self._MinimapLobby__arenaTypeID is not None:
            self.build()
        

    
    def setArena(self, arenaTypeID):
        self._MinimapLobby__arenaTypeID = int(arenaTypeID)
        arenaType = ArenaType.g_cache[self._MinimapLobby__arenaTypeID]
        self._MinimapLobby__cfg['texture'] = '../../gui/maps/icons/map/%s.png' % arenaType.geometryName
        self._MinimapLobby__cfg['size'] = arenaType.boundingBox
        self._MinimapLobby__cfg['teamBasePositions'] = arenaType.teamBasePositions
        self._MinimapLobby__cfg['teamSpawnPoints'] = arenaType.teamSpawnPoints
        self._MinimapLobby__cfg['controlPoint'] = arenaType.controlPoint
        self.build()

    
    def build(self):
        self._MinimapLobby__parentUI.call('minimap.{0:>s}.clear'.format(self._MinimapLobby__scope), [])
        (bottomLeft, upperRight) = self._MinimapLobby__cfg['size']
        self._MinimapLobby__parentUI.call('minimap.{0:>s}.changeMap'.format(self._MinimapLobby__scope), [
            self._MinimapLobby__cfg['texture']])
        (mapWidth, mapHeight) = (upperRight - bottomLeft) / self.MINIMAP_SIZE
        viewpoint = (upperRight + bottomLeft) * 0.5
        viewpointTranslate = Math.Matrix()
        viewpointTranslate.setTranslate((viewpoint.x, 0, viewpoint.y))
        ADD_POINT_EVENT = 'minimap.{0:>s}.addPoint'.format(self._MinimapLobby__scope)
        for (team, teamSpawnPoints) in enumerate(self._MinimapLobby__cfg['teamSpawnPoints'], 1):
            for (spawn, spawnPoint) in enumerate(teamSpawnPoints, 1):
                pos = (spawnPoint[0], 0, spawnPoint[1])
                m = Math.Matrix(viewpointTranslate).applyPoint(pos)
                if team == self._MinimapLobby__playerTeam:
                    pass
                1
                if len(teamSpawnPoints) > 1:
                    pass
                1
                m[0] / mapWidth - viewpoint.x * 0.5(m[2] / mapHeight - viewpoint.y * 0.5, [
                    'spawn',
                    'blue',
                    'red',
                    spawn + 1,
                    1])
            
        
        for (team, teamBasePoints) in enumerate(self._MinimapLobby__cfg['teamBasePositions'], 1):
            for (baseNumber, basePoint) in enumerate(teamBasePoints.values(), 2):
                pos = (basePoint[0], 0, basePoint[1])
                m = Math.Matrix(viewpointTranslate).applyPoint(pos)
                if team == self._MinimapLobby__playerTeam:
                    pass
                1
                if len(teamBasePoints) > 1:
                    pass
                1
                m[0] / mapWidth - viewpoint.x * 0.5(m[2] / mapHeight - viewpoint.y * 0.5, [
                    'base',
                    'blue',
                    'red',
                    baseNumber,
                    1])
            
        
        if self._MinimapLobby__cfg['controlPoint']:
            pos = (self._MinimapLobby__cfg['controlPoint'][0], 0, self._MinimapLobby__cfg['controlPoint'][1])
            m = Math.Matrix(viewpointTranslate).applyPoint(pos)
            self._MinimapLobby__parentUI.call(ADD_POINT_EVENT, [
                m[0] / mapWidth - viewpoint.x * 0.5,
                m[2] / mapHeight - viewpoint.y * 0.5,
                'control',
                'empty',
                1])
        

    
    def updatePoints(self):
        self._MinimapLobby__parentUI.call('minimap.updatePoints', [])



