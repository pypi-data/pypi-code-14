#-*- coding: utf-8 -*-

from sys import version
if not version[0] == '3':
    raise RuntimeError('this is for Python3 only!')

from distutils.core import setup, Extension

unrtf_c_sources = list(map(lambda f: 'unrtf_ext/src/{}'.format(f), [
   'attr.c',
   'attr.h',
   'convert.c',
   'convert.h',
   'defs.h',
   'error.c',
   'error.h',
   'fontentry.h',
   'hash.c',
   'hash.h',
   'malloc.c',
   'malloc.h',
   'my_iconv.c',
   'my_iconv.h',
   'output.c',
   'output.h',
   'parse.c',
   'parse.h',
   'path.c',
   'path.h',
   'unicode.c',
   'unicode.h',
   'user.c',
   'user.h',
   'util.c',
   'util.h',
   'word.c',
   'word.h',
   'lib.cpp',
   'lib.h',
   'pylib.cpp',
]))

unrtf_conf_files = list(map(lambda f: 'unrtf_ext/config/{}'.format(f), [
    'html.conf',
    'latex.conf',
    'rtf.conf',
    'SYMBOL.charmap',
    'text.conf',
    'troff_mm.conf',
    'vt.conf'
]))


unrtf_module = Extension('_unrtf',
                    define_macros = [('PACKAGE_VERSION', '"1"'),
                                     ('PKGDATADIR', '"/usr/local/share/python-unrtf/"')],
                    sources = unrtf_c_sources,
                    include_dirs = ['./unrtf_ext/src'])

setup (name = 'unrtf',
       version = '0.1.4',
       description = 'GNU unrtf python bindings',
       author = 'Sławomir Zborowski',
       author_email = 'slawomir.zborowski@nokia.com',
       url = 'https://github.com/szborows/python-unrtf',
       license = 'GNU General Public License v3 (GPLv3)',
       py_modules=['unrtf'],
       ext_modules = [unrtf_module],
       data_files = [('/usr/local/share/python-unrtf/', unrtf_conf_files)],
       keywords = 'unrtf rtf',
       classifiers = [
           'Development Status :: 3 - Alpha',
           'Environment :: Console',
           'Intended Audience :: Developers',
           'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
           'Operating System :: POSIX',
           'Programming Language :: C',
           'Programming Language :: Python :: 3 :: Only',
           'Programming Language :: Python :: 3.5',
           'Topic :: Utilities'
       ])
