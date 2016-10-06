import os
from setuptools import find_packages, setup

try:
    from pypandoc import convert

    def read_md(f):
        return convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, "
          "could not convert Markdown to RST")

    def read_md(f):
        return open(f, 'r', encoding='utf-8').read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-civil',
    version='0.0.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',  # example license
    description='A toolkit for social Django projects',
    long_description=read_md('README.md'),
    url='https://www.github.com/millers7/django-civil',
    author='Elwin Arens',
    author_email='elwin@millers7.com',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
