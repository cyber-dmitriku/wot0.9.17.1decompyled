# Source Generated with Decompyle++
# File: dossiers_utils.pyc (Python 2.6)

import BigWorld
import pickle
from helpers.i18n import makeString
import dossiers
import nations
from gui.Scaleform.utils.requesters import DossierRequester, StatsRequester
from gui.Scaleform.utils.RareAchievementsCache import g_rareAchievesCache
from constants import DOSSIER_TYPE, CLAN_MEMBER_FLAGS
from items.vehicles import getVehicleType, parseIntCompactDescr, VehicleDescr
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG
from PlayerEvents import g_playerEvents
from adisp import process, async
from dossiers.achievements import ACHIEVEMENTS, ACHIEVEMENT_SECTIONS_ORDER
from dossiers.dependences import getTankExpertRequirements, getMechanicEngineerRequirements
TOTAL_BLOCKS = (('common', ('battlesCount', 'wins', 'losses', 'survivedBattles')), ('battleeffect', ('frags', 'maxFrags', 'effectiveShots', 'damageDealt')), ('credits', ('xp', 'avgExperience', 'maxXP')))
VEHICLE_BLOCKS = (('common', ('battlesCount', 'wins', 'losses', 'survivedBattles')), ('battleeffect', ('frags', 'maxFrags', 'effectiveShots', 'damageDealt')), ('credits', ('xp', 'avgExperience', 'maxXP')))
CLIENT_ACHIEVEMENTS = {
    'whiteTiger': {
        'type': 'repeatable',
        'section': 'action' } }
CLIENT_ACCOUNT_MEDALS_LAYOUT = ('whiteTiger',)
CLIENT_VEHICLE_MEDALS_LAYOUT = tuple()
CLIENT_TANKMEN_MEDALS_LAYOUT = tuple()
TANK_EXPERT_GROUP = [
    'tankExpert']
MECH_ENGINEER_GROUP = [
    'mechanicEngineer']
for (name, id) in nations.INDICES.iteritems():
    TANK_EXPERT_GROUP.append('tankExpert%d' % id)
    MECH_ENGINEER_GROUP.append('mechanicEngineer%d' % id)


def __defineMedalsBlocks():
    global ACCOUNT_MEDALS_LAYOUT, TANKMEN_MEDALS_LAYOUT, VEHICLE_MEDALS_LAYOUT, ACCOUNT_MEDALS_LAYOUT, TANKMEN_MEDALS_LAYOUT, VEHICLE_MEDALS_LAYOUT
    ACCOUNT_MEDALS_LAYOUT = []
    TANKMEN_MEDALS_LAYOUT = []
    VEHICLE_MEDALS_LAYOUT = []
    for section in ACHIEVEMENT_SECTIONS_ORDER:
        continue
        block = _[1]
        for (name, params) in CLIENT_ACHIEVEMENTS.iteritems():
            if params['section'] == section and isAccountMedal(name):
                block.append(name)
                continue
            []
        
        block.sort()
        ACCOUNT_MEDALS_LAYOUT.append(tuple(block))
        continue
        block = _[2]
        for (name, params) in CLIENT_ACHIEVEMENTS.iteritems():
            if params['section'] == section and isVehicleMedal(name):
                block.append(name)
                continue
            []
        
        block.sort()
        VEHICLE_MEDALS_LAYOUT.append(tuple(block))
        continue
        block = _[3]
        for (name, params) in CLIENT_ACHIEVEMENTS.iteritems():
            if params['section'] == section and isTankmanMedal(name):
                block.append(name)
                continue
            []
        
        block.sort()
        TANKMEN_MEDALS_LAYOUT.append(tuple(block))
    
    ACCOUNT_MEDALS_LAYOUT = tuple(ACCOUNT_MEDALS_LAYOUT)
    TANKMEN_MEDALS_LAYOUT = tuple(TANKMEN_MEDALS_LAYOUT)
    VEHICLE_MEDALS_LAYOUT = tuple(VEHICLE_MEDALS_LAYOUT)


