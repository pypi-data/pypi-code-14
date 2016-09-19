from setuptools import setup

setup(
    name='buku',
    version='0.0.6',
    description='Powerful command-line bookmark manager. Your mini web!',
    url='https://github.com/jarun/Buku',
    author='jarun',
    author_email='ovv@outlook.com',
    license='GPLv3',
    packages=['console'],
    zip_safe=False,
    include_package_data=True,
    install_requires=['beautifulsoup4>=4.4.1', 'cryptography>=1.3.2'],
    test_suite="tests",
    entry_points={
        'console_scripts': ['buku=console:entry_point']
    },
)
