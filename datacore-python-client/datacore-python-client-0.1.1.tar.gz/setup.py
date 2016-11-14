import setuptools


setuptools.setup(
    name='datacore-python-client',
    version='0.1.1',
    description='Python Client for accessing datacore RESTfully',
    url='https://github.com/Bodaclick/datacore-python-client',
    author='Vincent Medina',
    author_email='vincent@everymundo.com',
    packages=['datacore'],
    install_requires=[
        "requests"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5',
      ],
    keywords="em datacore everymundo",
    zip_safe=False
)
