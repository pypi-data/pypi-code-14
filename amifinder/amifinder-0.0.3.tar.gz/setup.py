from setuptools import setup

setup(name='amifinder',
      version='0.0.3',
      description='Command line tool to find AMI IDs for a few OS',
      url='https://github.com/mbrannigan/amifinder',
      author='mbrannigan',
      author_email='mikejbrannigan@gmail.com',
      license='MIT',
      packages=['amifinder'],
      zip_safe=False,
      install_requires=[
          'click',
          'boto3',
      ],
      keywords=[
          'aws',
          'amazon web services',
          'ami',
          'amazon machine images',
          'automation',
      ],
      entry_points={
          'console_scripts': ['amifinder=amifinder.cli:cli'],
      },
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Development Status :: 4 - Beta',
      ],
      )
