"""Lightweight API wrapper for
`browser-info.net <http://www.browser-info.net/useragents>`_.
"""

from lxml import html
import urllib

__version__ = '0.2.0'
__repository__ = 'https://github.com/stylesuxx/browserinfo'

baseUrl = 'http://www.browser-info.net/useragents'
recentXpath = ('(//div[@class="datatable"])[1]//tr/td[2]/a/text()')
popularXpath = ('(//div[@class="datatable"])[2]//tr/td[2]/a/text()')
limit = 20


class BrowserinfoError(Exception):
    """Base class for exceptions thrown by this library.

        :param message: The error message
        :type message: str
    """
    def __init__(self, message):
        super(BrowserinfoError, self).__init__(message)


class DOMChanged(BrowserinfoError):
    """Raised when the DOM is not parsable.

    Over time, the page might change and no longer be parsable with the current
    rule set. In case this happens, this exception is raised with a link to
    the repository to file an issue.
    """
    def __init__(self):
        message = ('The site structure changed and is no longer parsable. '
                   'Please file an issue on github: %s' % __repository__)
        super(DOMChanged, self).__init__(message)


def _getResults(amount, xPath):
    amount = _sanitizeAmount(amount)
    f = urllib.urlopen(baseUrl)
    tree = html.fromstring(f.read())
    items = tree.xpath(xPath)
    items = items[:amount]

    if len(items) != amount:
        raise DOMChanged

    return items


def _sanitizeAmount(amount):
    if amount < 0:
        return 0

    if amount > limit:
        return limit

    return amount


def popular(amount=20):
    """Fetches populsr UA strings.

    Retrieves most popular UA strings, up to a maximum of 20.

    :param amount: The amount of UA strings to retrieve
    :type amount: int

    :returns: List of UA strings
    :rtype: list

    :raises DOMChanged: When retrieved amount does not match requested amount

    :Example:

    >>> import browserinfo
    >>> browserinfo.popular(1)
    ['Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.6.01001)']


    """

    return _getResults(amount, popularXpath)


def recent(amount=20):
    """Fetches recent UA strings.

    Retrieves most recent UA strings, up to a maximum of 20.

    :param amount: The amount of UA strings to retrieve
    :type amount: int

    :returns: List of UA strings
    :rtype: list

    :raises DOMChanged: When retrieved amount does not match requested amount

    :Example:

    >>> import browserinfo
    >>> browserinfo.recent(1)
    ['Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36']

    """

    return _getResults(amount, recentXpath)
