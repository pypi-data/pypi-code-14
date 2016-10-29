from setuptools import find_packages, setup

setup(
    name='ducker',
    version='0.1.3',
    author='Jorge Maldonado Ventura',
    author_email='jorgesumle@freakspot.net',
    description='Program that lets you search with DuckDuckGo from the command line.',
    entry_points={
        'console_scripts': [
            'ducker=ducker:main',
            'duck=ducker:main'
        ],
    },
    license='GNU General Public License v3 (GPLv3)',
    keywords='CLI DuckDuckGo search terminal',
    url='https://notabug.org/jorgesumle/ducker',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
