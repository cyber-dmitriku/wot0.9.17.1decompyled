# Source Generated with Decompyle++
# File: chapter.pyc (Python 2.6)

from tutorial.data import HasID, HasTargetID

class Chapter(HasID):
    
    def __init__(self, id, title, descriptions, bonusID, bonusMsg, forcedLoading, filePaths):
        self._Chapter__id = id
        self._Chapter__title = title
        self._Chapter__descriptions = descriptions
        self._Chapter__bonusID = bonusID
        self._Chapter__bonusMsg = bonusMsg
        self._Chapter__forcedLoading = forcedLoading
        self._Chapter__filePaths = filePaths
        self._Chapter__initialSceneID = None
        self._Chapter__defaultSceneID = None
        self._Chapter__scenes = []
        self._Chapter__sceneMap = { }
        self._Chapter__flags = []
        self._Chapter__hints = { }
        self._Chapter__dialogs = { }
        self._Chapter__triggers = { }
        self._Chapter__varSets = []
        self._Chapter__infoConditions = None
        self._Chapter__valid = False

    
    def getTitle(self):
        return self._Chapter__title

    
    def getDescription(self, afterBattle = False):
        if afterBattle:
            pass
        1
        return 1[0]

    
    def getBonusID(self):
        return self._Chapter__bonusID

    
    def hasBonus(self):
        return self._Chapter__bonusID > -1

    
    def ignoreBonus(self, bonusCompleted):
        if not self.hasBonus() and self._Chapter__forcedLoading != -1:
            pass
        return self._Chapter__forcedLoading == bonusCompleted

    
    def getBonusMessage(self):
        return self._Chapter__bonusMsg

    
    def isBonusReceived(self, bonusCompleted):
        return 1 << self._Chapter__bonusID & bonusCompleted != 0

    
    def getFilePath(self, afterBattle = False):
        if afterBattle:
            pass
        1
        return 1[0]

    
    def getID(self):
        return self._Chapter__id

    
    def setID(self, id):
        self._Chapter__id = id

    
    def setInitialSceneID(self, initialSceneID):
        self._Chapter__initialSceneID = initialSceneID

    
    def setDefaultSceneID(self, defaultSceneID):
        self._Chapter__defaultSceneID = defaultSceneID

    
    def getFlags(self):
        return self._Chapter__flags[:]

    
    def setFlags(self, flags):
        self._Chapter__flags = flags

    
    def addScene(self, scene):
        self._Chapter__sceneMap[scene.getID()] = len(self._Chapter__scenes)
        self._Chapter__scenes.append(scene)

    
    def getScene(self, sceneID):
        scene = None
        if sceneID in self._Chapter__sceneMap:
            scene = self._Chapter__scenes[self._Chapter__sceneMap[sceneID]]
        elif self._Chapter__defaultSceneID in self._Chapter__sceneMap:
            scene = self._Chapter__scenes[self._Chapter__sceneMap[self._Chapter__defaultSceneID]]
            scene.setID(sceneID)
        
        return scene

    
    def getInitialScene(self):
        initialScene = None
        if self._Chapter__initialSceneID in self._Chapter__sceneMap:
            initialScene = self._Chapter__scenes[self._Chapter__sceneMap[self._Chapter__initialSceneID]]
        
        if initialScene is None and len(self._Chapter__scenes):
            initialScene = self._Chapter__scenes[0]
        
        return initialScene

    
    def addHint(self, hint):
        self._Chapter__hints[hint.getID()] = hint

    
    def getHint(self, hintID):
        return self._Chapter__hints.get(hintID)

    
    def addDialog(self, dialog):
        self._Chapter__dialogs[dialog.getID()] = dialog

    
    def getDialog(self, dialogID):
        return self._Chapter__dialogs.get(dialogID)

    
    def addTrigger(self, trigger):
        self._Chapter__triggers[trigger.getID()] = trigger

    
    def getTrigger(self, triggerID):
        return self._Chapter__triggers.get(triggerID)

    
    def addVarSet(self, varSet):
        self._Chapter__varSets.append(varSet)

    
    def getVarSets(self):
        return self._Chapter__varSets[:]

    
    def setInfoConditions(self, conditions):
        self._Chapter__infoConditions = conditions

    
    def getInfoConditions(self):
        return self._Chapter__infoConditions

    
    def clear(self):
        self._Chapter__valid = False
        self._Chapter__flags = []
        self._Chapter__varSets = []
        if self._Chapter__infoConditions is not None:
            self._Chapter__infoConditions.clear()
        
        self._Chapter__infoConditions = None
        self._Chapter__sceneMap.clear()
        while len(self._Chapter__scenes):
            self._Chapter__scenes.pop().clear()
        while len(self._Chapter__hints):
            self._Chapter__hints.popitem()
        while len(self._Chapter__dialogs):
            (_, item) = self._Chapter__dialogs.popitem()
            item.clear()
        while len(self._Chapter__triggers):
            (_, item) = self._Chapter__triggers.popitem()
            item.clear()

    
    def isValid(self):
        return self._Chapter__valid

    
    def setValid(self, flag):
        self._Chapter__valid = flag



