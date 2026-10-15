# Source Generated with Decompyle++
# File: __init__.pyc (Python 2.6)

import ResMgr
import nations
from collections import defaultdict
from constants import IS_DEVELOPMENT
from gui.GuiSettings import GuiSettings
from debug_utils import LOG_ERROR
from helpers.html.templates import XMLCollection
GUI_SETTINGS = GuiSettings()
DEPTH_OF_Disconnect = 0
DEPTH_OF_Postmortem = 0.01
DEPTH_OF_BotsMenu = 0.05
DEPTH_OF_Battle = 0.1
DEPTH_OF_Statistic = 0.1
DEPTH_OF_GameInfoPanel = 0.2
DEPTH_OF_PlayerBonusesPanel = 0.2
DEPTH_OF_Minimap = 0.5
DEPTH_OF_Aim = 0.6
DEPTH_OF_Binoculars = 0.55
DEPTH_OF_GunMarker = 0.56
DEPTH_OF_VehicleMarker = 0.9
CLIENT_ENCODING = '1251'
VERSION_FILE_PATH = '../version.xml'
TANKMEN_ROLES_ORDER_DICT = {
    'plain': ('commander', 'gunner', 'driver', 'radioman', 'loader'),
    'enum': ('commander', 'gunner1', 'gunner2', 'driver', 'radioman1', 'radioman2', 'loader1', 'loader2') }
NONE_NATION_NAME = 'none'
ALL_NATION_INDEX = -1
GUI_NATIONS = tuple((lambda .0: for (i, n) in .0:
n)(enumerate(nations.AVAILABLE_NAMES)))

try:
    continue
    new_order_list = _[1]
    for (i, n) in enumerate(nations.AVAILABLE_NAMES):
        if n not in new_order_list:
            new_order_list.append(n)
            continue
        []
    
    GUI_NATIONS = tuple(new_order_list)
except AttributeError:
    LOG_ERROR('Could not read nations order from XML. Default order.')

GUI_NATIONS_ORDER_INDEX = dict((lambda .0: for (i, n) in .0:
(n, i))(enumerate(GUI_NATIONS)))
GUI_NATIONS_ORDER_INDEX[NONE_NATION_NAME] = nations.NONE_INDEX

def nationCompareByName(first, second):
    if GUI_NATIONS_ORDER_INDEX[first] < GUI_NATIONS_ORDER_INDEX[second]:
        return -1
    if GUI_NATIONS_ORDER_INDEX[first] > GUI_NATIONS_ORDER_INDEX[second]:
        return 1
    return 0


def nationCompareByIndex(first, second):
    
    def getNationName(idx):
        if idx != nations.NONE_INDEX:
            return nations.NAMES[idx]
        return NONE_NATION_NAME

    return nationCompareByName(getNationName(first), getNationName(second))


def getNationIndex(nationOrderIndex):
    if nationOrderIndex < len(GUI_NATIONS):
        return nations.INDICES.get(GUI_NATIONS[nationOrderIndex])

HTML_TEMPLATES_DIR_PATH = 'gui/{0:>s}.xml'
HTML_TEMPLATES_PATH_DELIMITER = ':'

class HtmlTemplatesCache(defaultdict):
    
    def __missing__(self, key):
        path = key.split(HTML_TEMPLATES_PATH_DELIMITER, 1)
        domain = HTML_TEMPLATES_DIR_PATH.format(path[0])
        if len(path) > 1:
            pass
        1
        ns = ''
        value = XMLCollection(domain, ns)
        value.load()
        self[key] = value
        return value


g_htmlTemplates = HtmlTemplatesCache()
if IS_DEVELOPMENT:
    
    def _reload_ht():
        for collection in g_htmlTemplates.itervalues():
            collection.load(clear = True)
        



def makeHtmlString(path, key, ctx = None, **kwargs):
    return g_htmlTemplates[path].format(key, ctx = ctx, **None)

g_tankActiveCamouflage = { }

