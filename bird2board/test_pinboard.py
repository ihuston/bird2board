import json
import os
import unittest
from datetime import datetime, timedelta
from unittest import TestCase

import pytest
from requests import HTTPError

from . import Pinboard


class TestPinboard(TestCase):

    @unittest.skipIf("PINBOARD_TOKEN" not in os.environ,
                     "requires a real user API token for connection")
    def test_pinboard_connection(self):
        token = os.getenv("PINBOARD_TOKEN", "mytoken")
        pinboard = Pinboard(token)
        assert pinboard.check_connection()

    def test_tweet_to_bookmark(self):
        pinboard = Pinboard("mytoken")
        tweet = {"screen_name": "my_name", "rest_id": 1,
                 "full_text": "my tweet",
                 "tweet_url": "https://twitter.com/my_name/status/1",
                 "tags": ["devops", "cicd"]}
        bookmark = pinboard.tweet_to_bookmark(tweet)
        expected = {"url": "https://twitter.com/my_name/status/1",
                    "description": "my tweet",
                    "extended": "my tweet",
                    "tags": "bird2board from:twitter_bookmarks devops cicd",
                    "replace": "no",
                    "shared": "no",
                    "toread": "no"}
        self.assertDictEqual(bookmark, expected)

    def test_tag_string(self):
        pinboard = Pinboard("mytoken")
        result = pinboard.tag_string(["a", "b", "mytag"])
        self.assertEqual(result, "a b mytag")

    @unittest.skipIf("PINBOARD_TOKEN" not in os.environ,
                     "requires a real user API token for connection")
    def test_save_bookmark(self):
        url = "https://twitter.com/xkcd/status/1399524012531896321"
        bookmark = {"url": url,
                    "description": "Next slide please",
                    "extended": "Next slide please",
                    "tags": "bird2board from:twitter_bookmarks",
                    "replace": "yes",
                    "shared": "no",
                    "toread": "yes"}
        pinboard = Pinboard(os.getenv("PINBOARD_TOKEN", "mytoken"))
        assert pinboard.add_bookmark(bookmark)

        response = pinboard.take_action("get", {"url": url})
        saved_bookmark = json.loads(response.content)["posts"][0]
        saved_tags = saved_bookmark["tags"].split(" ")
        self.assertSetEqual(set(saved_tags), {"bird2board", "from:twitter_bookmarks"})

    def test_failed_save(self):
        url = "https://twitter.com/xkcd/status/1399524012531896321"
        bookmark = {"url": url,
                    "description": "Next slide please",
                    "extended": "Next slide please",
                    "tags": "bird2board from:twitter_bookmarks",
                    "replace": "yes",
                    "shared": "no",
                    "toread": "yes"}
        pinboard = Pinboard("mytoken")
        with self.assertRaises(HTTPError):
            pinboard.add_bookmark(bookmark)

    def test_sleep_between_calls(self):
        pinboard = Pinboard("mytoken")
        last_call = datetime.now()
        pinboard.sleep_if_needed(last_call=last_call, wait=timedelta(seconds=0.1))
        self.assertGreater(datetime.now() - last_call, timedelta(seconds=0.1))


# Outside Test Class
@pytest.mark.parametrize('long, short',
                         [("my tweet", "my tweet"),
                          ("my longer tweet that should be shortened a bit I think",
                           "my longer tweet that should be shortened a bit I..."),
                          ("ifthestringhasnowhitespaceitsgoingtobehardtosplitinagoodplace",
                           "ifthestringhasnowhitespaceitsgoingtobehardtospliti...")])
def test_shorten_description(long, short):
    pinboard = Pinboard("mytoken")
    tweet = {"screen_name": "my_name", "rest_id": 1, "full_text": long,
             "tweet_url": "https://twitter.com/my_name/status/1", "tags": ["devops", "cicd"]}

    bookmark = pinboard.tweet_to_bookmark(tweet)
    assert bookmark["description"] == short
