# Source Generated with Decompyle++
# File: TmpConsoleCmds.pyc (Python 2.6)

import BigWorld
from debug_utils import *

class LanServers:
    
    def search(self):
        BigWorld.serverDiscovery.searching = 1

    
    def stop(self):
        BigWorld.serverDiscovery.searching = 0

    
    def show(self):
        for server in BigWorld.serverDiscovery.servers:
            print server
        

    
    def searchAndConnect(self, owner, user):
        self.search()
        self._LanServers__owner = owner
        self._LanServers__user = user
        BigWorld.serverDiscovery.changeNotifier = self._LanServers__checkIfFound

    
    def _LanServers__checkIfFound(self):
        for server in BigWorld.serverDiscovery.servers:
            if server.ownerName == self._LanServers__owner:
                self._LanServers__host = server.serverString
                del self._LanServers__owner
                self.stop()
                self._LanServers__login()
                break
                continue
        

    
    def _LanServers__login(self):
        
        class LoginInfo:
            pass

        login = LoginInfo()
        login.username = self._LanServers__user
        BigWorld.connect(self._LanServers__host, login, self._LanServers__progressFn)

    
    def _LanServers__progressFn(self, stage, status, serverMsg):
        print stage, status, serverMsg



def printPeriodTime():
    arena = BigWorld.player().arena
    print '%f / %f' % (arena.periodEndTime - BigWorld.serverTime(), arena.periodLength)


def printStatistics(byTotal = False, bots = True):
    statistics = BigWorld.player().arena.statistics
    teams = (None, [], [])
    for (name, team) in statistics.iteritems():
        stats = None
        if bots or not name.startswith('Bot'):
            teams[team].append((name, stats))
            continue
    
    if byTotal:
        pass
    1
    key = 'frags'
    teams[1].sort((lambda x, y: cmp(x[1]['key'], y[1]['key'])))
    teams[2].sort((lambda x, y: cmp(x[1]['key'], y[1]['key'])))
    for i in xrange(1, 3):
        print 'Team %d\n' % i
        for (name, stats) in teams[i]:
            print '%s\t%d\t%d' % (name, stats['frags'], stats['totalFrags'])
        
    


def printConst(module, prefix, value):
    mod = __import__(module)
    for c in dir(mod):
        if c.startswith(prefix) and getattr(mod, c) == value:
            print c
            return None
    
    print 'Not found'


