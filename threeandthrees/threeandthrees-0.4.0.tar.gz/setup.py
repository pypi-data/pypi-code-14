from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='threeandthrees',
    version='0.4.0',
    description='A CLI 3&3s game',
    long_description='Play a word game against the words file.',
    author='Ben Warren',
    url='https://github.com/bwarren2/threeandthrees',
    author_email='bwarren2@gmail.com',
    license='MIT',
    platforms='any',
    py_modules=['threeandthrees'],
    package_data={'': ['*.txt']},
    install_requires=required,
    scripts=['threeandthrees/3and3s'],
)
