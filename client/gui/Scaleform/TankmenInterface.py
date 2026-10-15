# Source Generated with Decompyle++
# File: TankmenInterface.pyc (Python 2.6)

import BigWorld
from CurrentVehicle import g_currentVehicle
from helpers.i18n import makeString
from adisp import async, process
from gui import SystemMessages
from items.tankmen import getSkillsConfig, MAX_SKILL_LEVEL, SKILLS_BY_ROLES, PERKS, COMMON_SKILLS, ACTIVE_SKILLS
from items import vehicles, tankmen
from items.tankmen import TankmanDescr
from helpers.i18n import convert
from gui.Scaleform.windows import UIInterface
from gui.Scaleform.Waiting import Waiting
from gui.Scaleform.utils.requesters import Requester, StatsRequester
from gui.Scaleform.utils.gui_items import formatTankmanPrice, getItemByCompact, getTankmanOpertnSysMessageType
from gui.Scaleform.utils.functions import getShortDescr
from AccountCommands import LOCK_REASON
from account_helpers.AccountPrebattle import AccountPrebattle
from account_helpers.AccountSettings import AccountSettings
from gui.Scaleform.utils.dossiers_utils import getDossierMedals
from constants import DOSSIER_TYPE
from debug_utils import *

class TankmenInterface(UIInterface):
    TANKMEN_ORDER = {
        'commander': 0,
        'gunner': 1,
        'driver': 2,
        'radioman': 3,
        'loader': 4 }
    STATS_BLOCKS = {
        'tankman': (('common', ('battlesCount',)), ('studying', ('nextSkillXPLeft', 'avgExperience', 'nextSkillBattlesLeft'))),
        'medals': ('warrior', 'invader', 'sniper', 'defender', 'steelwall', 'supporter', 'scout', 'medalWittmann', 'medalOrlik', 'medalOskin', 'medalHalonen', 'medalBurda', 'medalBillotte', 'medalKolobanov', 'medalFadin') }
    
    def __init__(self, creator):
        UIInterface.__init__(self)
        self.creator = creator

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self.uiHolder.addExternalCallbacks({
            'tankmen.buyTankman': self.onBuyTankman,
            'tankmen.equipTankman': self.onEquipTankman,
            'tankmen.unloadTankman': self.onUnloadTankman,
            'tankmen.unloadAllTankman': self.onUnloadAllTankman,
            'tankmen.dismissTankman': self.onDismissTankman,
            'tankmen.retrainingTankman': self.onRetrainingTankman,
            'tankmen.updateVehicleClassDropdown': self.updateVehicleClassDropdown,
            'tankmen.updateVehicleTypeDropdown': self.updateVehicleTypeDropdown,
            'tankmen.updateRoleDropdown': self.updateRoleDropdown,
            'tankmen.updateSkillsList': self.onUpdateSkillsList,
            'tankmen.showRecruitWindow': self.onShowRecruitWindow,
            'tankmen.addSkill': self.onAddSkill,
            'tankmen.dropSkills': self.onDropSkills,
            'tankmen.getPersonalCase': self.onGetPersonalCase,
            'tankmen.populateRetrainingWindow': self.onPopulateRetrainingWindow,
            'tankmen.getTankmanStats': self.onGetTankmanStats,
            'tankmen.getTankmanDocs': self.onGetTankmanDocs,
            'tankmen.replaceTankman': self.onReplaceTankman,
            'tankmen.getSkillDropWindow': self.onGetSkillDropWindow,
            'tankmen.calcSkillDropWindow': self.onCalcSkillDropWindow,
            'tankmen.getTeachingSkillWindow': self.onGetTeachingSkillWindow,
            'tankmen.convertFreeXpToSkill': self.onConvertFreeXpToSkill,
            'tankmen.calcFreeXpForSkill': self.onCalcFreeXpForSkill })
        Waiting.hide('loadPage')

    
    def dispossessUI(self):
        self.uiHolder.removeExternalCallbacks('tankmen.buyTankman', 'tankmen.equipTankman', 'tankmen.unloadTankman', 'tankmen.unloadAllTankman', 'tankmen.dismissTankman', 'tankmen.retrainingTankman', 'tankmen.updateVehicleClassDropdown', 'tankmen.updateVehicleTypeDropdown', 'tankmen.updateRoleDropdown', 'tankmen.showRecruitWindow', 'tankmen.updateSkillsList', 'tankmen.addSkill', 'tankmen.dropSkills', 'tankmen.getPersonalCase', 'tankmen.populateRetrainingWindow', 'tankmen.getTankmanStats', 'tankmen.getTankmanDocs', 'tankmen.replaceTankman', 'tankmen.getSkillDropWindow', 'tankmen.calcSkillDropWindow', 'tankmen.getTeachingSkillWindow', 'tankmen.convertFreeXpTo
