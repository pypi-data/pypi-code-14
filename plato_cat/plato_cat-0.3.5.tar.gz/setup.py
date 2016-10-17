from setuptools import find_packages, setup
from plato_cat import __version__


setup(name="plato_cat",
      version=__version__,
      description="a cat",
      author="piaoyuankui@le.com",
      url="http://plato_cat.com",
      license="MIT",
      install_requires=[
          'requests==2.10.0',
          'gevent==1.1.2',
      ],
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'plato-cat=plato_cat.cmd:cat',
              'plato-clean=plato_cat.cmd:clean',
              'plato-benchmark=plato_cat.cmd:bench'
          ]
      })
