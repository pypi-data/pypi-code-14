from os import path
from setuptools import setup

readme_path = path.join(path.abspath(path.dirname(__file__)), 'README.md')

long_description = open(readme_path).read()

setup(
    name='jupyterhub-systemdspawner',
    version='0.9.1',
    description='JupyterHub Spawner using systemd for resource isolation',
    long_description=long_description,
    url='https://github.com/jupyterhub/systemdspawner',
    author='Yuvi Panda',
    author_email='yuvipanda@gmail.com',
    license='3 Clause BSD',
    packages=['systemdspawner'],
    install_requires=['jupyterhub'],
)
