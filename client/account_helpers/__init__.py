# Source Generated with Decompyle++
# File: __init__.pyc (Python 2.6)

import BigWorld
import constants
import datetime

def isPremiumAccount(attrs):
    if attrs is not None:
        pass
    return attrs & constants.ACCOUNT_ATTR.PREMIUM != 0


def getPremiumExpiryDelta(expiryTime):
    check = datetime.datetime.utcfromtimestamp(expiryTime)
    now = datetime.datetime.utcnow()
    return check - now


def isDemonstrator(attrs):
    if attrs is not None:
        pass
    return attrs & constants.ACCOUNT_ATTR.ARENA_CHANGE != 0


def convertGold(gold):
    return gold


