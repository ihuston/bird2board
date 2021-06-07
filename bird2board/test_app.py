import pathlib
import unittest
from unittest import mock

from click.testing import CliRunner

import bird2board.app
from bird2board.app import convert


class MyTestCase(unittest.TestCase):

    @mock.patch.object(bird2board.app.Bird2Board, 'convert_directory')
    def test_convert(self, mock_convert_directory):
        mock_convert_directory.return_value = True
        runner = CliRunner()
        result = runner.invoke(convert, "-p my_token .")
        assert result.exit_code == 0
        mock_convert_directory.assert_called_once_with(pathlib.Path("."))

    @mock.patch.object(bird2board.app.Bird2Board, 'convert_directory', side_effect=Exception("Exploded!"))
    def test_failed_convert(self, mock_convert_directory):
        mock_convert_directory.return_value = False
        runner = CliRunner()
        result = runner.invoke(convert, "-p my_token .")
        mock_convert_directory.assert_called_once_with(pathlib.Path("."))
        assert result.exit_code == 1
