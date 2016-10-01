#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    script for env PYTHONSTARTUP
"""
import os
import sys

import myterm
import myterm.color


myterm.color.COLOR_OUT = [myterm.FOREGROUND_INFO, myterm.BACKGROUND_INFO]
myterm.color.COLOR_IN = [myterm.FOREGROUND_WARNING, myterm.BACKGROUND_WARNING]
myterm.color.COLOR_ERR = [myterm.FOREGROUND_CRITICAL, myterm.BACKGROUND_CRITICAL]
myterm.color.COLOR_INFO = [myterm.FOREGROUND_DEFAULT, myterm.BACKGROUND_DEFAULT]



class PromptPs(object):
    """
        manage PromptPs
    """
    def __init__(self, prt):
        self._prt = prt
        self.count = 0

    def __str__(self):
        self.count = self.count + 1
        sys.stdout.prompt('%d%s' % (self.count, self._prt))
        return None


class PromptPsSpace(object):
    """
        manage space of PromptPs
    """
    def __init__(self, ps):
        self._ps = ps

    def __str__(self):
        return '.' * (len(str(self._ps.count)) + len(self._ps._prt))

sys.ps1 = PromptPs(' >>')
sys.ps2 = PromptPsSpace(sys.ps1)


class Cls(object):
    """
        clear Terminal
    """
    def __repr__(self):
        sys.ps1.count = 0
        os.system('cls' if os.name == 'nt' else 'clear')
        return ''

cls = Cls()


class Clear(object):
    """
        clear Terminal
    """
    def __repr__(self):
        sys.ps1.count = 0
        os.system('cls' if os.name == 'nt' else 'clear')
        return ''

clear = Clear()

# for linux
try:
    import readline
except ImportError:
    # print "Module readline not available."
    pass
else:
    try:
        # tabulation support
        import rlcompleter

        class TabCompleter(rlcompleter.Completer):
            """
                Completer that supports indenting
            """
            def complete(self, text, state):
                if not text:
                    return ('    ', None)[state]
                else:
                    return rlcompleter.Completer.complete(self, text, state)

        readline.set_completer(TabCompleter().complete)
        readline.parse_and_bind("tab: complete")
    except:
        pass
