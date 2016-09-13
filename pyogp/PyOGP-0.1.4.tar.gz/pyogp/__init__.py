import requests
from urllib.parse import urljoin
from re import compile as re_compile
from bs4 import BeautifulSoup


class PyOGP(object):
    """
    """

    def __init__(self, required_set={'title', 'description', 'image'}):
        """

        :param url: required arguments
        :param required_set:
        :return:
        """
        self.required_set = required_set
        self.result = {}
        self.__soup = None

    def crawl(self, url):
        """

        :param url:
        :return:
        """

        response = requests.get(url=url)
        if response is None:
            raise ValueError("can not get response from url: {url}".format(url=url)).with_traceback()

        encoding = self._get_encoding(response)
        self.__soup = BeautifulSoup(response.content, "html.parser", from_encoding=encoding)
        self._get_ogp_meta()

        if 'description' not in self.result:
            self._get_description_meta()

        if self.__soup.frameset:
            frame_tags = self.__soup.frameset.find_all('frame')
            for frame in frame_tags:
                src = frame.attrs['src']
                url = self._get_absolute_url(url, src)
                self.crawl(url)

        if 'title' not in self.result:  # frame안에 og:title을 지키고있으면 일반적으로 <title>의 내용 보다 좋음
            content = self.__soup.head.title.text
            if content: self.result['title'] = content  # if content is not null.

        return self

    def _get_ogp_meta(self):
        head = self.__soup.html.head
        if head:
            ogp_meta_tags = head.find_all(property=re_compile(r'^og'))
        else:
            ogp_meta_tags = self.__soup.html.find_all(property=re_compile(r'^og'))

        for meta in ogp_meta_tags:
            if meta.has_attr(u'content'):
                property_ = meta.attrs[u'property'][3:]  # cut off 'og:'
                if (property_ in self.required_set) and (property_ not in self.result):
                    content = meta.get('content', False)
                    if content:
                        self.result[property_] = content  # content value not empty

    def _is_complete(self):
        """

        :return: whether is completed,  based on required set
        """
        return set(self.result.viewkeys()) == self.required_set

    def _get_description_meta(self):
        """
        get description by meta without og:description
        case : <meta name="description" content="...">
        :return:
        """
        description_meta_tags = self.__soup.html.head.find_all(name='meta',
                                                               attrs={"name": ("description",
                                                                               "DC.description",
                                                                               "Description")
                                                                      },
                                                               )
        for meta in description_meta_tags:
            content_ = meta.get('content', False)
            if content_:
                self.result['description'] = content_

    def _get_absolute_url(self, url, src):
        """
        get abosloute url from relative url(eg src value starts with '/foo')
        :param url:
        :param src:
        :return:
        """
        return urljoin(url, src)

    def _get_encoding(self, response):
        """

        :param response:
        :return:
        """
        encoding = 'utf-8'
        if 'Content-Type' in response.headers:
            content_types = response.headers.get('Content-Type').split(';')
            for c in content_types:
                if c.strip().startswith('charset'):
                    encoding = c.split('=')[1].strip()
                    break
        return encoding

    def get_soup(self):
        if self.__soup is None:
            raise AttributeError('__soup does not exists')
        else:
            return self.__soup

    def get_result(self):
        for key in self.required_set:
            self.result.setdefault(key)
        return self.result
