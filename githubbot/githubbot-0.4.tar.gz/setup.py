from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = ''.join(f.readlines())

setup(
    name='githubbot',
    version='0.4',
    description='Automatically labels repositories\' issues or pull requests on GitHub.',
    long_description=long_description,
    author='Jakub Tomanek',
    author_email='tomanj23@fit.cvut.cz',
    license='Public Domain',
    url='https://github.com/tomanj23/githubBot',
    install_requires=['Flask','Jinja2','MarkupSafe','Werkzeug','click','itsdangerous','requests'],
    packages=find_packages(),
    package_data={'githubbot':['static/*.css','templates/*.html']},
    entry_points={
        'console_scripts': [
            'githubbot = githubbot.githubbot:main',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Version Control'
        ],
)