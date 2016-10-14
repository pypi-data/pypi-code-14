from setuptools import setup, find_packages

setup(
    name = "wagtail-hallo-plugins",
    version = "1.0.2",
    author = "David Burke",
    author_email = "david@thelabnyc.com",
    description = ("A collection of plugins one can easily enable for wagtail's rich text editor - hallo."),
    license = "Apache License",
    keywords = "django wagtail hallo",
    url = "https://gitlab.com/thelabnyc/wagtail_hallo_plugins",
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
        'wagtail>=1.6.0',
    ]
)
