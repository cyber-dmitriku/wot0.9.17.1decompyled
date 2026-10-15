# Source Generated with Decompyle++
# File: FAQInterface.pyc (Python 2.6)

import BigWorld
from debug_utils import LOG_ERROR
from helpers import i18n
from messenger import g_settings
from messenger.gui.Scalefrom import FAQ_COMMANDS
import re
FAQ_BATCH_SIZE = 5

class FAQInterface(object):
    _FAQInterface__questionPattern = re.compile('^question_(\\d+)$')
    _FAQInterface__answerFormat = 'answer_{0:d}'
    
    def __init__(self):
        super(FAQInterface, self).__init__()
        self._FAQInterface__movieViewHandler = None
        self._FAQInterface__faqDictLoaded = False

    
    def _FAQInterface__buildFAQDict(self):
        if self._FAQInterface__faqDictLoaded:
            return None
        self._FAQInterface__faqDict = { }
        translator = i18n.g_translators['faq']
        for key in translator._catalog.iterkeys():
            if len(key) > 0:
                sreMatch = self._FAQInterface__questionPattern.match(key)
                if sreMatch is not None and len(sreMatch.groups()) > 0:
                    number = int(sreMatch.groups()[0])
                    answer = translator.gettext(self._FAQInterface__answerFormat.format(number))
                    if answer is not None and len(answer) > 0:
                        self._FAQInterface__faqDict[number] = (translator.gettext(key), answer)
                    else:
                        LOG_ERROR('Answer %s is not found' % number)
                
            len(sreMatch.groups()) > 0
        
        self._FAQInterface__faqDictLoaded = True

    
    def populateUI(self, movieViewHandler):
        self._FAQInterface__movieViewHandler = movieViewHandler
        self._FAQInterface__movieViewHandler.addExternalCallbacks({
            FAQ_COMMANDS.Get(): self.onGetFAQ })

    
    def dispossessUI(self):
        self._FAQInterface__movieViewHandler.removeExternalCallbacks(FAQ_COMMANDS.Get())
        self._FAQInterface__movieViewHandler = None

    
    def onGetFAQ(self, *args):
        self._FAQInterface__buildFAQDict()
        faq = sorted(self._FAQInterface__faqDict.items(), cmp = (lambda item, other: cmp(item[0], other[0])))
        formatHtml = g_settings.htmlTemplates.format
        batch = []
        if len(faq) > 0:
            (question, answer) = (number,)
            batch = [
                formatHtml('firstFAQItem', ctx = {
                    'number': number,
                    'question': question,
                    'answer': answer })]
        
        for (question, answer) in faq[1:]:
            if FAQ_BATCH_SIZE > len(batch):
                self._FAQInterface__movieViewHandler.call(FAQ_COMMANDS.Append(), [
                    ''.join(batch)])
                batch = []
            
            batch.append(formatHtml('nextFAQItem', ctx = {
                'number': number,
                'question': question,
                'answer': answer }))
        
        if len(batch) > 0:
            self._FAQInterface__movieViewHandler.call(FAQ_COMMANDS.Append(), [
                ''.join(batch)])
        



