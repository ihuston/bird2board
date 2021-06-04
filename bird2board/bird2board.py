#!/usr/bin/env python
import json
import os
from datetime import datetime, timedelta
from time import sleep

import requests


class Pinboard:
    format = "json"
    api_url = "https://api.pinboard.in/v1/posts/"
    default_tags = ["bird2board", "from:twitter_bookmarks"]
    last_call = None
    api_wait = timedelta(seconds=3)

    def __init__(self, auth_token=None):
        if auth_token is None:
            self.auth_token = os.getenv("PINBOARD_TOKEN")
        else:
            self.auth_token = auth_token

    def check_connection(self):
        return self.take_action("update", {}).ok

    def tweet_to_bookmark(self, tweet, default_tags=None):
        if default_tags is None:
            default_tags = self.default_tags

        bookmark = dict(url=tweet["tweet_url"],
                        description=tweet["full_text"][:30],
                        extended=tweet["full_text"],
                        tags=self.tag_string(default_tags),
                        replace="no",
                        shared="no",
                        toread="yes")
        return bookmark

    def add_bookmark(self, bookmark):
        return self.take_action("add", bookmark)

    def tag_string(self, tags):
        return " ".join(tags)

    def take_action(self, action, action_params):
        self.sleep_if_needed(self.last_call)

        params = action_params.copy()
        params["auth_token"] = self.auth_token
        params["format"] = self.format
        response = requests.get(self.api_url + action, params, timeout=3)
        return response

    def sleep_if_needed(self, last_call: datetime = None, wait=None):
        if wait is None:
            wait = self.api_wait
        if last_call is not None:
            end_of_wait = last_call + wait
            seconds_left = (end_of_wait - datetime.now()).total_seconds()
            sleep(seconds_left)
        return


class Twitter:

    def parse_json(self, text):
        json_dict = json.loads(text)
        tweets = json_dict['data']['bookmark_timeline']['timeline']['instructions'][0]['entries']
        extracted_data = []

        for t in tweets:
            tweet_data = t['content']['itemContent']['tweet']
            screen_name = tweet_data['core']['user']['legacy']['screen_name']
            rest_id = tweet_data['rest_id']
            parsed_tweet = {"screen_name": screen_name,
                            "full_text": tweet_data['legacy']['full_text'],
                            "rest_id": rest_id,
                            "tweet_url": self.tweet_url(screen_name, rest_id)}
            if len(tweet_data['legacy']['entities']['urls']) > 0:
                parsed_tweet["expanded_url"] = tweet_data['legacy']['entities']['urls'][0]['expanded_url']
            extracted_data.append(parsed_tweet)

        return extracted_data

    def tweet_url(self, screen_name, rest_id):
        return f"https://twitter.com/{screen_name}/status/{rest_id}"


def main():
    pass


if __name__ == "__main__":
    main()
