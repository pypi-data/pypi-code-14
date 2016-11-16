from setuptools import setup

# Stolen from the setuptools documentation.
def read(fname):
    from os.path import dirname, join
    return open(join(dirname(__file__), fname)).read()

# Don't list "test" in packages, because we don't want it installed.
setup(
    name         = 'dunshire',
    version      = '0.1.1',
    author       = 'Michael Orlitzky',
    author_email = 'michael@orlitzky.com',
    url          = 'http://michael.orlitzky.com/code/dunshire/',
    keywords     = 'game theory, cone programming, optimization',
    packages     = ['dunshire'],
    description  = 'A library for solving linear games over symmetric cones',
    long_description = read('doc/README.rst'),
    license      = 'AGPLv3+',
    install_requires = [ 'cvxopt >= 1.1.8' ],
    test_suite = 'test.build_suite',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
