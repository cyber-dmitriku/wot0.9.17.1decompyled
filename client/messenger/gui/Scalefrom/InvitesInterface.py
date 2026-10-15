# Source Generated with Decompyle++
# File: InvitesInterface.pyc (Python 2.6)

from account_helpers.AccountPrebattle import AccountPrebattle
import BigWorld
from constants import IS_DEVELOPMENT
from debug_utils import LOG_WARNING, LOG_DEBUG
from gui.Scaleform.CommandArgsParser import CommandArgsParser
from messenger.gui.interfaces import DispatcherProxyHolder
from messenger.gui.Scalefrom import INV_COMMANDS
from PlayerEvents import g_playerEvents
from debug_utils import LOG_CURRENT_EXCEPTION

class InvitesInterface(DispatcherProxyHolder):
    
    def __init__(self):
        self._InvitesInterface__movieViewHandler = None
        self._InvitesInterface__joinArgs = tuple()

    
    def invitesManager(self):
        return self._dispatcherProxy.invites

    invitesManager = property(invitesManager)
    
    def populateUI(self, movieViewHandler):
        self._InvitesInterface__movieViewHandler = movieViewHandler
        self.invitesManager.onReceivedInviteListInited += self._InvitesInterface__pim_onReceivedInviteListInited
        self.invitesManager.onReceivedInviteListModified += self._InvitesInterface__pim_onReceivedInviteListModified
        self._InvitesInterface__movieViewHandler.addExternalCallbacks({
            INV_COMMANDS.GetReceivedInvite(): self.onGetReceivedInvite,
            INV_COMMANDS.RequestList(): self.onRequestReceivedInviteList,
            INV_COMMANDS.AcceptInvite(): self.onAcceptInvite,
            INV_COMMANDS.RejectInvite(): self.onRejectInvite,
            INV_COMMANDS.LeftPrbAndAcceptInvite(): self.onLeftPrebattleAndAcceptInvite,
            INV_COMMANDS.RequestUnreadCount(): self.onRequestUnreadCount,
            INV_COMMANDS.ClearUnreadCount(): self.onClearUnreadCount })

    
    def dispossessUI(self):
        self.clear()
        self.invitesManager.onReceivedInviteListInited -= self._InvitesInterface__pim_onReceivedInviteListInited
        self.invitesManager.onReceivedInviteListModified -= self._InvitesInterface__pim_onReceivedInviteListModified
        self._InvitesInterface__movieViewHandler.removeExternalCallbacks(INV_COMMANDS.GetReceivedInvite(), INV_COMMANDS.RequestList(), INV_COMMANDS.AcceptInvite(), INV_COMMANDS.RejectInvite(), INV_COMMANDS.LeftPrbAndAcceptInvite(), INV_COMMANDS.RequestUnreadCount(), INV_COMMANDS.ClearUnreadCount())
        self._InvitesInterface__movieViewHandler = None

    
    def clear(self):
        if self._InvitesInterface__movieViewHandler:
            self._InvitesInterface__movieViewHandler.call(INV_COMMANDS.ClearData())
        

    
    def _InvitesInterface__comparator(self, data, other):
        return cmp(data[0].createTime, other[0].createTime)

    
    def _InvitesInterface__pim_onReceivedInviteListInited(self):
        self._InvitesInterface__movieViewHandler.call(INV_COMMANDS.RefreshList(), [
            self.invitesManager.getUnreadCount()])

    
    def _InvitesInterface__pim_onReceivedInviteListModified(self, added, changed, deleted):
        hasNew = len(added) > 0
        
        try:
            BigWorld.WGWindowsNotifier.onInvitation()
        except:
            LOG_CURRENT_EXCEPTION()

        if hasNew and not len(changed) and not len(deleted):
            invites = self.invitesManager.getReceivedInvites(added)
            invites = sorted(invites, cmp = self._InvitesInterface__comparator)
            links = map((lambda item: item[1]), invites)
            self._InvitesInterface__movieViewHandler.call(INV_COMMANDS.ReceiveInvites(), [
                '\n'.join(links)])
        else:
            self._InvitesInterface__movieViewHandler.call(INV_COMMANDS.RefreshList(), [
                self.invitesManager.getUnreadCount()])
            if len(deleted):
                self._InvitesInterface__movieViewHandler.call(INV_COMMANDS.DeletedInvites(), deleted)
            
            if len(changed):
                self._InvitesInterface__movieViewHandler.call(INV_COMMANDS.ChangedInvites(), changed)
            

    
    def onGetReceivedInvite(self, *args):
        parser = CommandArgsParser(self.onGetReceivedInvite.__name__, 1, [
            int])
        (inviteID,) = parser.parse(*args)
        (invite, _) = self.invitesManager.getReceivedInvite(inviteID)
        if invite:
            formatter = self.invitesManager.formatter
            parser.addArgs([
                int(invite.id),
                formatter.title(invite),
                formatter.format(invite),
                invite.comment,
                invite.opFlags()])
            self._InvitesInterface__movieViewHandler.respond(parser.args())
        elif IS_DEVELOPMENT:
            LOG_WARNING('Not found invite with id = %d' % inviteID)
        

    
    def onRequestReceivedInviteList(self, *args):
        parser = CommandArgsParser(self.onRequestReceivedInviteList.__name__)
        parser.parse(*args)
        invites = self.invitesManager.getReceivedInvites()
        invites = sorted(invites, cmp = self._InvitesInterface__comparator)
        links = map((lambda item: item[1]), invites)
        parser.addArg('\n'.join(links))
        self._InvitesInterface__movieViewHandler.respond(parser.args())

    
    def onAcceptInvite(self, *args):
        parser = CommandArgsParser(self.onAcceptInvite.__name__, 1, [
            int])
        (inviteID,) = parser.parse(*args)
        if inviteID:
            if AccountPrebattle.get():
                dialog = 'leftPrebattleAndAcceptInvite'
                if AccountPrebattle.isTraining():
                    dialog = 'leftTrainingAndAcceptInvite'
                elif AccountPrebattle.isSquad():
                    dialog = 'leftSquadAndAcceptInvite'
                elif AccountPrebattle.isCompany():
                    dialog = 'leftTeamAndAcceptInvite'
                
                self._InvitesInterface__movieViewHandler.call(INV_COMMANDS.CloseReceivedInviteWindow(), [
                    int(inviteID)])
                self._InvitesInterface__movieViewHandler.call('common.showMessageDialog', [
                    dialog,
                    True,
                    True,
                    None,
                    INV_COMMANDS.LeftPrbAndAcceptInvite(),
                    inviteID])
                return None
            if BigWorld.player().isInQueue:
                self._InvitesInterface__movieViewHandler.call('common.showMessageDialog', [
                    'cancelInvite',
                    True,
                    False])
                return None
            isCaptchaRequired = True
            captcha = self._InvitesInterface__movieViewHandler.captcha
            if isCaptchaRequired and captcha.isCaptchaRequired():
                (BigWorld.player().isInQueue, captcha.showCaptcha)((lambda : self._InvitesInterface__doAcceptInvite(inviteID)))
            else:
                self._InvitesInterface__doAcceptInvite(inviteID)
        

    
    def _InvitesInterface__doAcceptInvite(self, inviteID):
        self.invitesManager.acceptInvite(inviteID)

    
    def onRejectInvite(self, *args):
        parser = CommandArgsParser(self.onRejectInvite.__name__, 1, [
            int])
        (inviteID,) = parser.parse(*args)
        if inviteID:
            self.invitesManager.declineInvite(inviteID)
        

    
    def onRequestUnreadCount(self, *args):
        parser = CommandArgsParser(self.onRequestUnreadCount.__name__)
        parser.parse(*args)
        parser.addArg(self.invitesManager.getUnreadCount())
        self._InvitesInterface__movieViewHandler.respond(parser.args())

    
    def onClearUnreadCount(self, *args):
        self.invitesManager.resetUnreadCount()

    
    def onLeftPrebattleAndAcceptInvite(self, *args):
        self._InvitesInterface__joinArgs = args
        g_playerEvents.onPrebattleLeft += self._InvitesInterface__pe_onPrebattleLeft
        BigWorld.player().prb_leave(self._InvitesInterface__cb_onPrbLeft)

    
    def _InvitesInterface__cb_onPrbLeft(self, code):
        if code < 0:
            LOG_WARNING('Error to leave prebattle code: %s' % code)
            g_playerEvents.onPrebattleLeft -= self._InvitesInterface__pe_onPrebattleLeft
            self._InvitesInterface__joinArgs = tuple()
        

    
    def _InvitesInterface__pe_onPrebattleLeft(self):
        g_playerEvents.onPrebattleLeft -= self._InvitesInterface__pe_onPrebattleLeft
        if self._InvitesInterface__joinArgs:
            self.onAcceptInvite(*self._InvitesInterface__joinArgs)
            self._InvitesInterface__joinArgs = tuple()
        



