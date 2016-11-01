from setuptools import setup
# https://python-packaging.readthedocs.io/en/latest/minimal.html
setup(name='nodewire',
      version='0.4',
      description='NodeWire Gateway',
      url='http://www.nodewire.org',
      author='Ahmad Sadiq',
      author_email='sadiq.a.ahmad@gmail.com',
      license='BSD',
      packages=['nodewire'],
      scripts=['bin/nodewiregw.py', 'bin/nodewireRe.py'],
      install_requires=[
            'paho-mqtt',
            'configparser',
            'netifaces',
            'pyserial',
            'requests'
      ],
      zip_safe=False)
