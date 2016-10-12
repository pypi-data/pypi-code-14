from setuptools import setup, find_packages


setup(
    name="devpi-metawheel",
    description=open('README').read(),
    version='0.3',
    author="Polyconseil",
    author_email="opensource+devpi-metawheel@polyconseil.fr",
    url="https://github.com/Polyconseil/devpi-metawheel",
    license="MIT",
    keywords="devpi plugin",
    install_requires=[
        'packaging>=15.3',
    ],
    entry_points={
        'devpi_server': [
            "devpi-metawheel = devpi_metawheel.main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python",
    ],
)
