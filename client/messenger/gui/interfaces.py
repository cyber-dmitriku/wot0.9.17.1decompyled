# Source Generated with Decompyle++
# File: interfaces.pyc (Python 2.6)


class DispatcherProxyHolder(object):
    _dispatcherProxy = None


class MessengerWindowInterface(DispatcherProxyHolder):
    channels = property((lambda self: self._dispatcherProxy.channels))
    users = property((lambda self: self._dispatcherProxy.users))
    
    def show(self):
        pass

    
    def close(self):
        pass

    
    def editing(self):
        return False

    
    def populateUI(self, *args):
        pass

    
    def dispossessUI(self):
        pass

    
    def addChannelMessage(self, wrapper):
        '''
\t\tAdds message to channel
\t\t@param wrapper: object hold message data
\t\t'''
        pass

    
    def addSystemMessage(self, message):
        '''
\t\tAdds system message to channel
\t\t@param wrapper: object hold message data
\t\t'''
        pass

    
    def addChannel(self, channel):
        '''
\t\tAdds dummy channel
\t\t@param channel: object hold channel data
\t\t'''
        return True

    
    def removeChannel(self, cid):
        '''
\t\tRemove dummy channel
\t\t@param cid: channel id
\t\t'''
        return True

    
    def getChannelPage(self, cid):
        '''
\t\tGets channel page by cid
\t\t@param cid: channel id
\t\t'''
        pass

    
    def clear(self):
        '''
\t\tClear player data, when disconnect
\t\t'''
        pass

    
    def showActionFailureMessage(self, message, title = None, modal = None):
        pass

    
    def setJoinedToLazyChannel(self, cid, joined):
        pass

    
    def refreshChannelList(self):
        pass



class MessengerPageInterface(DispatcherProxyHolder):
    channels = property((lambda self: self._dispatcherProxy.channels))
    users = property((lambda self: self._dispatcherProxy.users))
    invites = property((lambda self: self._dispatcherProxy.invites))
    
    def format(self, message, playerIsTarget = False, system = False):
        '''
\t\tFormat message
\t\t'''
        return message.data

    
    def addMessage(self, message, format = True, playerIsTarget = False, system = False):
        pass

    
    def addSystemMessage(self, message):
        pass

    
    def addMember(self, member):
        '''
\t\tAdds member to message page
\t\t'''
        return True

    
    def addMembers(self, members):
        '''
\t\tAdds member to message page
\t\t'''
        return True

    
    def removeMember(self, uid):
        '''
\t\tRemove member from message page
\t\t@param uid: member id
\t\t'''
        return True

    
    def removeMembers(self, members):
        '''
\t\tRemove members from message page
\t\t@param members: member list
\t\t'''
        return True

    
    def setMemberStatus(self, uid, status):
        pass

    
    def open(self):
        pass

    
    def close(self):
        pass

    
    def clear(self):
        pass



class ProtocolPlugin(DispatcherProxyHolder):
    channels = property((lambda self: self._dispatcherProxy.channels))
    
    def connect(self):
        pass

    
    def disconnect(self):
        pass

    
    def broadcast(self, cid, message):
        return False



