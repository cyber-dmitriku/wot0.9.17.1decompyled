# Source Generated with Decompyle++
# File: BattleResults.pyc (Python 2.6)

import ArenaType
from CurrentVehicle import g_currentVehicle
from account_helpers.AccountPrebattle import AccountPrebattle
from arena_achievements import ACHIEVEMENTS
from constants import ARENA_BONUS_TYPE
import constants
from dossiers import RECORD_NAMES, RECORD_INDICES
from gui import makeHtmlString, GUI_SETTINGS
from gui.Scaleform.utils.dossiers_utils import getMedalDict
from gui.Scaleform.utils.requesters import Requester
from helpers import i18n
from messenger import getLongDatetimeFormat
import BigWorld
from adisp import process, async
from debug_utils import *
from items import vehicles as vehicles_core
from gui.Scaleform.windows import UIInterface
from gui.Scaleform.utils.requesters import StatsRequester
from messenger.gui import MessengerDispatcher
__author__ = 'd_dichkovsky'
RESULT_ = '#menu:finalStatistic/commonStats/resultlabel/{0}'
BATTLE_RESULTS_STR_ = '#battle_results:'
FINISH_REASON_ = BATTLE_RESULTS_STR_ + 'finish/reason/{0}'
XP_TITLE_ = BATTLE_RESULTS_STR_ + 'common/details/xpTitle'
XP_TITLE_DAILY_ = BATTLE_RESULTS_STR_ + 'common/details/xpTitleFirstVictory'
MILEAGE_STR_KEY_ = BATTLE_RESULTS_STR_ + 'team/stats/mileage'
TIME_DURATION_STR_ = BATTLE_RESULTS_STR_ + 'details/time/value'
XP_MULTIPLIER_SIGN_KEY_ = BATTLE_RESULTS_STR_ + 'common/xpMultiplierSign'
UNKNOWN_PLAYER_NAME_VALUE_ = BATTLE_RESULTS_STR_ + 'common/unknownPlayerName'
UNKNOWN_VEHICLE_NAME_VALUE_ = BATTLE_RESULTS_STR_ + 'common/unknownVehicleName'
ARENA_TYPE_ = '#arenas:type/{0}/name'
VEHICLE_ICON_FILE_ = '../maps/icons/vehicle/{0}.png'
VEHICLE_ICON_SMALL_FILE_ = '../maps/icons/vehicle/small/{0}.png'
VEHICLE_NO_IMAGE_FILE_NAME_ = 'noImage'
ARENA_SCREEN_FILE_ = '../maps/icons/map/stats/{0}.png'
ARENA_NAME_PATTERN_ = '{0} - {1}'
ACHIEVEMENTS_TO_FILTER = [
    'invincible',
    'diehard']
ACHIEVEMENTS_ON_RIGHT = tuple(filter((lambda item: item not in ACHIEVEMENTS_TO_FILTER), ACHIEVEMENTS))
ACHIEVEMENTS_WITH_RIBBON = ('evileye', 'medalOrlik', 'medalOskin', 'medalHalonen', 'medalBurda', 'medalBillotte', 'medalKolobanov', 'medalFadin', 'medalRadleyWalters', 'medalLafayettePool', 'medalLehvaslaiho', 'medalNikolas', 'medalPascucci', 'medalDumitru', 'medalBrunoPietro', 'medalTarczay', 'heroesOfRassenay', 'medalDeLanglade', 'medalTamadaYoshio', 'raider', 'kamikaze', 'bombardier', 'ironMan', 'invincible', 'medalBrothersInArms', 'medalCrucialContribution', 'medalWittmann', 'handOfDeath', 'luckyDevil', 'sturdy', 'mousebane', 'beasthunter', 'sinai', 'markOfMastery4')
STATS_KEYS_ = [
    ('shots', True),
    ('hits', True),
    ('he_hits', True),
    ('pierced', True),
    ('damageDealt', True),
    ('shotsReceived', True),
    ('teamHitsDamage', False),
    ('spotted', True),
    ('damaged', True),
    ('kills', True),
    ('damageAssisted', True),
    ('capturePoints', True),
    ('droppedCapturePoints', True),
    ('mileage', False)]

