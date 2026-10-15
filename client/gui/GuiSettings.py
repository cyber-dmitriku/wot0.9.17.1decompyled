# Source Generated with Decompyle++
# File: GuiSettings.pyc (Python 2.6)

import ResMgr
guiPresetsResource = 'gui/gui_settings.xml'

class GuiSettings:
    
    def readBoolean(dataSection):
        '''
\t\tformatter function for boolean values
\t\t'''
        return dataSection.readBool('')

    readBoolean = staticmethod(readBoolean)
    
    def readInt(dataSection):
        '''
\t\tformatter function for integer value
\t\t'''
        return dataSection.readInt('')

    readInt = staticmethod(readInt)
    
    def readVector2(dataSection):
        '''
\t\tformatter function for tuple of 2 numbers
\t\t'''
        return dataSection.asVector2.tuple()

    readVector2 = staticmethod(readVector2)
    
    def readVector3(dataSection):
        '''
\t\tformatter function for tuple of 3 numbers
\t\t'''
        return dataSection.asVector3.tuple()

    readVector3 = staticmethod(readVector3)
    
    def readVector4(dataSection):
        '''
\t\tformatter function for tuple of 4 numbers
\t\t'''
        return dataSection.asVector4.tuple()

    readVector4 = staticmethod(readVector4)
    
    def readStringsList(dataSection):
        '''
\t\tformatter function for list of strings
\t\t'''
        list = []
        for value in dataSection.values():
            list.append(value.asString)
        
        return list

    readStringsList = staticmethod(readStringsList)
    
    def __init__(self):
        '''
\t\tconstructs GuiSettings instance using values from guiPresetsResource
\t\t'''
        self._GuiSettings__settings = { }
        ds = ResMgr.openSection(guiPresetsResource)
        if ds is not None:
            for (key, value) in ds.items():
                if key in keyReaders:
                    self._GuiSettings__settings[key] = keyReaders[key](value)
                    continue
                self._GuiSettings__settings[key] = value.asString
            
        else:
            raise IOError('gui_settins file is missing')
        return ds is not None

    
    def __getattr__(self, name):
        if name in self._GuiSettings__settings:
            return self._GuiSettings__settings[name]
        raise AttributeError('Setting not found in {0}: {1}'.format(self.__class__, name))

    
    def __setattr__(self, name, value):
        if name == '_GuiSettings__settings':
            self.__dict__[name] = value
        elif name in self._GuiSettings__settings:
            raise AttributeError('Assignment is forbidden for {0}. Argument name: {1}'.format(self.__class__, name))
        


keyReaders = {
    'nations_order': GuiSettings.readStringsList,
    'minimapSize': GuiSettings.readBoolean,
    'goldTransfer': GuiSettings.readBoolean,
    'voiceChat': GuiSettings.readBoolean,
    'technicalInfo': GuiSettings.readBoolean,
    'nationHangarSpace': GuiSettings.readBoolean,
    'customizationCamouflages': GuiSettings.readBoolean,
    'customizationHorns': GuiSettings.readBoolean,
    'customizationEmblems': GuiSettings.readBoolean,
    'customizationInscriptions': GuiSettings.readBoolean,
    'showMinimapSuperHeavy': GuiSettings.readBoolean,
    'showMinimapDeath': GuiSettings.readBoolean,
    'permanentMinimapDeath': GuiSettings.readBoolean,
    'markerHitSplashDuration': GuiSettings.readInt,
    'sixthSenseDuration': GuiSettings.readInt,
    'minimapDeathDuration': GuiSettings.readInt,
    'rememberPassVisible': GuiSettings.readBoolean,
    'clearLoginValue': GuiSettings.readBoolean,
    'markerScaleSettings': GuiSettings.readVector4,
    'markerBgSettings': GuiSettings.readVector4,
    'specPrebatlesVisible': GuiSettings.readBoolean,
    'battleStatsInHangar': GuiSettings.readBoolean }

