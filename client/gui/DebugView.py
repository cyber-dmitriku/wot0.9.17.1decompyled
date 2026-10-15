# Source Generated with Decompyle++
# File: DebugView.pyc (Python 2.6)

import BigWorld
import game
import GUI
from debug_utils import *

class DebugView:
    
    def __init__(self, textureName = '', parentGUI = None):
        self._DebugView__listKeynames = []
        self._DebugView__dictItems = { }
        self._DebugView__bAutoUpdate = False
        self._DebugView__align = [
            False,
            False,
            False,
            False]
        self._DebugView__margin = [
            0,
            0,
            0,
            0]
        self._DebugView__window = None
        self._DebugView__createMainWindow(parentGUI)
        game.g_guiResetters.add(self._DebugView__onChangeScreenResolution)
        self.setTextureName(textureName)
        self.setVisible(False)

    
    def destroy(self):
        game.g_guiResetters.remove(self._DebugView__onChangeScreenResolution)
        self.clear()
        self._DebugView__destroyMainWindow()

    
    def clear(self):
        for curKeyname in self._DebugView__listKeynames[:]:
            self.removeItem(curKeyname)
        

    
    def setVisible(self, bValue):
        self._DebugView__window.visible = bool(bValue)

    
    def getVisible(self):
        return self._DebugView__window.visible

    
    def setPosition(self, pos3d):
        self._DebugView__window.position = tuple(pos3d)

    
    def getPosition(self):
        return self._DebugView__window.position

    
    def setSize(self, size):
        self._DebugView__window.size = tuple(size)

    
    def getSize(self):
        return self._DebugView__window.size

    
    def setTextureName(self, textureName):
        self._DebugView__window.textureName = str(textureName)

    
    def getTextureName(self):
        return self._DebugView__window.textureName

    
    def getParent(self):
        return self._DebugView__window.parent

    
    def getParentSize(self):
        parent = self._DebugView__window.parent
        if parent is not None:
            return parent.size

    
    def setAutoUpdate(self, bValue):
        self._DebugView__bAutoUpdate = bool(bValue)

    
    def getAutoUpdate(self):
        return self._DebugView__bAutoUpdate

    
    def setAlign(self, value, index = None):
        if index is None:
            self._DebugView__align = [
                bool(value[0]),
                bool(value[1]),
                bool(value[2]),
                bool(value[3])]
        else:
            self._DebugView__align[index] = bool(value)

    
    def getAlign(self, index = None):
        if index is None:
            return list(self._DebugView__align)
        return self._DebugView__align[index]

    
    def setMargin(self, value, index = None):
        if index is None:
            self._DebugView__margin = [
                float(value[0]),
                float(value[1]),
                float(value[2]),
                float(value[3])]
        else:
            self._DebugView__margin[index] = float(value)

    
    def getMargin(self, index = None):
        if index is None:
            return list(self._DebugView__margin)
        return self._DebugView__margin[index]

    
    def getListKeynames(self):
        return list(self._DebugView__listKeynames)

    
    def getDictItems(self):
        return dict(self._DebugView__dictItems)

    
    def iterkeynames(self):
        return iter(self._DebugView__listKeynames)

    
    def iteritems(self):
        return self._DebugView__dictItems.itervalues()

    
    def getItemsCount(self):
        return len(self._DebugView__listKeynames)

    
    def getItem(self, keyname):
        return self._DebugView__dictItems.get(str(keyname), None)

    
    def addItem(self, keyname, item):
        if not isinstance(item, DebugViewItem):
            return None
        
        try:
            newPos = self._DebugView__listKeynames.index(keyname)
            self.removeItem(keyname)
        except:
            isinstance(item, DebugViewItem)
            newPos = None

        if newPos is not None:
            self._DebugView__listKeynames.insert(newPos, keyname)
        else:
            self._DebugView__listKeynames.append(keyname)
        self._DebugView__dictItems[keyname] = item
        self._DebugView__window.addChild(item._guiName)
        self._DebugView__window.addChild(item._guiValue)
        if self._DebugView__bAutoUpdate:
            self.update()
        

    
    def removeItem(self, keyname):
        if keyname not in self._DebugView__listKeynames:
            return None
        item = self._DebugView__dictItems[keyname]
        self._DebugView__listKeynames.remove(keyname)
        del self._DebugView__dictItems[keyname]
        self._DebugView__window.delChild(item._guiName)
        self._DebugView__window.delChild(item._guiValue)
        if self._DebugView__bAutoUpdate:
            self.update()
        
        item.destroy()

    
    def renameKeyname(self, keyname, newKeyname):
        if keyname not in self._DebugView__listKeynames:
            return None
        item = self._DebugView__dictItems[keyname]
        del self._DebugView__dictItems[keyname]
        self._DebugView__dictItems[newKeyname] = item
        self._DebugView__listKeynames[self._DebugView__listKeynames.index(keyname)] = newKeyname
        if self._DebugView__bAutoUpdate:
            self.update()
        

    
    def rebuild(self):
        saved_parent = self.getParent()
        saved_position = self.getPosition()
        saved_size = self.getSize()
        saved_textureName = self.getTextureName()
        saved_visible = self.getVisible()
        for curItem in self._DebugView__dictItems.itervalues():
            self._DebugView__window.delChild(curItem._guiName)
            self._DebugView__window.delChild(curItem._guiValue)
        
        GUI.delRoot(self._DebugView__window)
        self._DebugView__window = None
        for curItem in self._DebugView__dictItems.itervalues():
            curItem._rebuild()
        
        self._DebugView__createMainWindow(saved_parent)
        self.setPosition(saved_position)
        self.setSize(saved_size)
        self.setTextureName(saved_textureName)
        self.setVisible(saved_visible)
        for curItem in self._DebugView__dictItems.itervalues():
            self._DebugView__window.addChild(curItem._guiName)
            self._DebugView__window.addChild(curItem._guiValue)
        
        if self._DebugView__bAutoUpdate:
            self.update()
        

    
    def moveLine(self, keyname, deltaLine):
        if deltaLine == 0:
            return None
        
        try:
            ind = self._DebugView__listKeynames.index(keyname)
        except:
            deltaLine == 0
            return None

        if deltaLine < 0:
            block = self._DebugView__listKeynames[ind + deltaLine:ind]
            block.insert(0, keyname)
            self._DebugView__listKeynames[ind + deltaLine:ind + 1] = block
        else:
            block = self._DebugView__listKeynames[(ind + 1, ind + 1 + deltaLine)]
            block.append(keyname)
            self._DebugView__listKeynames[ind:ind + 1 + deltaLine] = block
        if self._DebugView__bAutoUpdate:
            self.update()
        

    
    def swapLines(self, keyname1, keyname2):
        if deltaLine == 0:
            return None
        
        try:
            ind1 = self._DebugView__listKeynames.index(keyname1)
            ind2 = self._DebugView__listKeynames.index(keyname2)
        except:
            deltaLine == 0
            return None

        self._DebugView__listKeynames[ind1] = keyname2
        self._DebugView__listKeynames[ind2] = keyname1
        if self._DebugView__bAutoUpdate:
            self.update()
        

    
    def update(self):
        self.normalizeLayout()

    
    def normalizeLayout(self):
        if not self.getVisible():
            return None
        totalHeight = 0
        maxWidth1 = 0
        maxWidth2 = 0
        for curKeyname in self._DebugView__listKeynames:
            curItem = self._DebugView__dictItems[curKeyname]
            if curItem._guiName.width > maxWidth1:
                pass
            1
            maxWidth1 = maxWidth1
            if curItem._guiValue.width > maxWidth2:
                pass
            1
            maxWidth2 = maxWidth2
            if curItem._guiName.height > curItem._guiValue.height:
                curLineHeight = curItem._guiName.height
            else:
                curLineHeight = curItem._guiValue.height
            totalHeight += curLineHeight
        
        totalWidth = maxWidth1 + maxWidth2
        self._DebugView__window.size = (totalWidth, totalHeight)
        curHeight = 0
        for curKeyname in self._DebugView__listKeynames:
            curItem = self._DebugView__dictItems[curKeyname]
            curItem._guiName.position = LU2BW((0, curHeight, 1), curItem._guiName.parent)
            curItem._guiValue.position = LU2BW((totalWidth - maxWidth2, curHeight, 1), curItem._guiValue.parent)
            if curItem._guiName.height > curItem._guiValue.height:
                curLineHeight = curItem._guiName.height
            else:
                curLineHeight = curItem._guiValue.height
            curHeight += curLineHeight
        
        size = self.getSize()
        pos = list(self.getPosition())
        if self.getAlign(3):
            if pos[1] - size[1] < self.getMargin(3) - 1:
                pos[1] -= (pos[1] - size[1]) + 1 - self.getMargin(3)
            
        
        if self.getAlign(2):
            if pos[0] + size[0] > 1 - self.getMargin(2):
                pos[0] -= (pos[0] + size[0] - 1) + self.getMargin(2)
            
        
        if self.getAlign(1):
            if pos[1] > 1 - self.getMargin(1):
                pos[1] -= (pos[1] - 1) + self.getMargin(1)
            
        
        if self.getAlign(0):
            if pos[0] < self.getMargin(0) - 1:
                pos[0] -= pos[0] + 1 - self.getMargin(0)
            
        
        self._DebugView__window.position = tuple(pos)

    
    def _DebugView__createMainWindow(self, parentGUI):
        self._DebugView__window = GUI.Window()
        self._DebugView__window.horizontalAnchor = 'LEFT'
        self._DebugView__window.verticalAnchor = 'TOP'
        if parentGUI is None:
            GUI.addRoot(self._DebugView__window)
        else:
            parentGUI.addChild(self._DebugView__window)

    
    def _DebugView__destroyMainWindow(self):
        if self._DebugView__window.parent is not None:
            self._DebugView__window.parent.delChild(self._DebugView__window)
        else:
            GUI.delRoot(self._DebugView__window)
        self._DebugView__window = None

    
    def _DebugView__onChangeScreenResolution(self):
        self.rebuild()



