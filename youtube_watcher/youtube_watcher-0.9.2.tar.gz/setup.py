#!/usr/bin/env python3


from setuptools import setup


setup(name='youtube_watcher',
        version='0.9.2',
        description='A simple program to list new YouTube videos and download them',
        author='Steven J. Core',
        url='https://github.com/Sjc1000/youtube_watcher',
        author_email='42Echo6Alpha@gmail.com',
        license='GPL3.0',
        packages=['youtube_watcher'],
        zip_safe=False,
        include_package_data=True,
        install_requires=[
            'bs4',
            'youtube-dl'
            ],
        entry_points={
            'console_scripts': [
                'youtube_watcher = youtube_watcher.__init__:main'
                ]
            })
