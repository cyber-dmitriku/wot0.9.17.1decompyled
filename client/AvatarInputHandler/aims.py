# Source Generated with Decompyle++
# File: aims.pyc (Python 2.6)

import BigWorld
import GUI
import Math
import ResMgr
from debug_utils import *
from gui.Scaleform.ColorSchemeManager import _ColorSchemeManager
from helpers import i18n
from helpers.func_utils import *
from gui import DEPTH_OF_Aim
from gui.Scaleform.Flash import Flash
from functools import partial
import math
import weakref
from account_helpers.AccountSettings import AccountSettings
import BattleReplay

def createAim(type):
    if type == 'strategic':
        return StrategicAim((0, 0))
    if type == 'arcade':
        return ArcadeAim((0, 0.15), False)
    if type == 'sniper':
        return ArcadeAim((0, 0), True)
    if type == 'postmortem':
        return PostMortemAim((0, 0))
    LOG_ERROR('Undefined aim type. <%s>' % type)


class Aim(Flash):
    _UPDATE_INTERVAL = 0.03
    _Aim__FLASH_CLASS = 'WGAimFlash'
    
    def __init__(self, mode, offset):
        Flash.__init__(self, 'crosshair_panel_{0:>s}.swf'.format(mode), self._Aim__FLASH_CLASS)
        self.component.wg_inputKeyMode = 2
        self.component.position.z = DEPTH_OF_Aim
        self.component.focus = False
        self.component.moveFocus = False
        self.component.heightMode = 'PIXEL'
        self.component.widthMode = 'PIXEL'
        self.movie.backgroundAlpha = 0
        self.flashSize = GUI.screenResolution()
        self._offset = offset
        self._isLoaded = False
        self.mode = mode
        self._Aim__timeInterval = _TimeInterval(Aim._UPDATE_INTERVAL, '_update', weakref.proxy(self))
        self._Aim__isColorBlind = AccountSettings.getSettings('isColorBlind')

    
    def prerequisites(self):
        return []

    
    def create(self):
        AccountSettings.onSettingsChanging += self.applySettings
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.replayContainsGunReloads:
            self._Aim__cbIdSetReloading = BigWorld.callback(0, self.setReloadingFromReplay)
        else:
            self._Aim__cbIdSetReloading = None

    
    def destroy(self):
        AccountSettings.onSettingsChanging -= self.applySettings
        self.close()
        if self._Aim__cbIdSetReloading is not None:
            BigWorld.cancelCallback(self._Aim__cbIdSetReloading)
            self._Aim__cbIdSetReloading = None
        
        self._Aim__timeInterval.stop()

    
    def applySettings(self, type):
        if type == 'arcade' and self.mode == 'arcade':
            settings = dict(AccountSettings.getSettings('arcade'))
            subSetting = settings['centralTag']
            self._flashCall('setCenterType', [
                subSetting['alpha'],
                subSetting['type']])
            subSetting = settings['net']
            self._flashCall('setNetType', [
                subSetting['alpha'],
                subSetting['type']])
            subSetting = settings['reloader']
            self._flashCall('setReloaderType', [
                subSetting['alpha'],
                subSetting['type']])
            subSetting = settings['condition']
            self._flashCall('setConditionType', [
                subSetting['alpha'],
                subSetting['type']])
            subSetting = settings['cassette']
            self._flashCall('setCassetteType', [
                subSetting['alpha'],
                subSetting['type']])
        
        if type == 'sniper' and self.mode == 'sniper':
            settings = dict(AccountSettings.getSettings('sniper'))
            subSetting = settings['snpCentralTag']
            self._flashCall('setCenterType', [
                subSetting['alpha'],
                subSetting['type']])
            subSetting = settings['snpNet']
            self._flashCall('setNetType', [
                subSetting['alpha'],
                subSetting['type']])
            subSetting = settings['snpReloader']
            self._flashCall('setReloaderType', [
                subSetting['alpha'],
                subSetting['type']])
            subSetting = settings['snpCondition']
            self._flashCall('setConditionType', [
                subSetting['alpha'],
                subSetting['type']])
            subSetting = settings['snpCassette']
            self._flashCall('setCassetteType', [
                subSetting['alpha'],
                subSetting['type']])
        
        if type == 'isColorBlind':
            self._Aim__isColorBlind = AccountSettings.getSettings('isColorBlind')
        

    
    def enable(self):
        self.active(True)
        self.applySettings(self.mode)
        self._Aim__timeInterval.start()
        _g_aimState['target']['id'] = None
        self._enable(_g_aimState, _g_aimState['isFirstInit'])
        _g_aimState['isFirstInit'] = False
        self.onRecreateDevice()

    
    def disable(self):
        self.active(False)
        _g_aimState['target']['id'] = None
        self._Aim__timeInterval.stop()
        self._disable()

    
    def updateMarkerPos(self, pos, relaxTime):
        self.component.updateMarkerPos(pos, relaxTime)

    
    def onRecreateDevice(self):
        screen = GUI.screenResolution()
        self.component.size = screen
        self._flashCall('onRecreateDevice', [
            screen[0],
            screen[1],
            self._offset[0],
            self._offset[1]])

    
    def setVisible(self, isVisible):
        self.component.visible = isVisible

    
    def offset(self, value = None):
        if value is not None:
            self._offset = value
            self.onRecreateDevice()
        else:
            return self._offset
        return value is not None

    
    def setTarget(self, target):
        state = _g_aimState['target']
        vInfo = dict(target.publicInfo)
        state['id'] = target.id
        state['startTime'] = None
        clanAbbrev = BigWorld.player().arena.vehicles.get(target.id, { }).get('clanAbbrev', '')
        if len(clanAbbrev) > 0:
            pass
        1
        state['name'] = '%s[%s]' % (vInfo['name'], clanAbbrev)(vInfo['name'])
        state['vType'] = i18n.convert(target.typeDescriptor.type.userString)
        state['isFriend'] = vInfo['team'] == BigWorld.player().team
        self._setTarget(state['name'], state['vType'], state['isFriend'])

    
    def clearTarget(self):
        state = _g_aimState['target']
        state['id'] = None
        state['startTime'] = BigWorld.time()
        self._clearTarget(0)

    
    def getTargetColor(self, isFriend):
        if isFriend:
            pass
        1
        colorScheme = 'aim_target_ally'('aim_target_enemy', isColorBlind = self._Aim__isColorBlind)
        return _ColorSchemeManager._makeRGB(colorScheme)

    
    def setReloading(self, duration, startTime = None):
        state = _g_aimState['reload']
        _isReloading = state.get('isReloading', False)
        _startTime = state.get('startTime', 0)
        _duration = state.get('duration', 0)
        isReloading = duration != 0
        state['isReloading'] = isReloading
        state['correction'] = None
        if _isReloading and duration > 0 and _duration > 0 and _startTime > 0:
            current = BigWorld.time()
            state['correction'] = {
                'timeRemaining': duration,
                'startTime': current,
                'startPosition': (current - _startTime) / _duration }
            self._correctReloadingTime(duration)
        else:
            state['duration'] = duration
            if isReloading:
                pass
            1
            state['startTime'] = None
            self._setReloading(duration, 0, isReloading)

    
    def setHealth(self, current):
        state = _g_aimState['health']
        state['cur'] = current
        if state['max'] is None:
            state['max'] = float(BigWorld.player().vehicleTypeDescriptor.maxHealth)
        
        self._setHealth(state['cur'], state['max'])

    
    def setAmmoStock(self, quantity, quantityInClip, clipReloaded = False):
        _g_aimState['ammo'] = (quantity, quantityInClip)
        self._setAmmoStock(quantity, quantityInClip, clipReloaded = clipReloaded)

    
    def getAmmoState(self, quantity, quantityInClip):
        (clipCapacity, burst) = _g_aimState['clip']
        state = 'normal'
        isLow = quantity < 3
        if clipCapacity > 1:
            state = self._getClipState(clipCapacity, burst, quantityInClip)
            isLow |= (quantity <= clipCapacity)
        
        return (isLow, state)

    
    def setClipParams(self, capacity, burst):
        _g_aimState['clip'] = (capacity, burst)
        if capacity > 1:
            self._setClipParams(capacity, burst)
        

    
    def showHit(self, gYaw, isDamage):
        _g_aimState['hitIndicators'].append({
            'gYaw': gYaw,
            'startTime': BigWorld.time(),
            'isDamage': isDamage })
        self._showHit(_g_aimState['hitIndicators'][-1:][0])

    
    def isGunReload(self):
        return _g_aimState['reload']['isReloading']

    
    def resetVehicleMatrix(self):
        pass

    
    def _enable(self, state, isFirstInit):
        pass

    
    def _disable(self):
        pass

    
    def _showHit(self, hitDesc):
        pass

    
    def _setTarget(self, name, vType, isFriend):
        self._flashCall('setTarget', [
            name,
            vType,
            self.getTargetColor(isFriend)])

    
    def _clearTarget(self, startTime):
        self._flashCall('clearTarget', [
            startTime])

    
    def setReloadingFromReplay(self):
        self._setReloadingAsPercent(100 * BattleReplay.g_replayCtrl.getGunReloadAmountLeft())
        self._Aim__cbIdSetReloading = BigWorld.callback(0, self.setReloadingFromReplay)

    
    def _setReloading(self, duration, startTime = None, isReloading = True, correction = None):
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.replayContainsGunReloads:
            return None
        if replayCtrl.isRecording:
            replayCtrl.setGunReloadTime(startTime, duration)
        
        if correction is not None:
            params = self._getCorrectionReloadingParams(correction)
            if params is not None:
                self._flashCall('setReloading', params)
            
        else:
            self._flashCall('setReloading', [
                duration,
                startTime,
                isReloading,
                None])

    
    def _setReloadingAsPercent(self, percent):
        self._flashCall('setReloadingAsPercent', [
            percent])

    
    def _correctReloadingTime(self, duration):
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.replayContainsGunReloads:
            self.setReloadingFromReplay()
            return None
        self._flashCall('correctReloadingTime', [
            duration])

    
    def _getCorrectionReloadingParams(self, correction):
        cTimeRemaining = correction.get('timeRemaining', 0)
        cStartTime = correction.get('startTime', 0)
        cStartPosition = correction.get('startPosition', 0)
        if not cTimeRemaining > 0:
            LOG_WARNING('timeRemaining - invalid value ', cTimeRemaining)
            return None
        delta = BigWorld.time() - cStartTime
        currentPosition = cStartPosition + (delta / cTimeRemaining) * (1 - cStartPosition)
        return [
            cTimeRemaining - delta,
            cStartTime,
            True,
            currentPosition * 100]

    
    def _setHealth(self, cur, max):
        self._flashCall('setHealth', [
            cur / max])

    
    def _setAmmoStock(self, quantity, quantityInClip, clipReloaded = False):
        (isLow, state) = self.getAmmoState(quantity, quantityInClip)
        self._flashCall('setAmmoStock', [
            quantity,
            quantityInClip,
            isLow,
            state,
            clipReloaded])

    
    def _getClipState(self, capacity, burst, quantityInClip):
        state = 'normal'
        if burst > 1:
            total = math.ceil(float(capacity) / float(burst))
            current = math.ceil(float(quantityInClip) / float(burst))
        else:
            total = capacity
            current = quantityInClip
        if current <= 0.5 * total:
            if current == 1:
                pass
            1
            state = 'warning'
        
        return state

    
    def _setClipParams(self, capacity, burst):
        self._flashCall('setClipParams', [
            capacity,
            burst])

    
    def _update(self):
        targetID = _g_aimState['target']['id']
        if targetID is not None:
            targ = BigWorld.entity(targetID)
            if targ is None:
                self.clearTarget()
                LOG_ERROR('Invalid target ID')
            else:
                state = _g_aimState['target']
                state['dist'] = int((targ.position - BigWorld.player().getOwnVehiclePosition()).length)
                state['health'] = math.ceil(100 * max(0, targ.health) / targ.typeDescriptor.maxHealth)
        

    
    def _flashCall(self, funcName, args = None):
        self.call('Aim.' + funcName, args)



