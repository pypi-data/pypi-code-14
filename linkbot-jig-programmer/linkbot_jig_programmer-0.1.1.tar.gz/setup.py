#!/usr/bin/env python3

from setuptools import setup
import re

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('linkbot_jig_programmer/linkbot_jig_programmer.py').read(),
    re.M
    ).group(1)

setup(
    name = "linkbot_jig_programmer",
    packages = ["linkbot_jig_programmer", ],
    version = version,
    entry_points = {
        "console_scripts": ['linkbot-jig-programmer=linkbot_jig_programmer.linkbot_jig_programmer:main']
    },
    install_requires = ["PyLinkbot3 >= 3.0.0", 
                        "pystk500v2 >= 2.3.2", 
                        "pyserial == 2.7",
                        "crc16", ],
    description = "Tool for flashing Linkbot main-boards with a bootloader on"
        "the main programming jig.",
    zip_safe = False,
    include_package_data = True,
    author = "David Ko",
    author_email = "david@barobo.com",
    )

