
from __future__ import absolute_import

from ...lib.utils import validate_attribute_values

INPUT_TYPES_FOR_AUTOCOMPLETE_ATTRIBUTE = [
    'text', 'search', 'url', 'tel', 'email', 'password', 'range', 'color'
]


class Input(object):
    def __init__(self,
                 accept=None,
                 type=None,
                 align=None,
                 alt=None,
                 autocomplete=None,
                 autofocus=False):
        self.tag = 'input'
        self.validate_accept(type=type, accept=accept)
        validate_attribute_values(tag=self.tag,
                                  attribute_name='align',
                                  value=align)
        self.validate_alt(type=type, alt=alt)
        self.validate_autocomplete(type=type, autocomplete=autocomplete)
        self.validate_autofocus(autofocus=autofocus)

    def construct(self):
        pass

    def validate_accept(self, type, accept):
        """Validates the accept attribute for <input> tag (accept attribute
        can only be used with <input type="file">).
        """
        if not accept:
            return

        if type and type != 'file' and accept:
            raise AttributeError('<input>: accept attribute can only be used '
                                 'with <input type="file">.')

    def validate_alt(self, type, alt):
        """Validates the alt attribute for <input> tag (The alt attribute can
        only be used with <input type="image">).
        """
        if not alt:
            return

        if type and type != 'image' and alt:
            raise AttributeError('<input>: alt attribute can only be used with'
                                 ' <input type="image">.')

    def validate_autocomplete(self, type, autocomplete):
        """Validates the autocomplete attribute for <input> tag (The
        autocomplete attribute works with the following <input> types: text,
        search, url, tel, email, password, datepickers, range, and color).
        """
        if not autocomplete:
            return

        if (type and
                type not in INPUT_TYPES_FOR_AUTOCOMPLETE_ATTRIBUTE and
                autocomplete):
            raise AttributeError(
                '<input>: autocomplete attribute works with the following '
                '<input> types: {0}'
                .format(','.join(INPUT_TYPES_FOR_AUTOCOMPLETE_ATTRIBUTE)))

        validate_attribute_values(tag=self.tag,
                                  attribute_name='autocomplete',
                                  value=autocomplete)

    def validate_autofocus(self, autofocus):
        """Validates the autofocus attribute for <input> tag (The autofocus
        attribute should be a boolean value).
        """
        if not autofocus:
            return

        if not isinstance(autofocus, bool):
            raise AttributeError('<input>: autofocus attribute should be a '
                                 'boolean attribute')
