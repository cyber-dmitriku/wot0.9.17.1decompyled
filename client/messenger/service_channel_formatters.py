# Source Generated with Decompyle++
# File: service_channel_formatters.pyc (Python 2.6)

import types
from adisp import async, process
from debug_utils import LOG_ERROR, LOG_WARNING, LOG_CURRENT_EXCEPTION, LOG_DEBUG
import account_helpers
import ArenaType
import BigWorld
import offers
from constants import INVOICE_ASSET, AUTO_MAINTENANCE_TYPE, AUTO_MAINTENANCE_RESULT, PREBATTLE_TYPE, FINISH_REASON, KICK_REASON_NAMES, KICK_REASON
import dossiers
from helpers import i18n, html, getClientLanguage, getLocalizedData
from helpers import time_utils
from items import getTypeInfoByIndex, getTypeInfoByName, tankmen
from items import vehicles as vehicles_core
from account_helpers import rare_achievements
import enumerations
from messenger import getLongDatetimeFormat, g_settings, MESSENGER_I18N_FILE

def formatPrice(price, reverse = False):
    outPrice = []
    (credits, gold) = price[:2]
    if credits != 0 or gold == 0:
        cname = i18n.makeString('#menu:price/credits') + ': '
        cformatted = BigWorld.wg_getIntegralFormat(credits)
        if reverse:
            pass
        1
        [
            cformatted,
            ' ',
            cname]([
            cname,
            ' ',
            cformatted])
        if gold:
            outPrice.append(', ')
        
    
    if gold:
        gname = i18n.makeString('#menu:price/gold') + ': '
        gformatted = BigWorld.wg_getGoldFormat(gold)
        if reverse:
            pass
        1
        [
            gformatted,
            ' ',
            gname]([
            gname,
            ' ',
            gformatted])
    
    return ''.join(outPrice)


class ServiceChannelFormatter(object):
    
    def format(self, data, *args):
        pass

    
    def notify(self):
        return False

    
    def isAsync(self):
        return False



class ServerRebootFormatter(ServiceChannelFormatter):
    
    def format(self, message):
        if message.data:
            local_dt = time_utils.utcToLocalDatetime(message.data)
            return g_settings.msgTemplates.format('serverReboot', ctx = {
                'date': local_dt.strftime('%c') })
        return None



class ServerRebootCancelledFormatter(ServiceChannelFormatter):
    
    def format(self, message):
        if message.data:
            local_dt = time_utils.utcToLocalDatetime(message.data)
            return g_settings.msgTemplates.format('serverRebootCancelled', ctx = {
                'date': local_dt.strftime('%c') })
        return None



class BattleResultsFormatter(ServiceChannelFormatter):
    _BattleResultsFormatter__battleResultKeys = {
        -1: 'battleDefeatResult',
        0: 'battleDrawGameResult',
        1: 'battleVictoryResult' }
    _BattleResultsFormatter__goldTemplateKey = 'battleResultGold'
    _BattleResultsFormatter__i18n_penalty = i18n.makeString('#%s:serviceChannelMessages/battleResults/penaltyForDamageAllies' % MESSENGER_I18N_FILE)
    _BattleResultsFormatter__i18n_contribution = i18n.makeString('#%s:serviceChannelMessages/battleResults/contributionForDamageAllies' % MESSENGER_I18N_FILE)
    
    def notify(self):
        return True

    
    def format(self, message):
        battleResult = message.data
        arenaTypeID = battleResult.get('arenaTypeID', 0)
        if arenaTypeID > 0:
            pass
        1
        arenaType = None
        arenaCreateTime = battleResult.get('arenaCreateTime', None)
        if arenaCreateTime and arenaType:
            ctx = {
                'arenaName': i18n.makeString(arenaType.name),
                'createdAt': getLongDatetimeFormat(arenaCreateTime),
                'vehicleName': 'N/A',
                'xp': '0',
                'credits': '0' }
            vehicleCompDesc = battleResult.get('vehTypeCompDescr', None)
            if vehicleCompDesc:
                vt = vehicles_core.getVehicleType(vehicleCompDesc)
                ctx['vehicleName'] = vt.userString
            
            xp = battleResult.get('xp')
            if xp:
                ctx['xp'] = BigWorld.wg_getIntegralFormat(xp)
            
            ctx['xpEx'] = self._BattleResultsFormatter__makeXpExString(xp, battleResult)
            ctx['gold'] = self._BattleResultsFormatter__makeGoldString(battleResult.get('gold', 0))
            credits = battleResult.get('credits')
            if credits:
                ctx['credits'] = BigWorld.wg_getIntegralFormat(credits)
            
            ctx['creditsEx'] = self._BattleResultsFormatter__makeCreditsExString(credits, battleResult)
            ctx['achieves'] = self._BattleResultsFormatter__makeAchievementsString(battleResult)
            ctx['lock'] = self._BattleResultsFormatter__makeVehicleLockString(ctx['vehicleName'], battleResult)
            auxData = {
                'arenaUniqueID': str(int(battleResult.get('arenaUniqueID', 0))) }
            return g_settings.msgTemplates.format(self._BattleResultsFormatter__battleResultKeys[battleResult['isWinner']], ctx = ctx, data = auxData)
        return None

    
    def _BattleResultsFormatter__makeVehicleLockString(self, vehicle, battleResult):
        expireTime = battleResult.get('vehTypeUnlockTime', 0)
        if not expireTime:
            return ''
        return g_settings.htmlTemplates.format('battleResultLocks', ctx = {
            'vehicleName': vehicle,
            'expireTime': getLongDatetimeFormat(expireTime) })

    
    def _BattleResultsFormatter__makeXpExString(self, xp, battleResult):
        if not xp:
            return ''
        exStrings = []
        penalty = battleResult.get('xpPenalty', 0)
        if penalty > 0:
            exStrings.append(self._BattleResultsFormatter__i18n_penalty % BigWorld.wg_getIntegralFormat(penalty))
        
        if battleResult['isWinner'] == 1:
            xpFactor = battleResult.get('dailyXPFactor', 1)
            if xpFactor > 1:
                exStrings.append(i18n.makeString('#%s:serviceChannelMessages/battleResults/doubleXpFactor' % MESSENGER_I18N_FILE) % xpFactor)
            
        
        if len(exStrings):
            return ' ({0:>s})'.format('; '.join(exStrings))
        return ''

    
    def _BattleResultsFormatter__makeCreditsExString(self, credits, battleResult):
        if not credits:
            return ''
        exStrings = []
        penalty = sum([
            battleResult.get('creditsPenalty', 0),
            battleResult.get('creditsContributionOut', 0)])
        if penalty > 0:
            exStrings.append(self._BattleResultsFormatter__i18n_penalty % BigWorld.wg_getIntegralFormat(penalty))
        
        contribution = battleResult.get('creditsContributionIn', 0)
        if contribution > 0:
            exStrings.append(self._BattleResultsFormatter__i18n_contribution % BigWorld.wg_getIntegralFormat(contribution))
        
        if len(exStrings):
            return ' ({0:>s})'.format('; '.join(exStrings))
        return ''

    
    def _BattleResultsFormatter__makeGoldString(self, gold):
        if not gold:
            return ''
        return g_settings.htmlTemplates.format(self._BattleResultsFormatter__goldTemplateKey, {
            'gold': BigWorld.wg_getGoldFormat(gold) })

    
    def _BattleResultsFormatter__makeAchievementsString(self, battleResult):
        ACHIEVEMENTS = ACHIEVEMENTS
        ACHIEVEMENT_SECTIONS_INDICES = ACHIEVEMENT_SECTIONS_INDICES
        import dossiers.achievements
        
        def sortFunction(a, b):
            aKey = dossiers.RECORD_NAMES[a[0]]
            bKey = dossiers.RECORD_NAMES[b[0]]
            aOrderVal = ACHIEVEMENT_SECTIONS_INDICES[ACHIEVEMENTS.get(aKey, { }).get('section', 'battle')]
            bOrderVal = ACHIEVEMENT_SECTIONS_INDICES[ACHIEVEMENTS.get(bKey, { }).get('section', 'battle')]
            return aOrderVal - bOrderVal

        
        def filterFunc(item):
            if dossiers.RECORD_NAMES[item[0]] == 'maxXP':
                return False
            return True

        records = battleResult.get('popUpRecords', [])
        records = filter(filterFunc, records)
        if not len(records):
            return ''
        achieveList = []
        for (recordIdx, value) in sorted(records, cmp = sortFunction):
            achieveKey = dossiers.RECORD_NAMES[recordIdx]
            achieveI18n = i18n.makeString('#achievements:%s' % achieveKey)
            if achieveKey == 'maxXP':
                continue
            
            rule = AchievementsFormatRulesDict.get(achieveKey)
            if rule:
                achieveList.append(rule(achieveI18n, value))
                continue
            len(records)
            achieveList.append(achieveI18n)
        
        return g_settings.htmlTemplates.format('battleResultAchieves', {
            'achieves': ', '.join(achieveList) })


