import os
from setuptools import setup

setup(
    name = "starbucks-wifi-login-in-kor",
    version = "1.1",
    author = "jinsub ahn",
    author_email = "jinniahn@gmail.com",
    description = ("When you go starbucks in korea, you can be asked your information. "
                   "This program will input the information based on your data"),
    license = "BSD",
    keywords = "starbucks, autologin",
    url = "https://github.com/jinniahn/auto_starbuck_wifi_login",
    packages=['starbucks_wifi'],
    package_data={'starbucks_wifi': ['webdriver/*']},
    scripts=['bin/starbucks_login.py'],
    install_requires=[
        'selenium',
    ],    
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
