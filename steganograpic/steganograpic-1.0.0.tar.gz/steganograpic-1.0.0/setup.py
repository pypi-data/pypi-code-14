from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='steganograpic',
    version='1.0.0',
    description='Hide text inside image',
    long_description=readme(),
    url='https://github.com/arthursz/steganograpic',
    author='Arthur Zettler & Natasha Flores',
    author_email='arthur.zettler@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Operating System :: Unix'
    ],
    keywords='cryptography',
    install_requires=[
        'Pillow==3.4.2',
        'bitarray==0.8.1'
    ],
    entry_points={
        'console_scripts': ['steganograpic=steganograpic.command_line:main'],
    },
    zip_safe=True
)
