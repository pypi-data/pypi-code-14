import pytest
from ..doc import Doc

def f(a, b, c=4):
    '''
    This is the description.

    :param bool a: Parameter a
    :type b: Bob
    :param b: Blah blah
    :param int c: How many
    :rtype: list
    '''
    return []

def g(abc):
    '''
    :param int abc: A word
    '''
    pass

def hi(name: str, times: int=8,
       case: ('title', 'lower', 'upper')='title'):
    '''
    :param name: Name
    :param times: Number of times to say hi
    :param case: Case of the greeting
    '''
    for _ in range(times):
        print('Hi ' + getattr(name, case)())

_argvalues = [
    (hi, '', [('name', 'Name')], [
        ('times', 'Number of times to say hi'),
        ('case', 'Case of the greeting'),
    ]),
    (lambda:8, '', [], []),
    (g, '', [('abc', 'A word')], []),
    (f, 'This is the description.',
        [('a', 'Parameter a'), ('b', 'Blah blah')],
        [('c', 'How many')]),
]
@pytest.mark.parametrize('f, desc, args, kwargs', _argvalues)
def test_Doc(f, desc, args, kwargs):
    d = Doc(f)
    print(d)
    assert d.desc == desc
    assert d.args == args
    assert d.kwargs == kwargs + [('help', 'Display this help.')]
