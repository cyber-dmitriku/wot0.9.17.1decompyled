# Source Generated with Decompyle++
# File: gameVars.pyc (Python 2.6)

from CurrentVehicle import g_currentVehicle
from adisp import process
from gui.Scaleform.utils.gui_items import InventoryItem
from items import vehicles, ITEM_TYPE_NAMES
from tutorial.data.chapter import VehicleCondition
from tutorial.logger import LOG_CURRENT_EXCEPTION

def _getCvTypeName():
    result = None
    if g_currentVehicle.isPresent():
        result = g_currentVehicle.vehicle.descriptor.type.name
    
    return result

_vehicleVarGetters = {
    VehicleCondition.CV_TYPE_NAME: _getCvTypeName }

def vehicle(varID):
    getters = _vehicleVarGetters.get(varID)
    result = None
    if getters is not None:
        result = getters()
    
    return result


def addVehicleItemParams(itemCompactDecr, data):
    (itemTypeID, nationID, compTypeID) = vehicles.parseIntCompactDescr(itemCompactDecr)
    if not itemTypeID != ITEM_TYPE_NAMES[1]:
        raise AssertionError
    
    try:
        guiItem = InventoryItem(itemTypeName = ITEM_TYPE_NAMES[itemTypeID], compactDescr = itemCompactDecr)
        data.append(guiItem.itemTypeName)
        data.append(guiItem.level)
        params = guiItem.getParams(g_currentVehicle.vehicle)
        for param in params['parameters']:
            data.extend(param)
    except Exception:
        itemTypeID != ITEM_TYPE_NAMES[1]
        LOG_CURRENT_EXCEPTION()
    except:
        itemTypeID != ITEM_TYPE_NAMES[1]



def addTankmanSkillParams(skillName, data):
    data.append('../maps/icons/tankmen/skills/big/{0:>s}.png'.format(skillName))


