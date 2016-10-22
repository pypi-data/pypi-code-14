from setuptools import setup, find_packages
setup(
    name='oolong',
    version='0.1',
    keywords=('daily tool', 'common code'),
    description='common tool',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
    ],
    license='MIT License',
    author='roc.zhao',
    author_email='peng.zhao@tongji.edu.cn',
    packages=find_packages(),
    platforms='any',
)
