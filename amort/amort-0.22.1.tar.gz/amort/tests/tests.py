from amort.commandline import Amortization, cli
from click.testing import CliRunner
from decimal import Decimal
import pytest


@pytest.fixture
def schedule():
    test_schedule = Amortization(500000, 3, 15, 12)
    return test_schedule


@pytest.fixture
def rounding():
    decimal_rounding = Decimal(10) ** -2
    return decimal_rounding


def test_monthly_payment(schedule, rounding):
    assert schedule.monthly_payment().quantize(rounding) == Decimal(3452.91).quantize(rounding)


def test_beginning_balances(schedule, rounding):
    assert schedule.beginning_balances()[0] == 500000

    assert schedule.beginning_balances()[-1].quantize(rounding) == Decimal(3444.30).quantize(rounding)

    assert len(schedule.beginning_balances()) == 15 * 12


def test_monthly_payments(schedule, rounding):
    assert schedule.monthly_payments()[0].quantize(rounding) == Decimal(3452.91).quantize(rounding)

    assert schedule.monthly_payments()[-1].quantize(rounding) == Decimal(3444.30).quantize(rounding)


def test_principal_payments(schedule, rounding):
    assert schedule.principal_payments()[0].quantize(rounding) == Decimal(2202.91).quantize(rounding)

    assert schedule.principal_payments()[-1].quantize(rounding) == Decimal(3435.71).quantize(rounding)

    assert len(schedule.principal_payments()) == 15 * 12


def test_interest_payments(schedule, rounding):
    assert schedule.interest_payments()[0].quantize(rounding) == Decimal(1250).quantize(rounding)

    assert schedule.interest_payments()[-1].quantize(rounding) == Decimal(8.61).quantize(rounding)

    assert len(schedule.interest_payments()) == 15 * 12


def test_ending_balances(schedule, rounding):
    assert schedule.ending_balances()[-1].quantize(rounding) == 0.00

    assert len(schedule.ending_balances()) == 15 * 12


def test_cumulative_interest(schedule, rounding):
    assert schedule.cumulative_interest()[-1].quantize(rounding) == Decimal(121523.48).quantize(rounding)


def test_cli_print():
    runner = CliRunner()
    print_to_terminal = runner.invoke(cli, ['11300', '3', '5', '12'])
    assert (print_to_terminal.exit_code == 0)


def test_cli_html():
    runner = CliRunner()
    new_html_file = runner.invoke(cli, ['--html', '11300', '3', '5', '12'])
    assert (new_html_file.exit_code == 0)
