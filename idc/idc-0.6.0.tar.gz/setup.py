from setuptools import setup
from os import path

extra_files_path = path.expanduser('~/.idc')
config_path = path.join(extra_files_path, 'config')
sessions_path = path.join(extra_files_path, 'sessions')

setup(
    setup_requires=[
        'pbr'
    ],
    pbr=True,
)

