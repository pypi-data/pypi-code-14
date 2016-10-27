from distutils.core import setup

setup(name='statmail',
      version='1',
      description='STATistics and STATus sent via email for servers.',
      author='Ryan Birmingham',
      author_email='birm@rbirm.us',
      url='http://rbirm.us',
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Intended Audience :: Information Technology',
                   'Operating System :: POSIX'],
      long_description=open('README.md', 'r').read(),
      packages=['statmail'],
      )
