# Source Generated with Decompyle++
# File: DebugMonitorView.pyc (Python 2.6)

import BigWorld
from gui.DebugView import DebugView
from gui.DebugView import DebugViewItem
from debug_utils import *

class DebugMonitorView(DebugView):
    
    def __init__(self, textureName = '', parentGUI = None):
        DebugView.__init__(self, textureName, parentGUI)
        self._DebugMonitorView__contentInfo = { }
        self._DebugMonitorView__newContentInfo = { }

    
    def destroy(self):
        DebugView.destroy(self)

    
    def setContent(self, content):
        if not self.getVisible():
            return None
        contentItems = self._DebugMonitorView__buildContentItemsBy(content)
        if contentItems is None:
            self._DebugMonitorView__roolbackContentInfo()
            return None
        self._DebugMonitorView__commitContentInfo()
        self._DebugMonitorView__updateViewByContentItems(contentItems)

    
    def _DebugMonitorView__setItem(self, nameStr, valueStr, dividerStr, item = None):
        if item is None:
            item = DebugViewItem()
            item.setFont(('system_small.font', 'system_small.font'))
            item.setColour(((255, 255, 255, 255), (255, 255, 255, 255)))
            newKeyname = 'key_' + str(self.getItemsCount())
            self.addItem(newKeyname, item)
        
        item.setName(nameStr)
        item.setValue(valueStr)
        item.setDivider(dividerStr)
        item.setVisible(True)

    
    def _DebugMonitorView__updateContentInfoItem(self, keyname, value):
        resultDelta = 0
        if keyname in self._DebugMonitorView__contentInfo:
            (lastValue, resultDelta) = self._DebugMonitorView__contentInfo[keyname]
            if lastValue != value:
                
                try:
                    resultDelta = value - lastValue

            
        
        self._DebugMonitorView__newContentInfo[keyname] = (value, resultDelta)
        return resultDelta

    
    def _DebugMonitorView__commitContentInfo(self):
        self._DebugMonitorView__contentInfo = self._DebugMonitorView__newContentInfo
        self._DebugMonitorView__newContentInfo = { }

    
    def _DebugMonitorView__roolbackContentInfo(self):
        self._DebugMonitorView__newContentInfo = { }

    
    def _DebugMonitorView__buildContentItemsBy(self, content, baseIndent = 0, baseKeyname = ''):
        result = []
        
        try:
            if isinstance(content, dict):
                for (itemName, itemValue) in sorted(content.items()):
                    itemName = str(itemName)
                    itemKeyname = baseKeyname + itemName
                    if isinstance(itemValue, dict):
                        result += [
                            (' ' * baseIndent + itemName + ':', '', '')]
                        subResult = self._DebugMonitorView__buildContentItemsBy(itemValue, baseIndent + 1, itemKeyname)
                        if subResult is not None:
                            result += subResult
                        
                    
                    if isinstance(itemValue, int) and isinstance(itemValue, float) and isinstance(itemValue, bool) and isinstance(itemValue, str) or itemValue is None:
                        deltaValue = self._DebugMonitorView__updateContentInfoItem(itemKeyname, itemValue)
                        if isinstance(itemValue, float):
                            pass
                        1
                        valueStr1 = str(itemValue)
                        if isinstance(deltaValue, float):
                            pass
                        1
                        valueStr2 = str(deltaValue)
                        itemValueStr = valueStr1 + ' (' + valueStr2 + ')'
                        result += [
                            (' ' * baseIndent + itemName, itemValueStr, ' = ')]
                        continue
                
        except:
            LOG_ERROR("<DebugMonitor>: can't build content items. Look exception:")
            LOG_CURRENT_EXCEPTION()
            return None

        return result

    
    def _DebugMonitorView__updateViewByContentItems(self, contentItems):
        curIndex = -1
        for curItemKeyname in self.getListKeynames():
            curItem = self.getItem(curItemKeyname)
            curIndex += 1
            if curIndex >= len(contentItems):
                curItem.setVisible(False)
                continue
            
            (curNameStr, curValueStr, curDividerStr) = contentItems[curIndex]
            self._DebugMonitorView__setItem(curNameStr, curValueStr, curDividerStr, curItem)
        
        processedItemsCount = curIndex + 1
        for curIndex in xrange(processedItemsCount, len(contentItems)):
            (curNameStr, curValueStr, curDividerStr) = contentItems[curIndex]
            self._DebugMonitorView__setItem(curNameStr, curValueStr, curDividerStr, None)
        
        self.update()



