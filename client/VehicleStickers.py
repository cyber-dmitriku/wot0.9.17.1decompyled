# Source Generated with Decompyle++
# File: VehicleStickers.pyc (Python 2.6)

import BigWorld
import Account
import Vehicle
import items
import Event
import Math
import BattleReplay
from debug_utils import *

class VehicleStickers:
    
    def __init__(self, vDesc, emblemSlots, onHull = True, prereqs = None):
        self._VehicleStickers__slotsByType = { }
        self._VehicleStickers__texParamsBySlotType = { }
        self._VehicleStickers__isLoadingClanEmblems = False
        self._VehicleStickers__clanID = 0
        self._VehicleStickers__model = None
        self._VehicleStickers__parentNode = None
        self._VehicleStickers__isDamaged = False
        g_cache = items.vehicles.g_cache
        self._VehicleStickers__calcTexParams(vDesc, emblemSlots, onHull, prereqs)
        if 'clan' in self._VehicleStickers__texParamsBySlotType:
            self._VehicleStickers__texParamsBySlotType['clan'] = [
                ('', '')]
        
        self._VehicleStickers__stickerModel = BigWorld.WGStickerModel()
        self._VehicleStickers__stickerModel.setLODDistances(vDesc.type.emblemsLodDist, vDesc.type.damageStickersLodDist)

    
    def _VehicleStickers__calcTexParams(self, vDesc, emblemSlots, onHull, prereqs):
        g_cache = items.vehicles.g_cache
        customizationCache = g_cache.customization(vDesc.type.id[0])
        playerEmblemsCache = g_cache.playerEmblems()
        inscriptionsCache = (customizationCache['inscriptionGroups'], customizationCache['inscriptions'])
        for slot in emblemSlots:
            slotType = slot[5]
            if self._VehicleStickers__slotsByType.has_key(slotType):
                self._VehicleStickers__slotsByType[slotType].append(slot)
            else:
                self._VehicleStickers__slotsByType[slotType] = [
                    slot]
            if slotType not in self._VehicleStickers__texParamsBySlotType:
                self._VehicleStickers__texParamsBySlotType[slotType] = []
            
            emblemsDesc = None
            emblemsCache = None
            if slotType == 'player':
                if onHull:
                    pass
                1
                emblemsDesc = vDesc.playerEmblems[2:]
                emblemsCache = playerEmblemsCache
            elif slotType == 'inscription':
                if onHull:
                    pass
                1
                emblemsDesc = vDesc.playerInscriptions[2:]
                emblemsCache = inscriptionsCache
            
            if emblemsDesc is None:
                texParams = (0, '', '')
                self._VehicleStickers__texParamsBySlotType[slotType] = [
                    texParams]
                continue
            
            descIdx = len(self._VehicleStickers__slotsByType[slotType]) - 1
            emblemID = emblemsDesc[descIdx][0]
            if emblemID is None:
                self._VehicleStickers__texParamsBySlotType[slotType].append(None)
                continue
            
            (texName, bumpTexName) = emblemsCache[1][emblemID][1:3]
            texParams = (texName, bumpTexName)
            self._VehicleStickers__texParamsBySlotType[slotType].append(texParams)
        

    
    def __destroy__(self):
        self._VehicleStickers__isLoadingClanEmblems = False
        self.detachStickers()

    
    def attachStickers(self, model, parentNode, isDamaged):
        self.detachStickers()
        self._VehicleStickers__model = model
        self._VehicleStickers__parentNode = parentNode
        self._VehicleStickers__isDamaged = isDamaged
        self._VehicleStickers__parentNode.attach(self._VehicleStickers__stickerModel)
        replayCtrl = BattleReplay.g_replayCtrl
        for (slotType, slots) in self._VehicleStickers__slotsByType.iteritems():
            if (slotType != 'clan' and self._VehicleStickers__clanID == 0 or replayCtrl.isPlaying) and replayCtrl.isOffline:
                self._VehicleStickers__doAttachStickers(slotType)
                continue
            if slotType == 'clan':
                if self._VehicleStickers__isLoadingClanEmblems:
                    return None
                self._VehicleStickers__isLoadingClanEmblems = True
                fileCache = Account.g_accountRepository.customFilesCache
                fileServerSettings = Account.g_accountRepository.fileServerSettings
                clan_emblems = fileServerSettings['clan_emblems']
                url = None
                
                try:
                    url = clan_emblems['url_template'] % self._VehicleStickers__clanID
                except:
                    LOG_ERROR('Failed to attach stickers to the vehicle - server returned incorrect url format: %s' % clan_emblems['url_template'])
                    return None

                fileCache.get(url, self._VehicleStickers__onClanEmblemLoaded)
                continue
        

    
    def detachStickers(self):
        if self._VehicleStickers__model is None:
            return None
        self._VehicleStickers__parentNode.detach(self._VehicleStickers__stickerModel)
        self._VehicleStickers__stickerModel.clear()
        self._VehicleStickers__model = None
        self._VehicleStickers__parentNode = None
        self._VehicleStickers__isDamaged = False

    
    def addDamageSticker(self, texName, bumpTexName, segStart, segEnd, sizes, rayUp):
        if self._VehicleStickers__model is None:
            return 0
        return self._VehicleStickers__stickerModel.addSticker(texName, bumpTexName, self._VehicleStickers__model, segStart, segEnd, sizes, rayUp)

    
    def delDamageSticker(self, handle):
        if self._VehicleStickers__model is not None:
            self._VehicleStickers__stickerModel.delSticker(handle)
        

    
    def setClanID(self, clanID):
        if self._VehicleStickers__clanID == clanID:
            return None
        self._VehicleStickers__clanID = clanID
        if self._VehicleStickers__model is not None:
            self.attachStickers(self._VehicleStickers__model, self._VehicleStickers__parentNode, self._VehicleStickers__isDamaged)
        

    
    def setAlphas(self, emblemAlpha, dmgStickerAlpha):
        self._VehicleStickers__stickerModel.setAlphas(emblemAlpha, dmgStickerAlpha)

    
    def _VehicleStickers__doAttachStickers(self, slotType):
        if (self._VehicleStickers__model is None or slotType == 'clan') and self._VehicleStickers__clanID == 0:
            return None
        slots = self._VehicleStickers__slotsByType[slotType]
        for (rayStart, rayEnd, rayUp, size, hideIfDamaged, _) in enumerate(slots):
            if hideIfDamaged or self._VehicleStickers__isDamaged or self._VehicleStickers__texParamsBySlotType[slotType][idx] is None:
                continue
            
            (texName, bumpTexName) = self._VehicleStickers__texParamsBySlotType[slotType][idx]
            sizes = Math.Vector2(size, size)
            if slotType == 'inscription':
                sizes.y *= 0.5
            
            self._VehicleStickers__stickerModel.addSticker(texName, bumpTexName, self._VehicleStickers__model, rayStart, rayEnd, sizes, rayUp)
        

    
    def _VehicleStickers__onClanEmblemLoaded(self, url, data):
        if not self._VehicleStickers__isLoadingClanEmblems:
            return None
        self._VehicleStickers__isLoadingClanEmblems = False
        if data is None:
            return None
        
        try:
            (texName, bumpTexName) = self._VehicleStickers__texParamsBySlotType['clan'][0]
            self._VehicleStickers__stickerModel.setTextureData(data)
            self._VehicleStickers__doAttachStickers('clan')
        except Exception:
            data is None
            LOG_CURRENT_EXCEPTION()
        except:
            data is None




