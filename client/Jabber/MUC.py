# Source Generated with Decompyle++
# File: MUC.pyc (Python 2.6)

import xmpp.Entities as XMPPEntities
import xmpp.Stanzas as XMPPStanzas
from xmpp.Stanzas import getAttr, getChild, jidAttr
from wotdecorators import noexcept

class MUC(XMPPEntities.MUC):
    
    def __init__(self, room):
        XMPPEntities.MUC.__init__(self, room, room)

    
    def sendMessage(self, uMessage):
        if self.connection:
            self.connection.sendStanza(XMPPStanzas.mucMessage(self.connection.jid, self.room_jid, XMPPStanzas.xmlText(uMessage)))
            return True
        return False

    sendMessage = noexcept(sendMessage)
    
    def onConnected(self):
        to = self.room_jid + u'/' + self.connection.credentials[0]
        self.connection.sendStanza(XMPPStanzas.mucPresence(self.connection.jid, to))

    
    def onStanza(self, stanza):
        XMPPEntities.MUC.onStanza(self, stanza)
        stanzaName = stanza['name']
        if stanzaName == 'message':
            self._MUC__onStanzaMessage(stanza)
        elif stanzaName == 'presence':
            self._MUC__onStanzaPresence(stanza)
        elif stanzaName == 'iq':
            self._MUC__onStanzaInfoQuery(stanza)
        

    
    def _MUC__onStanzaMessage(self, stanza):
        from_jid = getAttr(stanza, 'from').encode('utf-8')
        user = jidAttr(from_jid, 'muc_user')
        messageType = getAttr(stanza, 'type')
        if messageType == 'error':
            return None
        body = getChild(stanza, 'body')
        if not body:
            return None
        self.eventMessage(user, body['data'].encode('utf-8'))

    
    def _MUC__onStanzaPresence(self, stanza):
        from_jid = getAttr(stanza, 'from').encode('utf8')
        user = jidAttr(from_jid, 'muc_user')
        presenceType = getAttr(stanza, 'type')
        if not presenceType:
            presenceType = 'available'
        
        if presenceType == 'unavailable':
            pass
        1
        self.eventUserOnline(user)

    
    def _MUC__onStanzaInfoQuery(self, stanza):
        pass



