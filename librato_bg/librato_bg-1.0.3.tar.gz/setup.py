from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst', 'md')
except ImportError:
    print("Warning: pypandoc module not found, could not convert Markdown to RST")
    long_description = open('README.md', 'r').read()


def _is_requirement(line):
    """Returns whether the line is a valid package requirement."""
    line = line.strip()
    return line and not (line.startswith("-r") or line.startswith("#"))


def _read_requirements(filename):
    """Returns a list of package requirements read from the file."""
    requirements_file = open(filename).read()
    return [line.strip() for line in requirements_file.splitlines()
            if _is_requirement(line)]


base_packages = _read_requirements("requirements/base.txt")
test_packages = _read_requirements("requirements/tests.txt")


setup(
    name='librato_bg',
    version=__import__('librato_bg').__version__,
    description="Enables submitting of Librato events in a background thread",
    long_description=long_description,

    url='https://github.com/nyaruka/python-librato-bg',
    license='MIT License',

    author='Nyaruka',
    author_email='code@nyaruka.com',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    packages=['librato_bg'],
    install_requires=base_packages,
    tests_require=base_packages + test_packages,
)
