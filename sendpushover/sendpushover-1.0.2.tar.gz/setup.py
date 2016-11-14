from setuptools import setup, find_packages

setup(
    name="sendpushover",
    version="1.0.2",
    description="A simple function for pushover.net",
    long_description="""import sendpushover

def sendPush(userkey, appkey, message, *, device='', title='', url='', url_title='', priority='', timestamp='', sound='')""",
    url="https://gitlab.com/arrrggghhh/pushover",
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
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.5",
        "Topic :: Utilities"
    ],
    keywords="pushover notification",
    install_requires=["requests >= 2.11.1"],
    py_modules=["sendpushover"],
)