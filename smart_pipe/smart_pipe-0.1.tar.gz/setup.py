from setuptools import setup

setup(
    name='smart_pipe',
    version='0.1',
    author="Max Lapan",
    author_email="max.lapan@gmail.com",
    description="Simple and fast key-value container optimized for sequential read, "
                "supporting indexed access and compression",
    license="GPL-v3",
    keywords="storage compressed sequential",
    url="http://smart-pipe.readthedocs.io/",
    packages=['smart_pipe'],
    scripts=["sp.py"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Software Development :: Libraries",
        "Topic :: Database",
    ]
)