AchievementsFormatRules = enumerations.Enumeration('Achievement format rules', [
    ('showRank', (lambda key, count: key % i18n.makeString('#achievements:achievement/rank%d' % int(count)))),
    ('showMaster', (lambda key, count: key % {
'name': i18n.makeString('#achievements:achievement/master%d' % int(count)) }))], instance = enumerations.CallabbleEnumItem)
AchievementsFormatRulesDict = {
    'medalKay': AchievementsFormatRules.showRank,
    'medalCarius': AchievementsFormatRules.showRank,
    'medalKnispel': AchievementsFormatRules.showRank,
    'medalPoppel': AchievementsFormatRules.showRank,
    'medalAbrams': AchievementsFormatRules.showRank,
    'medalLeClerc': AchievementsFormatRules.showRank,
    'medalLavrinenko': AchievementsFormatRules.showRank,
    'medalEkins': AchievementsFormatRules.showRank,
    'markOfMastery': AchievementsFormatRules.showMaster }

class AutoMaintenanceFormatter(ServiceChannelFormatter):
    _AutoMaintenanceFormatter__messages = {
        AUTO_MAINTENANCE_RESULT.NOT_ENOUGH_ASSETS: {
            AUTO_MAINTENANCE_TYPE.REPAIR: '#messenger:serviceChannelMessages/autoRepairError',
            AUTO_MAINTENANCE_TYPE.LOAD_AMMO: '#messenger:serviceChannelMessages/autoLoadError',
            AUTO_MAINTENANCE_TYPE.EQUIP: '#messenger:serviceChannelMessages/autoEquipError' },
        AUTO_MAINTENANCE_RESULT.OK: {
            AUTO_MAINTENANCE_TYPE.REPAIR: '#messenger:serviceChannelMessages/autoRepairSuccess',
            AUTO_MAINTENANCE_TYPE.LOAD_AMMO: '#messenger:serviceChannelMessages/autoLoadSuccess',
            AUTO_MAINTENANCE_TYPE.EQUIP: '#messenger:serviceChannelMessages/autoEquipSuccess' },
        AUTO_MAINTENANCE_RESULT.NOT_PERFORMED: {
            AUTO_MAINTENANCE_TYPE.REPAIR: '#messenger:serviceChannelMessages/autoRepairSkipped',
            AUTO_MAINTENANCE_TYPE.LOAD_AMMO: '#messenger:serviceChannelMessages/autoLoadSkipped',
            AUTO_MAINTENANCE_TYPE.EQUIP: '#messenger:serviceChannelMessages/autoEquipSkipped' } }
    
    def notify(self):
        return True

    
    def format(self, message):
        vehicleCompDescr = message.data.get('vehTypeCD', None)
        result = message.data.get('result', None)
        type = message.data.get('typeID', None)
        cost = message.data.get('cost', (0, 0))
        if vehicleCompDescr is not None and result is not None and type is not None:
            vt = vehicles_core.getVehicleType(vehicleCompDescr)
            if type == AUTO_MAINTENANCE_TYPE.REPAIR:
                formatMsgType = 'RepairSysMessage'
            elif cost[1] == 0:
                pass
            
            formatMsgType = 'PurchaseForGoldSysMessage'
            msg = i18n.makeString(self._AutoMaintenanceFormatter__messages[result][type]) % vt.userString
            if result == AUTO_MAINTENANCE_RESULT.OK:
                templateName = formatMsgType
            elif result == AUTO_MAINTENANCE_RESULT.NOT_ENOUGH_ASSETS:
                templateName = 'ErrorSysMessage'
            else:
                templateName = 'WarningSysMessage'
            if result == AUTO_MAINTENANCE_RESULT.OK:
                msg = msg + formatPrice((abs(cost[0]), abs(cost[1])))
            
            return g_settings.msgTemplates.format(templateName, {
                'text': msg })
        return None