class StrategicAim(Aim):
    
    def __init__(self, offset, isPostMortem = False):
        Aim.__init__(self, 'strategic', offset)

    
    def create(self):
        Aim.create(self)
        self._StrategicAim__damageCtrl = _DamageIndicatorCtrl(self._offset)

    
    def onRecreateDevice(self):
        Aim.onRecreateDevice(self)
        self._StrategicAim__damageCtrl.onRecreateDevice()

    
    def destroy(self):
        Aim.destroy(self)
        self._StrategicAim__damageCtrl.disable()
        self._StrategicAim__damageCtrl = None

    
    def _enable(self, state, isFirstInit):
        self._StrategicAim__damageCtrl.enable()
        if isFirstInit:
            return None
        Aim._flashCall(self, 'updateDistance', [
            self._getAimDistance()])
        hs = state['health']
        self._setHealth(hs['cur'], hs['max'])
        rs = state['reload']
        if rs['startTime'] is not None:
            self._setReloading(rs['duration'], startTime = BigWorld.time() - rs['startTime'], correction = rs['correction'])
        else:
            self._setReloading(rs['duration'], 0, False)
        (capacity, burst) = state['clip']
        if capacity > 1:
            self._setClipParams(capacity, burst)
        
        self._setAmmoStock(*state['ammo'])

    
    def _disable(self):
        self._StrategicAim__damageCtrl.disable()

    
    def _showHit(self, hitDesc):
        self._StrategicAim__damageCtrl.add(hitDesc)

    
    def _update(self):
        Aim._update(self)
        Aim._flashCall(self, 'updateDistance', [
            self._getAimDistance()])

    
    def _clearTarget(self, startTime):
        pass

    
    def _getAimDistance(self):
        (x, y, z) = BigWorld.player().gunRotator.markerInfo[0]
        v = BigWorld.player().getOwnVehiclePosition() - Math.Vector3(x, y, z)
        return int(v.length)



