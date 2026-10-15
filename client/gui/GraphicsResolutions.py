# Source Generated with Decompyle++
# File: GraphicsResolutions.pyc (Python 2.6)

import BigWorld
from debug_utils import LOG_CURRENT_EXCEPTION, LOG_ERROR, LOG_DEBUG

class GraphicsResolutions(object):
    MIN_HEIGHT = 768
    MIN_WIDTH = 1024
    MIN_COLOR_DEPTH = 23
    
    def _GraphicsResolutions__gcd(self, a, b):
        while a != 0:
            a = b % a
            b = a
        return b

    
    def __init__(self):
        self._GraphicsResolutions__allVideoModes = []
        maxWidth = 0
        maxHeight = 0
        self.ASPECT_RATIO = []
        self.ASPECT_RATIO.append((4, 3))
        self.ASPECT_RATIO.append((16, 9))
        self.ASPECT_RATIO.append((16, 10))
        self.ASPECT_RATIO.append((19, 10))
        for monitorModes in BigWorld.listVideoModesAllMonitors():
            modes = []
            for mode in monitorModes:
                if self._GraphicsResolutions__isVideoModeSuitable(mode):
                    modes.append(mode)
                    if mode[1] > maxWidth:
                        maxWidth = mode[1]
                    
                    if mode[2] > maxHeight:
                        maxHeight = mode[2]
                    
                mode[2] > maxHeight
            
            self._GraphicsResolutions__allVideoModes.append(modes)
        
        LOG_DEBUG('max resolution : %d / %d' % (maxWidth, maxHeight))
        if maxHeight > 0:
            _3dVisionAspectRatio = float(maxWidth) / float(maxHeight)
            LOG_DEBUG('aspect ratio : %f' % _3dVisionAspectRatio)
            if _3dVisionAspectRatio > 3.75:
                gcd = self._GraphicsResolutions__gcd(maxWidth, maxHeight)
                LOG_DEBUG('aspect ratio inted: %d / %d' % (maxWidth / gcd, maxHeight / gcd))
                self.ASPECT_RATIO.append((maxWidth / gcd, maxHeight / gcd))
            
        
        self._GraphicsResolutions__multisamplingTypes = BigWorld.getSupportedMultisamplingTypes()
        self._GraphicsResolutions__multisamplingTypes.insert(0, 0)
        self._GraphicsResolutions__customAAModes = BigWorld.getSupportedCustomAAModes()
        self._GraphicsResolutions__monitors = BigWorld.wg_getMonitorNames()
        self._GraphicsResolutions__curentMonitorIndex = BigWorld.wg_getActiveMonitorIndex()
        self._GraphicsResolutions__monitorChanged = False
        self._GraphicsResolutions__lastFullscreenSize = None
        self._GraphicsResolutions__lastWindowedSize = None
        BigWorld.wg_setSavePreferencesCallback(self.onSavePreferencesXml)

    
    def __windowSizes(self):
        _GraphicsResolutions__windowSizes = []
        for monitorModes in self._GraphicsResolutions__allVideoModes:
            maxWindow = BigWorld.wg_getMaxWindowedResolution(len(_GraphicsResolutions__windowSizes))
            modes = []
            for m in monitorModes:
                if m[1] > maxWindow[0] or m[2] > maxWindow[1]:
                    continue
                
                modes.append((m[1], m[2]))
            
            if maxWindow not in modes:
                modes.append(maxWindow)
            
            _GraphicsResolutions__windowSizes.append(modes)
        
        return _GraphicsResolutions__windowSizes

    _GraphicsResolutions__windowSizes = property(__windowSizes)
    
    def __videoModes(self):
        continue
        return [ (m[0], m[1], m[2]) for m in self._GraphicsResolutions__allVideoModes[self.monitorIndex] ]

    _GraphicsResolutions__videoModes = property(__videoModes)
    
    def __aspectRatios(self):
        return g_graficsResolutions.ASPECT_RATIO

    _GraphicsResolutions__aspectRatios = property(__aspectRatios)
    
    def __videoMode(self):
        return BigWorld.videoModeIndex()

    _GraphicsResolutions__videoMode = property(__videoMode)
    
    def __windowSize(self):
        return tuple(map(int, BigWorld.wg_getCurrentResolution(True)))

    _GraphicsResolutions__windowSize = property(__windowSize)
    
    def __aspectRatio(self):
        return round(BigWorld.getFullScreenAspectRatio(), 6)

    _GraphicsResolutions__aspectRatio = property(__aspectRatio)
    
    def __multisamplingType(self):
        return BigWorld.getMultisamplingType()

    _GraphicsResolutions__multisamplingType = property(__multisamplingType)
    
    def __customAAMode(self):
        return BigWorld.getCustomAAMode()

    _GraphicsResolutions__customAAMode = property(__customAAMode)
    
    def isVideoWindowed(self):
        return BigWorld.isVideoWindowed()

    isVideoWindowed = property(isVideoWindowed)
    
    def isVideoVSync(self):
        return BigWorld.isVideoVSync()

    isVideoVSync = property(isVideoVSync)
    
    def isTripleBuffered(self):
        return BigWorld.isTripleBuffered()

    isTripleBuffered = property(isTripleBuffered)
    
    def videoModeIndex(self):
        for (index, videoModeInfo) in enumerate(self._GraphicsResolutions__videoModes):
            if videoModeInfo[0] == self._GraphicsResolutions__videoMode:
                return index
        
        return -1

    videoModeIndex = property(videoModeIndex)
    
    def monitorIndex(self):
        return BigWorld.wg_getActiveMonitorIndex()

    monitorIndex = property(monitorIndex)
    
    def realMonitorIndex(self):
        return self._GraphicsResolutions__curentMonitorIndex

    realMonitorIndex = property(realMonitorIndex)
    
    def windowSizeIndex(self):
        for (index, size) in enumerate(self._GraphicsResolutions__windowSizes[self._GraphicsResolutions__curentMonitorIndex]):
            if size == self._GraphicsResolutions__windowSize:
                return index
        
        return len(self._GraphicsResolutions__windowSizes[self._GraphicsResolutions__curentMonitorIndex])

    windowSizeIndex = property(windowSizeIndex)
    
    def aspectRatioIndex(self):
        for (index, size) in enumerate(self._GraphicsResolutions__aspectRatios):
            if round(float(size[0]) / size[1], 6) == self._GraphicsResolutions__aspectRatio:
                return index
        
        return len(self._GraphicsResolutions__aspectRatios)

    aspectRatioIndex = property(aspectRatioIndex)
    
    def multisamplingTypeIndex(self):
        if self._GraphicsResolutions__multisamplingType in self._GraphicsResolutions__multisamplingTypes:
            return self._GraphicsResolutions__multisamplingTypes.index(self._GraphicsResolutions__multisamplingType)
        return -1

    multisamplingTypeIndex = property(multisamplingTypeIndex)
    
    def customAAModeIndex(self):
        if self._GraphicsResolutions__customAAMode in self._GraphicsResolutions__customAAModes:
            return self._GraphicsResolutions__customAAModes.index(self._GraphicsResolutions__customAAMode)
        return -1

    customAAModeIndex = property(customAAModeIndex)
    
    def videoModesList(self):
        allModes = []
        for monitorModes in self._GraphicsResolutions__allVideoModes:
            modes = []
            for m in monitorModes:
                modes.append('%dx%d' % (m[1], m[2]))
            
            allModes.append(modes)
        
        return allModes

    videoModesList = property(videoModesList)
    
    def monitorsList(self):
        return self._GraphicsResolutions__monitors

    monitorsList = property(monitorsList)
    
    def windowSizesList(self):
        allModes = []
        for monitorModes in self._GraphicsResolutions__windowSizes:
            modes = []
            for m in monitorModes:
                modes.append('%dx%d' % m)
            
            current = '%dx%d' % self._GraphicsResolutions__windowSize
            if current not in modes:
                modes.append(current + '*')
            
            allModes.append(modes)
        
        return allModes

    windowSizesList = property(windowSizesList)
    
    def aspectRatiosList(self):
        continue
        aspectRatios = [ '%d:%d' % m for m in self._GraphicsResolutions__aspectRatios ]
        if self.aspectRatioIndex == len(self._GraphicsResolutions__aspectRatios):
            aspectRatios.append('%s:1*' % BigWorld.wg_getNiceNumberFormat(self._GraphicsResolutions__aspectRatio))
        
        return aspectRatios

    aspectRatiosList = property(aspectRatiosList)
    
    def multisamplingTypesList(self):
        continue
        return [ '#settings:multisamplingType/type%s' % i for i in self._GraphicsResolutions__multisamplingTypes ]

    multisamplingTypesList = property(multisamplingTypesList)
    
    def customAAModesList(self):
        continue
        return [ '#settings:customAAMode/mode%s' % i for i in self._GraphicsResolutions__customAAModes ]

    customAAModesList = property(customAAModesList)
    
    def _GraphicsResolutions__isVideoModeSuitable(self, videoMode):
        if videoMode[1] >= GraphicsResolutions.MIN_WIDTH and videoMode[2] >= GraphicsResolutions.MIN_HEIGHT:
            pass
        return videoMode[3] >= GraphicsResolutions.MIN_COLOR_DEPTH

    
    def getVideoModeByIndex(self, index):
        if len(self._GraphicsResolutions__videoModes) > index:
            pass
        index > -1
        if 1:
            return self._GraphicsResolutions__videoModes[int(index)][0]

    
    def getWindowSizeByIndex(self, index):
        if len(self._GraphicsResolutions__windowSizes[self._GraphicsResolutions__curentMonitorIndex]) > index:
            pass
        index > -1
        if 1:
            return self._GraphicsResolutions__windowSizes[self._GraphicsResolutions__curentMonitorIndex][int(index)]
        return self._GraphicsResolutions__windowSize

    
    def getAspectRatioByIndex(self, index):
        if len(self._GraphicsResolutions__aspectRatios) > index:
            pass
        index > -1
        if 1:
            ars = self._GraphicsResolutions__aspectRatios[int(index)]
            return round(float(ars[0]) / ars[1], 6)

    
    def getMultisamplingTypeByIndex(self, index):
        if len(self._GraphicsResolutions__multisamplingTypes) > index:
            pass
        index > -1
        if 1:
            return self._GraphicsResolutions__multisamplingTypes[int(index)]

    
    def getCustomAAModeByIndex(self, index):
        if len(self._GraphicsResolutions__customAAModes) > index:
            pass
        index > -1
        if 1:
            return self._GraphicsResolutions__customAAModes[int(index)]

    
    def gamma(self):
        return BigWorld.getGammaCorrection()

    gamma = property(gamma)
    
    def applyChanges(self, isFullScreen, isVideoVSync, isTripleBuffered, sizeIndex, aspectRatioIndex, multisamplingIndex, customAAIndex, gamma, monitorIndex):
        if self._GraphicsResolutions__curentMonitorIndex != monitorIndex:
            self._GraphicsResolutions__monitorChanged = True
        
        self._GraphicsResolutions__curentMonitorIndex = monitorIndex
        BigWorld.wg_setActiveMonitorIndex(monitorIndex)
        if self.isVideoVSync != isVideoVSync:
            BigWorld.setVideoVSync(isVideoVSync)
        
        if self.isTripleBuffered != isTripleBuffered:
            BigWorld.setTripleBuffering(isTripleBuffered)
        
        if self.gamma != gamma:
            gamma = max(gamma, 0.5)
            gamma = min(gamma, 2)
            BigWorld.setGammaCorrection(gamma)
        
        aspectRatio = self.getAspectRatioByIndex(aspectRatioIndex)
        if aspectRatio is not None and aspectRatio != self._GraphicsResolutions__aspectRatio:
            BigWorld.changeFullScreenAspectRatio(aspectRatio)
        
        multisamplingType = self.getMultisamplingTypeByIndex(multisamplingIndex)
        if self._GraphicsResolutions__multisamplingType != multisamplingType:
            BigWorld.setMultisamplingType(multisamplingType)
        
        customAAMode = self.getCustomAAModeByIndex(customAAIndex)
        if self._GraphicsResolutions__customAAMode != customAAMode:
            BigWorld.setCustomAAMode(customAAMode)
        
        if isFullScreen:
            videoMode = self.getVideoModeByIndex(sizeIndex)
            if not (self._GraphicsResolutions__monitorChanged):
                if videoMode != self._GraphicsResolutions__videoMode or self.isVideoWindowed:
                    BigWorld.changeVideoMode(videoMode, False)
                
            windowSize = self.getWindowSizeByIndex(sizeIndex)
            self._GraphicsResolutions__lastIsWindowed = False
            self._GraphicsResolutions__lastFullscreenSize = (windowSize[0], windowSize[1])
        elif not (self._GraphicsResolutions__monitorChanged) and not (self.isVideoWindowed):
            BigWorld.changeVideoMode(self.getVideoModeByIndex(sizeIndex), True)
        
        windowSize = self.getWindowSizeByIndex(sizeIndex)
        oldResolution = BigWorld.wg_getCurrentResolution(True)
        if windowSize is not None:
            if oldResolution[0] != windowSize[0] or oldResolution[1] != windowSize[1]:
                BigWorld.resizeWindow(windowSize[0], windowSize[1])
            
        self._GraphicsResolutions__lastIsWindowed = True
        self._GraphicsResolutions__lastWindowedSize = (windowSize[0], windowSize[1])

    
    def onSavePreferencesXml(self, root):
        if not self._GraphicsResolutions__monitorChanged:
            return None
        devPref = root['devicePreferences']
        devPref.writeBool('windowed', self._GraphicsResolutions__lastIsWindowed)
        if self._GraphicsResolutions__lastFullscreenSize is not None:
            devPref.writeInt('fullscreenWidth', self._GraphicsResolutions__lastFullscreenSize[0])
            devPref.writeInt('fullscreenHeight', self._GraphicsResolutions__lastFullscreenSize[1])
        
        if self._GraphicsResolutions__lastWindowedSize is not None:
            devPref.writeInt('windowedWidth', self._GraphicsResolutions__lastWindowedSize[0])
            devPref.writeInt('windowedHeight', self._GraphicsResolutions__lastWindowedSize[1])
        


g_graficsResolutions = GraphicsResolutions()