class AchievementFormatter(ServiceChannelFormatter):
    
    def __getRareTitle(self, id, callback):
        rare_achievements.getRareAchievementText(getClientLanguage(), (id,), (lambda id, text: callback(text.get('title'))))

    _AchievementFormatter__getRareTitle = async(__getRareTitle)
    
    def notify(self):
        return True

    
    def isAsync(self):
        return True

    
    def format(self, message, callback):
        yield (lambda callback: callback(True))
        achievesList = list()
        achieves = message.data.get('popUpRecords')
        if achieves is not None:
            continue
            _[1]([ i18n.makeString('#achievements:%s' % name) for name in achieves ])
        
        rares = message.data.get('rareAchievements')
        if rares is not None:
            unknownAchieves = 0
            for id in rares:
                if id > 0:
                    yield self._AchievementFormatter__getRareTitle(id)
                    title = None
                    if title is None:
                        unknownAchieves += 1
                    else:
                        achievesList.append(title)
                title is None
            
            if unknownAchieves:
                if unknownAchieves > 1:
                    pass
                1
                i18n.makeString('#system_messages:%s/title'('actionAchievements' % 'actionAchievement'))
            
        
        if not len(achievesList):
            callback(None)
            return None
        callback(g_settings.msgTemplates.format('achievementReceived', {
            'achieves': ', '.join(achievesList) }))

    format = async(process(format))


class GoldReceivedFormatter(ServiceChannelFormatter):
    
    def format(self, message):
        data = message.data
        gold = data.get('gold', None)
        transactionTime = data.get('date', None)
        if gold and transactionTime:
            return g_settings.msgTemplates.format('goldReceived', {
                'date': getLongDatetimeFormat(transactionTime),
                'gold': BigWorld.wg_getGoldFormat(account_helpers.convertGold(gold)) })
        return None



class GiftReceivedFormatter(ServiceChannelFormatter):
    _GiftReceivedFormatter__handlers = {
        'money': ('_GiftReceivedFormatter__formatMoneyGiftMsg', {
            1: 'creditsReceivedAsGift',
            2: 'goldReceivedAsGift',
            3: 'creditsAndGoldReceivedAsGift' }),
        'xp': ('_GiftReceivedFormatter__formatXPGiftMsg', 'xpReceivedAsGift'),
        'premium': ('_GiftReceivedFormatter__formatPremiumGiftMsg', 'premiumReceivedAsGift'),
        'item': ('_GiftReceivedFormatter__formatItemGiftMsg', 'itemReceivedAsGift'),
        'vehicle': ('_GiftReceivedFormatter__formatVehicleGiftMsg', 'vehicleReceivedAsGift') }
    
    def format(self, message):
        data = message.data
        type = data.get('type')
        if type is not None:
            (handlerName, templateKey) = self._GiftReceivedFormatter__handlers.get(type, (None, None))
            if handlerName is not None:
                return getattr(self, handlerName)(templateKey, data)
        

    
    def _GiftReceivedFormatter__formatMoneyGiftMsg(self, keys, data):
        credits = data.get('credits', 0)
        gold = data.get('gold', 0)
        result = None
        ctx = { }
        idx = 0
        if credits > 0:
            idx |= 1
            ctx['credits'] = BigWorld.wg_getIntegralFormat(credits)
        
        if gold > 0:
            idx |= 2
            ctx['gold'] = BigWorld.wg_getGoldFormat(gold)
        
        if idx in keys:
            result = g_settings.msgTemplates.format(keys[idx], ctx)
        
        return result

    
    def _GiftReceivedFormatter__formatXPGiftMsg(self, key, data):
        xp = data.get('amount', 0)
        result = None
        if xp > 0:
            result = g_settings.msgTemplates.format(key, ctx = {
                'freeXP': BigWorld.wg_getIntegralFormat(xp) })
        
        return result

    
    def _GiftReceivedFormatter__formatPremiumGiftMsg(self, templateKey, data):
        days = data.get('amount', 0)
        result = None
        if days > 0:
            result = g_settings.msgTemplates.format(templateKey, ctx = {
                'days': days })
        
        return result

    
    def _GiftReceivedFormatter__formatItemGiftMsg(self, templateKey, data):
        amount = data.get('amount', 0)
        result = None
        itemTypeIdx = data.get('itemTypeIdx')
        itemCompactDesc = data.get('itemCD')
        if amount > 0 and itemTypeIdx is not None and itemCompactDesc is not None:
            result = g_settings.msgTemplates.format(templateKey, ctx = {
                'typeName': getTypeInfoByIndex(itemTypeIdx)['userString'],
                'itemName': vehicles_core.getDictDescr(itemCompactDesc)['userString'],
                'amount': amount })
        
        return result

    
    def _GiftReceivedFormatter__formatVehicleGiftMsg(self, templateKey, data):
        vCompDesc = data.get('typeCD', None)
        result = None
        if vCompDesc is not None:
            result = g_settings.msgTemplates.format(templateKey, ctx = {
                'vehicleName': vehicles_core.getVehicleType(vCompDesc).userString })
        
        return result



