from click.testing import CliRunner
from brite_etl.cli import main


def test_main():
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert 'Commands:\n' in result.output
    assert result.exit_code == 0
