import io
import pytest

from .. import COUNT, cli

def horetu(*args, **kwargs):
    fp = io.BytesIO()
    kwargs['exit_'] = lambda x: None
    kwargs['stdout'] = fp
    kwargs['argv'] = ['program-name'] + kwargs.get('argv', [])
    cli(*args, **kwargs)
    y = fp.getvalue().decode('utf-8')
    if y:
        try:
            return eval(y)
        except (NameError, SyntaxError):
            return y.strip()

def fa(force:bool=True):
    return force
def fb(force=True):
    return force
def fc(force:bool=False):
    return force
def fd(force=False):
    return force

testcases_bool = [
    (fa, True),
    (fb, True),
    (fc, False),
    (fd, False),
]
@pytest.mark.parametrize('f, default', testcases_bool)
def test_bool(f, default):
    assert horetu(f, argv=[]) == default
    assert horetu(f, argv=['-force']) == (not default)
    assert horetu(f, argv=['-f']) == (not default)

def test_takes_parameter():
    def build(src, recursive:bool=False, force:bool=False):
        return src
    assert horetu(build, argv=['-recursive', 'web']) == 'web'

def test_optional_positional():
    def f(required:int, optional_positional:int=0, *, kwarg:int=8):
        return required + optional_positional + kwarg
    assert horetu(f, argv=['2']) == 10
    assert horetu(f, argv=['2', '100']) == 110
    assert horetu(f, argv=['2', '100', '-kwarg', '3']) == 105
    assert horetu(f, argv=['-k', '3', '2', '100']) == 105

def test_flat():
    def f():
        return 8
    assert horetu(f, name=None, argv=[]) == 8

def test_simple_args():
    def main(first, second):
        return first + second
    assert horetu(main, argv=['a', 'b']) == 'ab'

nest = [
    (['f1', '8', '2', '9'], 1),
    (['f2', '8', '2'], 16),
]

@pytest.mark.parametrize('argv, expected', nest)
def test_nested(argv, expected):
    def f1(a:int, b:int, c:int):
        return a + b - c
    def f2(a:int, b:int):
        return a * b
    def f3():
        return 2
    fs = {'f1': f1, 'f2': f2, 'f3': f3}
    observed = horetu(fs, argv=argv, name='do-something')
    assert observed == expected
    observed = horetu(list(fs.values()), argv=argv, name='do-something')
    assert observed == expected

triple_nest = [
 #  (['aa', 'bb', '10', '3'], 30),
    (['aa', 'cc', 'BB'], 2),
 #  (['zz'], 8),
]
@pytest.mark.parametrize('argv, expected', triple_nest)
def test_triple_nested(argv, expected):
    def command1(a:int, b:int, c:int):
        return a + b - c
    def command2(a:int, b:int):
        return a * b
    def command3():
        return 2
    commands = {'aa': {'bb': command2, 'cc': {'AA': command1, 'BB': command3}}, 'zz': lambda: 8}
    observed = horetu(commands, argv=argv, name = 'do-something')
    assert observed == expected

def test_choices():
    def main(output_format: ('groff', 'RUNOFF')):
        assert output_format == 'RUNOFF'

    horetu(main, argv=['RUNOFF'])

    class exit_(object):
        def __new__(Class, code):
            Class.code = code

    cli(main, argv=['blah', 'troff'], exit_ = exit_)
    assert exit_.code == 2

def test_annotate_list():
    def f(colors: list = ['pink']):
        assert colors == ['pink', 'green']
    horetu(f, argv=['--color', 'green'])

def test_hyphen():
    def main(some_file, some_password=None, n=8):
        pass
    horetu(main, argv=['toilets.csv', '-s', 'abc', '-n' '2'])

def f_count(x, *, y: COUNT=8):
    return y
def test_count_default():
    assert horetu(f_count, argv=['blah']) == 8
def test_count():
    assert horetu(f_count, argv=['blah', '-y', '-y']) == 2

def test_count_errors1():
    def f(x, y: COUNT=2, *, z=8):
        pass
    with pytest.raises(TypeError):
        assert horetu(f, argv=['aoue']) == None

def test_count_errors2():
    def f(x: COUNT):
        pass
    with pytest.raises(TypeError):
        assert horetu(f, argv=['aoue']) == None

def test_count_errors3():
    def f(*x: COUNT):
        pass
    with pytest.raises(TypeError):
        assert horetu(f)


def f(a, b, c = 'xxx'):
    return a + b + c

def g(host = 'blah', port: int = 'blah'):
    return str((host, port))

def h(*args):
    return len(args)

def i(x):
    '''
    :param x: Something to return
    '''
    return x

def j(x: float):
    return x

def k(a, b = None, *, c = 8, d = 4):
    return str((a, b))

def Folder(x):
    if x.startswith('+'):
        return x[1:]
    else:
        raise ValueError('Folders must start with "+".')

def optional_with_types(folder: Folder = None, msg: str = None):
    return folder, msg

cases = [
    (f, ['1', '2'], '12xxx'),
    (g, ['-p', '8888'], ('blah', 8888)),
    (h, ['a', 'b', 'd', 'c'], 4),
    (i, ['aoeu'], 'aoeu'),
    (j, ['8.4'], 8.4),
    (k, ['aoeu'], ('aoeu', None)),
#   (optional_with_types, ['+INBOX', 'blah@blah.blah'], ('INBOX', 'blah@blah.blah')),
#   (optional_with_types, ['blah@blah.blah'], (None, 'blah@blah.blah')),
]

@pytest.mark.parametrize('function, argv, result', cases)
def test_cli(function, argv, result):
    assert horetu(function, argv=argv) == result
