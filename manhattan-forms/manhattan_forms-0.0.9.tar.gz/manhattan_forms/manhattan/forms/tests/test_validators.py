import pytest
from werkzeug.datastructures import MultiDict
from wtforms.fields import StringField

from manhattan.forms import BaseForm
from manhattan.forms import validators


def test_required_if():
    """
    Flag a field as required if a given condition is met by one or more other
    fields.
    """

    class MyForm(BaseForm):

        foo = StringField('Foo')
        bar = StringField('Bar')
        zee = StringField(
            'Zee',
            validators=[validators.RequiredIf(foo='bar', bar='zee')]
            )

    # Check `zee` is required if conditions are met
    form = MyForm(MultiDict({'foo': 'bar'}))
    form.validate()
    assert form.errors['zee'][0] == 'This field is required.'

    form = MyForm(MultiDict({'foo': 'foo', 'bar': 'zee'}))
    form.validate()
    assert form.errors['zee'][0] == 'This field is required.'

    # Check `zee` is optional if conditions are not met
    form = MyForm(MultiDict({'foo': 'foo', 'bar': 'bar'}))
    assert form.validate() == True