class InvoiceReceivedFormatter(ServiceChannelFormatter):
    _InvoiceReceivedFormatter__assetHandlers = {
        INVOICE_ASSET.GOLD: '_InvoiceReceivedFormatter__formatAmount',
        INVOICE_ASSET.CREDITS: '_InvoiceReceivedFormatter__formatAmount',
        INVOICE_ASSET.PREMIUM: '_InvoiceReceivedFormatter__formatAmount',
        INVOICE_ASSET.FREE_XP: '_InvoiceReceivedFormatter__formatAmount',
        INVOICE_ASSET.DATA: '_InvoiceReceivedFormatter__formatData' }
    _InvoiceReceivedFormatter__operationTemplateKeys = {
        INVOICE_ASSET.GOLD: 'goldAccruedInvoiceReceived',
        INVOICE_ASSET.CREDITS: 'creditsAccruedInvoiceReceived',
        INVOICE_ASSET.PREMIUM: 'premiumAccruedInvoiceReceived',
        INVOICE_ASSET.FREE_XP: 'freeXpAccruedInvoiceReceived',
        INVOICE_ASSET.GOLD | 16: 'goldDebitedInvoiceReceived',
        INVOICE_ASSET.CREDITS | 16: 'creditsDebitedInvoiceReceived',
        INVOICE_ASSET.PREMIUM | 16: 'premiumDebitedInvoiceReceived',
        INVOICE_ASSET.FREE_XP | 16: 'freeXpDebitedInvoiceReceived' }
    _InvoiceReceivedFormatter__messageTemplateKeys = {
        INVOICE_ASSET.GOLD: 'financialInvoiceReceived',
        INVOICE_ASSET.CREDITS: 'financialInvoiceReceived',
        INVOICE_ASSET.PREMIUM: 'premiumInvoiceReceived',
        INVOICE_ASSET.FREE_XP: 'freeXpInvoiceReceived',
        INVOICE_ASSET.DATA: 'dataInvoiceReceived' }
    _InvoiceReceivedFormatter__i18nPiecesString = i18n.makeString('#{0:>s}:serviceChannelMessages/invoiceReceived/pieces'.format(MESSENGER_I18N_FILE))
    _InvoiceReceivedFormatter__i18nCrewLvlString = i18n.makeString('#{0:>s}:serviceChannelMessages/invoiceReceived/crewLvl'.format(MESSENGER_I18N_FILE))
    
    def _InvoiceReceivedFormatter__getOperationTimeString(self, data):
        operationTime = data.get('at', None)
        if operationTime:
            fDatetime = getLongDatetimeFormat(time_utils.makeLocalServerTime(operationTime))
        else:
            fDatetime = 'N/A'
        return fDatetime

    
    def _InvoiceReceivedFormatter__getFinOperationString(self, assetType, amount):
        if amount > 0:
            pass
        1
        templateKey = 16
        templateKey |= assetType
        ctx = { }
        if assetType == INVOICE_ASSET.GOLD:
            ctx['amount'] = BigWorld.wg_getGoldFormat(abs(amount))
        else:
            ctx['amount'] = BigWorld.wg_getIntegralFormat(abs(amount))
        return g_settings.htmlTemplates.format(self._InvoiceReceivedFormatter__operationTemplateKeys[templateKey], ctx = ctx)

    
    def _InvoiceReceivedFormatter__getItemsString(self, items):
        accrued = []
        debited = []
        for (itemCompactDescr, count) in items.iteritems():
            if count:
                
                try:
                    item = vehicles_core.getDictDescr(itemCompactDescr)
                    itemString = '{0:>s} "{1:>s}" - {2:d} {3:>s}'.format(getTypeInfoByName(item['itemTypeName'])['userString'], item['userString'], count, self._InvoiceReceivedFormatter__i18nPiecesString)
                    if count > 0:
                        accrued.append(itemString)
                    else:
                        debited.append(itemString)
                LOG_ERROR('itemCompactDescr can not parse ', itemCompactDescr)
                LOG_CURRENT_EXCEPTION()

                continue
        
        result = ''
        if len(accrued):
            result = g_settings.htmlTemplates.format('itemsAccruedInvoiceReceived', ctx = {
                'items': ', '.join(accrued) })
        
        if len(debited):
            if len(result):
                result += '<br/>'
            
            result += g_settings.htmlTemplates.format('itemsDebitedInvoiceReceived', ctx = {
                'items': ', '.join(debited) })
        
        return result

    
    def _InvoiceReceivedFormatter__getVehicleNames(self, vehicles, exclude = None, validateNegative = True, showCrewLvl = True):
        addVehNames = []
        removeVehNames = []
        if exclude is None:
            exclude = []
        
        vehGetter = getattr(vehicles, 'get', None)
        for vehCompDescr in vehicles:
            if vehCompDescr is not None:
                isNegative = False
                if type(vehCompDescr) is types.IntType:
                    isNegative = vehCompDescr < 0
                    vehCompDescr = abs(vehCompDescr)
                
                if vehCompDescr in exclude:
                    continue
                
                crewLvl = 50
                if vehGetter is not None and showCrewLvl:
                    crewLvl = vehGetter(vehCompDescr, { }).get('crewLvl', 50)
                
                
                try:
                    vehUserString = vehicles_core.getVehicleType(vehCompDescr).userString
                    if crewLvl > 50:
                        crewLvl = self._InvoiceReceivedFormatter__i18nCrewLvlString % crewLvl
                        vehUserString = '{0:>s} ({1:>s})'.format(vehUserString, crewLvl)
                    
                    if isNegative and validateNegative:
                        removeVehNames.append(vehUserString)
                    else:
                        addVehNames.append(vehUserString)
                LOG_ERROR('Wrong vehicle compact descriptor', vehCompDescr)
                LOG_CURRENT_EXCEPTION()

                continue
        
        return (addVehNames, removeVehNames)

    
    def _InvoiceReceivedFormatter__getVehiclesString(self, vehicles, exclude = None):
        (addVehNames, removeVehNames) = self._InvoiceReceivedFormatter__getVehicleNames(vehicles, exclude = exclude)
        result = ''
        if len(addVehNames):
            result = g_settings.htmlTemplates.format('vehiclesAccruedInvoiceReceived', ctx = {
                'vehicles': ', '.join(addVehNames) })
        
        if len(removeVehNames):
            if len(result):
                result += '<br/>'
            
            result += g_settings.htmlTemplates.format('vehiclesDebitedInvoiceReceived', ctx = {
                'vehicles': ', '.join(removeVehNames) })
        
        return result

    
    def _InvoiceReceivedFormatter__getComptnString(self, comptnList):
        result = []
        html = g_settings.htmlTemplates
        for (itemDict, comptn) in comptnList:
            itemNames = []
            values = []
            items = itemDict.get('vehicles')
            if len(items):
                (itemNames, _) = self._InvoiceReceivedFormatter__getVehicleNames(items, validateNegative = False, showCrewLvl = False)
            
            gold = comptn.get('gold', 0)
            if gold > 0:
                values.append(html.format('goldCompensationInvoiceReceived', ctx = {
                    'amount': BigWorld.wg_getGoldFormat(gold) }))
            
            credits = comptn.get('credits', 0)
            if credits > 0:
                values.append(html.format('creditsCompensationInvoiceReceived', ctx = {
                    'amount': BigWorld.wg_getIntegralFormat(credits) }))
            
            if len(itemNames) and len(values):
                result.append(html.format('compensationForInvoiceReceived', ctx = {
                    'items': ', '.join(itemNames),
                    'compensation': ', '.join(values) }))
                continue
        
        return '<br/>'.join(result)

    
    def _InvoiceReceivedFormatter__getTankmenString(self, tmen):
        tmanUserStrings = []
        skillsConfig = tankmen.getSkillsConfig()
        for tmanCompDescr in tmen:
            
            try:
                tmanDescr = tankmen.TankmanDescr(tmanCompDescr)
                nationConfig = tankmen.getNationConfig(tmanDescr.nationID)
                tmanUserStrings.append('{0:>s} {1:>s} ({2:>s}, {3:>s}, {4:d}%)'.format(nationConfig['ranks'][tmanDescr.rankID].get('userString', ''), nationConfig['lastNames'][tmanDescr.lastNameID], skillsConfig.get(tmanDescr.role, { }).get('userString', ''), vehicles_core.g_cache.vehicle(tmanDescr.nationID, tmanDescr.vehicleTypeID).userString, tmanDescr.roleLevel))
            continue
            LOG_ERROR('Wrong tankman compact descriptor', tmanCompDescr)
            LOG_CURRENT_EXCEPTION()
            continue

        
        result = ''
        if len(tmanUserStrings):
            result = g_settings.htmlTemplates.format('tankmenInvoiceReceived', ctx = {
                'tankman': ', '.join(tmanUserStrings) })
        
        return result

    
    def _InvoiceReceivedFormatter__getSlotsString(self, slots):
        if slots > 0:
            template = 'slotsAccruedInvoiceReceived'
        else:
            template = 'slotsDebitedInvoiceReceived'
        return g_settings.htmlTemplates.format(template, {
            'amount': BigWorld.wg_getIntegralFormat(abs(slots)) })

    
    def _InvoiceReceivedFormatter__getL10nDescription(self, data):
        """
\t\tl10nDescr = data.get('data', {}).get('localized_description')
\t\tdescr = ''

\t\tif l10nDescr is not None and len(l10nDescr):
\t\t\t# gets description by client language, otherwise gets first
\t\t\t# description.
\t\t\tdescr = html.escape(
\t\t\t\tl10nDescr.get(getClientLanguage(), l10nDescr.values()[0])\t\t\t\t\t\t\t.get('description', u'').encode('utf-8')
\t\t\t)
\t\t\tif len(descr): descr = '<br/>' + descr

\t\treturn descr
\t\t"""
        lData = getLocalizedData(data.get('data', { }), 'localized_description')
        descr = html.escape(lData.get('description', u'').encode('utf-8'))
        if len(descr):
            descr = '<br/>' + descr
        
        return descr

    
    def _InvoiceReceivedFormatter__makeComptnItemDict(self, data):
        result = { }
        for (items, comptn) in data.get('compensation', []):
            for (key, data) in items.iteritems():
                exKey = 'ex_{0:>s}'.format(key)
                result.setdefault(exKey, [])
                result[exKey].extend(data)
            
        
        return result

    
    def _InvoiceReceivedFormatter__formatAmount(self, assetType, data):
        amount = data.get('amount', None)
        if amount is None:
            return None
        return g_settings.msgTemplates.format(self._InvoiceReceivedFormatter__messageTemplateKeys[assetType], ctx = {
            'at': self._InvoiceReceivedFormatter__getOperationTimeString(data),
            'desc': self._InvoiceReceivedFormatter__getL10nDescription(data),
            'op': self._InvoiceReceivedFormatter__getFinOperationString(assetType, amount) })

    
    def _InvoiceReceivedFormatter__formatData(self, assetType, data):
        dataEx = data.get('data', { })
        if dataEx is None or not len(dataEx):
            return None
        operations = []
        comptnDict = self._InvoiceReceivedFormatter__makeComptnItemDict(data)
        gold = dataEx.get('gold')
        if gold is not None:
            operations.append(self._InvoiceReceivedFormatter__getFinOperationString(INVOICE_ASSET.GOLD, gold))
        
        credits = dataEx.get('credits')
        if credits is not None:
            operations.append(self._InvoiceReceivedFormatter__getFinOperationString(INVOICE_ASSET.CREDITS, credits))
        
        freeXp = dataEx.get('freeXP')
        if freeXp is not None:
            operations.append(self._InvoiceReceivedFormatter__getFinOperationString(INVOICE_ASSET.FREE_XP, freeXp))
        
        premium = dataEx.get('premium')
        if premium is not None:
            operations.append(self._InvoiceReceivedFormatter__getFinOperationString(INVOICE_ASSET.PREMIUM, premium))
        
        items = dataEx.get('items', { })
        if items is not None and len(items) > 0:
            operations.append(self._InvoiceReceivedFormatter__getItemsString(items))
        
        tmen = dataEx.get('tankmen', { })
        if tmen is not None and len(tmen) > 0:
            operations.append(self._InvoiceReceivedFormatter__getTankmenString(tmen))
        
        vehicles = dataEx.get('vehicles', { })
        if vehicles is not None and len(vehicles) > 0:
            exclude = comptnDict.get('ex_vehicles', [])
            result = self._InvoiceReceivedFormatter__getVehiclesString(vehicles, exclude = exclude)
            if len(result):
                operations.append(result)
            
        
        compensation = data.get('compensation', [])
        if len(compensation):
            comptnStr = self._InvoiceReceivedFormatter__getComptnString(compensation)
            if len(comptnStr):
                operations.append(comptnStr)
            
        
        slots = dataEx.get('slots')
        if slots:
            operations.append(self._InvoiceReceivedFormatter__getSlotsString(slots))
        
        return g_settings.msgTemplates.format(self._InvoiceReceivedFormatter__messageTemplateKeys[assetType], ctx = {
            'at': self._InvoiceReceivedFormatter__getOperationTimeString(data),
            'desc': self._InvoiceReceivedFormatter__getL10nDescription(data),
            'op': '<br/>'.join(operations) })

    
    def format(self, message):
        LOG_DEBUG('invoiceReceived', message)
        data = message.data
        assetType = data.get('assetType', -1)
        handler = self._InvoiceReceivedFormatter__assetHandlers.get(assetType)
        if handler is not None:
            return getattr(self, handler)(assetType, data)
        return None



