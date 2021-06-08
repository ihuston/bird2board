import pathlib
import unittest.mock
from unittest import TestCase, mock

from click.testing import CliRunner

import bird2board.app
import bird2board.bird2board


class TestBird2Board(TestCase):
    tweets = [{"screen_name": "my_name", "rest_id": 1,
               "full_text": "my tweet", "expanded_url": "my_url",
               "tweet_url": "https://twitter.com/my_name/status/1",
               "tags": ['devops', 'cicd']},
              {"screen_name": "my_other_name", "rest_id": 2,
               "full_text": "my other tweet", "expanded_url": "my_other_url",
               "tweet_url": "https://twitter.com/my_other_name/status/2",
               "tags": []}]
    bookmark = {"url": "https://twitter.com/my_name/status/1",
                "description": "my tweet",
                "extended": "my tweet",
                "tags": "bird2board from:twitter_bookmarks devops cicd",
                "replace": "no",
                "shared": "no",
                "toread": "yes"}

    @mock.patch('bird2board.bird2board.pathlib')
    @mock.patch.object(bird2board.Pinboard, 'add_bookmark')
    @mock.patch.object(bird2board.Pinboard, 'tweet_to_bookmark')
    @mock.patch.object(bird2board.Twitter, 'parse_json')
    def test_convert_single_file(self, mock_parse_json, mock_tweet_to_bookmark, mock_add_bookmark, mock_pathlib):
        f = mock_pathlib.Path("./my_test_file.json")
        f.read_text.return_value = "my_file_content"
        mock_parse_json.return_value = self.tweets
        mock_tweet_to_bookmark.return_value = self.bookmark
        mock_add_bookmark.return_value = True

        b2b = bird2board.bird2board.Bird2Board("my_token")
        b2b.convert_single_file(f)

        mock_parse_json.assert_called_with("my_file_content")
        mock_tweet_to_bookmark.assert_any_call(self.tweets[0])
        mock_tweet_to_bookmark.assert_any_call(self.tweets[1])
        mock_add_bookmark.assert_called_with(self.bookmark)

    @mock.patch('bird2board.bird2board.pathlib')
    @mock.patch.object(bird2board.bird2board.Bird2Board, 'convert_single_file')
    def test_convert_directory(self, mock_convert_file, mock_pathlib):
        d = mock_pathlib.Path("./my_test_dir/")
        f1 = pathlib.Path("./testfile.json")
        f2 = pathlib.Path("./testfile2.json")
        d.iterdir.return_value = [f1, f2]
        d.is_file.return_value = False
        mock_convert_file.return_value = True

        b2b = bird2board.bird2board.Bird2Board("my_token")
        b2b.convert_directory(d)

        d.iterdir.assert_called()
        mock_convert_file.assert_any_call(f1)
        mock_convert_file.assert_any_call(f2)

    @mock.patch('bird2board.bird2board.pathlib')
    @mock.patch.object(bird2board.bird2board.Bird2Board, 'convert_single_file')
    def test_convert_directory_with_file(self, mock_convert_file, mock_pathlib):
        mock_convert_file.return_value = True

        runner = CliRunner()
        with runner.isolated_filesystem():
            with open('bookmark.json', "w") as f:
                f.write('{"data": {}')
            f = mock_pathlib.Path("./bookmark.json")
            b2b = bird2board.bird2board.Bird2Board("my_token")
            b2b.convert_directory(f)

        f.iterdir.assert_not_called()
        mock_convert_file.assert_called_with(f)

    @mock.patch('bird2board.bird2board.pathlib')
    @mock.patch.object(bird2board.bird2board.Bird2Board, 'convert_single_file')
    def test_filter_non_json(self, mock_convert_file, mock_pathlib):
        d = mock_pathlib.Path("./my_test_dir/")
        f1 = pathlib.Path("./testfile.json")
        f2 = pathlib.Path("./testfile2.txt")
        f3 = pathlib.Path("./testfile3.json")
        d.iterdir.return_value = [f1, f2, f3]
        d.is_file.return_value = False
        mock_convert_file.return_value = True

        b2b = bird2board.bird2board.Bird2Board("my_token")
        b2b.convert_directory(d)

        d.iterdir.assert_called()
        mock_convert_file.assert_any_call(f1)
        mock_convert_file.assert_any_call(f3)
        assert unittest.mock.call(f2) not in mock_convert_file.call_args_list