class Scene(HasID):
    
    def __init__(self, id = None):
        super(Scene, self).__init__()
        self._Scene__id = id
        self._Scene__lockedAreas = []
        self._Scene__activeAreas = []
        self._Scene__postEffects = []
        self._Scene__guiItems = []
        self._Scene__effects = []

    
    def getID(self):
        return self._Scene__id

    
    def setID(self, id):
        self._Scene__id = id

    
    def addLockedArea(self, area):
        self._Scene__lockedAreas.append(area)

    
    def getLockedAreas(self):
        return self._Scene__lockedAreas[:]

    
    def addActiveArea(self, area):
        self._Scene__activeAreas.append(area)

    
    def getActiveAreas(self):
        return self._Scene__activeAreas[:]

    
    def addPostEffect(self, postEffect):
        self._Scene__postEffects.append(postEffect)

    
    def getPostEffects(self):
        return self._Scene__postEffects[:]

    
    def addEffect(self, effect):
        self._Scene__effects.append(effect)

    
    def getEffects(self):
        return self._Scene__effects[:]

    
    def addGuiItem(self, item):
        self._Scene__guiItems.append(item)

    
    def getGuiItems(self):
        return self._Scene__guiItems[:]

    
    def clear(self):
        while len(self._Scene__lockedAreas):
            self._Scene__lockedAreas.pop().clear()
        while len(self._Scene__activeAreas):
            self._Scene__activeAreas.pop().clear()
        while len(self._Scene__postEffects):
            self._Scene__postEffects.pop().clear()
        while len(self._Scene__guiItems):
            self._Scene__guiItems.pop().clear()
        while len(self._Scene__effects):
            self._Scene__effects.pop().clear()



class Effect(object):
    ACTIVATE = 0
    DEACTIVATE = 1
    SHOW_HINT = 2
    CLOSE_HINT = 3
    SHOW_DIALOG = 4
    REFUSE_TRAINING = 5
    NEXT_CHAPTER = 6
    RUN_TRIGGER = 7
    REQUEST_BONUS = 8
    SET_ITEM_PROPS = 9
    FINISH_TRAINING = 10
    DEFINE_GUI_ITEM = 11
    INVOKE_GUI_CMD = 12
    SET_FILTER = 13
    
    def __init__(self, conditions = None):
        super(Effect, self).__init__()
        self._Effect__conditions = conditions

    
    def getType(self):
        raise NotImplementedError, 'Effect.getType not implemented'

    
    def getConditions(self):
        return self._Effect__conditions

    
    def clear(self):
        if self._Effect__conditions is not None:
            self._Effect__conditions.clear()
        
        self._Effect__conditions = None


continue
EFFECT_TYPE_NAMES = _[1](_[1][(v, k)])

class SimpleEffect(Effect):
    
    def __init__(self, type, conditions = None):
        super(SimpleEffect, self).__init__(conditions = conditions)
        self._SimpleEffect__type = type

    
    def __repr__(self):
        return 'SimpleEffect(type = {0!r:s})'.format(EFFECT_TYPE_NAMES.get(self._SimpleEffect__type))

    
    def getType(self):
        return self._SimpleEffect__type



class HasTargetEffect(SimpleEffect, HasTargetID):
    
    def __init__(self, targetID, type, conditions = None):
        super(HasTargetEffect, self).__init__(type, conditions = conditions)
        self._HasTargetEffect__targetID = targetID

    
    def __repr__(self):
        return 'HasTargetEffect(type = {0!r:s}, targetID = {1:>s})'.format(EFFECT_TYPE_NAMES.get(self.getType()), self._HasTargetEffect__targetID)

    
    def getTargetID(self):
        return self._HasTargetEffect__targetID

    
    def setTargetID(self, targetID):
        self._HasTargetEffect__targetID = targetID



