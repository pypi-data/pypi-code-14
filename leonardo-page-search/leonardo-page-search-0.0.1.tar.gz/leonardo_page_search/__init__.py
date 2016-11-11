
from django.apps import AppConfig

default_app_config = 'leonardo_page_search.Config'


LEONARDO_APPS = ['leonardo_page_search']

LEONARDO_PAGE_EXTENSIONS = [
    'leonardo_page_search.extension',
]


class Config(AppConfig):
    name = 'leonardo_page_search'
    verbose_name = "leonardo-page-search"
