# Source Generated with Decompyle++
# File: sub_parsers.pyc (Python 2.6)

from debug_utils import LOG_ERROR
from items import _xml, vehicles
from helpers.html import translation
import nations
from tutorial.control import triggers
from tutorial.data import chapter

def _parseID(xmlCtx, section, msg):
    id = section.asString
    if id is None or not len(id):
        _xml.raiseWrongXml(xmlCtx, section.name, msg)
    
    return id


def _readFlagCondition(xmlCtx, section, state, flags):
    flagID = _parseID(xmlCtx, section, 'Specify a flag ID')
    if flagID not in flags:
        flags.append(flagID)
    
    return chapter.FlagCondition(flagID, state)


def _readVehicleCondition(xmlCtx, section, varID):
    value = _parseID(xmlCtx, section, 'Specify a vehicle var value')
    return chapter.VehicleCondition(varID, value)

CONDITION_TAGS = {
    'active': (lambda xmlCtx, section, flags: _readFlagCondition(xmlCtx, section, chapter.FlagCondition.FLAG_ACTIVE, flags)),
    'inactive': (lambda xmlCtx, section, flags: _readFlagCondition(xmlCtx, section, chapter.FlagCondition.FLAG_INACTIVE, flags)),
    'cveh-type-name': (lambda xmlCtx, section, _: _readVehicleCondition(xmlCtx, section, chapter.VehicleCondition.CV_TYPE_NAME)) }

def _readConditions(xmlCtx, section, flags):
    result = chapter.Conditions()
    for (name, subSec) in section.items():
        if name == 'either':
            eitherCondition = _readConditions(xmlCtx, subSec, flags)
            result.appendEitherBlock(eitherCondition)
            continue
        function = CONDITION_TAGS.get(name)
        if function is None:
            LOG_ERROR('Condition is not supported: ', name)
            continue
        
        result.append(function(xmlCtx, subSec, flags))
    
    return result


def _parseConditions(xmlCtx, section, flags):
    condSec = section['condition']
    if condSec is not None:
        return _readConditions(xmlCtx, condSec, flags)

ACTION_TAGS = {
    'press': chapter.Action.PRESS,
    'click': chapter.Action.CLICK,
    'click-point': chapter.Action.CLICK_POINT,
    'close': chapter.Action.CLOSE,
    'change': chapter.Action.CHANGE,
    'click-item': chapter.Action.CLICK_ITEM,
    'press-item': chapter.Action.PRESS_ITEM,
    'change-text': chapter.Action.CHANGE_TEXT }

def _parseActions(xmlCtx, section, flags):
    result = []
    for (name, subSec) in section.items():
        type = ACTION_TAGS.get(name)
        if type is None:
            LOG_ERROR('Action is not supported: ', name)
            continue
        
        targetID = _parseID(xmlCtx, subSec, 'Specify a target ID')
        action = chapter.Action(type, targetID)
        if 'effects' in subSec.keys():
            for (_, effectSec) in _xml.getChildren(xmlCtx, subSec, 'effects'):
                effect = _parseEffect(xmlCtx, effectSec, flags)
                if effect is not None:
                    action.addEffect(effect)
                    continue
            
        
        result.append(action)
    
    return result


def _readActivateEffectSection(xmlCtx, section, flags, conditions):
    flagID = _parseID(xmlCtx, section, 'Specify a flag ID')
    if flagID not in flags:
        flags.append(flagID)
    
    return chapter.HasTargetEffect(flagID, chapter.Effect.ACTIVATE, conditions = conditions)


def _readDeactivateEffectSection(xmlCtx, section, flags, conditions):
    flagID = _parseID(xmlCtx, section, 'Specify a flag ID')
    if flagID not in flags:
        flags.append(flagID)
    
    return chapter.HasTargetEffect(flagID, chapter.Effect.DEACTIVATE, conditions = conditions)


def _readNextChapterEffectSection(xmlCtx, section, _, conditions):
    targetID = section.asString
    return chapter.HasTargetEffect(targetID, chapter.Effect.NEXT_CHAPTER, conditions = conditions)


def _readShowHintSection(xmlCtx, section, _, conditions):
    hintID = _parseID(xmlCtx, section, 'Specify a hint ID')
    return chapter.HasTargetEffect(hintID, chapter.Effect.SHOW_HINT, conditions = conditions)


