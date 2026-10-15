# Source Generated with Decompyle++
# File: dictionaries.pyc (Python 2.6)

from debug_utils import LOG_CURRENT_EXCEPTION
import re
import sre_compile
import ResMgr

_defaultReplacementFunction = lambda word: '*' * len(word)

class ObsceneLanguageDictionary(object):
    _ObsceneLanguageDictionary__nonAlphaNumPattern = re.compile(u'[^a-zA-Z]', re.M | re.S | re.U | re.I)
    _ObsceneLanguageDictionary__equivalents = { }
    _ObsceneLanguageDictionary__badWordPatterns = []
    replace = staticmethod(_defaultReplacementFunction)
    
    def load(cls, resourceId):
        '''
\t\tLoad obscene dictionary for the specified language.
\t\t@resourceId: the id of the resource to open.
\t\t@return: ObsceneLanguageDictionary object.
\t\t'''
        object = ObsceneLanguageDictionary.__new__(cls)
        dSection = ResMgr.openSection(resourceId)
        if dSection is None:
            return object
        eqsSection = dSection['equivalents']
        if eqsSection is not None:
            for eqSection in eqsSection.values():
                if eqSection.has_key('find'):
                    pass
                1
                find = None
                if eqSection.has_key('replace'):
                    pass
                1
                replace = None
                if find and replace:
                    object._ObsceneLanguageDictionary__equivalents[find] = replace
                    continue
            
        
        nonAnSection = dSection['nonAlphanumericCharacter']
        if nonAnSection is not None:
            nonAnPattern = nonAnSection.asWideString
            
            try:
                object._ObsceneLanguageDictionary__nonAlphaNumPattern = re.compile(nonAnPattern, re.M | re.S | re.U | re.I)
            except sre_compile.error:
                dSection is None
                LOG_CURRENT_EXCEPTION()
            

        badWordsSection = dSection['badWords']
        if badWordsSection is not None:
            for badWordSet in badWordsSection.values():
                
                try:
                    if badWordSet.has_key('include'):
                        include = re.compile(badWordSet['include'].asWideString, re.M | re.S | re.U | re.I)
                    else:
                        include = re.compile(badWordSet.asWideString, re.M | re.S | re.U | re.I)
                    exclude = None
                    if badWordSet.has_key('exclude'):
                        exclude = re.compile(badWordSet['exclude'].asWideString, re.M | re.S | re.U | re.I)
                    
                    object._ObsceneLanguageDictionary__badWordPatterns.append((include, exclude))
                continue
                except sre_compile.error:
                    dSection is None
                    LOG_CURRENT_EXCEPTION()
                    continue
                

            
        
        return object

    load = classmethod(load)
    
    def overrideReplacementFunction(function):
        '''
\t\tOverrides replacement method.
\t\t'''
        ObsceneLanguageDictionary.replace = staticmethod(function)

    overrideReplacementFunction = staticmethod(overrideReplacementFunction)
    
    def resetReplacementFunction():
        '''
\t\tResets to default replacement method.
\t\t'''
        ObsceneLanguageDictionary.replace = staticmethod(_defaultReplacementFunction)

    resetReplacementFunction = staticmethod(resetReplacementFunction)
    
    def searchAndReplace(self, text):
        '''
\t\tSearch bad words and if find, than replace by replacement function.
\t\tSearch stages:
\t\t\t1. splits string using space.
\t\t\t2. for each word: removed non-alphanumeric character, 
\t\t\tfind and replace equivalents to required characters
\t\t\t3. try finds bad words. If find, than replace, else do nothing.
\t\t
\t\t@param text: string to search for bad words (unicode).
\t\t@return: parsed string (unicode).
\t\t'''
        words = text.split(' ')
        for (idx, word) in enumerate(words):
            parsing = self._ObsceneLanguageDictionary__nonAlphaNumPattern.sub('', word.lower())
            for (find, replace) in self._ObsceneLanguageDictionary__equivalents.iteritems():
                parsing = parsing.replace(find, replace)
            
            for (include, exclude) in self._ObsceneLanguageDictionary__badWordPatterns:
                match = include.search(parsing)
                if match:
                    if exclude is None or not exclude.search(parsing):
                        words[idx] = self.replace(word)
                        break
                        continue
            
        
        return ' '.join(words)



class DomainNameDictionary(object):
    _DomainNameDictionary__webPrefix = '^(http(s)?://)?(www\\.)?'
    _DomainNameDictionary__domainNamePatterns = []
    replace = staticmethod(_defaultReplacementFunction)
    
    def load(cls, resourceId):
        '''
\t\tLoad domain names dictionary for the specified language.
\t\t@resourceId: the id of the resource to open.
\t\t@return: DomainNameDictionary object.
\t\t'''
        object = DomainNameDictionary.__new__(cls)
        dSection = ResMgr.openSection(resourceId)
        if dSection is None:
            return object
        domainNameSection = dSection['domainNames']
        if domainNameSection is not None:
            for domainNameSet in domainNameSection.values():
                
                try:
                    include = re.compile(object._DomainNameDictionary__webPrefix + domainNameSet.asWideString, re.M | re.S | re.U | re.I)
                    object._DomainNameDictionary__domainNamePatterns.append(include)
                continue
                except sre_compile.error:
                    dSection is None
                    LOG_CURRENT_EXCEPTION()
                    continue
                

            
        
        return object

    load = classmethod(load)
    
    def overrideReplacementFunction(function):
        '''
\t\tOverrides replacement method.
\t\t'''
        DomainNameDictionary.replace = staticmethod(function)

    overrideReplacementFunction = staticmethod(overrideReplacementFunction)
    
    def resetReplacementFunction():
        '''
\t\tResets to default replacement method.
\t\t'''
        DomainNameDictionary.replace = staticmethod(_defaultReplacementFunction)

    resetReplacementFunction = staticmethod(resetReplacementFunction)
    
    def searchAndReplace(self, text):
        '''
\t\tSearch domain names and if find, than replace by replacement function.
\t\tSearch stages:
\t\t\t1. splits string using space.
\t\t\t2. try finds domain names. If found, than replace, else do nothing.

\t\t@param text: string to search for domain names (unicode).
\t\t@return: parsed string (unicode).
\t\t'''
        words = text.split(' ')
        for (idx, word) in enumerate(words):
            for pattern in self._DomainNameDictionary__domainNamePatterns:
                match = pattern.search(word)
                if match:
                    words[idx] = self.replace(word)
                    break
                    continue
            
        
        return ' '.join(words)



