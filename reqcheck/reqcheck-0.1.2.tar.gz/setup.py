from setuptools import setup, find_packages

setup(
    name = 'reqcheck',
    version = '0.1.2',
    packages = find_packages(),
    install_requires = [
        'requests',
        'six',
        'tabulate',
    ],
    author = 'Jozef Leskovec',
    author_email = 'jozefleskovec@gmail.com',
    description = 'Compare installed Python package versions with PyPI',
    license = 'MIT',
    keywords = 'requirements check compare installed virtualenv venv pypi package packages version versions',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    url = 'https://github.com/jaleskovec/reqcheck',
    entry_points = {
        'console_scripts': [
            'reqcheck = reqcheck:cmdline',
        ],
    },
)