class DefineGuiItemEffect(HasTargetEffect):
    
    def __init__(self, targetID, type, parentRef, extraRef, conditions = None):
        super(DefineGuiItemEffect, self).__init__(targetID, type, conditions = conditions)
        self._DefineGuiItemEffect__parentRef = parentRef
        self._DefineGuiItemEffect__extraRef = extraRef

    
    def __repr__(self):
        return ('HasTargetEffect(type = {0!r:s}, targetID = {1:>s}, ' + 'parent = {2:>s}, extra-ref = {3:>s}').format(EFFECT_TYPE_NAMES.get(self.getType()), self.getTargetID(), self._DefineGuiItemEffect__parentRef, self._DefineGuiItemEffect__extraRef)

    
    def getParentReference(self):
        return self._DefineGuiItemEffect__parentRef

    
    def getExtraReference(self):
        return self._DefineGuiItemEffect__extraRef



class SetGuiItemProperty(HasTargetEffect):
    
    def __init__(self, targetID, props, conditions = None, revert = False):
        super(SetGuiItemProperty, self).__init__(targetID, Effect.SET_ITEM_PROPS, conditions = conditions)
        self._SetGuiItemProperty__props = props
        self._SetGuiItemProperty__revert = revert

    
    def getProps(self):
        return self._SetGuiItemProperty__props.copy()

    
    def isRevert(self):
        return self._SetGuiItemProperty__revert

    
    def clear(self):
        super(SetGuiItemProperty, self).clear()
        self._SetGuiItemProperty__props.clear()



class SetFilter(HasTargetEffect):
    
    def __init__(self, targetID, value, conditions = None):
        super(SetFilter, self).__init__(targetID, Effect.SET_FILTER, conditions = conditions)
        self._SetFilter__value = value

    
    def getValue(self):
        return self._SetFilter__value[:]



class Conditions(list):
    
    def __init__(self, *args):
        list.__init__(self, *args)
        self._eitherBlocks = []

    
    def __repr__(self):
        return 'Conditions({0:s}): {1!r:s}, {2!r:s}'.format(hex(id(self)), self[:], self._eitherBlocks)

    
    def appendEitherBlock(self, block):
        self._eitherBlocks.append(block)

    
    def eitherBlocks(self):
        return self._eitherBlocks[:]

    
    def clear(self):
        while len(self._eitherBlocks):
            self._eitherBlocks.pop()
        while len(self):
            self.pop()



class Condition(HasID):
    FLAG_CONDITION = 0
    VEHICLE_CONDITION = 1
    
    def __init__(self, type, id):
        super(Condition, self).__init__()
        self._type = type
        self._id = id

    
    def getID(self):
        return self._id

    
    def setID(self, id):
        self._id = id

    
    def getType(self):
        return self._type



class FlagCondition(Condition):
    FLAG_ACTIVE = 0
    FLAG_INACTIVE = 1
    
    def __init__(self, id, state = 0):
        super(FlagCondition, self).__init__(Condition.FLAG_CONDITION, id)
        self._state = state

    
    def isActiveState(self):
        return self._state == FlagCondition.FLAG_ACTIVE

    
    def isInactiveState(self):
        return self._state == FlagCondition.FLAG_INACTIVE



class VehicleCondition(Condition):
    CV_TYPE_NAME = 0
    
    def __init__(self, varID, value):
        super(VehicleCondition, self).__init__(Condition.VEHICLE_CONDITION, varID)
        self._value = value

    
    def isValueEqual(self, other):
        return self._value == other



class Hint(HasID, HasTargetID):
    
    def __init__(self, id, targetID, containerID, position, text, inPin, outPin, line, topmostLevel):
        super(Hint, self).__init__()
        self._Hint__id = id
        self._Hint__targetID = targetID
        self._Hint__containerID = containerID
        self._Hint__position = position
        self._Hint__text = text
        self._Hint__inPin = inPin
        self._Hint__outPin = outPin
        self._Hint__line = line
        self._Hint__topmostLevel = topmostLevel

    
    def getID(self):
        return self._Hint__id

    
    def setID(self, id):
        self._Hint__id = id

    
    def getTargetID(self):
        return self._Hint__targetID

    
    def setTargetID(self, targetID):
        self._Hint__targetID = targetID

    
    def getContainerID(self):
        return self._Hint__containerID

    
    def setContainerID(self, containerID):
        self._Hint__containerID = containerID

    
    def getData(self):
        return [
            self._Hint__id,
            self._Hint__position[0],
            self._Hint__position[1],
            self._Hint__text,
            self._Hint__inPin,
            self._Hint__outPin,
            self._Hint__line,
            self._Hint__topmostLevel]



