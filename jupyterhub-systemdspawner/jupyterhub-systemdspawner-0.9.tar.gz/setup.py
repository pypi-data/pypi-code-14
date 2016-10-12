from os import path
from setuptools import setup

readme_path = path.join(path.abspath(path.dirname(__file__)), 'README.md')

try:
    # Only people who need to upload to pypi need to have this installed.
    # Sourced from https://github.com/pypa/pypi-legacy/issues/148
    import pypandoc
    long_description = pypandoc.convert(readme_path, 'rst')
except ImportError:
    long_description = open(readme_path).read()

setup(
    name='jupyterhub-systemdspawner',
    version='0.9',
    description='JupyterHub Spawner using systemd for resource isolation',
    long_description=long_description,
    url='https://github.com/jupyterhub/systemdspawner',
    author='Yuvi Panda',
    author_email='yuvipanda@gmail.com',
    license='3 Clause BSD',
    packages=['systemdspawner'],
    install_requires=['jupyterhub'],
)
