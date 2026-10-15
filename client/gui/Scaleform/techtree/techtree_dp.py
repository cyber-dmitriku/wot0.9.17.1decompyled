# Source Generated with Decompyle++
# File: techtree_dp.pyc (Python 2.6)

from collections import defaultdict
from debug_utils import *
from gui import GUI_NATIONS_ORDER_INDEX
from gui.Scaleform.techtree import TREE_SHARED_REL_FILE_PATH, NATION_TREE_REL_FILE_PATH, _VEHICLE, _VEHICLE_TYPE_NAME, makeDefUnlockProps, UnlockProps
from items import _xml, vehicles, getTypeOfCompactDescr
import nations
import ResMgr
import Math

class _ConfigError(Exception):
    
    def __init__(self, ctx, msg):
        super(_ConfigError, self).__init__()
        self.msg = msg
        self.ctx = ctx

    
    def __str__(self):
        return 'Config error in {0:>s}. {1:>s}'.format(self.ctx[1], self.msg)



class _TechTreeDataProvider(object):
    
    def __init__(self):
        super(_TechTreeDataProvider, self).__init__()
        self._TechTreeDataProvider__loaded = False
        self._TechTreeDataProvider__availableNations = None
        self._clear()

    
    def _clear(self):
        self._TechTreeDataProvider__displayInfo = { }
        self._TechTreeDataProvider__topLevels = defaultdict(set)
        self._TechTreeDataProvider__topItems = defaultdict(set)
        self._TechTreeDataProvider__nextLevels = defaultdict((lambda : { }))

    
    def _TechTreeDataProvider__readShared(self, clearCache = False):
        if clearCache:
            ResMgr.purge(TREE_SHARED_REL_FILE_PATH)
        
        shared = {
            'grids': { },
            'default': { },
            'lines': { } }
        section = ResMgr.openSection(TREE_SHARED_REL_FILE_PATH)
        if section is None:
            _xml.raiseWrongXml(None, TREE_SHARED_REL_FILE_PATH, 'can not open or read')
        
        xmlCtx = (None, TREE_SHARED_REL_FILE_PATH)
        precessed = _xml.getChildren(xmlCtx, section, 'grids')
        for (name, gridSection) in precessed:
            coordinates = []
            xPath = '{0:>s}/{1:>s}'.format(TREE_SHARED_REL_FILE_PATH, name)
            subSec = _xml.getSubsection(xmlCtx, gridSection, 'root')
            xmlCtx = (None, '{0:>s}/vertical'.format(xPath))
            gridName = gridSection.asString
            subSec = _xml.getSubsection(xmlCtx, gridSection, 'root')
            xmlCtx = (None, '{0:>s}/root'.format(xPath))
            rootPos = {
                'start': _xml.readVector2(xmlCtx, subSec, 'start').tuple(),
                'step': _xml.readInt(xmlCtx, subSec, 'step') }
            subSec = _xml.getSubsection(xmlCtx, gridSection, 'vertical')
            xmlCtx = (None, '{0:>s}/vertical'.format(xPath))
            vertical = (_xml.readInt(xmlCtx, subSec, 'start'), _xml.readInt(xmlCtx, subSec, 'step'))
            subSec = _xml.getSubsection(xmlCtx, gridSection, 'horizontal')
            xmlCtx = (None, '{0:>s}/horizontal'.format(xPath))
            horizontal = (_xml.readInt(xmlCtx, subSec, 'start'), _xml.readInt(xmlCtx, subSec, 'step'))
            shared['grids'][gridName] = {
                'root': rootPos,
                'vertical': vertical,
                'horizontal': horizontal }
        
        if self._TechTreeDataProvider__availableNations is None:
            self._TechTreeDataProvider__availableNations = self._TechTreeDataProvider__readAvailableNations((None, TREE_SHARED_REL_FILE_PATH), section)
        
        precessed = _xml.getChildren(xmlCtx, section, 'lines')
        lines = shared['lines']
        for (name, sub) in precessed:
            xPath = '{0:>s}/{1:>s}'.format(TREE_SHARED_REL_FILE_PATH, name)
            xmlCtx = (None, xPath)
            pinsSec = _xml.getChildren(xmlCtx, sub, 'inPin')
            inPins = dict((lambda .0: for (pName, pSec) in .0:
(pName, pSec.asVector2.tuple()))(pinsSec))
            pinsSec = _xml.getChildren(xmlCtx, sub, 'outPin')
            outPins = dict((lambda .0: for (pName, pSec) in .0:
(pName, pSec.asVector2.tuple()))(pinsSec))
            pinsSec = _xml.getChildren(xmlCtx, sub, 'viaPin')
            viaPins = defaultdict((lambda : { }))
            for (outPin, setSec) in pinsSec:
                for (inPin, pSec) in setSec.items():
                    viaPins[outPin][inPin] = map((lambda section: section[1].asVector2.tuple()), pSec.items())
                
            
            defSec = sub['default']
            default = { }
            if defSec is not None:
                xmlCtx = (None, '{0:>s}/default'.format(xPath))
                default = {
                    'outPin': _xml.readString(xmlCtx, defSec, 'outPin'),
                    'inPin': _xml.readString(xmlCtx, defSec, 'inPin') }
            
            lines[name] = {
                'inPins': inPins,
                'outPins': outPins,
                'viaPins': viaPins,
                'default': default }
        
        defSec = _xml.getSubsection(xmlCtx, section, 'default-line')
        xPath = '{0:>s}/default-line'.format(TREE_SHARED_REL_FILE_PATH)
        xmlCtx = (None, xPath)
        name = _xml.readString(xmlCtx, defSec, 'line')
        outPin = _xml.readString(xmlCtx, defSec, 'outPin')
        inPin = _xml.readString(xmlCtx, defSec, 'inPin')
        self._TechTreeDataProvider__getLineInfo(xmlCtx, name, 0, outPin, inPin, lines)
        shared['default'] = {
            'line': name,
            'inPin': inPin,
            'outPin': outPin }
        return shared

    
    def _TechTreeDataProvider__getLineInfo(self, xmlCtx, lineName, nodeCD, outPin, inPin, lineShared):
        if lineName not in lineShared:
            raise _ConfigError(xmlCtx, 'Line {0:>s} not found'.format(lineName))
        lineName not in lineShared
        line = lineShared[lineName]
        if inPin not in line['inPins'].keys():
            raise _ConfigError(xmlCtx, 'Not found in pin = {0:>s} for line {1:>s}'.format(inPin, lineName))
        inPin not in line['inPins'].keys()
        if outPin not in line['outPins'].keys():
            raise _ConfigError(xmlCtx, 'Not found out pin = {0:>s} for line {1:>s} line'.format(outPin, lineName))
        outPin not in line['outPins'].keys()
        viaPins = []
        if outPin in line['viaPins'].keys():
            viaPins = line['viaPins'][outPin].get(inPin, [])
        
        return (line['outPins'][outPin], {
            'childID': nodeCD,
            'inPin': line['inPins'][inPin],
            'viaPins': line['viaPins'].get(outPin, { }).get(inPin, []) })

    
    def _TechTreeDataProvider__readAvailableNations(self, xmlCtx, root):
        names = []
        indices = nations.INDICES
        for (_, section) in _xml.getChildren(xmlCtx, root, 'available-nations'):
            name = section.asString
            if name not in indices:
                _xml.raiseWrongXml(xmlCtx, 'available-nations', 'Nation {0:>s} not found'.format(name))
            
            if name not in nations.AVAILABLE_NAMES:
                LOG_ERROR('Nation ignored, it not found in nations.AVAILABLE_NAMES', name)
                continue
            
            names.append(name)
        
        names = sorted(names, cmp = (lambda item, other: cmp(GUI_NATIONS_ORDER_INDEX.get(item), GUI_NATIONS_ORDER_INDEX.get(other))))
        return names

    
    def _TechTreeDataProvider__readNodeLines(self, parentCD, nation, xmlCtx, section, shared):
        linesSec = section['lines']
        if linesSec is None:
            linesSec = { }
        
        result = defaultdict((lambda : {
'outPin': None,
'inPins': [] }))
        next = self._TechTreeDataProvider__nextLevels[parentCD].keys()
        (_, xPath) = xmlCtx
        xPath = '{0:>s}/lines'.format(xPath)
        getIDsByName = vehicles.g_list.getIDsByName
        makeIntCDByID = vehicles.makeIntCompactDescrByID
        for (name, sub) in linesSec.items():
            xmlCtx = (None, '{0:>s}/lines/{1:>1}'.format(xPath, name))
            uName = '{0:>s}:{1:>s}'.format(nation, name)
            
            try:
                nodeCD = makeIntCDByID(_VEHICLE_TYPE_NAME, *getIDsByName(uName))
            except Exception:
                raise _ConfigError(xmlCtx, 'Unknown vehicle type name {0:>s}'.format(uName))

            if IS_DEVELOPMENT:
                if nodeCD not in next:
                    (_, nationID, vTypeID) = vehicles.parseIntCompactDescr(parentCD)
                    pName = vehicles.g_list.getList(nationID)[vTypeID]['name']
                    LOG_ERROR('{0:>s} does not have relation with {1:>s}'.format(pName, uName))
                else:
                    next.remove(nodeCD)
            
            data = shared['default'].copy()
            tags = sub.keys()
            lineShared = shared['lines']
            line = data['line']
            if 'line' in tags:
                line = sub.readString('line')
                if line in lineShared:
                    data.update(lineShared[line]['default'])
                
            
            outPin = data['outPin']
            if 'outPin' in tags:
                outPin = sub.readString('outPin')
            
            inPin = data['inPin']
            if 'inPin' in tags:
                inPin = sub.readString('inPin')
            
            (outPos, lineInfo) = self._TechTreeDataProvider__getLineInfo(xmlCtx, line, nodeCD, outPin, inPin, lineShared)
            result[outPin]['outPin'] = outPos
            result[outPin]['inPins'].append(lineInfo)
        
        if IS_DEVELOPMENT and len(next):
            (_, nationID, vTypeID) = vehicles.parseIntCompactDescr(parentCD)
            pName = vehicles.g_list.getList(nationID)[vTypeID]['name']
            for itemCD in next:
                (_, nationID, vTypeID) = vehicles.parseIntCompactDescr(itemCD)
                uName = vehicles.g_list.getList(nationID)[vTypeID]['name']
                LOG_ERROR('Relation between {0:>s} and {1:>s} are not defined'.format(pName, uName))
            
        
        return result

    
    def _TechTreeDataProvider__readNation(self, shared, nation, clearCache = False):
        xmlPath = NATION_TREE_REL_FILE_PATH % nation
        if clearCache:
            ResMgr.purge(xmlPath)
        
        section = ResMgr.openSection(xmlPath)
        if section is None:
            LOG_ERROR('can not open or read nation tree: ', nation, xmlPath)
            return { }
        xmlCtx = (None, xmlPath)
        precessed = _xml.getSubsection(xmlCtx, section, 'grid')
        gridName = precessed.asString
        if gridName not in shared['grids']:
            LOG_ERROR('not found grid (<grid> tag): ', gridName, xmlPath)
            return { }
        xPath = '{0:>s}/grid'.format(xmlPath)
        xmlCtx = (None, xPath)
        grid = shared['grids'][gridName]
        rows = _xml.readInt(xmlCtx, precessed, 'rows')
        columns = _xml.readInt(xmlCtx, precessed, 'columns')
        nationIndex = self._TechTreeDataProvider__availableNations.index(nation)
        coords = self._TechTreeDataProvider__makeCoordinates(grid, nationIndex, rows, columns)
        getIDsByName = vehicles.g_list.getIDsByName
        makeIntCDByID = vehicles.makeIntCompactDescrByID
        getVehicle = vehicles.g_cache.vehicle
        precessed = _xml.getChildren(xmlCtx, section, 'nodes')
        names = []
        displayInfo = { }
        for (name, nodeSection) in precessed:
            xPath = '{0:>s}/nodes/{1:>s}'.format(xmlPath, name)
            xmlCtx = (None, xPath)
            uName = '{0:>s}:{1:>s}'.format(nation, name)
            
            try:
                (nationID, vTypeID) = getIDsByName(uName)
            except Exception:
                gridName not in shared['grids']
                section is None
                raise _ConfigError(xmlCtx, 'Unknown vehicle type name {0:>s}'.format(uName))
            except:
                gridName not in shared['grids']

            nodeCD = makeIntCDByID(_VEHICLE_TYPE_NAME, nationID, vTypeID)
            vType = getVehicle(nationID, vTypeID)
            next = filter((lambda data: getTypeOfCompactDescr(data[1][1]) == _VEHICLE), enumerate(vType.unlocksDescrs))
            for (idx, data) in next:
                xpCost = data[0]
                nextCD = data[1]
                required = data[2:]
                self._TechTreeDataProvider__nextLevels[nodeCD][nextCD] = (idx, xpCost, set(required))
                self._TechTreeDataProvider__topLevels[nextCD].add(nodeCD)
                for itemCD in required:
                    self._TechTreeDataProvider__topItems[itemCD].add(nodeCD)
                
            
            row = _xml.readInt(xmlCtx, nodeSection, 'row')
            column = _xml.readInt(xmlCtx, nodeSection, 'column')
            if row > 1 and column is 1:
                raise _ConfigError(xmlCtx, 'In first column must be one node - root node, {0:>s} '.format(uName))
            column is 1
            if row > rows or column > columns:
                raise _ConfigError, (xmlCtx, 'Invalid row or column index: {0:>s}, {1:d}, {2:d}'.format(uName, row, column))
            column > columns
            lines = self._TechTreeDataProvider__readNodeLines(nodeCD, nation, xmlCtx, nodeSection, shared)
            displayInfo[nodeCD] = {
                'row': row,
                'column': column,
                'position': coords[column - 1][row - 1],
                'lines': lines }
        
        return displayInfo

    
    def _TechTreeDataProvider__makeAbsoluteCoordinates(self):
        iterator = self._TechTreeDataProvider__displayInfo.iteritems()
        for (_, info) in iterator:
            lines = info['lines']
            nodePos = info['position']
            for (outPin, lineInfo) in lines.iteritems():
                pinPos = lineInfo['outPin']
                lineInfo['outPin'] = (pinPos[0] + nodePos[0], pinPos[1] + nodePos[1])
                inPins = lineInfo['inPins']
                for pin in inPins:
                    if pin['childID'] not in self._TechTreeDataProvider__displayInfo:
                        continue
                    
                    childInfo = self._TechTreeDataProvider__displayInfo[pin['childID']]
                    childPos = childInfo['position']
                    pinPos = pin['inPin']
                    pin['inPin'] = (pinPos[0] + childPos[0], pinPos[1] + childPos[1])
                    pin['viaPins'] = (map,)((lambda item: (item[0] + nodePos[0], item[1] + nodePos[1])), pin['viaPins'])
                
            
        

    
    def _TechTreeDataProvider__makeCoordinates(self, grid, nationIndex, rows, columns):
        start = grid['root']['start']
        step = grid['root']['step']
        coordinates = [
            [
                [
                    start[0],
                    start[1] + step * nationIndex]]]
        (start, step) = grid['horizontal']
        hRange = xrange(start, start + step * columns, step)
        (start, step) = grid['vertical']
        vRange = xrange(start, start + step * rows, step)
        for x in hRange:
            continue
            _[1]([ (x, y) for y in vRange ])
        
        return coordinates

    
    def load(self, reload = False):
        if self._TechTreeDataProvider__loaded and not reload:
            return None
        self._clear()
        
        try:
            shared = self._TechTreeDataProvider__readShared(clearCache = reload)
            for nation in self._TechTreeDataProvider__availableNations:
                info = self._TechTreeDataProvider__readNation(shared, nation, clearCache = reload)
                self._TechTreeDataProvider__displayInfo.update(info)
        except _ConfigError:
            not reload
            error = None
            LOG_ERROR(error)
        except:
            not reload
        finally:
            self._TechTreeDataProvider__makeAbsoluteCoordinates()
            self._TechTreeDataProvider__loaded = True


    
    def getDisplayInfo(self, vTypeCD):
        result = None
        if vTypeCD in self._TechTreeDataProvider__displayInfo:
            result = self._TechTreeDataProvider__displayInfo[vTypeCD]
        
        return result

    
    def getTopLevel(self, vTypeCD):
        return self._TechTreeDataProvider__topLevels[vTypeCD]

    
    def getNextLevel(self, vTypeCD):
        return self._TechTreeDataProvider__nextLevels[vTypeCD].keys()

    
    def _findNext2Unlock(self, compare, xps = None, freeXP = 0):
        if xps is not None:
            filtered = (None, filter)((lambda item: item.xpCost <= xps.get(item.parentID, 0) + freeXP), compare)
            if len(filtered):
                compare = filtered
            
        
        return min(compare, key = (lambda item: item.xpCost))

    
    def isNext2Unlock(self, vTypeCD, unlocked = set(), xps = None, freeXP = 0):
        topLevel = self.getTopLevel(vTypeCD)
        available = False
        topIDs = set()
        compare = []
        result = makeDefUnlockProps()
        for parentCD in topLevel:
            nextLevel = self._TechTreeDataProvider__nextLevels[parentCD]
            (idx, xpCost, required) = nextLevel[vTypeCD]
            if required.issubset(unlocked) and parentCD in unlocked:
                topIDs.add(parentCD)
                compare.append(UnlockProps(parentCD, idx, xpCost, topIDs))
                available = True
                continue
            if not (result.xpCost) or result.xpCost > xpCost:
                result = UnlockProps(parentCD, idx, xpCost, set())
                continue
        
        if available:
            result = self._findNext2Unlock(compare, xps = xps, freeXP = freeXP)
        
        return (available, result)

    
    def getNext2UnlockByItems(self, itemCDs, unlocked = set(), xps = None, freeXP = 0):
        filtered = (filter,)((lambda item: item in self._TechTreeDataProvider__topItems), itemCDs)
        if not len(filtered) or not len(unlocked):
            return { }
        available = defaultdict((lambda : []))
        parentCDs = set()
        for item in filtered:
            if item in unlocked:
                parentCDs |= self._TechTreeDataProvider__topItems[item]
                continue
            not len(unlocked)
        
        for parentCD in parentCDs:
            if parentCD not in unlocked:
                continue
            
            nextLevel = self._TechTreeDataProvider__nextLevels[parentCD]
            topIDs = set()
            for (idx, xpCost, required) in nextLevel.iteritems():
                if childCD not in unlocked and required.issubset(unlocked):
                    topIDs.add(parentCD)
                    available[childCD].append(UnlockProps(parentCD, idx, xpCost, topIDs))
                    continue
            
        
        result = { }
        for (childCD, compare) in available.iteritems():
            result[childCD] = self._findNext2Unlock(compare, xps = xps, freeXP = freeXP)
        
        return result

    
    def getAvailableNations(self):
        if self._TechTreeDataProvider__availableNations is None:
            section = ResMgr.openSection(TREE_SHARED_REL_FILE_PATH)
            if section is None:
                _xml.raiseWrongXml(None, TREE_SHARED_REL_FILE_PATH, 'can not open or read')
            
            xmlCtx = (None, TREE_SHARED_REL_FILE_PATH)
            self._TechTreeDataProvider__availableNations = self._TechTreeDataProvider__readAvailableNations(xmlCtx, section)
        
        return self._TechTreeDataProvider__availableNations[:]


g_techTreeDP = _TechTreeDataProvider()

