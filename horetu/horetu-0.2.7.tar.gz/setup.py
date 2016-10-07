from distutils.core import setup

packages=[
    'horetu',
    'funmap',
    'triedict',
    'horetu.input', 
    'horetu.output',
    'horetu.render',
]

setup(name='horetu',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Make a command-line interface from a function.',
      url='http://src.thomaslevine.com/horetu/',
      packages=packages,
      include_package_data=True,
      package_data = {
          'horetu.render': ['render/templates/*'],
      },
      install_requires=[
      ],
      extras_require={
          'all': ['horetu[wsgi]'],
          'docs': ['sphinxcontrib-autorun>=0.1'],
          'wsgi': ['Jinja2>=2.8', 'WebOb>=1.6.1'],
          'tests': ['pytest>=2.6.4'],
          'dev': ['horetu[docs]', 'horetu[tests]', 'horetu[all]'],
      },
      tests_require=[
          'horetu[tests]',
      ],
      classifiers=[
          'Programming Language :: Python :: 3.5',
      ],
      version='0.2.7',
      license='AGPL',
      )
