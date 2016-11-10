""" building plibfast module with a Cython file and external
  library and header that depend to system and CPU extensions
"""

from sys import prefix
from os import system as ossys
from platform import processor
from platform import system
from setuptools import Extension
from setuptools import setup
from setuptools.dist import Distribution
import subprocess


def get_prefix():
    """
    Get prefix from either config file or command line
    :return: str
    prefix install path
    """
    dist = Distribution()
    dist.parse_config_files()
    dist.parse_command_line()
    try:
        user_prefix = dist.get_option_dict('install')['prefix'][1]
    except KeyError:
        user_prefix = prefix
    return user_prefix


def get_cpu_extension(current_system):
    """
    Get Intel CPU extensions
    :return: str
    Current system CPU extensions
    :raise:
    Exception: When flags info is not available
    NotImplementedError : When current_system is not linux
    """
    if current_system == 'Linux':
        with open('/proc/cpuinfo') as cpu_info_file:
            line = cpu_info_file.read()
            tab = set(line.split('\n'))
            line = [string for string in tab if string.find('flags') != -1 ]
            if line:
                res = []
                for entry in line[0].split():
                    res.append(entry.upper())
                return res
        raise Exception('Intel CPU extensions not found on your system')
    if current_system == 'Darwin':
        stdoutdata = subprocess.getoutput("sysctl -a | grep machdep.cpu")
        if not stdoutdata:
            raise Exception('Intel CPU extensions not found on your system')
        return stdoutdata.split()
    else:
        raise NotImplementedError('Not implemented for other system than Linux')


def get_install_externals():
    """
    Download and install compiled lib_vectorize and plib_vectorized_def.h
    for specific system (linux or darwin) and Intel CPU extensions
    :raises: Exception
    When file(s) cannot be download or install on the system
    """
    # Get current system type and CPU extensions
    searching_extensions = ('AVX512', 'AVX2', 'AVX', 'SSE4', 'SSSE3',
                            'SSE2', 'SSE')
    current_system = system()  # Linux or Darwin
    cpu_extensions = get_cpu_extension(current_system)
    current_cpu_extension = None
    if cpu_extensions:
        for extension in searching_extensions:
            for flag in cpu_extensions:
                if flag.find(extension) != -1:
                    current_cpu_extension = extension
                    break
            if current_cpu_extension:
                break

    if current_system == 'Linux':
        current_processor = processor()
    elif current_system == 'Darwin':
        current_processor = 'x86_64'
    else:
        raise Exception("Current processor not supported ")
#   get lib_vectorize library and install it to prefix
    extension_lib = 'so'
    if current_system == 'Darwin':
        extension_lib = 'dylib'

    server_url = 'https://gitlab.in2p3.fr/CTA-LAPP/' \
                 'binaries_plib_vectorize/raw/master'

    url = '{}/{}/{}/{}/libplib8_vectorize.{}'.format(server_url,
                                                          current_system,
                                                          current_processor,
                                                          current_cpu_extension,
                                                          extension_lib)
#   download and install library
    if current_system == 'Linux':
        ret = ossys('wget ' + url)
    elif current_system == 'Darwin':
        print('DEBUG ----> {}'.format('curl -O ' + url))
        ret = ossys('curl -O ' + url)
    if ret:
        raise Exception('Error while executing wget {}'.format(url))

    if current_system == 'Darwin':
        cmd = 'install_name_tool -id \"@rpath/libplib8_vectorize.dylib\" libplib8_vectorize.dylib' 
        print('DEBUG -> cmd {}'.format(cmd))
        ossys(cmd)

    command = 'mv libplib8_vectorize.{} {}/lib'.format(extension_lib,
                                                       get_prefix())
    ret = ossys(command)
    if ret:
        raise Exception('Error while executing {}'.format(command))

	

#   download and install header
    url = '{}/{}/{}/{}/plib_vectorized_def.h'.format(server_url, current_system,
                                                     current_processor,
                                                     current_cpu_extension)
    if current_system == 'Linux':
        ret = ossys('wget ' + url)
    elif current_system == 'Darwin':
        ret = ossys('curl -O ' + url)
    if ret:
        raise Exception('Error while executiong {}'.format(url))


# Build C extensions thanks to cython

try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
    print("Cython not found")
    raise Exception('Please install Cython on your system')
else:
    use_cython = True
# Download lib_vectorize + header file for specific system/CPU extensions
    get_install_externals()

cmdclass = {}
ext_modules = []
lib_prefix = ""
include_prefix = "plibfast/src"
generate_include_prefix = "plibfast/src"
ext_modules += [
    Extension("plibfast.alloc", ["plibfast/src/align_wrapper.pyx"],
              libraries=['plib8_vectorize'],
              runtime_library_dirs=['/Users/jean/miniconda3/envs/cta/lib/'],
              extra_link_args=['-Wl,-rpath,{}/lib'.format(get_prefix())],
              depends=['plibfast/src/alloc_aligned_type.c',
              'plibfast/src/reduction.c'],
              include_dirs=['.', 'plibfast/src/', include_prefix,
              generate_include_prefix])
]
cmdclass.update({'build_ext': build_ext}),
NAME = 'plibfast'
VERSION = '1.0.2'
AUTHOR = 'Pierre Aubert, Jean Jacquemier'
AUTHOR_EMAIL = 'jean.jacquemier@lapp.in2p3.fr'
URL = 'https://gitlab.in2p3.fr/CTA-LAPP/plibfast'
DESCRIPTION = 'Python wrapper for fast math library'
LICENSE = 'BSD License'

setup(name=NAME,
      version=VERSION,
      cmdclass=cmdclass,
      ext_modules=ext_modules,
      description=DESCRIPTION,
      install_requires=['numpy', 'cython'],
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      url=URL,
      packages=['plibfast', 'plibfast.math','plibfast.save'],
      classifiers=['Intended Audience :: Science/Research',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: C',
                   'Programming Language :: Cython',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: Implementation :: CPython',
                   'Topic :: Scientific/Engineering :: Astronomy',
                   'Development Status :: 3 - Alpha'])
