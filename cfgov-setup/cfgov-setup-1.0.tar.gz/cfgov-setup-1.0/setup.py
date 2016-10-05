from setuptools import setup

setup(name='cfgov-setup',
      version='1.0',
      py_modules='cfgov_setup',
      entry_points={'distutils.setup_keywords':
               ['frontend_build_script=cfgov_setup:do_frontend_build']
           }
      )
