# Source Generated with Decompyle++
# File: parsers.pyc (Python 2.6)

import ResMgr
from helpers.html import translation
from items import _xml
from tutorial.data.descriptor import DescriptorData
from tutorial.data.chapter import Chapter, Scene
from tutorial.doc_loader import sub_parsers
from tutorial.settings import GLOBAL_REFS_FILE_PATH

class DescriptorParser(object):
    
    def _DescriptorParser__parseChapterSummaries(self, xmlCtx, section, descriptor):
        for (_, subSection) in _xml.getChildren(xmlCtx, section, 'chapters'):
            chapterID = _xml.readString(xmlCtx, subSection, 'chapter-id')
            title = translation(_xml.readString(xmlCtx, subSection, 'title'))
            descSec = _xml.getSubsection(xmlCtx, subSection, 'description')
            defDesc = translation(descSec.asString)
            abDesc = translation(descSec.readString('after-battle', defDesc))
            descriptions = (defDesc, abDesc)
            bonusID = subSection.readInt('bonus-id', -1)
            bonusMsg = subSection.readString('bonus-msg')
            forcedLoading = subSection.readInt('forced-loading', -1)
            pathSec = _xml.getSubsection(xmlCtx, subSection, 'file-path')
            defFilePath = pathSec.asString
            afterBattleFilePath = pathSec.readString('after-battle', defFilePath)
            filePaths = (defFilePath, afterBattleFilePath)
            descriptor.addChapter(Chapter(chapterID, title, descriptions, bonusID, bonusMsg, forcedLoading, filePaths))
        

    
    def parse(self, filePath):
        descriptor = DescriptorData()
        section = ResMgr.openSection(filePath)
        if section is None:
            _xml.raiseWrongXml(None, filePath, 'can not open or read')
        
        xmlCtx = (None, filePath)
        descriptor.setGuiFilePath(_xml.readString(xmlCtx, section, 'gui'))
        self._DescriptorParser__parseChapterSummaries(xmlCtx, section, descriptor)
        return descriptor



class ChapterParser(object):
    
    def __init__(self):
        super(ChapterParser, self).__init__()

    
    def parse(self, chapter, afterBattle = False):
        filePath = chapter.getFilePath(afterBattle = afterBattle)
        section = ResMgr.openSection(filePath)
        if section is None:
            _xml.raiseWrongXml(None, filePath, 'can not open or read')
        
        xmlCtx = (None, filePath)
        chapter.clear()
        flags = []
        itemFlags = []
        subSec = _xml.getSubsection(xmlCtx, section, 'chapter-info')
        chapter.setInfoConditions(sub_parsers._parseConditions(xmlCtx, subSec, flags))
        if 'initial-scene' in section.keys():
            chapter.setInitialSceneID(_xml.readString(xmlCtx, section, 'initial-scene'))
        
        if 'default-scene' in section.keys():
            chapter.setDefaultSceneID(_xml.readString(xmlCtx, section, 'default-scene'))
        
        for (_, subSec) in _xml.getChildren(xmlCtx, section, 'dialogs'):
            dialog = sub_parsers._parseDialog(xmlCtx, subSec, flags)
            chapter.addDialog(dialog)
        
        for (_, subSec) in _xml.getChildren(xmlCtx, section, 'hints'):
            hint = sub_parsers._parseHint(xmlCtx, subSec, flags)
            chapter.addHint(hint)
        
        for (_, subSec) in _xml.getChildren(xmlCtx, section, 'triggers'):
            trigger = sub_parsers._parseTrigger(xmlCtx, subSec, flags, chapter)
            if trigger is not None:
                chapter.addTrigger(trigger)
                continue
        
        gVarIDs = []
        for (name, subSec) in _xml.getChildren(xmlCtx, section, 'vars'):
            if name == 'var-set':
                chapter.addVarSet(sub_parsers._parseVarSet(xmlCtx, subSec, flags))
                continue
            if name == 'var-set-ref':
                gVarIDs.append(sub_parsers._parseID(xmlCtx, subSec, 'Specify a var ID'))
                continue
            _xml.raiseWrongXml(xmlCtx, name, 'Unknown tag')
        
        if len(gVarIDs):
            GlobalRefParser().parse(chapter, varIDs = gVarIDs, flags = flags)
        
        for (_, sceneSec) in _xml.getChildren(xmlCtx, section, 'scenes'):
            sceneID = sceneSec.asString
            if sceneID is None or not len(sceneID):
                _xml.raiseWrongXml(xmlCtx, 'scene', 'Specify a unique name for the scene')
            
            scene = Scene(id = sceneID)
            for (_, subSec) in _xml.getChildren(xmlCtx, sceneSec, 'gui-items'):
                item = sub_parsers._parseGuiItem(xmlCtx, subSec, flags, itemFlags)
                if item is not None:
                    scene.addGuiItem(item)
                    continue
            
            for (_, subSec) in _xml.getChildren(xmlCtx, sceneSec, 'post-effects'):
                effect = sub_parsers._parseEffect(xmlCtx, subSec, flags, afterBattle = afterBattle)
                if effect is not None:
                    scene.addPostEffect(effect)
                    continue
            
            for (_, subSec) in _xml.getChildren(xmlCtx, sceneSec, 'runtime-effects'):
                effect = sub_parsers._parseEffect(xmlCtx, subSec, flags, afterBattle = afterBattle)
                if effect is not None:
                    scene.addEffect(effect)
                    continue
            
            for (_, subSec) in _xml.getChildren(xmlCtx, sceneSec, 'locked-areas'):
                area = sub_parsers._parseLockedArea(xmlCtx, subSec, flags)
                scene.addLockedArea(area)
            
            for (_, subSec) in _xml.getChildren(xmlCtx, sceneSec, 'active-areas'):
                area = sub_parsers._parseActiveArea(xmlCtx, subSec, flags)
                if area is not None:
                    scene.addActiveArea(area)
                    continue
            
            chapter.addScene(scene)
        
        flags = (filter,)((lambda flag: flag not in itemFlags), flags)
        chapter.setFlags(flags)
        chapter.setValid(True)
        return chapter



class GlobalRefParser(object):
    
    def __init__(self):
        super(GlobalRefParser, self).__init__()

    
    def parse(self, chapter, varIDs = None, flags = None):
        if varIDs is None:
            varIDs = []
        
        if flags is None:
            flags = []
        
        section = ResMgr.openSection(GLOBAL_REFS_FILE_PATH)
        if section is None:
            _xml.raiseWrongXml(None, GLOBAL_REFS_FILE_PATH, 'can not open or read')
        
        xmlCtx = (None, GLOBAL_REFS_FILE_PATH)
        if len(varIDs):
            for (_, subSec) in _xml.getChildren(xmlCtx, section, 'vars'):
                varID = sub_parsers._parseID(xmlCtx, subSec, 'Specify a var ID')
                if varID in varIDs:
                    chapter.addVarSet(sub_parsers._parseVarSet(xmlCtx, subSec, flags))
                    continue
            
        



