# Source Generated with Decompyle++
# File: logger.pyc (Python 2.6)

from constants import IS_DEVELOPMENT
from debug_utils import _doLog, LOG_CURRENT_EXCEPTION

class LOG_LEVEL:
    ERROR = 1
    WARNING = 2
    DEBUG = 4

CURRENT_LOG_LEVEL = LOG_LEVEL.ERROR
if IS_DEVELOPMENT:
    CURRENT_LOG_LEVEL |= LOG_LEVEL.WARNING


def LOG_DEBUG(msg, *args):
    if CURRENT_LOG_LEVEL & LOG_LEVEL.DEBUG:
        _doLog('TUTORIAL DEBUG', msg, args)
    


def LOG_WARNING(msg, *args):
    if CURRENT_LOG_LEVEL & LOG_LEVEL.WARNING:
        _doLog('TUTORIAL WARNING', msg, args)
    


def LOG_ERROR(msg, *args):
    if CURRENT_LOG_LEVEL & LOG_LEVEL.ERROR:
        _doLog('TUTORIAL ERROR', msg, args)
    

__all__ = ('LOG_DEBUG', 'LOG_WARNING', 'LOG_ERROR', 'LOG_CURRENT_EXCEPTION')

