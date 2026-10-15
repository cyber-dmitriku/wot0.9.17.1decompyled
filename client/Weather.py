# Source Generated with Decompyle++
# File: Weather.pyc (Python 2.6)

import BigWorld
import ResMgr
import FX
import random
from functools import partial
import traceback
from Listener import Listenable
import Math
if BigWorld.component != 'editor':
    import game as Personality
else:
    import Personality
weatherXML = ResMgr.openSection('scripts/weather.xml')

class WeatherSystem:
    '''
\tThis class represents a single weather system.  It binds together some
\tskyboxes, an effect file, bloom settings, and a number of other built-in
\tweather system properties.  It knows how to load all its required
\tresources in the background, and fade between any existing weather system
\tand its own.
\tIt loads from an XML data section, which by default can be found in the
\tfile "scripts/data/weather.xml".
\tThere are two main entry points for WeatherSystem
\t- fadeIn
\t- prepareResources
\tPlease see the pyDoc help for these methods for more detailed information.
\t'''
    
    def __init__(self, ds):
        self.name = ds.name
        self.skyBoxes = list(ds.readStrings('skyBox'))
        self.skyBoxModels = []
        self.rain = ds.readFloat('rain', 0)
        self.sun = ds.readVector4('sun', (1, 1, 1, 1))
        self.ambient = ds.readVector4('ambient', (1, 1, 1, 1))
        self.fog = ds.readVector4('fog', (1, 1, 1, 1))
        self.windSpeed = ds.readVector2('windSpeed', (0, 0))
        self.windGustiness = ds.readFloat('windGustiness', 0)
        self.skyBoxFogFactor = ds.readFloat('fogFactor', 0.15)
        self.fader = Math.Vector4Morph()
        self.fader.duration = 1
        f = self._fogAmount(self.fog[3])
        self.fader.target = (f, 0, 1, 0)
        self.fx = None
        self.fxName = ds.readString('sfx')
        self.loaded = False

    
    def _loadSkyBoxes(self, callback = None, immediate = False):
        if self.loaded:
            if callback:
                callback()
            
        elif not immediate:
            BigWorld.loadResourceListBG(self.skyBoxes, partial(self._onLoadSkyBoxes, callback))
        else:
            resourceRefs = { }
            for i in self.skyBoxes:
                
                try:
                    resourceRefs[i] = BigWorld.Model(i)
                continue
                except ValueError:
                    resourceRefs[i] = BigWorld.Model('')
                    continue
                

            
            self._onLoadSkyBoxes(callback, resourceRefs)

    
    def _onLoadSkyBoxes(self, callback, resourceRef):
        self.loaded = True
        for sb in self.skyBoxes:
            
            try:
                self.skyBoxModels.append(resourceRef[sb])
            continue
            except ValueError:
                self.skyBoxModels.append(BigWorld.Model(''))
                continue
            

        
        if callback != None:
            callback()
        

    
    def _unload(self):
        for i in self.skyBoxModels:
            BigWorld.delSkyBox(i, self.fader)
        
        self.skyBoxModels = []
        if self.fx != None:
            self.fx.detach()
            self.fx = None
        
        self.loaded = False

    
    def _loadFX(self, callback = None):
        if self.fxName != '':
            BigWorld.loadResourceListBG(FX.prerequisites(self.fxName), partial(self._onLoadFX, callback))
        elif callback:
            callback()
        

    
    def _onLoadFX(self, callback, resourceRef):
        if self.fx != None:
            self.fx.detach()
            self.fx = None
        
        if self.loaded:
            self.fx = FX.Persistent(self.fxName, resourceRef)
            self.fx.attach(None)
            self.fx.go()
            if callback:
                callback()
            
        

    
    def _fadeOutFX(self):
        if self.fx != None:
            return self.fx.stop()
        return 0

    
    def fadeIn(self, fadingIn, fadeSpeed, immediate = False):
        '''
\t\tThis method Fades in / out this weather system.  We load
\t\tour models/textures on demand when fading in, and free them
\t\tas soon as we have fully faded out.
\t\tIf immediate is set to True, then the natural fade out speed
\t\tof the effect is clamped to the passed in fade time. This may cause it
\t\tto noticeably pop when detached from the scene.  If\timmediate is False,
\t\tthe effect will fade out at its own natural speed, determined by the
\t\teffect itself to prevent popping.
\t\t'''
        curr = self.fader.value
        if fadingIn:
            if not self.loaded:
                print "calling fadeIn on a weather system that isn't loaded.  please call prepareResources() first", self.name
                traceback.print_stack()
                return None
            for sb in self.skyBoxModels:
                if sb != None:
                    BigWorld.addSkyBox(sb, self.fader)
                    continue
            
            f = self._fogAmount(self.fog[3])
            self.fader.duration = fadeSpeed - 0.1
            self.fader.target = (f, 0, 1, 1)
            
            try:
                BigWorld.weather().windAverage(self.windSpeed[0], self.windSpeed[1])
                BigWorld.weather().windGustiness(self.windGustiness)
            except ValueError:
                pass
            except EnvironmentError:
                pass
            

        if self.loaded:
            sfxFadeSpeed = self._fadeOutFX()
            if not immediate:
                fadeSpeed = max(fadeSpeed, sfxFadeSpeed)
            
            BigWorld.callback(fadeSpeed, self._unload)
            self.fader.duration = fadeSpeed - 0.1
            self.fader.target = (curr[0], curr[1], curr[2], 0)
        

    
    def _fogAmount(self, amount):
        '''
\t\tReturns the fog amount.  This is adjusted by the sky box fog factor
\t\tso the fog and the skyboxes interact correctly.
\t\t'''
        return (amount - 1) * self.skyBoxFogFactor

    
    def prepareResources(self, callback = None, immediate = False):
        '''
\t\tThis method prepares the weather system for use.  It cues up
\t\tresource loading in the background thread, and when ready, calls
\t\tthe supplied callback function.  If immediate is set to true,
\t\tthe callback function is called immediately, and no resources are
\t\tpreloaded.  This will probably then cause resource loading to hit
\t\tand stall the main thread when this weather system is summoned.
\t\t'''
        if not self.loaded:
            self._loadSkyBoxes(partial(self._loadFX, callback), immediate)
        elif callback:
            callback()
        

    
    def setFadeSpeed(self, duration):
        '''
\t\tThis method sets the fade in/out speed for the weather system.
\t\t'''
        self.fader.duration = duration

    
    def edUnloadSkyBoxes(self):
        '''
\t\tThis method unsets all sky boxes used by this weather system.
\t\t'''
        for sb in self.skyBoxModels:
            if sb != None:
                BigWorld.delSkyBox(sb, self.fader)
                continue
        

    
    def edReloadSkyBoxes(self):
        '''
\t\tThis method resets all sky boxes used by this weather system, and
\t\tmakes sure the skybox models list properly reflects the contents
\t\tof the skyboxes list.
\t\t'''
        self.tempCopy = self.skyBoxModels
        self.skyBoxModels = []
        for sb in self.skyBoxes:
            
            try:
                model = BigWorld.Model(sb)
            except ValueError:
                model = BigWorld.Model('')

            self.skyBoxModels.append(model)
            BigWorld.addSkyBox(model, self.fader)
        



