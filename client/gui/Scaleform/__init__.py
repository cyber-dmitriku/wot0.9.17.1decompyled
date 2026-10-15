# Source Generated with Decompyle++
# File: __init__.pyc (Python 2.6)

from types import InstanceType
SCALEFORM_SUPPORT = False

try:
    import _Scaleform
    SCALEFORM_SUPPORT = True
except ImportError:
    raise NotImplementedError, 'Client not support Scaleform'

SCALEFORM_SWF_PATH = 'gui/flash'
SCALEFORM_STARTUP_VIDEO_PATH = 'gui/flash/video'
SCALEFORM_STARTUP_VIDEO_MASK = 'video/%s'
SCALEFORM_WALLPAPER_PATH = 'gui/maps/login'
SCALEFORM_FONT_LIB_PATH = 'gui/flash'
SCALEFORM_FONT_CONFIG_FILE = 'fontconfig.xml'
SCALEFORM_FONT_CONFIG_PATH = 'gui/flash/%s' % SCALEFORM_FONT_CONFIG_FILE
SCALEFORM_DEFAULT_CONFIG_NAME = 'All'

class VehicleActions(object):
    '''
\tRepresent vehicleActionMarker convertion action to bitMask
\t'''
    _VehicleActions__ACTIONS = {
        'hunting': 1 }
    
    def getBitMask(actions):
        bitMask = 0
        for (key, value) in actions.items():
            mask = VehicleActions._VehicleActions__ACTIONS.get(key, 0)
            if isinstance(mask, dict):
                mask = mask.get(value, 0)
            
            bitMask |= mask
        
        return bitMask

    getBitMask = staticmethod(getBitMask)
    
    def isHunting(actions):
        return 'hunting' in actions.keys()

    isHunting = staticmethod(isHunting)


