try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup
  

setup(
    name             = 'Looppool',
    version          = '0.1.0',
    author           = 'saaj',
    author_email     = 'mail@saaj.me',
    packages         = ['looppool'],
    test_suite       = 'looppool.test',
    url              = 'https://bitbucket.org/saaj/looppool',
    license          = 'LGPL-2.1+',
    description      = 'Tornado IO loop process pool with message passing',
    long_description = open('README.txt', 'rb').read().decode('utf-8'),
    install_requires = ['tornado >= 4, < 5'],
    platforms        = ['Any'],
    keywords    = 'python tornado multiprocessing process-pool io-loop',
    classifiers = [
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers'
    ]
)

