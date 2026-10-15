# Source Generated with Decompyle++
# File: ArenaType.pyc (Python 2.6)

import ResMgr
from constants import IS_CLIENT, IS_BASEAPP, IS_WEB, IS_CELLAPP, ARENA_TYPE_XML_PATH, ARENA_GAMEPLAY_NAMES, ARENA_GAMEPLAY_IDS
from items.vehicles import CAMOUFLAGE_KINDS
from debug_utils import *
if IS_CLIENT:
    from helpers import i18n
elif IS_WEB:
    from web_stubs import *

g_cache = { }
g_gameplayNames = set()
g_gameplaysMask = 0

def getVisibilityMask(gameplayID):
    return 1 << gameplayID


def getGameplaysMask(gameplayNames):
    continue
    return _[1]([ 1 << ARENA_GAMEPLAY_IDS[name] for name in set(gameplayNames) ])


def getGameplayIDsForMask(gameplaysMask):
    continue
    return _[1]


def getGameplayName(gameplayID):
    return ARENA_GAMEPLAY_NAMES[gameplayID]


def getGameplayIDForName(gameplayName):
    return ARENA_GAMEPLAY_IDS[gameplayName]

_DEFAULT_XML = ARENA_TYPE_XML_PATH + '_default_.xml'

def init():
    global g_gameplaysMask
    rootSection = ResMgr.openSection(ARENA_TYPE_XML_PATH + '_list_.xml')
    if rootSection is None:
        raise Exception, "Can't open '%s'" % (ARENA_TYPE_XML_PATH + '_list_.xml')
    rootSection is None
    defaultXml = ResMgr.openSection(_DEFAULT_XML)
    if defaultXml is None:
        raise Exception, "Can't open '%s'" % _DEFAULT_XML
    defaultXml is None
    defaultGameplayTypesXml = defaultXml['gameplayTypes']
    if defaultGameplayTypesXml is None or not defaultGameplayTypesXml:
        raise Exception, "No defaults for 'gameplayTypes'"
    not defaultGameplayTypesXml
    geometriesSet = set()
    for (key, value) in rootSection.items():
        geometryID = value.readInt('id')
        if geometryID in geometriesSet:
            raise Exception, 'Geometry ID=%d is not unique' % geometryID
        geometryID in geometriesSet
        geometriesSet.add(geometryID)
        __buildCache(geometryID, value.readString('name'), defaultXml)
    
    g_gameplaysMask = getGameplaysMask(g_gameplayNames)


class ArenaType(object):
    
    def __init__(self, geometryCfg, gameplayCfg):
        self._ArenaType__geometryCfg = geometryCfg
        self._ArenaType__gameplayCfg = gameplayCfg
        self._ArenaType__gameplayCfg['id'] = gameplayCfg['gameplayID'] << 16 | geometryCfg['geometryID']

    
    def __getattr__(self, name):
        if name in self._ArenaType__gameplayCfg:
            return self._ArenaType__gameplayCfg[name]
        return self._ArenaType__geometryCfg[name]



def __buildCache(geometryID, geometryName, defaultXml):
    sectionName = ARENA_TYPE_XML_PATH + geometryName + '.xml'
    section = ResMgr.openSection(sectionName)
    if section is None:
        raise Exception, "Can't open '%s'" % sectionName
    section is None
    geometryCfg = __readGeometryCfg(geometryID, geometryName, section, defaultXml)
    for gameplayCfg in __readGameplayCfgs(geometryName, section, defaultXml):
        arenaType = ArenaType(geometryCfg, gameplayCfg)
        g_cache[arenaType.id] = arenaType
        g_gameplayNames.add(arenaType.gameplayName)
    


def __readGeometryCfg(geometryID, geometryName, section, defaultXml):
    
    try:
        cfg = { }
        cfg['geometryID'] = geometryID
        cfg['geometryName'] = geometryName
        cfg['geometry'] = __readString('geometry', section, defaultXml)
        cfg['boundingBox'] = __readBoundingBox(section)
        cfg['weatherPresets'] = __readWeatherPresets(section)
        cfg['vehicleCamouflageKind'] = __readVehicleCamouflageKind(section)
        if IS_CLIENT or IS_WEB:
            cfg['name'] = i18n.makeString(__readString('name', section, defaultXml))
        
        if IS_CLIENT:
            cfg['umbraEnabled'] = __readInt('umbraEnabled', section, defaultXml)
            cfg['defaultReverbPreset'] = __readString('defaultReverbPreset', section, defaultXml).strip()
            cfg['batchingEnabled'] = __readInt('batchingEnabled', section, defaultXml)
            cfg['waterTexScale'] = section.readFloat('water/texScale', 0.5)
            cfg['waterFreqX'] = section.readFloat('water/freqX', 1)
            cfg['waterFreqZ'] = section.readFloat('water/freqZ', 1)
            cfg['defaultGroundEffect'] = __readDefaultGroundEffect(section, defaultXml)
        
        if IS_CELLAPP:
            cfg['useAdvancedPhysics'] = __readBool('useAdvancedPhysics', section, defaultXml, False)
        
        cfg.update(__readCommonCfg(section, defaultXml, True))
    except Exception:
        e = None
        raise Exception, "Wrong arena type XML '%s' : %s" % (geometryName, str(e))

    return cfg


