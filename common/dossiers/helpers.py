# Source Generated with Decompyle++
# File: helpers.pyc (Python 2.6)

import time
import dossiers
import arena_achievements
from itertools import izip
from constants import ARENA_BONUS_TYPE_CAPS as BONUS_CAPS
from debug_utils import *

def updateVehicleDossier(descr, battleResults, dossierXP, resultsOverriding = None):
    results = _resultOverriding(battleResults, resultsOverriding)
    (stop, _, _) = _updateDossierCommonPart(descr, results, dossierXP)
    if not stop:
        _updateVehicleDossierImpl(descr, results)
    
    return set(descr.popUps)


def updateAccountDossier(databaseID, descr, battleResults, dossierXP, vehTypeCompDescr, vehDossierDescr, resultsOverriding = None):
    results = _resultOverriding(battleResults, resultsOverriding)
    (stop, isMaxFragsGained, isMaxXPGained) = _updateDossierCommonPart(descr, results, dossierXP)
    if not stop:
        _updateAccountDossierImpl(descr, results, vehTypeCompDescr, vehDossierDescr, isMaxFragsGained, isMaxXPGained)
        _validateAccountAndVehicleDossiers(databaseID, descr, vehDossierDescr, vehTypeCompDescr)
    
    return set(descr.popUps)


def updateTankmanDossier(descr, battleResults, resultsOverriding = None):
    results = _resultOverriding(battleResults, resultsOverriding)
    _updateTankmanDossierImpl(descr, results)
    return set(descr.popUps)


def _resultOverriding(battleResults, resultsOverriding):
    if resultsOverriding is None:
        return battleResults
    results = dict(battleResults)
    results.update(resultsOverriding)
    return results


def _updateDossierCommonPart(descr, results, dossierXP):
    if not bool(BONUS_CAPS.get(results['bonusType']) & BONUS_CAPS.DOSSIER_TOTAL_VALUES):
        return (True, False, False)
    descr.expand()
    descr['battleLifeTime'] += results['lifeTime']
    descr['lastBattleTime'] = int(time.time())
    _updateDossierRecordsWithBonusTypePrefix(descr, '', results, dossierXP)
    if bool(BONUS_CAPS.get(results['bonusType']) & BONUS_CAPS.DOSSIER_COMPANY_VALUES):
        _updateDossierRecordsWithBonusTypePrefix(descr, 'company/', results, dossierXP)
    
    if bool(BONUS_CAPS.get(results['bonusType']) & BONUS_CAPS.DOSSIER_CLAN_VALUES):
        _updateDossierRecordsWithBonusTypePrefix(descr, 'clan/', results, dossierXP)
    
    if results['killerID'] == 0 and results['winnerTeam'] == results['team']:
        descr['winAndSurvived'] += 1
    
    kill_list = results['kill_list']
    if kill_list:
        vehTypeFrags = dict(descr['vehTypeFrags'])
        vehicles8p = dossiers.g_cache['vehicles8+']
        beastVehicles = dossiers.g_cache['beastVehicles']
        sinaiVehicles = dossiers.g_cache['sinaiVehicles']
        frags8p = 0
        fragsBeast = 0
        fragsSinai = 0
        for (_, vtcd, _) in kill_list:
            frags = vehTypeFrags.get(vtcd, 0)
            vehTypeFrags[vtcd] = min(frags + 1, 60001)
            if vtcd in vehicles8p:
                frags8p += 1
            
            if vtcd in beastVehicles:
                fragsBeast += 1
            
            if vtcd in sinaiVehicles:
                fragsSinai += 1
                continue
            bool(BONUS_CAPS.get(results['bonusType']) & BONUS_CAPS.DOSSIER_TOTAL_VALUES)
        
        descr['vehTypeFrags'] = vehTypeFrags
        if frags8p != 0:
            descr['frags8p'] += frags8p
        
        if fragsBeast != 0:
            descr['fragsBeast'] += fragsBeast
        
        if fragsSinai != 0:
            descr['fragsSinai'] += fragsSinai
        
    
    if not bool(BONUS_CAPS.get(results['bonusType']) & BONUS_CAPS.DOSSIER_RND_VALUES):
        return (False, False, False)
    isMaxXPGained = False
    if dossierXP != 0 and dossierXP >= descr['maxXP']:
        isMaxXPGained = True
        descr['maxXP'] = dossierXP
    
    for achieveIdx in results['achievements']:
        arena_achievements.updateDossierRecord(descr, achieveIdx)
    
    isMaxFragsGained = False
    if kill_list and len(kill_list) >= descr['maxFrags']:
        descr['maxFrags'] = len(kill_list)
        isMaxFragsGained = True
    
    return (False, isMaxFragsGained, isMaxXPGained)