def _readCloseHintSection(xmlCtx, section, _, conditions):
    hintID = _parseID(xmlCtx, section, 'Specify a hint ID')
    return chapter.HasTargetEffect(hintID, chapter.Effect.CLOSE_HINT, conditions = conditions)


def _readShowDialogSection(xmlCtx, section, _, conditions):
    dialogID = _parseID(xmlCtx, section, 'Specify a dialog ID')
    return chapter.HasTargetEffect(dialogID, chapter.Effect.SHOW_DIALOG, conditions = conditions)


def _readRunTriggerEffectSection(xmlCtx, section, _, conditions):
    triggerID = _parseID(xmlCtx, section, 'Specify a trigger ID')
    return chapter.HasTargetEffect(triggerID, chapter.Effect.RUN_TRIGGER, conditions = conditions)


def _readGuiItemDefinition(xmlCtx, section, _, conditions):
    newGuiItemId = _parseID(xmlCtx, section, 'Specify a new gui item ID')
    parentReferenceId = _xml.readString(xmlCtx, section, 'parent-ref')
    extraReferenceId = _xml.readString(xmlCtx, section, 'extra-ref')
    return chapter.DefineGuiItemEffect(newGuiItemId, chapter.Effect.DEFINE_GUI_ITEM, parentReferenceId, extraReferenceId, conditions = conditions)


def _readGuiItemPropertiesEffectSection(xmlCtx, section, _, conditions):
    itemID = _parseID(xmlCtx, section, 'Specify a item ID')
    props = { }
    for (_, subSec) in _xml.getChildren(xmlCtx, section, 'properties'):
        (propType, propSec) = subSec.items()[0]
        props[subSec.asString] = _readVarValue(propType, propSec)
    
    revert = section.readBool('revert')
    return chapter.SetGuiItemProperty(itemID, props, conditions = conditions, revert = revert)


def _readInvokeGuiCmdSection(xmlCtx, section, _, conditions):
    commandID = _parseID(xmlCtx, section, 'Specify a command ID')
    return chapter.HasTargetEffect(commandID, chapter.Effect.INVOKE_GUI_CMD, conditions = conditions)


def _readSetFilterSection(xmlCtx, section, _, conditions):
    filterID = _parseID(xmlCtx, section, 'Specify a filter ID')
    value = []
    for (name, subSec) in _xml.getChildren(xmlCtx, section, 'value'):
        value.append(_readVarValue(name, subSec))
    
    return chapter.SetFilter(filterID, tuple(value), conditions = conditions)

EFFECT_TAGS = {
    'activate': _readActivateEffectSection,
    'inactivate': _readDeactivateEffectSection,
    'show-hint': _readShowHintSection,
    'close-hint': _readCloseHintSection,
    'show-dialog': _readShowDialogSection,
    'refuse-training': (lambda xmlCtx, section, flags, conditions: chapter.SimpleEffect(chapter.Effect.REFUSE_TRAINING, conditions = conditions)),
    'next-chapter': _readNextChapterEffectSection,
    'run-trigger': _readRunTriggerEffectSection,
    'request-bonus': (lambda xmlCtx, section, flags, conditions: chapter.SimpleEffect(chapter.Effect.REQUEST_BONUS, conditions = conditions)),
    'set-gui-item-props': _readGuiItemPropertiesEffectSection,
    'finish-training': (lambda xmlCtx, section, flags, conditions: chapter.SimpleEffect(chapter.Effect.FINISH_TRAINING, conditions = conditions)),
    'define-gui-item': _readGuiItemDefinition,
    'invoke-gui-cmd': _readInvokeGuiCmdSection,
    'set-filter': _readSetFilterSection }

def _parseEffect(xmlCtx, section, flags, afterBattle = False):
    function = EFFECT_TAGS.get(section.name)
    result = None
    if 'after-battle-filter' in section.keys() and not afterBattle:
        return result
    if function is not None:
        result = function(xmlCtx, section, flags, _parseConditions(xmlCtx, section, flags))
    else:
        LOG_ERROR('Effect is not supported:', section.name)
    return result


