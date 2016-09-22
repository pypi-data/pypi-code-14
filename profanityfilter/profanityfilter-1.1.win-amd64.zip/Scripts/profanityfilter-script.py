#!C:\Python35\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'profanityfilter==1.1','console_scripts','profanityfilter'
__requires__ = 'profanityfilter==1.1'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('profanityfilter==1.1', 'console_scripts', 'profanityfilter')()
    )
