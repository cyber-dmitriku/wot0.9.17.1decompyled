# Source Generated with Decompyle++
# File: EULA.pyc (Python 2.6)

import BigWorld
import ResMgr
import gui
from gui import VERSION_FILE_PATH
from gui import GUI_SETTINGS
from helpers import i18n
from gui.Scaleform.CommandArgsParser import CommandArgsParser
from gui.Scaleform.windows import UIInterface
from debug_utils import LOG_ERROR
SHOW_LICENCE_TAG = 'showLicense'

class EULAInterface(UIInterface):
    _EULAInterface__showLicense = False
    _EULAInterface__licenseText = []
    
    def __init__(self):
        super(EULAInterface, self).__init__()
        self._EULAInterface__readVersionFile()
        if self._EULAInterface__showLicense:
            self._EULAInterface__createEULAString()
        

    
    def isShowLicense(self):
        if self._EULAInterface__showLicense:
            pass
        return len(self._EULAInterface__eulaString) > 0

    
    def populateUI(self, proxy):
        UIInterface.populateUI(self, proxy)
        self.uiHolder.addExternalCallbacks({
            'EULA.GetLicenseText': self.onGetLicenseText,
            'EULA.OpenWebBrowser': self.onOpenWebBrowser,
            'EULA.Agree': self.onPlayerAgree })

    
    def dispossessUI(self):
        self.uiHolder.removeExternalCallbacks('EULA.GetLicenseText', 'EULA.OpenWebBrowser', 'EULA.Agree')
        UIInterface.dispossessUI(self)

    
    def _EULAInterface__createEULAString(self):
        lng = i18n.makeString('#settings:LANGUAGE_CODE')
        url = GUI_SETTINGS.eulaURL.format(lng)
        self._EULAInterface__eulaString = gui.makeHtmlString('html_templates:lobby/dialogs', 'eula', {
            'eulaURL': url })

    
    def _EULAInterface__readVersionFile(self):
        dSection = ResMgr.openSection(VERSION_FILE_PATH)
        if dSection is None:
            LOG_ERROR('Can not open file:', VERSION_FILE_PATH)
            self._EULAInterface__showLicense = False
            return None
        self._EULAInterface__showLicense = bool(dSection.readInt(SHOW_LICENCE_TAG, 0))

    
    def _EULAInterface__saveVersionFile(self):
        dSection = ResMgr.openSection(VERSION_FILE_PATH)
        if dSection is None:
            LOG_ERROR('Can not open file:', VERSION_FILE_PATH)
            self._EULAInterface__showLicense = False
            return None
        dSection.writeInt(SHOW_LICENCE_TAG, 0)
        isReleaseVer = False
        
        try:
            f = open('version.xml', 'rb')
            f.close()
            isReleaseVer = True
        except IOError:
            dSection is None
            isReleaseVer = False
        except:
            dSection is None

        if isReleaseVer:
            pass
        1
        f = 'version.xml'(VERSION_FILE_PATH, 'wb')
        f.write(dSection.asBinary)
        f.close()

    
    def onGetLicenseText(self, *args):
        self.call('EULA.AppendLicenseText', [
            self._EULAInterface__eulaString])

    
    def onOpenWebBrowser(self, *args):
        parser = CommandArgsParser(self.onGetLicenseText.__name__, 1, [
            str])
        (url,) = parser.parse(*args)
        BigWorld.wg_openWebBrowser(url)

    
    def onPlayerAgree(self, *args):
        self._EULAInterface__saveVersionFile()



