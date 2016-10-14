from setuptools import setup, find_packages


setup(
    name="gwebsocket",
    version='0.9.8',
    url="https://bitbucket.org/btubbs/gwebsocket",
    author="Brent Tubbs",
    author_email="brent.tubbs@gmail.com",
    description=("Websocket handler for the gevent pywsgi server, a Python "
                 "network library"),
    long_description=open("README.rst").read(),
    download_url="https://bitbucket.org/btubbs/gwebsocket",
    packages=find_packages(exclude=["examples", "tests"]),
    license=open('LICENSE').read(),
    zip_safe=False,
    install_requires=("gevent"),
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
