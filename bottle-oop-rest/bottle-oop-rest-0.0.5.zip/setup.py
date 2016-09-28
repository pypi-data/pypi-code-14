from setuptools import setup

setup(
    name='bottle-oop-rest',
    version='0.0.5',
    packages=['borest'],
    url='https://github.com/jar3b/bottle-oop-rest',
    license='MIT',
    author='hello',
    author_email='hellotan@live.ru',
    description='Bottle.py OOP REST simple library',
    install_requires=[
        'bottle>=0.12.9',
        'gevent>=1.1.2'
    ]
)
