from setuptools import setup, find_packages

install_requires = ['django>=1.7', 'requests>=2.0.0']

setup(
    name='django-opencred',
    version=__import__('opencred').__version__,
    description='OpenCred integration for Django.',
    long_description="""""",
    author='OpenCred',
    author_email='info@opencred.io',
    url='https://github.com/opencred/django-opencred',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=install_requires,
    test_suite='tests.runtests',
)
