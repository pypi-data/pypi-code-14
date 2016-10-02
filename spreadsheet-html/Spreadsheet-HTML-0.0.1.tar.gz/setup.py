from setuptools import setup, find_packages
import Spreadsheet.HTML

setup(
    name='Spreadsheet-HTML',
    version=Spreadsheet.HTML.__version__,
    description='Just another HTML table generator (for Python)',
    author='Jeff Anderson',
    author_email='jeffa@cpan.org',
    url='https://github.com/jeffa/Spreadsheet-HTML-python',
    license='Artistic',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['HTML-Auto'],
    classifiers=[
        "Topic :: Text Processing :: Markup :: HTML",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Artistic License",
    ],
    long_description="""\
    Just another HTML table generator.
    --------------------------------

    Generate HTML tables with ease (HTML4, XHTML and HTML5).
"""
)
