# setup.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

from setuptools import setup

if __name__ == '__main__':

    long_description = open('README').read()

    setup(
        name='chesstab',
        version='0.41.5',
        description='Database for chess games',
        author='Roger Marsh',
        author_email='roger.marsh@solentware.co.uk',
        url='http://www.solentware.co.uk',
        package_dir={'chesstab':''},
        packages=[
            'chesstab',
            'chesstab.core', 'chesstab.gui', 'chesstab.help',
            'chesstab.db', 'chesstab.dpt', 'chesstab.sqlite', 'chesstab.apsw',
            'chesstab.fonts',
            'chesstab.about',
            ],
        package_data={
            'chesstab.about': ['LICENCE', 'CONTACT'],
            'chesstab.fonts': ['*.TTF', '*.zip'],
            'chesstab.help': ['*.rst', '*.html'],
            },
        long_description=long_description,
        license='BSD',
        classifiers=[
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Operating System :: OS Independent',
            'Topic :: Games/Entertainment :: Board Games',
            'Intended Audience :: End Users/Desktop',
            'Development Status :: 4 - Beta',
            ],
        install_requires=['rmappsup==0.38.10', 'pgn==0.10.3', 'uci==0.1.1'],
        dependency_links=[
            'http://solentware.co.uk/files/rmappsup-0.38.10.tar.gz',
            'http://solentware.co.uk/files/pgn-0.10.3.tar.gz',
            'http://solentware.co.uk/files/uci-0.1.1.tar.gz',],
        )
