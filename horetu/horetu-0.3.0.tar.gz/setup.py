from distutils.core import setup

packages=[
    'horetu',
    'funmap',
    'triedict',
    'horetu.input', 
    'horetu.render',
    'horetu.render.argparse',
]

setup(name='horetu',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Make a command-line interface from a function.',
      url='http://src.thomaslevine.com/horetu/',
      packages=packages,
      install_requires=[
      ],
      extras_require={
          'all': ['horetu[wsgi]', 'horetu[django]'],
          'django': ['Django>=1.10.2'],
          'docs': ['sphinxcontrib-autorun>=0.1'],
          'wsgi': ['WebOb>=1.6.1'],
          'tests': ['pytest>=2.6.4'],
          'dev': ['horetu[docs]', 'horetu[tests]', 'horetu[all]'],
      },
      tests_require=[
          'horetu[tests]',
      ],
      classifiers=[
          'Programming Language :: Python :: 3.5',
      ],
      version='0.3.0',
      license='AGPL',
      )
