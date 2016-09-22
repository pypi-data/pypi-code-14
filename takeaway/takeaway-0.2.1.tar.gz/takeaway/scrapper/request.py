from .error import ScrapperError

from requests.exceptions import ConnectionError, ChunkedEncodingError, HTTPError

import requests
import logging

HEADERS = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko)' +
                              ' Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'gzip',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}


class Request:
    """
    Custom request class to handle custom_error + default header
    """
    @staticmethod
    def get(url, headers=None, cookies=None, session=None):
        """
        Make a get request to url.
        :param url: url for the request
        :param headers: headers if not default
        :param cookies: cookies to send
        :param session: session to use
        :return: response
        """
        if headers is not None:
            for k, v in headers.items():
                HEADERS[k] = v
        try:
            if session:
                response = session.get(url)
            else:
                response = requests.get(url, headers=HEADERS, cookies=cookies)

        except HTTPError:
            raise ScrapperError(1901, url=url)

        except ConnectionError:
            raise ScrapperError(1902, url=url)

        except ChunkedEncodingError:
            raise ScrapperError(1903, url=url)

        return response

    @staticmethod
    def post(url, data, headers=None, cookies=None, session=None):
        """
        Make post request to url
        :param url: url for the request
        :param data: data to send
        :param headers: headers if not default
        :param cookies: cookie to send
        :param session: session to use
        :return: response
        """
        if headers is not None:
            for k, v in headers.items():
                HEADERS[k] = v

        try:
            if session:
                response = session.post(url, data=data)
            else:
                response = requests.post(url, data=data, headers=HEADERS, cookies=cookies)

        except HTTPError:
            raise ScrapperError(1901, url=url)

        except ConnectionError:
            raise ScrapperError(1902, url=url)

        except ChunkedEncodingError:
            raise ScrapperError(1903, url=url)

        return response
