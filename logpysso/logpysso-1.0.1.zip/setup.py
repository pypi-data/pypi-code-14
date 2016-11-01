from distutils.core import setup

setup(
    name='logpysso',
    version='1.0.1',
    packages=['logpysso'],
    url='http://logpresso.com',
    license='',
    author='hando.kim',
    author_email='hando.kim@eediom.com',
    description='logpresso python client',
    classifier = [
        'Topic:: Software Development:: Libraries',
        'Programming Language :: Python ::3.5'
    ],
    package_data = {'logpysso':['araqne-logdb-client-1.0.5-package.jar'],},
)
