from setuptools import setup, find_packages

setup(
        name = "droigo",
        version = "0.2.7",
        keywords = "droigo golang",
        description = "Golang coding standard tools for Droi",
        license = "BSD",
        author = "Fiathux Su",
        author_email = "fiathux@gmail.com",
        url = "http://gitlab.droi.com/fxcat/golang4all",
        platforms = "any",
        packages = ["droigotools"],
        entry_points = {
            "console_scripts":[
                "droigo = droigotools:main"
                ]
            }
        )