def _readBonusSection(xmlCtx, section):
    bonusSec = _xml.getSubsection(xmlCtx, section, 'bonus')
    return [
        translation(_xml.readString(xmlCtx, bonusSec, 'value')),
        translation(_xml.readString(xmlCtx, bonusSec, 'label')),
        _xml.readString(xmlCtx, bonusSec, 'background')]


def _readGreetingDialogSection(xmlCtx, section, _, dialogID, type, title, text, buttons):
    image = _xml.readString(xmlCtx, section, 'image')
    bonus = _readBonusSection(xmlCtx, section)
    return chapter.GreetingDialog(dialogID, type, title, text, buttons, image, bonus)


def _readQuestDialogSection(xmlCtx, section, _, dialogID, type, title, text, buttons):
    quest = translation(_xml.readString(xmlCtx, section, 'quest'))
    image = _xml.readString(xmlCtx, section, 'image')
    bonus = _readBonusSection(xmlCtx, section)
    return chapter.QuestDialog(dialogID, type, title, text, buttons, image, bonus, quest)


def _readSubQuestDialogSection(xmlCtx, section, _, dialogID, type, title, text, buttons):
    quest = translation(_xml.readString(xmlCtx, section, 'quest'))
    image = _xml.readString(xmlCtx, section, 'image')
    return chapter.QuestDialog(dialogID, type, title, text, buttons, image, ('', '', ''), quest)


def _readQuestAndHelpDialogSection(xmlCtx, section, _, dialogID, type, title, text, buttons):
    quest = translation(_xml.readString(xmlCtx, section, 'quest'))
    image = _xml.readString(xmlCtx, section, 'image')
    bonus = _readBonusSection(xmlCtx, section)
    help = _xml.readString(xmlCtx, section, 'help')
    return chapter.QuestAndHelpDialog(dialogID, type, title, text, buttons, image, bonus, quest, help)


def _readQuestCompletedDialogSection(xmlCtx, section, _, dialogID, type, title, text, buttons):
    bonus = _readBonusSection(xmlCtx, section)
    hint = translation(_xml.readString(xmlCtx, section, 'hint'))
    submit = translation(_xml.readString(xmlCtx, section, 'submit-label'))
    return chapter.QuestCompletedDialog(dialogID, type, title, text, buttons, None, bonus, hint, submit)


def _readVarRefDialogSection(xmlCtx, section, _, dialogID, type, title, text, buttons):
    image = _xml.readString(xmlCtx, section, 'image')
    varRef = _xml.readString(xmlCtx, section, 'var-ref')
    return chapter.VarRefDialog(dialogID, type, title, text, buttons, image, varRef)

DIALOG_SUB_PARERS = {
    'greeting': _readGreetingDialogSection,
    'quest': _readQuestDialogSection,
    'subQuest': _readSubQuestDialogSection,
    'questAndHelp': _readQuestAndHelpDialogSection,
    'questCompleted': _readQuestCompletedDialogSection,
    'finished': _readQuestCompletedDialogSection,
    'vehicleItemInfo': _readVarRefDialogSection,
    'tankmanSkill': _readVarRefDialogSection }

def _parseDialog(xmlCtx, section, flags):
    dialogID = _parseID(xmlCtx, section, 'Specify a dialog ID')
    type = _xml.readString(xmlCtx, section, 'type')
    title = translation(_xml.readString(xmlCtx, section, 'title'))
    text = translation(_xml.readString(xmlCtx, section, 'text'))
    buttonsSec = _xml.getSubsection(xmlCtx, section, 'buttons')
    buttons = [
        _xml.readString(xmlCtx, buttonsSec, 'submit'),
        buttonsSec.readString('cancel', '')]
    parser = DIALOG_SUB_PARERS.get(type)
    if parser is not None:
        dialog = parser(xmlCtx, section, flags, dialogID, type, title, text, buttons)
    else:
        dialog = chapter.Dialog(dialogID, type, title, text, buttons, section.readString('image'))
    dialog.setActions(_parseActions(xmlCtx, _xml.getSubsection(xmlCtx, section, 'actions'), flags))
    return dialog


