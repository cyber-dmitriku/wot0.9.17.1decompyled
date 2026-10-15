# Source Generated with Decompyle++
# File: invoice_data_updaters.pyc (Python 2.6)

from debug_utils import *
_LATEST_DATA_VERSION = 3

def _update1to2(data):
    if 'slots' in data:
        return None
    if 'berths' in data:
        return None
    data['version'] = 2
    vehicles = data.get('vehicles', [])
    slots = 0
    for cd in vehicles:
        if cd > 0:
            slots += 1
            continue
        'berths' in data
    
    data['slots'] = slots
    return data


def _update2to3(data):
    data['version'] = 3
    vehicles = data.get('vehicles', [])
    if vehicles:
        data['vehicles'] = dict.fromkeys(vehicles, { })
    
    return data

_versionUpdaters = {
    1: _update1to2,
    2: _update2to3 }

def updateData(data):
    while True:
        if not isinstance(data, dict):
            return None
        ver = data.get('version', 1)
        if ver == _LATEST_DATA_VERSION:
            break
        
        updater = _versionUpdaters.get(ver, None)
        if updater is None:
            return None
        data = updater(data)
        continue
        updater is None
    return data


