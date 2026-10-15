# Source Generated with Decompyle++
# File: GuiBinding.pyc (Python 2.6)

from windows import UIInterface

def disposer(obj, disposeUI):
    
    def wrapper():
        disposeUI()
        obj.GUI.script = None
        obj.GUI = None

    return wrapper

binding = {
    'RadialMenu': '_level0.radialMenu' }

def FlashBind(guiDestinationAlias):
    guiDestination = binding.get(guiDestinationAlias)
    
    def injector(wrappedMethod):
        
        def wrapper(*args):
            object = args[0]
            UIInterface.populateUI(*args)
            object.GUICtrl = object.uiHolder.getMember(guiDestination)
            object.GUICtrl.script = object
            object.disposeUI = disposer(object, wrappedMethod)
            wrappedMethod(*args)

        return wrapper

    return injector


