# Source Generated with Decompyle++
# File: Flash.pyc (Python 2.6)

import json
import constants
import GUI
import _Scaleform
import weakref
from gui.Scaleform import SCALEFORM_SWF_PATH
from debug_utils import LOG_DEBUG, LOG_CODEPOINT_WARNING, LOG_ERROR, LOG_GUI, _doLog

class Flash(object):
    
    def __init__(self, swf, className = 'Flash', args = None):
        if args is None:
            args = []
        
        self._Flash__fsCbs = { }
        self._Flash__exCbs = { }
        movieDefinition = _Scaleform.MovieDef(SCALEFORM_SWF_PATH + '/' + swf)
        movie = movieDefinition.createInstance()
        self.component = getattr(GUI, className)(movie, *args)
        self.component.focus = True
        self.component.moveFocus = True
        self.component.position.z = 0.5
        self.flashSize = (2, 2)
        self.isActive = False
        movie = self.component.movie
        movie.setFSCommandCallback(_FuncObj(self, 'handleFsCommandCallback'))
        movie.setExternalInterfaceCallback(_FuncObj(self, 'handleExternalInterfaceCallback'))

    
    def __del__(self):
        pass

    
    def _Flash__onLogGui(self, type, msg, *kargs):
        if type == 'DEBUG' and not (constants.IS_DEVELOPMENT):
            return None
        _doLog('%s.GUI' % str(type), msg, kargs)

    
    def _Flash__onLogGuiFormat(self, type, msg, *kargs):
        if type == 'DEBUG' and not (constants.IS_DEVELOPMENT):
            return None
        _doLog('%s.GUI' % str(type), msg % kargs, None)

    
    def movie(self):
        return self.component.movie

    movie = property(movie)
    
    def afterCreate(self):
        self.addExternalCallback('debug.LOG_GUI', self._Flash__onLogGui)
        self.addExternalCallback('debug.LOG_GUI_FORMAT', self._Flash__onLogGuiFormat)

    
    def beforeDelete(self):
        self.removeAllCallbacks()

    
    def active(self, state):
        if self.isActive != state:
            self.isActive = state
            if state:
                GUI.addRoot(self.component)
                self.component.size = self.flashSize
            else:
                GUI.delRoot(self.component)
        

    
    def close(self):
        self.component.script = None
        self.active(False)
        self.beforeDelete()

    
    def setMovieVariable(self, path, value):
        if not isinstance(value, list):
            value = [
                value]
        
        
        try:
            self.movie.invoke(('_root._level0.' + path, value))
        except Exception:
            LOG_ERROR('Error to set movie variable "' + '_root._level0.' + path + '"')


    
    def getMember(self, path):
        return getattr(self.movie, path, None)

    
    def call(self, methodName, args = None):
        if args is None:
            args = []
        
        args.insert(0, methodName)
        self.movie.invoke(('call', args))

    
    def callNice(self, methodName, args = None):
        if args is None:
            args = []
        
        jsonArgs = [
            methodName,
            json.dumps(args)]
        self.movie.invoke(('callJson', jsonArgs))

    
    def respond(self, args = None):
        if args is None:
            args = []
        
        self.movie.invoke(('respond', args))

    
    def addFsCallback(self, command, function):
        self._Flash__fsCbs.setdefault(command, set())
        self._Flash__fsCbs[command].add(function)

    
    def removeFsCallback(self, command):
        
        try:
            self._Flash__fsCbs.pop(command)
        except KeyError:
            pass


    
    def addFsCallbacks(self, commands):
        for (command, function) in commands.items():
            self.addFsCallback(command, function)
        

    
    def removeFsCallbacks(self, *args):
        for command in args:
            self.removeFsCallback(command)
        

    
    def addExternalCallback(self, command, function):
        self._Flash__exCbs.setdefault(command, set())
        self._Flash__exCbs[command].add(function)

    
    def removeExternalCallback(self, command, function = None):
        
        try:
            if function is None:
                self._Flash__exCbs.pop(command)
            elif function in self._Flash__exCbs[command]:
                self._Flash__exCbs[command].remove(function)
        except KeyError:
            pass


    
    def addExternalCallbacks(self, commands):
        for (command, function) in commands.items():
            self.addExternalCallback(command, function)
        

    
    def removeExternalCallbacks(self, *args):
        for command in args:
            self.removeExternalCallback(command)
        

    
    def removeAllCallbacks(self):
        self._Flash__fsCbs.clear()
        self._Flash__exCbs.clear()

    
    def handleFsCommandCallback(self, command, arg):
        result = False
        if command in self._Flash__fsCbs:
            result = True
            callbacks = self._Flash__fsCbs[command]
            for callback in callbacks:
                callback(arg)
            
        else:
            LOG_DEBUG('FsCommandCallback "%s" not found' % command, arg)
        return result

    
    def handleExternalInterfaceCallback(self, command, args):
        result = False
        if command == 'callNice':
            tmp = list(json.loads(args[0]))
            command = tmp.pop(0)
            args = tmp
        
        if command in self._Flash__exCbs:
            result = True
            callbacks = self._Flash__exCbs[command]
            for callback in callbacks:
                callback(*args)
            
        else:
            LOG_DEBUG('ExternalInterfaceCallback "%s" not found' % command, args)
        return result



class _FuncObj:
    
    def __init__(self, obj, funcName):
        self._FuncObj__weakObj = weakref.ref(obj)
        self._FuncObj__funcName = funcName

    
    def __call__(self, command, args):
        if self._FuncObj__weakObj() is not None:
            getattr(self._FuncObj__weakObj(), self._FuncObj__funcName)(command, args)
        else:
            LOG_CODEPOINT_WARNING('weak object has been already destroyed.')



