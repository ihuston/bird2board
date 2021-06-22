import json
from unittest import TestCase

from . import Twitter


def embed_tweets(tweets):
    return {'data': {'bookmark_timeline':
                         {'timeline': {'instructions':
                                           [{'entries': tweets}]}}}}


class TestBird(TestCase):

    def setUp(self) -> None:
        self.t1 = {'content':
                       {'entryType': 'Tweet',
                        'itemContent':
                            {'tweet':
                                 {'legacy':
                                      {'full_text': "my tweet",
                                       'entities': {'urls': [{'expanded_url': "my_expanded_url",
                                                              'url': "my_url"}],
                                                    'hashtags': [{'indices': [224, 231], 'text': 'devops'},
                                                                 {'indices': [200, 204], 'text': 'cicd'}]}
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
                                       'entities': {'urls': [{'expanded_url': "my_other_expanded_url",
                                                              'url': "my_other_url"}],
                                                    'hashtags': []},
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
        tweets = [self.t1, self.t2, self.end_marker]
        test_json_text = json.dumps(embed_tweets(tweets))

        expected = [{"screen_name": "my_name", "rest_id": 1,
                     "full_text": "my tweet", "expanded_url": "my_expanded_url",
                     "tweet_url": "https://twitter.com/my_name/status/1",
                     "tags": ['devops', 'cicd']},
                    {"screen_name": "my_other_name", "rest_id": 2,
                     "full_text": "my other tweet", "expanded_url": "my_other_expanded_url",
                     "tweet_url": "https://twitter.com/my_other_name/status/2",
                     "tags": []}]

        twitter = Twitter()
        result = twitter.parse_json(test_json_text)
        self.assertDictEqual(result[0], expected[0])
        self.assertDictEqual(result[1], expected[1])

    def test_no_urls(self):
        t1 = self.t1.copy()
        t1['content']['itemContent']['tweet']['legacy']['entities']['urls'] = []
        test_json_text = json.dumps(embed_tweets([t1]))

        expected = [{"screen_name": "my_name", "rest_id": 1,
                     "full_text": "my tweet",
                     "tweet_url": "https://twitter.com/my_name/status/1",
                     "tags": ['devops', 'cicd']}]

        twitter = Twitter()
        result = twitter.parse_json(test_json_text)
        self.assertDictEqual(result[0], expected[0])

    def test_with_url(self):
        t1 = self.t1.copy()
        t1['content']['itemContent']['tweet']['legacy']['full_text'] = "my really big tweet with my_url"
        test_json_text = json.dumps(embed_tweets([t1]))
        expected = [{"screen_name": "my_name", "rest_id": 1,
                     "full_text": "my really big tweet with my_expanded_url", "expanded_url": "my_expanded_url",
                     "tweet_url": "https://twitter.com/my_name/status/1",
                     "tags": ['devops', 'cicd']}]

        twitter = Twitter()
        result = twitter.parse_json(test_json_text)
        self.assertDictEqual(result[0], expected[0])

    def test_with_multiple_urls(self):
        t1 = self.t1.copy()
        t1['content']['itemContent']['tweet']['legacy']['full_text'] = "my really big tweet with my_url and another_url"
        t1['content']['itemContent']['tweet']['legacy']['entities']['urls'] = [{'expanded_url': "my_expanded_url",
                                                                                'url': "my_url"},
                                                                               {'expanded_url': "another_expanded_url",
                                                                                'url': "another_url"}]
        test_json_text = json.dumps(embed_tweets([t1]))
        expected = [{"screen_name": "my_name", "rest_id": 1,
                     "full_text": "my really big tweet with my_expanded_url and another_expanded_url",
                     "expanded_url": "my_expanded_url",
                     "tweet_url": "https://twitter.com/my_name/status/1",
                     "tags": ['devops', 'cicd']}]

        twitter = Twitter()
        result = twitter.parse_json(test_json_text)
        self.assertDictEqual(result[0], expected[0])
