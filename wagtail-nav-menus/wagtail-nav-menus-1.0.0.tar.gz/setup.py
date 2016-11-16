from setuptools import setup, find_packages

setup(
    name="wagtail-nav-menus",
    version="1.0.0",
    author="David Burke",
    author_email="david@thelabnyc.com",
    description="Wagtail Nav Menus is a app to provide highly customizable menus in wagtail by leveraging StreamFields.",
    license="Apache License",
    keywords="django wagtail",
    url="https://gitlab.com/thelabnyc/wagtail-nav-menus",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires=[
        'wagtail>=1.6.2',
    ]
)
