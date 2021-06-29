import json
import logging


def replace_urls(text, urls):
    result = text
    for url in urls:
        result = result.replace(url['url'], url['expanded_url'])
    return result


def tweet_url(screen_name, rest_id):
    return f"https://twitter.com/{screen_name}/status/{rest_id}"


def extract_tags(tweet_data):
    if "hashtags" in tweet_data['entities']:
        return [h['text'] for h in tweet_data['entities']['hashtags']]
    else:
        return []


class Twitter:

    def parse_json(self, text):
        json_dict = json.loads(text)
        tweets = json_dict['globalObjects']['tweets']
        users = json_dict['globalObjects']['users']
        extracted_data = []

        for t in tweets.values():
            parsed_tweet = self.parse_single_tweet(t, users)
            extracted_data.append(parsed_tweet)
        return extracted_data

    def parse_single_tweet(self, tweet_data, users):
        try:
            screen_name = users[tweet_data['user_id_str']]['screen_name']
        except KeyError:
            logging.error(f"expected structure not found in users: {users.keys()}")
            logging.debug(users)
            raise
        id_str = tweet_data['id_str']
        parsed_tweet = {"screen_name": screen_name,
                        "full_text": tweet_data['full_text'],
                        "rest_id": id_str,
                        "tweet_url": tweet_url(screen_name, id_str),
                        "tags": extract_tags(tweet_data)}

        if 'urls' in tweet_data['entities']:
            parsed_tweet["expanded_url"] = tweet_data['entities']['urls'][0]['expanded_url']
            parsed_tweet["full_text"] = replace_urls(parsed_tweet["full_text"],
                                                     tweet_data['entities']['urls'])
        return parsed_tweet
