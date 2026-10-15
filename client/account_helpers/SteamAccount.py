# Source Generated with Decompyle++
# File: SteamAccount.pyc (Python 2.6)

import BigWorld
import constants
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG
STEAM_IS_DEVELOPMENT = constants.IS_DEVELOPMENT
STEAM_SUPPORT = False

class __SteamAccount(object):
    _GET_USER_INFO_URL = 'https://api.steampowered.com/ISteamMicroTxn/GetUserInfo/V0001/?steamid=%d'
    _STEAM_LOGIN_SUFFIX = '@steam.com'
    
    def __init__(self):
        self.userInfo = None

    
    def isValid(self):
        if STEAM_SUPPORT:
            pass
        return BigWorld.wg_isSteamInitialized()

    isValid = property(isValid)
    
    def steamID(self):
        if not self.isValid:
            raise AssertionError, 'Available only for steam users'
        return BigWorld.wg_getSteamID()

    steamID = property(steamID)
    
    def getCredentials(self):
        if not self.isValid:
            raise AssertionError, 'Available only for steam users'
        if STEAM_IS_DEVELOPMENT:
            pass
        1
        user = self._STEAM_LOGIN_SUFFIX % self.steamID
        if STEAM_IS_DEVELOPMENT:
            pass
        1
        password = BigWorld.wg_getSteamAuthTicket()
        return (user, password)


g_steamAccount = __SteamAccount()

