#!python
# EASY-INSTALL-ENTRY-SCRIPT: 'Twisted==16.4.1','console_scripts','cftp'
__requires__ = 'Twisted==16.4.1'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('Twisted==16.4.1', 'console_scripts', 'cftp')()
    )
