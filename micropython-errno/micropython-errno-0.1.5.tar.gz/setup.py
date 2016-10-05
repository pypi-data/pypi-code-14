import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system.
sys.path.pop(0)
from setuptools import setup
from setuptools import Command

class Repack(Command):
    user_options = []
    def run(self):
        sys.path.append("..")
        import recompress_gzip_4k
        recompress_gzip_4k.recompress_latest("dist")
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass

setup(name='micropython-errno',
      version='0.1.5',
      description='errno module for MicroPython',
      long_description="This is a module reimplemented specifically for MicroPython standard library,\nwith efficient and lean design in mind. Note that this module is likely work\nin progress and likely supports just a subset of CPython's corresponding\nmodule. Please help with the development if you are interested in this\nmodule.",
      url='https://github.com/micropython/micropython/issues/405',
      author='MicroPython Developers',
      author_email='micro-python@googlegroups.com',
      maintainer='MicroPython Developers',
      maintainer_email='micro-python@googlegroups.com',
      license='MIT',
      py_modules=['errno'],
      cmdclass={
        'repack': Repack,
      })
