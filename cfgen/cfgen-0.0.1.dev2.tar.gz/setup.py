from setuptools import setup

setup(
    name="cfgen",
    version="0.0.1.dev2",
    description="Configuration tool for configuration files",
    author="Renat Zhilkibaev",
    author_email="rzhilkibaev@gmail.com",
    license="MIT",
    url="https://github.com/rzhilkibaev/cfgen",
    packages=["cfgen"],
    install_requires=["docopt", "future", "jinja2"],
    entry_points={"console_scripts": ["cfgen=cfgen.cfgen:main"]},
)
