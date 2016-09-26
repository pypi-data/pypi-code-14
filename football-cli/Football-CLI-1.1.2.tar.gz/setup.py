from distutils.core import setup
from setuptools import find_packages

setup(
    name='Football-CLI',
    version='1.1.2',
    packages=find_packages(),
    url='https://github.com/jctissier/Football-CLI',
    license='MIT',
    author='Jean-Claude Tissier',
    author_email='jeanclaude.tca@gmail.com',
    entry_points = {
        'console_scripts':[
            'Football-CLI = Football_CLI.__main__:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    description='Football Stats & Live Streams links CLI from your terminal',
    install_requires=[
    'beautifulsoup4',
    'praw==3.5.0',
    'termcolor==1.1.0',
    'requests==2.10.0'
    ],
    keywords='Football stats web scraper'
)