class AdminMessageFormatter(ServiceChannelFormatter):
    
    def format(self, message):
        if message.data:
            return g_settings.msgTemplates.format('adminMessage', {
                'text': message.data.decode('utf-8') })
        return None



class AccountTypeChangedFormatter(ServiceChannelFormatter):
    
    def format(self, message):
        data = message.data
        isPremium = data.get('isPremium', None)
        expiryTime = data.get('expiryTime', None)
        result = None
        if isPremium is not None:
            if isPremium:
                pass
            1
            accountTypeName = i18n.makeString('#menu:accountTypes/base')
            if expiryTime:
                pass
            1
            expiryDatetime = None
            if expiryDatetime:
                templateKey = 'accountTypeChangedWithExpiration'
                ctx = {
                    'accType': accountTypeName,
                    'expiryTime': expiryDatetime }
            else:
                templateKey = 'accountTypeChanged'
                ctx = {
                    'accType': accountTypeName }
            result = g_settings.msgTemplates.format(templateKey, ctx = ctx)
        
        return result



class PremiumActionFormatter(ServiceChannelFormatter):
    _templateKey = None
    
    def _getMessage(self, isPremium, expiryTime):
        pass

    
    def format(self, message):
        data = message.data
        isPremium = data.get('isPremium', None)
        expiryTime = data.get('expiryTime', None)
        if isPremium is not None:
            return self._getMessage(isPremium, expiryTime)



