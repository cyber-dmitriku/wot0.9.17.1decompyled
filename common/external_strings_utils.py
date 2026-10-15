# Source Generated with Decompyle++
# File: external_strings_utils.pyc (Python 2.6)

import re
import unicodedata
from debug_utils import LOG_CURRENT_EXCEPTION
from constants import CREDENTIALS_RESTRICTION, CREDENTIALS_RESTRICTION_SET
if CREDENTIALS_RESTRICTION_SET == CREDENTIALS_RESTRICTION.BASIC:
    _ACCOUNT_NAME_RE = re.compile('^[a-zA-Z0-9_]+$')
    _ACCOUNT_NAME_MIN_LENGTH = 2
    _ACCOUNT_NAME_MAX_LENGTH = 24
    _ACCOUNT_NAME_MIN_LENGTH_REG = 3
    _LOGIN_NAME_RE = re.compile('^[a-z0-9_-]+(\\.[a-z0-9_-]+)*@[a-z0-9-]+(\\.[a-z0-9-]+)*\\.([a-z]{2,4})$')
    _LOGIN_NAME_MIN_LENGTH = 1
    _LOGIN_NAME_MAX_LENGTH = 255
    _PASSWORD_RE = re.compile('^[a-zA-Z0-9_]+$')
    _PASSWORD_MIN_LENGTH = 6
    _PASSWORD_MAX_LENGTH = 100
    _CLAN_ABBREV_RE = re.compile('^[A-Z0-9_\\-]+$')
    _CLAN_NAME_MAX_LENGTH = 70
    _CLAN_ABBREV_MAX_LENGTH = 5
    _UPPERCASE_CLAN_ABBREV = True
    _REQUIRE_NORMALIZED_CLAN_ABBREV = True
    CLAN_DESCR_MAX_LENGTH = 1000
    CLAN_MOTTO_MAX_LENGTH = 100
elif CREDENTIALS_RESTRICTION_SET == CREDENTIALS_RESTRICTION.CHINESE:
    _ACCOUNT_NAME_EXCLUDED_SYMBOLS = range(32) + [
        34,
        38,
        39,
        47,
        58,
        60,
        62,
        64,
        127]
    _ACCOUNT_NAME_RE = re.compile(u'(?u)^[^' + u''.join(map((lambda n: u'\\x%0.2x' % n), _ACCOUNT_NAME_EXCLUDED_SYMBOLS)) + unichr(65535) + unichr(65534) + u']+$')
    _ACCOUNT_NAME_MIN_LENGTH = 4
    _ACCOUNT_NAME_MAX_LENGTH = 14
    _ACCOUNT_NAME_MIN_LENGTH_REG = _ACCOUNT_NAME_MIN_LENGTH
    _LOGIN_NAME_RE = re.compile('^[_a-z0-9-+@.]+$')
    _LOGIN_NAME_MIN_LENGTH = 4
    _LOGIN_NAME_MAX_LENGTH = 30
    _PASSWORD_RE = re.compile('^[!-~]+$')
    _PASSWORD_MIN_LENGTH = 6
    _PASSWORD_MAX_LENGTH = 32
    _CLAN_ABBREV_RE = _ACCOUNT_NAME_RE
    _CLAN_NAME_MAX_LENGTH = 70
    _CLAN_ABBREV_MAX_LENGTH = 5
    _UPPERCASE_CLAN_ABBREV = False
    _REQUIRE_NORMALIZED_CLAN_ABBREV = False
    CLAN_DESCR_MAX_LENGTH = 1000
    CLAN_MOTTO_MAX_LENGTH = 100
elif CREDENTIALS_RESTRICTION_SET == CREDENTIALS_RESTRICTION.VIETNAM:
    _ACCOUNT_NAME_RE = re.compile('^[a-zA-Z0-9_]+$')
    _ACCOUNT_NAME_MIN_LENGTH = 2
    _ACCOUNT_NAME_MAX_LENGTH = 24
    _ACCOUNT_NAME_MIN_LENGTH_REG = 3
    _LOGIN_NAME_RE = re.compile('^[a-zA-Z0-9_][a-zA-Z0-9._]+$')
    _LOGIN_NAME_MIN_LENGTH = 3
    _LOGIN_NAME_MAX_LENGTH = 24
    _PASSWORD_RE = re.compile('^[a-zA-Z0-9+!@#$%^&*()?.,_=";:><{}\\[\\]\']+$')
    _PASSWORD_MIN_LENGTH = 4
    _PASSWORD_MAX_LENGTH = 32
    _CLAN_ABBREV_RE = re.compile('^[A-Z0-9_\\-]+$')
    _CLAN_NAME_MAX_LENGTH = 70
    _CLAN_ABBREV_MAX_LENGTH = 5
    _UPPERCASE_CLAN_ABBREV = True
    _REQUIRE_NORMALIZED_CLAN_ABBREV = True
    CLAN_DESCR_MAX_LENGTH = 1000
    CLAN_MOTTO_MAX_LENGTH = 100
elif not False:
    raise AssertionError, 'Unknown credential restrictions set'
CLAN_DESCR_MAX_BYTES = CLAN_DESCR_MAX_LENGTH * 4
CLAN_MOTTO_MAX_BYTES = CLAN_MOTTO_MAX_LENGTH * 4

def unicode_from_utf8(utf8str):
    unicodeStr = unicode(utf8str, 'utf8')
    return (unicodedata.normalize('NFKC', unicodeStr), unicodeStr)


