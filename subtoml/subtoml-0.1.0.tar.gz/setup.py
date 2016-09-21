from setuptools import setup


def readme():
    try:
        with open('README.rst') as f:
            return f.read()
    except IOError:
        pass


setup(
    name='subtoml',
    version='0.1.0',
    description='Sed for TOML: subtitute parts of a TOML file',
    long_description=readme(),
    url='https://bitbucket.org/dahlia/subtoml',
    author='Hong Minhee',
    author_email='\x68\x6f\x6e\x67.minhee' '@' '\x67\x6d\x61\x69\x6c.com',
    license='GPLv3 or later',
    py_modules=['subtoml'],
    install_requires=['pytoml >= 0.1.11'],
    entry_points={
        'console_scripts': ['subtoml = subtoml:main']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Software Development :: Pre-processors',
        'Topic :: Text Editors :: Text Processing',
        'Topic :: Text Processing :: Filters',
        'Topic :: Utilities',
    ]
)
