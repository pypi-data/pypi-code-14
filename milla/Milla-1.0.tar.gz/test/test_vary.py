from milla import vary
import collections
import functools
import milla
import nose.tools
import sys
try:
    from unittest import mock
except ImportError:
    import mock


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

def test_renders_decorator():
    '''renders modifies and returns the decorated object'''

    def func():
        pass

    func2 = vary.renders('text/html')(func)

    assert func2 is func
    assert 'text/html' in func.renders


def test_default_renderer_decorator():
    '''default_renderer modifies and returns the decorated object'''

    def func():
        pass

    func2 = vary.default_renderer(func)

    assert func2 is func
    assert func.default_renderer


def test_variedresponsemeta_renderers():
    '''VariedResponseMeta adds renderers dict to implementation classes'''

    TestClass = vary.VariedResponseMeta('TestClass', (object,), {})

    assert isinstance(TestClass.renderers, collections.Mapping)


def test_variedresponsemeta_default_renderer():
    '''VariedResponseMeta adds default_type to implementation classes'''

    TestClass = vary.VariedResponseMeta('TestClass', (object,), {})

    assert TestClass.default_type is None


def test_variedresponsemeta_renders():
    '''Test VariedResponseMeta implementation class renderers population'''

    VariedResponse = vary.VariedResponseMeta('VariedResponse', (object,), {})

    class TestClass(VariedResponse):

        @vary.renders('text/html')
        def render_html(self, context):
            pass


    if PY2:
        want_func = TestClass.render_html.__func__
    else:
        want_func = TestClass.render_html
    assert TestClass.renderers['text/html'] is want_func


def test_variedresponsemeta_default_renderer():
    '''Test VariedResponseMeta implementation class sets default type'''

    VariedResponse = vary.VariedResponseMeta('VariedResponse', (object,), {})

    class TestClass(VariedResponse):

        @vary.default_renderer
        @vary.renders('text/html')
        def render_html(self, context):
            pass

    assert TestClass.default_type == 'text/html'


def test_variedresponsebase_init_super():
    '''VariedResponseBase.__init__ calls Response.__init__'''

    request = milla.Request.blank('http://localhost/')
    with mock.patch.object(milla.Response, '__init__') as init:
        vary.VariedResponseBase(request, 'a', b='c')

    assert init.called_with('a', b='c')


def test_variedresponsebase_for_request():
    '''VariedResponseBase.for_request returns a partial'''

    request = milla.Request.blank('http://localhost/')
    klass = vary.VariedResponseBase.for_request(request)
    assert isinstance(klass, functools.partial), klass


def test_variedresponsebase_set_payload_set_vary():
    '''VariedResponseBase.set_payload sets the Vary response header'''

    def render_html(response, context):
        pass

    request = milla.Request.blank('http://localhost/')
    response = vary.VariedResponseBase(request)
    response.renderers['text/html'] = render_html
    response.set_payload({})

    assert response.headers['Vary'] == 'Accept'


def test_variedresponsebase_set_payload_add_vary():
    '''VariedResponseBase.set_payload adds to the Vary response header'''

    def render_html(response, context):
        pass

    request = milla.Request.blank('http://localhost/')
    response = vary.VariedResponseBase(request)
    response.renderers['text/html'] = render_html
    response.vary = ('Cookie',)
    response.set_payload({})

    assert response.headers['Vary'] == 'Cookie, Accept'


def test_variedresponsebase_set_payload_match():
    '''VariedResponseBase.set_payload calls the matching renderer'''

    class State(object):
        html_called = False
        json_called = False

    def render_html(response, state):
        state.html_called = True

    render_html.renders = ('text/html',)

    def render_json(response, state):
        state.json_called = True

    render_json.renders = ('application/json',)

    def check_type(accept, attr):
        request = milla.Request.blank('http://localhost/')
        request.accept = accept
        response = vary.VariedResponseBase(request)
        response.renderers = {
            'text/html': render_html,
            'application/json': render_json,
        }
        state = State()
        response.set_payload(state)

        assert getattr(state, attr)

    tests = [
        ('text/html', 'html_called'),
        ('application/json', 'json_called'),
    ]
    for accept, attr in tests:
        yield check_type, accept, attr


@nose.tools.raises(milla.HTTPNotAcceptable)
def test_variedresponsebase_set_payload_not_acceptable():
    '''VariedResponseBase.set_payload raises HTTPNotAcceptable'''

    def render_html(response, context):
        pass

    request = milla.Request.blank('http://localhost/')
    request.accept = 'text/plain'
    response = vary.VariedResponseBase(request)
    response.renderers['text/html'] = render_html
    response.set_payload({})


def test_variedresponsebase_set_payload_default_format():
    '''VariedResponseBase.set_payload falls back to the default renderer'''

    class State(object):
        called = False

    state = State()

    def render_html(response, context):
        state.called = True

    request = milla.Request.blank('http://localhost/')
    request.accept = 'text/plain'
    response = vary.VariedResponseBase(request)
    response.renderers['text/html'] = render_html
    response.default_type = 'text/html'
    ctx = {}
    response.set_payload(ctx)

    assert state.called


def test_variedresponsebase_set_payload_renderer_unknown_kwargs():
    '''VariedResponseBase.set_payload ignores unknown keyword arguments'''

    def render_html(response, context):
        pass

    request = milla.Request.blank('http://localhost/')
    response = vary.VariedResponseBase(request)
    response.renderers['text/html'] = render_html
    response.set_payload({}, foo='bar')
