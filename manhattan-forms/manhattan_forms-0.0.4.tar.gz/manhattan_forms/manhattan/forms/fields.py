from datetime import datetime

from wtforms.fields import Field, SelectMultipleField
from wtforms.widgets import CheckboxInput, ListWidget, TextInput

__all__ = [
    'CheckboxField',
    'TimeField'
    ]


class CheckboxField(SelectMultipleField):
    """
    The `Checkbox` field supports for a list of checkboxes within a form, for
    single checkboxes use the `wtforms.fields.BooleanField`.
    """

    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class TimeField(Field):
    """
    The `TimeField` accepts a time string in 24hr format (by default HH:MM) and
    if valid returns a `datetime.time` instance.
    """

    widget = TextInput()

    def __init__(self, label=None, validators=None, format='%H:%M', **kwargs):
        super().__init__(label, validators, **kwargs)
        self.format = format

    def _value(self):
        if self.raw_data:
            return ' '.join(self.raw_data)
        elif self.data is not None:
            return self.data.strftime(self.format)
        return ''

    def process_formdata(self, values):
        if not values:
            return

        time_str = ' '.join(values)
        try:
            self.data = datetime.strptime(time_str, self.format).time()
        except ValueError:
            self.data = None
            raise ValueError(self.gettext('Not a valid time value.'))