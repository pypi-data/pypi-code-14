from distutils.core import setup

setup(
    name = 'feelinglucky',
    version = '0.1.4',
    description = 'This package gives you the url of the first google search result of a query',
    author = 'Dinesh Rai',
    author_email = 'dinesh@techiemd.com',
    url = 'https://github.com/DineshRai/feelinglucky', 
    py_modules=['feelinglucky'],
    install_requires=[
        "requests",
        "BeautifulSoup4"
    ]
)