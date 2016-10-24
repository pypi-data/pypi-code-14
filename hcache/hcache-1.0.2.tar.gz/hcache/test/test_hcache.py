from hcache import Cached, cached

class A(Cached):
    @cached
    def foo(self, n):
        return [n]

    @property
    @cached
    def bar(self):
        return [11]

def test_cache():
    a = A()
    r1 = a.foo(5)
    r2 = a.foo(5)
    a.foo(6)
    r3 = a.foo(5)

    assert r1 is r2
    assert r1 is not r3

def test_cache_property():
    a = A()
    r1 = a.bar
    r2 = a.bar
    assert r1 is r2