class PostMortemAim(Aim):
    
    def __init__(self, offset):
        Aim.__init__(self, 'postmortem', offset)
        self._PostMortemAim__msgCaption = i18n.makeString('#ingame_gui:player_messages/postmortem_caption')

    
    def create(self):
        Aim.create(self)
        self._PostMortemAim__vID = None

    
    def destroy(self):
        Aim.destroy(self)

    
    def changeVehicle(self, vID):
        self._PostMortemAim__vID = vID

    
    def _update(self):
        Aim._update(self)
        if self._PostMortemAim__vID is not None:
            vehicle = BigWorld.entity(self._PostMortemAim__vID)
            if vehicle is not None:
                name = vehicle.publicInfo['name']
                type = vehicle.typeDescriptor.type.userString
                healthPercent = math.ceil(100 * max(0, vehicle.health) / vehicle.typeDescriptor.maxHealth)
                self._PostMortemAim__setText(name, type, healthPercent)
            
        
        Aim._flashCall(self, 'updateTarget', [
            _g_aimState['target']['dist']])

    
    def _PostMortemAim__setText(self, name, type, health):
        text = i18n.convert(self._PostMortemAim__msgCaption % {
            'name': name,
            'type': type,
            'health': health })
        Aim._flashCall(self, 'updatePlayerInfo', [
            text])



