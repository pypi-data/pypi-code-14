#!/usr/bin/env python3
from orange import setup

console_scripts=['dos2unix=orange.path:dos2unix',
                 'pytest=orange.pytools:pytest',
                 'pysdist=orange.pytools:pysdist',
                 'pyupload=orange.pytools:pyupload',
                 'canshu=orange.ggcs:canshu',
                 #'mongodb=orange.mongodb:main',
                 'pyver=orange.pyver:main',
                 'plist=orange.plist:main',
                 'pyinit=orange.init:main',
                 'sysinit=orange.sysinit:proc']
setup(
        name='orange-kit',
        platforms='any',
        description='orange',
        long_description='orange',
        url='https://github.com/huangtao-sh/orange.git',
        entry_points={'console_scripts':console_scripts},
        license='GPL',
        )
