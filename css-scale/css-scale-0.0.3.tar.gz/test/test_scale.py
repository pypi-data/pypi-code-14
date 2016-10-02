from os import path

from css_scale.scale import scale, coordinate

__location__ = path.dirname(__file__)


def test_scale():
    with open(path.join(__location__, 'scale.css'), 'r') as fp:
        source = fp.read()
        assert scale(source) == source


def test_coordinate():
    assert coordinate({'start': 1, 'end': 2}, {'start': 0, 'end': 10}) == tuple()
    assert coordinate({'start': 1, 'end': 3}, {'start': 0, 'end': 10}) == ((None, 5, 1), (5, None, 2))
    assert coordinate({'start': 1, 'end': 3}, {'start': 0, 'end': 10, 'bound_start': True}) == ((0, 5, 1), (5, None, 2))
    assert coordinate({'start': 1, 'end': 3}, {'start': 0, 'end': 10, 'bound_end': True}) == ((None, 5, 1), (5, 10, 2))
    assert coordinate({'start': 1, 'end': 4}, {'start': 0, 'end': 10}) == ((None, 3, 1), (3, 6, 2), (6, None, 3))
