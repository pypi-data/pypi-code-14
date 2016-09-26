from setuptools import setup


def listify(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def contents(filename):
    with open(filename) as f:
        return f.read()

setup(
    name='pyrencode',
    packages=['pyrencode', 'pyrencode.settings'],
    version='0.0.4',
    description='A pure python rencoder',
    license='MIT',
    long_description=contents('README.txt'),
    author='Stephanos Papanikolopoulos',
    author_email='spapanik21@gmail.com',
    url='https://github.com/spapanik/pyrencode',
    download_url='https://github.com/spapanik/pyrencode/tarball/0.0.4',
    keywords=listify('KEYWORDS.txt'),
    classifiers=listify('CLASSIFIERS.txt'),
)
