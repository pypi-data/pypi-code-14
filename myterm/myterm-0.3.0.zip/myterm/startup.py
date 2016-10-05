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
    def __init__(self, prt, env):
        self._prt = prt
        self._env = env
        self.count = 0

    def __str__(self):
        self.count = self.count + 1
        sys.stdout.prompt('%s%d%s' % (self._env, self.count, self._prt))
        return None


class PromptPsSpace(object):
    """
        manage space of PromptPs
    """
    def __init__(self, ps, env):
        self._ps = ps
        self._env = env

    def __str__(self):
        return self._env + '.' * (len(str(self._ps.count)) + len(self._ps._prt))

# Environnement virtuel
env = os.environ.get('VIRTUAL_ENV')
if env:
    env_name = '(%s) ' % os.path.basename(env)
    print("\nVirtualenv '{}' contains:".format(env_name))
    print(', '.join(sorted([dist.project_name for dist in pip.get_installed_distributions()])) + '\n')
else:
    env_name = ''
     
sys.ps1 = PromptPs(' >>', env_name)
sys.ps2 = PromptPsSpace(sys.ps1, env_name)


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