def getAccountMedalsLayout():
    
    try:
        pass
    except:
        __defineMedalsBlocks()

    return ACCOUNT_MEDALS_LAYOUT


def getTankmenMedalsLayout():
    
    try:
        pass
    except:
        __defineMedalsBlocks()

    return TANKMEN_MEDALS_LAYOUT


def getVehicleMedalsLayout():
    
    try:
        pass
    except:
        __defineMedalsBlocks()

    return VEHICLE_MEDALS_LAYOUT


def getMedalsLayout(dossierType):
    if dossierType == DOSSIER_TYPE.ACCOUNT:
        return getAccountMedalsLayout()
    if dossierType == DOSSIER_TYPE.TANKMAN:
        return getTankmenMedalsLayout()
    if dossierType == DOSSIER_TYPE.VEHICLE:
        return getVehicleMedalsLayout()
    return list()

MEDALS_UNIC_FOR_RANK = ('medalKay', 'medalCarius', 'medalKnispel', 'medalPoppel', 'medalAbrams', 'medalLeClerc', 'medalLavrinenko', 'medalEkins', 'markOfMastery')
MEDALS_TITLES = [
    'lumberjack']
MEDALS_TITLES.extend(TANK_EXPERT_GROUP)
MEDALS_TITLES.extend(MECH_ENGINEER_GROUP)
MEDALS_SERIES = {
    'titleSniper': {
        'cur': 'sniperSeries',
        'max': 'maxSniperSeries',
        'format': ('maxSniperSeries',) },
    'invincible': {
        'cur': 'invincibleSeries',
        'max': 'maxInvincibleSeries',
        'format': ('maxInvincibleSeries',) },
    'diehard': {
        'cur': 'diehardSeries',
        'max': 'maxDiehardSeries',
        'format': ('maxDiehardSeries',) },
    'handOfDeath': {
        'cur': 'killingSeries',
        'max': 'maxKillingSeries',
        'format': ('maxKillingSeries',) },
    'armorPiercer': {
        'cur': 'piercingSeries',
        'max': 'maxPiercingSeries',
        'format': ('maxPiercingSeries',) } }
CLAN_MEMBERS = {
    CLAN_MEMBER_FLAGS.LEADER: 'leader',
    CLAN_MEMBER_FLAGS.VICE_LEADER: 'vice_leader',
    CLAN_MEMBER_FLAGS.RECRUITER: 'recruiter',
    CLAN_MEMBER_FLAGS.TREASURER: 'treasurer',
    CLAN_MEMBER_FLAGS.DIPLOMAT: 'diplomat',
    CLAN_MEMBER_FLAGS.COMMANDER: 'commander',
    CLAN_MEMBER_FLAGS.PRIVATE: 'private',
    CLAN_MEMBER_FLAGS.RECRUIT: 'recruit' }
_ICONS_MASK = '../maps/icons/vehicle/small/%s.png'

def getAchievementSection(name):
    achievInfo = ACHIEVEMENTS.get(name)
    if achievInfo is not None:
        return achievInfo.get('section')
    achievInfo = CLIENT_ACHIEVEMENTS.get(name)
    if achievInfo is not None:
        return achievInfo.get('section')


def getAchievementType(name):
    achievInfo = ACHIEVEMENTS.get(name)
    if achievInfo is not None:
        return achievInfo.get('type')
    achievInfo = CLIENT_ACHIEVEMENTS.get(name)
    if achievInfo is not None:
        return achievInfo.get('section')

g_dossiersCache = { }

def getUserDossier(userName):
    if not g_dossiersCache.has_key(userName):
        g_dossiersCache[userName] = DossierRequester(userName)
    
    return g_dossiersCache[userName]


def closeUserDossier(userName):
    if g_dossiersCache.has_key(userName):
        if not g_dossiersCache[userName].isValid:
            return None
        del g_dossiersCache[userName]
    else:
        LOG_DEBUG('Attempt to clear empty user dossier: %s' % str(userName))


