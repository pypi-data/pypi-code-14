from setuptools import setup

with open('README.rst') as f:
    long_description = ''.join(f.readlines())

setup(
    name='pytwitterwallv',
    version='0.7.1',
    description='Console and web simple client for Twitter',
    long_description=long_description,
    author='Vojtech Knaisl',
    author_email='vknaisl@gmail.com',
    keywords='twitter,tweets',
    license='Public Domain',
    url='https://github.com/vknaisl/pytwitterwallv',
    packages=['pytwitterwallv'],
    include_package_data = True,
    package_data={
        "pytwitterwallv": ["pytwitterwallv/templates"]}
    ,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application'
    ],
    setup_requires=['pytest-runner'],
    install_requires=[
        'requests',
        'jinja2',
        'click',
        'flask'
    ],
    tests_require=[
        'flexmock',
        'betamax',
        'pytest'
    ],
    entry_points={
        'console_scripts': [
            'pytwitterwallv=pytwitterwallv.pytwitterwallv:cli'
        ]
    },
)
