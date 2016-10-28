from fifty_flask.views.generic import GenericView, url_rule
from flask import url_for
from tests.mixins import AppMixin
from unittest import TestCase


class IndexView(GenericView):
    def get(self, *args, **kwargs):
        return 'get'

    def post(self, *args, **kwargs):
        return 'post'


class ArgsView(GenericView):
    def get(self, *args, **kwargs):
        assert args == self.args, '*args is different'
        assert kwargs == self.kwargs, '**kwargs is different'
        assert 'test' in kwargs
        return ''


class GenericViewTests(AppMixin, TestCase):
    def setUp(self):
        super(GenericViewTests, self).setUp()
        IndexView.add_url_rule(self.app, '/', 'index')
        ArgsView.add_url_rule(self.app, '/args/<test>', 'args')

    def test_get(self):
        """View responds to a GET.
        """
        response = self.test_app.get(url_for('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'get')

    def test_post(self):
        """View responds to a POST.
        """
        response = self.test_app.post(url_for('index'), data={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'post')

    def test_missing_method(self):
        """View does not respond to a disallowed request method.
        """
        response = self.test_app.delete(url_for('index'), data={})
        self.assertEqual(response.status_code, 405)

    def test_args_kwargs(self):
        """*args and **kwargs are available anywhere in the view via self.
        """
        self.test_app.get(url_for('args', test='test'))

    def test_url_rule_single_route(self):
        """View class can be decorated with a single route.
        """
        route = '/single-route-view/'
        route_name = 'single_route_view'
        route_response = 'single route ok'

        @url_rule(self.app, route, route_name)
        class SingleRouteView(GenericView):
            def get(self, *args, **kwargs):
                return route_response

        response = self.test_app.get(route)
        self.assertEqual(response.data, route_response)
        self.assertEqual(url_for(route_name), route)

    def test_url_rule_multiple_routes(self):
        """View class can be decorated with multiple routes.
        """
        routes = ['/route1-view/', '/route2-view/']
        route_name = 'multiple_route_view'
        route_response = 'multiple routes ok'

        @url_rule(self.app, routes, route_name)
        class MultipleRouteView(GenericView):
            def get(self, *args, **kwargs):
                return route_response

        for route in routes:
            response = self.test_app.get(route)
            self.assertEqual(response.data, route_response)

        self.assertEqual(url_for(route_name), routes[0])
