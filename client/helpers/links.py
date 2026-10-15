# Source Generated with Decompyle++
# File: links.pyc (Python 2.6)

import BigWorld
import ResMgr
import constants
from debug_utils import LOG_CURRENT_EXCEPTION, LOG_ERROR
from gui import GUI_SETTINGS

def openRegistrationWebsite():
    
    try:
        url = 'http://game.worldoftanks.ru/registration/'
        
        try:
            url = GUI_SETTINGS.registrationURL
        except:
            LOG_CURRENT_EXCEPTION()

        if constants.IS_DEVELOPMENT:
            pass
        1
        ds = '../game/ref.xml'('../ref.xml')
        if ds is not None:
            refCode = ds.readString('refCode')
            if len(refCode) > 0:
                url = url + 'code/' + refCode
            
        
        BigWorld.wg_openWebBrowser(url)
    except Exception:
        LOG_CURRENT_EXCEPTION()



def getPaymentWebsiteURL():
    url = 'http://game.worldoftanks.ru/payment/'
    
    try:
        url = GUI_SETTINGS.paymentURL
    except:
        LOG_CURRENT_EXCEPTION()

    
    try:
        import base64 as base64
        connectionManager = connectionManager
        import ConnectionManager
        if not connectionManager.areaID:
            pass
        areaID = 'errorArea'
        if not connectionManager.loginName:
            pass
        loginName = 'errorLogin'
        userEncoded = base64.b64encode(loginName)
        url = url % {
            'areaID': areaID,
            'userEncoded': userEncoded }
    except:
        LOG_CURRENT_EXCEPTION()

    return url


def openPaymentWebsite():
    
    try:
        url = getPaymentWebsiteURL()
        if len(url) > 0:
            BigWorld.wg_openWebBrowser(url)
        else:
            LOG_ERROR('Payment website url is empty.Check tag <paymentURL> in the "text/settings.xml".')
    except Exception:
        LOG_CURRENT_EXCEPTION()



def openFinPasswordWebsite():
    
    try:
        url = 'http://game.worldoftanks.ru/'
        
        try:
            url = GUI_SETTINGS.finPasswordURL
        except:
            LOG_CURRENT_EXCEPTION()

        BigWorld.wg_openWebBrowser(url)
    except Exception:
        LOG_CURRENT_EXCEPTION()



def openMigrationWebsite(login):
    
    try:
        url = 'http://game.worldoftanks.ru/migration/%s'
        
        try:
            url = GUI_SETTINGS.migrationURL
        except:
            LOG_CURRENT_EXCEPTION()

        BigWorld.wg_openWebBrowser(url % login)
    except Exception:
        LOG_CURRENT_EXCEPTION()



