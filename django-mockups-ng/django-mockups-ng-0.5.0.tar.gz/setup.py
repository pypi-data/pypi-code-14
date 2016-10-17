from setuptools import setup, find_packages


setup(
    name = 'django-mockups-ng',
    version = '0.5.0',
    description = 'Provides tools to auto generate content.',
    long_description = open('README.rst').read(),
    author = 'ifanr',
    author_email = 'ifanrx@ifanr.com',
    url = 'https://github.com/sorl/django-mockups',
    license = 'BSD',
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
