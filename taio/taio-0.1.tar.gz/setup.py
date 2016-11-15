from setuptools import setup, Extension, find_packages
import sys
import os

if sys.version < '2.7' and not sys.version[0] == "3":
    print("taio requires python of at least version 2.7 to build correctly")
    sys.exit()

debug = os.environ.get("TAIODEBUG")
if debug is not None:
    compile_list = ['-D_FILE_OFFSET_BITS=64', '-g']
    if debug.isdigit() and int(debug)  >= 2:
        print "exitended debug enabled"
        compile_list = ['-D_FILE_OFFSET_BITS=64', '-g', '-DDEBUG']
    else:
        print "debug enabled"
else:
    compile_list = ['-D_FILE_OFFSET_BITS=64']

if os.path.isfile("/usr/local/include/ck_spinlock.h") or os.path.isfile("/usr/include/ck_spinlock.h"):
    compile_list.append("-DSPINLOCK=1")
    libs  = ['aio','ck']
else:
    libs = ['aio']


version = '0.1'

taiocore = \
    Extension('taio.core',
              sources=['taio/aio_core.c', 'taio/module_python.c', 'taio/ctx_methods.c', 'taio/ctx_python.c',
                       'taio/file_methods.c', 'taio/file_python.c'],
              libraries=libs,
              include_dirs=['./taio'],
              depends=['taio/aio.h'],
              extra_compile_args=compile_list,
              define_macros=[('TAIO_VERSION', '"{0}"'.format(version))])

setup(
    name="taio",
    #packages = [ 'taio' ],
    packages=find_packages(exclude=["tests", "examples"]),
    version=version,
    description='Twisted  Asynchronous I/O bindings (native linux)',
    author='Radoslaw Ryckowski',
    author_email='radek.ryckowski@gmail.com',
    classifiers=[
        'Operating System :: POSIX',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License'
    ],
    ext_modules=[taiocore])
