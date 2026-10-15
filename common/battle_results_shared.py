# Source Generated with Decompyle++
# File: battle_results_shared.pyc (Python 2.6)

import struct
from itertools import izip
from debug_utils import *
VEH_INTERACTION_DETAILS = ('spotted', 'killed', 'hits', 'he_hits', 'pierced', 'damageDealt', 'damageAssisted', 'crits', 'fire')
VEH_INTERACTION_DETAILS_INDICES = dict((lambda .0: for x in .0:
(x[1], x[0]))(enumerate(VEH_INTERACTION_DETAILS)))
VEH_CELL_RESULTS = ('health', 'credits', 'xp', 'shots', 'hits', 'he_hits', 'pierced', 'damageDealt', 'damageAssisted', 'damageReceived', 'shotsReceived', 'spotted', 'damaged', 'kills', 'tdamageDealt', 'tkills', 'isTeamKiller', 'capturePoints', 'droppedCapturePoints', 'mileage', 'lifeTime', 'killerID', 'achievements', 'repair', 'freeXP', 'details', 'potentialDamageDealt', 'potentialDamageReceived', 'soloHitsAssisted', 'isEnemyBaseCaptured', 'stucks', 'spot_list', 'damage_list', 'kill_list', 'ammo', 'crewActivityFlags', 'series', 'tkillRating', 'tkillLog', 'hasTHit')
VEH_CELL_RESULTS_INDICES = dict((lambda .0: for x in .0:
(x[1], x[0]))(enumerate(VEH_CELL_RESULTS)))
VEH_BASE_RESULTS = VEH_CELL_RESULTS[:VEH_CELL_RESULTS.index('potentialDamageDealt')] + ('accountDBID', 'team', 'typeCompDescr', 'gold', 'xpPenalty', 'creditsPenalty', 'creditsContributionIn', 'creditsContributionOut', 'eventIndices', 'vehLockTimeFactor') + VEH_CELL_RESULTS[VEH_CELL_RESULTS.index('potentialDamageDealt'):]
VEH_BASE_RESULTS_INDICES = dict((lambda .0: for x in .0:
(x[1], x[0]))(enumerate(VEH_BASE_RESULTS)))
VEH_PUBLIC_RESULTS = VEH_BASE_RESULTS[:VEH_BASE_RESULTS.index('xpPenalty')]
VEH_PUBLIC_RESULTS_INDICES = dict((lambda .0: for x in .0:
(x[1], x[0]))(enumerate(VEH_PUBLIC_RESULTS)))
VEH_FULL_RESULTS = VEH_BASE_RESULTS[:VEH_BASE_RESULTS.index('eventIndices')] + ('tmenXP', 'eventCredits', 'eventGold', 'eventXP', 'eventFreeXP', 'eventTMenXP', 'autoRepairCost', 'autoLoadCost', 'autoEquipCost', 'isPremium', 'premiumXPFactor10', 'premiumCreditsFactor10', 'dailyXPFactor10', 'aogasFactor10', 'markOfMastery', 'dossierPopUps')
VEH_FULL_RESULTS_INDICES = dict((lambda .0: for x in .0:
(x[1], x[0]))(enumerate(VEH_FULL_RESULTS)))
PLAYER_INFO = ('name', 'clanDBID', 'clanAbbrev', 'prebattleID', 'team')
PLAYER_INFO_INDICES = dict((lambda .0: for x in .0:
(x[1], x[0]))(enumerate(PLAYER_INFO)))
COMMON_RESULTS = ('arenaTypeID', 'arenaCreateTime', 'winnerTeam', 'finishReason', 'duration', 'bonusType', 'vehLockMode')
COMMON_RESULTS_INDICES = dict((lambda .0: for x in .0:
(x[1], x[0]))(enumerate(COMMON_RESULTS)))
if not not (set(VEH_FULL_RESULTS) & set(COMMON_RESULTS)):
    raise AssertionError

def dictToList(indices, d):
    l = [
        None] * len(indices)
    for (name, index) in indices.iteritems():
        l[index] = d[name]
    
    return l


def listToDict(names, l):
    d = { }
    for x in enumerate(names):
        d[x[1]] = l[x[0]]
    
    return d


class _VehicleInteractionDetailsItem(object):
    
    def __init__(self, values, offset):
        self._VehicleInteractionDetailsItem__values = values
        self._VehicleInteractionDetailsItem__offset = offset

    
    def __getitem__(self, key):
        return self._VehicleInteractionDetailsItem__values[self._VehicleInteractionDetailsItem__offset + VEH_INTERACTION_DETAILS_INDICES[key]]

    
    def __setitem__(self, key, value):
        self._VehicleInteractionDetailsItem__values[self._VehicleInteractionDetailsItem__offset + VEH_INTERACTION_DETAILS_INDICES[key]] = min(int(value), 65535)

    
    def __str__(self):
        return str(dict(self))

    
    def __iter__(self):
        return izip(VEH_INTERACTION_DETAILS, self._VehicleInteractionDetailsItem__values[self._VehicleInteractionDetailsItem__offset:])



class VehicleInteractionDetails(object):
    
    def __init__(self, vehicleIDs, values):
        self._VehicleInteractionDetails__vehicleIDs = vehicleIDs
        self._VehicleInteractionDetails__values = values
        size = len(VEH_INTERACTION_DETAILS)
        self._VehicleInteractionDetails__offsets = (dict,)((lambda .0: for x in .0:
(x[1], x[0] * size))(enumerate(self._VehicleInteractionDetails__vehicleIDs)))

    
    def fromPacked(packed):
        size = len(VEH_INTERACTION_DETAILS)
        count = len(packed) / struct.calcsize('I%dH' % size)
        unpacked = struct.unpack('%dI%dH' % (count, count * size), packed)
        vehicleIDs = unpacked[:count]
        values = unpacked[count:]
        return VehicleInteractionDetails(vehicleIDs, values)

    fromPacked = staticmethod(fromPacked)
    
    def __getitem__(self, vehicleID):
        offset = self._VehicleInteractionDetails__offsets.get(vehicleID, None)
        if offset is None:
            self._VehicleInteractionDetails__vehicleIDs.append(vehicleID)
            offset = len(self._VehicleInteractionDetails__values)
            size = len(VEH_INTERACTION_DETAILS)
            self._VehicleInteractionDetails__values += [
                0] * size
            self._VehicleInteractionDetails__offsets[vehicleID] = offset
        
        return _VehicleInteractionDetailsItem(self._VehicleInteractionDetails__values, offset)

    
    def __contains__(self, vehicleID):
        return vehicleID in self._VehicleInteractionDetails__offsets

    
    def __str__(self):
        return str(self.toDict())

    
    def pack(self):
        count = len(self._VehicleInteractionDetails__vehicleIDs)
        size = len(VEH_INTERACTION_DETAILS)
        packed = struct.pack('%dI' % count, *self._VehicleInteractionDetails__vehicleIDs) + struct.pack(('%dH' % count) * size, *self._VehicleInteractionDetails__values)
        return packed

    
    def toDict(self):
        continue
        return _[1]([ (vehID, dict(_VehicleInteractionDetailsItem(self._VehicleInteractionDetails__values, offset))) for (vehID, offset) in self._VehicleInteractionDetails__offsets.iteritems() ])



