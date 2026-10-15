# Source Generated with Decompyle++
# File: __init__.pyc (Python 2.6)

import ResMgr
from tutorial.doc_loader.parsers import DescriptorParser, ChapterParser
from tutorial.settings import DESCRIPTOR_FILE_PATH, GLOBAL_REFS_FILE_PATH
from tutorial.logger import LOG_CURRENT_EXCEPTION

def loadDescriptorData(clearCache = False):
    
    try:
        if clearCache:
            ResMgr.purge(DESCRIPTOR_FILE_PATH)
        
        return DescriptorParser().parse(DESCRIPTOR_FILE_PATH)
    except Exception:
        LOG_CURRENT_EXCEPTION()
        return None



def loadChapterData(chapter, afterBattle = False):
    if chapter is not None and not chapter.isValid():
        
        try:
            ChapterParser().parse(chapter, afterBattle = afterBattle)
        except Exception:
            LOG_CURRENT_EXCEPTION()
            return None
        

    return chapter


def clearChapterData(chapter):
    ResMgr.purge(GLOBAL_REFS_FILE_PATH)
    defPath = chapter.getFilePath(afterBattle = False)
    abPath = chapter.getFilePath(afterBattle = True)
    ResMgr.purge(defPath)
    if defPath != abPath:
        ResMgr.purge(abPath)
    
    chapter.clear()