def __onCenterIsLongDisconnected(isLongDisconnected):
    global g_dossiersCache
    if isLongDisconnected:
        return None
    g_dossiersCache = dict(filter((lambda item: item[1].isAvailable), g_dossiersCache.iteritems()))

g_playerEvents.onCenterIsLongDisconnected += __onCenterIsLongDisconnected

def isAccountMedal(medalname):
    if not medalname in dossiers._ACCOUNT_RECORDS_LAYOUT[0] and medalname in CLIENT_ACCOUNT_MEDALS_LAYOUT:
        pass
    return medalname == 'rareAchievements'


def isVehicleMedal(medalname):
    if not medalname in dossiers._VEHICLE_RECORDS_LAYOUT[0]:
        pass
    return medalname in CLIENT_VEHICLE_MEDALS_LAYOUT


def isTankmanMedal(medalname):
    if not medalname in dossiers._TANKMAN_RECORDS_LAYOUT[0]:
        pass
    return medalname in CLIENT_TANKMEN_MEDALS_LAYOUT


def getCommonInfo(userName, dossier, clanInfo, clanEmblemFile):
    import cgi as cgi
    lastBattleTimeUserString = makeString('#menu:account/profile/emptyBattleList')
    if dossier['lastBattleTime']:
        lastBattleTimeUserString = '%s %s' % (BigWorld.wg_getLongDateFormat(dossier['lastBattleTime']), BigWorld.wg_getLongTimeFormat(dossier['lastBattleTime']))
    
    value = [
        clanInfo is not None,
        userName,
        '%s %s' % (BigWorld.wg_getLongDateFormat(dossier['creationTime']), BigWorld.wg_getLongTimeFormat(dossier['creationTime'])),
        lastBattleTimeUserString]
    
    def getGoldFmt(str):
        return "<font color='#FBCD5E'>" + str + '</font>'

    if clanInfo is not None:
        value.append("[<font color='#ffffff'>%s</font>] %s" % (cgi.escape(clanInfo[1]), cgi.escape(clanInfo[0])))
        value.append(makeString('#menu:profile/header/clan/joinDate') % getGoldFmt(BigWorld.wg_getLongDateFormat(clanInfo[4])))
        if clanInfo[3] in CLAN_MEMBERS:
            pass
        1
        clanPosition = '#menu:profile/header/clan/position/%s' % CLAN_MEMBERS[clanInfo[3]]('')
        if clanInfo[3] in CLAN_MEMBERS:
            pass
        1
        makeString('#menu:profile/header/clan/position') % getGoldFmt(clanPosition)('')
        clanEmblemId = None
        if clanEmblemFile:
            clanEmblemId = 'userInfoId' + userName
            BigWorld.wg_addTempScaleformTexture(clanEmblemId, clanEmblemFile)
        
        value.append(clanEmblemId)
    else:
        value.extend([
            '',
            '',
            '',
            None])
    return value


def getClanEmblemTextureID(clanDBID, isBig, textureID, callback):
    import imghdr as imghdr
    if clanDBID is not None and clanDBID != 0:
        if not isBig:
            pass
        1
        yield clanDBID('clan_emblems_small', 'clan_emblems_big')
        (clanEmblemUrl, clanEmblemFile) = StatsRequester().getFileFromServer
        if clanEmblemFile and imghdr.what(None, clanEmblemFile) is not None:
            BigWorld.wg_addTempScaleformTexture(textureID, clanEmblemFile)
            callback(True)
            return None
    
    callback(False)

getClanEmblemTextureID = async(process(getClanEmblemTextureID))

