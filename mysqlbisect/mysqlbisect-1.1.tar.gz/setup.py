from setuptools import setup

setup(
    name='mysqlbisect',
    description='Perform a binary search in a large number of MySQL database dumps',
    author='Raphael Michel',
    author_email='mail@raphaelmichel.de',
    url='https://github.com/raphaelm/mysql-bisect',
    keywords=['database', 'backup', 'bisect', 'search', 'mysqldump'],
    classifiers=[
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: Database'
    ],
    version='1.1',
    py_modules=['mysqlbisect'],
    install_requires=[
        'Click',
        'mysqlclient'
    ],
    entry_points='''
[console_scripts]
mysqlbisect=mysqlbisect:bisect
    ''',
)
