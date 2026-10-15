# Source Generated with Decompyle++
# File: AccountSettings.pyc (Python 2.6)

import BigWorld
import Settings
import Event
import pickle
import base64
KEY_FILTERS = 'filters'
KEY_SETTINGS = 'settings'
KEY_FAVORITES = 'favorites'
CAROUSEL_FILTER = 'carousel_filter'
BARRACKS_FILTER = 'barracks_filter'
DEFAULT_VALUES = {
    KEY_FILTERS: {
        'shop_current': (-1, 'vehicle'),
        'shop_vehicle': (5, 'lightTank', 'mediumTank', 'heavyTank', 'at-spg', 'spg', 'locked'),
        'shop_module': (5, 'vehicleGun', 'vehicleTurret', 'vehicleEngine', 'vehicleChassis', 'vehicleRadio', 'myVehicles', 0, 'locked', 'inHangar'),
        'shop_shell': (4, 'ARMOR_PIERCING', 'ARMOR_PIERCING_CR', 'HOLLOW_CHARGE', 'HIGH_EXPLOSIVE', 'myVehicleGun', 0),
        'shop_optionalDevice': ('myVehicle', 0, 'onVehicle'),
        'shop_equipment': ('myVehicle', 0, 'onVehicle'),
        'inventory_current': (-1, 'vehicle'),
        'inventory_vehicle': (5, 'lightTank', 'mediumTank', 'heavyTank', 'at-spg', 'spg', 'brocken', 'locked'),
        'inventory_module': (5, 'vehicleGun', 'vehicleTurret', 'vehicleEngine', 'vehicleChassis', 'vehicleRadio', 'myVehicles', 0),
        'inventory_shell': (4, 'ARMOR_PIERCING', 'ARMOR_PIERCING_CR', 'HOLLOW_CHARGE', 'HIGH_EXPLOSIVE', 'myVehicleGun', 0),
        'inventory_optionalDevice': ('myVehicle', 0, 'onVehicle'),
        'inventory_equipment': ('myVehicle', 0, 'onVehicle'),
        CAROUSEL_FILTER: {
            'nation': -1,
            'tankType': -1,
            'ready': False },
        BARRACKS_FILTER: {
            'nation': -1,
            'role': -1,
            'tankType': -1,
            'location': 3,
            'nationID': None } },
    KEY_FAVORITES: {
        'vehicles': [],
        'current': 0 },
    KEY_SETTINGS: {
        'tankmanDropSkillIdx': 0,
        'cursor': False,
        'arcade': {
            'mixing': {
                'alpha': 90,
                'type': 0 },
            'gunTag': {
                'alpha': 90,
                'type': 0 },
            'centralTag': {
                'alpha': 90,
                'type': 0 },
            'net': {
                'alpha': 90,
                'type': 0 },
            'reloader': {
                'alpha': 90,
                'type': 0 },
            'condition': {
                'alpha': 90,
                'type': 0 },
            'cassette': {
                'alpha': 90,
                'type': 0 } },
        'sniper': {
            'snpMixing': {
                'alpha': 90,
                'type': 0 },
            'snpGunTag': {
                'alpha': 90,
                'type': 0 },
            'snpCentralTag': {
                'alpha': 90,
                'type': 0 },
            'snpNet': {
                'alpha': 90,
                'type': 0 },
            'snpReloader': {
                'alpha': 90,
                'type': 0 },
            'snpCondition': {
                'alpha': 90,
                'type': 0 },
            'snpCassette': {
                'alpha': 90,
                'type': 0 } },
        'markers': {
            'ally': {
                'markerBaseIcon': False,
                'markerBaseLevel': False,
                'markerBaseHpIndicator': False,
                'markerBaseDamage': True,
                'markerBaseHp': 0,
                'markerBaseVehicleName': False,
                'markerBasePlayerName': True,
                'markerAltIcon': True,
                'markerAltLevel': True,
                'markerAltHpIndicator': True,
                'markerAltDamage': True,
                'markerAltHp': 1,
                'markerAltVehicleName': True,
                'markerAltPlayerName': False },
            'enemy': {
                'markerBaseIcon': False,
                'markerBaseLevel': False,
                'markerBaseHpIndicator': False,
                'markerBaseDamage': True,
                'markerBaseHp': 0,
                'markerBaseVehicleName': False,
                'markerBasePlayerName': True,
                'markerAltIcon': True,
                'markerAltLevel': True,
                'markerAltHpIndicator': True,
                'markerAltDamage': True,
                'markerAltHp': 1,
                'markerAltVehicleName': True,
                'markerAltPlayerName': False },
            'dead': {
                'markerBaseIcon': False,
                'markerBaseLevel': False,
                'markerBaseHpIndicator': False,
                'markerBaseDamage': True,
                'markerBaseHp': 0,
                'markerBaseVehicleName': False,
                'markerBasePlayerName': True,
                'markerAltIcon': True,
                'markerAltLevel': True,
                'markerAltHpIndicator': True,
                'markerAltDamage': True,
                'markerAltHp': 1,
                'markerAltVehicleName': True,
                'markerAltPlayerName': False } },
        'shopBuyWindow': True,
        'showVehicleIcon': False,
        'showVehicleLevel': False,
        'showExInf4Destroyed': False,
        'ingameHelpVersion': -1,
        'isColorBlind': False,
        'useServerAim': False,
        'minimapAlpha': 0,
        'minimapSize': 0,
        'nationalVoices': False,
        'players_panel': {
            'state': 'medium',
            'showLevels': True,
            'showTypes': True },
        'gameplayMask': 7 } }

