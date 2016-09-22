import inspect
import pytest
from .. import funmap

@pytest.fixture
def P():
    @funmap('sub', 'call', 'kwargs')
    def Program(sub, call, kwargs):
        '''
        Specification for a program

        :type sub: dict from (map of str) to program
        :param sub: Dictionary of sub-programs
        :param call: Call the program's underlying function        
        :type kwargs: dict from str to Kwarg
        :param kwargs: Dictionary of keyword arguments
        '''
        return { 'sub':{}, 'call':lambda:None, 'kwargs':{} }
    return Program

def test_doc(P):
    assert 'Specification for a program' in inspect.getdoc(P)

def test_class(P):
    p = P(1, 2, 3)
    assert isinstance(p, P)

def test_class_name():
    A = funmap('a')
    assert A.__name__ == 'Map'
    def f():
        return {'a':8}
    a = A(f)
    assert A.__name__ == 'Map'
    assert a.__name__ == 'f' 

def test_explicit_name():
    A = funmap('a', name='AAAA')
    assert A.__name__ == 'AAAA'

    def b(): return {'a':8}
    assert A(b).__name__ == 'b'

def test_default_name():
    A = funmap('a')
    assert A.__name__ == 'Map'

    def b(): return {'a':8}
    assert A(b).__name__ == 'b'

def test_instance_name(P):
    assert P.__name__ == 'Program'

def test_evaluated_instance_name(P):
    p = P(1, 2, 3)
    assert not hasattr(p, '__name__')

def test_class():
    Class = funmap('a', 'b')
    @Class
    def F():
        return {'a':3, 'b':5}
    f = F()
    assert isinstance(f, Class)

def test_classes():
    A = funmap('a')
    @A
    def a():
        return {'a':3}
    assert isinstance(a(), A)

    B = funmap('bc')
    @B
    def b():
        return {'bc':98}
    assert isinstance(b(), B)

    assert not isinstance(a(), B)
    assert not isinstance(b(), A)

def test_decorated_class():
    @funmap('a')
    def A():
        return {'a':3}

    a = A()
    assert isinstance(a, A)

def test_return():
    @funmap('a', 'b')
    def F():
        return {'a':3, 'b':5}

    with pytest.raises(TypeError):
        f = F(b'oaeu', 808, 'sths', '/')
    f = F()
    assert f.a == 3
    assert f.b == 5

def test_readonly(P):
    with pytest.raises(TypeError):
        P['x'] = 3
    with pytest.raises(TypeError):
        P(*'abc')['x'] = 3
