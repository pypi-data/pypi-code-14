from setuptools import setup, find_packages

setup(
    name="peoplegraph-api-client",
    version="0.1.0",
    license='MIT License',
    packages=["peoplegraph_api_client"],
    url="https://github.com/deep-compute/peoplegraph-api-client",
    download_url="https://github.com/deep-compute/peoplegraph-api-client/tarball/0.1.0",
    install_requires=[
        "python-dateutil",
        "requests>=2.11",
    ],
    author="Deep-Compute",
    author_email="rebello.anthony@gmail.com",
    description="Peoplegraph api client",
    keywords=["peoplegraph"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "peoplegraph = peoplegraph_api_client.main:main",
        ]
    }
)
