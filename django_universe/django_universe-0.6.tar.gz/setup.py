import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='django_universe',
    version='0.6',
    packages=['django_universe'],
    description='A line of description for v0.5',
    long_description=README,
    author='jerin',
    author_email='jerinzam@gmail.com',
    url='https://github.com/jerinzam/django-universe/',
    download_url='https://github.com/jerinzam/django-universe/tarball/0.6',
    license='MIT',
    install_requires=[
        'Django>=1.6',
    ]
)