class Weather(Listenable):
    '''
\tThis class manages a list of WeatherSystems, and provides an API to
\tcontrol the weather on the client and in the tools.
\t'''
    
    def __init__(self):
        Listenable.__init__(self)
        self.fadeSpeed = 15
        self.system = None
        self.randomWeatherCallback = None
        self.summoning = False
        self.pendingWeatherChange = None
        self.localOverride = None
        self.overridenWeather = None
        self.onChangeSpace()

    
    def toggleRandomWeather(self, force = None):
        '''
\t\tThis method chooses a random weather system every 60 seconds.
\t\t'''
        if force != None:
            turningOff = not force
        else:
            turningOff = self.randomWeatherCallback != None
        stateChanged = False
        wasOn = self.randomWeatherCallback != None
        if turningOff and self.randomWeatherCallback != None:
            BigWorld.cancelCallback(self.randomWeatherCallback)
            self.randomWeatherCallback = None
            stateChanged = wasOn
        elif not turningOff:
            self._randomWeather(True)
            stateChanged = not wasOn
        
        if stateChanged:
            Personality.addChatMsg(-1, 'Random weather turned ' + ('on', 'off')[turningOff])
        

    
    def isWeatherRandom(self):
        '''
\t\tThis method returns whether or not random weather is currently enabled.
\t\t'''
        return self.randomWeatherCallback != None

    
    def nextWeatherSystem(self, direction, immediate = False):
        '''
\t\tThis method summons the next weather system that is available
\t\tfor the current space.  If direction is False however, the
\t\tprevious weather system will be summoned instead. 
\t\t'''
        systems = self._weatherSystemsForCurrentSpace()
        idx = 0
        if self.system != None:
            for s in systems:
                if s.name == self.system.name:
                    break
                
                idx += 1
            
        
        if direction:
            idx += 1
        else:
            idx -= 1
        self.toggleRandomWeather(False)
        self.summon(systems[idx % len(systems)].name, immediate)

    
    def _randomWeather(self, initial = False):
        if initial or self.randomWeatherCallback != None:
            self.randomWeatherCallback = BigWorld.callback(60, self._randomWeather)
            systems = self._weatherSystemsForCurrentSpace()
            ds = random.choice(systems)
            self.summon(ds.name)
        

    
    def _setFadeSpeed(self, duration):
        self.fadeSpeed = max(0.1, duration)
        self.weatherController.duration = self.fadeSpeed
        self.sunlightController.duration = self.fadeSpeed
        self.ambientController.duration = self.fadeSpeed
        self.fogController.duration = self.fadeSpeed
        if self.system:
            self.system.setFadeSpeed(self.fadeSpeed)
        

    
    def _weatherSystemsForCurrentSpace(self):
        systems = weatherXML.values()
        return systems

    
    def onChangeSpace(self, spaceID = -1, spaceSettings = None):
        '''
\t\tThis method implements a callback for when the camera space has
\t\tchanged.  When the space is changed, appropriate weather is chosen
\t\tfor the new space.  This is chosen by either the last known
\t\tweather system for the space, or the default from the weather xml file.\t\t
\t\t'''
        self.currentSpaceID = spaceID
        m = Math.Vector4Morph()
        m.duration = self.fadeSpeed
        m.target = (0, 0, 0, 0)
        m.time = m.duration
        BigWorld.weatherController(m)
        self.weatherController = m
        m = Math.Vector4Morph()
        m.duration = self.fadeSpeed
        m.target = (1, 1, 1, 1)
        m.time = m.duration
        BigWorld.sunlightController(m)
        self.sunlightController = m
        m = Math.Vector4Morph()
        m.duration = self.fadeSpeed
        m.target = (1, 1, 1, 1)
        m.time = m.duration
        BigWorld.ambientController(m)
        self.ambientController = m
        m = Math.Vector4Morph()
        m.duration = self.fadeSpeed
        m.target = (1, 1, 1, 1)
        m.time = m.duration
        BigWorld.fogController(m)
        self.fogController = m

    
    def summon(self, systemName, immediate = False, serverSync = False, resummon = False):
        '''
\t\tThis method queues a weather system for display.  Usually weather
\t\tsystems will fade in over a period of 15 seconds or so, to make the
\t\ttransition appear seamless to the viewer.  However, you may ask for
\t\tan immediate transition, this will fade the new weather system in
\t\tover a much shorter period of time.  The serverSync argument tells
\t\tthe method whether or not this weather system has been summoned by
\t\tthe server.  If not, it indicates that the user has chosen the system
\t\tinstead; in this case if environmentSync is set to true, the server
\t\twill be informed of the change and this will be propogated to other
\t\tclients.
\t\t'''
        if self.localOverride != None:
            self.overridenWeather = systemName
            systemName = self.localOverride
        
        if not resummon and self.system and self.system.name == systemName:
            return None
        if resummon:
            self._setFadeSpeed(0.1)
        elif immediate:
            self._setFadeSpeed(2.5)
        else:
            self._setFadeSpeed(15)
        if self.summoning and not immediate:
            self.pendingWeatherChange = systemName
            self.listeners.weather(systemName = systemName)
            return None
        for ds in weatherXML.values():
            if ds.name == systemName:
                
                try:
                    if not serverSync and BigWorld.getEnvironmentSync():
                        p = BigWorld.player()
                        p.cell.syncServWeather(p.spaceID, systemName)
                except KeyError:
                    not immediate
                    self.system.name == systemName
                except AttributeError:
                    self.system.name == systemName
                except:
                    not immediate

                system = WeatherSystem(ds)
                self.summoning = True
                self.listeners.weather(system = system)
                system.prepareResources(partial(self._systemReadySummon, system, immediate, resummon), immediate)
                continue
            not immediate
        

    
    def override(self, systemName, immediate = False):
        '''
\t\tThis method allows you to set a local override to the weather systems; for example
\t\tif you have a regional weather system entity overriding the weather for the rest
\t\tof the space.
\t\tCalling this method with and empty string, or None as the systemName, will remove
\t\tthe existing override, and restore the last requested system.
\t\t'''
        if systemName == None or systemName == '':
            self.localOverride = None
            self.summon(self.overridenWeather, immediate, serverSync = False, resummon = False)
            self.overridenWeather = None
        else:
            self.overridenWeather = self.system.name
            self.summon(systemName, immediate, serverSync = False, resummon = False)
            self.localOverride = systemName

    
    def _systemReadySummon(self, system, immediate, resummon):
        if self.system:
            self.system.fadeIn(False, self.fadeSpeed, immediate)
            self.system = None
        
        if system != None:
            self.system = system
            self.system.fadeIn(True, self.fadeSpeed)
            self.skyBoxFogFactor = system.skyBoxFogFactor
            self.rain(system.rain)
            self.ambient(system.ambient)
            self.fog(system.fog, False)
            self.sun(system.sun)
            BigWorld.callback(self.fadeSpeed, self._onSystemSummoned)
        else:
            self._onSystemSummoned()

    
    def _onSystemSummoned(self):
        self.listeners.weather(system = self.system)
        self.summoning = False
        if self.pendingWeatherChange != None:
            self.summon(self.pendingWeatherChange)
            self.pendingWeatherChange = None
        

    
    def newSystemByName(self, systemName):
        '''
\t\tThis method returns a new WeatherSystem instance, by name.
\t\t'''
        for ds in weatherXML.values():
            if ds.name == systemName:
                system = WeatherSystem(ds)
                return system
        

    
    def _animateValue(self, value, v4a, index):
        expected = Math.Vector4(v4a.target)
        expected[index] = value
        v4a.target = expected

    
    def _animateVector4(self, v4a, value):
        v4a.target = value

    
    def rain(self, amount):
        '''
\t\tThis method sets the current rain amount.  It will be overridden when
\t\ta new weather system is summoned.
\t\t'''
        self._animateValue(amount, self.weatherController, 0)

    
    def fog(self, value, applyToSystem = True):
        '''
\t\tThis method sets the current fog colour and density.  It will be
\t\toverridden when a new weather system is summoned.
\t\t'''
        self._animateVector4(self.fogController, value)
        if applyToSystem:
            fogAmount = value[3]
            self._animateValue(self.system._fogAmount(fogAmount), self.system.fader, 0)
        

    
    def sun(self, value):
        '''
\t\tThis method sets the current sun colour.  It is a multiplier over the existing
\t\ttime of day sun colour.  It will be overridden when\ta new weather
\t\tsystem is summoned.
\t\t'''
        value *= value.w
        value.w = 1
        self._animateVector4(self.sunlightController, value)

    
    def ambient(self, value):
        '''
\t\tThis method sets the current ambient colour.  It is a multiplier over
\t\tthe existing time of day sun colour.  It will be overridden when
\t\ta new weather system is summoned.
\t\t'''
        value *= value.w
        value.w = 1
        self._animateVector4(self.ambientController, value)


s_weather = None

def weather():
    '''
\tThis function gets the global weather system singleton.
\t'''
    global s_weather
    if not s_weather:
        s_weather = Weather()
    
    return s_weather


def fini():
    '''
\tThis function releases the new weather system. While not necessary for
\tmemory leak reasons (as when scripts are shutdown, this python object
\tis also released,) we want explicit control over when the weather system
\tsingleton is released.
\t'''
    global s_weather
    if s_weather is not None:
        Personality.delCameraSpaceChangeListener(s_weather.onChangeSpace)
        s_weather = None
    


