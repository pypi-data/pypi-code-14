from python_agent.tests.integration.coverage.build_coverage.revision1.calculator import Calculator

calc = Calculator()


def test_add():
    assert calc.add(1, 1) == 2


def test_sub():
    assert calc.sub(1, 1) == 0


def test_mul():
    assert calc.mul(2, 3) == 6


def test_div():
    assert calc.div(6, 3) == 2
