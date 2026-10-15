# Source Generated with Decompyle++
# File: SystemMessages.pyc (Python 2.6)

from abc import ABCMeta, abstractmethod
from enumerations import Enumeration
SM_TYPE = Enumeration('System message type', [
    'Error',
    'Warning',
    'Information',
    'GameGreeting',
    'PowerLevel',
    'FinancialTransactionWithGold',
    'FinancialTransactionWithCredits',
    'PurchaseForGold',
    'DismantlingForGold',
    'PurchaseForCredits',
    'Selling',
    'Repair',
    'CustomizationForGold',
    'CustomizationForCredits'])

class BaseSystemMessages(object):
    __metaclass__ = ABCMeta
    
    def init(self):
        pass

    init = abstractmethod(init)
    
    def destroy(self):
        pass

    destroy = abstractmethod(destroy)
    
    def pushMessage(self, text, type = SM_TYPE.Information):
        pass

    pushMessage = abstractmethod(pushMessage)
    
    def pushI18nMessage(self, key, *args, **kwargs):
        pass

    pushI18nMessage = abstractmethod(pushI18nMessage)

g_instance = None

def pushMessage(text, type = SM_TYPE.Information):
    if g_instance:
        g_instance.pushMessage(text, type)
    


def pushI18nMessage(key, *args, **kwargs):
    if g_instance:
        g_instance.pushI18nMessage(key, *args, **args)
    


