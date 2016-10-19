# templates.py
#
# part of modulenv
#
# Copyright (c) 2016 Sven E. Templer
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

def avail ():
    c = configs.keys()
    return sorted(c)

new = {
    
    'default' : '''
[module]
name = default
group = default
versions = 1.0
[prepends]
PATH = $modbin/bin
MANPATH = $modbin/share/man
INFOPATH = $modbin/share/man
LD_LIBRARY_PATH = $modbin/lib
'''

}

configs = {

    'R' : '''
[module]
    name = R
    group = lang
    versions = 2.15.3 3.3.1
[prepends]
    PATH = $modbin/bin
    LD_LIBRARY_PATH = $modbin/lib64
    MANPATH = $modbin/share/man
    INFOPATH = $modbin/share/man
[setenvs]
    R_LIBS = $modenv
    R_LIBS_USER = $modenv
    RSTUDIO_WHICH_R = $modbin/bin/R
''',

    'R-devel' : '''

[module]
    name = R-devel
    group = lang
    versions = 20160510
[prepends]
    PATH = $modbin/bin
    LD_LIBRARY_PATH = $modbin/lib64
    MANPATH = $modbin/share/man
    INFOPATH = $modbin/share/man
[setenvs]
    R_LIBS = $user
    R_LIBS_USER = $user
''',

     'python' : '''
[module]
    name = python
    group = lang
    versions = 2.7.12 3.5.2
[prepends]
    PATH = $modenv/bin:$modbin/bin
    MANPATH = $modbin/share/man
    INFOPATH = $modbin/share/man
[setenvs]
    PYTHONHOME = $modbin
    PYTHONPATH = $modbin
    PYTHONUSERBASE = $modenv
    JUPYER_RUNTIME_DIR = $modenv/jupyter/runtime
    RJUPYTER_DATA_DIR = $modenv/jupyter/rdata
''',

    'julia' : '''
[module]
    name = julia
    group = lang
    versions = 0.5.0
[prepends]
    PATH = $modbin/bin
    MANPATH = $modbin/share/man
    INFOPATH = $modbin/share/man
[setenvs]
    JULIA_PKGDIR = $modenv
''',

   'shellset' : '''
[module]
    name = shellset
    group = system
    versions = 0.4.1
    default = 0.4.1
    latest = 0.4.1
    depends = R
[prepends]
    PATH = $modbin/bin
    MANPATH = $modbin/share/man
    INFOPATH = $modbin/share/man
''',

    'slurm-tools' : '''
[module]
    name = slurm-tools
    group = system
    versions = 1.0.1
    depends = slurm
[prepends]
    PATH = $modbin/bin
    MANPATH = $modbin/share/man
    INFOPATH = $modbin/share/man
'''

}

### EOF
