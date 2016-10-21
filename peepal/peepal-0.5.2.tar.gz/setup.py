from distutils.core import setup
import re
import ast

with open('README.rst', encoding='utf-8') as file:
    long_description = file.read()

_version_re = re.compile(r'__version__\s*=\s*(.*)')

with open('peepal/__init__.py', encoding='utf-8') as file:
    version = ast.literal_eval(_version_re.search(file.read()).group(1))

setup(
    name = 'peepal',
    packages = ['peepal', 'peepal.middleware'], 
    version = version,
    description = 'A minimalist python 3 web framework.',
    long_description = long_description,
    author = 'Zhibin Jin',
    author_email = 'zbjin@yahoo.com',
    license = 'MIT',
    platforms = 'any',
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)