def _updateDossierRecordsWithBonusTypePrefix(descr, prefix, results, dossierXP):
    descr[prefix + 'battlesCount'] += 1
    if dossierXP != 0:
        descr[prefix + 'xp'] += dossierXP
    
    if results['winnerTeam'] == results['team']:
        descr[prefix + 'wins'] += 1
    elif results['winnerTeam'] == 3 - results['team']:
        descr[prefix + 'losses'] += 1
    
    if results['killerID'] == 0:
        descr[prefix + 'survivedBattles'] += 1
    
    shots = results['shots']
    if shots != 0:
        descr[prefix + 'shots'] += shots
    
    hits = results['hits']
    if hits != 0:
        descr[prefix + 'hits'] += hits
    
    spotted = results['spotted']
    if spotted:
        descr[prefix + 'spotted'] += spotted
    
    damageDealt = results['damageDealt']
    if damageDealt != 0:
        descr[prefix + 'damageDealt'] += damageDealt
    
    damageReceived = results['damageReceived']
    if damageReceived != 0:
        descr[prefix + 'damageReceived'] += damageReceived
    
    capturePoints = results['capturePoints']
    if capturePoints != 0:
        descr[prefix + 'capturePoints'] += capturePoints
    
    droppedCapturePoints = min(results['droppedCapturePoints'], 100)
    if droppedCapturePoints != 0:
        descr[prefix + 'droppedCapturePoints'] += droppedCapturePoints
    
    kills = results['kills']
    if kills:
        descr[prefix + 'frags'] += kills
    


def _updateVehicleDossierImpl(descr, results):
    if not bool(BONUS_CAPS.get(results['bonusType']) & BONUS_CAPS.DOSSIER_RND_VALUES):
        return None
    if descr['markOfMastery'] < results['markOfMastery']:
        descr['markOfMastery'] = results['markOfMastery']
    
    _updatePerBattleSeries(descr, 'invincible', results)
    _updatePerBattleSeries(descr, 'diehard', results)
    _updateInBattleSeries(descr, 'sniper', results)
    _updateInBattleSeries(descr, 'killing', results)
    _updateInBattleSeries(descr, 'piercing', results)


def _updatePerBattleSeries(descr, achieveName, results):
    achieveIdx = arena_achievements.ACHIEVEMENT_INDICES[achieveName]
    recordName = achieveName + 'Series'
    if not descr.hasRecord(recordName):
        return None
    if achieveIdx in results['achievements']:
        descr[recordName] += 1
    else:
        descr[recordName] = 0


def _updateInBattleSeries(descr, achieveName, results):
    achieveIdx = arena_achievements.INBATTLE_SERIES_INDICES[achieveName]
    recordName = achieveName + 'Series'
    if not descr.hasRecord(recordName):
        return None
    series = results['series'].get(achieveIdx, [])
    if series:
        descr[recordName] = descr[recordName] + series[0]
    
    for runLength in series[1:]:
        descr[recordName] = runLength
    


def _updateAccountDossierImpl(descr, results, vehTypeCompDescr, vehDossierDescr, isMaxFragsGained, isMaxXPGained):
    if not vehDossierDescr is not None:
        raise AssertionError
    vehDossiersCut = dict(descr['vehDossiersCut'])
    (battlesCount, wins, markOfMastery) = vehDossiersCut.get(vehTypeCompDescr, (0, 0, 0))
    if results['winnerTeam'] == results['team']:
        wins += 1
    
    if vehDossierDescr['markOfMastery'] > markOfMastery:
        markOfMastery = vehDossierDescr['markOfMastery']
    
    vehDossiersCut[vehTypeCompDescr] = (battlesCount + 1, wins, markOfMastery)
    descr['vehDossiersCut'] = vehDossiersCut
    if not bool(BONUS_CAPS.get(results['bonusType']) & BONUS_CAPS.DOSSIER_RND_VALUES):
        return None
    series = ('maxInvincibleSeries', 'maxDiehardSeries', 'maxSniperSeries', 'maxKillingSeries', 'maxPiercingSeries')
    for recordName in series:
        if vehDossierDescr[recordName] > descr[recordName]:
            descr[recordName] = vehDossierDescr[recordName]
            continue
        bool(BONUS_CAPS.get(results['bonusType']) & BONUS_CAPS.DOSSIER_RND_VALUES)
    
    if isMaxXPGained:
        descr['maxXPVehicle'] = vehTypeCompDescr
    
    if isMaxFragsGained:
        descr['maxFragsVehicle'] = vehTypeCompDescr
    


def _updateTankmanDossierImpl(descr, results):
    if not bool(BONUS_CAPS.get(results['bonusType']) & BONUS_CAPS.DOSSIER_TOTAL_VALUES):
        return None
    descr['battlesCount'] += 1
    if not bool(BONUS_CAPS.get(results['bonusType']) & BONUS_CAPS.DOSSIER_RND_VALUES):
        return None
    for achieveIdx in results['achievements']:
        arena_achievements.updateDossierRecord(descr, achieveIdx)
    


