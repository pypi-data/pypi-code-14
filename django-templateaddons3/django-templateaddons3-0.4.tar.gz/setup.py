from setuptools import setup, find_packages

install_requires = [
    'Django>=1.8,<1.11',
]


setup(
    name='django-templateaddons3',
    version='0.4',
    url='https://github.com/django-templateaddons/django-templateaddons3',
    download_url='https://github.com/django-templateaddons/django-templateaddons3/releases',
    author='django-templateaddons',
    author_email='django-templateaddons@github.com',
    license='BSD',
    description="A set of tools for use with templates of the Django "
                "framework: additional template tags, context processors "
                "and utilities for template tag development.",
    long_description=open('README.rst').read(),
    platforms='Any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: JavaScript',
        'Topic :: Internet :: WWW/HTTP :: Site Management'
    ],
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,
)
