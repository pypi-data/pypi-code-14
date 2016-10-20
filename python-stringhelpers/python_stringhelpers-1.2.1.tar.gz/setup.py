from setuptools import setup

VERSION = __import__("stringhelpers").__version__

setup(
    name='python_stringhelpers',
    description='A set of various string helpers.',
    version=VERSION,
    license='MIT',
    author='Dusty Gamble',
    author_email='dusty.gamble@gmail.com',
    url='https://github.com/ipsod/python_stringhelpers',
    packages=['stringhelpers'],
    zip_safe=False,
    classifiers=[
        'Topic :: Utilities',
        'Topic :: Text Processing',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ]
)