class ArcadeAim(Aim):
    
    def __init__(self, offset, isSniper):
        if isSniper:
            pass
        1
        self('sniper', 'arcade', offset)
        self._ArcadeAim__isSniper = isSniper

    
    def create(self):
        Aim.create(self)
        self._ArcadeAim__damageCtrl = _DamageIndicatorCtrl(self._offset)

    
    def destroy(self):
        Aim.destroy(self)
        self._ArcadeAim__damageCtrl.disable()
        self._ArcadeAim__damageCtrl = None

    
    def _enable(self, state, isFirstInit):
        self._ArcadeAim__damageCtrl.enable()
        if isFirstInit:
            return None
        ts = state['target']
        if ts['startTime'] is not None:
            self._setTarget(ts['name'], ts['vType'], ts['isFriend'])
            Aim._flashCall(self, 'updateTarget', [
                ts['dist']])
            self._clearTarget(BigWorld.time() - ts['startTime'])
        
        hs = state['health']
        self._setHealth(hs['cur'], hs['max'])
        rs = state['reload']
        if rs['startTime'] is not None:
            self._setReloading(rs['duration'], startTime = BigWorld.time() - rs['startTime'], correction = rs['correction'])
        else:
            self._setReloading(rs['duration'], 0, False)
        (capacity, burst) = state['clip']
        if capacity > 1:
            self._setClipParams(capacity, burst)
        
        self._setAmmoStock(*state['ammo'])

    
    def _disable(self):
        self._ArcadeAim__damageCtrl.disable()

    
    def setVisible(self, isVisible):
        Aim.setVisible(self, isVisible)
        self._ArcadeAim__damageCtrl.setVisible(isVisible)

    
    def onRecreateDevice(self):
        Aim.onRecreateDevice(self)
        self._ArcadeAim__damageCtrl.onRecreateDevice()

    
    def _showHit(self, hitDesc):
        self._ArcadeAim__damageCtrl.add(hitDesc)

    
    def _update(self):
        Aim._update(self)
        Aim._flashCall(self, 'updateTarget', [
            _g_aimState['target']['dist']])



