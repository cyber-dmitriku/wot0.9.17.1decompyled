# Source Generated with Decompyle++
# File: HangarSpace.pyc (Python 2.6)

import BigWorld
from gui.ClientHangarSpace import ClientHangarSpace
from gui import GUI_SETTINGS
from gui.Scaleform.Waiting import Waiting
from CurrentVehicle import g_currentVehicle
from debug_utils import LOG_DEBUG, LOG_CURRENT_EXCEPTION
import nations

class _HangarSpace(object):
    isPremium = property((lambda self: if self._HangarSpace__spaceInited:
self._HangarSpace__isSpacePremiumself._HangarSpace__delayedIsPremium))
    
    def __init__(self):
        self._HangarSpace__space = ClientHangarSpace()
        self._HangarSpace__inited = False
        self._HangarSpace__spaceInited = False
        self._HangarSpace__isSpacePremium = False
        self._HangarSpace__delayedIsPremium = False
        self._HangarSpace__spacePath = None
        self._HangarSpace__delayedRefreshCallback = None
        self._HangarSpace__spaceDestroyedDuringLoad = False

    
    def space(self):
        if self.spaceInited:
            return self._HangarSpace__space

    space = property(space)
    
    def inited(self):
        return self._HangarSpace__inited

    inited = property(inited)
    
    def spaceInited(self):
        return self._HangarSpace__spaceInited

    spaceInited = property(spaceInited)
    
    def spaceLoading(self):
        return self._HangarSpace__space.spaceLoading()

    
    def init(self, isPremium):
        if not self._HangarSpace__spaceInited:
            LOG_DEBUG('_HangarSpace::init')
            Waiting.show('loadHangarSpace')
            self._HangarSpace__inited = True
            self._HangarSpace__isSpacePremium = isPremium
            self._HangarSpace__spacePath = self._HangarSpace__getSpacePath(isPremium)
            self._HangarSpace__space.create(isPremium, self._HangarSpace__spacePath, self._HangarSpace__spaceDone)
            g_currentVehicle.onChanged += self.refreshVehicle
            self.refreshVehicle()
        

    
    def refreshSpace(self, isPremium):
        if not self._HangarSpace__spaceInited:
            LOG_DEBUG('_HangarSpace::refreshSpace(isPremium={0!r:s}, space={1:>s}) - is delayed until space load is done'.format(isPremium, self._HangarSpace__spacePath))
            if self._HangarSpace__delayedRefreshCallback is None:
                self._HangarSpace__delayedRefreshCallback = BigWorld.callback(0.1, self._HangarSpace__delayedRefresh)
            
            self._HangarSpace__delayedIsPremium = isPremium
            return None
        spacePath = self._HangarSpace__getSpacePath(isPremium)
        LOG_DEBUG('_HangarSpace::refreshSpace(isPremium={0!r:s}, space={1:>s})'.format(isPremium, spacePath))
        if self._HangarSpace__isSpacePremium != isPremium or self._HangarSpace__spacePath != spacePath:
            self.destroy()
            self.init(isPremium)
        
        self._HangarSpace__isSpacePremium = isPremium

    
    def destroy(self):
        if self._HangarSpace__spaceInited:
            LOG_DEBUG('_HangarSpace::destroy')
            self._HangarSpace__inited = False
            self._HangarSpace__spaceInited = False
            self._HangarSpace__space.destroy()
            g_currentVehicle.onChanged -= self.refreshVehicle
        elif self.spaceLoading():
            LOG_DEBUG('_HangarSpace::destroy - delayed until space load done')
            self._HangarSpace__spaceDestroyedDuringLoad = True
        
        if self._HangarSpace__delayedRefreshCallback is not None:
            BigWorld.cancelCallback(self._HangarSpace__delayedRefreshCallback)
            self._HangarSpace__delayedRefreshCallback = None
        

    
    def refreshVehicle(self):
        if self._HangarSpace__inited:
            if self._HangarSpace__spaceInited:
                spacePath = self._HangarSpace__getSpacePath(self._HangarSpace__isSpacePremium)
                if spacePath != self._HangarSpace__spacePath:
                    self.refreshSpace(self._HangarSpace__isSpacePremium)
                
            
            Waiting.show('loadHangarSpaceVehicle', True)
            if g_currentVehicle.isInHangar() and g_currentVehicle.vehicle.modelState:
                self._HangarSpace__space.recreateVehicle(g_currentVehicle.vehicle.descriptor, g_currentVehicle.vehicle.modelState, self._HangarSpace__changeDone)
            else:
                self._HangarSpace__space.removeVehicle()
                self._HangarSpace__changeDone()
        

    
    def _HangarSpace__spaceDone(self):
        self._HangarSpace__spaceInited = True
        if self._HangarSpace__spaceDestroyedDuringLoad:
            self._HangarSpace__spaceDestroyedDuringLoad = False
            self.destroy()
        
        Waiting.hide('loadHangarSpace')

    
    def _HangarSpace__changeDone(self):
        Waiting.hide('loadHangarSpaceVehicle')

    
    def _HangarSpace__delayedRefresh(self):
        self._HangarSpace__delayedRefreshCallback = None
        if not self._HangarSpace__spaceInited:
            self._HangarSpace__delayedRefreshCallback = BigWorld.callback(0.1, self._HangarSpace__delayedRefresh)
            return None
        self.refreshSpace(self._HangarSpace__delayedIsPremium)

    
    def _HangarSpace__getSpacePath(self, isPremium):
        spaceName = self._HangarSpace__space.getDefSpacePath(isPremium)
        if GUI_SETTINGS.nationHangarSpace and g_currentVehicle.isPresent():
            
            try:
                (nationID, _) = g_currentVehicle.vehicle.descriptor.type.id
                nationName = nations.NAMES[nationID]
                spaceName = self._HangarSpace__space.getNationSpacePath(self._HangarSpace__isSpacePremium, nationName)
            except Exception:
                LOG_CURRENT_EXCEPTION()
            

        return spaceName


g_hangarSpace = _HangarSpace()

