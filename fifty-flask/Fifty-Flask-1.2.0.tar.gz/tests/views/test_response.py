from fifty_flask.views.generic import ResponseMixin, ContextMixin
from tests.mixins import AppMixin
from unittest import TestCase


class StrResponse(ResponseMixin):
    def render_response(self, **context):
        return 'hello there'


class InheritedContext(ContextMixin):
    def get_context_data(self, **context):
        context = super(InheritedContext, self).get_context_data(**context)
        context['base'] = True
        return context


class OverrideContext(InheritedContext):
    def get_context_data(self, **context):
        context = super(OverrideContext, self).get_context_data(**context)
        context['base'] = False
        return context


class UpdateContext(InheritedContext):
    def get_context_data(self, **context):
        context = super(UpdateContext, self).get_context_data(**context)
        context['updated'] = True
        return context


class RemoveContext(UpdateContext):
    def get_context_data(self, **context):
        context = super(RemoveContext, self).get_context_data(**context)
        del context['updated']
        return context


class ReplaceContext(InheritedContext):
    def get_context_data(self, **context):
        return {'replaced': True}


class ResponseTests(TestCase):
    pass


class BaseContextTests(TestCase):
    def test_base_context(self):
        """Default context is an empty dict.
        """
        context = ContextMixin().get_context_data()
        self.assertEqual(context, {})

    def test_explicit_context(self):
        """Passing context directly into the mixin should return that same context.
        """
        d = {'a': 'b'}
        context = ContextMixin().get_context_data(**d)
        self.assertEqual(context, d)

    def test_inherit_context(self):
        """Inherit from base context and add to it.
        """
        context = InheritedContext().get_context_data()
        self.assertEqual(context, {'base': True})

    def test_override_context(self):
        """Inherit from base context and change an existing value.
        """
        context = OverrideContext().get_context_data()
        self.assertEqual(context, {'base': False})

    def test_update_context(self):
        """Inherit from base context and add a new value.
        """
        context = UpdateContext().get_context_data()
        self.assertEqual(context, {'base': True, 'updated': True})

    def test_remove_context(self):
        """Inherit from update context and remove a value.
        """
        context = RemoveContext().get_context_data()
        self.assertEqual(context, {'base': True})

    def test_replace_context(self):
        """Inherit from base context, but ignore it completely and return new context.
        """
        context = ReplaceContext().get_context_data()
        self.assertEqual(context, {'replaced': True})
