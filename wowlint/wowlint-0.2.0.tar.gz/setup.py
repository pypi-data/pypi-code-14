import re

from setuptools import setup, find_packages


VERSIONFILE = "src/wowlint/_version.py"
verstr = "unknown"
try:
    verstrline = open(VERSIONFILE, "rt").read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        verstr = mo.group(1)
except EnvironmentError:
    print "unable to find version in %s" % (VERSIONFILE,)
    raise RuntimeError("if %s exists, it is required to be well-formed" % (VERSIONFILE,))

setup(
    name='wowlint',
    version=verstr,
    description='Linter for Words of Worship resource files',
    author='James Muscat',
    author_email='jamesremuscat@gmail.com',
    url='https://github.com/jamesremuscat/wowlint',
    install_requires=['construct==2.5.2', 'enum34', 'pyenchant', 'pyyaml'],
    setup_requires=['nose>=1.0'],
    # tests_require = ['mock'],
    packages=find_packages('src', exclude=["*.tests"]),
    package_dir = {'':'src'},
    entry_points={
        'console_scripts': [
            'wowlint = wowlint.command:main'
        ],
    }
)
