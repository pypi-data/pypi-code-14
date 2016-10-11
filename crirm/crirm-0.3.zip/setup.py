from setuptools import setup, find_packages

setup(
      description='CRIteria REMove. Delete files based on various criteria like age, file size etc.',
      author='Daniel Eder',
      url='http://github.com/lycis/crirm',
      download_url='http://github.com/lycis/crirm',
      author_email='daniel@deder.at',
      version=0.3,
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      name='crirm',
      license='MIT',
      entry_points={
        'console_scripts': [
            'crirm=crirm.main:main',
        ],
      }
)