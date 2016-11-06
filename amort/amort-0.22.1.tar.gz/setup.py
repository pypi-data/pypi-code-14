from setuptools import setup

setup(name='amort',
      version='0.22.1',
      author='Mandeep',
      author_email='info@mandeep.xyz',
      description='A command line application that creates amortization schedules.',
      license='GPLv3+',
      packages=['amort', 'amort.tests'],
      install_requires=[
        'click==6.6',
      ],
      entry_points='''
        [console_scripts]
        amortization=amort.commandline:cli
        ''',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
      ],
      )
