from setuptools import find_packages, setup

setup(
    name="drfdocs-louielu",
    version=__import__('rest_framework_docs').__version__,
    author="louielu",
    author_email="louie.lu@hopebaytech.com",
    packages=find_packages(),
    include_package_data=True,
    url="https://louie.lu",
    license='BSD',
    description="patch for Documentation for Web APIs made with Django Rest Framework.",
    long_description=open("README.md").read(),
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
)
