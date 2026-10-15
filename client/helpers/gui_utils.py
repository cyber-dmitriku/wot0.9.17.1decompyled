# Source Generated with Decompyle++
# File: gui_utils.pyc (Python 2.6)

import GUI
import Math

def setAnchor(component, hor, vert):
    component.horizontalAnchor = hor
    component.verticalAnchor = vert


def setPixMode(component):
    component.heightMode = 'PIXEL'
    component.widthMode = 'PIXEL'
    component.verticalPositionMode = 'PIXEL'
    component.horizontalPositionMode = 'PIXEL'


def pixToClipVector2(pixVector):
    scrRes = GUI.screenResolution()
    return Math.Vector2(2 * pixVector[0] / scrRes[0], -2 * pixVector[1] / scrRes[1])


def buildTexMapping(texCoords, texSize, fullTexSize):
    max = texCoords + texSize
    return ((texCoords[0] / fullTexSize[0], texCoords[1] / fullTexSize[1]), (texCoords[0] / fullTexSize[0], max[1] / fullTexSize[1]), (max[0] / fullTexSize[0], max[1] / fullTexSize[1]), (max[0] / fullTexSize[0], texCoords[1] / fullTexSize[1]))


