#from distutils.core import setup
from setuptools import setup


setup(
    name='redishammingdist',
    version='0.1',
    packages=[
        'redishammingdist',
    ],
    license='MIT',
    url='http://github.com/phelimb/redis-hamming-distance',
    description='.',
    author='Phelim Bradley',
    author_email='wave@phel.im',
    install_requires=[
            'redispartition'],
)
