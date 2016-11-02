from __future__ import print_function
from setuptools import setup, Command
import sys


# run our tests
class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import sys, subprocess
        tests = [('test suite', ['-m', 'test.test_pyconfreader']),
                 ]
        if sys.hexversion >= 0x03000000:
            # Skip doctests for python < 3.0. They use print statements, which
            #  I can't get to work with print_function in 2.7. Testing under
            #  3.x is good enough.
            tests.append(('doctests',   ['-m' 'doctest', 'README.rst']))
        for name, cmds in tests:
            print(name)
            errno = subprocess.call([sys.executable] + cmds)
            if errno != 0:
                raise SystemExit(errno)
        print('test complete')


setup(name='pyconfreader',
      version='0.4',
      url='https://gitlab.com/ericvsmith/pyconfreader',
      author='Eric V. Smith',
      author_email='eric@trueblade.com',
      description='A library to read config files written in Python.',
      long_description=open('README.rst').read() + '\n' + open('CHANGES.txt').read(),
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Apache Software License',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   ],
      license='Apache License Version 2.0',
      py_modules=['pyconfreader'],

      cmdclass = {'test': PyTest},
      )
