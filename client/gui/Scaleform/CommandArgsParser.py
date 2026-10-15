# Source Generated with Decompyle++
# File: CommandArgsParser.pyc (Python 2.6)


class CommandArgsParser(object):
    
    def __init__(self, callbackName, count = 0, converters = None):
        self._CommandArgsParser__callbackName = callbackName
        self._CommandArgsParser__count = count
        if converters is not None:
            pass
        1
        self._CommandArgsParser__converters = []
        self._CommandArgsParser__responseID = None
        self._CommandArgsParser__responseArgs = []

    
    def parse(self, *args):
        self._CommandArgsParser__responseID = args[0]
        self._CommandArgsParser__responseArgs = []
        self._CommandArgsParser__responseArgs.append(self._CommandArgsParser__responseID)
        result = []
        convertersLen = len(self._CommandArgsParser__converters)
        if len(args) == self._CommandArgsParser__count + 1:
            for index in xrange(1, len(args)):
                if convertersLen >= index:
                    result.append(self._CommandArgsParser__converters[index - 1](args[index]))
                    continue
                result.append(args[index])
            
            return result
        raise ValueError, 'Callback %s takes %d arguments' % (self._CommandArgsParser__callbackName, self._CommandArgsParser__count)

    
    def addArgs(self, values, converters = None):
        if converters is None:
            converters = []
        
        parsed = (map,)((lambda item: if len(converters) > item[0]:
converters[item[0]](item[1])item[1]), enumerate(values))
        self._CommandArgsParser__responseArgs.extend(parsed)

    
    def addArg(self, value, converter = None):
        if converter:
            pass
        1
        parsed = value
        self._CommandArgsParser__responseArgs.append(parsed)

    
    def args(self):
        return self._CommandArgsParser__responseArgs



