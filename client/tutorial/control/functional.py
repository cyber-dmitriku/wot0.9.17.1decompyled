# Source Generated with Decompyle++
# File: functional.pyc (Python 2.6)

from account_helpers.AccountSettings import AccountSettings
from tutorial.control import TutorialProxyHolder, gameVars
from tutorial.data import chapter
from tutorial.logger import LOG_ERROR, LOG_DEBUG

class FunctionalConditions(TutorialProxyHolder):
    
    def __init__(self, conditions):
        super(FunctionalConditions, self).__init__()
        self._conditions = conditions

    
    def allConditionsOk(self):
        if self._conditions is None:
            return True
        ok = self.evaluateWithAND()
        for eitherCondition in self._conditions.eitherBlocks():
            if ok:
                ok = FunctionalConditions(eitherCondition).evaluateWithOR()
                continue
            self._conditions is None
        
        return ok

    
    def evaluateWithAND(self):
        if self._conditions is None:
            return True
        result = True
        flags = self._tutorial.getFlags()
        for condition in self._conditions:
            if result:
                if condition.getType() == chapter.Condition.FLAG_CONDITION:
                    result = condition.isActiveState() == flags.isActiveFlag(condition.getID())
                elif condition.getType() == chapter.Condition.VEHICLE_CONDITION:
                    result = condition.isValueEqual(gameVars.vehicle(condition.getID()))
                
            condition.getType() == chapter.Condition.FLAG_CONDITION
        
        return result

    
    def evaluateWithOR(self):
        if self._conditions is None:
            return True
        result = False
        flags = self._tutorial.getFlags()
        for condition in self._conditions:
            if not result:
                if condition.getType() == chapter.Condition.FLAG_CONDITION:
                    result = condition.isActiveState() == flags.isActiveFlag(condition.getID())
                elif condition.getType() == chapter.Condition.VEHICLE_CONDITION:
                    result = condition.isValueEqual(gameVars.vehicle(condition.getID()))
                
            condition.getType() == chapter.Condition.FLAG_CONDITION
        
        return result



class FunctionalVarSet(object):
    
    def __init__(self, varSet):
        super(FunctionalVarSet, self).__init__()
        self._varSet = varSet

    
    def getFirstActual(self):
        if self._varSet is None:
            return None
        for (var, conditions) in self._varSet:
            result = FunctionalConditions(conditions).allConditionsOk()
            if result:
                return var
        



class FunctionalEffect(TutorialProxyHolder):
    
    def __init__(self, effect):
        super(FunctionalEffect, self).__init__()
        self._effect = effect

    
    def triggerEffect(self):
        raise NotImplementedError, 'method triggerEffect is not implemented'

    
    def getTarget(self):
        pass

    
    def isInstantaneous(self):
        return True

    
    def isStillRunning(self):
        return False

    
    def stop(self):
        pass

    
    def isAllConditionsOK(self):
        result = True
        if self._effect is not None:
            return FunctionalConditions(self._effect.getConditions()).allConditionsOk()
        return result



class FunctionalActivateEffect(FunctionalEffect):
    
    def triggerEffect(self):
        targetID = self._effect.getTargetID()
        flags = self._tutorial.getFlags()
        if not flags.isActiveFlag(targetID):
            flags.activateFlag(targetID)
            self._tutorial.invalidateFlags()
        



class FunctionalDeactivateEffect(FunctionalEffect):
    
    def triggerEffect(self):
        targetID = self._effect.getTargetID()
        flags = self._tutorial.getFlags()
        if flags.isActiveFlag(targetID):
            flags.deactivateFlag(targetID)
            self._tutorial.invalidateFlags()
        



class FunctionalRefuseTrainingEffect(FunctionalEffect):
    
    def triggerEffect(self):
        self._tutorial.refuse()

    
    def isStillRunning(self):
        return True

    
    def isInstantaneous(self):
        return False