class Dialog(HasID):
    
    def __init__(self, id, type, title, text, buttons, image):
        super(Dialog, self).__init__()
        self._Dialog__id = id
        self._Dialog__title = title
        self._Dialog__text = text
        self._Dialog__buttons = buttons
        self._Dialog__image = image
        self._Dialog__actions = { }
        self._Dialog__type = type

    
    def getID(self):
        return self._Dialog__id

    
    def setID(self, id):
        self._Dialog__id = id

    
    def getType(self):
        return self._Dialog__type

    
    def getData(self):
        return [
            self.getType(),
            self._Dialog__id,
            self._Dialog__buttons[0],
            self._Dialog__buttons[1],
            self._Dialog__title,
            self._Dialog__text,
            self._Dialog__image]

    
    def isDataFull(self):
        return True

    
    def addAction(self, action):
        self._Dialog__actions[action.getTargetID()] = action

    
    def getAction(self, targetID):
        return self._Dialog__actions.get(targetID)

    
    def setActions(self, actions):
        self._Dialog__actions = dict(map((lambda action: (action.getTargetID(), action)), actions))

    
    def clear(self):
        while len(self._Dialog__actions):
            (_, action) = self._Dialog__actions.popitem()
            action.clear()



class GreetingDialog(Dialog):
    
    def __init__(self, id, type, title, text, size, buttons, bonus):
        super(GreetingDialog, self).__init__(id, type, title, text, size, buttons)
        self._GreetingDialog__bonus = bonus

    
    def getData(self):
        data = super(GreetingDialog, self).getData()
        data.extend(self._GreetingDialog__bonus)
        return data



class QuestDialog(GreetingDialog):
    
    def __init__(self, id, type, title, text, buttons, image, bonus, quest):
        super(QuestDialog, self).__init__(id, type, title, text, buttons, image, bonus)
        self._QuestDialog__quest = quest

    
    def getData(self):
        data = super(QuestDialog, self).getData()
        data.append(self._QuestDialog__quest)
        return data



class QuestAndHelpDialog(QuestDialog):
    
    def __init__(self, id, type, title, text, buttons, image, bonus, quest, help):
        super(QuestAndHelpDialog, self).__init__(id, type, title, text, buttons, image, bonus, quest)
        self._QuestAndHelpDialog__help = help

    
    def getData(self):
        data = super(QuestAndHelpDialog, self).getData()
        data.append(self._QuestAndHelpDialog__help)
        return data



class QuestCompletedDialog(GreetingDialog):
    
    def __init__(self, id, type, title, text, buttons, image, bonus, hint, submit):
        super(QuestCompletedDialog, self).__init__(id, type, title, text, buttons, image, bonus)
        self._QuestCompletedDialog__hint = hint
        self._QuestCompletedDialog__submit = submit

    
    def getData(self):
        data = super(QuestCompletedDialog, self).getData()
        data.append(self._QuestCompletedDialog__hint)
        data.append(self._QuestCompletedDialog__submit)
        return data



class VarRefDialog(Dialog):
    
    def __init__(self, id, type, title, text, buttons, image, varRef):
        super(VarRefDialog, self).__init__(id, type, title, text, buttons, image)
        self._VarRefDialog__varRef = varRef

    
    def getVarRef(self):
        return self._VarRefDialog__varRef

    
    def isDataFull(self):
        return False



class Action(HasTargetID):
    PRESS = 0
    CLICK = 1
    CLICK_POINT = 2
    CLOSE = 3
    CHANGE = 4
    CLICK_ITEM = 5
    PRESS_ITEM = 6
    CHANGE_TEXT = 7
    
    def __init__(self, type, targetID):
        super(Action, self).__init__()
        self._Action__type = type
        self._Action__targetID = targetID
        self._Action__effects = []

    
    def getTargetID(self):
        return self._Action__targetID

    
    def setTargetID(self, id):
        self._Action__targetID = id

    
    def getType(self):
        return self._Action__type

    
    def addEffect(self, effect):
        self._Action__effects.append(effect)

    
    def getEffects(self):
        return self._Action__effects[:]

    
    def clear(self):
        while len(self._Action__effects):
            self._Action__effects.pop().clear()



