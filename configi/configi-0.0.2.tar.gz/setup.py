try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = open('README.rst').read()

setup(
    author='Josef Lange',
    author_email='josef.d.lange@me.com',
    name='configi',
    description='Configi is a straightforward wrapper for configuration data. It provides a consistent interface to a number of back-ends, currently via arbitrary HTTP JSON loading, Redis K/V store, and S3 JSON file loading.',
    version='0.0.2',
    py_modules=['configi'],
    license='MIT',
    long_description=long_description,
    install_requires=[
        'requests'
    ],
    url='https://github.com/josefdlange/configi',
    test_suite='nose.collector',
    tests_require=['nose']
)

# End

