from setuptools import setup

setup(name='ntv-firmware',
      version='1.0',
      description='Utility function for locating the serial port of a particular firmware device.',
      url='https://git.native.com/ntv/python-firmware',
      author='Alan Pich',
      author_email='alanp@native.com',
      license='MIT',
      packages=['ntv_firmware'],
      install_requires=[
      ],
      entry_points={
        # 'console_scripts': ['eopdev=eopdev.cli:eopdev']
      },
      zip_safe=False)
