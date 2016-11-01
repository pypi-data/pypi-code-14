#!C:\Python27\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'u-cli==0.1.8','console_scripts','uclime'
__requires__ = 'u-cli==0.1.8'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('u-cli==0.1.8', 'console_scripts', 'uclime')()
    )
