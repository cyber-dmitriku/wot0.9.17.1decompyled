# Source Generated with Decompyle++
# File: BattleDispatcherInterface.pyc (Python 2.6)

import AccountCommands
import BigWorld
from account_helpers.AccountPrebattle import AccountPrebattle
from account_helpers.AccountSettings import AccountSettings
from account_helpers import isDemonstrator
from adisp import process
import constants
import ArenaType
from CurrentVehicle import g_currentVehicle
from debug_utils import LOG_ERROR, LOG_DEBUG
from gui import SystemMessages, GUI_SETTINGS
from gui.Scaleform.ingame_help import IngameHelpLobbyDelegator
from gui.Scaleform.windows import UIInterface
from gui.Scaleform.utils.requesters import StatsRequester
from gui.Scaleform.utils.functions import makeTooltip, checkAmmoLevel
from helpers import i18n
from messenger import LAZY_CHANNELS
from messenger.gui import MessengerDispatcher
from PlayerEvents import g_playerEvents
from items.tankmen import getSkillsConfig
from items.vehicles import VehicleDescr
from items import vehicles

class BattleDispatcherInterface(UIInterface):
    
    def __init__(self):
        self._BattleDispatcherInterface__doTeamReady = False
        self._BattleDispatcherInterface__doTeamReadyForced = False
        self._BattleDispatcherInterface__totalVehicleLevels = 0
        self._BattleDispatcherInterface__maxLightVehicleLevels = 0
        self._BattleDispatcherInterface__maxMediumVehicleLevels = 0
        self._BattleDispatcherInterface__maxHeavyVehicleLevels = 0
        self._BattleDispatcherInterface__maxSPGVehicleLevels = 0
        self._BattleDispatcherInterface__maxATSPGVehicleLevels = 0
        self.ingameHelpDelegator = IngameHelpLobbyDelegator()

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self.uiHolder.addExternalCallbacks({
            'common.FightButtonClick': self.onFightButtonClick,
            'common.FightButtonSelectClick': self.onFightButtonSelectClick,
            'common.onConfirmSquadHaveNotReadyPlayers': self.onConfirmSquadHaveNotReadyPlayers,
            'common.onConfirmTeamHaveNotReadyPlayers': self.onConfirmCompanyHaveNotReadyPlayers })
        self.ingameHelpDelegator.populateUI(proxy)
        g_playerEvents.onEnqueued += self.pe_onEnqueued
        g_playerEvents.onEnqueueFailure += self.pe_onEnqueueFailure
        g_playerEvents.onKickedFromQueue += self.pe_onKickedFromQueue
        g_playerEvents.onPrebattleJoined += self.pe_onPrebattleJoined
        g_playerEvents.onPrebattleJoinFailure += self.pe_onPrebattleJoinFailure
        g_playerEvents.onPrebattleLeft += self.pe_onPrebattleLeft
        g_playerEvents.onKickedFromPrebattle += self.pe_onPrebattleLeft
        g_playerEvents.onPrebattleAutoInvitesChanged += self.updateFightButton
        self._BattleDispatcherInterface__validateVehicleLevelLimits()

    
    def dispossessUI(self):
        self.uiHolder.removeExternalCallbacks('common.FightButtonClick', 'common.FightButtonSelectClick', 'common.onConfirmSquadHaveNotReadyPlayers', 'common.onConfirmTeamHaveNotReadyPlayers')
        self.ingameHelpDelegator.dispossessUI()
        g_playerEvents.onEnqueued -= self.pe_onEnqueued
        g_playerEvents.onEnqueueFailure -= self.pe_onEnqueueFailure
        g_playerEvents.onKickedFromQueue -= self.pe_onKickedFromQueue
        g_playerEvents.onPrebattleJoined -= self.pe_onPrebattleJoined
        g_playerEvents.onPrebattleJoinFailure -= self.pe_onPrebattleJoinFailure
        g_playerEvents.onPrebattleLeft -= self.pe_onPrebattleLeft
        g_playerEvents.onKickedFromPrebattle -= self.pe_onPrebattleLeft
        g_playerEvents.onPrebattleAutoInvitesChanged -= self.updateFightButton
        MessengerDispatcher.g_instance.requestCreatePrb = None
        UIInterface.dispossessUI(self)

    
    def start(self, isInQueue = False):
        self.pe_onPrebattleJoined()
        self.prb_onPrebattleSettingsRecived()
        if isInQueue:
            self.pe_onEnqueued()
        
        self.updateDemonstratorButton()

    
    def onPageLoadInit(self, pageName):
        if pageName not in ('hangar', 'battleloading'):
            self.updateFightButton()
        

    
    def _BattleDispatcherInterface__getDisableTooltip(self):
        if not self._BattleDispatcherInterface__isValidLightVehicleMaxLevelLimits():
            (min, max) = AccountPrebattle.getClassLevelLimits('lightTank')
            return makeTooltip(i18n.makeString('#tooltips:redButton/disabled/vehicleLightLevelLimits/header'), i18n.makeString('#tooltips:redButton/disabled/vehicleLightLevelLimits/body', min, max))
        if not self._BattleDispatcherInterface__isValidMediumVehicleMaxLevelLimits():
            (min, max) = AccountPrebattle.getClassLevelLimits('mediumTank')
            return makeTooltip(i18n.makeString('#tooltips:redButton/disabled/vehicleMediumLevelLimits/header'), i18n.makeString('#tooltips:redButton/disabled/vehicleMediumLevelLimits/body', min, max))
        if not self._BattleDispatcherInterface__isValidHeavyVehicleMaxLevelLimits():
            (min, max) = AccountPrebattle.getClassLevelLimits('heavyTank')
            return makeTooltip(i18n.makeString('#tooltips:redButton/disabled/vehicleHeavyLevelLimits/header'), i18n.makeString('#tooltips:redButton/disabled/vehicleHeavyLevelLimits/body', min, max))
        if not self._BattleDispatcherInterface__isValidSPGVehicleMaxLevelLimits():
            (min, max) = AccountPrebattle.getClassLevelLimits('SPG')
            return makeTooltip(i18n.makeString('#tooltips:redButton/disabled/vehicleSPGLevelLimits/header'), i18n.makeString('#tooltips:redButton/disabled/vehicleSPGLevelLimits/body', min, max))
        if not self._BattleDispatcherInterface__isValidATSPGVehicleMaxLevelLimits():
            (min, max) = AccountPrebattle.getClassLevelLimits('AT-SPG')
            return makeTooltip(i18n.makeString('#tooltips:redButton/disabled/vehicleATSPGLevelLimits/header'), i18n.makeString('#tooltips:redButton/disabled/vehicleATSPGLevelLimits/body', min, max))
        if not self._BattleDispatcherInterface__isValidVehicleLevelLimits():
            (min, max) = (1, 150)
            if AccountPrebattle.getSettings() is not None:
                (min, max) = AccountPrebattle.getSettings().get('limit_total_level')
            
            return makeTooltip(i18n.makeString('#tooltips:redButton/disabled/vehicleTotalLevelLimits/header'), i18n.makeString('#tooltips:redButton/disabled/vehicleTotalLevelLimits/body', min, max))
        if g_currentVehicle.isReadyToFight():
            return None
        if not g_currentVehicle.isPresent():
            return '#tooltips:redButton/disabled/buyNeeded'
        if g_currentVehicle.isInBattle():
            return '#tooltips:redButton/disabled/vehicleLocked'
        if not g_currentVehicle.isCrewFull():
            crew_list = ''
            for index in xrange(len(g_currentVehicle.vehicle.crew)):
                if g_currentVehicle.vehicle.crew[index] is None:
                    if len(crew_list) != 0:
                        pass
                    1
                    ', ' += '' + i18n.makeString(getSkillsConfig()[g_currentVehicle.vehicle.descriptor.type.crewRoles[index][0]]['userString']).lower()
                    continue
            
            return makeTooltip('#tooltips:redButton/disabled/crewNotFull/header', i18n.makeString('#tooltips:redButton/disabled/crewNotFull/body') % crew_list)
        if g_currentVehicle.isBroken():
            return '#tooltips:redButton/disabled/repairNeeded'

    
    def updateDemonstratorButton(self):
        
        def getArenaNameSuffix(arenaType):
            if arenaType.gameplayName == 'ctf':
                return ''
            return ' - ' + i18n.makeString('#arenas:type/%s/name' % arenaType.gameplayName)

        yield StatsRequester().getAccountAttrs()
        accountAttrs = None
        maps = [
            isDemonstrator(accountAttrs),
            'demonstration']
        if maps[0]:
            continue
            arenas = [ (arenaType.name + getArenaNameSuffix(arenaType), arenaTypeID) for (arenaTypeID, arenaType) in ArenaType.g_cache.iteritems() ]
            arenas.sort()
            for arena in arenas:
                maps.append(arena[0])
                maps.append(arena[1])
            
        
        self.call('common.setDemonstratorButton', maps)

    updateDemonstratorButton = process(updateDemonstratorButton)
    
    def updateFightButton(self):
        isPrebattle = self.uiHolder.currentInterface == 'prebattle'
        isTraning = self.uiHolder.currentInterface == 'training'
        if not (not g_currentVehicle.isReadyToFight() or not AccountPrebattle.isMemberReady()) and isPrebattle and isTraning and not self._BattleDispatcherInterface__isValidVehicleLevelLimits():
            pass
        self.call('common.disableFightButton', [
            not self._BattleDispatcherInterface__isValidAllLevelLimits(),
            self._BattleDispatcherInterface__getDisableTooltip()])
        label = '#menu:headerButtons/battle'
        if (AccountPrebattle.isSquad() and AccountPrebattle.isCompany() or AccountPrebattle.isBattleSession()) and not AccountPrebattle.isCreator():
            if AccountPrebattle.isMemberReady():
                label = '#menu:headerButtons/notReady'
            else:
                label = '#menu:headerButtons/ready'
        
        menu = '#menu:headerButtons/battle/menu/standart'
        if AccountPrebattle.isSquad():
            menu = '#menu:headerButtons/battle/menu/squad'
        elif AccountPrebattle.isTraining():
            menu = '#menu:headerButtons/battle/menu/training'
        elif AccountPrebattle.isCompany():
            menu = '#menu:headerButtons/battle/menu/team'
        elif AccountPrebattle.isBattleSession():
            menu = '#menu:headerButtons/battle/menu/battle_session'
        
        fightTypes = [
            label,
            menu]
        fightTypes.append('#menu:headerButtons/battle/types/standart')
        fightTypes.append('standart')
        fightTypes.append(AccountPrebattle.get() is not None)
        fightTypes.append('#tooltips:battleTypes/standart')
        if not AccountPrebattle.isSquad():
            fightTypes.append('#menu:headerButtons/battle/types/squad')
            fightTypes.append('squad')
            fightTypes.append(AccountPrebattle.get() is not None)
            fightTypes.append('#tooltips:battleTypes/squad')
        elif AccountPrebattle.isCreator():
            pass
        
        None(None % '')
        fightTypes.append('prebattleLeave')
        fightTypes.append(False)
        fightTypes.append(None)
        fightTypes.append('#menu:headerButtons/battle/types/training')
        fightTypes.append('training')
        if not AccountPrebattle.get() is None:
            pass
        fightTypes.append(not AccountPrebattle.isTraining())
        fightTypes.append('#tooltips:battleTypes/training')
        fightTypes.append('#menu:headerButtons/battle/types/company')
        fightTypes.append('company')
        fightTypes.append(False)
        fightTypes.append('#tooltips:battleTypes/company')
        hiddenSpecPrebattles = True
        if GUI_SETTINGS.specPrebatlesVisible:
            hiddenSpecPrebattles = not getattr(BigWorld.player(), 'prebattleAutoInvites', None)
            fightTypes.append('#menu:headerButtons/battle/types/spec')
            fightTypes.append('spec')
            fightTypes.append(hiddenSpecPrebattles)
            fightTypes.append('#tooltips:battleTypes/spec')
        
        messenger = MessengerDispatcher.g_instance
        cid = messenger.channels.setIsLazyChannelHidden(LAZY_CHANNELS.SPECIAL_BATTLES[0], hiddenSpecPrebattles)
        if cid is not None:
            if hiddenSpecPrebattles:
                messenger.currentWindow.getChannelPage(cid).close()
            
            messenger.currentWindow.refreshChannelList()
        
        self.call('common.setFightButton', fightTypes)
        self.uiHolder.updateTankParams()

    
    def __processTraining(self):
        yield checkAmmoLevel()
        result = None
        if result:
            self.uiHolder.movie.invoke(('loadTraining',))
        

    _BattleDispatcherInterface__processTraining = process(__processTraining)
    
    def _BattleDispatcherInterface__processSpecList(self):
        self._BattleDispatcherInterface__openPrebattleChannelPage(LAZY_CHANNELS.SPECIAL_BATTLES)

    
    def _BattleDispatcherInterface__processSpec(self, confirm = False):
        if AccountPrebattle.isBattleSession():
            self._BattleDispatcherInterface__setReadyMemberStatus(True, 'battleSession')
        

    
    def _BattleDispatcherInterface__setReadyMemberStatus(self, isReady, prbType, isForced = False):
        if isReady:
            if not AccountPrebattle.isMemberReady():
                
                def setMemberReady():
                    yield checkAmmoLevel()
                    result = None
                    if result:
                        AccountPrebattle.setMemdberReady()
                        if AccountPrebattle.isCreator():
                            self._BattleDispatcherInterface__doTeamReady = True
                            self._BattleDispatcherInterface__doTeamReadyForced = isForced
                        
                    

                setMemberReady = (None, process)(setMemberReady)
                if self.uiHolder.captcha.isCaptchaRequired():
                    self.uiHolder.captcha.showCaptcha(setMemberReady)
                else:
                    setMemberReady()
            elif AccountPrebattle.isCreator():
                self._BattleDispatcherInterface__setReadyTeam(prbType, isForced)
            
        elif AccountPrebattle.isMemberReady():
            None((BigWorld.player().prb_notReady, constants.PREBATTLE_ACCOUNT_STATE.NOT_READY), (lambda code: self.onPrebattleReadyResponse(code, prbType, 'member')))
        

    
    def _BattleDispatcherInterface__setReadyTeam(self, prbType, isForced = False):
        if AccountPrebattle.isCreator() and AccountPrebattle.isMemberReady():
            
            def doTeamReady():
                None(None, (BigWorld.player().prb_teamReady, AccountPrebattle.getMemberTeam(), isForced), (lambda code: self.onPrebattleReadyResponse(code, prbType, 'team', isForced)))

            if self.uiHolder.captcha.isCaptchaRequired():
                self.uiHolder.captcha.showCaptcha(doTeamReady)
            else:
                doTeamReady()
        

    
    def _BattleDispatcherInterface__processCompanyList(self):
        self._BattleDispatcherInterface__openPrebattleChannelPage(LAZY_CHANNELS.COMPANIES)

    
    def _BattleDispatcherInterface__processCompany(self, confirm = False):
        if AccountPrebattle.isCompany():
            if AccountPrebattle.isCreator():
                if AccountPrebattle.getMemberRoster() != AccountPrebattle.TEAM_ROSTERSID[0]:
                    self.call('common.showMessageDialog', [
                        'teamDoesNotHaveCommander',
                        False,
                        False])
                    return None
                if not self._BattleDispatcherInterface__isValidVehicleLevelLimits():
                    settings = AccountPrebattle.getSettings()
                    (minTL, maxTL) = (1, 150)
                    if settings is not None:
                        (minTL, maxTL) = settings.get('limit_total_level', (1, 150))
                    
                    message = i18n.makeString('#dialogs:teamLevelLimitation/messageEx', current = self._BattleDispatcherInterface__totalVehicleLevels, min = minTL, max = maxTL)
                    self.call('common.showMessageDialog', [
                        'teamLevelLimitation',
                        False,
                        False,
                        message])
                    return None
                if not confirm:
                    (notReadyCount, _, playerCount, limitMaxCount) = AccountPrebattle.getPlayersReadyStat(AccountPrebattle.TEAM_ROSTERSID[0])
                    if not AccountPrebattle.isMemberReady():
                        pass
                    1
                    creatorWeight = 0
                    if playerCount - notReadyCount < limitMaxCount - creatorWeight:
                        message = i18n.makeString('#dialogs:teamHaveNotReadyPlayers/messageEx', playerCount - notReadyCount)
                        self.call('common.showMessageDialog', [
                            'teamHaveNotReadyPlayers',
                            True,
                            True,
                            message,
                            'common.onConfirmTeamHaveNotReadyPlayers'])
                        return None
                
            
            self._BattleDispatcherInterface__setReadyMemberStatus(True, 'team', confirm)
        

    
    def _BattleDispatcherInterface__processSquad(self, confirm = False):
        if not AccountPrebattle.isSquad():
            if self.uiHolder.captcha.isCaptchaRequired():
                self.uiHolder.captcha.showCaptcha(self._BattleDispatcherInterface__doCreateSquad)
            else:
                self._BattleDispatcherInterface__doCreateSquad()
        elif AccountPrebattle.isCreator() and not confirm:
            (notReadyCount, haveInBattle, playerCount, _) = AccountPrebattle.getPlayersReadyStat(AccountPrebattle.SUQAD_ROSTERID)
            if haveInBattle:
                self.call('common.showMessageDialog', [
                    'squadHavePlayersInBattle',
                    True,
                    False])
                return None
            if not AccountPrebattle.isMemberReady():
                notReadyCount -= 1
            
            if notReadyCount > 0:
                message = i18n.makeString('#dialogs:squadHaveNotReadyPlayers/messageEx', notReadyCount, playerCount)
                self.call('common.showMessageDialog', [
                    'squadHaveNotReadyPlayers',
                    True,
                    True,
                    message,
                    'common.onConfirmSquadHaveNotReadyPlayers'])
                return None
        
        self._BattleDispatcherInterface__setReadyMemberStatus(True, 'squad', confirm)

    
    def _BattleDispatcherInterface__doCreateSquad(self):
        MessengerDispatcher.g_instance.requestCreatePrb = constants.PREBATTLE_TYPE.SQUAD
        BigWorld.player().prb_createSquad()

    
    def _BattleDispatcherInterface__calculateTotalVehicleLevels(self):
        totalLevel = 0
        prebattle = AccountPrebattle.get()
        if prebattle is None:
            return None
        self._BattleDispatcherInterface__maxLightVehicleLevels = 0
        self._BattleDispatcherInterface__maxMediumVehicleLevels = 0
        self._BattleDispatcherInterface__maxHeavyVehicleLevels = 0
        self._BattleDispatcherInterface__maxSPGVehicleLevels = 0
        self._BattleDispatcherInterface__maxATSPGVehicleLevels = 0
        for player in prebattle.rosters.get(AccountPrebattle.getMemberTeam(), { }).values():
            vehCompDescr = player.get('vehCompDescr', '')
            if len(vehCompDescr) > 0:
                vd = VehicleDescr(compactDescr = vehCompDescr)
                level = vd.type.level
                totalLevel += level
                if 'lightTank' in vehicles.VEHICLE_CLASS_TAGS.intersection(vd.type.tags):
                    self._BattleDispatcherInterface__maxLightVehicleLevels = max(self._BattleDispatcherInterface__maxLightVehicleLevels, level)
                elif 'mediumTank' in vehicles.VEHICLE_CLASS_TAGS.intersection(vd.type.tags):
                    self._BattleDispatcherInterface__maxMediumVehicleLevels = max(self._BattleDispatcherInterface__maxMediumVehicleLevels, level)
                elif 'heavyTank' in vehicles.VEHICLE_CLASS_TAGS.intersection(vd.type.tags):
                    self._BattleDispatcherInterface__maxHeavyVehicleLevels = max(self._BattleDispatcherInterface__maxHeavyVehicleLevels, level)
                elif 'SPG' in vehicles.VEHICLE_CLASS_TAGS.intersection(vd.type.tags):
                    self._BattleDispatcherInterface__maxSPGVehicleLevels = max(self._BattleDispatcherInterface__maxSPGVehicleLevels, level)
                elif 'AT-SPG' in vehicles.VEHICLE_CLASS_TAGS.intersection(vd.type.tags):
                    self._BattleDispatcherInterface__maxATSPGVehicleLevels = max(self._BattleDispatcherInterface__maxATSPGVehicleLevels, level)
                
            'lightTank' in vehicles.VEHICLE_CLASS_TAGS.intersection(vd.type.tags)
        
        self._BattleDispatcherInterface__totalVehicleLevels = totalLevel

    
    def _BattleDispatcherInterface__isValidVehicleLevelLimits(self):
        if AccountPrebattle.isCreator():
            pass
        checkLevels = AccountPrebattle.isCompany()
        settings = AccountPrebattle.getSettings()
        (min, max) = (1, 150)
        if settings is not None:
            (min, max) = settings.get('limit_total_level', (1, 150))
        
        if checkLevels:
            if min <= self._BattleDispatcherInterface__totalVehicleLevels:
                pass
            self._BattleDispatcherInterface__totalVehicleLevels <= max
            if not 1:
                pass
        return not checkLevels

    
    def _BattleDispatcherInterface__isValidLightVehicleMaxLevelLimits(self):
        if AccountPrebattle.isCreator():
            pass
        checkLevels = AccountPrebattle.isCompany()
        (min, max) = AccountPrebattle.getClassLevelLimits('lightTank')
        if checkLevels:
            if min <= self._BattleDispatcherInterface__maxLightVehicleLevels:
                pass
            self._BattleDispatcherInterface__maxLightVehicleLevels <= max
            if not 1 and self._BattleDispatcherInterface__maxLightVehicleLevels == 0:
                pass
        return not checkLevels

    
    def _BattleDispatcherInterface__isValidMediumVehicleMaxLevelLimits(self):
        if AccountPrebattle.isCreator():
            pass
        checkLevels = AccountPrebattle.isCompany()
        (min, max) = AccountPrebattle.getClassLevelLimits('mediumTank')
        if checkLevels:
            if min <= self._BattleDispatcherInterface__maxMediumVehicleLevels:
                pass
            self._BattleDispatcherInterface__maxMediumVehicleLevels <= max
            if not 1 and self._BattleDispatcherInterface__maxMediumVehicleLevels == 0:
                pass
        return not checkLevels

    
    def _BattleDispatcherInterface__isValidHeavyVehicleMaxLevelLimits(self):
        if AccountPrebattle.isCreator():
            pass
        checkLevels = AccountPrebattle.isCompany()
        (min, max) = AccountPrebattle.getClassLevelLimits('heavyTank')
        if checkLevels:
            if min <= self._BattleDispatcherInterface__maxHeavyVehicleLevels:
                pass
            self._BattleDispatcherInterface__maxHeavyVehicleLevels <= max
            if not 1 and self._BattleDispatcherInterface__maxHeavyVehicleLevels == 0:
                pass
        return not checkLevels

    
    def _BattleDispatcherInterface__isValidSPGVehicleMaxLevelLimits(self):
        if AccountPrebattle.isCreator():
            pass
        checkLevels = AccountPrebattle.isCompany()
        (min, max) = AccountPrebattle.getClassLevelLimits('SPG')
        if checkLevels:
            if min <= self._BattleDispatcherInterface__maxSPGVehicleLevels:
                pass
            self._BattleDispatcherInterface__maxSPGVehicleLevels <= max
            if not 1 and self._BattleDispatcherInterface__maxSPGVehicleLevels == 0:
                pass
        return not checkLevels

    
    def _BattleDispatcherInterface__isValidATSPGVehicleMaxLevelLimits(self):
        if AccountPrebattle.isCreator():
            pass
        checkLevels = AccountPrebattle.isCompany()
        (min, max) = AccountPrebattle.getClassLevelLimits('AT-SPG')
        if checkLevels:
            if min <= self._BattleDispatcherInterface__maxATSPGVehicleLevels:
                pass
            self._BattleDispatcherInterface__maxATSPGVehicleLevels <= max
            if not 1 and self._BattleDispatcherInterface__maxATSPGVehicleLevels == 0:
                pass
        return not checkLevels

    
    def _BattleDispatcherInterface__isValidAllLevelLimits(self):
        if self._BattleDispatcherInterface__isValidLightVehicleMaxLevelLimits() and self._BattleDispatcherInterface__isValidMediumVehicleMaxLevelLimits() and self._BattleDispatcherInterface__isValidHeavyVehicleMaxLevelLimits() and self._BattleDispatcherInterface__isValidSPGVehicleMaxLevelLimits():
            pass
        return self._BattleDispatcherInterface__isValidATSPGVehicleMaxLevelLimits()

    
    def _BattleDispatcherInterface__validateVehicleLevelLimits(self):
        if not AccountPrebattle.isCompany():
            return None
        prevValue = self._BattleDispatcherInterface__totalVehicleLevels
        prevMaxLightValue = self._BattleDispatcherInterface__maxLightVehicleLevels
        prevMaxMediumValue = self._BattleDispatcherInterface__maxMediumVehicleLevels
        prevMaxHeavyValue = self._BattleDispatcherInterface__maxHeavyVehicleLevels
        prevMaxSPGValue = self._BattleDispatcherInterface__maxSPGVehicleLevels
        prevMaxATSPGValue = self._BattleDispatcherInterface__maxATSPGVehicleLevels
        self._BattleDispatcherInterface__calculateTotalVehicleLevels()
        if prevValue != self._BattleDispatcherInterface__totalVehicleLevels and prevMaxLightValue != self._BattleDispatcherInterface__maxLightVehicleLevels and prevMaxMediumValue != self._BattleDispatcherInterface__maxMediumVehicleLevels and prevMaxHeavyValue != self._BattleDispatcherInterface__maxHeavyVehicleLevels and prevMaxSPGValue != self._BattleDispatcherInterface__maxSPGVehicleLevels or prevMaxATSPGValue != self._BattleDispatcherInterface__maxATSPGVehicleLevels:
            self.updateFightButton()
        

    
    def _BattleDispatcherInterface__openPrebattleChannelPage(self, info):
        messenger = MessengerDispatcher.g_instance
        cid = messenger.channels.getLazyChannelIdByClientIdx(info[0])
        if cid is not None:
            messenger.currentWindow.getChannelPage(cid).open()
        

    
    def pe_onEnqueued(self):
        self.uiHolder.movie.invoke(('loadPrebattle',))

    
    def pe_onEnqueueFailure(self, errorCode, errorStr):
        error = constants.JOIN_FAILURE_NAMES[errorCode]
        message = '#system_messages:arena_start_errors/join/%s' % error
        SystemMessages.pushI18nMessage(message, type = SystemMessages.SM_TYPE.Error)

    
    def pe_onKickedFromQueue(self):
        SystemMessages.pushI18nMessage('#system_messages:arena_start_errors/kick/timeout', type = SystemMessages.SM_TYPE.Warning)

    
    def pe_onPrebattleJoined(self):
        prebattle = AccountPrebattle.get()
        if prebattle is not None:
            prebattle.onSettingsReceived += self.prb_onPrebattleSettingsRecived
            prebattle.onSettingUpdated += self.prb_onPrebattleSettingsRecived
            prebattle.onRosterReceived += self.prb_onPrebattleRosterRecived
            prebattle.onTeamStatesReceived += self.prb_onTeamStateChanged
            prebattle.onPlayerStateChanged += self.prb_onPlayerStateChanged
            prebattle.onPlayerRosterChanged += self.prb_onPlayerRosterChanged
            prebattle.onPlayerAdded += self.prb_onPlayerAdded
            prebattle.onPlayerRemoved += self.prb_onPlayerRemoved
            prebattle.onKickedFromQueue += self.prb_onKickedFromQueue
        

    
    def pe_onPrebattleJoinFailure(self, errorCode):
        error = constants.JOIN_FAILURE_NAMES[errorCode]
        message = '#system_messages:arena_start_errors/join/%s' % error
        SystemMessages.pushI18nMessage(message, type = SystemMessages.SM_TYPE.Error)
        self.updateFightButton()

    
    def pe_onPrebattleLeft(self, code = None):
        self._BattleDispatcherInterface__totalVehicleLevels = 0
        self._BattleDispatcherInterface__maxLightVehicleLevels = 0
        self._BattleDispatcherInterface__maxMediumVehicleLevels = 0
        self._BattleDispatcherInterface__maxHeavyVehicleLevels = 0
        self._BattleDispatcherInterface__maxSPGVehicleLevels = 0
        self._BattleDispatcherInterface__maxATSPGVehicleLevels = 0
        prebattle = AccountPrebattle.get()
        if prebattle:
            prebattle.onSettingsReceived -= self.prb_onPrebattleSettingsRecived
            prebattle.onSettingUpdated -= self.prb_onPrebattleSettingsRecived
            prebattle.onRosterReceived -= self.prb_onPrebattleRosterRecived
            prebattle.onTeamStatesReceived -= self.prb_onTeamStateChanged
            prebattle.onPlayerStateChanged -= self.prb_onPlayerStateChanged
            prebattle.onPlayerRosterChanged -= self.prb_onPlayerRosterChanged
            prebattle.onPlayerAdded -= self.prb_onPlayerAdded
            prebattle.onPlayerRemoved -= self.prb_onPlayerRemoved
            prebattle.onKickedFromQueue -= self.prb_onKickedFromQueue
        
        (msg, msgLvl) = g_currentVehicle.getHangarMessage()
        self.call('hangar.readyToFight', [
            g_currentVehicle.isReadyToFight(),
            msg,
            msgLvl,
            g_currentVehicle.isPresent(),
            AccountPrebattle.isMemberReady(),
            g_currentVehicle.isCrewFull()])
        self.updateFightButton()

    
    def prb_onPrebattleSettingsRecived(self, name = ''):
        if AccountPrebattle.isSquad() and AccountPrebattle.isCompany() or AccountPrebattle.isBattleSession():
            if AccountPrebattle.isMemberReady() and AccountPrebattle.isTeamReady():
                self.uiHolder.movie.invoke(('loadPrebattle',))
            
        elif AccountPrebattle.isTraining():
            if (g_currentVehicle.isReadyToFight() or AccountPrebattle.isMemberReady()) and not len(name):
                self.uiHolder.movie.invoke(('loadTraining',))
            
        
        if name in ('limit_total_level', 'limit_level', 'limit_class_level'):
            self._BattleDispatcherInterface__calculateTotalVehicleLevels()
            self.updateFightButton()
        

    
    def prb_onPrebattleRosterRecived(self):
        self._BattleDispatcherInterface__validateVehicleLevelLimits()
        self.updateFightButton()

    
    def prb_onTeamStateChanged(self):
        if AccountPrebattle.isSquad() and AccountPrebattle.isCompany() or AccountPrebattle.isBattleSession():
            if AccountPrebattle.isMemberReady() or AccountPrebattle.isCreator():
                if AccountPrebattle.isTeamReady() and AccountPrebattle.isMemberInKeyStaff():
                    self.pe_onEnqueued()
                else:
                    self.uiHolder.movie.invoke(('loadHangar',))
            
        
        self.updateFightButton()

    
    def prb_onPlayerStateChanged(self, id, roster):
        self._BattleDispatcherInterface__validateVehicleLevelLimits()
        yield StatsRequester().getVehicleTypeLocks()
        vehicleTypeLocks = None
        yield StatsRequester().getGlobalVehicleLocks()
        globalVehicleLocks = None
        clanLock = None
        if g_currentVehicle.isPresent():
            clanDamageLock = vehicleTypeLocks.get(g_currentVehicle.vehicle.descriptor.type.compactDescr, { }).get(1, None)
            clanNewbeLock = globalVehicleLocks.get(1, None)
            if not clanDamageLock:
                pass
            clanLock = clanNewbeLock
        
        if AccountPrebattle.isSquad() and AccountPrebattle.isCompany() or AccountPrebattle.isBattleSession():
            if AccountPrebattle.isSquad():
                pass
            1
            prebattleType = 'company'
            if BigWorld.player().id == id:
                self.updateFightButton()
                ready = AccountPrebattle.isMemberReady()
                (msg, msgLvl) = g_currentVehicle.getHangarMessage()
                self.call('hangar.readyToFight', [
                    g_currentVehicle.isReadyToFight(),
                    msg,
                    msgLvl,
                    g_currentVehicle.isPresent(),
                    ready,
                    g_currentVehicle.isCrewFull()])
                if AccountPrebattle.isCreator() and AccountPrebattle.isMemberReady() and self._BattleDispatcherInterface__doTeamReady:
                    self._BattleDispatcherInterface__setReadyTeam(prebattleType, self._BattleDispatcherInterface__doTeamReadyForced)
                    self._BattleDispatcherInterface__doTeamReady = False
                    self._BattleDispatcherInterface__doTeamReadyForced = False
                
            
        

    prb_onPlayerStateChanged = process(prb_onPlayerStateChanged)
    
    def prb_onPlayerRosterChanged(self, id, prevRoster, roster, actorID):
        self._BattleDispatcherInterface__validateVehicleLevelLimits()

    
    def prb_onPlayerAdded(self, id, roster):
        self._BattleDispatcherInterface__validateVehicleLevelLimits()

    
    def prb_onPlayerRemoved(self, id, roster, name):
        self._BattleDispatcherInterface__validateVehicleLevelLimits()

    
    def prb_onKickedFromQueue(self, *args):
        if AccountPrebattle.isSquad() and AccountPrebattle.isCompany() or AccountPrebattle.isBattleSession():
            SystemMessages.pushI18nMessage('#system_messages:squad/kickedFromQueue', type = SystemMessages.SM_TYPE.Warning)
        

    
    def onPrebattleReadyResponse(self, code, prebattleType, playerType, isForced = False):
        if code == AccountCommands.RES_FAILURE and playerType == 'member':
            SystemMessages.pushI18nMessage('#system_messages:%s/notSetReadyStatus' % prebattleType, type = SystemMessages.SM_TYPE.Warning)
        elif code < 0 and playerType == 'team' and not isForced:
            self._BattleDispatcherInterface__processCompany()
        elif code < 0 and playerType == 'squad' and not isForced:
            self._BattleDispatcherInterface__processSquad()
        elif code < 0:
            LOG_ERROR('Server return error for %s %s ready request: responseCode=%s' % (prebattleType, playerType, code))
        

    
    def onPrebattleLeaveResponse(self, code):
        if code < 0:
            LOG_ERROR('Server return error for prebattle leave request: responseCode=%s' % code)
        

    
    def onFightButtonSelectClick(self, callbackId, queueType):
        self.onFightButtonClick(callbackId, None, queueType)

    
    def onFightButtonClick(self, callbackId, mapId = None, queueType = 0, confirm = False):
        MessengerDispatcher.g_instance.requestCreatePrb = None
        if not g_currentVehicle.isPresent():
            SystemMessages.pushI18nMessage('#menu:hangar/no_current_vehicle_selected', type = SystemMessages.SM_TYPE.Error)
            return None
        if queueType == 'prebattleLeave':
            BigWorld.player().prb_leave(self.onPrebattleLeaveResponse)
            return None
        if queueType == 'company':
            self._BattleDispatcherInterface__processCompanyList()
            return None
        if queueType == 'spec':
            self._BattleDispatcherInterface__processSpecList()
            return None
        if not g_currentVehicle.isLocked() and not g_currentVehicle.isBroken():
            if queueType == 'training' or AccountPrebattle.isTraining():
                self._BattleDispatcherInterface__processTraining()
                return None
            if AccountPrebattle.isCompany():
                self._BattleDispatcherInterface__processCompany()
                return None
            if AccountPrebattle.isBattleSession():
                self._BattleDispatcherInterface__processSpec()
                return None
            if queueType == 'squad' or AccountPrebattle.isSquad():
                self._BattleDispatcherInterface__processSquad()
                return None
            
            def enqueueForArena(mapId):
                if mapId:
                    mapId = int(mapId)
                    LOG_DEBUG('Demonstrator mapID: %s' % ArenaType.g_cache[mapId].geometryName)
                else:
                    mapId = -1
                yield checkAmmoLevel()
                result = None
                if result:
                    gameplayMask = AccountSettings.getSettings('gameplayMask')
                    invID = g_currentVehicle.vehicle.inventoryId
                    BigWorld.player().enqueueForArena(invID, gameplaysMask = gameplayMask, arenaTypeID = mapId)
                    LOG_DEBUG('Player joined to enqueue (invID, gameplayMask, mapID) =', invID, gameplayMask, mapId)
                

            enqueueForArena = process(enqueueForArena)
            if self.uiHolder.captcha.isCaptchaRequired():
                (AccountPrebattle.isSquad(), self.uiHolder.captcha.showCaptcha)((lambda : enqueueForArena(mapId)))
            elif self.ingameHelpDelegator.isRequiredToShow():
                (AccountPrebattle.isSquad(), self.ingameHelpDelegator.showIngameHelp)((lambda : enqueueForArena(mapId)))
            else:
                enqueueForArena(mapId)
        elif AccountPrebattle.get():
            if AccountPrebattle.isCreator():
                if AccountPrebattle.isSquad():
                    self._BattleDispatcherInterface__processSquad()
                
                if AccountPrebattle.isCompany():
                    self._BattleDispatcherInterface__processCompany()
                
                return None
            if AccountPrebattle.isMemberReady():
                if AccountPrebattle.isSquad():
                    pass
                1
                prebattleType = 'company'
                self._BattleDispatcherInterface__setReadyMemberStatus(False, prebattleType)
                return None
        
        SystemMessages.pushI18nMessage('#menu:hangar/vehicle_locked', type = SystemMessages.SM_TYPE.Error)

    
    def onConfirmSquadHaveNotReadyPlayers(self, callbackId):
        self._BattleDispatcherInterface__processSquad(confirm = True)

    
    def onConfirmCompanyHaveNotReadyPlayers(self, callbackId):
        self._BattleDispatcherInterface__processCompany(confirm = True)



