# Source Generated with Decompyle++
# File: dumpers.pyc (Python 2.6)

import gui
from helpers import i18n, html
from items import getTypeInfoByName, vehicles
from gui.Scaleform.techtree import _PREMIUM_TAGS, _VEHICLE_TYPE_NAME, NODE_STATE
__all__ = [
    '_BaseDumper',
    'ResearchItemsObjDumper',
    'ResearchItemsXMLDumper',
    'NationObjDumper',
    'NationXMLDumper']

class _BaseDumper(object):
    
    def dump(self, data):
        return { }



class ResearchItemsObjDumper(_BaseDumper):
    
    def dump(self, data):
        itemGetter = data.getItem
        nodesData = (None, map)((lambda node: self._getItemData(node, itemGetter(node['id']))), data._nodes)
        topLevelData = (None, map)((lambda node: self._getItemData(node, itemGetter(node['id']))), data._topLevel)
        return {
            'nodes': nodesData,
            'top': topLevelData,
            'global': self._getGlobalData(data) }

    
    def _getGlobalData(self, data):
        return {
            'enableInstallItems': data.isEnableInstallItems(),
            'statusString': data.getRootStatusString(),
            'extraInfo': self._getExtraInfo(data) }

    
    def _getExtraInfo(self, data):
        item = data.getItem(data.getRootCD())
        result = { }
        if item.isPremium:
            type = i18n.makeString('#tooltips:tankCaruselTooltip/vehicleType/elite/{0:>s}'.format(item.type))
            result = {
                'type': item.type,
                'title': gui.makeHtmlString('html_templates:lobby/research', 'premium_title', ctx = {
                    'name': item.name,
                    'type': type,
                    'level': i18n.makeString('#tooltips:level/{0:d}'.format(item.level)) }),
                'content': gui.makeHtmlString('html_templates:lobby/research', 'premium_content', ctx = {
                    'description': item.description }) }
        
        return result

    
    def _getItemData(self, node, item):
        nodeCD = node['id']
        vClass = {
            'userString': '',
            'name': '' }
        iconPath = ''
        isVehicle = item.itemTypeName == _VEHICLE_TYPE_NAME
        if isVehicle:
            tags = item.tags
            vClassSet = vehicles.VEHICLE_CLASS_TAGS & tags
            if len(vClassSet):
                info = getTypeInfoByName(item.itemTypeName)['tags'][set(vClassSet).pop()]
                vClass = info.copy()
            
            if len(tags & _PREMIUM_TAGS):
                node['state'] |= NODE_STATE.PREMIUM
            
            if node['displayInfo']['renderer'] == 'root':
                iconPath = item.icon
                node['nation'] = item.nationName
            else:
                iconPath = item.smallIcon
        else:
            vClass.update({
                'name': item.itemTypeName,
                'userString': item.userType })
        data = {
            'nameString': item.shortName,
            'primaryClass': vClass,
            'level': item.level,
            'longName': item.longName,
            'iconPath': iconPath,
            'pickleDump': item.pack() }
        data.update(node)
        props = data['unlockProps']
        data['unlockProps'] = props._replace(required = list(props.required))
        return data