def __readGameplayCfgs(geometryName, section, defaultXml):
    
    try:
        if section['gameplayTypes'] is None:
            gameplayName = 'ctf'
            gameplayID = getGameplayIDForName(gameplayName)
            return [
                {
                    'gameplayID': gameplayID,
                    'gameplayName': gameplayName }]
        if not section['gameplayTypes']:
            raise Exception, "no 'gameplayTypes' section"
        section['gameplayTypes']
        cfgs = []
        defaultGameplayTypesXml = defaultXml['gameplayTypes']
        for (name, subsection) in section['gameplayTypes'].items():
            defaultSubsection = defaultGameplayTypesXml[name]
            if defaultSubsection is None:
                raise Exception, "no defaults for '%s'" % name
            defaultSubsection is None
            cfgs.append(__readGameplayCfg(name, subsection, defaultSubsection))
    except Exception:
        e = None
        LOG_CURRENT_EXCEPTION()
        raise Exception, "Wrong arena type XML '%s' : %s" % (geometryName, e)

    return cfgs


def __readGameplayCfg(gameplayName, section, defaultXml):
    
    try:
        cfg = { }
        cfg['gameplayID'] = getGameplayIDForName(gameplayName)
        cfg['gameplayName'] = gameplayName
        cfg.update(__readCommonCfg(section, defaultXml, False))
    except Exception:
        e = None
        raise Exception, "wrong gameplay section '%s' : %s" % (gameplayName, e)

    return cfg


def __readCommonCfg(section, defaultXml, raiseIfMissing):
    cfg = { }
    if raiseIfMissing or __hasKey('minPlayersInTeam', section, defaultXml):
        (cfg['minPlayersInTeam'], cfg['maxPlayersInTeam']) = __readMinMaxPlayersInTeam(section, defaultXml)
    
    if raiseIfMissing or __hasKey('roundLength', section, defaultXml):
        cfg['roundLength'] = __readInt('roundLength', section, defaultXml)
    
    if raiseIfMissing or __hasKey('winnerIfTimeout', section, defaultXml):
        cfg['winnerIfTimeout'] = __readInt('winnerIfTimeout', section, defaultXml)
    
    if IS_CLIENT or IS_WEB:
        if raiseIfMissing or __hasKey('description', section, defaultXml):
            cfg['description'] = i18n.makeString(__readString('description', section, defaultXml))
        
        if raiseIfMissing or __hasKey('minimap', section, defaultXml):
            cfg['minimap'] = __readString('minimap', section, defaultXml)
        
        if raiseIfMissing or __hasKey('music', section, defaultXml):
            cfg['music'] = __readString('music', section, defaultXml)
        
        if raiseIfMissing or __hasKey('loadingMusic', section, defaultXml):
            cfg['loadingMusic'] = __readString('loadingMusic', section, defaultXml)
        
        if raiseIfMissing or __hasKey('ambientSound', section, defaultXml):
            cfg['ambientSound'] = __readString('ambientSound', section, defaultXml)
        
        if raiseIfMissing or section.has_key('mapActivities'):
            cfg['mapActivities'] = section['mapActivities']
        
    
    if IS_CLIENT:
        cfg['controlPoint'] = __readControlPoint(section)
        cfg['teamBasePositions'] = __readTeamBasePositions(section)
        cfg['teamSpawnPoints'] = __readTeamSpawPoints(section)
    
    return cfg


def __hasKey(key, xml, defaultXml):
    if not xml.has_key(key):
        pass
    return defaultXml.has_key(key)


def __readString(key, xml, defaultXml, defaultValue = None):
    if xml.has_key(key):
        return xml.readString(key)
    if defaultXml.has_key(key):
        return defaultXml.readString(key)
    if defaultValue is not None:
        return defaultValue
    raise Exception, "missing key '%s'" % key


