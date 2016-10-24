from setuptools import setup

setup_params = dict(
    name='uh',
    use_scm_version=True,
    packages=['uh'],
    url='https://github.com/dmonroy/uh',
    license='MIT License',
    author='Darwin Monroy',
    author_email='contact@darwinmonroy.com',
    description='Upload Handler',
    install_requires=[
        'chilero'
    ],
    setup_requires=[
        'setuptools_scm'
    ]
)


if __name__ == '__main__':
    setup(**setup_params)
