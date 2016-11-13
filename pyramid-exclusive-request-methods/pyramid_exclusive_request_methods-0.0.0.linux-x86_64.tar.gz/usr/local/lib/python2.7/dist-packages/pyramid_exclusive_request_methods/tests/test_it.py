import unittest
from pyramid.config import Configurator
from pyramid.response import Response
from webtest import TestApp

class BasicTest(unittest.TestCase):

    def test_it(self):
        from pyramid_exclusive_request_methods import Exclusively

        def test_view1(context, request):
            return Response(text=u'HEY')


        def test_view2(context, request):
            return Response(text=u'HEY')

        c = Configurator(package=__name__)
        c.include('pyramid_exclusive_request_methods')
        c.add_route('test1', '/1')
        c.add_route('test2', '/2')
        c.add_view(test_view1, route_name='test1', request_method=Exclusively(['GET', 'POST']))
        c.add_view(test_view2, route_name='test2', request_method=['GET', 'POST'])

        t = TestApp(c.make_wsgi_app())
        resp = t.get('/1')
        self.assertEquals(resp.status_int, 200)
        resp = t.post('/1')
        self.assertEquals(resp.status_int, 200)
        resp = t.put('/1', status=405)
        self.assertEquals(resp.status_int, 405)

        resp = t.get('/2')
        self.assertEquals(resp.status_int, 200)
        resp = t.post('/2')
        self.assertEquals(resp.status_int, 200)
        resp = t.put('/2', status=404)
        self.assertEquals(resp.status_int, 404)
