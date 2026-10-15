# Source Generated with Decompyle++
# File: __init__.pyc (Python 2.6)


class TutorialProxyHolder(object):
    _tutorial = None
    
    def _gui(self):
        return self._tutorial._gui

    _gui = property(_gui)


def setTutorialProxy(tutorial):
    TutorialProxyHolder._tutorial = tutorial


def clearTutorialProxy():
    TutorialProxyHolder._tutorial = None


