# This file is a part of 'gravely' software. Copyright (c) 2016 LCODE team.
# Distributed under the terms of the MIT License, see LICENSE.txt.

from unittest import mock

import nose.tools


@mock.patch('gravely.simulation.run')
@mock.patch('sys.argv', ['gravely', '--config', 'my.cfg', 'run'])
def test_subcommand_run(mock_run):
    import gravely.main
    gravely.main.main()
    mock_run.assert_called_with('my.cfg')


@nose.tools.raises(AssertionError)
@mock.patch('gravely.simulation.run', mock.MagicMock())
@mock.patch('sys.argv', ['gravely', 'run', '--config', 'my.cfg', '--z'])
def test_subcommand_run_fails_with_extra_args():
    import gravely.main
    gravely.main.main()


@mock.patch('gravely.tests.run')
@mock.patch('sys.argv', ['gravely', 'test', 'gravely.tests.express'])
def test_subcommand_test(mock_test):
    import gravely.main
    gravely.main.main()
    mock_test.assert_called_with(['gravely.tests.express'])


@mock.patch('gravely.tests.run')
@mock.patch('sys.argv', ['gravely', 'test', 'gravely.tests.express', '--z'])
def test_subcommand_test_passes_extra_arg(mock_test):
    import gravely.main
    gravely.main.main()
    mock_test.assert_called_with(['gravely.tests.express', '--z'])


@nose.tools.raises(SystemExit)
@mock.patch('sys.argv', ['gravely', 'unknown', '-z'])
@mock.patch('sys.stderr', mock.MagicMock())
def test_unknown_subcommand():
    import gravely.main
    gravely.main.main()


@nose.tools.raises(SystemExit)
@mock.patch('sys.argv', ['gravely'])
@mock.patch('sys.stdout', mock.MagicMock())
def test_no_subcommand():
    import gravely.main
    gravely.main.main()
