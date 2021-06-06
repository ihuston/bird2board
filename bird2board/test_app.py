import pathlib
from unittest import TestCase, mock

import bird2board.app


class TestApp(TestCase):
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

    @mock.patch('bird2board.app.pathlib')
    @mock.patch.object(bird2board.app.Pinboard, 'add_bookmark')
    @mock.patch.object(bird2board.app.Pinboard, 'tweet_to_bookmark')
    @mock.patch.object(bird2board.app.Twitter, 'parse_json')
    def test_convert_single_file(self, mock_parse_json, mock_tweet_to_bookmark, mock_add_bookmark, mock_pathlib):
        f = mock_pathlib.Path("./my_test_file.json")
        f.read_text.return_value = "my_file_content"
        mock_parse_json.return_value = self.tweets
        mock_tweet_to_bookmark.return_value = self.bookmark
        mock_add_bookmark.return_value = True

        bird2board.app.convert_single_file(f, "my_token")

        mock_parse_json.assert_called_with("my_file_content")
        mock_tweet_to_bookmark.assert_any_call(self.tweets[1])
        mock_tweet_to_bookmark.assert_any_call(self.tweets[1])
        mock_add_bookmark.assert_called_with(self.bookmark)
