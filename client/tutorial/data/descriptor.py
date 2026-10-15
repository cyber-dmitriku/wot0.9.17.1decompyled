# Source Generated with Decompyle++
# File: descriptor.pyc (Python 2.6)


class DescriptorData(object):
    
    def __init__(self):
        super(DescriptorData, self).__init__()
        self._DescriptorData__guiFilePath = ''
        self._DescriptorData__contents = []
        self._DescriptorData__idMapping = { }

    
    def getGuiFilePath(self):
        return self._DescriptorData__guiFilePath

    
    def setGuiFilePath(self, filePath):
        self._DescriptorData__guiFilePath = filePath

    
    def addChapter(self, chapter):
        self._DescriptorData__idMapping[chapter.getID()] = len(self._DescriptorData__contents)
        self._DescriptorData__contents.append(chapter)

    
    def getChapter(self, chapterID):
        result = None
        if chapterID in self._DescriptorData__idMapping:
            result = self._DescriptorData__contents[self._DescriptorData__idMapping[chapterID]]
        
        return result

    
    def isChapterInitial(self, chapter, bonusCompleted):
        if not chapter is not None and chapter.ignoreBonus(bonusCompleted):
            pass
        return not chapter.isBonusReceived(bonusCompleted)

    
    def getInitialChapterID(self, bonusCompleted = None):
        if bonusCompleted is None:
            if len(self._DescriptorData__contents):
                return self._DescriptorData__contents[0].getID()
            return None
        for chapter in self._DescriptorData__contents:
            if chapter.hasBonus() and not chapter.isBonusReceived(bonusCompleted):
                return chapter.getID()
        
        return None

    
    def getAllBonuses(self):
        result = 0
        for chapter in self._DescriptorData__contents:
            if chapter.hasBonus():
                result |= 1 << chapter.getBonusID()
                continue
        
        return result

    
    def isAllBonusesReceived(self, bonusCompleted):
        return self.getAllBonuses() <= bonusCompleted



