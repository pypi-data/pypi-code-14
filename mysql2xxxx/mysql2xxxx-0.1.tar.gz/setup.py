from setuptools import setup

setup(
    name='mysql2xxxx',
    version='0.1',
    description='Includes the script mysql2json for getting JSON from a MySQL database',
    author='David D Lowe',
    author_email='daviddlowe.flimm@gmail.com',
    url='https://github.com/Flimm/mysql2xxxx-python',
    scripts=[
        'mysql2json.py',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=['mysqlclient'],
)
