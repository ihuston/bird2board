import json
import logging


class Twitter:

    def parse_json(self, text):
        json_dict = json.loads(text)
        tweets = json_dict['data']['bookmark_timeline']['timeline']['instructions'][0]['entries']
        extracted_data = []

        for t in tweets:
            if t['content']['entryType'] == "TimelineTimelineCursor":  # end marker
                logging.debug("Skipping end marker.")
                continue
            tweet_data = t['content']['itemContent']['tweet']
            if 'core' not in tweet_data:
                logging.debug(f"Skipping empty tweet: {tweet_data}")
                continue
            try:
                screen_name = tweet_data['core']['user']['legacy']['screen_name']
            except KeyError:
                logging.error(f"expected structure not found in tweet_data: {tweet_data.keys()}")
                logging.debug(tweet_data)
                raise
            rest_id = tweet_data['rest_id']
            parsed_tweet = {"screen_name": screen_name,
                            "full_text": tweet_data['legacy']['full_text'],
                            "rest_id": rest_id,
                            "tweet_url": self.tweet_url(screen_name, rest_id),
                            "tags": self.extract_tags(tweet_data)}

            if len(tweet_data['legacy']['entities']['urls']) > 0:
                parsed_tweet["expanded_url"] = tweet_data['legacy']['entities']['urls'][0]['expanded_url']
            extracted_data.append(parsed_tweet)

        return extracted_data

    def tweet_url(self, screen_name, rest_id):
        return f"https://twitter.com/{screen_name}/status/{rest_id}"

    def extract_tags(self, tweet_data):
        return [h['text'] for h in tweet_data['legacy']['entities']['hashtags']]
