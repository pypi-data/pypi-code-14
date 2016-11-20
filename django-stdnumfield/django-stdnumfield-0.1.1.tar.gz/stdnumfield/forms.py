from django import forms
from django.utils.itercompat import is_iterable
from django.utils.six import string_types

from stdnumfield import settings
from stdnumfield.validators import StdnumFormatValidator


class StdnumField(forms.CharField):
    formats = None

    def __init__(self, max_length=None, min_length=None, strip=True,
                 formats=None, *args, **kwargs):
        super(StdnumField, self).__init__(max_length, min_length, strip,
                                          *args, **kwargs)
        if formats is None:
            raise ValueError('StdnumField defined without formats')
        if not is_iterable(formats) or isinstance(formats, string_types):
            formats = [formats]
        for format in formats:
            if format not in settings.DEFAULT_FORMATS:
                raise ValueError(
                    'Unknown format for StdnumField: "{}". Is it missing from '
                    'settings.STDNUMFIELD["DEFAULT_FORMATS"]?'.format(
                        format,
                    ))
        self.formats = formats

    def validate(self, value):
        super(StdnumField, self).validate(value)
        validator = StdnumFormatValidator(self.formats)
        validator(value)