class PremiumBoughtFormatter(PremiumActionFormatter):
    _templateKey = 'premiumBought'
    
    def _getMessage(self, isPremium, expiryTime):
        result = None
        if isPremium is True and expiryTime > 0:
            result = g_settings.msgTemplates.format(self._templateKey, ctx = {
                'expiryTime': getLongDatetimeFormat(expiryTime) })
        
        return result



class PremiumExtendedFormatter(PremiumBoughtFormatter):
    _templateKey = 'premiumExtended'


class PremiumExpiredFormatter(PremiumActionFormatter):
    _templateKey = 'premiumExpired'
    
    def _getMessage(self, isPremium, expiryTime):
        result = None
        if isPremium is False:
            result = g_settings.msgTemplates.format(self._templateKey)
        
        return result



class WaresSoldFormatter(ServiceChannelFormatter):
    
    def notify(self):
        return True

    
    def format(self, message):
        result = None
        if message.data:
            offer = offers._makeOutOffer(message.data)
            result = g_settings.msgTemplates.format('waresSoldAsGold', ctx = {
                'srcWares': BigWorld.wg_getGoldFormat(offer.srcWares),
                'dstName': offer.dstName,
                'fee': offer.fee })
        
        return result



class WaresBoughtFormatter(ServiceChannelFormatter):
    
    def notify(self):
        return True

    
    def format(self, message):
        result = None
        if message.data:
            offer = offers._makeInOffer(message.data)
            result = g_settings.msgTemplates.format('waresBoughtAsGold', ctx = {
                'srcName': offer.srcName,
                'srcWares': BigWorld.wg_getGoldFormat(offer.srcWares) })
        
        return result



