from distutils.core import setup

setup(name='contemarlo',
      version='0.1.0',
      description='Deterministic Monte-Carlo-Like without memory constraints.',
      author='Ryan Birmingham',
      author_email='birm@rbirm.us',
      url='http://rbirm.us',
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   "Topic :: Scientific/Engineering :: Mathematics",
                   "License :: OSI Approved :: GNU General Public License (GPL)"],
      long_description=open('README.txt', 'r').read(),
      packages=['contemarlo'],
      )
