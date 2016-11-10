from distutils.core import setup

setup(
    name="Slowloris_IMproved",
    py_modules=["sim"],
    entry_points={"console_scripts": ["sim=sim:main"]},
    version="0.3.2",
    description="IMproved low bandwidth DoS tool. Slowloris rewrite in Python, original by Gokberk Yaltirakli.",
    author="Robin Kanters",
    author_email="robin@robinkanters.nl",
    url="https://github.com/robinkanters/slowloris",
    keywords=["dos", "http", "slowloris"]
)
