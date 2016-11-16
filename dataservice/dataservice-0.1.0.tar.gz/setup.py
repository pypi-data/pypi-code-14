from setuptools import setup


setup(name='dataservice',
        version='0.1.0',
        description='Duke Data Service Python Tools',
        url='https://github.com/benneely/dds',
        keywords='duke dds dataservice',
        author='Ben Neely',
        license='MIT',
        packages=['dataservice','dataservice.core'],
        install_requires=[
          'requests',
          'PyYAML',
        ],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'Topic :: Utilities',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
        ],
    )

