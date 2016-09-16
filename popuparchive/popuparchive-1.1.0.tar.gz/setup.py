from distutils.core import setup

setup(
    name="popuparchive",
    packages=["popuparchive"],
    version="1.1.0",
    description='Python client for interacting with the Pop Up Archive API.',
    author='Pop Up Archive',
    author_email='edison@popuparchive.com',
    url='https://github.com/popuparchive/pua-sdk-python',
    download_url=' https://github.com/popuparchive/pua-sdk-python/tarball/1.0.0',
    license='Apache License 2.0',
    keywords=[
        'transcription',
        'audio',
        'archives',
        'mp3',
        'radio',
        'podcasts'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=[
        'requests',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ]
)
