# -*- coding: utf-8 -*-
"""Test cases for the storj.cli package."""

import mock
import os
import unittest

from click.testing import CliRunner

from steenzout.sphinx import cli


class GenerateTestCase(unittest.TestCase):
    """Test case for the generate command."""

    runner = CliRunner()

    @mock.patch('steenzout.sphinx.cli.ResourceGenerator')
    @mock.patch('steenzout.sphinx.cli.tempfile.NamedTemporaryFile', autospec=True)
    @mock.patch('steenzout.sphinx.cli.shutil.copy', autospec=True)
    def test_generate(self, mock_copy, mock_tempfile_class, mock_generator_class):
        mock_generator = mock_generator_class()
        mock_generator.conf = mock.MagicMock()
        mock_generator.conf.return_value = 'conf content'

        mock_generator.makefile = mock.MagicMock()
        mock_generator.makefile.return_value = 'makefile content'

        mock_tempfile = mock_tempfile_class()
        mock_tempfile.close = mock.MagicMock()
        mock_tempfile.close.side_effect = [None, None]
        mock_tempfile.write = mock.MagicMock()
        mock_tempfile.write.side_effect = [None, None]

        mock_copy.side_effect = [None, None]

        result = self.runner.invoke(
            cli.generate, ['organization', 'package', 'docs'])

        assert result.exit_code == 0
        assert result.output == ''

        assert mock_generator.conf.call_count == 1
        assert mock_generator.makefile.call_count == 1
        assert mock_tempfile.write.call_count == 2
        assert mock_tempfile.close.call_count == 2

        mock_generator.makefile.assert_called_once_with()
        mock_tempfile.write.assert_any_call('makefile content')
        mock_copy.assert_any_call(mock.ANY, os.path.join(os.getcwd(), 'docs', 'Makefile'))

        mock_generator.conf.assert_called_once_with()
        mock_tempfile.write.assert_any_call('conf content')
        mock_copy.assert_any_call(mock.ANY, os.path.join(os.getcwd(), 'docs', 'conf.py'))