class FunctionalNextChapterEffect(FunctionalEffect):
    
    def triggerEffect(self):
        nextChapter = self._effect.getTargetID()
        if nextChapter is None or not len(nextChapter):
            nextChapter = self._tutorial._descriptor.getInitialChapterID(bonusCompleted = self._tutorial._bonusCompleted)
        
        if self._tutorial._currentChapter != nextChapter:
            self._gui.showWaiting('chapter-loading', isSingle = True)
            self._gui.clear()
            self._tutorial.goToNextChapter(nextChapter)
        



class FunctionalShowHintEffect(FunctionalEffect):
    
    def triggerEffect(self):
        hint = self._tutorial._data.getHint(self._effect.getTargetID())
        if hint is not None:
            self._gui.playEffect('ShowHint', hint.getData(), itemRef = hint.getTargetID(), containerRef = hint.getContainerID())
        else:
            LOG_ERROR('Hint not found', self._effect.getTargetID())



class FunctionalCloseHintEffect(FunctionalEffect):
    
    def triggerEffect(self):
        self._gui.stopEffect('ShowHint', self._effect.getTargetID())



class FunctionalShowDialogEffect(FunctionalEffect):
    
    def __init__(self, effect):
        self._isRunning = False
        self._isDialogClosed = False
        super(FunctionalShowDialogEffect, self).__init__(effect)

    
    def triggerEffect(self):
        self._gui.hideWaiting('update-scene')
        dialog = self.getTarget()
        if dialog is not None:
            self._isRunning = True
            if self._gui.isGuiDialogDisplayed():
                self._isDialogClosed = True
                return None
            data = dialog.getData()
            if not dialog.isDataFull():
                self._FunctionalShowDialogEffect__fetchAdditionalData(dialog, data)
            
            self._gui.playEffect('ShowDialog', data)
        else:
            LOG_ERROR('Dialog not found', self._effect.getTargetID())

    
    def isInstantaneous(self):
        return False

    
    def isStillRunning(self):
        if self._isRunning:
            if self._isDialogClosed and not self._gui.isGuiDialogDisplayed():
                self._isDialogClosed = False
                self.triggerEffect()
            
            if not (self._isDialogClosed) and not self._gui.isTutorialDialogDisplayed(self._effect.getTargetID()):
                self._isDialogClosed = True
            
        
        return self._isRunning

    
    def stop(self):
        self._isRunning = False
        self._isDialogClosed = False

    
    def getTarget(self):
        return self._tutorial._data.getDialog(self._effect.getTargetID())

    
    def _FunctionalShowDialogEffect__fetchAdditionalData(self, dialog, data):
        var = self._tutorial.getVars().get(dialog.getVarRef())
        if var is None:
            return None
        if dialog.getType() == 'vehicleItemInfo':
            self._gui.showWaiting('request-item-params')
            gameVars.addVehicleItemParams(var, data)
            self._gui.hideWaiting('request-item-params')
        elif dialog.getType() == 'tankmanSkill':
            gameVars.addTankmanSkillParams(var, data)
        else:
            data.append(var)



class FunctionalRunTriggerEffect(FunctionalEffect):
    
    def __init__(self, effect):
        super(FunctionalRunTriggerEffect, self).__init__(effect)

    
    def isInstantaneous(self):
        return False

    
    def isStillRunning(self):
        trigger = self.getTarget()
        if trigger is not None:
            return trigger.isRunning
        return False

    
    def triggerEffect(self):
        trigger = self.getTarget()
        if trigger is not None:
            trigger.run()
        else:
            LOG_ERROR('Trigger not found', self._effect.getTargetID())

    
    def getTarget(self):
        return self._tutorial._data.getTrigger(self._effect.getTargetID())



class FunctionalRequestBonusEffect(FunctionalEffect):
    
    def isInstantaneous(self):
        return False

    
    def isStillRunning(self):
        return not (self._tutorial._isBonusReceived)

    
    def triggerEffect(self):
        self._tutorial.requestForBonus()



