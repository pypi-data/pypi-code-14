from setuptools import setup


setup(
    name='Flask-StatsdTagged',
    version='0.7',
    url='https://github.com/forsberg/Flask-Statsd-Tagged/',
    license='BSD',
    author='Erik Forsberg',
    author_email='forsberg@efod.se',
    description='Flask extension for sending statsd data with tags, for use with telegraf statsd plugin',
    long_description=__doc__,
    py_modules=['flask_statsd_tagged'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'statsd',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
