# environment.py
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

import os
import shutil
import time
import modulenv.utils as utl
import modulenv.templates as tmp
import modulenv.files as mf
from modulenv.module import Module

class Environment ( ):

    def __init__ ( self, path = '.' ):
        self.prefix = path
        self.exists = os.path.exists(path)
        self.empty = False if self.exists and len(os.listdir(path)) > 0 else True
        self.modules = set()
        if self.exists:
            self.prefix = utl.pathnorm(path)
            self._scan()

    def __contains__( self, mod ):
        if not isinstance(mod, Module):
            utl.quit('can only search for Module in Environment')
        return mod.name() in self.names()
        # n = mod['module']['name']
        # g = mod['module']['group']
        # return n in self.modules and g == self.modules[n]['group']

    def _scan ( self ):
        d0 = os.path.join(self.prefix, 'mod/')
        groups = utl.pathtree(d0, level = 1, incdir = True, incfile = False, absolute = False)
        #modules = set()
        for group in groups:
            d1 = os.path.join(d0, group)
            names = utl.pathtree(d1, level = 1, incdir = True, incfile = False, absolute = False)
            for name in names:
                m = Module()
                m.read_dir(os.path.join(d1, name))
                self.modules.add(m)
                #modules[name] = m
        #self.modules = modules
        return

    def valid ( self ):
        ls = os.listdir(self.prefix)
        full = ['mod', 'env', 'bin', 'src', 'log']
        v = all( i in full for i in ls ) # and all( i in ls for i in full)
        # todo: check type of ls (dir, file)
        return v

    def groups ( self ):
        return sorted(set([ m.group() for m in self.modules ]))

    def names ( self ):
        return sorted(set([ m.name() for m in self.modules ]))

    def fullnames ( self, versions = False ):
        return sorted(set([ m.fullname(versions = versions) for m in self.modules ]))

    def init ( self, bindir = None, envdir = None, home = None, clear = True, cmd = None ):
        if not self.exists:
            os.makedirs(self.prefix)
            self.prefix = utl.pathnorm(self.prefix)
        else:
            if not self.empty:
                utl.quit('directory not emtpy: ' + self.prefix)
        dirs = { 'bin' : bindir, 'env' : envdir, 'mod' : None }
        for target, source in dirs.items():
            target = os.path.join(self.prefix, target)
            if source is None:
                os.makedirs(target)
            else:
                source = utl.pathnorm(source)
                os.symlink(source, target)
        # todo: expand log message to arguments
        # .rc file
        fpath = os.path.join(self.prefix, 'src')
        if not home:
            home = os.getenv('MODULESHOME')
        if not home or not os.path.exists(home):
            utl.quit('MODULESHOME unset or path not existing: ' + str(home))
        if clear:
            clear = 'unset MODULEPATH'
        else:
            clear = ''
        if not cmd:
            search = [ '/bin/modulecmd', '/usr/bin/modulecmd', '/usr/local/bin/modulecmd',
                    '/usr/local/opt/modules/Modules/bin/modulecmd' ]
            for f in search:
                if os.path.exists(f):
                    cmd = f
                    break
        if not cmd or not os.path.exists(cmd):
            utl.quit('could not find modulecmd')
        d = { 'home' : home, 'clear' : clear, 'prefix' : self.prefix, 'cmd' : cmd }
        f = open(fpath, 'w')
        f.write(mf.rc.format(d))
        f.close()
        return

    def show ( self ):
        print('  * module environment: ' + self.prefix)
        for name in self.fullnames(versions = True):
            print('    - ' + name)
        return

    def add ( self, mod, bin = None, force = False ):
        mpath = os.path.join(self.prefix, 'mod', mod.group(), mod.name())
        # force clean
        if os.path.exists(mpath):
            if force:
                shutil.rmtree(mpath)
            else:
                utl.quit('path ' + mpath + ' exists')
        # create directories
        os.makedirs(mpath)
        for v in mod.versions():
            if v == 'latest':
                utl.warn('version name latest ignored')
                continue
            p = os.path.join(self.prefix, 'env', mod.group(), mod.name(), v)
            if not os.path.exists(p):
                os.makedirs(p)
        # write versions
        mod.write(mpath, self.prefix)
        self.modules.add(mod)
        return

    def rm ( self, name ):
        drop = set()
        keep = set()
        for m in self.modules:
            if name == m.name():
                drop.add(m)
            else:
                keep.add(m)
        for m in drop:
            mpath = os.path.join(self.prefix, 'mod', m.fullname())
            shutil.rmtree(mpath)
            print('  * removed ' + m.fullname(versions = True))
        self.modules = keep
        return

