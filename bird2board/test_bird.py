import json
from unittest import TestCase

from . import Twitter


def embed_tweets(tweets, users):
    return {'globalObjects': {'tweets': tweets, 'users': users}}


class TestBird(TestCase):

    def setUp(self) -> None:
        self.tweets = {'1': {'id_str': "1", 'full_text': "my tweet", 'user_id_str': "101",
                             'entities': {'urls': [{'expanded_url': "my_expanded_url",
                                                    'url': "my_url"}],
                                          'hashtags': [{'indices': [224, 231], 'text': 'devops'},
                                                       {'indices': [200, 204], 'text': 'cicd'}]}
                             },

                       '2': {'id_str': "2", 'full_text': "my other tweet", 'user_id_str': "102",
                             'entities': {'urls': [{'expanded_url': "my_other_expanded_url",
                                                    'url': "my_other_url"}],
                                          }
                             }}

        self.users = {'101': {'id_str': "101", 'screen_name': "my_name"},
                      '102': {'id_str': "102", 'screen_name': "my_other_name"}}

    def test_parse_json(self):
        test_json_text = json.dumps(embed_tweets(self.tweets, self.users))

        expected = [{"screen_name": "my_name", "rest_id": "1",
                     "full_text": "my tweet", "expanded_url": "my_expanded_url",
                     "tweet_url": "https://twitter.com/my_name/status/1",
                     "tags": ['devops', 'cicd']},
                    {"screen_name": "my_other_name", "rest_id": "2",
                     "full_text": "my other tweet", "expanded_url": "my_other_expanded_url",
                     "tweet_url": "https://twitter.com/my_other_name/status/2",
                     "tags": []}]

        twitter = Twitter()
        result = twitter.parse_json(test_json_text)
        self.assertDictEqual(result[0], expected[0])
        self.assertDictEqual(result[1], expected[1])

    def test_no_urls(self):
        tweets = self.tweets.copy()
        del tweets['1']['entities']['urls']
        test_json_text = json.dumps(embed_tweets(tweets, self.users))

        expected = [{"screen_name": "my_name", "rest_id": "1",
                     "full_text": "my tweet",
                     "tweet_url": "https://twitter.com/my_name/status/1",
                     "tags": ['devops', 'cicd']}]

        twitter = Twitter()
        result = twitter.parse_json(test_json_text)
        self.assertDictEqual(result[0], expected[0])

    def test_with_url(self):
        tweets = self.tweets.copy()
        tweets['1']['full_text'] = "my really big tweet with my_url"
        test_json_text = json.dumps(embed_tweets(tweets, self.users))
        expected = [{"screen_name": "my_name", "rest_id": "1",
                     "full_text": "my really big tweet with my_expanded_url", "expanded_url": "my_expanded_url",
                     "tweet_url": "https://twitter.com/my_name/status/1",
                     "tags": ['devops', 'cicd']}]

        twitter = Twitter()
        result = twitter.parse_json(test_json_text)
        self.assertDictEqual(result[0], expected[0])

    def test_with_multiple_urls(self):
        tweets = self.tweets.copy()
        tweets['1']['full_text'] = "my really big tweet with my_url and another_url"
        tweets['1']['entities']['urls'] = [{'expanded_url': "my_expanded_url",
                                            'url': "my_url"},
                                           {'expanded_url': "another_expanded_url",
                                            'url': "another_url"}]
        test_json_text = json.dumps(embed_tweets(tweets, self.users))
        expected = [{"screen_name": "my_name", "rest_id": "1",
                     "full_text": "my really big tweet with my_expanded_url and another_expanded_url",
                     "expanded_url": "my_expanded_url",
                     "tweet_url": "https://twitter.com/my_name/status/1",
                     "tags": ['devops', 'cicd']}]

        twitter = Twitter()
        result = twitter.parse_json(test_json_text)
        self.assertDictEqual(result[0], expected[0])
