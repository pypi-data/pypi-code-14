from datetime import time
import pytest
from werkzeug.datastructures import MultiDict

from manhattan.forms import BaseForm
from manhattan.forms import fields


def test_checkbox_field():
    """Support for multiple checkboxes"""

    class MyForm(BaseForm):

        foo = fields.CheckboxField(
            'Foo',
            choices=[
                ('bar', 'Bar'),
                ('zee', 'Zee'),
                ('omm', 'Omm')
                ]
            )

    # Check a valid selections are supported
    form = MyForm(MultiDict({'foo': ['bar', 'zee', 'omm']}))
    assert form.validate() == True
    assert form.data['foo'] == ['bar', 'zee', 'omm']

    # Check invalid selections raise an error
    form = MyForm(MultiDict({'foo': ['one', 'zee', 'omm']}))
    assert form.validate() == False
    assert form.errors['foo'][0] == "'one' is not a valid choice for this field"

def test_time_field():
    """Accept a valid time"""

    class MyForm(BaseForm):

        class Meta:
            csrf = False

        foo = fields.TimeField('Foo')

    # Check valid times are accepted
    form = MyForm(MultiDict({'foo': '22:50'}))
    assert form.validate() == True
    assert form.data['foo'] == time(22, 50)

    # Check invalid times raise an error
    form = MyForm(MultiDict({'foo': 'Ten-fifty'}))
    assert form.validate() == False
    assert form.errors['foo'][0] == 'Not a valid time value.'

    # Check a custom format can be used to accept seconds
    class MyForm(BaseForm):

        foo = fields.TimeField('Foo', format='%H:%M:%S')

    form = MyForm(MultiDict({'foo': '22:50:55'}))
    assert form.validate() == True
    assert form.data['foo'] == time(22, 50, 55)