class ResearchItemsXMLDumper(ResearchItemsObjDumper):
    _ResearchItemsXMLDumper__xmlBody = '<?xml version="1.0" encoding="utf-8"?><graph><top>{0:>s}</top><nodes>{1:>s}</nodes><global><enableInstallItems>{2[enableInstallItems]:b}</enableInstallItems><statusString>{2[statusString]:>s}</statusString><extraInfo><type>{2[extraInfo][type]:>s}</type><title><![CDATA[{2[extraInfo][title]:>s}]]></title><content><![CDATA[{2[extraInfo][content]:>s}]]></content></extraInfo></global></graph>'
    _ResearchItemsXMLDumper__nodeFormat = '<node><id>{id:d}</id><nameString>{nameString:>s}</nameString><class><name>{primaryClass[name]:>s}</name><userString>{primaryClass[userString]:>s}</userString></class><level>{level:d}</level><earnedXP>{earnedXP:d}</earnedXP><state>{state:d}</state><unlockProps><parentID>{unlockProps[0]:d}</parentID><unlockIdx>{unlockProps[1]:d}</unlockIdx><xpCost>{unlockProps[2]:n}</xpCost><required>{unlockProps[3]:>s}</required></unlockProps><iconPath><![CDATA[{iconPath:>s}]]></iconPath><longName>{longName:>s}</longName><dump><![CDATA[{pickleDump:>s}]]></dump><shopPrice><credits>{shopPrice[0]:n}</credits><gold>{shopPrice[1]:n}</gold></shopPrice><display><renderer>{displayInfo[renderer]:>s}</renderer><path>{displayInfo[path]:>s}</path><level>{displayInfo[level]:d}</level></display></node>'
    _ResearchItemsXMLDumper__idFormat = '<id>{0:d}</id>'
    
    def dump(self, data):
        return self._ResearchItemsXMLDumper__xmlBody.format(self._ResearchItemsXMLDumper__buildNodesData(data, '_topLevel'), self._ResearchItemsXMLDumper__buildNodesData(data, '_nodes'), self._getGlobalData(data))

    
    def _getExtraInfo(self, data):
        result = super(ResearchItemsXMLDumper, self)._getExtraInfo(data)
        return {
            'type': result.get('type', ''),
            'title': html.escape(result.get('title', '')),
            'content': html.escape(result.get('content', '')) }

    
    def _ResearchItemsXMLDumper__buildNodesData(self, data, storage):
        nodesDump = []
        itemGetter = data.getItem
        nodes = getattr(data, storage, [])
        for node in nodes:
            data = self._getItemData(node, itemGetter(node['id']))
            data['unlockProps'] = self._ResearchItemsXMLDumper__buildUnlockProps(data['unlockProps'])
            data['displayInfo'] = self._ResearchItemsXMLDumper__buildDisplayInfo(data['displayInfo'])
            nodesDump.append(self._ResearchItemsXMLDumper__nodeFormat.format(**None))
        
        return ''.join(nodesDump)

    
    def _ResearchItemsXMLDumper__buildUnlockProps(self, unlockProps):
        dump = (map,)((lambda item: self._ResearchItemsXMLDumper__idFormat.format(item)), unlockProps.required)
        return unlockProps._replace(required = ''.join(dump))

    
    def _ResearchItemsXMLDumper__buildDisplayInfo(self, displayInfo):
        info = displayInfo.copy()
        info['path'] = ''.join((map,)((lambda item: self._ResearchItemsXMLDumper__idFormat.format(item)), displayInfo['path']))
        return info



class NationObjDumper(_BaseDumper):
    
    def dump(self, data):
        nodes = data._nodes
        nodesData = []
        itemGetter = data.getItem
        nodesData = (None, map)((lambda node: self._getVehicleData(node, itemGetter(node['id']))), nodes)
        return {
            'nodes': nodesData,
            'scrollIndex': data._scrollIndex }

    
    def _getVehicleData(self, node, item):
        nodeCD = node['id']
        tags = item.tags
        vClassSet = vehicles.VEHICLE_CLASS_TAGS & tags
        vClass = {
            'userString': '',
            'name': '' }
        if len(vClassSet):
            info = getTypeInfoByName(item.itemTypeName)['tags'][set(vClassSet).pop()]
            vClass = info.copy()
        
        if len(tags & _PREMIUM_TAGS):
            node['state'] |= NODE_STATE.PREMIUM
        
        data = {
            'type': item.itemTypeName,
            'nameString': item.shortName,
            'primaryClass': vClass,
            'level': item.level,
            'longName': item.longName,
            'iconPath': item.smallIcon,
            'pickleDump': item.pack() }
        data.update(node)
        props = data['unlockProps']
        data['unlockProps'] = props._replace(required = list(props.required))
        return data



