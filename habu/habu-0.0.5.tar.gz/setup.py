from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='habu',
    version='0.0.5',
    description='Ethical Hacking Utils',
    long_description=readme,
    author='Fabian Martinez Portantier',
    author_email='fportantier@securetia.com',
    url='https://github.com/securetia/habu',
    license='GNU General Public License v3 (GPLv3)',
    install_requires=[
        'Click',
        'Requests',
    ],
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    entry_points='''
        [console_scripts]
        habu.ip=habu.cli.cmd_ip:cmd_ip
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
    ],
    keywords = ['security'],
    zip_safe=False,
    test_suite='pyroma',
)

