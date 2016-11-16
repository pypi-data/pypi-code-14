

from setuptools import setup, find_packages


setup(name='mroylib_min',
    version='0.1',
    description='a simple way to use mongo db, let db like dict',
    url='https://github.com/Qingluan/.git',
    author='Qing luan',
    author_email='darkhackdevil@gmail.com',
    license='MIT',
    zip_safe=False,
    packages=find_packages(),
    install_requires=['requests','termcolor','bson','simplejson','pysocks'],

)


