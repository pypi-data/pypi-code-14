from datetime import time

from mongoframes import *
from pymongo import MongoClient
import pytest
from werkzeug.datastructures import MultiDict

from manhattan.forms import BaseForm
from manhattan.forms import fields


# Fixtures

class Dragon(Frame):
    """
    A dragon.
    """

    _fields = {
        'name',
        'breed'
        }

    def __str__(self):
        return '{d.name} ({d.breed})'.format(d=self)


@pytest.fixture(scope='session')
def mongo_client(request):
    """Connect to the test database"""

    # Connect to mongodb and create a test database
    Frame._client = MongoClient('mongodb://localhost:27017/manhattan_forms')

    def fin():
        # Remove the test database
        Frame._client.drop_database('manhattan_forms')

    request.addfinalizer(fin)

    return Frame._client

@pytest.fixture(scope='function')
def dragons(mongo_client):
    """Create a collection of dragons"""

    Dragon(name='Burt', breed='Fire-drake').insert()
    Dragon(name='Fred', breed='Fire-drake').insert()
    Dragon(name='Albert', breed='Cold-drake').insert()


# Tests

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

def test_document_checkboxes_field(dragons):
    """
    Support for multiple checkboxes generated from documents in the database.
    """

    class MyForm(BaseForm):

        class Meta:
            csrf = False

        foo = fields.DocumentCheckboxField(
            'Foo',
            frame_cls=Dragon,
            filter=Q.breed == 'Fire-drake',
            sort=[('name', ASC)]
            )

    my_form = MyForm()
    choices = [
        (d._id, str(d)) for d in
        Dragon.many(Q.breed == 'Fire-drake', sort=[('name', ASC)])
        ]
    assert my_form.foo.choices == choices

    # Check setting id and label attributes
    class MyForm(MyForm):
        foo = fields.DocumentCheckboxField(
            'Foo',
            frame_cls=Dragon,
            id_attr='name',
            label_attr='breed',
            sort=[('name', ASC)]
            )

    my_form = MyForm()
    choices = [(d.name, d.breed) for d in Dragon.many(sort=[('name', ASC)])]
    assert my_form.foo.choices == choices

    # Check setting a projection
    class MyForm(MyForm):
        foo = fields.DocumentCheckboxField(
            'Foo',
            frame_cls=Dragon,
            label_attr='breed',
            sort=[('name', ASC)],
            projection={'name': True}
            )

    my_form = MyForm()
    choices = [(d._id, None) for d in Dragon.many(sort=[('name', ASC)])]
    assert my_form.foo.choices == choices

    # Check setting a filter as a lambda argument
    class MyForm(BaseForm):
        foo = fields.DocumentCheckboxField(
            'Foo',
            frame_cls=Dragon,
            filter=lambda form, field: Q.breed == 'Fire-drake',
            sort=[('name', ASC)]
            )

    my_form = MyForm()
    choices = [
        (d._id, str(d)) for d in
        Dragon.many(Q.breed == 'Fire-drake', sort=[('name', ASC)])
        ]
    assert my_form.foo.choices == choices

    # Check setting a limit
    class MyForm(MyForm):
        foo = fields.DocumentCheckboxField(
            'Foo',
            frame_cls=Dragon,
            label_attr='name',
            sort=[('name', ASC)],
            limit=2
            )

    my_form = MyForm()
    choices = [
        (d._id, d.name) for d in Dragon.many(sort=[('name', ASC)], limit=2)]
    assert my_form.foo.choices == choices

