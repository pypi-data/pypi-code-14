from setuptools import setup

setup(name='journal_dates',
      packages=[''],
      version='0.1.1',
      description='Prints a monthly journal template',
      url='http://github.com/bzamecnik/journal_dates',
      author='Bohumir Zamecnik',
      author_email='bohumir.zamecnik@gmail.com',
      license='MIT',
      install_requires=['arrow'],
      zip_safe=False,
      entry_points={
        'console_scripts': [
            'journal_dates=journal_dates:main',
        ],
      },
       # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
       classifiers=[
           # How mature is this project? Common values are
           #   3 - Alpha
           #   4 - Beta
           #   5 - Production/Stable
           'Development Status :: 3 - Alpha',

           'Topic :: Utilities',

           'License :: OSI Approved :: MIT License',

           'Programming Language :: Python :: 2',
           'Programming Language :: Python :: 3',

           'Operating System :: POSIX :: Linux',
           'Operating System :: MacOS :: MacOS X',
       ])
