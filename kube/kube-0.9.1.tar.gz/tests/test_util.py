import datetime
import json

import pytest

from kube import _error
from kube import _testing
from kube import _util as util


def test_parse_rfc3339():
    d = util.parse_rfc3339('2009-02-13T23:31:30Z')
    assert isinstance(d, datetime.datetime)
    assert d.year == 2009
    assert d.month == 2
    assert d.day == 13
    assert d.hour == 23
    assert d.minute == 31
    assert d.second == 30
    assert d.microsecond == 0
    assert d.tzinfo is None
    assert d.timestamp() == 1234567890


def test_fetch_resource_no_ns(request, cluster):
    data = {
        'apiVersion': 'v1',
        'kind': 'Namespace',
        'metadata': {
            'generateName': 'testsec-',
        },
    }
    raw = cluster.proxy.post('namespaces', json=data)
    name = raw['metadata']['name']
    def fin():
        cluster.proxy.delete('namespaces', name)
    request.addfinalizer(fin)
    ret = util.fetch_resource(cluster, 'namespaces', name)
    assert ret == raw


def test_fetch_resource_ns(request, cluster):
    data = {
        'apiVersion': 'v1',
        'kind': 'Secret',
        'metadata': {
            'generateName': 'testsec-',
            'namespace': 'default',
        },
    }
    raw = cluster.proxy.post('namespaces', 'default', 'secrets', json=data)
    ns = raw['metadata']['namespace']
    name = raw['metadata']['name']
    def fin():
        cluster.proxy.delete('namespaces', ns, 'secrets', name)
    request.addfinalizer(fin)
    ret = util.fetch_resource(cluster, 'secrets', name, namespace=ns)
    assert ret == raw


def test_fetch_resource_404(cluster):
    with pytest.raises(LookupError):
        util.fetch_resource(cluster, 'this-does-not-exist', 'foo')


def test_fetch_resource_err(cluster):
    def get(*args):             # pylint: disable=unused-argument
        raise _testing.StubAPIError(411, 'oops')
    cluster.proxy.get = get
    with pytest.raises(_error.APIError):
        util.fetch_resource(cluster, 'foo', 'bar')


def test_filter_list_empty_labels(cluster):
    gen = util.filter_list(cluster, 'namespaces', labels={}, fields=None)
    with pytest.raises(ValueError):
        next(gen)


def test_filter_list_empty_fields(cluster):
    gen = util.filter_list(cluster, 'namespaces', labels=None, fields={})
    with pytest.raises(ValueError):
        next(gen)


def test_freeze():
    orig = {'str': 'val', 'int': 42, 'list': ['a', 'b', 0, {'a': 1}]}
    frozen = util.freeze(orig)
    assert frozen['str'] == orig['str']
    assert frozen['int'] == orig['int']
    assert frozen['list'][0] == 'a'
    assert frozen['list'][1] == 'b'
    assert frozen['list'][2] == 0
    assert frozen['list'][3]['a'] == 1
    with pytest.raises(TypeError):
        frozen['foo'] = 'bar'
    with pytest.raises(TypeError):
        frozen['list'][3]['foo'] = 'bar'


def test_thaw():
    orig = {'str': 'val', 'int': 42, 'list': ['a', 'b', 0, {'a': 1}]}
    frozen = util.freeze(orig)
    thawed = util.thaw(frozen)
    assert thawed == orig
    thawed['foo'] = 'bar'
    assert thawed['foo'] == 'bar'
    assert 'foo' not in frozen
    assert 'foo' not in orig


def test_statusproperty():
    class Foo:
        @util.statusproperty
        def attr(self):
            raise Exception('oops')

    inst = Foo()
    with pytest.raises(_error.StatusError):
        assert inst.attr


def test_jsond_decode():
    orig = {'str': 'val', 'int': 42, 'list': ['a', 'b', 0, {'a': 1}]}
    data = json.dumps(orig)
    frozen = json.loads(data, cls=util.ImmutableJSONDecoder)
    with pytest.raises(Exception):
        del frozen['int']
    assert frozen['int'] == 42
    with pytest.raises(Exception):
        frozen['new'] = 'hello'
    assert 'new' not in frozen
    assert frozen == util.freeze(orig)
