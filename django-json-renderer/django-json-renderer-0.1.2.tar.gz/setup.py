from distutils.core import setup
import os
import django_json_renderer as renderer

if os.path.exists('README.rst'):
    with open('README.rst') as f:
        long_description = f.read()

setup(
    name = 'django-json-renderer',
    version = renderer.__version__,
    description = renderer.__description__,
    long_description = long_description,
    author = renderer.__author__,
    author_email = 'ticshot@gmail.com',
    url = 'https://github.com/HakurouKen/django-render-json',
    py_modules = ['django_json_renderer'],
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    license = renderer.__license__
)
