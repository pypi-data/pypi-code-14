from setuptools import find_packages, setup

setup(
    name='Fifty-Flask',
    version='1.2.0',
    url='https://bitbucket.org/50onred/fifty/overview',
    license='BSD',
    author='Craig Slusher',
    author_email='craig@50onred.com',
    description='Flask enhancements.',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'flask>=0.11',
    ],
    tests_require=[
        'nose'
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
