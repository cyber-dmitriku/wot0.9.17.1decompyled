# Source Generated with Decompyle++
# File: obfuscators.pyc (Python 2.6)

import base64
from debug_utils import LOG_CURRENT_EXCEPTION

class XORObfuscator:
    _XORObfuscator__PREFIX = '#obfuscate:'
    
    def __init__(self, key):
        if len(key) < 1:
            raise ValueError, 'Key length must be at least one character'
        len(key) < 1
        self._XORObfuscator__key = key

    
    def _XORObfuscator__doXor(self, data):
        kIdx = 0
        processed = []
        for x in range(len(data)):
            processed.append(chr(ord(data[x]) ^ ord(self._XORObfuscator__key[kIdx])))
            kIdx = (kIdx + 1) % len(self._XORObfuscator__key)
        
        return ''.join(processed)

    
    def obfuscate(self, data):
        return base64.b64encode(self._XORObfuscator__PREFIX + self._XORObfuscator__doXor(data))

    
    def unobfuscate(self, data):
        if len(data.strip()) % 4 != 0:
            return data
        
        try:
            decode = base64.b64decode(data)
        except:
            len(data.strip()) % 4 != 0
            LOG_CURRENT_EXCEPTION()
            return data

        if decode.startswith(self._XORObfuscator__PREFIX):
            return self._XORObfuscator__doXor(decode[len(self._XORObfuscator__PREFIX):])
        return data



class PasswordObfuscator(XORObfuscator):
    
    def __init__(self):
        XORObfuscator.__init__(self, '416c34666745786b'.decode('hex'))



