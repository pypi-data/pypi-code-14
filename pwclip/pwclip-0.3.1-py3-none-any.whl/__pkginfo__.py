"""pwclip packaging information"""
import sys
from os import getcwd
from os.path import join, dirname

modname = distname = 'pwclip'
numversion = (0, 3, 1)
version = '.'.join([str(num) for num in numversion])
install_requires = ['pyusb', 'yubico', 'tkinter', 'gnupg']
if sys.version_info[:2] > (2, 7):
	install_requires = ['pyusb', 'yubico', 'gnupg']
license = 'GPL'
description = "gui to temporarily save passwords to clipboard (paste-buffer)"
web = 'http://janeiskla.de'
mailinglist = ""
author = 'Leon Pelzer'
author_email = 'mail@leonpelzer.de'
classifiers = ['Development Status :: 4 - Beta',
               'Environment :: Console',
               'Environment :: MacOS X',
               'Environment :: Win32 (MS Windows)',
               'Environment :: X11 Applications',
               'Intended Audience :: Developers',
               'Intended Audience :: End Users/Desktop',
               'Intended Audience :: System Administrators',
               'Intended Audience :: Information Technology',
               'License :: OSI Approved :: GNU General Public License (GPL)',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Programming Language :: Python :: 3',
               'Topic :: Security',
               'Topic :: Utilities',
               'Topic :: Desktop Environment',
               'Topic :: System :: Systems Administration']

with open(join(getcwd(), 'README'), 'r') as rfh:
	readme = rfh.read()

long_desc = ( readme )

scripts = [join('bin', 'pwclip')]

entry_points = {'console_scripts': ['pwclip = pwclip.__init__:pwclipper']}
