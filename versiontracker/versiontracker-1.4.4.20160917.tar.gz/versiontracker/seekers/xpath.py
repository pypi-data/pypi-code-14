import re
from urllib.parse import urljoin

from lxml.html.soupparser import fromstring
import requests

from versiontracker.baseseekers import BaseSeeker, download


_TRASH_RE = re.compile(r"(?s)<!--.*?-->|<\?.*?\?>")
_PROTOCOL_RE = re.compile(r"^(ht|f)tps?://")
_XPATH_PARAMS = {
    "namespaces": {
        "re": "http://exslt.org/regular-expressions"
    }
}


def _xpath_match_value(xpath_match):
    try:
        xpath_match = xpath_match[0]
    except IndexError:
        pass
    if isinstance(xpath_match, str):
        return xpath_match.strip()
    elif isinstance(xpath_match, list):
        return " ".join(xpath_match)
    else:
        return xpath_match.text_content().strip()


def _value_from_xpath(root, xpath):
    return _xpath_match_value(root.xpath(xpath, **_XPATH_PARAMS))


class Seeker(BaseSeeker):

    def _complete_xpath(self, xpath):
        if xpath is None:
            return xpath
        if self.base:
            return self.base + xpath
        return xpath

    def __init__(self, data):
        super(Seeker, self).__init__(data)
        self.url = data["url"]
        self.base = data.get("base", None)
        self.version = self._complete_xpath(data.get("version", ''))
        self.date = self._complete_xpath(data.get("date", ''))
        self.date_url = self._complete_xpath(data.get('date-url', None))
        self.no_date = data.get('no-date', False)
        self.url_xpath = self._complete_xpath(data.get('url-xpath', None))

    def data(self):
        html = _TRASH_RE.sub("", download(self.url))
        root = fromstring(html, features='lxml')
        version = _value_from_xpath(root, self.version)
        if self.no_date:
            date = None
        elif self.date_url:
            date_url = urljoin(
                self.url, _value_from_xpath(root, self.date_url))
            date = requests.head(date_url).headers["Last-Modified"]
        elif self.date:
            date = _value_from_xpath(root, self.date)
        else:
            date = None
        if self.url_xpath:
            url = urljoin(
                self.url, _value_from_xpath(root, self.url_xpath))
        else:
            url = self.url
        return {
            "id": self.id,
            "version": version,
            "url": url,
            "date": date,
        }
