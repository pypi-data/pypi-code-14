import subprocess
from setuptools import setup

subprocess.call("python install.py", shell=True)

setup(name='edisionnet', version='1.0.0', py_modules = ['install'], packages=['edisionnet'],  install_requires=[
              'Pynetinfo==0.1.9',
                    ],)
