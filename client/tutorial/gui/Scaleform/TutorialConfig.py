# Source Generated with Decompyle++
# File: TutorialConfig.pyc (Python 2.6)

import ResMgr
from items import _xml
from tutorial.doc_loader import sub_parsers

class TutorialConfig(object):
    
    def __init__(self):
        super(TutorialConfig, self).__init__()
        self._TutorialConfig__sceneAliases = { }
        self._TutorialConfig__sceneMethods = { }
        self._TutorialConfig__guiItems = { }
        self._TutorialConfig__defAreaProps = {
            'path': None,
            'targetID': None,
            'lockedSymbol': '',
            'position': (0, 0),
            'size': (None, None),
            'changeSize': False,
            'lockedPopUp': False }
        self._TutorialConfig__areas = { }
        self._TutorialConfig__commands = { }

    
    def _TutorialConfig__readSceneAliasesSection(self, xmlCtx, section):
        self._TutorialConfig__sceneAliases.clear()
        self._TutorialConfig__sceneMethods.clear()
        for (tagName, subSection) in _xml.getChildren(xmlCtx, section, 'scene-aliases'):
            sceneID = subSection.asString
            self._TutorialConfig__sceneAliases[tagName] = sceneID
            self._TutorialConfig__sceneMethods[sceneID] = _xml.readString(xmlCtx, subSection, 'go-to')
        

    
    def _TutorialConfig__readGuiItemsSection(self, xmlCtx, section):
        self._TutorialConfig__guiItems.clear()
        for (_, subSection) in _xml.getChildren(xmlCtx, section, 'gui-items'):
            itemID = sub_parsers._parseID(xmlCtx, subSection, 'Specify a GUI item ID')
            path = _xml.readString(xmlCtx, subSection, 'path')
            self._TutorialConfig__guiItems[itemID] = {
                'path': path,
                'locked': True }
        

    
    def _TutorialConfig__readDefAreaPropsSection(self, xmlCtx, section):
        subSection = _xml.getSubsection(xmlCtx, section, 'def-area-props')
        self._TutorialConfig__defAreaProps.update({
            'lockedArea': _xml.readString(xmlCtx, subSection, 'locked-symbol'),
            'changeSize': subSection.readBool('change-size', False) })

    
    def _TutorialConfig__readCommandsSection(self, xmlCtx, section):
        self._TutorialConfig__commands.clear()
        for (_, subSection) in _xml.getChildren(xmlCtx, section, 'gui-commands'):
            commandID = sub_parsers._parseID(xmlCtx, subSection, 'Specify a command ID')
            command = (_xml.readString(xmlCtx, subSection, 'name'), [])
            argsSection = _xml.getChildren(xmlCtx, subSection, 'args')
            for (name, argSection) in argsSection:
                command[1].append(sub_parsers._readVarValue(name, argSection))
            
            self._TutorialConfig__commands[commandID] = command
        

    
    def _TutorialConfig__readAreasSection(self, xmlCtx, section):
        self._TutorialConfig__areas.clear()
        for (_, subSection) in _xml.getChildren(xmlCtx, section, 'areas'):
            areaID = sub_parsers._parseID(xmlCtx, subSection, 'Specify a area ID')
            targetID = None
            path = None
            if subSection.has_key('path'):
                path = _xml.readString(xmlCtx, subSection, 'path')
            elif subSection.has_key('gui-item-ref'):
                targetID = _xml.readString(xmlCtx, subSection, 'gui-item-ref')
                item = self._TutorialConfig__guiItems.get(targetID)
                if item is None:
                    _xml.raiseWrongXml(xmlCtx, 'area', 'GUI Item not found: {0:>s}'.format(targetID))
                
                path = item['path']
            
            if 'locked-symbol' in subSection.keys():
                symbol = _xml.readString(xmlCtx, subSection, 'locked-symbol')
            else:
                symbol = self._TutorialConfig__defAreaProps['lockedSymbol']
            position = (0, 0)
            if 'position' in subSection.keys():
                position = _xml.readVector2(xmlCtx, subSection, 'position').tuple()
            
            size = (None, None)
            if 'size' in subSection.keys():
                size = _xml.readVector2(xmlCtx, subSection, 'size').tuple()
            
            changeSize = subSection.readBool('change-size', self._TutorialConfig__defAreaProps['changeSize'])
            lockedPopUp = subSection.readBool('locked-popup', self._TutorialConfig__defAreaProps['lockedPopUp'])
            self._TutorialConfig__areas[areaID] = {
                'path': path,
                'targetID': targetID,
                'lockedSymbol': symbol,
                'position': position,
                'size': size,
                'changeSize': changeSize,
                'lockedPopUp': lockedPopUp }
        

    
    def loadConfig(self, filePath):
        section = ResMgr.openSection(filePath)
        if section is None:
            _xml.raiseWrongXml(None, filePath, 'can not open or read')
        
        xmlCtx = (None, filePath)
        self._TutorialConfig__readSceneAliasesSection(xmlCtx, section)
        self._TutorialConfig__readGuiItemsSection(xmlCtx, section)
        self._TutorialConfig__readDefAreaPropsSection(xmlCtx, section)
        self._TutorialConfig__readCommandsSection(xmlCtx, section)
        self._TutorialConfig__readAreasSection(xmlCtx, section)

    
    def reloadConfig(self, filePath):
        ResMgr.purge(filePath)
        self.loadConfig(filePath)

    
    def getSceneID(self, guiPage):
        
        try:
            return self._TutorialConfig__sceneAliases[guiPage]
        except KeyError:
            return None


    
    def getGoToSceneMethod(self, sceneID):
        
        try:
            return self._TutorialConfig__sceneMethods[sceneID]
        except KeyError:
            return None


    
    def getArea(self, areaID):
        if areaID in self._TutorialConfig__areas:
            return self._TutorialConfig__areas[areaID].copy()
        return self._TutorialConfig__defAreaProps.copy()

    
    def getItem(self, targetID):
        if targetID in self._TutorialConfig__guiItems:
            return self._TutorialConfig__guiItems[targetID].copy()
        return {
            'path': '',
            'locked': False }

    
    def addItem(self, targetID, path, locked = False):
        self._TutorialConfig__guiItems[targetID] = {
            'path': path,
            'locked': locked }

    
    def getCommand(self, commandID):
        
        try:
            return self._TutorialConfig__commands[commandID]
        except KeyError:
            return None


    
    def removeItem(self, targetID):
        item = self._TutorialConfig__guiItems.get(targetID)
        if item is not None and not item['locked']:
            self._TutorialConfig__guiItems.pop(targetID)
        



