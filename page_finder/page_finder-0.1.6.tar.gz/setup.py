from setuptools import setup
from setuptools.extension import Extension
from page_finder import __version__

setup(
    name='page_finder',
    version=__version__,
    url='https://github.com/scrapinghub/page_finder',
    author='page_finder developers',
    maintainer='Pedro Lopez-Adeva Fernandez-Layos',
    maintainer_email='pedro@scrapinghub.com',
    install_requires=['numpy'],
    packages=['page_finder'],
    ext_modules=[Extension("page_finder.edit_distance",
                 sources=["page_finder/edit_distance.c"])],
    license='MIT',
    keywords=['crawler', 'frontier', 'scrapy', 'web', 'requests'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
