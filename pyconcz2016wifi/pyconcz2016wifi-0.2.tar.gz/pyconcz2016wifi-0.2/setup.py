from distutils.core import setup

setup(name='pyconcz2016wifi',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Connect to the internet at PyConCZ 2016.',
      url='http://src.thomaslevine.com/pyconcz2016wifi/',
      install_requires=[
          'requests>=2.11.1',
          'horetu>=0.2.7',
      ],
      scripts=['pyconcz2016wifi'],
      classifiers=[
          'Programming Language :: Python :: 3.5',
      ],
      version='0.2',
      license='AGPL',
      )