class _DamageIndicatorCtrl:
    _HIT_INDICATOR_MAX_ON_SCREEN = 5
    
    def __init__(self, offset):
        self.proxy = weakref.proxy(self)
        self._DamageIndicatorCtrl__worldToClip = None
        self._DamageIndicatorCtrl__isVisible = True
        self._DamageIndicatorCtrl__offset = offset
        self._DamageIndicatorCtrl__hits = list()

    
    def enable(self):
        for hitDesc in _g_aimState['hitIndicators'][:]:
            self.add(hitDesc)
        

    
    def disable(self):
        for hitDesc in _g_aimState['hitIndicators']:
            if hitDesc.get('comp', None) is not None:
                hitDesc['comp'].close()
                BigWorld.cancelCallback(hitDesc['callbackID'])
                hitDesc['comp'] = None
                hitDesc['callbackID'] = None
                continue
        

    
    def setVisible(self, isVisible):
        self._DamageIndicatorCtrl__isVisible = isVisible
        for hitDesc in _g_aimState['hitIndicators']:
            if hitDesc.get('comp', None) is not None:
                hitDesc['comp'].component.visible = isVisible
                continue
        

    
    def add(self, hitDesc):
        duration = _DamageIndicator.TOTAL_FRAMES / float(_DamageIndicator.FRAME_RATE)
        globalYaw = hitDesc['gYaw']
        startTime = hitDesc['startTime']
        isDamage = hitDesc['isDamage']
        timePass = BigWorld.time() - startTime
        if timePass >= duration:
            self._remove(startTime)
            return None
        if len(_g_aimState['hitIndicators']) >= self._HIT_INDICATOR_MAX_ON_SCREEN:
            self._remove(min((lambda .0: for desc in .0:
desc['startTime'])(_g_aimState['hitIndicators'])))
        
        hitInd = _DamageIndicator()
        hitInd.setup(globalYaw, self._DamageIndicatorCtrl__offset)
        hitInd.active(True)
        hitInd.component.visible = self._DamageIndicatorCtrl__isVisible
        hitInd.call('DamageIndicator.setDamageFlagAndAnimFrame', [
            isDamage,
            timePass * _DamageIndicator.FRAME_RATE])
        callbackID = BigWorld.callback(duration, partial(callMethod, self.proxy, '_remove', startTime))
        hitDesc['comp'] = hitInd
        hitDesc['callbackID'] = callbackID

    
    def onRecreateDevice(self):
        for desc in _g_aimState['hitIndicators']:
            desc['comp'].setup(desc['gYaw'], self._DamageIndicatorCtrl__offset)
        

    
    def _remove(self, startTime):
        removedDesc = None
        for desc in _g_aimState['hitIndicators']:
            if desc['startTime'] == startTime:
                removedDesc = desc
                break
                continue
        
        if removedDesc is not None:
            if removedDesc.get('comp', None) is not None:
                removedDesc['comp'].close()
            
            _g_aimState['hitIndicators'].remove(removedDesc)
        