class Area(HasID, HasTargetID):
    
    def __init__(self, id, conditions = None, useMask = False, hideMask = 'alpha'):
        super(Area, self).__init__()
        self._Area__id = id
        self._Area__targetID = None
        self._Area__conditions = conditions
        self._Area__actions = { }
        self._Area__useMask = useMask
        self._Area__hideMask = hideMask

    
    def getID(self):
        return self._Area__id

    
    def setID(self, id):
        self._Area__id = id

    
    def getTargetID(self):
        return self._Area__targetID

    
    def setTargetID(self, id):
        self._Area__targetID = id

    
    def getConditions(self):
        return self._Area__conditions

    
    def addAction(self, action):
        self._Area__actions[action.getTargetID()] = action

    
    def getAction(self, targetID):
        return self._Area__actions.get(targetID)

    
    def getActions(self):
        return self._Area__actions.copy()

    
    def setActions(self, actions):
        self._Area__actions = dict(map((lambda action: (action.getTargetID(), action)), actions))

    
    def isUseMask(self):
        return self._Area__useMask

    
    def getHideMaskMode(self):
        return self._Area__hideMask

    
    def setUseMask(self, flag, hide = 'alpha'):
        self._Area__useMask = flag
        self._Area__hideMask = hide

    
    def clear(self):
        if self._Area__conditions is not None:
            self._Area__conditions.clear()
        
        self._Area__conditions = None
        while len(self._Area__actions):
            (_, action) = self._Area__actions.popitem()
            action.clear()



class GuiItemRef(HasTargetID):
    LIFE_CYCLE_PERMANENT = 0
    LIFE_CYCLE_DYNAMIC = 1
    
    def __init__(self, targetID, props, conditions = None):
        super(GuiItemRef, self).__init__()
        self._GuiItemRef__targetID = targetID
        self._GuiItemRef__props = props
        self._GuiItemRef__conditions = conditions

    
    def getTargetID(self):
        return self._GuiItemRef__targetID

    
    def setTargetID(self, id):
        self._GuiItemRef__targetID = id

    
    def getProps(self):
        return self._GuiItemRef__props.copy()

    
    def getLifeCycle(self):
        raise NotImplementedError, 'GuiItemRef.getLifeCycle not implemented'

    
    def getConditions(self):
        return self._GuiItemRef__conditions

    
    def clear(self):
        self._GuiItemRef__props.clear()
        if self._GuiItemRef__conditions is not None:
            self._GuiItemRef__conditions.clear()
        
        self._GuiItemRef__conditions = None



class PermanentGuiItemRef(GuiItemRef):
    
    def getLifeCycle(self):
        return GuiItemRef.LIFE_CYCLE_PERMANENT



class DynamicGuiItemRef(GuiItemRef):
    
    def __init__(self, targetID, props, conditions = None):
        super(DynamicGuiItemRef, self).__init__(targetID, props, conditions)
        self._DynamicGuiItemRef__findCriteria = None
        self._DynamicGuiItemRef__notOnSceneEffects = []
        self._DynamicGuiItemRef__onSceneEffects = []

    
    def getLifeCycle(self):
        return GuiItemRef.LIFE_CYCLE_DYNAMIC

    
    def addNotOnSceneEffect(self, effect):
        self._DynamicGuiItemRef__notOnSceneEffects.append(effect)

    
    def getNotOnSceneEffects(self):
        return self._DynamicGuiItemRef__notOnSceneEffects[:]

    
    def addOnSceneEffect(self, effect):
        self._DynamicGuiItemRef__onSceneEffects.append(effect)

    
    def getOnSceneEffects(self):
        return self._DynamicGuiItemRef__onSceneEffects[:]

    
    def setFindCriteria(self, criteria):
        self._DynamicGuiItemRef__findCriteria = criteria

    
    def getFindCriteria(self):
        if self._DynamicGuiItemRef__findCriteria:
            return self._DynamicGuiItemRef__findCriteria[:]

    
    def clear(self):
        super(DynamicGuiItemRef, self).clear()
        self._DynamicGuiItemRef__findCriteria = None
        while len(self._DynamicGuiItemRef__notOnSceneEffects):
            self._DynamicGuiItemRef__notOnSceneEffects.pop().clear()
        while len(self._DynamicGuiItemRef__onSceneEffects):
            self._DynamicGuiItemRef__onSceneEffects.pop().clear()



class VarSet(HasID):
    
    def __init__(self, id, varSet):
        super(VarSet, self).__init__()
        self._VarSet__id = id
        self._VarSet__varSet = varSet

    
    def getID(self):
        return self._VarSet__id

    
    def setID(self, id):
        self._VarSet__id = id

    
    def __iter__(self):
        return iter(self._VarSet__varSet)



