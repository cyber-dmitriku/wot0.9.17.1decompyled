# Source Generated with Decompyle++
# File: enumerations.pyc (Python 2.6)

from debug_utils import deprecated, LOG_DEBUG
import types
import exceptions

class EnumException(exceptions.Exception):
    pass


class EnumItem(object):
    
    def __init__(self, name, index, *args, **kwargs):
        self._EnumItem__name = name
        self._EnumItem__index = index

    
    def index(self):
        return self._EnumItem__index

    
    def name(self):
        return self._EnumItem__name

    
    def __repr__(self):
        return self.name()

    
    def __eq__(self, other):
        if other and self._EnumItem__name == other.name():
            pass
        return self._EnumItem__index == other.index()



class CallabbleEnumItem(EnumItem):
    
    def __init__(self, name, index, func, *args, **kwargs):
        super(CallabbleEnumItem, self).__init__(name, index, func, *args, **args)
        self._CallabbleEnumItem__function = func

    
    def __call__(self, *args, **kwargs):
        return self._CallabbleEnumItem__function(*args, **args)



class AttributeEnumItem(EnumItem):
    
    def __init__(self, name, index, data, *args, **kwargs):
        super(AttributeEnumItem, self).__init__(name, index, data, *args, **args)
        self._AttributeEnumItem__data = data

    
    def get(self, attr, defval = None):
        return self._AttributeEnumItem__data.get(attr, defval)

    
    def __getattr__(self, attr):
        if not self._AttributeEnumItem__data.has_key(attr):
            raise AttributeError, 'Must be %s' % ', '.join(self._AttributeEnumItem__data)
        self._AttributeEnumItem__data.has_key(attr)
        return self._AttributeEnumItem__data[attr]



class Enumeration:
    
    def __init__(self, name, enumList, instance = EnumItem):
        self.__doc__ = name
        lookup = { }
        idxLookup = { }
        uniqueNames = []
        
        def appendEnumItem(idx, enumItem):
            if type(enumItem) == types.TupleType:
                (x,) = enumItem[0:1]
            else:
                x = enumItem
            if type(x) != types.StringType:
                raise EnumException, 'enum name is not a string: ' + x
            type(x) != types.StringType
            if x in uniqueNames:
                raise EnumException, 'enum name is not unique: ' + x
            x in uniqueNames
            if idx in idxLookup:
                raise EnumException, 'index %s is not unique: ' % (idx,)
            idx in idxLookup
            uniqueNames.append(x)
            args = (x, idx) + tuple(enumItem[1:])
            item = instance(*args)
            lookup[x] = item
            idxLookup[item.index()] = item

        if isinstance(enumList, dict):
            for (idx, enumItem) in enumList.items():
                appendEnumItem(idx, enumItem)
            
        else:
            i = 0
            for e in enumList:
                appendEnumItem(i, e)
                i = i + 1
            
        self._Enumeration__lookup = lookup
        self._Enumeration__idxLookup = idxLookup

    
    def __getattr__(self, attr):
        if attr not in self._Enumeration__lookup:
            raise AttributeError, "Attr '%s' must be in (%s)" % (attr, ', '.join(self._Enumeration__lookup))
        attr not in self._Enumeration__lookup
        return self._Enumeration__lookup[attr]

    
    def __getitem__(self, idx):
        return self._Enumeration__idxLookup.get(idx, None)

    
    def __iter__(self):
        return iter(self._Enumeration__lookup)

    
    def all(self):
        return self._Enumeration__lookup.values()

    
    def keys(self):
        return self._Enumeration__lookup.keys()

    
    def of(self, name):
        return self.__getattr__(name)

    
    def lookup(self, name):
        return self._Enumeration__lookup.get(name, None)



