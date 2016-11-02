# Exposes 3rd-party admin utils at package level.
from daterange_filter.filter import DateRangeFilter

from administration.admin import ModelAdmin
from administration.utils import foreign_link, colored_name
from administration.filters import DropdownFilter

__all__ = [
    'ModelAdmin', 'DateRangeFilter', 'DropdownFilter',
    'foreign_link', 'colored_name',
]

default_app_config = 'administration.apps.AdministrationConfig'
