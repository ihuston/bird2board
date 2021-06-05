import json
from unittest import TestCase

from . import Twitter


class TestTwitterBookmarksParse(TestCase):

    def setUp(self) -> None:
        self.t1 = {'content':
                       {'entryType': 'Tweet',
                        'itemContent':
                            {'tweet':
                                 {'legacy':
                                      {'full_text': "my tweet",
                                       'entities': {'urls': [{'expanded_url': "my_url"}]}
                                       },
                                  'core':
                                      {'user': {'legacy': {'screen_name': "my_name"}}},
                                  'rest_id': 1
                                  }
                             }
                        }
                   }

        self.t2 = {'content':
                       {'entryType': 'Tweet',
                        'itemContent':
                            {'tweet':
                                 {'legacy':
                                      {'full_text': "my other tweet",
                                       'entities': {'urls': [{'expanded_url': "my_other_url"}]}
                                       },
                                  'core':
                                      {'user': {'legacy': {'screen_name': "my_other_name"}}},
                                  'rest_id': 2
                                  }
                             }
                        }
                   }

        self.end_marker = {'content':
                               {'entryType': 'TimelineTimelineCursor'}}

    def test_parse_json(self):
        test_json_dict = {'data': {'bookmark_timeline':
                                       {'timeline': {'instructions':
                                                         [{'entries': [self.t1, self.t2, self.end_marker]}]}}}}
        test_json_text = json.dumps(test_json_dict)

        expected = [{"screen_name": "my_name", "rest_id": 1,
                     "full_text": "my tweet", "expanded_url": "my_url",
                     "tweet_url": "https://twitter.com/my_name/status/1"},
                    {"screen_name": "my_other_name", "rest_id": 2,
                     "full_text": "my other tweet", "expanded_url": "my_other_url",
                     "tweet_url": "https://twitter.com/my_other_name/status/2"}]

        twitter = Twitter()
        result = twitter.parse_json(test_json_text)
        self.assertDictEqual(result[0], expected[0])
        self.assertDictEqual(result[1], expected[1])

    def test_no_urls(self):
        t1 = self.t1.copy()
        t1['content']['itemContent']['tweet']['legacy']['entities']['urls'] = []

        test_json_dict = {'data': {'bookmark_timeline': {'timeline': {'instructions': [{'entries': [t1]}]}}}}
        test_json_text = json.dumps(test_json_dict)

        expected = [{"screen_name": "my_name", "rest_id": 1,
                     "full_text": "my tweet",
                     "tweet_url": "https://twitter.com/my_name/status/1"}]

        twitter = Twitter()
        result = twitter.parse_json(test_json_text)
        self.assertDictEqual(result[0], expected[0])