def getDossierVehicleList(dossier, isOnlyTotal = False):
    battlesCount = float(dossier['battlesCount'])
    winsCount = float(dossier['wins'])
    if battlesCount != 0:
        pass
    1
    data = [
        '#menu:profile/list/totalName',
        None,
        0,
        -1,
        __getData('battlesCount', dossier),
        '%d%%' % round(100 * winsCount / battlesCount),
        '',
        0]
    if not isOnlyTotal:
        vehList = dossier['vehDossiersCut'].items()
        vehList.sort(cmp = __dossierComparator)
        for (vehTypeCompactDesr, battles) in vehList:
            
            try:
                vehType = getVehicleType(vehTypeCompactDesr)
                data.append(vehTypeCompactDesr)
                data.append(vehType.userString)
                data.append(_ICONS_MASK % vehType.name.replace(':', '-'))
                data.append(vehType.level)
                data.append(vehType.id[0])
                data.append(battles[0])
                if battles[0] != 0:
                    pass
                1
                '%d%%' % round(100 * float(battles[1]) / battles[0])('')
                data.append(battles[2])
            continue
            except Exception:
                'ALL'
                LOG_ERROR('Get vehicle info error vehTypeCompactDesr: %s' % str(vehTypeCompactDesr))
                LOG_CURRENT_EXCEPTION()
                continue
            

        
    
    return data


def checkTankExpertActivity(type, dossier):
    res = getTankExpertRequirements(dossiers.g_cache, dossier['vehTypeFrags'])
    if not len(res.get(type, list())):
        return (True, None)
    vehiclesNames = list()
    for vehTypeCompDescr in res.get(type, list()):
        
        try:
            (_, nation_id, innation_id) = parseIntCompactDescr(vehTypeCompDescr)
            vehiclesNames.append(VehicleDescr(typeID = (nation_id, innation_id)).type.userString)
        continue
        except Exception:
            len(res.get(type, list()))
            continue
            continue
        

    
    return (False, vehiclesNames)


def checkTechEngineerActivity(type, dossier, nationID, unlocks = None):
    achieveName = 'mechanicEngineer'
    if nationID > -1:
        achieveName = '%s%d' % (achieveName, nationID)
    
    if unlocks is None:
        unlocks = dossiers.g_cache['vehiclesInTrees']
    
    res = getMechanicEngineerRequirements(dossiers.g_cache, set(), unlocks, nationID)
    if not len(res.get(achieveName, list())):
        return (True, None)
    vehiclesNames = list()
    for vehTypeCompDescr in res.get(achieveName, list()):
        
        try:
            (_, nation_id, innation_id) = parseIntCompactDescr(vehTypeCompDescr)
            vehiclesNames.append(VehicleDescr(typeID = (nation_id, innation_id)).type.userString)
        continue
        except Exception:
            len(res.get(achieveName, list()))
            continue
            continue
        

    
    return (False, vehiclesNames)

