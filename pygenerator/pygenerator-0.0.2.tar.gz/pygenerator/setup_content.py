SETUP = """import os
import sys

from setuptools import find_packages, setup


PYTHON3 = sys.version_info > (3, )
HERE = os.path.abspath(os.path.dirname(__file__))


def readme():
    with open(os.path.join(HERE, 'README.rst')) as f:
        return f.read()


def get_version():
    with open(os.path.join(HERE, '{{PROJECT_MAIN_PACKAGE}}/__init__.py'), 'r') as f:
        content = ''.join(f.readlines())
    env = {}
    if PYTHON3:
        exec(content, env, env)
    else:
        compiled = compile(content, 'get_version', 'single')
        eval(compiled, env, env)
    return env['__version__']


setup(
    name='{{PROJECT_NAME}}',
    version=get_version(),
    description='{{PROJECT_DESCRIPTION}}',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    keywords='{{PROJECT_KEYWORDS}}',
    url='{{PROJECT_URL}}',
    author='{{PROJECT_AUTHOR}}',
    author_email='{{PROJECT_AUTHOR_EMAIL}}',
    license='{{PROJECT_LICENSE}}',
    packages=find_packages(),
    test_suite='{{PROJECT_MAIN_PACKAGE}}.tests',
    scripts={{PROJECT_SCRIPTS}},
    install_requires={{PROJECT_REQUIRES}},
    tests_require={{PROJECT_TESTS_REQUIRES}},
    extras_require={
        'test': {{PROJECT_EXTRAS_REQUIRES}},
    },
    include_package_data=True,
    zip_safe=False
)
"""
