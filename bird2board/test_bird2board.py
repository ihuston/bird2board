import json
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

    def test_prepare_url(self):
        pinboard = bird2board.Pinboard("mytoken")
        url = pinboard.prepare_url(action="update")
        assert url == pinboard.api_url + "update?auth_token=mytoken&format=json"

class TestTwitterBookmarksParse(TestCase):

    def test_parse_json(self):
        t1 = {'content':
                  {'itemContent':
                       {'tweet':
                            {'legacy':
                                 {'full_text':
                                      "my tweet",
                                  'entities': {'urls': [{'expanded_url': "my_url"}]}
                                  },
                             'core':
                                 {'user': {'legacy': {'screen_name': "my_name"}}},
                             'rest_id': 1
                             }
                        }
                   }
              }

        t2 = {'content':
                  {'itemContent':
                       {'tweet':
                            {'legacy':
                                 {'full_text':
                                      "my other tweet",
                                  'entities': {'urls': [{'expanded_url': "my_other_url"}]}
                                  },
                             'core':
                                 {'user': {'legacy': {'screen_name': "my_other_name"}}},
                             'rest_id': 2
                             }
                        }
                   }
              }

        test_json_dict = {'data': {'bookmark_timeline': {'timeline': {'instructions': [{'entries': [t1, t2]}]}}}}
        test_json_text = json.dumps(test_json_dict)

        expected = [{"screen_name": "my_name", "rest_id": 1,
                     "full_text": "my tweet", "expanded_url": "my_url"},
                    {"screen_name": "my_other_name", "rest_id": 2,
                     "full_text": "my other tweet", "expanded_url": "my_other_url"}]
        twitter = bird2board.Twitter()
        self.assertListEqual(twitter.parse_json(test_json_text), expected)