ACTIVITY_HANDLERS = {
    'tankExpert': (lambda t, d, u: checkTankExpertActivity(t, d)),
    'tankExpert0': (lambda t, d, u: checkTankExpertActivity(t, d)),
    'tankExpert1': (lambda t, d, u: checkTankExpertActivity(t, d)),
    'tankExpert2': (lambda t, d, u: checkTankExpertActivity(t, d)),
    'tankExpert3': (lambda t, d, u: checkTankExpertActivity(t, d)),
    'tankExpert4': (lambda t, d, u: checkTankExpertActivity(t, d)),
    'tankExpert5': (lambda t, d, u: checkTankExpertActivity(t, d)),
    'tankExpert6': (lambda t, d, u: checkTankExpertActivity(t, d)),
    'tankExpert7': (lambda t, d, u: checkTankExpertActivity(t, d)),
    'tankExpert8': (lambda t, d, u: checkTankExpertActivity(t, d)),
    'tankExpert9': (lambda t, d, u: checkTankExpertActivity(t, d)),
    'tankExpert10': (lambda t, d, u: checkTankExpertActivity(t, d)),
    'tankExpert11': (lambda t, d, u: checkTankExpertActivity(t, d)),
    'tankExpert12': (lambda t, d, u: checkTankExpertActivity(t, d)),
    'tankExpert13': (lambda t, d, u: checkTankExpertActivity(t, d)),
    'tankExpert14': (lambda t, d, u: checkTankExpertActivity(t, d)),
    'mechanicEngineer': (lambda t, d, u: checkTechEngineerActivity(t, d, -1, u)),
    'mechanicEngineer0': (lambda t, d, u: checkTechEngineerActivity(t, d, 0, u)),
    'mechanicEngineer1': (lambda t, d, u: checkTechEngineerActivity(t, d, 1, u)),
    'mechanicEngineer2': (lambda t, d, u: checkTechEngineerActivity(t, d, 2, u)),
    'mechanicEngineer3': (lambda t, d, u: checkTechEngineerActivity(t, d, 3, u)),
    'mechanicEngineer4': (lambda t, d, u: checkTechEngineerActivity(t, d, 4, u)),
    'mechanicEngineer5': (lambda t, d, u: checkTechEngineerActivity(t, d, 5, u)),
    'mechanicEngineer6': (lambda t, d, u: checkTechEngineerActivity(t, d, 6, u)),
    'mechanicEngineer7': (lambda t, d, u: checkTechEngineerActivity(t, d, 7, u)),
    'mechanicEngineer8': (lambda t, d, u: checkTechEngineerActivity(t, d, 8, u)),
    'mechanicEngineer9': (lambda t, d, u: checkTechEngineerActivity(t, d, 9, u)),
    'mechanicEngineer10': (lambda t, d, u: checkTechEngineerActivity(t, d, 10, u)),
    'mechanicEngineer11': (lambda t, d, u: checkTechEngineerActivity(t, d, 11, u)),
    'mechanicEngineer12': (lambda t, d, u: checkTechEngineerActivity(t, d, 12, u)),
    'mechanicEngineer13': (lambda t, d, u: checkTechEngineerActivity(t, d, 13, u)),
    'mechanicEngineer14': (lambda t, d, u: checkTechEngineerActivity(t, d, 14, u)) }

def __packMedalData(type, isActive = True, icon = '../maps/icons/achievement/noImage.png', rareIconId = None, value = 0, isUnic = False, isRare = False, isTitle = False, descr = '', vehiclesList = None):
    data = [
        type,
        not isActive,
        icon,
        value,
        isUnic,
        isRare,
        isTitle,
        descr,
        rareIconId]
    if vehiclesList is not None:
        data.append(len(vehiclesList))
        continue
        _[1]([ x for x in vehiclesList ])
    else:
        data.append(0)
    data.append(False)
    return data


def getMedalDict(achievementType, rank = None, rareAchieveId = None):
    packedList = getMedal(achievementType, rank, rareAchieveId)
    result = dict()
    result['type'] = packedList.pop(0)
    result['inactive'] = packedList.pop(0)
    result['icon'] = packedList.pop(0)
    result['rank'] = packedList.pop(0)
    result['unic'] = packedList.pop(0)
    result['rare'] = packedList.pop(0)
    result['title'] = packedList.pop(0)
    result['description'] = packedList.pop(0)
    result['rareIconId'] = packedList.pop(0)
    result['vehicles'] = list()
    vehiclesCount = packedList.pop(0)
    for i in xrange(vehiclesCount):
        result['vehicles'].append(packedList.pop(0))
    
    result['last'] = packedList.pop(0)
    return result


def checkWhiteTigerMedal(dossier):
    vehicles = vehicles
    import items
    
    try:
        whiteTigerCompDescr = 56337
        return dossier['vehTypeFrags'].get(whiteTigerCompDescr, 0)
    except Exception:
        return 0



def getRareAchievementMedalData(dossier, medalId):
    import imghdr
    import uuid as uuid
    type = str(medalId)
    iconId = None
    iconData = g_rareAchievesCache.getImageData(medalId)
    if iconData and imghdr.what(None, iconData) is not None:
        iconId = str(uuid.uuid4())
        BigWorld.wg_addTempScaleformTexture(iconId, iconData)
    
    return __packMedalData(type = type, icon = '../maps/icons/achievement/actionUnknown.png', rareIconId = iconId, isTitle = True, isRare = True, descr = g_rareAchievesCache.getDescription(medalId))