def utf8_accepted(utf8str, re, minLen, maxLen, checkBeforeNFKC = True):
    (nfkc, plain) = unicode_from_utf8(utf8str)
    
    matchFn = lambda uniStr: if re.match(uniStr):
if minLen <= len(uniStr):
len(uniStr) <= maxLenminLen <= len(uniStr)len(uniStr)
    if checkBeforeNFKC and not matchFn(plain):
        return False
    return matchFn(nfkc)


def normalized_unicode_trim(utf8str, length):
    
    try:
        (unicodeStr, _) = unicode_from_utf8(utf8str)
        if len(unicodeStr) > max(0, length):
            unicodeStr = unicodeStr[:length]
        
        return unicodeStr.encode('utf8')
    except:
        LOG_CURRENT_EXCEPTION()
        return None



def normalized_unicode_trim_and_lowercase(utf8str, length):
    
    try:
        (unicodeStr, _) = unicode_from_utf8(utf8str)
        if len(unicodeStr) > max(0, length):
            unicodeStr = unicodeStr[:length]
        
        return unicodeStr.lower().encode('utf8')
    except:
        LOG_CURRENT_EXCEPTION()
        return None



def isAccountNameValid(text, minLength = _ACCOUNT_NAME_MIN_LENGTH):
    return utf8_accepted(text, _ACCOUNT_NAME_RE, minLength, _ACCOUNT_NAME_MAX_LENGTH)


def normalizedAccountName(text):
    return normalized_unicode_trim_and_lowercase(text, _ACCOUNT_NAME_MAX_LENGTH)


def isPasswordValid(text):
    return utf8_accepted(text, _PASSWORD_RE, _PASSWORD_MIN_LENGTH, _PASSWORD_MAX_LENGTH)


def isAccountLoginValid(text):
    return utf8_accepted(text, _LOGIN_NAME_RE, _LOGIN_NAME_MIN_LENGTH, _LOGIN_NAME_MAX_LENGTH)


def normalizedAccountLogin(text):
    
    try:
        text = normalize_utf8(text)
        if len(text) > _LOGIN_NAME_MAX_LENGTH:
            text = text[:_LOGIN_NAME_MAX_LENGTH]
        
        return text.lower()
    except:
        LOG_CURRENT_EXCEPTION()
        return None



def isClanNameValid(text):
    
    try:
        utext = unicode(text, 'utf8').strip()
        if utext.encode('utf8') != text:
            return False
        if 2 <= len(utext):
            pass
        len(utext) <= _CLAN_NAME_MAX_LENGTH
        if not 1:
            return False
        for word in utext.split(' '):
            if not word or any(map((lambda c: ord(c) < 32), word)):
                return False
        
        return True
    except:
        LOG_CURRENT_EXCEPTION()
        return False



def normalizedClanName(text):
    
    try:
        (utext, _) = unicode_from_utf8(text)
        if len(utext) > _CLAN_NAME_MAX_LENGTH:
            utext = utext[:_CLAN_NAME_MAX_LENGTH]
        
        return utext.lower().encode('utf8')
    except:
        LOG_CURRENT_EXCEPTION()
        return None



def isClanAbbrevValid(abbrev):
    if not utf8_accepted(abbrev, _CLAN_ABBREV_RE, 2, _CLAN_ABBREV_MAX_LENGTH) and not _REQUIRE_NORMALIZED_CLAN_ABBREV:
        pass
    return abbrev == normalizedClanAbbrev(abbrev)


def normalizedClanAbbrev(abbrev):
    
    try:
        (abbrev, _) = unicode_from_utf8(abbrev)
        if len(abbrev) > _CLAN_ABBREV_MAX_LENGTH:
            abbrev = abbrev[:_CLAN_ABBREV_MAX_LENGTH]
        
        if _UPPERCASE_CLAN_ABBREV:
            abbrev = abbrev.upper()
        
        return abbrev.encode('utf8')
    except:
        LOG_CURRENT_EXCEPTION()
        return None



def isChannelNameValid(channelName):
    test = channelName.strip()
    if test:
        pass
    return test[0] not in '[<{('


def escapeSQL(text, default = '\\0'):
    if text is None:
        return default
    return text.replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"').replace('\x0', '\\0')


def normalize_utf8(utf8str):
    return unicode(utf8str, 'utf8').encode('utf8')


def truncate_utf8(utf8str, maxbytes):
    if len(utf8str) < maxbytes:
        return utf8str
    if maxbytes <= 0:
        return ''
    if _is_utf8_one_byte(utf8str[maxbytes - 1]):
        return utf8str[:maxbytes]
    for x in xrange(1, 5):
        if _is_utf8_first_byte(utf8str[maxbytes - x]):
            ut8_len = _decode_utf8_len_byte(utf8str[maxbytes - x])
            if x == ut8_len:
                break
            
            return utf8str[:maxbytes - x]
    
    return utf8str[:maxbytes]


def _is_utf8_one_byte(byte):
    o = ord(byte)
    return 127 & o == o


def _is_utf8_first_byte(byte):
    o = ord(byte)
    return 191 & o != o


def _decode_utf8_len_byte(byte):
    o = ord(byte)
    v = 240 & o
    if v >= 240:
        return 4
    if v >= 224:
        return 3
    if v >= 192:
        return 2
    if v < 127:
        return 1
    return 0


