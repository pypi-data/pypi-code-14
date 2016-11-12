from distutils.core import setup
import os 

del os.link

setup(
    name="listdownloader",
    version="0.1.1",
    author="Samer Afach",
    author_email="samer@afach.de",
    packages=["listdownloader"],
    include_package_data=True,
    url="https://git.afach.de/samerafach/ListDownloader",
    description="Downloads a list of files",
    install_requires=[],
    scripts=['bin/downloadlist.py']
)