def getWhiteTigerMedalData(dossier = None, value = 0):
    type = 'whiteTiger'
    if not value:
        pass
    return __packMedalData(type = type, icon = '../maps/icons/achievement/%s.png' % type, value = checkWhiteTigerMedal(dossier), descr = getMedalDescription(type))


def getMedalDescription(medalName, rank = 0):
    return makeString('#achievements:%s_descr' % medalName)


def getMedalHeroInfo(medalName):
    infoKey = '%s_heroInfo' % medalName
    msg = makeString('#achievements:%s' % infoKey)
    if msg == infoKey:
        return ''
    return msg


def getMedalValue(medalName, dossier):
    if dossier is None:
        return 0
    if medalName == 'whiteTiger':
        return checkWhiteTigerMedal(dossier)
    if getAchievementType(medalName) == 'class':
        return dossier[medalName]
    if medalName in MEDALS_SERIES.keys():
        return dossier[MEDALS_SERIES[medalName]['max']]
    max_value = dossiers.getRecordMaxValue(medalName)
    if dossier[medalName] >= max_value:
        return makeString('#achievements:achievement/maxMedalValue') % (max_value - 1)
    return dossier[medalName]


def getDossierMedals(dossier, dossier_type = DOSSIER_TYPE.ACCOUNT, unlocks = None):
    medals = [
        dossier_type,
        pickle.dumps(dossier.makeCompDescr())]
    blocks = getMedalsLayout(dossier_type)
    for group in blocks:
        for type in group:
            if type == 'markOfMastery':
                continue
            
            if type == 'whiteTiger':
                if checkWhiteTigerMedal(dossier):
                    medals.extend(getWhiteTigerMedalData(dossier = dossier))
                
            checkWhiteTigerMedal(dossier)
            if type == 'rareAchievements':
                for a in dossier[type]:
                    medals.extend(getRareAchievementMedalData(dossier, a))
                
            if dossier[type]:
                iconFileName = type
                if type in MEDALS_UNIC_FOR_RANK:
                    iconFileName = '%s%d' % (iconFileName, dossier[type])
                
                handler = ACTIVITY_HANDLERS.get(type, (lambda : (True, None)))
                (isActive, vehiclesNames) = handler(type, dossier, unlocks)
                medals.extend(__packMedalData(type = type, isActive = isActive, icon = '../maps/icons/achievement/%s.png' % iconFileName, value = getMedalValue(type, dossier), isUnic = type in MEDALS_UNIC_FOR_RANK, isTitle = type in MEDALS_TITLES, descr = getMedalDescription(type), vehiclesList = vehiclesNames))
                continue
        
        if len(medals) > 2:
            medals[-1] = blocks[-1] != group
            continue
    
    return medals


def getMedal(achievementType, rank = None, rareAchieveId = None):
    if achievementType == 'whiteTiger':
        return getWhiteTigerMedalData()
    if achievementType == 'rareAchievements':
        return getRareAchievementMedalData(medalId = rareAchieveId)
    iconFileName = achievementType
    if achievementType in MEDALS_UNIC_FOR_RANK:
        iconFileName = '%s%d' % (iconFileName, rank)
    
    return __packMedalData(type = achievementType, icon = '../maps/icons/achievement/%s.png' % iconFileName, isUnic = achievementType in MEDALS_UNIC_FOR_RANK, isTitle = achievementType in MEDALS_TITLES, descr = getMedalDescription(achievementType), value = rank)


def getDossierTotalBlocks(dossier):
    data = [
        '#menu:profile/list/totalName',
        len(TOTAL_BLOCKS)]
    for (blockType, fields) in TOTAL_BLOCKS:
        data.append(blockType)
        data.append(len(fields))
        for fieldType in fields:
            data.append(fieldType)
            data.append(__getData(fieldType, dossier))
            data.append(__getDataExtra(blockType, fieldType, dossier, True, True))
        
    
    return data


