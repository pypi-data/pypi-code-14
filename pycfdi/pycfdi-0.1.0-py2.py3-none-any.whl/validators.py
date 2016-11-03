# -*- coding: utf-8 -*-

from __future__ import absolute_import

from cerberus import Validator

from datetime import datetime
import logging
import re

log = logging.getLogger(__name__)


class CfdiValidator(Validator):

    def _regex_validator(self, value, regex):
        is_string = type(value) == str
        return is_string and bool(re.match(regex, value))

    def _validate_type_alphanumeric(self, value):
        regex = '[a-zA-Z0-9]'
        return self._regex_validator(value, regex)

    def _validate_type_alphabetic(self, value):
        regex = '[a-zA-Z]'
        return self._regex_validator(value, regex)

    def _validate_type_numeric(self, value):
        regex = '[0-9]'
        return self._regex_validator(value, regex)

    def _validate_type_importe(self, value):
        is_float = type(value) == float
        if is_float:
            as_decimal_str = str(value)
            decimal_places = len(''.join(re.findall('\.\d+', as_decimal_str))) - 1
            return 6 >= decimal_places > 0
        return False

    def _validate_type_rfc(self, value):
        regex = '[A-Z,Ñ,&]{3,4}[0-9]{2}[0-1][0-9][0-3][0-9][A-Z,0-9][A-Z,0-9][0-9,A-Z]$'
        return self._regex_validator(value, regex)

    def _validate_type_mx_zipcode(self, value):
        regex = '(0[1-9]|[1][0-6]|[2-9]\d)(\d{3})$'
        return self._regex_validator(value, regex)

    def _validate_type_iso8601_datetime(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
            return True
        except ValueError:
            return False

    def _validate_type_iso8601_date(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False
