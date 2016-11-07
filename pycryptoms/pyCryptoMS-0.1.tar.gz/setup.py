# -*- coding: utf-8 -*-
from distutils.core import setup, Extension
from distutils import sysconfig
import distutils.command.build_ext
from distutils.spawn import find_executable
from distutils.version import LooseVersion

import glob
import os
import re
import subprocess

__PACKAGE_VERSION__ = "0.1"
__LIBRARY_VERSION__ = "2.9"
SWIG_MIN_VERSION    = "2.0"

################################################################################

# Delete unwanted flags for C compilation
# Distutils has the lovely feature of providing all the same flags that
# Python was compiled with. The result is that adding extra flags is easy,
# but removing them is a total pain. Doing so involves subclassing the
# compiler class, catching the arguments and manually removing the offending
# flag from the argument list used by the compile function.
# That's the theory anyway, the docs are too poor to actually guide you
# through what you have to do to make that happen.
d = sysconfig.get_config_vars()
for k, v in d.items():
    for unwanted in ('-Wstrict-prototypes', '-DNDEBUG', '-O2'):
        if str(v).find(unwanted) != -1:
            v = d[k] = str(v).replace(unwanted, '')

################################################################################

class Build_Ext_find_swig3(distutils.command.build_ext.build_ext):
    """ Doc:
    https://pythonhosted.org/bob.extension/_modules/distutils/command/build_ext.html
    https://github.com/vishnubob/wub/blob/master/setup.py

    """

    def find_swig(self):

        if os.name != "posix":
            # Call parent function
            return super(Build_Ext_find_swig3, self).find_swig()
        else:
            return self.get_swig_executable()

    def get_swig_executable(self):
        # stolen from https://github.com/FEniCS/ffc/blob/master/setup.py
        "Get SWIG executable"

        # Find SWIG executable
        swig_executable = None
        for executable in ["swig", "swig3.0"]:
            swig_executable = find_executable(executable)
            if swig_executable is not None:
                # Check that SWIG version is ok
                output = subprocess.check_output(
                            [swig_executable, "-version"]).decode('utf-8')
                swig_version = re.findall(r"SWIG Version ([0-9.]+)", output)[0]
                if LooseVersion(swig_version) >= LooseVersion(SWIG_MIN_VERSION):
                    break
                swig_executable = None
        if swig_executable is None:
            raise OSError("Unable to find SWIG version %s or higher." % SWIG_MIN_VERSION)
        print("Found SWIG: %s (version %s)" % (swig_executable, swig_version))
        return swig_executable

################################################################################

modules = [
    Extension(
        "_pyCryptoMS",
       ["src/Binding/CryptoMS.i", 'src/Binding/CryptoMS.cpp'] + \
       glob.glob(os.path.join('src/cmsat/*.cpp')),
        # Stolen at: http://stackoverflow.com/questions/25997532/
        # swig-with-openmp-and-python-does-swig-threads-need-extra-gil-handling
        swig_opts=['-c++', '-threads', '-includeall'],
        include_dirs=['src', 'src/cmsat'], #, 'src/mtl', 'src/MTRand'],
        define_macros=[
            ('VERSION', '"' + __LIBRARY_VERSION__ + '"'),
            ('USE_GAUSS', None),
            ('_pyCryptoMS_EXPORTS', None),
            ('NDEBUG', None)
        ],
        # With gcc, you need to compile and link with -fopenmp to enable OpenMP.
        # Other compilers have different options; with intel it's -openmp,
        # with pgi it's -mp, etc.
        #
        # -Wno-uninitialized : Workaround for the following error:
        # CryptoMS_wrap.cpp:
        # In function ‘PyObject* _wrap_new_CryptoMSError(PyObject*, PyObject*)’:
        # CryptoMS_wrap.cpp:4837:47: error: ‘argv[0]’ may
        #be used uninitialized in this function [-Werror=maybe-uninitialized]
        # PyString_AsStringAndSize(obj, &cstr, &len);
        #                                           ^
        # CryptoMS_wrap.cpp:12366:13: note: ‘argv[0]’ was declared here
        #   PyObject *argv[2];
        #             ^
        extra_compile_args=["-fopenmp", "-g", #"-MD", "-MP", "-MF",
#            "-Wall",
#            "-Werror",
            "-DNDEBUG",
            "-flto",
#            "-Wno-deprecated",
#            "-O2",
#            "-mtune=native",
#            "-fomit-frame-pointer",
            "-Wno-uninitialized"],
        extra_link_args=['-lgomp', "-flto",],
    ),
]

setup(
    name = "pyCryptoMS",
    version = __PACKAGE_VERSION__,
    license="GPLv3",
    author="Based on the work of"
        + "Geoffroy Andrieux, "
        + "Michel Le Borgne, "
        + "Mate Soos, "
        + "Niklas Een, "
        + "Niklas Sorensson.",
    author_email="geoffroy.andrieux@irisa.fr",
    description="SAT compiler version :" + __LIBRARY_VERSION__,
    long_description=open('src/Binding/README.md').read(),
    url='http://cadbiom.genouest.org/index.html',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
    ],
    package_dir={'': 'src/Binding'},
    py_modules=['pyCryptoMS'],
    ext_modules = modules,
    cmdclass={
        "build_ext": Build_Ext_find_swig3
    }
)