def getDossierTotalBlocksSummary(dossier, isCompact = False):
    data = []
    for (blockType, fields) in TOTAL_BLOCKS:
        for fieldType in fields:
            data.append('#menu:profile/stats/items/' + fieldType)
            data.append(__getData(fieldType, dossier))
            data.append(__getDataExtra(blockType, fieldType, dossier, True, isCompact))
        
    
    return data


def getDossierVehicleBlocks(dossier, vehTypeId):
    vehType = getVehicleType(int(vehTypeId))
    data = [
        makeString('#menu:profile/list/descr', vehType.userString),
        len(VEHICLE_BLOCKS)]
    for (blockType, fields) in VEHICLE_BLOCKS:
        data.append(blockType)
        data.append(len(fields))
        for fieldType in fields:
            data.append(fieldType)
            data.append(__getData(fieldType, dossier))
            data.append(__getDataExtra(blockType, fieldType, dossier))
        
    
    return data


def __getData(fieldType, dossier):
    if fieldType == 'effectiveShots':
        if dossier['shots'] != 0:
            return '%d%%' % round((float(dossier['hits']) / dossier['shots']) * 100)
        return '0%'
    if fieldType == 'avgExperience':
        if dossier['battlesCount'] != 0:
            return BigWorld.wg_getIntegralFormat(round(float(dossier['xp']) / dossier['battlesCount']))
        return BigWorld.wg_getIntegralFormat(0)
    return BigWorld.wg_getIntegralFormat(dossier[fieldType])


def __getDataExtra(blockType, fieldType, dossier, isTotal = False, isCompact = False):
    extra = ''
    if blockType == 'common':
        if fieldType != 'battlesCount' and dossier['battlesCount'] != 0:
            extra = '(%d%%)' % round((float(dossier[fieldType]) / dossier['battlesCount']) * 100)
        
    
    if isTotal:
        if fieldType == 'maxFrags' and dossier['maxFrags'] != 0:
            if not isCompact:
                pass
            1
            extra = getVehicleType(dossier['maxFragsVehicle']).shortUserString
        
        if fieldType == 'maxXP' and dossier['maxXP'] != 0:
            if not isCompact:
                pass
            1
            extra = getVehicleType(dossier['maxXPVehicle']).shortUserString
        
    
    return extra


def __dossierComparator(x1, x2):
    if x1[1][0] < x2[1][0]:
        return 1
    if x1[1][0] > x2[1][0]:
        return -1
    if x1[1][1] < x2[1][1]:
        return 1
    if x1[1][1] > x2[1][1]:
        return -1
    return 0


def __getMedalKayNextLevelValue(dossier):
    medalKayCfg = dossiers.RECORD_CONFIGS['medalKay']
    battleHeroes = dossier['battleHeroes']
    maxMedalClass = len(medalKayCfg)
    curClass = dossier['medalKay']
    if curClass == 1:
        return None
    return medalKayCfg[(maxMedalClass - curClass) + 1] - battleHeroes


def __getMedalCariusNextLevelValue(dossier):
    medalCariusCfg = dossiers.RECORD_CONFIGS['medalCarius']
    frags = dossier['frags']
    maxMedalClass = len(medalCariusCfg)
    curClass = dossier['medalCarius']
    if curClass == 1:
        return None
    return medalCariusCfg[(maxMedalClass - curClass) + 1] - frags


def __getMedalKnispelNextLevelValue(dossier):
    medalKnispelCfg = dossiers.RECORD_CONFIGS['medalKnispel']
    damageDealt = dossier['damageDealt']
    damageReceived = dossier['damageReceived']
    maxMedalClass = len(medalKnispelCfg)
    curClass = dossier['medalKnispel']
    if curClass == 1:
        return None
    return medalKnispelCfg[(maxMedalClass - curClass) + 1] - damageDealt + damageReceived


