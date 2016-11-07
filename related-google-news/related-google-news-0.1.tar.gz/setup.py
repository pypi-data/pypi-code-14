from distutils.core import setup

setup(
    name='related-google-news',
    packages=['related_google_news'],
    version='0.1',
    description='Gets collections of related news from Google News RSS feed',
    author='Veronica Lynn',
    author_email='me@veronicaelynn.com',
    url='https://github.com/kolvia/related-google-news',
    download_url='https://github.com/kolvia/related-google-news/tarball/0.1',
    keywords=['scraper', 'news'],
    classifiers=[],
    install_requires=['bs4', 'feedparser']
)