class BattleResultsManager(UIInterface):
    _BattleResultsManager__playersNameCache = dict()
    TEST_MALIAVKO = {
        'personal': {
            'spotted': 19,
            'repair': 0,
            'xpPenalty': 0,
            'markOfMastery': 2,
            'killerID': 0,
            'damageReceived': 244,
            'premiumCreditsFactor10': 15,
            'shotsReceived': 123,
            'premiumXPFactor10': 15,
            'xp': 3104,
            'eventIndices': [
                1,
                2],
            'droppedCapturePoints': 0,
            'damageAssisted': 0,
            'creditsContributionIn': 0,
            'eventFreeXP': 10,
            'damaged': 19,
            'autoRepairCost': 200000,
            'typeCompDescr': 54289,
            'capturePoints': 0,
            'aogasFactor10': 8,
            'eventCredits': 100,
            'health': 1650,
            'details': {
                7456: {
                    'spotted': 1,
                    'hits': 1,
                    'fire': 0,
                    'he_hits': 0,
                    'damageDealt': 150,
                    'crits': 1,
                    'pierced': 1,
                    'killed': 1,
                    'damageAssisted': 0 },
                7457: {
                    'spotted': 1,
                    'hits': 1,
                    'fire': 0,
                    'he_hits': 0,
                    'damageDealt': 190,
                    'crits': 0,
                    'pierced': 1,
                    'killed': 1,
                    'damageAssisted': 0 },
                7458: {
                    'spotted': 1,
                    'hits': 3,
                    'fire': 0,
                    'he_hits': 0,
                    'damageDealt': 320,
                    'crits': 1,
                    'pierced': 3,
                    'killed': 1,
                    'damageAssisted': 0 },
                7451: {
                    'spotted': 1,
                    'hits': 1,
                    'fire': 0,
                    'he_hits': 0,
                    'damageDealt': 105,
                    'crits': 1,
                    'pierced': 1,
                    'killed': 1,
                    'damageAssisted': 0 },
                7460: {
                    'spotted': 1,
                    'hits': 2,
                    'fire': 0,
                    'he_hits': 0,
                    'damageDealt': 400,
                    'crits': 0,
                    'pierced': 2,
                    'killed': 1,
                    'damageAssisted': 0 },
                7461: {
                    'spotted': 1,
                    'hits': 1,
                    'fire': 0,
                    'he_hits': 0,
                    'damageDealt': 140,
                    'crits': 0,
                    'pierced': 1,
                    'killed': 1,
                    'damageAssisted': 0 },
                7462: {
                    'spotted': 1,
                    'hits': 1,
                    'fire': 0,
                    'he_hits': 0,
                    'damageDealt': 200,
                    'crits': 0,
                    'pierced': 1,
                    'killed': 1,
                    'damageAssisted': 0 },
                7452: {
                    'spotted': 1,
                    'hits': 1,
                    'fire': 0,
                    'he_hits': 0,
                    'damageDealt': 185,
                    'crits': 1,
                    'pierced': 1,
                    'killed': 1,
                    'damageAssisted': 0 },
                7453: {
                    'spotted': 1,
                    'hits': 1,
                    'fire': 0,
                    'he_hits': 0,
                    'damageDealt': 250,
                    'crits': 0,
                    'pierced': 1,
                    'killed': 1,
                    'damageAssisted': 0 },
                7454: {
                    'spotted': 1,
                    'hits': 1,
                    'fire': 0,
                    'he_hits': 0,
                    'damageDealt': 250,
                    'crits': 0,
                    'pierced': 1,
                    'killed': 1,
                    'damageAssisted': 0 },
                7479: {
                    'spotted': 1,
                    'hits': 1,
                    'fire': 0,
                    'he_hits': 0,
                    'damageDealt': 140,
                    'crits': 0,
                    'pierced': 1,
                    'killed': 1,
                    'damageAssisted': 0 },
                7480: {
                    'spotted': 1,
                    'hits': 2,
                    'fire': 1,
                    'he_hits': 0,
                    'damageDealt': 520,
                    'crits': 1,
                    'pierced': 2,
                    'killed': 1,
                    'damageAssisted': 0 },
                7481: {
                    'spotted': 1,
                    'hits': 1,
                    'fire': 0,
                    'he_hits': 0,
                    'damageDealt': 290,
                    'crits': 0,
                    'pierced': 1,
                    'killed': 1,
                    'damageAssisted': 0 },
                7450: {
                    'spotted': 1,
                    'hits': 3,
                    'fire': 1,
                    'he_hits': 0,
                    'damageDealt': 690,
                    'crits': 1,
                    'pierced': 3,
                    'killed': 1,
                    'damageAssisted': 0 },
                7483: {
                    'spotted': 1,
                    'hits': 1,
                    'fire': 0,
                    'he_hits': 0,
                    'damageDealt': 150,
                    'crits': 0,
                    'pierced': 1,
                    'killed': 1,
                    'damageAssisted': 0 },
                7484: {
                    'spotted': 1,
                    'hits': 2,
                    'fire': 0,
                    'he_hits': 0,
                    'damageDealt': 400,
                    'crits': 2,
                    'pierced': 2,
                    'killed': 1,
                    'damageAssisted': 0 },
                7485: {
                    'spotted': 1,
                    'hits': 3,
                    'fire': 0,
                    'he_hits': 0,
                    'damageDealt': 690,
                    'crits': 0,
                    'pierced': 3,
                    'killed': 1,
                    'damageAssisted': 0 },
                7486: {
                    'spotted': 1,
                    'hits': 1,
                    'fire': 0,
                    'he_hits': 0,
                    'damageDealt': 105,
                    'crits': 2,
                    'pierced': 1,
                    'killed': 1,
                    'damageAssisted': 0 },
                7455: {
                    'spotted': 1,
                    'hits': 2,
                    'fire': 1,
                    'he_hits': 0,
                    'damageDealt': 400,
                    'crits': 2,
                    'pierced': 2,
                    'killed': 1,
                    'damageAssisted': 0 } },
            'achievements': [
                32,
                35,
                24,
                4,
                0,
                6,
                14],
            'isPremium': False,
            'mileage': 249,
            'freeXP': 155,
            'kills': 19,
            'eventTMenXP': 0,
            'team': 1,
            'tmenXP': 3104,
            'pierced': 29,
            'credits': 106974,
            'eventGold': 10,
            'accountDBID': 76,
            'autoEquipCost': None,
            'gold': 0,
            'tdamageDealt': 0,
            'hits': 29,
            'dossierPopUps': [
                (2, 1),
                (41, 2),
                (144, 4),
                (145, 4),
                (143, 4),
                (38, 4),
                (34, 6),
                (40, 6),
                (55, 4),
                (110, 4),
                (151, 3),
                (150, 1),
                (149, 1)],
            'eventXP': 20,
            'tkills': 0,
            'creditsPenalty': 0,
            'damageDealt': 5575,
            'autoLoadCost': None,
            'vehLockTimeFactor': 1,
            'shots': 43,
            'he_hits': 0,
            'lifeTime': 139,
            'creditsContributionOut': 0,
            'dailyXPFactor10': 20 },
        'players': {
            76: {
                'clanDBID': 0,
                'clanAbbrev': '',
                'team': 1,
                'name': 'zeo161',
                'prebattleID': 2301 } },
        'vehicles': {
            7448: {
                'spotted': 19,
                'repair': 0,
                'killerID': 0,
                'damageReceived': 244,
                'shotsReceived': 123,
                'xp': 3104,
                'droppedCapturePoints': 0,
                'damageAssisted': 0,
                'damaged': 19,
                'typeCompDescr': 54289,
                'capturePoints': 0,
                'health': 1650,
                'details': ' \x1d\x0\x0!\x1d\x0\x0"\x1d\x0\x0\x1a\x1d\x0\x0\x1b\x1d\x0\x0\x1c\x1d\x0\x0\x1d\x1d\x0\x0\x1e\x1d\x0\x0\x1f\x1d\x0\x0$\x1d\x0\x0%\x1d\x0\x0&\x1d\x0\x0;\x1d\x0\x08\x1d\x0\x07\x1d\x0\x09\x1d\x0\x0<\x1d\x0\x0=\x1d\x0\x0>\x1d\x0\x0\x1\x0\x1\x0\x1\x0\x0\x0\x1\x0\x96\x0\x0\x0\x1\x0\x0\x0\x1\x0\x1\x0\x1\x0\x0\x0\x1\x0\xbe\x0\x0\x0\x0\x0\x0\x0\x1\x0\x1\x0\x3\x0\x0\x0\x3\x0@\x1\x0\x0\x1\x0\x0\x0\x1\x0\x1\x0\x3\x0\x0\x0\x3\x0\xb2\x2\x0\x0\x1\x0\x1\x0\x1\x0\x1\x0\x1\x0\x0\x0\x1\x0i\x0\x0\x0\x1\x0\x0\x0\x1\x0\x1\x0\x1\x0\x0\x0\x1\x0\xb9\x0\x0\x0\x1\x0\x0\x0\x1\x0\x1\x0\x1\x0\x0\x0\x1\x0\xfa\x0\x0\x0\x0\x0\x0\x0\x1\x0\x1\x0\x1\x0\x0\x0\x1\x0\xfa\x0\x0\x0\x0\x0\x0\x0\x1\x0\x1\x0\x2\x0\x0\x0\x2\x0\x90\x1\x0\x0\x2\x0\x1\x0\x1\x0\x1\x0\x2\x0\x0\x0\x2\x0\x90\x1\x0\x0\x0\x0\x0\x0\x1\x0\x1\x0\x1\x0\x0\x0\x1\x0\x8c\x0\x0\x0\x0\x0\x0\x0\x1\x0\x1\x0\x1\x0\x0\x0\x1\x0\xc8\x0\x0\x0\x0\x0\x0\x0\x1\x0\x1\x0\x1\x0\x0\x0\x1\x0\x96\x0\x0\x0\x0\x0\x0\x0\x1\x0\x1\x0\x2\x0\x0\x0\x2\x0\x8\x2\x0\x0\x1\x0\x1\x0\x1\x0\x1\x0\x1\x0\x0\x0\x1\x0\x8c\x0\x0\x0\x0\x0\x0\x0\x1\x0\x1\x0\x1\x0\x0\x0\x1\x0"\x1\x0\x0\x0\x0\x0\x0\x1\x0\x1\x0\x2\x0\x0\x0\x2\x0\x90\x1\x0\x0\x2\x0\x0\x0\x1\x0\x1\x0\x3\x0\x0\x0\x3\x0\xb2\x2\x0\x0\x0\x0\x0\x0\x1\x0\x1\x0\x1\x0\x0\x0\x1\x0i\x0\x0\x0\x2\x0\x0\x0',
                'achievements': [
                    32,
                    35,
                    24,
                    4,
                    0,
                    6,
                    14],
                'mileage': 249,
                'freeXP': 155,
                'kills': 19,
                'team': 1,
                'pierced': 29,
                'credits': 106974,
                'accountDBID': 76,
                'tdamageDealt': 0,
                'hits': 29,
                'tkills': 0,
                'damageDealt': 5575,
                'shots': 43,
                'he_hits': 0,
                'lifeTime': 139 } },
        'common': {
            'finishReason': 1,
            'arenaCreateTime': 1344516473,
            'duration': 139.6,
            'arenaTypeID': 1024,
            'winnerTeam': 1,
            'vehLockMode': 0,
            'bonusType': 1 },
        'arenaUniqueID': 0x33E5023B179L }
    TEST_DATA = {
        'personal': {
            'spotted': 0,
            'repair': 0,
            'xpPenalty': 0,
            'markOfMastery': 0,
            'killerID': 0,
            'damageReceived': 0,
            'premiumCreditsFactor10': 15,
            'shotsReceived': 0,
            'premiumXPFactor10': 15,
            'xp': 68,
            'droppedCapturePoints': 0,
            'damageAssisted': 0,
            'creditsContributionIn': 0,
            'eventFreeXP': 0,
            'damaged': 0,
            'autoRepairCost': None,
            'typeCompDescr': 9217,
            'capturePoints': 0,
            'aogasFactor10': 10,
            'eventCredits': 0,
            'health': 1550,
            'details': { },
            'achievements': [
                34,
                35],
            'isPremium': False,
            'mileage': 0,
            'freeXP': 3,
            'kills': 0,
            'eventTMenXP': 0,
            'team': 2,
            'tmenXP': 68,
            'pierced': 0,
            'credits': 15600,
            'eventGold': 0,
            'accountDBID': 225,
            'autoEquipCost': (0, 0),
            'gold': 0,
            'tdamageDealt': 0,
            'isTeamKiller': False,
            'hits': 0,
            'dossierPopUps': [],
            'eventXP': 0,
            'tkills': 0,
            'creditsPenalty': 0,
            'damageDealt': 0,
            'autoLoadCost': (0, 0),
            'shots': 0,
            'he_hits': 0,
            'lifeTime': 15,
            'creditsContributionOut': 0,
            'dailyXPFactor10': 10 },
        'players': {
            224: {
                'clanDBID': 0,
                'clanAbbrev': '',
                'team': 2,
                'name': 'kid1',
                'prebattleID': 15024 },
            225: {
                'clanDBID': 0,
                'clanAbbrev': '',
                'team': 2,
                'name': 'kid2',
                'prebattleID': 15024 },
            250: {
                'clanDBID': 0,
                'clanAbbrev': '',
                'team': 2,
                'name': 'kid3',
                'prebattleID': 15024 },
            159: {
                'clanDBID': 0,
                'clanAbbrev': '',
                'team': 1,
                'name': 'kid',
                'prebattleID': 15024 } },
        'vehicles': {
            15032: {
                'spotted': 0,
                'repair': 0,
                'killerID': 0,
                'damageReceived': 0,
                'shotsReceived': 0,
                'xp': 68,
                'droppedCapturePoints': 0,
                'damageAssisted': 0,
                'damaged': 0,
                'typeCompDescr': 3649,
                'capturePoints': 0,
                'health': 1800,
                'details': '',
                'achievements': [
                    34,
                    35],
                'mileage': 0,
                'freeXP': 3,
                'kills': 0,
                'team': 2,
                'pierced': 0,
                'credits': 9750,
                'accountDBID': 224,
                'gold': 0,
                'tdamageDealt': 0,
                'isTeamKiller': False,
                'hits': 0,
                'tkills': 0,
                'damageDealt': 0,
                'shots': 0,
                'he_hits': 0,
                'lifeTime': 15 },
            15033: {
                'spotted': 0,
                'repair': 0,
                'killerID': 0,
                'damageReceived': 0,
                'shotsReceived': 0,
                'xp': 68,
                'droppedCapturePoints': 0,
                'damageAssisted': 0,
                'damaged': 0,
                'typeCompDescr': 9217,
                'capturePoints': 0,
                'health': 1550,
                'details': '',
                'achievements': [
                    34,
                    35],
                'mileage': 0,
                'freeXP': 3,
                'kills': 0,
                'team': 2,
                'pierced': 0,
                'credits': 15600,
                'accountDBID': 225,
                'gold': 0,
                'tdamageDealt': 0,
                'isTeamKiller': False,
                'hits': 0,
                'tkills': 0,
                'damageDealt': 0,
                'shots': 0,
                'he_hits': 0,
                'lifeTime': 15 },
            15034: {
                'spotted': 0,
                'repair': 0,
                'killerID': 0,
                'damageReceived': 0,
                'shotsReceived': 0,
                'xp': 68,
                'droppedCapturePoints': 0,
                'damageAssisted': 0,
                'damaged': 0,
                'typeCompDescr': 3329,
                'capturePoints': 0,
                'health': 90,
                'details': '',
                'achievements': [
                    34,
                    35],
                'mileage': 0,
                'freeXP': 3,
                'kills': 0,
                'team': 2,
                'pierced': 0,
                'credits': 1632,
                'accountDBID': 250,
                'gold': 0,
                'tdamageDealt': 0,
                'isTeamKiller': False,
                'hits': 0,
                'tkills': 0,
                'damageDealt': 0,
                'shots': 0,
                'he_hits': 0,
                'lifeTime': 15 },
            15035: {
                'spotted': 0,
                'repair': 0,
                'killerID': 15035,
                'damageReceived': 0,
                'shotsReceived': 0,
                'xp': 0,
                'droppedCapturePoints': 0,
                'damageAssisted': 0,
                'damaged': 0,
                'typeCompDescr': 545,
                'capturePoints': 0,
                'health': -1,
                'details': '',
                'achievements': [],
                'mileage': 66,
                'freeXP': 0,
                'kills': 0,
                'team': 1,
                'pierced': 0,
                'credits': 955,
                'accountDBID': 159,
                'gold': 0,
                'tdamageDealt': 0,
                'isTeamKiller': False,
                'hits': 0,
                'tkills': 0,
                'damageDealt': 0,
                'shots': 1,
                'he_hits': 0,
                'lifeTime': 10 } },
        'common': {
            'finishReason': 1,
            'arenaCreateTime': 1346150443,
            'duration': 15,
            'arenaTypeID': 3,
            'winnerTeam': 2,
            'vehLockMode': 0,
            'bonusType': 1 },
        'arenaUniqueID': 0x2851503CA02BL }
    TEST_DATA1 = {
        'personal': {
            'spotted': 1,
            'repair': 1517,
            'xpPenalty': 0,
            'markOfMastery': 0,
            'killerID': 0,
            'damageReceived': 84,
            'premiumCreditsFactor10': 15,
            'shotsReceived': 0,
            'premiumXPFactor10': 15,
            'xp': 422,
            'droppedCapturePoints': 0,
            'damageAssisted': 0,
            'creditsContributionIn': 0,
            'eventFreeXP': 0,
            'damaged': 1,
            'autoRepairCost': 1517,
            'typeCompDescr': 12305,
            'capturePoints': 0,
            'aogasFactor10': 10,
            'eventCredits': 0,
            'health': 1966,
            'details': {
                44: {
                    'spotted': 1,
                    'hits': 0,
                    'fire': 0,
                    'he_hits': 0,
                    'damageDealt': 200,
                    'crits': 1,
                    'pierced': 0,
                    'killed': 1,
                    'damageAssisted': 0 } },
            'achievements': [
                35],
            'isPremium': True,
            'mileage': 748,
            'freeXP': 20,
            'kills': 1,
            'eventTMenXP': 0,
            'team': 1,
            'tmenXP': 422,
            'pierced': 0,
            'credits': 16534,
            'eventGold': 0,
            'accountDBID': 159,
            'autoEquipCost': (0, 0),
            'gold': 0,
            'tdamageDealt': 0,
            'isTeamKiller': False,
            'hits': 0,
            'dossierPopUps': [],
            'eventXP': 0,
            'tkills': 0,
            'creditsPenalty': 0,
            'damageDealt': 200,
            'autoLoadCost': (0, 0),
            'shots': 0,
            'he_hits': 0,
            'lifeTime': 143,
            'creditsContributionOut': 0,
            'dailyXPFactor10': 20 },
        'players': {
            159: {
                'clanDBID': 3,
                'clanAbbrev': 'KID',
                'team': 1,
                'name': 'kid',
                'prebattleID': 35 } },
        'vehicles': {
            41: {
                'spotted': 1,
                'repair': 1517,
                'killerID': 0,
                'damageReceived': 84,
                'shotsReceived': 0,
                'xp': 141,
                'droppedCapturePoints': 0,
                'damageAssisted': 0,
                'damaged': 1,
                'typeCompDescr': 12305,
                'capturePoints': 0,
                'health': 1966,
                'details': ',\x0\x0\x0\x1\x0\x1\x0\x0\x0\x0\x0\x0\x0\xc8\x0\x0\x0\x1\x0\x0\x0',
                'achievements': [
                    35],
                'mileage': 748,
                'freeXP': 7,
                'kills': 1,
                'team': 1,
                'pierced': 0,
                'credits': 11023,
                'accountDBID': 159,
                'gold': 0,
                'tdamageDealt': 0,
                'isTeamKiller': False,
                'hits': 0,
                'tkills': 0,
                'damageDealt': 200,
                'shots': 0,
                'he_hits': 0,
                'lifeTime': 143 } },
        'common': {
            'finishReason': 1,
            'arenaCreateTime': 1346742844,
            'duration': 143.7,
            'arenaTypeID': 1024,
            'winnerTeam': 1,
            'vehLockMode': 0,
            'bonusType': 1 },
        'arenaUniqueID': 0x255045AA3CL }
    
    def __init__(self):
        UIInterface.__init__(self)

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self.uiHolder.addExternalCallbacks({
            'battleResults.show': self.onBattleResultsShow,
            'battleResults.onWndLoaded': self.onBattleResultsWndLoaded })

    
    def dispossessUI(self):
        if self.uiHolder is not None:
            self.uiHolder.removeExternalCallbacks('battleResults.show', 'battleResults.onWndLoaded')
        
        UIInterface.dispossessUI(self)

    
    def onBattleResultsShow(self, cid, arenaUniqueId):
        if GUI_SETTINGS.battleStatsInHangar:
            self._BattleResultsManager__showBattleResults(arenaUniqueId)
        

    
    def onBattleResultsWndLoaded(self, cid, arenaUniqueId):
        wnd = self.getBattleResultsWindow(long(arenaUniqueId))
        if wnd is not None:
            wnd.script = self
        

    
    def getBattleResultsWindow(self, arenaUniqueId):
        
        try:
            g_windowsManager = g_windowsManager
            import gui.WindowsManager
            wl = g_windowsManager.window.getMember('windowLayout')
            wl.resync()
            window = wl.children['battleResultsWnd' + str(arenaUniqueId)]
            window.resync()
            return window.form.form
        except Exception:
            LOG_CURRENT_EXCEPTION()
            return None


    
    def _BattleResultsManager__showBattleResults(self, arenaUniqueId):
        self.uiHolder.call('common.showBattleResults', [
            str(arenaUniqueId)])

    
    def _BattleResultsManager__getPlayerName(self, playerDBID, playersData):
        playerName = self._BattleResultsManager__playersNameCache.get(playerDBID, None)
        if playerName is None:
            playerInfo = playersData.get(playerDBID, dict())
            playerName = playerInfo.get('name', i18n.makeString(UNKNOWN_PLAYER_NAME_VALUE_))
            clanName = playerInfo.get('clanAbbrev', '')
            if len(clanName) > 0:
                playerName = ''.join([
                    playerName,
                    ' [',
                    clanName,
                    ']'])
            
            self._BattleResultsManager__playersNameCache[playerDBID] = playerName
        
        return playerName

    
    def _BattleResultsManager__getVehicleData(self, vehicleCompDesc):
        vehicleName = i18n.makeString(UNKNOWN_VEHICLE_NAME_VALUE_)
        vehicleShortName = i18n.makeString(UNKNOWN_VEHICLE_NAME_VALUE_)
        vehicleIcon = VEHICLE_ICON_FILE_.format(VEHICLE_NO_IMAGE_FILE_NAME_)
        vehicleIconSmall = VEHICLE_ICON_SMALL_FILE_.format(VEHICLE_NO_IMAGE_FILE_NAME_)
        vehicleBalanceWeight = 0
        if vehicleCompDesc:
            vt = vehicles_core.getVehicleType(vehicleCompDesc)
            vehicleName = vt.userString
            vehicleShortName = vt.shortUserString
            nameReplaced = vt.name.replace(':', '-')
            vehicleIcon = VEHICLE_ICON_FILE_.format(nameReplaced)
            vehicleIconSmall = VEHICLE_ICON_SMALL_FILE_.format(nameReplaced)
            vehicleBalanceWeight = vt.balanceByClass
        
        return (vehicleName, vehicleShortName, vehicleIcon, vehicleIconSmall, vehicleBalanceWeight)

    
    def _BattleResultsManager__vehiclesComparator(self, item, other):
        res = 0
        iKiller = item.get('killerID', 0)
        iWeight = item.get('balanceWeight', 0)
        oKiller = other.get('killerID', 0)
        oWeight = other.get('balanceWeight', 0)
        if (iKiller == 0 or oKiller == 0 or iKiller != 0) and oKiller != 0:
            res = cmp(iWeight, oWeight)
            if not res:
                res = cmp(item.get('vehicleName', ''), other.get('vehicleName', ''))
            
        elif not iKiller:
            res = -1
        else:
            res = 1
        return res

    
    def _BattleResultsManager__getStatsLine(self, label = None, col1 = None, col2 = None, col
