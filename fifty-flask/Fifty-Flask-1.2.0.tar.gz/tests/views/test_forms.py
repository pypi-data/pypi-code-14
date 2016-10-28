from fifty_flask.views.generic import FormView
from flask import url_for
from tests.forms import PersonForm
from tests.mixins import AppMixin
from unittest import TestCase


class PersonFormView(FormView):
    form_cls = PersonForm
    template_name = 'form.html'

    def get_form_kwargs(self):
        form_kwargs = super(PersonFormView, self).get_form_kwargs()
        form_kwargs.setdefault('csrf_enabled', False)
        return form_kwargs


class PopulatedPersonFormView(PersonFormView):
    def get_form_obj(self):
        class Person(object):
            name = 'Craig'
        return Person()


class FormViewTests(AppMixin, TestCase):
    def setUp(self):
        super(FormViewTests, self).setUp()
        PersonFormView.add_url_rule(self.app, '/form-view/', 'form_view')
        PopulatedPersonFormView.add_url_rule(self.app, '/populated-form-view/',
                'populated_form_view')

    def test_form_get(self):
        """The response should render an empty form.
        """
        response = self.test_app.get(url_for('form_view'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('name="name" type="text" value=""', response.data)
        self.assertIn('name="age" type="text" value=""', response.data)

    def test_valid_form_post(self):
        """The response should be a redirect, since it's a valid form post.
        """
        data = {
                'name': 'Craig',
                'age': 32
                }

        response = self.test_app.post(url_for('form_view'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, url_for('form_view', _external=True))

    def test_invalid_form_post(self):
        """The response should include a form validation error, with the fields still populated
        with the posted data.
        """
        data = {
                'age': 32
                }

        response = self.test_app.post(url_for('form_view'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('This field is required', response.data)
        self.assertIn('name="name" type="text" value=""', response.data)
        self.assertIn('name="age" type="text" value="32"', response.data)

    def test_populated_form_get(self):
        """The response should have a pre-populated text field.
        """
        response = self.test_app.get(url_for('populated_form_view'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('name="name" type="text" value="Craig"', response.data)
