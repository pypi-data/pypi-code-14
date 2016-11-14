from setuptools import setup, find_packages

setup(
    name="coffeebuzz",
    version="1.0.0",
    description="A simple function for CoffeeBuzz for macOS.",
    long_description="""import coffeebuzz

def changeCoffeeStatus(targetMode)
targetMode should be one of 'off', 'doze', and 'buzz'""",
    url="https://gitlab.com/arrrggghhh/coffeebuzz",
    author="HyeonChol Jang",
    author_email="zxcxz7@icloud.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3.5",
        "Topic :: Utilities"
    ],
    keywords="macos coffeebuzz",
    py_modules=["coffeebuzz"],
)