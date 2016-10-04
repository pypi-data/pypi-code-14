from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

VERSION = "0.3"

setup(
    name='ha-alpr',
    version=VERSION,
    license='MIT License',
    author='Pascal Vizeli',
    author_email='pvizeli@syshack.ch',
    url='https://github.com/pvizeli/ha-alpr',
    download_url='https://github.com/pvizeli/ha-alpr/tarball/'+VERSION,
    description=('a Python module that provides an interface OpenAlpr command '
                 'line tool for Home-Assistant.'),
    long_description=long_description,
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        ],
    keywords=['openalpr', 'plate', 'homeassistant', 'wrapper', 'api'],
    zip_safe=False,
    platforms='any',
    py_modules=['haalpr'],
)
