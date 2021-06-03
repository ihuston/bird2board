import os
import unittest
from unittest import TestCase

from . import bird2board


class TestPinboard(TestCase):

    @unittest.skipIf("PINBOARD_TOKEN" not in os.environ,
                     "requires a real user API token for connection")
    def test_pinboard_connection(self):
        token = os.getenv("PINBOARD_TOKEN", "mytoken")
        pinboard = bird2board.Pinboard(token)
        assert pinboard.check_connection()

    def test_tweet_to_bookmark(self):
        pinboard = bird2board.Pinboard("mytoken")
        tweet = {"screen_name": "my_name", "rest_id": 1,
                 "full_text": "my tweet",
                 "tweet_url": "https://twitter.com/my_name/status/1"}
        bookmark = pinboard.tweet_to_bookmark(tweet)
        expected = {"url": "https://twitter.com/my_name/status/1",
                    "description": "my tweet",
                    "extended": "my tweet",
                    "replace": "no",
                    "shared": "no",
                    "toread": "yes"}
        self.assertDictEqual(bookmark, expected)

    @unittest.skipIf("PINBOARD_TOKEN" not in os.environ,
                     "requires a real user API token for connection")
    def test_save_bookmark(self):
        bookmark = {"url": "https://twitter.com/xkcd/status/1399524012531896321",
                    "description": "Next slide please",
                    "extended": "Next slide please",
                    "replace": "yes",
                    "shared": "no",
                    "toread": "yes"}
        pinboard = bird2board.Pinboard(os.getenv("PINBOARD_TOKEN", "mytoken"))
        assert pinboard.add_bookmark(bookmark)

