# files.py
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

rc = '''# modulenv rc file

{0[clear]}

export MODULESHOME="{0[home]}"
export MODULENV_CMD="{0[cmd]}"
export MODULENV_PREFIX="{0[prefix]}"
export MODULENV_SHELL="`ps -p $$ -ocomm= | tr -d '-'`"

module () {{ eval `$MODULENV_CMD $MODULENV_SHELL $*`; }}

if [ "${{LOADEDMODULES:-}}" = "" ]
then
    LOADEDMODULES=
    export LOADEDMODULES
fi

for dir in `ls -d $MODULENV_PREFIX/mod/* 2>/dev/null`
do
    if [ -z "${{MODULEPATH}}" ]
    then
        export MODULEPATH="$dir"
    else
        export MODULEPATH="$dir:$MODULEPATH"
    fi
done

if [ "$MODULENV_SHELL" = "bash" ] && [ ${{BASH_VERSINFO:-0}} -ge 3 ] && [ -r $MODULESHOME/init/bash_completion ]
then
    source $MODULESHOME/init/bash_completion
fi

#EOF
'''

module = '''\
#%Module1.0#####################################################################

# variables
set home $::env(HOME)
set name {0[name]}
set version {0[version]}
set prefix {0[prefix]}
set modbin $prefix/bin/$name/$version
set modenv $prefix/env/$name/$version
set about "$name version $version"

# conflict
conflict $name

# depends
{0[depends]}

# paths
{0[prepends]}

# environment
{0[setenvs]}

# help
proc ModulesHelp {{ }} {{
        global version
        puts stderr "\n\t$about\n"
}}
module-whatis   "$about"

#EOF
'''

version = '''\
#%Module1.0#####################################################################
# default version
set ModulesVersion "{0[default]}"
#EOF
'''

