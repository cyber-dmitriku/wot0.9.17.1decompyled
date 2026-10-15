# Source Generated with Decompyle++
# File: func_utils.pyc (Python 2.6)

import BigWorld
from functools import partial

def callback(delay, obj, methodName, *args):
    return BigWorld.callback(delay, partial(callMethod, obj, methodName, *args))


def callMethod(obj, methodName, *args):
    if hasattr(obj, methodName):
        getattr(obj, methodName)(*args)
    


