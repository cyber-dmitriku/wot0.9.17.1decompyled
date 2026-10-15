# Source Generated with Decompyle++
# File: __init__.pyc (Python 2.6)

import i18n
import constants
import ResMgr
from debug_utils import LOG_CURRENT_EXCEPTION
from gui import GUI_SETTINGS

def getClientLanguage():
    '''
\tReturn client string of language code
\t'''
    import ResMgr as ResMgr
    import constants as constants
    lng = constants.DEFAULT_LANGUAGE
    
    try:
        lng = i18n.makeString('#settings:LANGUAGE_CODE')
        if not lng.strip() and lng == '#settings:LANGUAGE_CODE' or lng == 'LANGUAGE_CODE':
            lng = constants.DEFAULT_LANGUAGE
    except Exception:
        LOG_CURRENT_EXCEPTION()

    return lng


def getLocalizedData(dataDict, key):
    resVal = { }
    if dataDict:
        lng = getClientLanguage()
        localesDict = dataDict.get(key, { })
        if localesDict:
            if lng in localesDict:
                resVal = localesDict[lng]
            elif constants.DEFAULT_LANGUAGE in localesDict:
                resVal = localesDict[constants.DEFAULT_LANGUAGE]
            else:
                resVal = localesDict.items()[0][1]
        
    
    return resVal


def int2roman(number):
    '''
\tConvert arabic number to roman number
\t@param number: int - number
\t@return: string - roman number
\t'''
    numerals = {
        1: 'I',
        4: 'IV',
        5: 'V',
        9: 'IX',
        10: 'X',
        40: 'XL',
        50: 'L',
        90: 'XC',
        100: 'C',
        400: 'CD',
        500: 'D',
        900: 'CM',
        1000: 'M' }
    result = ''
    for (value, numeral) in sorted(numerals.items(), reverse = True):
        while number >= value:
            result += numeral
            number -= value
    
    return result


def getClientVersion():
    sec = ResMgr.openSection('../version.xml')
    version = i18n.makeString(sec.readString('appname')) + ' ' + sec.readString('version')
    return version