class _DamageIndicator(Flash):
    _DamageIndicator__SWF_FILE_NAME = 'DamageIndicator.swf'
    _DamageIndicator__FLASH_CLASS = 'WGHitIndicatorFlash'
    _DamageIndicator__FLASH_MC_NAME = 'damageMC'
    _DamageIndicator__FLASH_SIZE = (680, 680)
    TOTAL_FRAMES = 90
    FRAME_RATE = 24
    
    def __init__(self):
        Flash.__init__(self, self._DamageIndicator__SWF_FILE_NAME, self._DamageIndicator__FLASH_CLASS, [
            self._DamageIndicator__FLASH_MC_NAME])
        self.component.wg_inputKeyMode = 2
        self.component.position.z = DEPTH_OF_Aim
        self.movie.backgroundAlpha = 0
        self.component.focus = False
        self.component.moveFocus = False
        self.component.heightMode = 'PIXEL'
        self.component.widthMode = 'PIXEL'
        self.flashSize = self._DamageIndicator__FLASH_SIZE

    
    def setup(self, gYaw, offset):
        self.component.position.x = offset[0]
        self.component.position.y = offset[1]
        self.component.wg_globalYaw = gYaw

    
    def __del__(self):
        pass



class _TimeInterval:
    
    def __init__(self, interval, funcName, scopeProxy = None):
        self._TimeInterval__cbId = None
        self._TimeInterval__interval = interval
        self._TimeInterval__funcName = funcName
        self._TimeInterval__scopeProxy = scopeProxy

    
    def start(self):
        if self._TimeInterval__cbId is not None:
            LOG_ERROR('To start a new time interval You should before stop already the running time interval.')
            return None
        self._TimeInterval__cbId = BigWorld.callback(self._TimeInterval__interval, self._TimeInterval__update)

    
    def stop(self):
        if self._TimeInterval__cbId is not None:
            BigWorld.cancelCallback(self._TimeInterval__cbId)
            self._TimeInterval__cbId = None
        

    
    def _TimeInterval__update(self):
        self._TimeInterval__cbId = None
        if self._TimeInterval__scopeProxy is not None:
            funcObj = getattr(self._TimeInterval__scopeProxy, self._TimeInterval__funcName, None)
            if funcObj is not None:
                funcObj()
            
        
        self._TimeInterval__cbId = BigWorld.callback(self._TimeInterval__interval, self._TimeInterval__update)



def clearState():
    global _g_aimState
    _g_aimState = {
        'isFirstInit': True,
        'target': {
            'id': None,
            'dist': 0,
            'health': 0,
            'startTime': None,
            'name': None,
            'vType': None,
            'isFriend': None },
        'reload': { },
        'hitIndicators': [],
        'ammo': (0, 0),
        'clip': (1, 1),
        'health': {
            'cur': None,
            'max': None } }

_g_aimState = None

