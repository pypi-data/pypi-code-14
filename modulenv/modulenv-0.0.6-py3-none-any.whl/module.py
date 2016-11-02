# module.py
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
import configparser
import modulenv.utils as utl
import modulenv.templates as tmp
import modulenv.files as mf

class Module ( ):

    def __init__ ( self ):
        self.config = {
                'module' :   {
                    'name' :     '',
                    'group' :    '',
                    'versions' : [],
                    'default' :  '',
                    'latest' :   '',
                    'depends' :  [] },
                'prepends' : {},
                'setenvs' :  {} }
        self.section_order = ['module', 'prepends', 'setenvs']
        self.module_order  = ['name', 'group', 'versions', 'default', 'latest', 'depends']

    def reset ( self ):
        self.__init__()

    def valid (self, verbose = False, show = False, quit = False):
        # todo: error if name in depends to avoid self-loading which is not checked by module
        msg = []
        valid = True
        c = self.config
        if not 'module' in c:
            msg.append('error: missing section module')
            valid = False
        else:
            if not c['module']['group']:
                msg.append('error: missing module/group')
                valid = False
            if not c['module']['versions']:
                msg.append('error: missing module/versions')
                valid = False
            if not c['module']['latest']:
                msg.append('note: no latest version defined')
            else:
                if not c['module']['latest'] in c['module']['versions']:
                    msg.append('error: latest version not in versions')
                    valid = False
            if not c['module']['default']:
                msg.append('warning: no default version defined')
            else:
                if c['module']['default'] == 'latest':
                    if not c['module']['latest']:
                        msg.append('error: default version is latest, which is not defined')
                        valid = False
                elif not c['module']['default'] in c['module']['versions']:
                    msg.append('error: default version not in versions')
                    valid = False
            if not c['module']['depends']:
                msg.append('note: no depends defined')
        if not c['prepends']:
            msg.append('note: no prepend-path')
        if not c['setenvs']:
            msg.append('note: no setenv')
        msg.append('validity ' + ('OK' if valid else 'ERROR'))
        if verbose:
            print('  * ' + '\n  * '.join(msg))
        if show:
            print('  * content:\n')
            self.show()
        if quit and not valid:
            utl.quit('invalid module config')
        return valid

    def name ( self, setvalue = None ):
        if not setvalue:
            return self.config['module']['name']
        self.config['module']['name'] = str(setvalue)

    def group ( self, setvalue = None ):
        if not setvalue:
            return self.config['module']['group']
        self.config['module']['group'] = str(setvalue)

    def versions ( self, setvalue = None, getstring = False ):
        if not setvalue and getstring:
            return ' '.join(list(sorted(set(self.config['module']['versions']))))
        if not setvalue:
            return list(sorted(set(self.config['module']['versions'])))
        if isinstance(setvalue, list):
            self.config['module']['versions'] = list(set(setvalue))
        elif isinstance(setvalue, str):
            self.config['module']['versions'] = list(set(setvalue.split(' ')))
        else:
            utl.quit('Module.versions accepts only list or string')

    def latest ( self, setvalue = None ):
        if not setvalue:
            return self.config['module']['latest']
        self.config['module']['latest'] = str(setvalue)

    def default ( self, setvalue = None ):
        #print('xx='+str(self.config['module']['default']))
        if not setvalue:
            if self.config['module']['default'] == 'latest':
                return self.config['module']['latest']
            return self.config['module']['default']
        self.config['module']['default'] = str(setvalue)

    def depends ( self, setvalue = None, getstring = False, fullstring = False ):
        if not setvalue and getstring and fullstring:
            return '\n'.join(['module load ' + v for v in self.config['module']['depends']])
        if not setvalue and getstring:
            return ' '.join(self.config['module']['depends'])
        if not setvalue:
            return self.config['module']['depends']
        if instance(setvalue, list):
            setvalue = ' '.join(setvalue)
        self.config['module']['depends'] = str(setvalue)

    def prepends ( self, setvalue = None, getstring = False ):
        if not setvalue and getstring:
            return '\n'.join(['prepend-path ' + v + ' ' + k for v, k in self.config['prepends'].items()])
        if not setvalue:
            return self.config['prepends']
        self.config['prepends'] = setvalue

    def setenvs ( self, setvalue = None, getstring = False ):
        if not setvalue and getstring:
            return '\n'.join(['setenv ' + v + ' ' + k for v, k in self.config['setenvs'].items()])
        if not setvalue:
            return self.config['setenvs']
        self.config['setenvs'] = setvalue

    def fullname ( self, versions = False ):
        n = self.group() + '/' + self.name()
        if versions:
            vl = self.latest()
            vd = self.default()
            vs = []
            for v in sorted(self.versions()):
                tag = ''
                if v == vl:
                    tag += '=latest'
                if v == vd:
                    tag += '=default'
                v += tag
                vs.append(v)
            n += ' [' + ', '.join(vs) + ']'
        return n

    def read_cfgparser ( self, c ):
        self.reset()
        for section in self.config:
            if not section in c:
                continue
            if section == 'module':
                for variable in self.config[section]:
                    if variable in c[section]:
                        if variable in ['versions', 'depends']:
                            self.config[section][variable] = c[section][variable].split(' ')
                        else:
                            self.config[section][variable] = c[section][variable]
            else:
                for variable in c[section]:
                    self.config[section][variable] = c[section][variable]

    def read_dict( self, d ):
        c = configparser.ConfigParser()
        c.optionxform = str
        c.read_dict(d)
        self.read_cfgparser(c)

    def read_cfg ( self, path = None, string = None ):
        c = configparser.ConfigParser()
        c.optionxform = str
        if path:
            c.read(path)
        elif string:
            c.read_string(string)
        self.read_cfgparser(c)

    def read_template ( self, name ):
        if name in ['default']:
            self.read_cfg(string = tmp.new[name])
            return
        if not name in tmp.configs:
            utl.quit('missing module template: ' + name)
        self.read_cfg(string = tmp.configs[name])

    def read_dir ( self, path ):
        path = utl.pathnorm(path)
        self.group(os.path.basename(os.path.dirname(path)))
        self.name(os.path.basename(path))
        files = utl.pathtree(path, level = 1, incdir = False)
        oripath = os.getcwd()
        os.chdir(path)
        # if not '.version' in files:
        #    utl.warn('missing .version file')
        self.versions([ v for v in files if not v == '.version' ])
        if not self.versions():
            utl.quit('missing module files')
        if '.version' in files:
            if not len(utl.grep('.version', '^\#\%Module1\.0')):
                utl.quit('invalid .version file')
            v = utl.grep('.version', '^set[\t\ ]+ModulesVersion[\t\ \"]+([^\ \"]*).*', '\\1')
            if len(v) > 0:
                self.default(v)
        os.chdir(oripath)
        return

        # todo: collect prepends, depends, setenvs - this is relevant for a import function
        #for f in files:
        #    fpath = os.path.join(path, f)
        #    # check header
        #    if not len(utl.grep(fpath, '^\#\%Module1\.0')):
        #        continue
        #    # check default version
        #    if f == '.version':
        #        v = utl.grep(fpath,
        #            '^set[\t\ ]+ModulesVersion[\t\ \"]+([^\ \"]*).*', '\\1')
        #        if len(v) > 0:
        #            default = v[len(v)-1]
        #        continue
        #    if f == 'latest':
        #        latest = utl.grep(fpath, '^set[\ \t]*version[\ \t]*(.*)', '\\1')[0]
        #    # get prependss and setenvss
        #    p= {}
        #    s= {}
        #    for g in utl.grep(fpath, '^prepend-path[\ \t]*(.*)', '\\1'):
        #        v, k = g.split(' ')
        #        p[v] = k
        #    for g in utl.grep(fpath, '^setenvs[\ \t]*(.*)', '\\1'):
        #        v, k = g.split(' ')
        #        s[v] = k
        #    for g in utl.grep(fpath, '^module[\ \t]*load[\ \t]*(.*)', '\\1'):
        #        depends.append(g)
        #    versions.append(f)
        #    prepends[f] = prep
        #    setenvs[f] = sete
        #self.define(path,group,name,versions,default,latest,depends,prepends,setenvs)

    def show ( self, prefix = '' ):
        print('# modulenv config file')
        for section in self.section_order:
            print('\n[' + section + ']\n')
            if section is 'module':
                variables = self.module_order
            else:
                variables = self.config[section]
            for variable in variables:
                value = self.config[section][variable]
                if not value:
                    value = ''
                if isinstance(value, list):
                    value = ' '.join(value)
                print(variable + ' = ' + value)
                #print(prefix + section + '.' + variable + ' = ' + value)

    def write ( self, path = '.', prefix = None ):
        if not self.valid():
            utl.quit('cannot write invalid module')
        name     = self.name()
        latest   = self.latest()
        default  = self.default()
        prepends = self.prepends(getstring = True)
        setenvs  = self.setenvs(getstring = True)
        depends  = self.depends(getstring = True, fullstring = True)
        files    = self.versions()
        files.append('.version')
        if self.latest():
            files.append('latest')
        # versions
        for fname in files:
            version = fname
            d = { 'name'    :  name,
                  'version' :  version if not version == 'latest' else latest,
                  'default' :  default,
                  'prefix'  :  prefix,
                  'depends' :  depends,
                  'prepends' : prepends,
                  'setenvs'  : setenvs }
            fpath = os.path.join(path, fname)
            if fname == '.version' and not default:
                continue
            f = open(os.path.join(fpath), 'w')
            if fname == '.version':
                f.write(mf.version.format(d))
            else:
                f.write(mf.module.format(d))
            f.close()

