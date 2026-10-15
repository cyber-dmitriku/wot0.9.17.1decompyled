# Source Generated with Decompyle++
# File: Profile.pyc (Python 2.6)

import BigWorld
import constants
from adisp import process
from gui.Scaleform.windows import UIInterface
from gui.Scaleform.utils.requesters import StatsRequester
from gui.Scaleform.utils import dossiers_utils
from PlayerEvents import g_playerEvents
from gui.Scaleform.Waiting import Waiting
from gui.ClientUpdateManager import g_clientUpdateManager
from gui.Scaleform.utils.RareAchievementsCache import g_rareAchievesCache
from debug_utils import *

class Profile(UIInterface):
    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self.uiHolder.movie.backgroundAlpha = 0
        self.uiHolder.movie.wg_inputKeyMode = 1
        self.uiHolder.addExternalCallbacks({
            'profile.getStat': self.getStat,
            'profile.getStatsList': self.getStatsList })
        g_clientUpdateManager.addCallbacks({
            '': self.onValuesUpdate,
            'stats.dossier': self.onDossierUpdate })
        g_playerEvents.onDossiersResync += self.onValuesUpdate
        g_rareAchievesCache.onTextReceived += self.onRareDataReceived
        g_rareAchievesCache.onImageReceived += self.onRareDataReceived
        self.onValuesUpdate()

    
    def dispossessUI(self):
        self.uiHolder.removeExternalCallbacks('profile.getStat', 'profile.getStatsList')
        g_clientUpdateManager.removeObjectCallbacks(self)
        g_rareAchievesCache.onImageReceived -= self.onRareDataReceived
        g_rareAchievesCache.onTextReceived -= self.onRareDataReceived
        g_playerEvents.onDossiersResync -= self.onValuesUpdate
        UIInterface.dispossessUI(self)

    
    def onRareDataReceived(self, id, *args):
        self.getStat(-1, 'ALL')

    
    def onValuesUpdate(self, *args):
        self._Profile__updateStatsList()
        Waiting.hide('loadPage')

    
    def onDossierUpdate(self, dossier):
        self.getStat(-1, 'ALL')

    
    def getStatsList(self, cid):
        yield StatsRequester().getAccountDossier()
        dossier = None
        self.call('profile.setStatsList', dossiers_utils.getDossierVehicleList(dossier))

    getStatsList = process(getStatsList)
    
    def __updateStatsList(self):
        self.uiHolder.updateAccountInfo()
        Waiting.show('loadStats')
        yield StatsRequester().getAccountDossier()
        dossier = None
        yield StatsRequester().getClanInfo()
        clanInfo = None
        yield StatsRequester().getClanDBID()
        clanDBID = None
        g_rareAchievesCache.request(dossier['rareAchievements'])
        self.call('profile.setCommonInfo', dossiers_utils.getCommonInfo(BigWorld.player().name, dossier, clanInfo, None))
        Waiting.hide('loadStats')
        if clanDBID is not None and clanDBID != 0:
            tID = 'userInfoId' + BigWorld.player().name
            yield dossiers_utils.getClanEmblemTextureID(clanDBID, True, tID)
            success = None
            if success:
                self.call('profile.setClanEmblem', [
                    tID])
            
        

    _Profile__updateStatsList = process(__updateStatsList)
    
    def getStat(self, callBackId, vehTypeId):
        Waiting.show('loadStats')
        yield StatsRequester().getUnlocks()
        unlocks = None
        if vehTypeId == 'ALL':
            yield StatsRequester().getAccountDossier()
            dossier = None
            data = dossiers_utils.getDossierTotalBlocks(dossier)
            medals = dossiers_utils.getDossierMedals(dossier, constants.DOSSIER_TYPE.ACCOUNT, unlocks)
        else:
            yield StatsRequester().getVehicleDossier(vehTypeId)
            dossier = None
            data = dossiers_utils.getDossierVehicleBlocks(dossier, vehTypeId)
            medals = dossiers_utils.getDossierMedals(dossier, constants.DOSSIER_TYPE.VEHICLE, unlocks)
        self.call('profile.setMedals', medals)
        self.call('profile.setStat', data)
        Waiting.hide('loadStats')

    getStat = process(getStat)


