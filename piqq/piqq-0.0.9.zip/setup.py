from setuptools import setup

setup(
    name='piqq',
    version='0.0.9',
    packages=['piqq', 'piqq.exceptions'],
    url='https://git.hellotan.ru/jar3b/piqq',
    license='MIT',
    author='jar3b',
    author_email='hellotan@live.ru',
    description='PIQQ - The OOP-based add-on for aioamqp library',
    install_requires=[
        'aioamqp==0.8.2'
    ]
)
