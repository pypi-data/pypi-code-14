from os import path

from fss.scale import scale, tri, coordinate

__location__ = path.dirname(__file__)


def test_scale():
    with open(path.join(__location__, 'scale.css'), 'r') as fp:
        source = fp.read()
        assert scale(source) == source


def test_tri():
    assert tri((1, 2, 3), 4) == (1, 2, 3)
    assert tri((1, 2), 3) == (1, 2, 3)


def test_coordinate():
    assert coordinate([1, 2], [0, 10]) == tuple()
    assert coordinate([1, 3], [0, 10]) == ((None, 5, 1), (5, None, 2))
    assert coordinate([1, 4], [0, 10]) == ((None, 3, 1), (3, 6, 2), (6, None, 3))
