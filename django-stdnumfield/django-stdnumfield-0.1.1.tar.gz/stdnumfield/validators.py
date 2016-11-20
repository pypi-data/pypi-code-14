# coding=utf-8
from django.core.exceptions import ValidationError
from django.template.defaultfilters import truncatechars
from stdnum.exceptions import ValidationError as Stdnum_ValidationError
from django.utils.deconstruct import deconstructible

from stdnumfield import settings
from stdnumfield.utils import import_stdnum


@deconstructible
class StdnumFormatValidator(object):
    formats = []

    def __init__(self, formats):
        self.formats = formats

    def _get_formats(self):
        if not self.formats:
            self.formats = settings.DEFAULT_FORMATS
        return self.formats

    def __call__(self, value):
        formats = self._get_formats()
        if not formats:
            raise ValueError(
                'StdnumFormatValidator called without specified formats')
        for format in formats:
            try:
                stdnum_format = import_stdnum(format)
            except ValueError:
                raise
            else:
                try:
                    stdnum_format.validate(value)
                except Stdnum_ValidationError:
                    pass
                else:
                    return
        raise ValidationError(
            'Value does not match with any of the formats: "{}"'
            .format(truncatechars(', '.join(self.formats), 30)))
