import pathlib
import unittest
from unittest import mock

from click.testing import CliRunner


from bird2board.app import convert
from bird2board.bird2board import Bird2Board


class MyTestCase(unittest.TestCase):

    @mock.patch.object(Bird2Board, 'convert_directory')
    def test_convert(self, mock_convert_directory):
        mock_convert_directory.return_value = True
        runner = CliRunner()
        result = runner.invoke(convert, "-p my_token .")
        assert result.exit_code == 0
        mock_convert_directory.assert_called_once_with(pathlib.Path("."))

    @mock.patch.object(Bird2Board, 'convert_directory')
    def test_convert_file(self, mock_convert_directory):
        mock_convert_directory.return_value = True
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('bookmark.json', "w") as f:
                f.write('{"data": {}')
            result = runner.invoke(convert, "-p my_token ./bookmark.json")
            assert result.exit_code == 0
            mock_convert_directory.assert_called_once_with(pathlib.Path("./bookmark.json"))

    @mock.patch.object(Bird2Board, 'convert_directory', side_effect=Exception("Exploded!"))
    def test_failed_convert(self, mock_convert_directory):
        mock_convert_directory.return_value = False
        runner = CliRunner()
        result = runner.invoke(convert, "-p my_token .")
        mock_convert_directory.assert_called_once_with(pathlib.Path("."))
        assert result.exit_code == 1
