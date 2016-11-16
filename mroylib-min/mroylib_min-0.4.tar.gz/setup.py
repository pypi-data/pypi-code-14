

from setuptools import setup, find_packages


setup(name='mroylib_min',
    version='0.4',
    description='a simple way to use mongo db, let db like dict',
    url='https://github.com/Qingluan/.git',
    author='Qing luan',
    author_email='darkhackdevil@gmail.com',
    license='MIT',
    zip_safe=False,
    packages=find_packages(),
    install_requires=['redis', 'pymysql', 'bs4','requests','termcolor','bson','simplejson','pysocks'],

)


