from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='habu',
    version='0.0.1',
    description='Penetration Testing Utils',
    long_description=readme,
    author='Fabian Martinez Portantier',
    author_email='fportantier@securetia.com',
    url='https://github.com/securetia/habu',
    license=license,
    install_requires=[
        'Click',
        'Requests',
    ],
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    entry_points='''
        [console_scripts]
        habu.myip=habu.cli.myip:myip
    ''',
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    keywords = ['security'],
    zip_safe=False,
    test_suite='pyroma',
)