def _parseHint(xmlCtx, section, _):
    hintID = _parseID(xmlCtx, section, 'Specify a hint ID')
    targetID = _xml.readString(xmlCtx, section, 'gui-item-ref')
    containerID = section.readString('container-ref')
    if not len(containerID):
        containerID = None
    
    text = translation(_xml.readString(xmlCtx, section, 'text'))
    inPin = _xml.readString(xmlCtx, section, 'inPin')
    outPin = _xml.readString(xmlCtx, section, 'outPin')
    line = _xml.readString(xmlCtx, section, 'line')
    position = section.readVector2('position')
    topmostLevel = section.readBool('topmost-level', True)
    return chapter.Hint(hintID, targetID, containerID, position, text, inPin, outPin, line, topmostLevel)


def _parseLockedArea(xmlCtx, section, flags):
    area = chapter.Area(_parseID(xmlCtx, section, 'Specify a area ID'), _parseConditions(xmlCtx, section, flags))
    if 'gui-item-ref' in section.keys():
        area.setTargetID(_xml.readString(xmlCtx, section, 'gui-item-ref'))
    
    return area


def _parseActiveArea(xmlCtx, section, flags):
    area = _parseLockedArea(xmlCtx, section, flags)
    if 'use-mask' in section.keys():
        area.setUseMask(section.readBool('use-mask', False), section.readString('hide-mask', 'alpha'))
    
    area.setActions(_parseActions(xmlCtx, _xml.getSubsection(xmlCtx, section, 'actions'), flags))
    return area


def _readValidateVarTriggerSection(xmlCtx, section, triggerID, clazz, **kwargs):
    validateVarID = _xml.readString(xmlCtx, section, 'validate-var')
    setVarID = section.readString('set-var')
    if not len(setVarID):
        setVarID = None
    
    return clazz(triggerID, validateVarID, setVarID = setVarID, **None)


def _readItemUnlockedTriggerSection(xmlCtx, section, _, triggerID):
    return _readValidateVarTriggerSection(xmlCtx, section, triggerID, triggers.ItemUnlockedTrigger, validateUpdateOnly = 'validate-update-only' in section.keys())


def _readInventoryItemTriggerSection(xmlCtx, section, _, triggerID):
    itemTypeID = _xml.readInt(xmlCtx, section, 'item-type-id')
    return _readValidateVarTriggerSection(xmlCtx, section, triggerID, triggers.InventoryItemTrigger, itemTypeID = itemTypeID)


def _readCurrentVehicleTriggerSection(xmlCtx, section, _, triggerID):
    isLockedFlagID = section.readString('locked')
    if not len(isLockedFlagID):
        isLockedFlagID = None
    
    isCrewFullFlagID = section.readString('crew-full')
    if not len(isCrewFullFlagID):
        isCrewFullFlagID = None
    
    return _readValidateVarTriggerSection(xmlCtx, section, triggerID, triggers.CurrentVehicleTrigger, isLockedFlagID = isLockedFlagID, isCrewFullFlagID = isCrewFullFlagID)


def _readItemXPTriggerSection(xmlCtx, section, _, triggerID):
    vehicleVarID = _xml.readString(xmlCtx, section, 'vehicle-var')
    return _readValidateVarTriggerSection(xmlCtx, section, triggerID, triggers.ItemExperienceTrigger, vehicleVarID = vehicleVarID)


def _readTankmanLevelTriggerSection(xmlCtx, section, _, triggerID):
    role = _xml.readString(xmlCtx, section, 'role')
    roleLevel = _xml.readInt(xmlCtx, section, 'role-level')
    inVehicleFlagID = _xml.readString(xmlCtx, section, 'in-vehicle')
    specVehicleFlagID = section.readString('spec-vehicle')
    if not len(specVehicleFlagID):
        specVehicleFlagID = None
    
    setVarID = section.readString('set-var')
    if not len(setVarID):
        setVarID = None
    
    return triggers.TankmanLevelTrigger(triggerID, role, roleLevel, setVarID, inVehicleFlagID, specVehicleFlagID)

