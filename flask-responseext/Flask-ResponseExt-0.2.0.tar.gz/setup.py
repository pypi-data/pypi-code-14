from setuptools import setup


setup(
    name='Flask-ResponseExt',
    version='0.2.0',
    url='https://github.com/joelcolucci/flask-responseext',
    license='MIT',
    author='Joel Colucci',
    author_email='joelcolucci@gmail.com',
    description='An extension of the Flask Response class.',
    long_description=__doc__,
    packages=['flask_responseext'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
