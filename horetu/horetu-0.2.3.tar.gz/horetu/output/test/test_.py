import functools
import pytest
from .. import Output, reify_args, reify_kwargs
from ... import exceptions
from ...signature import Signature

_argvalues = [
]
@pytest.mark.parametrize('function, inputs, exp', _argvalues)
def test_output(function, inputs, exp):
    config_file = None
    config_sep = ' '
    f = functools.partial(Output, config_file, config_sep, function, inputs)
    if isinstance(exp, exceptions.HoretuException):
        with pytest.raises(exp):
            f()
    else:
        obs = f()
        assert obs == exp

def test_reify_args():
    section = []
    positionals = ['one', 'two']
    def something(input_file, output_file, n_cores: int = 3):
        '''
        Do something to a file with several cores.
        '''
        # Pretend that something happens here.
    signature = Signature(something)
    
    expected = ['one', 'two']

    observed = reify_args(signature, section, positionals)
    assert observed == expected

def test_reify_kwargs():
    kwargs = [('help', None)]

    def get(url:str, *args:str):
        kwargs = {}
        for arg in args:
            k, v = arg.split('=')
            kwargs[k] = eval(v)
        print(f(url, **kwargs).text)
    signature = Signature(get)

    assert isinstance(reify_kwargs(signature, kwargs), exceptions.HoretuShowHelp)
