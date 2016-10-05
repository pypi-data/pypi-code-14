from zquery import __version__
from setuptools import setup


def read(f):
    return open(f, encoding='utf-8').read()

setup(
    name='zquery',
    version=__version__,
    description='Zhihu UNOFFICIAL API library based on Python3',
    author='wisedoge',
    author_email='wisedoge@outlook.com',
    url='https://github.com/WiseDoge/zquery',
    packages=[
        'zquery'
    ],
    py_modules=['run'],
    include_package_data=True,
    platforms='any',
    install_requires=[
        'prettytable',
        'requests',
        'bs4',
        'lxml',
        'docopt',
        'pillow',
    ],
    entry_points={
        'console_scripts': ['zquery=run:cli']
    },
    license='apache 2.0',
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython'
    ]
)