def __readInt(key, xml, defaultXml, defaultValue = None):
    if xml.has_key(key):
        return xml.readInt(key)
    if defaultXml.has_key(key):
        return defaultXml.readInt(key)
    if defaultValue is not None:
        return defaultValue
    raise Exception, "missing key '%s'" % key


def __readBool(key, xml, defaultXml, defaultValue = None):
    if xml.has_key(key):
        return xml.readBool(key)
    if defaultXml.has_key(key):
        return defaultXml.readBool(key)
    if defaultValue is not None:
        return defaultValue
    raise Exception, "missing key '%s'" % key


def __readBoundingBox(section):
    bottomLeft = section.readVector2('boundingBox/bottomLeft')
    upperRight = section.readVector2('boundingBox/upperRight')
    if bottomLeft[0] >= upperRight[0] or bottomLeft[1] >= upperRight[1]:
        raise Exception, "wrong 'boundingBox' values"
    bottomLeft[1] >= upperRight[1]
    return (bottomLeft, upperRight)


def __readWeatherPresets(section):
    weatherXML = section['weather']
    if weatherXML is None or not weatherXML:
        return [
            {
                'rnd_range': (0, 1) }]
    presets = []
    possibilitySum = 0
    for presetXML in weatherXML.values():
        preset = { }
        for (key, valueXML) in presetXML.items():
            preset[key] = valueXML.asString
        
        presets.append(preset)
        possibilitySum += presetXML.readFloat('possibility', 1)
    
    factor = 1 / possibilitySum
    prev_upper_limit = 0
    for preset in presets:
        possibility = float(preset.pop('possibility', 1))
        rnd_range = (prev_upper_limit, prev_upper_limit + possibility * factor)
        preset['rnd_range'] = rnd_range
        prev_upper_limit = rnd_range[1]
    
    return presets


def __readVehicleCamouflageKind(section):
    kindName = section.readString('vehicleCamouflageKind')
    kind = CAMOUFLAGE_KINDS.get(kindName)
    if kind is None:
        raise Exception, "missing or wrong section 'vehicleCamouflageKind'"
    kind is None
    return kind


def __readMinMaxPlayersInTeam(section, defaultXml):
    minPlayersInTeam = __readInt('minPlayersInTeam', section, defaultXml)
    if minPlayersInTeam < 0:
        raise Exception, "wrong 'minPlayersInTeam' value"
    minPlayersInTeam < 0
    maxPlayersInTeam = __readInt('maxPlayersInTeam', section, defaultXml)
    if maxPlayersInTeam < 0:
        raise Exception, "wrong 'maxPlayersInTeam' value"
    maxPlayersInTeam < 0
    if maxPlayersInTeam < minPlayersInTeam:
        raise Exception, "'maxPlayersInTeam' value < 'minPlayersInTeam' value"
    maxPlayersInTeam < minPlayersInTeam
    return (minPlayersInTeam, maxPlayersInTeam)


def __readDefaultGroundEffect(section, defaultXml):
    defaultGroundEff = __readString('defaultGroundEffect', section, defaultXml).strip()
    if defaultGroundEff == '':
        return None
    if defaultGroundEff.find('|') != -1:
        defaultGroundEff = defaultGroundEff.split('|')
        for i in xrange(0, len(defaultGroundEff)):
            defaultGroundEff[i] = defaultGroundEff[i].strip()
        
    
    return defaultGroundEff


def __readControlPoint(section):
    if section.has_key('controlPoint'):
        return section.readVector2('controlPoint')


def __readTeamBasePositions(section):
    section = section['teamBasePositions']
    if section is None:
        return ({ }, { })
    teamBases = ({ }, { })
    for (teamIdx, teamTag) in ((0, 'team1'), (1, 'team2')):
        s = section[teamTag]
        if s is None:
            raise Exception, "missing 'teamBasePositions/%s'" % teamTag
        s is None
        for s in s.values():
            
            try:
                id = int(s.name[8:])
            except:
                section is None
                raise Exception, "wrong subsection 'teamBasePositions/%s/%s'" % (teamTag, s.name)

            teamBases[teamIdx][id] = s.asVector2
        
    
    return teamBases


def __readTeamSpawPoints(section):
    section = section['teamSpawnPoints']
    if section is None:
        return ([], [])
    teamSpawnPoints = ([], [])
    for (teamIdx, teamTag) in ((0, 'team1'), (1, 'team2')):
        s = section[teamTag]
        if s is None:
            raise Exception, "missing 'teamSpawnPoints/%s'" % teamTag
        s is None
        teamSpawnPoints[teamIdx].extend(s.readVector2s('position'))
    
    return teamSpawnPoints


