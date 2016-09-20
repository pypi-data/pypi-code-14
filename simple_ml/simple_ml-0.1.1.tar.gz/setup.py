from setuptools import setup

setup(name='simple_ml',
      version='0.1.1',
      description='Machine learning tool simplified for hackers',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ],
      url='https://github.com/luanjunyi/simple-ml',
      author='Jerry Luan',
      author_email='luanjunyi@gmail.com',
      license='MIT',
      packages=['simple_ml'],
      install_requires=[
          'numpy',
          'scipy',
      ],
      zip_safe=False)