class NationXMLDumper(NationObjDumper):
    _NationXMLDumper__xmlBody = '<?xml version="1.0" encoding="utf-8"?><tree><nodes>{0:>s}</nodes><scrollIndex>{1:d}</scrollIndex></tree>'
    _NationXMLDumper__nodeFormat = '<node><id>{id:d}</id><nameString>{nameString:>s}</nameString><class><name>{primaryClass[name]:>s}</name><userString>{primaryClass[userString]:>s}</userString></class><level>{level:d}</level><earnedXP>{earnedXP:d}</earnedXP><state>{state:d}</state><unlockProps><parentID>{unlockProps[0]:d}</parentID><unlockIdx>{unlockProps[1]:d}</unlockIdx><xpCost>{unlockProps[2]:n}</xpCost><topIDs>{unlockProps[3]:>s}</topIDs></unlockProps><iconPath>{iconPath:>s}</iconPath><longName>{longName:>s}</longName><dump><![CDATA[{pickleDump:>s}]]></dump><shopPrice><credits>{shopPrice[0]:n}</credits><gold>{shopPrice[1]:n}</gold></shopPrice><display>{displayInfo:>s}</display></node>'
    _NationXMLDumper__displayInfoFormat = '<row>{row:d}</row><column>{column:d}</column><position><x>{position[0]:n}</x><y>{position[1]:n}</y></position><lines>{lines:>s}</lines>'
    _NationXMLDumper__setFormat = '<set><outLiteral>{0:>s}</outLiteral><outPin><x>{1[0]:n}</x><y>{1[1]:n}</y></outPin><inPins>{2:>s}</inPins></set>'
    _NationXMLDumper__inPinFormat = '<item><childID>{childID:d}</childID><inPin><x>{inPin[0]:n}</x><y>{inPin[1]:n}</y></inPin><viaPins>{dump:>s}</viaPins></item>'
    _NationXMLDumper__viaPinFormat = '<pin><x>{0[0]:n}</x><y>{0[1]:n}</y></pin>'
    _NationXMLDumper__topIDFormat = '<id>{0:d}</id>'
    
    def dump(self, data):
        return self._NationXMLDumper__xmlBody.format(self._NationXMLDumper__buildNodesData(data), data._scrollIndex)

    
    def _NationXMLDumper__buildNodesData(self, data):
        nodesDump = []
        itemGetter = data.getItem
        for node in data._nodes:
            data = self._getVehicleData(node, itemGetter(node['id']))
            data.update(node)
            data['unlockProps'] = self._NationXMLDumper__buildUnlockProps(data['unlockProps'])
            data['displayInfo'] = self._NationXMLDumper__buildDisplayInfo(data['displayInfo'])
            nodesDump.append(self._NationXMLDumper__nodeFormat.format(**None))
        
        return ''.join(nodesDump)

    
    def _NationXMLDumper__buildUnlockProps(self, unlockProps):
        dump = (map,)((lambda item: self._NationXMLDumper__topIDFormat.format(item)), unlockProps.required)
        return unlockProps._replace(required = ''.join(dump))

    
    def _NationXMLDumper__buildDisplayInfo(self, displayInfo):
        info = displayInfo.copy()
        lines = info['lines']
        dump = []
        for (outPin, data) in lines.iteritems():
            inPins = []
            for inPin in data['inPins']:
                viaPins = (map,)((lambda item: self._NationXMLDumper__viaPinFormat.format(item)), inPin['viaPins'])
                inPins.append(self._NationXMLDumper__inPinFormat.format(dump = ''.join(viaPins), **None))
            
            dump.append(self._NationXMLDumper__setFormat.format(outPin, data['outPin'], ''.join(inPins)))
        
        info['lines'] = ''.join(dump)
        return self._NationXMLDumper__displayInfoFormat.format(**None)