class FunctionalGuiItemSetPropertiesEffect(FunctionalEffect):
    
    def triggerEffect(self):
        effect = self._effect
        self._gui.setItemProps(effect.getTargetID(), effect.getProps(), revert = effect.isRevert())



class FunctionalFinishTrainingEffect(FunctionalEffect):
    
    def triggerEffect(self):
        self._tutorial.stop(finished = True)

    
    def isStillRunning(self):
        return True

    
    def isInstantaneous(self):
        return False



class FunctionalDefineGuiItem(FunctionalEffect):
    
    def triggerEffect(self):
        effect = self._effect
        parentReference = self._gui.config.getItem(effect.getParentReference())
        extraReference = self._gui.config.getItem(effect.getExtraReference())
        targetId = effect.getTargetID()
        ERROR = '%s was not found in gui-items list'
        if parentReference is not None:
            if extraReference is not None:
                extraPath = '{0:>s}.{1:>s}'.format(parentReference.get('path'), extraReference.get('path'))
                self._gui.config.addItem(targetId, extraPath, True)
            else:
                LOG_ERROR(ERROR % effect.getExtraReference())
        else:
            LOG_ERROR(ERROR % effect.getParentReference())



class FunctionalGuiCommandEffect(FunctionalEffect):
    
    def triggerEffect(self):
        targetID = self._effect.getTargetID()
        command = self._gui.config.getCommand(targetID)
        if command is not None:
            self._gui.invokeCommand(command)
        else:
            LOG_ERROR('Command not found', targetID)



class FunctionalSetFilterEffect(FunctionalEffect):
    
    def triggerEffect(self):
        AccountSettings.setFilter(self._effect.getTargetID(), self._effect.getValue())


_functionalEffects = {
    chapter.Effect.ACTIVATE: FunctionalActivateEffect,
    chapter.Effect.DEACTIVATE: FunctionalDeactivateEffect,
    chapter.Effect.SHOW_HINT: FunctionalShowHintEffect,
    chapter.Effect.CLOSE_HINT: FunctionalCloseHintEffect,
    chapter.Effect.SHOW_DIALOG: FunctionalShowDialogEffect,
    chapter.Effect.REFUSE_TRAINING: FunctionalRefuseTrainingEffect,
    chapter.Effect.NEXT_CHAPTER: FunctionalNextChapterEffect,
    chapter.Effect.RUN_TRIGGER: FunctionalRunTriggerEffect,
    chapter.Effect.REQUEST_BONUS: FunctionalRequestBonusEffect,
    chapter.Effect.SET_ITEM_PROPS: FunctionalGuiItemSetPropertiesEffect,
    chapter.Effect.FINISH_TRAINING: FunctionalFinishTrainingEffect,
    chapter.Effect.DEFINE_GUI_ITEM: FunctionalDefineGuiItem,
    chapter.Effect.INVOKE_GUI_CMD: FunctionalGuiCommandEffect,
    chapter.Effect.SET_FILTER: FunctionalSetFilterEffect }

def factory(effects):
    result = []
    for effect in effects:
        if effect is None:
            continue
        
        clazz = _functionalEffects.get(effect.getType())
        if clazz is not None:
            result.append(clazz(effect))
            continue
        LOG_ERROR('Not found FunctionalEffect class by effect type:', effect.getType())
    
    return result


class FunctionalChapterInfo(TutorialProxyHolder):
    
    def __init__(self, conditions):
        super(FunctionalChapterInfo, self).__init__()
        self._conditions = None
        if conditions is not None and len(conditions):
            self._conditions = FunctionalConditions(conditions)
        
        self._isShow = False

    
    def update(self):
        if self._conditions is None:
            return None
        ok = self._conditions.allConditionsOk()
        if ok and not (self._isShow):
            chapter = self._tutorial._data
            self._gui.setChapterInfo(chapter.getTitle(), chapter.getDescription(afterBattle = self._tutorial._cache.isAfterBattle()))
            self._isShow = True
        elif not ok and self._isShow:
            self._gui.clearChapterInfo()
            self._isShow = False
        



