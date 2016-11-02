from distutils.core import setup

setup(
    name="fugu",
    version="0.0.1",
    url="https://github.com/beardypig/fugu",
    author="beardypig",
    author_email="beardypig@users.noreply.github.com",
    license="Apache 2.0",
    packages=["fugu"],
    package_dir={"": "src"},
    classifiers=["Development Status :: 3 - Alpha",
                 "Environment :: Console",
                 "Operating System :: POSIX",
                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3.3",
                 "Programming Language :: Python :: 3.4",
                 "Programming Language :: Python :: 3.5",
                 "Topic :: Multimedia :: Sound/Audio",
                 "Topic :: Multimedia :: Video",
                 "Topic :: Utilities"]
)
