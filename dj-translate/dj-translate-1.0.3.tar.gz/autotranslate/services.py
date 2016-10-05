# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import collections
import six
import urllib2
import urllib
import re
from fake_useragent import UserAgent

from autotranslate.compat import goslate, googleapiclient

from django.conf import settings


class BaseTranslatorService:

    """
    Defines the base methods that should be implemented
    """

    def translate_string(self, text, target_language, source_language='en'):
        """
        Returns a single translated string literal for the target language.
        """
        raise NotImplementedError('.translate_string() must be overridden.')

    def translate_strings(self, strings, target_language, source_language='en', optimized=True):
        """
        Returns a iterator containing translated strings for the target language
        in the same order as in the strings.
        :return:    if `optimized` is True returns a generator else an array
        """
        raise NotImplementedError('.translate_strings() must be overridden.')


class GoSlateTranslatorService(BaseTranslatorService):

    """
    Uses the free web-based API for translating.
    https://bitbucket.org/zhuoqiang/goslate
    """

    def __init__(self):
        self.ua = UserAgent()

    def get_chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def _translate(self, to_translate, to_language="auto", from_language="auto"):

        agent = self.ua.random

        agent = {'User-Agent': agent}

        base_link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s"
        if (sys.version_info[0] < 3):
            to_translate = urllib.quote_plus(to_translate)
            link = base_link % (to_language, from_language, to_translate)
            request = urllib2.Request(link, headers=agent)
            page = urllib2.urlopen(request).read()
        else:
            to_translate = urllib.parse.quote(to_translate)
            link = base_link % (to_language, from_language, to_translate)
            request = urllib.request.Request(link, headers=agent)
            page = urllib.request.urlopen(request).read().decode("utf-8")
        expr = r'class="t0">(.*?)<'
        result = re.findall(expr, page)
        if (len(result) == 0):
            return ("")
        return(result[0])

    def translate_string(self, text, target_language, source_language='en'):
        pass

    def translate_strings(self, strings, target_language, source_language='en', optimized=True):

        print "Translating into " + target_language

        final_string = []

        for strr in strings:

            try:

                converted_strings = re.sub(r'\s+', ' ', strr)

                translated_strings = self._translate(
                    converted_strings, target_language, source_language)

                print converted_strings
                print translated_strings

                print "*" * 50

                final_string.append(translated_strings)

            except:
                final_string.append(strr)

        return final_string


class GoogleAPITranslatorService(BaseTranslatorService):

    """
    Uses the paid Google API for translating.
    https://github.com/google/google-api-python-client
    """

    def __init__(self, max_segments=128):
        assert googleapiclient, '`GoogleAPITranslatorService` requires `google-api-python-client` package'

        self.developer_key = getattr(settings, 'GOOGLE_TRANSLATE_KEY', None)
        assert self.developer_key, ('`GOOGLE_TRANSLATE_KEY` is not configured, '
                                    'it is required by `GoogleAPITranslatorService`')

        from googleapiclient.discovery import build
        self.service = build(
            'translate', 'v2', developerKey=self.developer_key)

        # the google translation API has a limit of max
        # 128 translations in a single request
        # and throws `Too many text segments Error`
        self.max_segments = max_segments
        self.translated_strings = []

    def translate_string(self, text, target_language, source_language='en'):
        assert isinstance(
            text, six.string_types), '`text` should a string literal'
        response = self.service.translations() \
            .list(source=source_language, target=target_language, q=[text]).execute()
        return response.get('translations').pop(0).get('translatedText')

    def translate_strings(self, strings, target_language, source_language='en', optimized=True):
        assert isinstance(strings, collections.MutableSequence), \
            '`strings` should be a sequence containing string_types'
        assert not optimized, 'optimized=True is not supported in `GoogleAPITranslatorService`'
        if len(strings) <= self.max_segments:
            setattr(self, 'translated_strings', getattr(
                self, 'translated_strings', []))
            response = self.service.translations() \
                .list(source=source_language, target=target_language, q=strings).execute()
            self.translated_strings.extend(
                [t.get('translatedText') for t in response.get('translations')])
            return self.translated_strings
        else:
            self.translate_strings(
                strings[0:self.max_segments], target_language, source_language, optimized)
            _translated_strings = self.translate_strings(strings[self.max_segments:],
                                                         target_language, source_language, optimized)

            # reset the property or it will grow with subsequent calls
            self.translated_strings = []
            return _translated_strings