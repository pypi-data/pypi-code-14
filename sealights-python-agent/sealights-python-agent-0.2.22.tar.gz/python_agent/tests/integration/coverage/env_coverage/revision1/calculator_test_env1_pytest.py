from python_agent.tests.integration.coverage.env_coverage.revision1.calculator import Calculator


calc = Calculator()


def test_add():
    assert calc.add(1, 1) == 2

