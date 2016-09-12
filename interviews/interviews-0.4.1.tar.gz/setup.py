from setuptools import find_packages, setup

setup(
    name="interviews",
    version="0.4.1",
    author="Fabien Schwob",
    author_email="github@x-phuture.com",
    license="BSD",
    url="https://github.com/jibaku/interviews",
    packages=find_packages(exclude=[]),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
