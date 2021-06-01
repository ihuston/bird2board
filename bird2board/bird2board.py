#!/usr/bin/env python
import json
import os

import requests


class Pinboard:
    format = "json"
    api_url = "https://api.pinboard.in/v1/posts/"

    def __init__(self, auth_token=None):
        if auth_token is None:
            self.auth_token = os.getenv("PINBOARD_TOKEN")
        else:
            self.auth_token = auth_token

    def check_connection(self):
        req = requests.request("GET", self.prepare_url("update"))
        return req.ok

    def prepare_url(self, action):
        return f"{self.api_url}{action}?auth_token={self.auth_token}&format={self.format}"


class Twitter:

    def parse_json(self, text):
        json_dict = json.loads(text)
        tweets = json_dict['data']['bookmark_timeline']['timeline']['instructions'][0]['entries']
        extracted_data = []

        for t in tweets:
            tweet_data = t['content']['itemContent']['tweet']
            parsed_tweet = {"screen_name": tweet_data['core']['user']['legacy']['screen_name'],
                            "full_text": tweet_data['legacy']['full_text'],
                            "rest_id": tweet_data['rest_id']}
            if len(tweet_data['legacy']['entities']['urls']) > 0:
                parsed_tweet["expanded_url"] = tweet_data['legacy']['entities']['urls'][0]['expanded_url']
            extracted_data.append(parsed_tweet)

        return extracted_data


def main():
    pass


if __name__ == "__main__":
    main()
