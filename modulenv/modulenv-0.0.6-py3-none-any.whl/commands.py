# commands.py
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
import sys
import tarfile
import urllib.request
import modulenv.utils as utl
import modulenv.templates as tmp
from modulenv import __version__
from modulenv.module import Module
from modulenv.environment import Environment

def none( args ):
    print('command missing, use --help to see list of commands available')

def version ( args ):
    print('modulenv version ' + __version__)

### menv

def env_init( args ):
    e = Environment(path = args.prefix)
    e.init(bindir = args.bin, envdir = args.env, home = args.moduleshome,
           clear = args.clearmodpath, cmd = args.modulecmd)
    utl.log('init', os.path.join(args.prefix, 'log'))
    print('  * new module environment created',
          '    activate (e.g. in ~/.profile) by:',
          '    source ' + os.path.join(e.prefix, 'src'),
          sep = '\n')

def env_status ( args ):
    e = Environment(path = args.prefix)
    if not e.valid():
        utl.quit('not a valid environment')
    e.show()

def env_add ( args ):
    e = Environment(path = args.prefix)
    if e.empty:
        utl.quit('cannot add to empty environment, init first')
    if not e.valid():
        utl.quit('not a valid environment')
    mods = []
    files = args.file
    from_stdin = files[0] is '-' and not args.template
    if from_stdin:
        files = ['stdin']
    for infile in files:
        m = Module()
        if args.verbose:
            if from_stdin:
                print('  * processing standard input')
            elif args.template:
                print('  * processing template ' + infile)
            else:
                print('  * processing file ' + infile)
        if args.template:
            m.read_template(infile)
        else:
            if from_stdin:
                infile = ''.join(sys.stdin.readlines())
                m.read_cfg(string = infile)
            else:
                m.read_cfg(infile)
            v = m.valid(verbose = args.verbose)
            if not v:
                utl.quit('cannot add invalid module')
        mods.append(m)
    for m in mods:
        e.add(m, force = args.force)
        utl.log('add ' + m.fullname(), os.path.join(args.prefix, 'log'))
        print('  * added ' + m.fullname())
        oldgroups = e.groups()
        if not m.group() in oldgroups:
            print('  [' + m.group() +
                  '] is a new module group folder - activate with:\n  source ' +
                  os.path.join(e.prefix, 'src'))
    return

def env_rm ( args ):
    e = Environment(path = args.prefix)
    if not e.valid():
        utl.quit('not a valid environment')
    if e.empty:
        utl.quit('cannot remove from emtpy environment')
    if not args.name in e.names():
        utl.quit('module not in environment: ' + args.name)
    m = [ m.fullname() for m in e.modules if m.name() == args.name ]
    utl.log('rm ' + m[0], os.path.join(args.prefix, 'log'))
    e.rm(args.name)

### mconf

def conf_check ( args ):
    for f in args.files:
        print('\n* config file ' + f)
        m = Module()
        m.read_cfg(f)
        m.valid(verbose = True, show = args.verbose)

def conf_new ( args ):
    m = Module()
    m.read_template('default')
    m.name(args.name)
    m.group(args.group)
    m.versions(args.versions)
    if args.default:
        m.default(args.default)
    if args.latest:
        m.latest(args.latest)
    if args.depends:
        m.depends(args.depends)
    if args.prepends:
        d = {}
        for pair in args.prepends:
            pair = pair.split('=')
            var = pair[0].strip()
            val = '='.join(pair[1:len(pair)]).strip()
            d[var] = val
        m.prepends(d)
    if args.setenvs:
        d = {}
        for pair in args.setenvs:
            pair = pair.split('=')
            var = pair[0].strip()
            val = '='.join(pair[1:len(pair)]).strip()
            d[var] = val
        m.setenvs(d)
    v = m.valid(verbose = args.verbose)
    m.show()
    # add file output

def conf_template ( args ):
    if not args.name:
        print('  * available:')
        for i in tmp.avail():
            print('    - ' + i)
    else:
        m = Module()
        m.read_template(args.name)
        m.show()
        # for installer: print(tmp.module_installs[args.name])

###

def sources ( args ):
    name = args.name
    print('* ' + name + ' source')
    if not name in tmp.sources:
        utl.quit('missing source for: ' + name)
    v = args.version
    if args.download and not v:
        utl.quit('missing version')
    versions = []
    print('  checking versions')
    for s in tmp.sources[name]:
        response = urllib.request.urlopen(s)
        html = response.read()
        html = str(html)
        if name == 'R':
            html = html.split('.tar.gz')
            html = utl.grep(pattern = '.*R-(\d\.\d+\.\d.*)$', replacement = '\\1',
                lines = html)
            html.sort(key = lambda s: [int(u) for u in s.split('-')[0].split('.')])
        elif name == 'python':
            html = html.split('/</a>')
            html = utl.grep(pattern = '.*>(\d+\.\d+\.\d+)$', replacement = '\\1',
                lines = html)
            html.sort(key = lambda s: [int(u) for u in s.split('.')])
        elif name in ['shellset', 'julia']:
            html = html.split('zipball/')
            html = utl.grep(pattern = '^.*(\d+\.\d+\.\d+).*', replacement = '\\1',
                lines = html)
            html = list(set(html))
            html.sort(key = lambda s: [int(u) for u in s.split('.')])
        #if isinstance(html, list):
        #    html = ' - '.join(html)
        versions.extend(html)
        if not args.download:
            print(': '.join([name, s]))
    if not args.download:
        if isinstance(versions, list):
            versions = ' - '.join(versions)
        print(versions)
        return
    if not v in versions:
        utl.quit('invalid version')
    if not os.path.exists(args.prefix):
        os.makedirs(args.prefix)
    os.chdir(args.prefix)
    if not os.path.exists('src-' + name):
        os.makedirs('src-' + name)
    os.chdir('src-' + name)
    if name == 'R':
        maj = v.split('.')[0]
        url = "ftp://stat.ethz.ch/CRAN/src/base/R-" + maj + '/R-' + v + '.tar.gz'
        out = v + '.tar.gz'
    else:
        return
    if os.path.exists(out):
        utl.quit('path exists')
    print('  downloading ' + url + ' -> ' + os.path.join(args.prefix, 'src-'+name, out))
    urllib.request.urlretrieve(url, out)
    try:
        file = tarfile.open(out, 'r:gz')
        try:
            file.extractall()
        finally:
            file.close()
    finally:
        print('* done')
    return

