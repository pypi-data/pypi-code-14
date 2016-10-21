from setuptools import setup

import sys
import sysconfig
import os
import os.path as op
import distutils.spawn as ds
import distutils.dir_util as dd
import distutils.sysconfig
import distutils

import itertools
from glob import iglob


def _get_distutils_build_directory():
    """
    Returns the directory distutils uses to build its files.
    We need this directory since we build extensions which have to link
    other ones.
    """
    pattern = "lib.{platform}-{major}.{minor}"
    return os.path.join('build', pattern.format(platform=sysconfig.get_platform(),
                                                major=sys.version_info[0],
                                                minor=sys.version_info[1]))


def _get_source_files(directory):
    path = os.path.join('src', directory)
    iterable_sources = (iglob(os.path.join(root,'*.cpp')) for root, dirs, files in os.walk(path))
    source_files = itertools.chain.from_iterable(iterable_sources)
    return list(source_files)


def _remove_strict_prototype_option_from_distutils_config():
    strict_prototypes = '-Wstrict-prototypes'
    config = distutils.sysconfig.get_config_vars()
    for key, value in config.iteritems():
        if strict_prototypes in str(value):
            config[key] = config[key].replace(strict_prototypes, '')

_remove_strict_prototype_option_from_distutils_config()


def _has_numpy_headers():
    try:
        import numpy
        return True
    except:
        return False


def get_extension_modules():
    """
    Extension module which is actually a plain C++ library without Python bindings
    """
    turbodbc_sources = _get_source_files('cpp_odbc') + _get_source_files('turbodbc')
    turbodbc_library = distutils.core.Extension('libturbodbc',
                                                sources=turbodbc_sources,
                                                include_dirs=['include/'],
                                                extra_compile_args=['--std=c++11'],
                                                libraries=['odbc', 'boost_python'])
    
    """
    An extension module which contains the main Python bindings for turbodbc
    """
    turbodbc_python = distutils.core.Extension('turbodbc_intern',
                                               sources=_get_source_files('turbodbc_python'),
                                               include_dirs=['include/'],
                                               extra_compile_args=['--std=c++11'],
                                               libraries=['odbc', 'boost_python', 'turbodbc'],
                                               extra_link_args=["-Wl,-rpath,$ORIGIN"],
                                               library_dirs=[_get_distutils_build_directory()])
    
    """
    An extension module which contains Python bindings which require numpy support
    to work. Not included in the standard Python bindings so this can stay optional.
    """
    if _has_numpy_headers():
        import numpy
        turbodbc_numpy = distutils.core.Extension('turbodbc_numpy_support',
                                                  sources=_get_source_files('turbodbc_numpy'),
                                                  include_dirs=['include/', numpy.get_include()],
                                                  extra_compile_args=['--std=c++11'],
                                                  libraries=['odbc', 'boost_python', 'turbodbc'],
                                                  extra_link_args=["-Wl,-rpath,$ORIGIN"],
                                                  library_dirs=[_get_distutils_build_directory()])
        return [turbodbc_library, turbodbc_python, turbodbc_numpy]
    else:
        return [turbodbc_library, turbodbc_python]


setup(name = 'turbodbc',
      version = '0.4.1',
      description = 'turbodbc is a Python DB API 2.0 compatible ODBC driver',
      include_package_data = True,
      url = 'https://github.com/blue-yonder/turbodbc',
      author='Michael Koenig',
      author_email = 'michael.koenig@blue-yonder.com',
      packages = ['turbodbc'],
      classifiers = ['Development Status :: 4 - Beta',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: POSIX :: Linux',
                     'Programming Language :: C++',
                     'Programming Language :: Python :: 2.7',
                     'Topic :: Database'],
      ext_modules = get_extension_modules()
      )
