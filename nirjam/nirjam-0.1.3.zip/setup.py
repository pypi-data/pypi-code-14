from setuptools import setup

setup(name='nirjam',
      version='0.1.3',
      description='A mixture features for the Raspberry Pi',
      url='http://github.com/vlee489/nirjam',
      author='vlee489',
      author_email='vlee@vlee.me.uk',
      license='MIT',
      packages=['nirjam'],
      install_requires=[
          'RPi.GPIO',
      ],
      zip_safe=False)