def _validateAccountAndVehicleDossiers(databaseID, accDossier, vehDossier, vehTypeCompDescr):
    needRecalculateBattlesCountAndWins = False
    
    try:
        if accDossier['battlesCount'] < vehDossier['battlesCount']:
            raise Exception, "Sum 'battlesCount' mismatch (%s, %s, %s, %s)" % (databaseID, vehTypeCompDescr, accDossier['battlesCount'], vehDossier['battlesCount'])
        accDossier['battlesCount'] < vehDossier['battlesCount']
    except Exception:
        LOG_CURRENT_EXCEPTION()
        needRecalculateBattlesCountAndWins = True

    (battlesCount, wins, markOfMastery) = accDossier['vehDossiersCut'].get(vehTypeCompDescr, (0, 0, 0))
    
    try:
        if battlesCount != vehDossier['battlesCount']:
            raise Exception, "'battlesCount' mismatch (%s, %s, %s, %s)" % (databaseID, vehTypeCompDescr, battlesCount, vehDossier['battlesCount'])
        battlesCount != vehDossier['battlesCount']
    except Exception:
        LOG_CURRENT_EXCEPTION()
        vehDossiersCut = dict(accDossier['vehDossiersCut'])
        vehDossiersCut[vehTypeCompDescr] = (vehDossier['battlesCount'], wins, markOfMastery)
        accDossier['vehDossiersCut'] = vehDossiersCut
        battlesCount = vehDossier['battlesCount']
        needRecalculateBattlesCountAndWins = True

    
    try:
        if wins != vehDossier['wins']:
            raise Exception, "'wins' mismatch (%s, %s, %s, %s)" % (databaseID, vehTypeCompDescr, wins, vehDossier['wins'])
        wins != vehDossier['wins']
    except Exception:
        LOG_CURRENT_EXCEPTION()
        vehDossiersCut = dict(accDossier['vehDossiersCut'])
        vehDossiersCut[vehTypeCompDescr] = (battlesCount, vehDossier['wins'], markOfMastery)
        accDossier['vehDossiersCut'] = vehDossiersCut
        wins = vehDossier['wins']
        needRecalculateBattlesCountAndWins = True

    
    try:
        if markOfMastery != vehDossier['markOfMastery']:
            raise Exception, "'markOfMastery' mismatch (%s, %s, %s, %s)" % (databaseID, vehTypeCompDescr, markOfMastery, vehDossier['markOfMastery'])
        markOfMastery != vehDossier['markOfMastery']
    except Exception:
        LOG_CURRENT_EXCEPTION()
        vehDossiersCut = dict(accDossier['vehDossiersCut'])
        vehDossiersCut[vehTypeCompDescr] = (battlesCount, wins, vehDossier['markOfMastery'])
        accDossier['vehDossiersCut'] = vehDossiersCut

    if needRecalculateBattlesCountAndWins:
        _recalculateBattlesCountAndWins(accDossier)
    
    
    try:
        if accDossier['maxXP'] < vehDossier['maxXP']:
            raise Exception, "'maxXP' mismatch (%s, %s, %s, %s)" % (databaseID, vehTypeCompDescr, accDossier['maxXP'], vehDossier['maxXP'])
        accDossier['maxXP'] < vehDossier['maxXP']
    except Exception:
        LOG_CURRENT_EXCEPTION()
        accDossier['maxXP'] = vehDossier['maxXP']
        accDossier['maxXPVehicle'] = vehTypeCompDescr

    
    try:
        if accDossier['maxFrags'] < vehDossier['maxFrags']:
            raise Exception, "'maxFrags' mismatch (%s, %s, %s, %s)" % (databaseID, vehTypeCompDescr, accDossier['maxFrags'], vehDossier['maxFrags'])
        accDossier['maxFrags'] < vehDossier['maxFrags']
    except Exception:
        LOG_CURRENT_EXCEPTION()
        accDossier['maxFrags'] = vehDossier['maxFrags']
        accDossier['maxFragsVehicle'] = vehTypeCompDescr

    for record in arena_achievements.ACHIEVEMENTS:
        
        try:
            if record in accDossier and record in vehDossier and accDossier[record] < vehDossier[record]:
                raise Exception, "'%s' mismatch (%s, %s, %s, %s)" % (record, databaseID, vehTypeCompDescr, accDossier[record], vehDossier[record])
            accDossier[record] < vehDossier[record]
        continue
        except Exception:
            LOG_CURRENT_EXCEPTION()
            accDossier[record] = vehDossier[record]
            continue
        

    


def _recalculateBattlesCountAndWins(accDossier):
    battlesCountSum = 0
    winsSum = 0
    for (battlesCount, wins, markOfMastery) in accDossier['vehDossiersCut'].itervalues():
        battlesCountSum += battlesCount
        winsSum += wins
    
    accDossier['battlesCount'] = battlesCountSum
    accDossier['wins'] = winsSum


