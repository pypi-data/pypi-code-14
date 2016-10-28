from setuptools import setup, find_packages

setup(
    name='django-filepicker-model',
    version='0.1.1',
    description='Filepicker for Django without a frontend',
    author='jpwagner',
    author_email='jim@sevenleague.co',
    url='http://github.com/sevenleague/django-filepicker-model',
    packages=find_packages(),
    install_requires=['django >= 1.3','requests', 'filepicker'],
    zip_safe=False,
)