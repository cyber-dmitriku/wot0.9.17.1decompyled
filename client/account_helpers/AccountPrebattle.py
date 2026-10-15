# Source Generated with Decompyle++
# File: AccountPrebattle.pyc (Python 2.6)

import BigWorld
import constants
from items import vehicles
from adisp import process, async
from debug_utils import LOG_ERROR
from gui import SystemMessages
from PlayerEvents import g_playerEvents

class AccountPrebattle:
    ROSTERS = (1, 17, 2, 18)
    ROSTERS2TEAMS = {
        1: (1, False),
        17: (1, True),
        2: (2, False),
        18: (2, True) }
    SUQAD_ROSTERID = 1
    TEAM_ROSTERSID = (1, 17)
    
    def create(type, callback, isOpen = True, comment = '', arenaTypeID = None, roundLength = 0):
        '''
\t\tCreate prebbattle with specified parameters
\t\tExample:
\t\t\tsuccess = yield AccountPrebbatle.create(constants.PREBATTLE_TYPE.SQUAD)
\t\t\tif success:
\t\t\t\t#do somthing

\t\t@param type: integer - prebattle type from constants.PREBATTLE_TYPE
\t\t@param isOpen: boolean - (for COMPANY and TRAINING)True:everybody can join otherwise by invites only
\t\t@param comment: string - (for COMPANY and TRAINING) user defined description
\t\t@param arenaTypeID: integer - for TRAINING user defined arena
\t\t@param roundLength: integer - for TRAINING user defined round legth in seconds
\t\t'''
        
        def onPrebattleJoined():
            g_playerEvents.onPrebattleJoined -= onPrebattleJoined
            g_playerEvents.onPrebattleJoinFailure -= onPrebattleJoinFailure
            callback(True)

        
        def onPrebattleJoinFailure(errorCode):
            g_playerEvents.onPrebattleJoined -= onPrebattleJoined
            g_playerEvents.onPrebattleJoinFailure -= onPrebattleJoinFailure
            message = '#system_messages:arena_start_errors/join/%s' % constants.JOIN_FAILURE_NAMES[errorCode]
            SystemMessages.pushI18nMessage(message, type = SystemMessages.SM_TYPE.Error)
            callback(False)

        yield AccountPrebattle._AccountPrebattle__exitConfirmation()
        exitComplete = (None, None, (None, None, None))
        if exitComplete:
            g_playerEvents.onPrebattleJoined += onPrebattleJoined
            g_playerEvents.onPrebattleJoinFailure += onPrebattleJoinFailure
            if type == constants.PREBATTLE_TYPE.SQUAD:
                BigWorld.player().prb_createSquad()
            elif type == constants.PREBATTLE_TYPE.COMPANY:
                BigWorld.player().prb_createCompany(isOpen, comment)
            elif type == constants.PREBATTLE_TYPE.TRAINING:
                BigWorld.player().prb_createTraining(arenaTypeID, roundLength, isOpened, comment)
            else:
                LOG_ERROR('Unknown prebattle type')
                callback(False)
        else:
            callback(False)

    create = staticmethod(async(process(create)))
    
    def join(prebattleID, callback):
        '''
\t\tJoin prebbattle
\t\tExample:
\t\t\tsuccess = yield AccountPrebbatle.join(123)
\t\t\tif success:
\t\t\t\t#do somthing

\t\t@param prebattleID: integer - prebattle id to join
\t\t'''
        
        def onPrebattleJoined():
            g_playerEvents.onPrebattleJoined -= onPrebattleJoined
            g_playerEvents.onPrebattleJoinFailure -= onPrebattleJoinFailure
            callback(True)

        
        def onPrebattleJoinFailure(errorCode):
            g_playerEvents.onPrebattleJoined -= onPrebattleJoined
            g_playerEvents.onPrebattleJoinFailure -= onPrebattleJoinFailure
            message = '#system_messages:arena_start_errors/join/%s' % constants.JOIN_FAILURE_NAMES[errorCode]
            SystemMessages.pushI18nMessage(message, type = SystemMessages.SM_TYPE.Error)
            callback(False)

        yield AccountPrebattle._AccountPrebattle__exitConfirmation()
        exitComplete = (None, None, (None, None, None))
        if exitComplete:
            BigWorld.player().prb_join(prebattleID)
        else:
            callback(False)

    join = staticmethod(async(process(join)))
    
    def exit(callback):
        '''
\t\tExit from prebattle if anny
\t\tExample:
\t\t\tsuccess = yield AccountPrebattle.exit()
\t\t\tif success:
\t\t\t\t#do somthing may create new prebattle
\t\t'''
        
        def onPrebattleLeaveResponse(errorCode):
            if errorCode < 0:
                LOG_ERROR('Server return error for prebattle leave request: responseCode=%s' % errorCode)
            
            callback(errorCode >= 0)

        if AccountPrebattle.get():
            BigWorld.player().prb_leave(onPrebattleLeaveResponse)
        else:
            callback(True)

    exit = staticmethod(async(exit))
    
    def getCurrentPlayerId():
        if BigWorld.player():
            return BigWorld.player().id
        return 0

    getCurrentPlayerId = staticmethod(getCurrentPlayerId)
    
    def get():
        if hasattr(BigWorld.player(), 'prebattle'):
            return BigWorld.player().prebattle

    get = staticmethod(get)
    
    def isSquad():
        return AccountPrebattle.type() == constants.PREBATTLE_TYPE.SQUAD

    isSquad = staticmethod(isSquad)
    
    def isCompany():
        return AccountPrebattle.type() == constants.PREBATTLE_TYPE.COMPANY

    isCompany = staticmethod(isCompany)
    
    def isTraining():
        return AccountPrebattle.type() == constants.PREBATTLE_TYPE.TRAINING

    isTraining = staticmethod(isTraining)
    
    def isBattleSession():
        return AccountPrebattle.type() in (constants.PREBATTLE_TYPE.TOURNAMENT, constants.PREBATTLE_TYPE.CLAN)

    isBattleSession = staticmethod(isBattleSession)
    
    def isTeamReady():
        if AccountPrebattle.get() and AccountPrebattle.getMemberTeam():
            return AccountPrebattle.get().teamStates[AccountPrebattle.getMemberTeam()] in (constants.PREBATTLE_TEAM_STATE.LOCKED, constants.PREBATTLE_TEAM_STATE.READY)
        return False

    isTeamReady = staticmethod(isTeamReady)
    
    def isMemberReady(id = None):
        if id is None:
            pass
        1
        player = AccountPrebattle.getCurrentPlayerId()(id)
        if player:
            return player['state'] == constants.PREBATTLE_ACCOUNT_STATE.READY
        return False

    isMemberReady = staticmethod(isMemberReady)
    
    def getMember(id):
        if AccountPrebattle.get():
            if AccountPrebattle.get().rosters:
                for roster in AccountPrebattle.ROSTERS:
                    member = AccountPrebattle.get().rosters.get(roster, { }).get(id, None)
                    if member:
                        return member
                
            
        

    getMember = staticmethod(getMember)
    
    def getMemberTeam(id = None):
        roster = AccountPrebattle.getMemberRoster(id)
        return AccountPrebattle.ROSTERS2TEAMS.get(roster, (None, None))[0]

    getMemberTeam = staticmethod(getMemberTeam)
    
    def isMemberInKeyStaff(id = None):
        roster = AccountPrebattle.getMemberRoster(id)
        return not AccountPrebattle.ROSTERS2TEAMS.get(roster, (None, None))[1]

    isMemberInKeyStaff = staticmethod(isMemberInKeyStaff)
    
    def getMemberRoster(id = None):
        if AccountPrebattle.get():
            if AccountPrebattle.get().rosters:
                for roster in AccountPrebattle.ROSTERS:
                    if id is None:
                        pass
                    1
                    if AccountPrebattle.getCurrentPlayerId()(id, None):
                        return roster
                
            
        

    getMemberRoster = staticmethod(getMemberRoster)
    
    def isCreator():
        member = AccountPrebattle.getMember(AccountPrebattle.getCurrentPlayerId())
        if member:
            settings = AccountPrebattle.get().settings
            if settings is None:
                return None
            accRole = settings.get('roles', { }).get(member['dbID'], 0)
            if not accRole:
                accRole = settings.get('clanRoles', { }).get(member['clanDBID'], 0)
            
            if not accRole:
                accRole = settings.get('teamRoles', { }).get(AccountPrebattle.getMemberTeam(), 0)
            
            creatorRole = None
            if AccountPrebattle.isSquad():
                creatorRole = constants.PREBATTLE_ROLE.SQUAD_CREATOR
            elif AccountPrebattle.isCompany():
                creatorRole = constants.PREBATTLE_ROLE.COMPANY_CREATOR
            elif AccountPrebattle.isTraining():
                creatorRole = constants.PREBATTLE_ROLE.TRAINING_CREATOR
            elif AccountPrebattle.isBattleSession():
                if AccountPrebattle.getMemberTeam() == 1:
                    creatorRole = constants.PREBATTLE_ROLE.TEAM_READY_1
                else:
                    creatorRole = constants.PREBATTLE_ROLE.TEAM_READY_2
                return accRole & creatorRole != 0
            settings is None
            return accRole == creatorRole
        return False

    isCreator = staticmethod(isCreator)
    
    def type():
        if AccountPrebattle.get():
            if AccountPrebattle.get().settings:
                return AccountPrebattle.get().settings['type']
        

    type = staticmethod(type)
    
    def typeName():
        if AccountPrebattle.type() is not None:
            return constants.PREBATTLE_TYPE_NAMES[AccountPrebattle.type()]

    typeName = staticmethod(typeName)
    
    def getBattleType():
        if AccountPrebattle.get():
            if AccountPrebattle.isSquad():
                return constants.ARENA_GUI_TYPE.RANDOM
            if AccountPrebattle.isCompany():
                return constants.ARENA_GUI_TYPE.COMPANY
            if AccountPrebattle.isTraining():
                return constants.ARENA_GUI_TYPE.TRAINING
            return constants.ARENA_GUI_TYPE.UNKNOWN
        return constants.ARENA_GUI_TYPE.RANDOM

    getBattleType = staticmethod(getBattleType)
    
    def getPlayersReadyStat(rosterId):
        prebattle = AccountPrebattle.get()
        notReadyCount = 0
        playerCount = 0
        limitMaxCount = 0
        haveInBattle = False
        if prebattle:
            players = prebattle.rosters.get(rosterId, { })
            playerCount = len(players)
            settings = prebattle.settings
            limitMaxCount = settings.get('limit_max_count', { }).get(rosterId, 0)
            for (_, accInfo) in players.iteritems():
                state = accInfo.get('state', constants.PREBATTLE_ACCOUNT_STATE.UNKNOWN)
                if not (state & constants.PREBATTLE_ACCOUNT_STATE.READY) or state & constants.PREBATTLE_ACCOUNT_STATE.OFFLINE:
                    notReadyCount += 1
                    if not haveInBattle and state & constants.PREBATTLE_ACCOUNT_STATE.IN_BATTLE:
                        haveInBattle = True
                    
            
        
        return (notReadyCount, haveInBattle, playerCount, limitMaxCount)

    getPlayersReadyStat = staticmethod(getPlayersReadyStat)
    
    def getPrebattleLocalizedData(extraData = None):
        led = { }
        if extraData is None:
            if AccountPrebattle.get():
                if AccountPrebattle.get().settings:
                    extraData = AccountPrebattle.get().settings.get('extraData', { })
                
            
        
        if extraData:
            getClientLanguage = getClientLanguage
            import helpers
            lng = getClientLanguage()
            ld = extraData.get('localized_data', { })
            if ld:
                if lng in ld:
                    led = ld[lng]
                elif constants.DEFAULT_LANGUAGE in ld:
                    led = ld[constants.DEFAULT_LANGUAGE]
                else:
                    led = ld.items()[0][1]
            
        
        return led

    getPrebattleLocalizedData = staticmethod(getPrebattleLocalizedData)
    
    def getPrebattleDescription(extraData = None):
        led = AccountPrebattle.getPrebattleLocalizedData(extraData)
        if led:
            return ': '.join([
                led.get('event_name', ''),
                led.get('session_name', '')]).strip()
        return ''

    getPrebattleDescription = staticmethod(getPrebattleDescription)
    
    def getSettings():
        if AccountPrebattle.get():
            return AccountPrebattle.get().settings
        return { }

    getSettings = staticmethod(getSettings)
    
    def getLevelLimits():
        prbSettings = AccountPrebattle.getSettings()
        (min, max) = (1, 10)
        if prbSettings is not None:
            (min, max) = prbSettings.get('limit_level', (min, max))
        
        return (min, max)

    getLevelLimits = staticmethod(getLevelLimits)
    
    def getClassLevelLimits(classType):
        prbSettings = AccountPrebattle.getSettings()
        (min, max) = AccountPrebattle.getLevelLimits()
        if prbSettings is not None:
            if prbSettings.get('limit_class_level', { }).has_key(classType):
                (min, max) = prbSettings.get('limit_class_level', { })[classType]
            
        
        return (min, max)

    getClassLevelLimits = staticmethod(getClassLevelLimits)
    
    def setMemdberReady():
        notValidReason = 'no_readyVehicle'
        g_currentVehicle = g_currentVehicle
        import CurrentVehicle
        if g_currentVehicle.isReadyToFight():
            isVehicleValid = isVehicleValid
            import prebattle_shared
            (isV, notValidReason) = isVehicleValid(g_currentVehicle.vehicle.descriptor, g_currentVehicle.vehicle.getShellsList(), AccountPrebattle.getSettings())
            if isV:
                BigWorld.player().prb_ready(g_currentVehicle.vehicle.inventoryId, AccountPrebattle._AccountPrebattle__onPrebattleReadyResponse)
                return True
        
        if notValidReason in ('wrong_level', 'wrong_class_level'):
            if notValidReason == 'wrong_class_level':
                classTag = set(vehicles.VEHICLE_CLASS_TAGS.intersection(g_currentVehicle.vehicle.tags)).pop()
                (minLevel, maxLevel) = AccountPrebattle.getSettings().get('limit_class_level', { }).get(classTag, (0, 65535))
            else:
                (minLevel, maxLevel) = AccountPrebattle.getSettings().get('limit_level', (0, 65535))
            SystemMessages.pushI18nMessage('#system_messages:prebattleReady/%s' % notValidReason, minLevel, maxLevel, type = SystemMessages.SM_TYPE.Error)
            return False
        SystemMessages.pushI18nMessage('#system_messages:prebattleReady/%s' % notValidReason, type = SystemMessages.SM_TYPE.Error)
        return False

    setMemdberReady = staticmethod(setMemdberReady)
    
    def __onPrebattleReadyResponse(code):
        import AccountCommands as AccountCommands
        if code == AccountCommands.RES_FAILURE:
            SystemMessages = SystemMessages
            import gui
            SystemMessages.pushI18nMessage('#system_messages:prebattleReady/notSetReadyStatus', type = SystemMessages.SM_TYPE.Error)
        elif code < 0:
            LOG_ERROR = LOG_ERROR
            import debug_utils
            LOG_ERROR('Server return error for member ready request:  responseCode=%s' % code)
        

    _AccountPrebattle__onPrebattleReadyResponse = staticmethod(__onPrebattleReadyResponse)
    
    def __exitConfirmation(callback):
        success = False
        if not AccountPrebattle.get():
            yield AccountPrebattle.exit()
            success = None
        else:
            customMessage = '#dialogs:exitCurrentPrebattle/customMessage/%s' % constants.PREBATTLE_TYPE_NAMES[AccountPrebattle.type()]
            async_showConfirmDialog = async_showConfirmDialog
            import gui.Scaleform.utils.functions
            yield async_showConfirmDialog('exitCurrentPrebattle', customMessage = customMessage)
            isConfirmedExit = None
            if isConfirmedExit:
                yield AccountPrebattle.exit()
                success = None
            
        callback(success)

    _AccountPrebattle__exitConfirmation = staticmethod(async(process(__exitConfirmation)))


