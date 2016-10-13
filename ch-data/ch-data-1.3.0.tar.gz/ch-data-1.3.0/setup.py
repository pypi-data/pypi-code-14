import os, json
from distutils.core import setup

package = json.load(open("./package.json"))

setup(
        name = "ch-data",
        packages = ["ch-data"],
        package_dir = {"ch-data": "."},
        package_data = {
            "ch-data": [
                "*.js",
                "*.json",
                "package.json"
            ]
        },
        version = package["version"],
        description = "PyPI package for data files",
        author = "Diwank Singh",
        author_email = "diwank.singh@gmail.com",
        url = "https://github.com/creatorrr/ch-data")

