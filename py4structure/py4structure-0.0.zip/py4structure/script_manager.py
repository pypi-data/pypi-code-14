'''
--------------------------------------------------------------------------
Copyright (C) 2015-2016 Lukasz Laba <lukaszlab@o2.pl>

File version 0.6 date 2016-02-24

This file is part of py4Structure.
py4Structure is a range of free open source structural engineering design 
Python applications.
http://py4Structure.org/

py4Structure is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

py4Structure is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------
'''

import sys
import subprocess
import os
import time

import seepy

#seepy_path = vars(seepy)['__path__'][0] + '/SeePy.py'
#seepy_path = '/home/lukaszlab/Dropbox/PYAPPS_STRUCT/SOURCE_SEEPY/seepy/SeePy.py'
seepy_path ='C:\Users\luka\Dropbox\PYAPPS_STRUCT\SOURCE_SEEPY\seepy\SeePy.py'

class Manager() :
    def __init__(self):
        self.package_dir = os.path.split(__file__)[0]
        self.script_dir = os.path.join(self.package_dir, 'scripts')
        self.script_list = self.get_script_list()

    def get_script_list(self):
        list = []
        for fname in os.listdir(self.script_dir):
            if 'see.py' in fname:
                list.append(fname)
        return list
        
    def run_some_script(self, scriptname):
        if scriptname in self.script_list:
            script_path = os.path.join(self.script_dir, scriptname)
            subprocess.Popen(['python', seepy_path, script_path, '-l'])
        else:
            print '!! ' + scriptname + ' not find in ' + self.script_dirse + ' !!'

script_maneger = Manager()

if __name__ == "__main__":
    manager = Manager()
    print manager.get_script_list()
    manager.run_some_script(manager.script_list[1])
    #manager.run_some_script('dsdsd')
    
    
