import os
import json
import requests

from utils import green_string, red_color
from config import Config


class Client:
    base_api_url = "http://www.i18nize.com/api/v1/"
    def __init__(self, config):
        self.config = Config(**config)

    def get_project_api_url(self):
        return os.path.join(self.base_api_url, 'content/projects', self.config.PROJECT_ID, '')

    def get_languages_api_url(self):
        return os.path.join(self.get_project_api_url(), 'languages', '')

    def get_locale_api_url(self, language_code):
        s = 'development/{}'.format(language_code) if not self.config.LIVE else language_code
        return os.path.join(self.get_project_api_url(), 'locale', s, '')

    def get_auth_api_url(self):
        return os.path.join(self.base_api_url, 'token-auth', '')

    def get_locale_filepath(self, language_code, prefix):
        filename = u'{}.{}'.format(language_code, prefix)
        return os.path.join(self.config.DESTINATION_DIR, filename)

    def get(self, url):
        response = requests.get(url)
        return response.json()

    def get_langauges(self):
        return self.get(self.get_languages_api_url())

    def write_file(self, prefix, data, language_code):
        filename = u'{}.{}'.format(language_code, prefix)
        filepath = os.path.join(self.config.DESTINATION_DIR, filename)

        with open(filepath, 'w') as outfile:
            json.dump(data, outfile, indent=4)
            print 'Downloaded {} to {} (live: {})'.format(green_string(language_code), green_string(filepath), self.config.LIVE)

    def write_json_file(self, data, language_code):
        self.write_file('json', data, language_code)

    def get_locale(self, language_code):
        try:
            url = self.get_locale_api_url(language_code)
            response = self.get(url)
            self.write_json_file(response, language_code)
        except Exception, e:
            print '{} to collect locales for {}. ({})'.format(red_color("Failed"), red_color(language_code), e)

    def get_all_locales(self):
        languages = self.get_langauges()

        for language in languages:
            language_code = language.get('language_code')
            self.get_locale(language_code)