class AccountSettings(object):
    onSettingsChanging = Event.Event()
    version = 5
    _AccountSettings__cache = {
        'login': None,
        'section': None }
    _AccountSettings__isFirstRun = True
    
    def __readSection(ds, name):
        if not ds.has_key(name):
            ds.write(name, '')
        
        return ds[name]

    _AccountSettings__readSection = staticmethod(__readSection)
    
    def __readUserSection():
        if AccountSettings._AccountSettings__isFirstRun:
            AccountSettings.convert()
            AccountSettings._AccountSettings__isFirstRun = False
        
        userLogin = getattr(BigWorld.player(), 'name', '')
        if AccountSettings._AccountSettings__cache['login'] != userLogin:
            ads = AccountSettings._AccountSettings__readSection(Settings.g_instance.userPrefs, Settings.KEY_ACCOUNT_SETTINGS)
            for (key, section) in ads.items():
                if key == 'account' and section.readString('login') == userLogin:
                    AccountSettings._AccountSettings__cache['login'] = userLogin
                    AccountSettings._AccountSettings__cache['section'] = section
                    break
                    continue
            else:
                newSection = ads.createSection('account')
                AccountSettings._AccountSettings__cache['login'] = userLogin
                AccountSettings._AccountSettings__cache['section'] = newSection
        
        return AccountSettings._AccountSettings__cache['section']

    _AccountSettings__readUserSection = staticmethod(__readUserSection)
    
    def convert():
        ads = AccountSettings._AccountSettings__readSection(Settings.g_instance.userPrefs, Settings.KEY_ACCOUNT_SETTINGS)
        currVersion = ads.readInt('version', 0)
        if currVersion != AccountSettings.version:
            if currVersion < 1:
                for (key, section) in ads.items()[:]:
                    newSection = ads.createSection('account')
                    newSection.copy(section)
                    newSection.writeString('login', key)
                    ads.deleteSection(key)
                
            
            if currVersion < 2:
                MARKER_SETTINGS_MAP = {
                    'showVehicleIcon': 'markerBaseIcon',
                    'showVehicleLevel': 'markerBaseLevel',
                    'showExInf4Destroyed': 'markerBaseDead' }
                for (key, section) in ads.items()[:]:
                    if key == 'account':
                        accSettings = AccountSettings._AccountSettings__readSection(section, KEY_SETTINGS)
                        defaultMarker = DEFAULT_VALUES[KEY_SETTINGS]['markers'].copy()
                        needUpdate = False
                        for (key1, section1) in accSettings.items()[:]:
                            if key1 in MARKER_SETTINGS_MAP:
                                defaultMarker[MARKER_SETTINGS_MAP[key1]] = pickle.loads(base64.b64decode(accSettings.readString(key1)))
                                accSettings.deleteSection(key1)
                                needUpdate = True
                                continue
                        
                        if needUpdate:
                            accSettings.write('markers', base64.b64encode(pickle.dumps(defaultMarker)))
                        
                
            
            if currVersion < 3:
                for (key, section) in ads.items()[:]:
                    if key == 'account':
                        accSettings = AccountSettings._AccountSettings__readSection(section, KEY_SETTINGS)
                        defaultCursor = DEFAULT_VALUES[KEY_SETTINGS]['arcade'].copy()
                        cassetteDefValues = DEFAULT_VALUES[KEY_SETTINGS]['arcade'].copy()['cassette']
                        for (key1, section1) in accSettings.items()[:]:
                            if key1 == 'cursors':
                                defaultCursor = pickle.loads(base64.b64decode(section1.asString))
                                defaultCursor['cassette'] = cassetteDefValues
                                accSettings.deleteSection(key1)
                                break
                                continue
                        
                        accSettings.write('cursors', base64.b64encode(pickle.dumps(defaultCursor)))
                        continue
                
            
            if currVersion < 4:
                for (key, section) in ads.items()[:]:
                    if key == 'account':
                        accSettings = AccountSettings._AccountSettings__readSection(section, KEY_SETTINGS)
                        defaultCursor = DEFAULT_VALUES[KEY_SETTINGS]['arcade'].copy()
                        for (key1, section1) in accSettings.items()[:]:
                            if key1 == 'cursors':
                                defaultCursor = pickle.loads(base64.b64decode(section1.asString))
                                accSettings.deleteSection(key1)
                                break
                                continue
                        
                        accSettings.write('arcade', base64.b64encode(pickle.dumps(defaultCursor)))
                        continue
                
            
            if currVersion < 5:
                for (key, section) in ads.items()[:]:
                    if key == 'account':
                        accSettings = AccountSettings._AccountSettings__readSection(section, KEY_SETTINGS)
                        for (key1, section1) in accSettings.items()[:]:
                            if key1 == 'markers':
                                accSettings.deleteSection(key1)
                                continue
                        
                
            
            ads.writeInt('version', AccountSettings.version)
        

    convert = staticmethod(convert)
    
    def getFilter(name):
        return AccountSettings._AccountSettings__getValue(name, KEY_FILTERS)

    getFilter = staticmethod(getFilter)
    
    def setFilter(name, value):
        AccountSettings._AccountSettings__setValue(name, value, KEY_FILTERS)

    setFilter = staticmethod(setFilter)
    
    def getSettings(name):
        return AccountSettings._AccountSettings__getValue(name, KEY_SETTINGS)

    getSettings = staticmethod(getSettings)
    
    def setSettings(name, value):
        AccountSettings._AccountSettings__setValue(name, value, KEY_SETTINGS)

    setSettings = staticmethod(setSettings)
    
    def getFavorites(name):
        return AccountSettings._AccountSettings__getValue(name, KEY_FAVORITES)

    getFavorites = staticmethod(getFavorites)
    
    def setFavorites(name, value):
        AccountSettings._AccountSettings__setValue(name, value, KEY_FAVORITES)

    setFavorites = staticmethod(setFavorites)
    
    def __getValue(name, type):
        if DEFAULT_VALUES[type].has_key(name):
            fds = AccountSettings._AccountSettings__readSection(AccountSettings._AccountSettings__readUserSection(), type)
            
            try:
                if fds.has_key(name):
                    return pickle.loads(base64.b64decode(fds.readString(name)))
            except:
                pass

            return DEFAULT_VALUES[type][name]

    _AccountSettings__getValue = staticmethod(__getValue)
    
    def __setValue(name, value, type):
        if DEFAULT_VALUES[type].has_key(name) and AccountSettings._AccountSettings__getValue(name, type) != value:
            fds = AccountSettings._AccountSettings__readSection(AccountSettings._AccountSettings__readUserSection(), type)
            if DEFAULT_VALUES[type][name] != value:
                fds.write(name, base64.b64encode(pickle.dumps(value)))
            else:
                fds.deleteSection(name)
            AccountSettings.onSettingsChanging(name)
        

    _AccountSettings__setValue = staticmethod(__setValue)


