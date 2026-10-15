# Source Generated with Decompyle++
# File: Event.pyc (Python 2.6)

from debug_utils import *

class Event(object):
    
    def __init__(self, manager = None):
        self._Event__delegates = set()
        if manager is not None:
            manager.register(self)
        

    
    def __call__(self, *args):
        for delegate in set(self._Event__delegates):
            
            try:
                delegate(*args)
            continue
            LOG_CURRENT_EXCEPTION()
            continue

        

    
    def __iadd__(self, delegate):
        self._Event__delegates.add(delegate)
        return self

    
    def __isub__(self, delegate):
        self._Event__delegates.discard(delegate)
        return self

    
    def clear(self):
        self._Event__delegates.clear()

    
    def __repr__(self):
        return 'Event(%s):%s' % (len(self._Event__delegates), repr(self._Event__delegates))



class Handler(object):
    
    def __init__(self, manager = None):
        self._Handler__delegate = None
        if manager is not None:
            manager.register(self)
        

    
    def __call__(self, *args):
        if self._Handler__delegate is not None:
            return self._Handler__delegate(*args)

    
    def set(self, delegate):
        self._Handler__delegate = delegate

    
    def clear(self):
        self._Handler__delegate = None



class EventManager(object):
    
    def __init__(self):
        self._EventManager__events = []

    
    def register(self, event):
        self._EventManager__events.append(event)

    
    def clear(self):
        for event in self._EventManager__events:
            event.clear()
        



