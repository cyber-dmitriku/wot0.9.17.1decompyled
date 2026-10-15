# Source Generated with Decompyle++
# File: JoinedChannelsInterface.pyc (Python 2.6)

from account_helpers.AccountSettings import AccountSettings
from gui.Scaleform.CommandArgsParser import CommandArgsParser
from messenger.gui.interfaces import DispatcherProxyHolder
from messenger.gui.Scalefrom import JCH_COMMANDS
from messenger import LAZY_CHANNELS

class JoinedChannelsInterface(DispatcherProxyHolder):
    
    def __init__(self):
        self._JoinedChannelsInterface__movieViewHandler = None
        self._JoinedChannelsInterface__waitActivationChannels = []
        self._JoinedChannelsInterface__sortedChList = []
        self._JoinedChannelsInterface__isPopulated = False

    
    def channelsManager(self):
        return self._dispatcherProxy.channels

    channelsManager = property(channelsManager)
    
    def populateUI(self, movieViewHandler):
        self._JoinedChannelsInterface__movieViewHandler = movieViewHandler
        self._JoinedChannelsInterface__isPopulated = True
        self.channelsManager.onChannelRefresh += self._JoinedChannelsInterface__onChannelRefresh
        self._JoinedChannelsInterface__buildChannelList()
        self._JoinedChannelsInterface__movieViewHandler.addExternalCallbacks({
            JCH_COMMANDS.RequestLength(): self.onRequestChannelsLength,
            JCH_COMMANDS.RequestItemRange(): self.onRequestChannelsItems,
            JCH_COMMANDS.WaitActivation(): self.onWaitChannelActivation,
            JCH_COMMANDS.ChannelActivated(): self.onChannelActivated,
            JCH_COMMANDS.LeaveChannel(): self.onLeaveChannel,
            JCH_COMMANDS.RequestChannelData(): self.onRequestChannelData })

    
    def dispossessUI(self):
        if not self._JoinedChannelsInterface__isPopulated:
            return None
        self.clear()
        self.channelsManager.onChannelRefresh -= self._JoinedChannelsInterface__onChannelRefresh
        self._JoinedChannelsInterface__movieViewHandler.removeExternalCallbacks(JCH_COMMANDS.RequestLength(), JCH_COMMANDS.RequestItemRange(), JCH_COMMANDS.WaitActivation(), JCH_COMMANDS.ChannelActivated(), JCH_COMMANDS.LeaveChannel(), JCH_COMMANDS.RequestChannelData())
        self._JoinedChannelsInterface__movieViewHandler = None
        self._JoinedChannelsInterface__isPopulated = False

    
    def updateChannelWrappers(self):
        self.channelsManager.updateChannelWrappers()

    
    def refresh(self):
        if self._JoinedChannelsInterface__isPopulated:
            self._JoinedChannelsInterface__buildChannelList()
            self._JoinedChannelsInterface__movieViewHandler.call(JCH_COMMANDS.RefreshList(), [
                len(self._JoinedChannelsInterface__sortedChList)])
        

    
    def remove(self, cid):
        if self._JoinedChannelsInterface__isPopulated:
            self._JoinedChannelsInterface__buildChannelList()
            self._JoinedChannelsInterface__movieViewHandler.call(JCH_COMMANDS.RemoveChannel(), [
                int(cid)])
        

    
    def clear(self):
        self._JoinedChannelsInterface__sortedChList = []
        if self._JoinedChannelsInterface__isPopulated:
            self._JoinedChannelsInterface__movieViewHandler.call(JCH_COMMANDS.ClearList())
        

    
    def waiting(self, cid):
        if cid not in self._JoinedChannelsInterface__waitActivationChannels:
            self._JoinedChannelsInterface__waitActivationChannels.append(cid)
        

    
    def _JoinedChannelsInterface__comparator(self, channel, other):
        if channel.lazy | other.lazy:
            if channel.lazy != 0 and other.lazy != 0:
                result = cmp(LAZY_CHANNELS.ORDERS.get(channel.lazy, -1), LAZY_CHANNELS.ORDERS.get(other.lazy, -1))
            elif channel.lazy != 0:
                pass
            
            result = 1
        elif channel.isSystem ^ other.isSystem:
            if channel.isSystem:
                pass
            1
            result = 1
        else:
            result = cmp(channel.joinedTime, other.joinedTime)
        return result

    
    def _JoinedChannelsInterface__buildChannelList(self):
        self._JoinedChannelsInterface__sortedChList = sorted(self.channelsManager.getChannelList(lazy = True), cmp = self._JoinedChannelsInterface__comparator)
        ids = map((lambda channel: channel.cid), self._JoinedChannelsInterface__sortedChList)
        self._JoinedChannelsInterface__waitActivationChannels = (filter,)((lambda cid: cid in ids), self._JoinedChannelsInterface__waitActivationChannels)

    
    def _JoinedChannelsInterface__onChannelRefresh(self, channel):
        self._JoinedChannelsInterface__movieViewHandler.call(JCH_COMMANDS.GhangeChannelName(), [
            channel.cid,
            channel.channelNameCensored])

    
    def onRequestChannelsLength(self, *args):
        parser = CommandArgsParser(self.onRequestChannelsLength.__name__)
        parser.parse(*args)
        parser.addArg(len(self._JoinedChannelsInterface__sortedChList))
        self._JoinedChannelsInterface__movieViewHandler.respond(parser.args())

    
    def onRequestChannelsItems(self, *args):
        parser = CommandArgsParser(self.onRequestChannelsItems.__name__, 2, [
            int,
            int])
        (startIndex, endIndex) = parser.parse(*args)
        for item in self._JoinedChannelsInterface__sortedChList[startIndex:endIndex + 1]:
            parser.addArgs(item)
            if item.cid in self._JoinedChannelsInterface__waitActivationChannels:
                pass
            1
            True(False)
        
        self._JoinedChannelsInterface__movieViewHandler.respond(parser.args())

    
    def onWaitChannelActivation(self, *args):
        parser = CommandArgsParser(self.onWaitChannelActivation.__name__, 1, [
            long])
        (cid,) = parser.parse(*args)
        if cid not in self._JoinedChannelsInterface__waitActivationChannels:
            self._JoinedChannelsInterface__waitActivationChannels.append(cid)
        

    
    def onChannelActivated(self, *args):
        parser = CommandArgsParser(self.onChannelActivated.__name__, 1, [
            long])
        (cid,) = parser.parse(*args)
        if cid in self._JoinedChannelsInterface__waitActivationChannels:
            self._JoinedChannelsInterface__waitActivationChannels.remove(cid)
        

    
    def onLeaveChannel(self, *args):
        parser = CommandArgsParser(self.onLeaveChannel.__name__, 1, [
            long])
        (cid,) = parser.parse(*args)
        self.channelsManager.exitFromChannel(cid)

    
    def onRequestChannelData(self, *args):
        parser = CommandArgsParser(self.onRequestChannelData.__name__, 1, [
            long])
        (cid,) = parser.parse(*args)
        idx = None
        channel = None
        for (idx, item) in enumerate(self._JoinedChannelsInterface__sortedChList):
            if item.cid == cid:
                channel = item
                break
                continue
        
        if channel is not None:
            parser.addArg(idx)
            parser.addArgs(channel)
            self._JoinedChannelsInterface__movieViewHandler.respond(parser.args())
        



