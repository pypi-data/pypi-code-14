from setuptools import setup

setup(
    name='my_sample',
    version='0.4.0',
    description='Not the most useful package',
    long_description='Check it out on GitHub...',
    keywords='sample pip tutorial',
    url='https://github.com/kylebebak/my_sample',
    download_url = 'https://github.com/kylebebak/my_sample/tarball/0.4.0',
    author='kylebebak',
    author_email='kylebebak@gmail.com',
    license='MIT',
    packages=['my_sample'],
    install_requires=[],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ]
)
