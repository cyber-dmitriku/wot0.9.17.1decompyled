# Source Generated with Decompyle++
# File: exeptions.pyc (Python 2.6)

import exceptions

class ChannelNotFound(exceptions.Exception):
    
    def __init__(self, cid, *args, **kwargs):
        super(ChannelNotFound, self).__init__(*args, **args)
        self.cid = cid

    
    def __str__(self):
        return 'Not found a channel with id = %d, the first request from the server information on the channel with this id' % self.cid