class FunctionalScene(TutorialProxyHolder):
    
    def __init__(self, scene):
        super(FunctionalScene, self).__init__()
        LOG_DEBUG('New functional scene', scene.getID())
        self._FunctionalScene__scene = scene
        self._FunctionalScene__actions = { }
        self._FunctionalScene__dynamicItems = { }
        self._FunctionalScene__dynamicItemsOnScene = []
        self._sceneToBeUpdated = True
        self._gui.showWaiting('update-scene')

    
    def leave(self):
        if self._sceneToBeUpdated:
            self._gui.hideWaiting('update-scene')
            self._sceneToBeUpdated = False
        

    
    def update(self):
        if self._sceneToBeUpdated:
            self._sceneToBeUpdated = False
            self._updateScene()
        
        for (itemID, item) in self._FunctionalScene__dynamicItems.iteritems():
            criteria = item.getFindCriteria()
            if criteria is not None:
                criteria[2] = self._tutorial.getVars().get(criteria[2])
            
            result = self._gui.findItem(itemID, criteria)
            wasOnScene = itemID in self._FunctionalScene__dynamicItemsOnScene
            effects = []
            if result is not None and not wasOnScene:
                LOG_DEBUG('Gui item is on scene', itemID)
                self._FunctionalScene__dynamicItemsOnScene.append(itemID)
                props = item.getProps()
                if len(props):
                    self._gui.setItemProps(item.getTargetID(), props)
                
                effects = item.getOnSceneEffects()
            elif result is None and wasOnScene:
                LOG_DEBUG('Gui item is not on scene', itemID)
                effects = item.getNotOnSceneEffects()
                self._FunctionalScene__dynamicItemsOnScene.remove(itemID)
            
            if len(effects):
                self._tutorial.storeEffectsInQueue(factory(effects))
                continue
        

    
    def _updateScene(self):
        LOG_DEBUG('Update scene.')
        self._gui.updateLockedAreas(filter(self._FunctionalScene__areAllConditionsOk, self._FunctionalScene__scene.getLockedAreas()))
        activeAreas = filter(self._FunctionalScene__areAllConditionsOk, self._FunctionalScene__scene.getActiveAreas())
        for area in activeAreas:
            actions = area.getActions()
            if len(actions):
                self._FunctionalScene__actions.update(actions)
                continue
        
        self._gui.updateActiveAreas(activeAreas)
        items = filter(self._FunctionalScene__isPermanentGuiItem, self._FunctionalScene__scene.getGuiItems())
        for item in items:
            self._gui.setItemProps(item.getTargetID(), item.getProps(), revert = True)
        
        items = filter(self._FunctionalScene__isDynamicGuiItem, self._FunctionalScene__scene.getGuiItems())
        self._FunctionalScene__dynamicItems = dict(map((lambda item: (item.getTargetID(), item)), items))
        effects = filter(self._FunctionalScene__areAllConditionsOk, self._FunctionalScene__scene.getEffects())
        if len(effects):
            self._tutorial.storeEffectsInQueue(factory(effects))
        
        self._gui.hideWaiting('update-scene')

    
    def getAction(self, targetID):
        return self._FunctionalScene__actions.get(targetID)

    
    def _FunctionalScene__areAllConditionsOk(self, item):
        return FunctionalConditions(item.getConditions()).allConditionsOk()

    
    def _FunctionalScene__isPermanentGuiItem(self, item):
        if item.getLifeCycle() == chapter.GuiItemRef.LIFE_CYCLE_PERMANENT:
            pass
        return FunctionalConditions(item.getConditions()).allConditionsOk()

    
    def _FunctionalScene__isDynamicGuiItem(self, item):
        if item.getLifeCycle() == chapter.GuiItemRef.LIFE_CYCLE_DYNAMIC:
            pass
        return FunctionalConditions(item.getConditions()).allConditionsOk()



