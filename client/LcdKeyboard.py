# Source Generated with Decompyle++
# File: LcdKeyboard.pyc (Python 2.6)

import BigWorld
_g_instance = None

class LCD_KEY:
    LEFT = 256
    RIGHT = 512
    OK = 1024
    CANCEL = 2048
    UP = 4096
    DOWN = 8192
    MENU = 16384


def enableLcdKeyboardSpecificKeys(bValue):
    global _g_instance
    if bValue:
        if _g_instance is not None:
            return True
        _g_instance = BigWorld.WGLcdKeyboard()
        if not _g_instance.isValid():
            _g_instance.destroy()
            _g_instance = None
            return False
    elif _g_instance is None:
        return True
    _g_instance.destroy()
    _g_instance = None
    return True


def getKeys(mask = 0xFFFFFFFFL):
    if _g_instance is None:
        return 0
    return _g_instance.getKeys() & mask


def finalize():
    enableLcdKeyboardSpecificKeys(False)


