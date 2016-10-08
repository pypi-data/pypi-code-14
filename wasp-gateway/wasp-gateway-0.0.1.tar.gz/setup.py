from setuptools import setup, find_packages

__version__ = '0.0.1'

setup(name='wasp-gateway',
      version=__version__,
      description=('API Gateway: Central access point into a microservice '
                   'based system'),
      author='Matt Rasband, Nick Humrich',
      author_email='matt.rasband@gmail.com',
      license='Apache-2.0',
      url='https://github.com/WickedAsyncServicesPlatform/wasp-gateway',
      download_url=('https://github.com/WickedAsyncServicesPlatform'
                    '/wasp-gateway/releases'),
      keywords=[
          'microservice',
          'gateway',
          'api',
          'asyncio',
          'aiohttp'
      ],
      packages=find_packages(),
      classifiers=[
          'Programming Language :: Python :: 3.5',
          'License :: OSI Approved :: Apache Software License',
          'Intended Audience :: Developers',
          'Development Status :: 2 - Pre-Alpha',
          'Topic :: Software Development',
      ],
      setup_requires=[
          'pytest-runner',
          'flake8',
      ],
      install_requires=[
          'aiohttp>=1.0',
      ],
      extras_require={
          'recommends': ['uvloop'],
      },
      tests_require=[
        'pytest-aiohttp',
        'pytest',
      ],
      entry_points={},
      zip_safe=False)