def __getMedalPoppelNextLevelValue(dossier):
    medalPoppelCfg = dossiers.RECORD_CONFIGS['medalPoppel']
    spotted = dossier['spotted']
    maxMedalClass = len(medalPoppelCfg)
    curClass = dossier['medalPoppel']
    if curClass == 1:
        return None
    return medalPoppelCfg[(maxMedalClass - curClass) + 1] - spotted


def __getMedalAbramsNextLevelValue(dossier):
    medalAbramsCfg = dossiers.RECORD_CONFIGS['medalAbrams']
    winAndSurvived = dossier['winAndSurvived']
    maxMedalClass = len(medalAbramsCfg)
    curClass = dossier['medalAbrams']
    if curClass == 1:
        return None
    return medalAbramsCfg[(maxMedalClass - curClass) + 1] - winAndSurvived


def __getMedalLeClercNextLevelValue(dossier):
    medalLeClercCfg = dossiers.RECORD_CONFIGS['medalLeClerc']
    capturePoints = dossier['capturePoints']
    maxMedalClass = len(medalLeClercCfg)
    curClass = dossier['medalLeClerc']
    if curClass == 1:
        return None
    return medalLeClercCfg[(maxMedalClass - curClass) + 1] - capturePoints


def __getMedalLavrinenkoNextLevelValue(dossier):
    medalLavrinenkoCfg = dossiers.RECORD_CONFIGS['medalLavrinenko']
    droppedCapturePoints = dossier['droppedCapturePoints']
    maxMedalClass = len(medalLavrinenkoCfg)
    curClass = dossier['medalLavrinenko']
    if curClass == 1:
        return None
    return medalLavrinenkoCfg[(maxMedalClass - curClass) + 1] - droppedCapturePoints


def __getMedalEkinsNextLevelValue(dossier):
    medalEkinsCfg = dossiers.RECORD_CONFIGS['medalEkins']
    frags = dossier['frags8p']
    maxMedalClass = len(medalEkinsCfg)
    curClass = dossier['medalEkins']
    if curClass == 1:
        return None
    return medalEkinsCfg[(maxMedalClass - curClass) + 1] - frags


def __getMedalBeasthunterNextLevelValue(dossier):
    minFrags = dossiers.RECORD_CONFIGS['beasthunter']
    beastFrags = dossier['fragsBeast']
    (medals, series) = divmod(beastFrags, minFrags)
    return minFrags - medals


def __getMedalMousebanNextLevelValue(dossier):
    minFrags = dossiers.RECORD_CONFIGS['mousebane']
    mausFrags = dossier['vehTypeFrags'].get(dossiers.g_cache['mausTypeCompDescr'], 0)
    (medals, series) = divmod(mausFrags, minFrags)
    return minFrags - medals

ACHIEVEMENTS_NEXT_LEVEL_VALUES = {
    'medalKay': {
        'name': 'heroesLeft',
        'func': __getMedalKayNextLevelValue },
    'medalCarius': {
        'name': 'vehiclesLeft',
        'func': __getMedalCariusNextLevelValue },
    'medalKnispel': {
        'name': 'damageLeft',
        'func': __getMedalKnispelNextLevelValue },
    'medalPoppel': {
        'name': 'vehiclesLeft',
        'func': __getMedalPoppelNextLevelValue },
    'medalAbrams': {
        'name': 'battlesLeft',
        'func': __getMedalAbramsNextLevelValue },
    'medalLeClerc': {
        'name': 'capturePointsLeft',
        'func': __getMedalLeClercNextLevelValue },
    'medalLavrinenko': {
        'name': 'dropPointsLeft',
        'func': __getMedalLavrinenkoNextLevelValue },
    'medalEkins': {
        'name': 'vehiclesLeft',
        'func': __getMedalEkinsNextLevelValue },
    'beasthunter': {
        'name': 'vehiclesLeft',
        'func': __getMedalBeasthunterNextLevelValue },
    'mousebane': {
        'name': 'vehiclesLeft',
        'func': __getMedalMousebanNextLevelValue } }

