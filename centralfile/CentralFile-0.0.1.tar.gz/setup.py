from distutils.core import setup

setup(name='CentralFile',
      version='0.0.1',
      description='Centalized Configuration File Management',
      author='Ryan Birmingham',
      author_email='birm@rbirm.us',
      url='http://rbirm.us',
      classifiers=['Development Status :: 1 - Planning', 'Topic :: Database',
                   'Topic :: Internet', 'Topic :: Desktop Environment',
                   'Topic :: Security',
                   'Intended Audience :: Information Technology'],
      long_description=open('readme.md', 'r').read(),
      packages=['CentralFile'],
      )