class PrebattleFormatter(ServiceChannelFormatter):
    _PrebattleFormatter__battleTypeByPrebattleType = {
        PREBATTLE_TYPE.TOURNAMENT: 'tournament',
        PREBATTLE_TYPE.CLAN: 'clan' }
    _battleFinishReasonKeys = { }
    _defaultBattleFinishReasonKey = ('base', True)
    
    def notify(self):
        return True

    
    def _getIconId(self, type):
        iconId = 'BattleResultIcon'
        if type == PREBATTLE_TYPE.CLAN:
            iconId = 'ClanBattleResultIcon'
        elif type == PREBATTLE_TYPE.TOURNAMENT:
            iconId = 'TournamentBattleResultIcon'
        
        return iconId

    
    def _makeBattleTypeString(self, type):
        typeString = self._PrebattleFormatter__battleTypeByPrebattleType.get(type, 'prebattle')
        key = '#{0:>s}:serviceChannelMessages/prebattle/battleType/{1:>s}'.format(MESSENGER_I18N_FILE, typeString)
        return i18n.makeString(key)

    
    def _makeDescriptionString(self, data, showBattlesCount = True):
        if data.has_key('localized_data') and len(data['localized_data']):
            description = account_helpers.AccountPrebattle.AccountPrebattle.getPrebattleDescription(data).encode('utf-8')
            description = html.escape(description)
        else:
            type = data.get('type')
            description = self._makeBattleTypeString(type)
        battlesLimit = data.get('battlesLimit', 0)
        if showBattlesCount and battlesLimit > 1:
            battlesCount = data.get('battlesCount')
            if battlesCount > 0:
                key = '#{0:>s}:serviceChannelMessages/prebattle/numberOfBattle'.format(MESSENGER_I18N_FILE)
                numberOfBattleString = i18n.makeString(key, battlesCount)
                description = '{0:>s} {1:>s}'.format(description, numberOfBattleString)
            else:
                LOG_WARNING('Invalid value of battlesCount ', battlesCount)
        
        return description

    
    def _getOpponentsString(self, opponents):
        first = opponents.get('1', { }).get('name', '').encode('utf-8')
        second = opponents.get('2', { }).get('name', '').encode('utf-8')
        result = ''
        if len(first) > 0 and len(second) > 0:
            result = g_settings.htmlTemplates.format('prebattleOpponents', ctx = {
                'first': html.escape(first),
                'second': html.escape(second) })
        
        return result

    
    def _getBattleResultString(self, winner, team):
        result = 'undefined'
        if 3 > winner:
            pass
        winner > -1
        if 1 and team in (1, 2):
            if not winner:
                result = 'draftGame'
            elif team != winner:
                pass
            
            result = 'win'
        
        return result

    
    def _makeBattleResultString(self, finishReason, winner, team):
        (finishString, showResult) = self._battleFinishReasonKeys.get(finishReason, self._defaultBattleFinishReasonKey)
        if showResult:
            resultString = self._getBattleResultString(winner, team)
            key = '#{0:>s}:serviceChannelMessages/prebattle/finish/{1:>s}/{2:>s}'.format(MESSENGER_I18N_FILE, finishString, resultString)
        else:
            key = '#{0:>s}:serviceChannelMessages/prebattle/finish/{1:>s}'.format(MESSENGER_I18N_FILE, finishString)
        return i18n.makeString(key)

    
    def _makeCreateAtString(self, message):
        if message.createdAt is not None:
            result = message.createdAt.strftime('%c')
        else:
            LOG_WARNING('Invalid value of created_at = None')
            import time as time
            result = getLongDatetimeFormat(time.time())
        return result



class PrebattleArenaFinishFormatter(PrebattleFormatter):
    _battleFinishReasonKeys = {
        FINISH_REASON.TECHNICAL: ('technical', True),
        FINISH_REASON.FAILURE: ('failure', False),
        FINISH_REASON.UNKNOWN: ('failure', False) }
    
    def format(self, message):
        LOG_DEBUG('prbArenaFinish', message)
        data = message.data
        type = data.get('type')
        winner = data.get('winner')
        team = data.get('team')
        wins = data.get('wins')
        finishReason = data.get('finishReason')
        if None in [
            type,
            winner,
            team,
            wins,
            finishReason]:
            return None
        battleResult = self._makeBattleResultString(finishReason, winner, team)
        subtotal = ''
        battlesLimit = data.get('battlesLimit', 0)
        if battlesLimit > 1:
            battlesCount = data.get('battlesCount', -1)
            winsLimit = data.get('winsLimit', -1)
            if battlesCount == battlesLimit and winsLimit == wins[1] or winsLimit == wins[2]:
                playerTeamWins = wins[team]
                if team == 1:
                    pass
                1
                otherTeamWins = 2[1]
                if winsLimit > 0 and playerTeamWins < winsLimit and otherTeamWins < winsLimit:
                    winner = None
                elif playerTeamWins == otherTeamWins:
                    winner = 0
                elif wins[1] > wins[2]:
                    pass
                
                winner = 2
                sessionResult = self._makeBattleResultString(-1, winner, team)
                subtotal = g_settings.htmlTemplates.format('prebattleTotal', ctx = {
                    'result': sessionResult,
                    'first': wins[1],
                    'second': wins[2] })
            else:
                subtotal = g_settings.htmlTemplates.format('prebattleSubtotal', ctx = {
                    'first': wins[1],
                    'second': wins[2] })
        
        return g_settings.msgTemplates.format('prebattleArenaFinish', ctx = {
            'desc': self._makeDescriptionString(data),
            'createdAt': self._makeCreateAtString(message),
            'opponents': self._getOpponentsString(data.get('opponents', { })),
            'result': battleResult,
            'subtotal': subtotal }, data = {
            'icon': self._getIconId(type) })



class PrebattleKickFormatter(PrebattleFormatter):
    
    def format(self, message):
        data = message.data
        result = None
        type = data.get('type')
        kickReason = data.get('kickReason')
        if type > 0 and kickReason > 0:
            ctx = { }
            key = '#system_messages:prebattle/kick/type/unknown'
            if type == PREBATTLE_TYPE.SQUAD:
                key = '#system_messages:prebattle/kick/type/squad'
            elif type == PREBATTLE_TYPE.COMPANY:
                key = '#system_messages:prebattle/kick/type/team'
            
            ctx['type'] = i18n.makeString(key)
            kickName = KICK_REASON_NAMES[kickReason]
            key = '#system_messages:prebattle/kick/reason/{0:>s}'.format(kickName)
            ctx['reason'] = i18n.makeString(key)
            result = g_settings.msgTemplates.format('prebattleKick', ctx = ctx)
        
        return result



