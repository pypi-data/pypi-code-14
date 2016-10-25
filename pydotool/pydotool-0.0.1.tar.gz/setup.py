from distutils.core import setup

setup(
    name="pydotool",
    version="0.0.1",
    author="Redhat Raptor",
    author_email="redhat.raptor@gmail.com",
    packages=["app"],
    include_package_data=True,
    url="http://pypi.python.org/pypi/pydotool_v001/",
    license="LICENSE.txt",
    description="A Python based tool for DigitalOcean",
    long_description=open("README.txt").read(),
    install_requires=[
        "cement",
        "requests",
        "python_hosts",
        "terminaltables"
    ],
)
