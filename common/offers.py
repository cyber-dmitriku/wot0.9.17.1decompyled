# Source Generated with Decompyle++
# File: offers.pyc (Python 2.6)

import time
from collections import namedtuple
import BigWorld
from constants import IS_BASEAPP
from debug_utils import *
ENTITY_TYPE_ACCOUNT = 0
ENTITY_TYPE_CLAN = 1
ENTITY_TYPE_NAMES_BY_IDS = ('Account', 'Clan')
ENTITY_TYPE_IDS_BY_NAMES = {
    'Account': ENTITY_TYPE_ACCOUNT,
    'Clan': ENTITY_TYPE_CLAN }
ENTITY_TYPE_IDS = (ENTITY_TYPE_ACCOUNT, ENTITY_TYPE_CLAN)
OFFER_SELL = 0
_OFFER_KIND_MASK = 192
SRC_WARE_GOLD = 0
SRC_WARE_CREDITS = 256
SRC_WARE_ITEMS = 512
SRC_WARE_VEHICLE = 768
SRC_WARE_TANKMAN = 1024
SRC_WARE_KINDS = (SRC_WARE_GOLD, SRC_WARE_CREDITS, SRC_WARE_ITEMS, SRC_WARE_VEHICLE, SRC_WARE_TANKMAN)
SRC_WARE_MONEY_KINDS = (SRC_WARE_GOLD, SRC_WARE_CREDITS)
_SRC_WARE_KIND_MASK = 3840
DST_WARE_GOLD = 0
DST_WARE_CREDITS = 4096
DST_WARE_KINDS = (DST_WARE_GOLD, DST_WARE_CREDITS)
_DST_WARE_KIND_MASK = 61440

def makeOfferFlags(offerKind, srcWareKind, dstWareKind, srcEntityType, dstEntityType):
    return offerKind | srcWareKind | dstWareKind | srcEntityType | dstEntityType << 3

ParsedOfferFlags = namedtuple('ParsedOfferFlags', 'offerKind srcWareKind dstWareKind srcEntityType dstEntityType')

def parseOfferFlags(flags):
    raw = (flags & _OFFER_KIND_MASK, flags & _SRC_WARE_KIND_MASK, flags & _DST_WARE_KIND_MASK, flags & 7, flags >> 3 & 7)
    return ParsedOfferFlags._make(raw)


def parseSrcEntityTypeFromFlags(flags):
    return flags & 7


def parseDstEntityTypeFromFlags(flags):
    return flags >> 3 & 7


class OutOffers(object):
    Offer = namedtuple('Offer', 'flags dstDBID dstName srcWares dstWares validTill fee')
    
    def __init__(self, offersDict, outWriterGetter = None):
        offersDict.setdefault('nextID', 0)
        offersDict.setdefault('done', { })
        offersDict.setdefault('out', { })
        self._OutOffers__data = offersDict
        if outWriterGetter is not None:
            pass
        1
        self._OutOffers__outWriter = _WriterGetter(offersDict['out'])

    
    def __getitem__(self, offerID):
        return _makeOutOffer(self._OutOffers__data['out'][offerID])

    
    def get(self, offerID):
        offer = self._OutOffers__data['out'].get(offerID)
        if offer is not None:
            return _makeOutOffer(offer)

    
    def getExt(self, offerID, default = None):
        outExt = self._OutOffers__data.get('outExt')
        if outExt is None:
            return default
        return outExt.get(offerID, default)

    
    def items(self):
        continue
        return [ (id, _makeOutOffer(data)) for (id, data) in self._OutOffers__data['out'].iteritems() ]

    
    def clear(self):
        self._OutOffers__data['out'].clear()
        self._OutOffers__data['done'].clear()
        self._OutOffers__data.pop('outExt', None)
        self._OutOffers__data['nextID'] += 1

    
    def count(self):
        return len(self._OutOffers__data['out'])

    
    def doneOffers(self):
        return self._OutOffers__data['done']

    
    def timedOutOffers(self):
        res = []
        currTime = int(time.time())
        for (offerID, offer) in self._OutOffers__data['out'].iteritems():
            if offer[5] <= currTime:
                res.append(offerID)
                continue
        
        return res

    
    def inventorySlots(self):
        vehs = []
        numTmen = 0
        for offer in self._OutOffers__data['out'].itervalues():
            srcWareKind = offer[0] & _SRC_WARE_KIND_MASK
            if srcWareKind == SRC_WARE_VEHICLE:
                vehs.append(offer[3][0])
                continue
            if srcWareKind == SRC_WARE_TANKMAN:
                numTmen += 1
                continue
        
        return (vehs, numTmen)

    
    def moveToDone(self, offerID):
        data = self._OutOffers__data
        data['done'][offerID] = self._OutOffers__outWriter().pop(offerID)
        outExt = data.get('outExt')
        if outExt is not None:
            outExt.pop(offerID, None)
        
        data['nextID'] += 1
        return len(data['done'])

    
    def remove(self, offerID):
        if self._OutOffers__outWriter().pop(offerID, None) is not None:
            self._OutOffers__data['nextID'] += 1
            outExt = self._OutOffers__data.get('outExt')
            if outExt is not None:
                outExt.pop(offerID, None)
            
        

    
    def removeDone(self, offerID):
        self._OutOffers__data['done'].pop(offerID, None)

    
    def updateDestination(self, offerID, dstEntityType, dstEntityDBID, dstEntityName):
        if not self._OutOffers__data['out'][offerID][1] == dstEntityDBID:
            raise AssertionError

    
    def createOffer(self, flags, srcDBID, srcName, dstDBID, dstName, validSec, srcWares, srcFee, dstWares, dstFee, ext = None):
        currTime = int(time.time())
        validTill = currTime + int(validSec)
        offer = (flags, dstDBID, dstName, srcWares, dstWares, validTill, srcFee)
        data = self._OutOffers__data
        offerID = ((currTime & 1048575) << 12) + (data['nextID'] & 4095)
        data['nextID'] += 1
        if not offerID not in data['out'] or offerID not in data['done']:
            raise AssertionError
        self._OutOffers__outWriter()[offerID] = offer
        if ext is not None:
            data.setdefault('outExt', { })[offerID] = ext
        
        return (offerID, (offerID, flags, srcDBID, srcName, srcWares, dstWares, validTill, dstFee))



