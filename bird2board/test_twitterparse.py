import json
from unittest import TestCase

from . import bird2board


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
                     "full_text": "my tweet", "expanded_url": "my_url",
                     },
                    {"screen_name": "my_other_name", "rest_id": 2,
                     "full_text": "my other tweet", "expanded_url": "my_other_url"}]
        twitter = bird2board.Twitter()
        result = twitter.parse_json(test_json_text)
        self.assertDictEqual(result[0], expected[0])
        self.assertDictEqual(result[1], expected[1])