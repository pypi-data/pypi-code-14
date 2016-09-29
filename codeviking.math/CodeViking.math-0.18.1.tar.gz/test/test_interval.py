from codeviking.math.interval import RI


def test_RI():
    i = RI(-2, .83)
    assert -2.1 not in i
    assert -2.0 in i
    assert 0.8 in i
    assert 0.831 not in i


def test_RI_constrain():
    i = RI(-3.0, 1.0)
    assert i.constrain(0.8) == 0.8
    assert i.constrain(-33.0) == -3.0
    assert i.constrain(2.0) == 1.0


def test_RI_alpha():
    i = RI(-3.0, 1.0)
    assert i.alpha(-4.0) == -0.25
    assert i.alpha(3.0) == 1.5
    assert i.alpha(0.0) == 0.75


def test_RI_interpolate():
    i = RI(-3.0, 1.0)
    assert i.interpolate(0.0) == -3.0
    assert i.interpolate(0.5) == -1.0
    assert i.interpolate(1.0) == 1.0