class PrebattleDestructionFormatter(PrebattleFormatter):
    _battleFinishReasonKeys = {
        KICK_REASON.ARENA_CREATION_FAILURE: ('failure', False),
        KICK_REASON.AVATAR_CREATION_FAILURE: ('failure', False),
        KICK_REASON.VEHICLE_CREATION_FAILURE: ('failure', False),
        KICK_REASON.PREBATTLE_CREATION_FAILURE: ('failure', False),
        KICK_REASON.BASEAPP_CRASH: ('failure', False),
        KICK_REASON.CELLAPP_CRASH: ('failure', False),
        KICK_REASON.UNKNOWN_FAILURE: ('failure', False),
        KICK_REASON.CREATOR_LEFT: ('creatorLeft', False),
        KICK_REASON.PLAYERKICK: ('playerKick', False),
        KICK_REASON.TIMEOUT: ('timeout', False) }
    
    def format(self, message):
        LOG_DEBUG('prbDestruction', message)
        data = message.data
        type = data.get('type')
        team = data.get('team')
        wins = data.get('wins')
        kickReason = data.get('kickReason')
        if None in [
            type,
            team,
            wins,
            kickReason]:
            return None
        playerTeamWins = wins[team]
        if team == 1:
            pass
        1
        otherTeamWins = 2[1]
        winsLimit = data.get('winsLimit')
        if winsLimit > 0 and playerTeamWins < winsLimit and otherTeamWins < winsLimit:
            winner = None
        elif playerTeamWins == otherTeamWins:
            winner = 0
        elif wins[1] > wins[2]:
            pass
        
        winner = 2
        battleResult = self._makeBattleResultString(kickReason, winner, team)
        total = ''
        if data.get('battlesLimit', 0) > 1:
            total = '({0:d}:{1:d})'.format(wins[1], wins[2])
        
        return g_settings.msgTemplates.format('prebattleDestruction', ctx = {
            'desc': self._makeDescriptionString(data, showBattlesCount = False),
            'createdAt': self._makeCreateAtString(message),
            'opponents': self._getOpponentsString(data.get('opponents', { })),
            'result': battleResult,
            'total': total }, data = {
            'icon': self._getIconId(type) })



class VehCamouflageTimedOutFormatter(ServiceChannelFormatter):
    
    def notify(self):
        return True

    
    def format(self, message):
        data = message.data
        formatted = None
        vehTypeCompDescr = data.get('vehTypeCompDescr')
        if vehTypeCompDescr is not None:
            vType = vehicles_core.getVehicleType(vehTypeCompDescr)
            if vType is not None:
                formatted = g_settings.msgTemplates.format('vehCamouflageTimedOut', ctx = {
                    'vehicleName': vType.userString })
            
        
        return formatted



class VehEmblemTimedOutFormatter(ServiceChannelFormatter):
    
    def notify(self):
        return True

    
    def format(self, message):
        data = message.data
        formatted = None
        vehTypeCompDescr = data.get('vehTypeCompDescr')
        if vehTypeCompDescr is not None:
            vType = vehicles_core.getVehicleType(vehTypeCompDescr)
            if vType is not None:
                formatted = g_settings.msgTemplates.format('vehEmblemTimedOut', ctx = {
                    'vehicleName': vType.userString })
            
        
        return formatted



class VehInscriptionTimedOutFormatter(ServiceChannelFormatter):
    
    def notify(self):
        return True

    
    def format(self, message):
        data = message.data
        formatted = None
        vehTypeCompDescr = data.get('vehTypeCompDescr')
        if vehTypeCompDescr is not None:
            vType = vehicles_core.getVehicleType(vehTypeCompDescr)
            if vType is not None:
                formatted = g_settings.msgTemplates.format('vehInscriptionTimedOut', ctx = {
                    'vehicleName': vType.userString })
            
        
        return formatted



class ClientSysMessageFormatter(ServiceChannelFormatter):
    _ClientSysMessageFormatter__templateKey = '%sSysMessage'
    
    def format(self, data, auxData):
        type = auxData[0]
        return g_settings.msgTemplates.format(self._ClientSysMessageFormatter__templateKey % type, ctx = {
            'text': data })



class PremiumAccountExpiryFormatter(ServiceChannelFormatter):
    
    def format(self, data, auxData):
        return g_settings.msgTemplates.format('durationOfPremiumAccountExpires', ctx = {
            'expiryTime': getLongDatetimeFormat(data) })



class AOGASNotifyFormatter(ServiceChannelFormatter):
    
    def format(self, data, auxData):
        return g_settings.msgTemplates.format('AOGASNotify', {
            'text': i18n.makeString('#AOGAS:{0:>s}'.format(data.name())) })



class VehicleTypeLockExpired(ServiceChannelFormatter):
    
    def format(self, message):
        result = None
        if message.data:
            ctx = { }
            vehTypeCompDescr = message.data.get('vehTypeCompDescr')
            if vehTypeCompDescr is None:
                templateKey = 'vehiclesAllLockExpired'
            else:
                templateKey = 'vehicleLockExpired'
                ctx['vehicleName'] = vehicles_core.getVehicleType(vehTypeCompDescr).userString
            result = g_settings.msgTemplates.format(templateKey, ctx = ctx)
        
        return result



class ServerDowntimeCompensation(ServiceChannelFormatter):
    _ServerDowntimeCompensation__templateKey = 'serverDowntimeCompensation'
    
    def format(self, message):
        result = None
        subjects = ''
        data = message.data
        if data is not None:
            for (key, value) in data.items():
                if value:
                    if len(subjects) > 0:
                        subjects += ', '
                    
                    subjects += i18n.makeString('#%s:serviceChannelMessages/' % MESSENGER_I18N_FILE + self._ServerDowntimeCompensation__templateKey + '/' + key)
                    continue
            
            if len(subjects) > 0:
                result = g_settings.msgTemplates.format(self._ServerDowntimeCompensation__templateKey, ctx = {
                    'text': i18n.makeString('#%s:serviceChannelMessages/' % MESSENGER_I18N_FILE + self._ServerDowntimeCompensation__templateKey) % subjects })
            
        
        return result



class ActionNotificationFormatter(ServiceChannelFormatter):
    _ActionNotificationFormatter__templateKey = 'action%s'
    
    def format(self, message, *args):
        result = None
        data = message.get('data')
        if data:
            result = g_settings.msgTemplates.format(self._ActionNotificationFormatter__templateKey % message.get('state', ''), ctx = {
                'text': data }, data = {
                'icon': message.get('type', '') })
        
        return result