TRIGGER_SUB_PARSERS = {
    'bonus': (lambda xmlCtx, section, chapter, triggerID: triggers.BonusTrigger(triggerID, chapter.getBonusID())),
    'battleCount': (lambda xmlCtx, section, chapter, triggerID: _readValidateVarTriggerSection(xmlCtx, section, triggerID, triggers.BattleCountRequester)),
    'unlocked': _readItemUnlockedTriggerSection,
    'installed': (lambda xmlCtx, section, chapter, triggerID: _readValidateVarTriggerSection(xmlCtx, section, triggerID, triggers.ItemInstalledTrigger)),
    'vehicleSetting': (lambda xmlCtx, section, chapter, triggerID: _readValidateVarTriggerSection(xmlCtx, section, triggerID, triggers.VehicleSettingTrigger)),
    'eliteVehicle': (lambda xmlCtx, section, chapter, triggerID: _readValidateVarTriggerSection(xmlCtx, section, triggerID, triggers.EliteVehicleTrigger)),
    'accCredits': (lambda xmlCtx, section, chapter, triggerID: _readValidateVarTriggerSection(xmlCtx, section, triggerID, triggers.AccountCreditsTrigger)),
    'itemPrice': (lambda xmlCtx, section, chapter, triggerID: _readValidateVarTriggerSection(xmlCtx, section, triggerID, triggers.ItemPriceTrigger)),
    'eqInstalled': (lambda xmlCtx, section, chapter, triggerID: _readValidateVarTriggerSection(xmlCtx, section, triggerID, triggers.EquipmentInstalledTrigger)),
    'inventory': _readInventoryItemTriggerSection,
    'currentVehicle': _readCurrentVehicleTriggerSection,
    'cVehCrew': (lambda xmlCtx, section, chapter, triggerID: triggers.CurVehicleCrewTrigger(triggerID)),
    'cVehLocked': (lambda xmlCtx, section, chapter, triggerID: triggers.CurVehicleLockedTrigger(triggerID)),
    'itemXP': _readItemXPTriggerSection,
    'tankmanLevel': _readTankmanLevelTriggerSection,
    'tankmanSkill': (lambda xmlCtx, section, chapter, triggerID: _readValidateVarTriggerSection(xmlCtx, section, triggerID, triggers.TankmanSkillTrigger)),
    'freeVehSlot': (lambda xmlCtx, section, chapter, triggerID: triggers.FreeVehicleSlotTrigger(triggerID)) }

def _parseTrigger(xmlCtx, section, flags, chapter):
    triggerID = _parseID(xmlCtx, section, 'Specify a trigger ID')
    trigger = None
    type = _xml.readString(xmlCtx, section, 'type')
    parser = TRIGGER_SUB_PARSERS.get(type)
    if parser is not None:
        trigger = parser(xmlCtx, section, chapter, triggerID)
        if 'on-effects' in section.keys():
            for (_, effectSec) in _xml.getChildren(xmlCtx, section, 'on-effects'):
                effect = _parseEffect(xmlCtx, effectSec, flags)
                if effect is not None:
                    trigger.addOnEffect(effect)
                    continue
            
        
        if 'off-effects' in section.keys():
            for (_, effectSec) in _xml.getChildren(xmlCtx, section, 'off-effects'):
                effect = _parseEffect(xmlCtx, effectSec, flags)
                if effect is not None:
                    trigger.addOffEffect(effect)
                    continue
            
        
        if 'exclude-triggers' in section.keys():
            for (_, triggerSec) in _xml.getChildren(xmlCtx, section, 'exclude-triggers'):
                trigger.addExcludeTriggerID(triggerSec.asString)
            
        
    else:
        LOG_ERROR('TUTORIAL. Trigger is not supported:', type)
    return trigger


def _readPermanentGuiItemSection(xmlCtx, section, itemFlags, itemID, props, conditions):
    return chapter.PermanentGuiItemRef(itemID, props, conditions = conditions)