def test_document_select_field(dragons):
    """
    Support for select field generated from documents in the database.
    """

    class MyForm(BaseForm):

        class Meta:
            csrf = False

        foo = fields.DocumentSelectField(
            'Foo',
            frame_cls=Dragon,
            filter=Q.breed == 'Fire-drake',
            sort=[('name', ASC)]
            )

    empty_option = ('', 'Select...')

    my_form = MyForm()
    choices = [
        (d._id, str(d)) for d in
        Dragon.many(Q.breed == 'Fire-drake', sort=[('name', ASC)])
        ]
    choices.insert(0, empty_option)
    assert my_form.foo.choices == choices

    # Check setting id and label attributes
    class MyForm(MyForm):
        foo = fields.DocumentSelectField(
            'Foo',
            frame_cls=Dragon,
            id_attr='name',
            label_attr='breed',
            sort=[('name', ASC)]
            )

    my_form = MyForm()
    choices = [(d.name, d.breed) for d in Dragon.many(sort=[('name', ASC)])]
    choices.insert(0, empty_option)
    assert my_form.foo.choices == choices

    # Check setting a projection
    class MyForm(MyForm):
        foo = fields.DocumentSelectField(
            'Foo',
            frame_cls=Dragon,
            label_attr='breed',
            sort=[('name', ASC)],
            projection={'name': True}
            )

    my_form = MyForm()
    choices = [(d._id, None) for d in Dragon.many(sort=[('name', ASC)])]
    choices.insert(0, empty_option)
    assert my_form.foo.choices == choices

    # Check setting a filter as a lambda argument
    class MyForm(BaseForm):
        foo = fields.DocumentSelectField(
            'Foo',
            frame_cls=Dragon,
            filter=lambda form, field: Q.breed == 'Fire-drake',
            sort=[('name', ASC)]
            )

    my_form = MyForm()
    choices = [
        (d._id, str(d)) for d in
        Dragon.many(Q.breed == 'Fire-drake', sort=[('name', ASC)])
        ]
    choices.insert(0, empty_option)
    assert my_form.foo.choices == choices

    # Check setting a limit
    class MyForm(MyForm):
        foo = fields.DocumentSelectField(
            'Foo',
            frame_cls=Dragon,
            label_attr='name',
            sort=[('name', ASC)],
            limit=2
            )

    my_form = MyForm()
    choices = [
        (d._id, d.name) for d in Dragon.many(sort=[('name', ASC)], limit=2)]
    choices.insert(0, empty_option)
    assert my_form.foo.choices == choices

    # Check setting without empty option
    class MyForm(MyForm):
        foo = fields.DocumentSelectField(
            'Foo',
            frame_cls=Dragon,
            filter=Q.breed == 'Fire-drake',
            sort=[('name', ASC)],
            empty_label=None
            )

    my_form = MyForm()
    choices = [
        (d._id, str(d)) for d in
        Dragon.many(Q.breed == 'Fire-drake', sort=[('name', ASC)])
        ]
    assert my_form.foo.choices == choices

def test_price_field():
    """Accept a price"""

    class MyForm(BaseForm):

        class Meta:
            csrf = False

        foo = fields.PriceField('Foo')

    # Check that populating the form
    my_form = MyForm(foo=1000)
    assert my_form.foo._value() == '10.00'

    # Check various different price formats
    my_form = MyForm(MultiDict({'foo': '10'}))
    assert my_form.data['foo'] == 1000

    my_form = MyForm(MultiDict({'foo': '.1'}))
    assert my_form.data['foo'] == 10

    my_form = MyForm(MultiDict({'foo': '1.1'}))
    assert my_form.data['foo'] == 110

    my_form = MyForm(MultiDict({'foo': '10.01'}))
    assert my_form.data['foo'] == 1001

    # Check setting denomination units
    class MyForm(BaseForm):
        foo = fields.PriceField('Foo', denomination_units=1)

    my_form = MyForm(MultiDict({'foo': '10.01'}))
    assert my_form.data['foo'] == 10

    # Check setting coerce
    class MyForm(BaseForm):
        foo = fields.PriceField('Foo', denomination_units=1, coerce=float)

    my_form = MyForm(MultiDict({'foo': '10.01'}))
    assert my_form.data['foo'] == 10.01

def test_string_list_field():
    """Accept a list defined as a string"""

    class MyForm(BaseForm):

        class Meta:
            csrf = False

        foo = fields.StringListField('Foo')

    my_form = MyForm(MultiDict({'foo': 'bar\nzee\nZee\n\nomm'}))
    assert my_form.data['foo'] == ['bar', 'zee', 'omm']

    # Check setting a separator
    class MyForm(BaseForm):
        foo = fields.StringListField('Foo', separator=',')

    my_form = MyForm(MultiDict({'foo': 'bar,zee,omm'}))
    assert my_form.data['foo'] == ['bar', 'zee', 'omm']

    # Check setting removing blanks
    class MyForm(BaseForm):
        foo = fields.StringListField('Foo', remove_blanks=False)

    my_form = MyForm(MultiDict({'foo': 'bar\nzee\n\nomm'}))
    assert my_form.data['foo'] == ['bar', 'zee', '', 'omm']

    # Check setting removing duplicates
    class MyForm(BaseForm):
        foo = fields.StringListField('Foo', remove_duplicates=False)

    my_form = MyForm(MultiDict({'foo': 'bar\nzee\nzee\nomm'}))
    assert my_form.data['foo'] == ['bar', 'zee', 'zee', 'omm']

    # Check setting case sensitivity
    class MyForm(BaseForm):
        foo = fields.StringListField('Foo', case_sensitive=True)

    my_form = MyForm(MultiDict({'foo': 'bar\nzee\nZee\nomm'}))
    assert my_form.data['foo'] == ['bar', 'zee', 'Zee', 'omm']

    # Check setting coerce
    class MyForm(BaseForm):
        foo = fields.StringListField('Foo', coerce=int)

    my_form = MyForm(MultiDict({'foo': '1\n2\n3'}))
    assert my_form.data['foo'] == [1, 2, 3]

    # Check setting sort
    class MyForm(BaseForm):
        foo = fields.StringListField('Foo', sort=True)

    my_form = MyForm(MultiDict({'foo': 'bar\nzee\nomm'}))
    assert my_form.data['foo'] == ['bar', 'omm', 'zee']

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