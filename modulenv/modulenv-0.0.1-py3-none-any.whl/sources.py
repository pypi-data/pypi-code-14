# sources.py
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

urls = { 
    'R' :        [ 'ftp://stat.ethz.ch/CRAN/src/base/R-2/',
                   'ftp://stat.ethz.ch/CRAN/src/base/R-3/' ],
    'python' :   [ 'https://www.python.org/ftp/python/' ],
    'shellset' : [ 'https://api.github.com/repos/setempler/shellset/tags' ],
    'julia' :    [ 'https://api.github.com/repos/JuliaLang/julia/tags' ]
    }

versions = { 
    'R' :        '',
    'python' :   'https://www.python.org/ftp/python/',
    'shellset' : 'https://api.github.com/repos/setempler/shellset/tags',
    'julia' :    'https://api.github.com/repos/JuliaLang/julia/tags'
    }


installer = {

    'R' : '''\
#!/bin/bash
VERSION=S{1}
PREFIX=${2}
cd $PREFIX
mkdir -p src
v=$(curl -s ftp://stat.ethz.ch/CRAN/src/base/R-{2,3}/ | \
		grep -o "[0-9]\.[0-9]\.[0-9]" | \
		sort -u | \
		xargs echo)
[[ "$v" = *${VERSION}* ]] && echo latest=$VERSION || exit


opt=$HOME/opt/bin
v=3.3.1
# or latest
v=$(curl -s ftp://stat.ethz.ch/CRAN/src/base/ | grep latest | egrep -o "\d+\.\d+\.\d+")
mkdir -p $opt/R
cd $opt/R
curl -# -o src-${v}.tar.gz ftp://stat.ethz.ch/CRAN/src/base/R-${v%%.*}/R-${v}.tar.gz
# or latest
curl -# -o src-${v}.tar.gz ftp://stat.ethz.ch/CRAN/src/base/R-latest.tar.gz
mkdir -p tmp
tar xf src-${v}.tar.gz -C tmp #--strip-components 1
mv tmp/R-$v src-${v}
cd src-$v
# if homebrew on OSX is installed to not default prefix
CPPFLAGS="-I$(brew --prefix)/include" \
    PKG_CONFIG_PATH="$(brew --prefix)/lib/pkgconfig" \
    LDFLAGS="-L$(brew --prefix)/lib" \
    ./configure --prefix=$opt/R/$v --enable-R-shlib --with-recommended-packages=no --with-x=no
make
make install
#    --with-cairo --with-libpng --with-libtiff --with-jpeglib  --with-x=no
# OSX RStudio:
#R_LIBS=$HOME/opt/env/R/3.3.1 \
#    R_LIBS_USER=$HOME/opt/env/R/3.3.1  \
#    RSTUDIO_WHICH_R=$HOME/opt/bin/R/3.3.1/bin/R \
#    open /Applications/RStudio.app
''',

    'R-devel' : '''\
#!/bin/bash

# R-devel
opt=
day=$(date +%Y%m%d)
v=devel-$day
mkdir -p $opt/R/{,source-}$v
cd $opt/R
curl -# -o source-${v}.tar.gz ftp://stat.ethz.ch/R/R-devel.tar.gz
tar xf source-${v}.tar.gz -C source-$v --strip-components 1
cd source-$v
./configure --prefix=$opt/R/$v --with-x=no --enable-R-shlib --with-recommended-packages=no
make
make install
''',

     'python' : '''\
#!/bin/bash

# python
opt=$HOME/opt/bin/python
# show latest:
curl -s https://www.python.org/ftp/python/ | \
    egrep -o '>[0-9]\.[\.0-9]+' | tr -d '>' | gsort -V
v=3.5.2
v=2.7.11
opt=$opt/$v
mkdir -p $opt
cd $opt
curl -o src-$v.tgz https://www.python.org/ftp/python/$v/Python-$v.tgz
tar xf src-$v.tgz
mv Python-$v src-$v
cd src-$v
CPPFLAGS=-I$(brew --prefix openssl)/include \
LDFLAGS=-L$(brew --prefix openssl)/lib \
./configure --prefix=$opt
make
make install
cd $v/bin
ln -s python3 python
ln -s pip3 pip
ln -s pydoc3 pydoc
ln -s idle3 idle
ln -s python3-config python-config
#ln -s pyvenv-3.5 pyvenv
''',

   'julia' : '''\
#!/bin/bash

# julia
opt=
v=0.4.5
mkdir -p $opt/julia/{$v,source-github}
cd $opt/julia
git clone git@github.com:JuliaLang/julia.git source-github
cd source-github
git checkout v$v
make clean #?
make -j 2
cp -a usr/* $opt/julia/$v
''',

    'rsync' : '''\
#!/bin/bash

# rsync
opt=
v=3.1.2
mkdir -p $opt/rsync/{,source-}$v
cd $opt/rsync
curl -# -o source-${v}.tar.gz https://download.samba.org/pub/rsync/src/rsync-${v}.tar.gz
tar xf source-${v}.tar.gz -C source-$v --strip-components 1
cd source-$v
./configure --prefix=$opt/rsync/$v
make
make install
''',

    'shellset' : '''\
#!/bin/bash

# shellset
opt=
mkdir -o $opt/shellset
cd $opt/shellset
git clone https://github.com/setempler/shellset source-git
cd source-git
# edit 'prefix' in config.mk
# checkout version
make
make install
''',

    'slurm-tools' : '''\
#!/bin/bash

# shellset
opt=$HOME/opt
mkdir -o $opt/slurm-tools
cd $opt/slurm-tools
git clone git@bitbucket.org:setempler/slurm-tools
cd slurm-tools
git checkout 1.0.1
install $opt/slurm-tools/1.0.1
''',

    'vim' : '''\
#!/bin/bash

# vim
opt=
git clone https://github.com/vim/vim.git
cd vim
# git tag
# v=... # v7.4.1989
configure --prefix=$opt/vim/$v
cd src
make
make install
''',

    'zsh' : '''\
#!/bin/bash

# zsh
opt=
git clone git://git.code.sf.net/p/zsh/code ~/src/zsh
cd ~/src/zsh
mkdir -p ~/opt/zsh/5.2-dev-1_commit-062aeca
Util/preconfig # requires autoconf
./configure --prefix=$HOME/opt/zsh/5.2-dev-1_commit-062aeca
make -j 6
make install
'''

}


