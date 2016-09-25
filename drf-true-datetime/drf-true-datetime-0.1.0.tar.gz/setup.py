import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


requirements = [
]


setup(
    name='drf-true-datetime',
    packages=['drf_true_datetime'],
    version='0.1.0',
    description='Custom date time field for DRF to fix bad client time',
    author='HyperTrack',
    author_email='devops@hypertrack.io',
    url='https://github.com/hypertrack/drf-true-datetime',
    license='MIT',
    download_url='https://github.com/hypertrack/drf-true-datetime/tarball/0.1',
    keywords=['drf', 'django', 'datetime'],
    classifiers=[],
    install_requires=requirements
)
