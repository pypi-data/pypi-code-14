# from distutils.core import setup
# from distutils.extension import Extension
from setuptools import setup
from setuptools import Extension
import os
import sys
print 'This module requires libboost-python-dev, libpython-dev, libpqxx-4.0, libpqxx-dev, libhdf5-dev'

if sys.platform =='darwin':
    os.system('sudo port install boost hdf5 python27 libpqxx')
elif sys.platform =='linux2':
    os.system('sudo apt-get install libboost-python-dev libpython-dev libpqxx-4.0 libpqxx-dev libhdf5-dev')

srcs = ['package/src/' + i for i in os.listdir('package/src') if i.endswith('cpp')]
headers = ['package/header/' + i for i in os.listdir('package/header')]
inc = ['package/header', '/usr/include/hdf5/serial']
if 'C_INCLUDE_PATH' in os.environ.keys():
    c_inc = os.environ.get('C_INCLUDE_PATH').split(':')
    print 'Appending C_LIBRARY_PATH'
    if '' in c_inc:
        c_inc.remove('')
    inc += c_inc

if 'CPLUS_INCLUDE_PATH' in os.environ.keys():
    cplus_inc = os.environ.get('CPLUS_INCLUDE_PATH').split(':')
    print 'Appending CPLUS_LIBRARY_PATH'
    if '' in cplus_inc:
        cplus_inc.remove('')
    inc += cplus_inc


lib = ['/opt/local/lib', '/usr/local/lib'] if sys.platform=='darwin' else\
    ['/usr/local/lib','/usr/lib','/usr/lib/x86_64-linux-gnu']

if 'LD_LIBRARY_PATH' in os.environ.keys():
    print 'Appending LD_LIBRARY_PATH'
    lib += os.environ.get('LD_LIBRARY_PATH').split(':')

LIB_BOOST_PYTHON='boost_python-mt' if sys.platform == 'darwin' else\
    'boost_python'

libraries=[LIB_BOOST_PYTHON, 'python2.7', 'pqxx']
if sys.platform =='darwin':
    libraries += ['hdf5', 'hdf5_hl']
elif sys.platform == 'linux2':
    import platform
    if float(platform.linux_distribution()[1]) >= 16:
        libraries += ['hdf5_serial', 'hdf5_serial_hl']
    else:
        libraries += ['hdf5', 'hdf5_hl']

classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish (should match "license" above)
     'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2.7',
]

print libraries
setup(name='mygraph',
      classifiers=classifiers,
      license='MIT',
      version='0.9.5',
      description='Python wrapper of C++ Time-dependent Hyperpath algorithm implementation, requires python-dev, boost_python, pqxx and hdf5 installed',
      keywords='hyperpath',
      author='Jiangshan(Tonny) Ma',
      author_email='tonny.achilles@gmail.com',
      url='http://fukudalab.hypernav.mobi',
      data_files=[('data', ['package/data/bell.dat'])],
      package_data = { 'package': ['package/data/*'] },
      #install_requires=['numpy'],
      ext_modules=[
          Extension("mygraph",
                    define_macros=[('MAJOR_VERSION', '0'), ('MINOR_VERSION', '9')],
                    include_dirs=inc,
                    library_dirs=lib,
                    libraries=libraries,
                    extra_compile_args=['-std=c++0x'],
                    sources=srcs)
      ])
