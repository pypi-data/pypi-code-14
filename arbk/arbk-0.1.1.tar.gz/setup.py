from distutils.core import setup

setup(name='arbk',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Scraper për Agjencia e Regjistrimit të Bizneseve',
      url='http://src.thomaslevine.com/arbk/',
      packages=['arbk'],
      install_requires = [
          'requests>=2.11.1',
          'vlermv>=1.4.2',
          'horetu>=0.2.7',
          'lxml>=3.4.2',
      ],
      tests_require = [
          'pytest>=2.6.4',
      ],
      version='0.1.1',
      license='AGPL',
      entry_points = {
          'console_scripts': ['arbk = arbk:cli']
      },
)
