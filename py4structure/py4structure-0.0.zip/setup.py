from distutils.core import setup
setup(
    name='py4structure',
    version='0.0',
    description='Structural engeenering design python scripts for SeePy',
    long_description = open("README.txt").read(),
    author='Lukasz Laba',
    author_email='lukaszlab@o2.pl',
    url='https://bitbucket.org/lukaszlaba/py4structure/wiki/Home',
    packages=['py4structure', 'py4structure.scripts'],
    package_data = {'': ['*.png', '*.svg']},
    license = 'GNU General Public License (GPL)',
    keywords = 'civil engineering ,structural engineering, concrete structures, steel structures',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        ],
    )