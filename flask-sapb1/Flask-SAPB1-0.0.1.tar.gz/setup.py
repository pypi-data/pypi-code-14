"""
Flask-SAPB1
-------------

"""
from setuptools import find_packages, setup

setup(
    name='Flask-SAPB1',
    version='0.0.1',
    url='https://github.com/ideabosque/Flask-SAPB1',
    license='MIT',
    author='Idea Bosque',
    author_email='ideabosque@gmail.com',
    description='Use to connect SAP B1 DI API.',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='win32',
    install_requires=['Flask', 'pymssql', 'pywin32'],
    download_url = 'https://github.com/ideabosque/Flask-SAPB1/tarball/0.0.1',
    keywords = ['SAP B1', 'SAP Business One', 'DI'], # arbitrary keywords
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Framework :: Flask',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