def _readDynamicGuiItemSection(xmlCtx, section, itemFlags, itemID, props, conditions):
    item = chapter.DynamicGuiItemRef(itemID, props, conditions = conditions)
    if 'find-criteria' in section.keys():
        subSec = _xml.getSubsection(xmlCtx, section, 'find-criteria')
        parentID = _xml.readString(xmlCtx, subSec, 'parent-ref')
        varPath = _xml.readString(xmlCtx, subSec, 'var-path')
        varRef = _xml.readString(xmlCtx, subSec, 'var-ref')
        item.setFindCriteria([
            parentID,
            varPath,
            varRef])
    
    for (_, effectSec) in _xml.getChildren(xmlCtx, section, 'not-on-scene-effects'):
        effect = _parseEffect(xmlCtx, effectSec, itemFlags)
        if effect is not None:
            item.addNotOnSceneEffect(effect)
            continue
    
    for (_, effectSec) in _xml.getChildren(xmlCtx, section, 'on-scene-effects'):
        effect = _parseEffect(xmlCtx, effectSec, itemFlags)
        if effect is not None:
            item.addOnSceneEffect(effect)
            continue
    
    return item

GUI_ITEMS_SUB_PARSERS = {
    'permanent': _readPermanentGuiItemSection,
    'dynamic': _readDynamicGuiItemSection }

def _parseGuiItem(xmlCtx, section, flags, itemFlags):
    itemID = _parseID(xmlCtx, section, 'Specify a GUI item ID')
    lifeCycle = _xml.readString(xmlCtx, section, 'life-cycle')
    parser = GUI_ITEMS_SUB_PARSERS.get(lifeCycle)
    item = None
    if parser is not None:
        props = { }
        if 'properties' in section.keys():
            for (_, subSec) in _xml.getChildren(xmlCtx, section, 'properties'):
                (propType, propSec) = subSec.items()[0]
                props[subSec.asString] = _readVarValue(propType, propSec)
            
        
        item = parser(xmlCtx, section, itemFlags, itemID, props, _parseConditions(xmlCtx, section, flags))
    else:
        LOG_ERROR('Gui item is not supported:', lifeCycle)
    return item


def _readAsStringSection(name, section):
    return translation(getattr(section, name))


def _readAsListSection(_, section):
    value = []
    for (name, subSec) in section.items():
        if name == 'condition':
            continue
        
        value.append(_readVarValue(name, subSec))
    
    return value


def _readAsIntSequence(_, section):
    return map((lambda item: if len(item):
int(item)), section.asString.split(' '))


def _readAsVehTypeNameSection(_, section):
    return vehicles.makeIntCompactDescrByID('vehicle', *vehicles.g_list.getIDsByName(section.asString))


def _readAsVehItemNameSection(itemName, itemIDsMethod, section):
    (nationName, chassisName) = section.asString.split(':')
    nationID = nations.INDICES[nationName]
    itemGetter = getattr(vehicles.g_cache, itemIDsMethod)
    return vehicles.makeIntCompactDescrByID(itemName, nationID, itemGetter(nationID)[chassisName])


def _readAsEquipmentSection(_, section):
    equipmentName = section.asString
    return vehicles.makeIntCompactDescrByID('equipment', nations.NONE_INDEX, vehicles.g_cache.equipmentIDs()[equipmentName])

CUSTOM_VARS_PARERS = {
    'asString': _readAsStringSection,
    'asList': _readAsListSection,
    'asIntSequence': _readAsIntSequence,
    'asVehTypeName': _readAsVehTypeNameSection,
    'asVehChassisName': (lambda name, section: _readAsVehItemNameSection('vehicleChassis', 'chassisIDs', section)),
    'asVehGunName': (lambda name, section: _readAsVehItemNameSection('vehicleGun', 'gunIDs', section)),
    'asVehEngineName': (lambda name, section: _readAsVehItemNameSection('vehicleEngine', 'engineIDs', section)),
    'asVehRadioName': (lambda name, section: _readAsVehItemNameSection('vehicleRadio', 'radioIDs', section)),
    'asVehTurretName': (lambda name, section: _readAsVehItemNameSection('vehicleTurret', 'turretIDs', section)),
    'asEquipment': _readAsEquipmentSection }

def _readVarValue(name, section):
    if name in CUSTOM_VARS_PARERS:
        value = CUSTOM_VARS_PARERS[name](name, section)
    else:
        value = getattr(section, name)
    return value


def _parseVarSet(xmlCtx, section, flags):
    varID = _parseID(xmlCtx, section, 'Specify a var ID')
    varSet = []
    for (name, subSec) in section.items():
        value = _readVarValue(name, subSec)
        varSet.append((value, _parseConditions(xmlCtx, subSec, flags)))
    
    return chapter.VarSet(varID, varSet)


