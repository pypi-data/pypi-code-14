from python_agent.tests.integration.coverage.env_coverage.revision1.calculator import Calculator


calc = Calculator()


def test_sub():
    assert calc.sub(1, 1) == 0


def test_mul():
    assert calc.mul(2, 3) == 6
