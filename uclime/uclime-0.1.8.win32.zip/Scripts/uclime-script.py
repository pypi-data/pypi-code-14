#!C:\Python27\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'uclime==0.1.8','console_scripts','uclime'
__requires__ = 'uclime==0.1.8'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('uclime==0.1.8', 'console_scripts', 'uclime')()
    )
