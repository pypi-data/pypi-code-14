import inspect
import pytest
from .. import signature

@pytest.mark.parametrize('default', [True, False])
@pytest.mark.parametrize('kind', [inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                  inspect.Parameter.KEYWORD_ONLY])
@pytest.mark.parametrize('annotation', [bool, inspect.Parameter.empty])
def test_annotate_bool(default, kind, annotation):
    p = inspect.Parameter('force', kind, default=default, annotation=annotation)
    assert signature.Annotation(p).call(None) == (not default)


@pytest.mark.parametrize('kind', [inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                  inspect.Parameter.KEYWORD_ONLY])
def test_annotate_count(kind):
    p = inspect.Parameter('v', kind, default=3, annotation=signature.COUNT)
    a = signature.Annotation(p)
    one = a.call(None)
    two = a.call(None)
    assert one == 1
    assert two == 2