class DebugViewItem:
    
    def __init__(self, name = '', value = '', divider = ' = '):
        self._DebugViewItem__name = str(name)
        self._DebugViewItem__value = str(value)
        self._DebugViewItem__divider = str(divider)
        self._DebugViewItem__createGUI()
        self.setFont(('default_smaller.font', 'default_smaller.font'))
        self.setColour(((255, 255, 255, 255), (255, 255, 255, 255)))
        self.setMaterialFX(('ADD', 'ADD'))

    
    def destroy(self):
        self._DebugViewItem__destroyGUI()

    
    def setName(self, name):
        self._DebugViewItem__name = str(name)
        self._guiName.text = self._DebugViewItem__name + self._DebugViewItem__divider

    
    def getName(self):
        return self._name

    
    def setValue(self, value):
        self._DebugViewItem__value = str(value)
        self._guiValue.text = self._DebugViewItem__value

    
    def getValue(self):
        return self._DebugViewItem__value

    
    def setDivider(self, divider):
        self._DebugViewItem__divider = str(divider)
        self._guiName.text = self._DebugViewItem__name + self._DebugViewItem__divider

    
    def getDivider(self):
        return self._DebugViewItem__divider

    
    def setFont(self, font2):
        self._guiName.font = str(font2[0])
        self._guiValue.font = str(font2[1])

    
    def setFontName(self, font):
        self._guiValue.font = str(font)

    
    def setFontValue(self, font):
        self._guiName.font = str(font)

    
    def getFont(self):
        return (self._guiName.font, self._guiValue.font)

    
    def getFontName(self):
        return self._guiName.font

    
    def getFontValue(self):
        return self._guiValue.font

    
    def setColour(self, colour2):
        self._guiName.colour = tuple(colour2[0])
        self._guiValue.colour = tuple(colour2[1])

    
    def setColourName(self, colour):
        self._guiName.colour = tuple(colour)

    
    def setColourValue(self, colour):
        self._guiValue.colour = tuple(colour)

    
    def getColour(self):
        return (self._guiName.colour, self._guiValue.colour)

    
    def getColourName(self):
        return self._guiName.colour

    
    def getColourValue(self):
        return self._guiValue.colour

    
    def setMaterialFX(self, materialFX2):
        self._guiName.materialFX = str(materialFX2[0])
        self._guiValue.materialFX = str(materialFX2[1])

    
    def setMaterialFXName(self, materialFX):
        self._guiName.materialFX = str(materialFX)

    
    def setMaterialFXValue(self, materialFX):
        self._guiValue.materialFX = str(materialFX)

    
    def getMaterialFX(self):
        return (self._guiName.materialFX, self._guiValue.materialFX)

    
    def getMaterialFXName(self):
        return self._guiName.materialFX

    
    def getMaterialFXValue(self):
        return self._guiValue.materialFX

    
    def setVisible(self, bValue):
        self._guiName.visible = bool(bValue)
        self._guiValue.visible = bool(bValue)

    
    def getVisible(self):
        return self._guiName.visible

    
    def getHeight(self):
        return self._guiName.size[1]

    
    def _setPosition(self, pos2):
        (self._guiName.position, self._guiValue.position) = pos2

    
    def _getPosition(self):
        return (self._guiName.position, self._guiValue.position)

    
    def _rebuild(self):
        saved_font2 = self.getFont()
        saved_colour2 = self.getColour()
        saved_materialFX2 = self.getMaterialFX()
        saved_position2 = self._getPosition()
        saved_visible = self.getVisible()
        self._DebugViewItem__createGUI()
        self.setFont(saved_font2)
        self.setColour(saved_colour2)
        self.setMaterialFX(saved_materialFX2)
        self._setPosition(saved_position2)
        self.setVisible(saved_visible)

    
    def _DebugViewItem__createGUI(self):
        self._guiName = GUI.Text(self._DebugViewItem__name + self._DebugViewItem__divider)
        self._guiName.horizontalAnchor = 'LEFT'
        self._guiName.verticalAnchor = 'TOP'
        self._guiValue = GUI.Text(self._DebugViewItem__value)
        self._guiValue.horizontalAnchor = 'LEFT'
        self._guiValue.verticalAnchor = 'TOP'

    
    def _DebugViewItem__destroyGUI(self):
        if not self._guiName.parent is None:
            raise AssertionError
        if not self._guiValue.parent is None:
            raise AssertionError
        GUI.delRoot(self._guiName)
        self._guiName = None
        GUI.delRoot(self._guiValue)
        self._guiValue = None



def LU2BW(point3d, parent = None):
    if parent is None:
        sizeX = -2
        sizeY = 2
    else:
        (sizeX, sizeY) = parent.size
        sizeX = -sizeX
    return (sizeX * 0.5 + point3d[0], sizeY * 0.5 - point3d[1], point3d[2])


