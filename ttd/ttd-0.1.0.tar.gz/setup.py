from setuptools import setup

setup(
    name="ttd",
    version="0.1.0",
    description="Time Till Done (ttd) is a simple progress bar for your long running Python scripts",
    long_description=open('README.rst').read(),
    author="Jarrod C Taylor",
    author_email="jarrod.c.taylor@gmail.com",
    url="https://github.com/JarrodCTaylor/ttd",
    license="WTFPL",
    py_modules=['ttd'],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Environment :: Console",
        "Topic :: Terminals",
        "Topic :: System :: Shells"
    ],
    tests_require=["nose"],
    test_suite="nose.collector",
)