class InOffers(object):
    Offer = namedtuple('Offer', 'srcOfferID flags srcDBID srcName srcWares dstWares validTill fee')
    
    def __init__(self, offersDict, inWriterGetter = None):
        offersDict.setdefault('nextID', 0)
        offersDict.setdefault('in', { })
        self._InOffers__data = offersDict
        if inWriterGetter is not None:
            pass
        1
        self._InOffers__inWriter = _WriterGetter(offersDict['in'])

    
    def __getitem__(self, offerID):
        return _makeInOffer(self._InOffers__data['in'][offerID])

    
    def get(self, offerID):
        offer = self._InOffers__data['in'].get(offerID)
        if offer is not None:
            return _makeInOffer(offer)

    
    def items(self):
        continue
        return [ (id, _makeOutOffer(data)) for (id, data) in self._InOffers__data['in'].iteritems() ]

    
    def clear(self):
        self._InOffers__data['in'].clear()
        self._InOffers__data['nextID'] += 1

    
    def count(self):
        return len(self._InOffers__data['in'])

    
    def timedOutOffers(self):
        res = []
        currTime = int(time.time())
        for (offerID, offer) in self._InOffers__data['in'].iteritems():
            if offer[6] <= currTime:
                res.append(offerID)
                continue
        
        return res

    
    def findOfferBySource(self, srcEntityType, srcEntityDBID, srcOfferID):
        for (inOfferID, offer) in self._InOffers__data['in'].iteritems():
            if offer[0] == srcOfferID and offer[2] == srcEntityDBID and parseSrcEntityTypeFromFlags(offer[1]) == srcEntityType:
                return inOfferID
        

    
    def add(self, offer):
        data = self._InOffers__data
        offerID = data['nextID']
        data['nextID'] += 1
        self._InOffers__inWriter()[offerID] = tuple(offer)
        return offerID

    
    def remove(self, offerID):
        if self._InOffers__inWriter().pop(offerID, None) is not None:
            self._InOffers__data['nextID'] += 1
        



def collectOutOfferResults(outOffer):
    offerFlags = parseOfferFlags(outOffer.flags)
    gold = 0
    credits = 0
    items = None
    if offerFlags.srcWareKind == SRC_WARE_GOLD:
        gold -= outOffer.srcWares + outOffer.fee
    elif offerFlags.srcWareKind == SRC_WARE_CREDITS:
        credits -= outOffer.srcWares + outOffer.fee
    else:
        items = outOffer.srcWares
    if offerFlags.dstWareKind == DST_WARE_GOLD:
        gold += outOffer.dstWares
    else:
        credits += outOffer.dstWares
    return (offerFlags, gold, credits, items)


def collectInOfferResults(inOffer):
    offerFlags = parseOfferFlags(inOffer.flags)
    gold = 0
    credits = 0
    items = None
    if offerFlags.srcWareKind == SRC_WARE_GOLD:
        gold += inOffer.srcWares
    elif offerFlags.srcWareKind == SRC_WARE_CREDITS:
        credits += inOffer.srcWares
    else:
        items = inOffer.srcWares
    if offerFlags.dstWareKind == DST_WARE_GOLD:
        gold -= inOffer.dstWares + inOffer.fee
    else:
        credits -= inOffer.dstWares + inOffer.fee
    return (offerFlags, gold, credits, items)

_makeOutOffer = OutOffers.Offer._make
_makeInOffer = InOffers.Offer._make

class _WriterGetter(object):
    
    def __init__(self, dict):
        self._WriterGetter__d = dict

    
    def __call__(self):
        return self._WriterGetter__d



