from distutils.core import setup

setup(
    name="lsq_linear",
    version="0.1.0",
    description="Implementation of scipy.optimize.lsq_linear for old scipy version",
    author="xica",
    author_email="info@xica.net",
    url="https://github.com/xica/scipy-lsq_linear",
    packages=["lsq_linear"],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS"
    ],
    license="BSD",
    install_requires=[
        "numpy>=1.8.1",
        "scipy>=0.14.0,<0.17.0"
    ]
)
