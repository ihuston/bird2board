import logging
import os
from datetime import timedelta, datetime
from time import sleep

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class Pinboard:
    format = "json"
    api_url = "https://api.pinboard.in/v1/posts/"
    default_tags = ["bird2board", "from:twitter_bookmarks"]
    last_call = None
    api_wait = timedelta(seconds=3)
    retry_strategy = Retry(total=3, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry_strategy)

    def __init__(self, auth_token=None, replace=False, shared=False, toread=False):
        if auth_token is None:
            self.auth_token = os.getenv("PINBOARD_TOKEN")
        else:
            self.auth_token = auth_token
        self.replace = replace
        self.shared = shared
        self.toread = toread
        self.http = requests.Session()
        current_user_agent = self.http.headers['User-Agent']
        self.http.headers.update({'User-Agent': current_user_agent + " bird2board"})
        self.http.mount("http://", self.adapter)
        self.http.mount("https://", self.adapter)

    def check_connection(self):
        return self.take_action("update", {}).ok

    def tweet_to_bookmark(self, tweet, default_tags=None):
        if default_tags is None:
            default_tags = self.default_tags
        tags = []
        tags.extend(default_tags)
        if "tags" in tweet:
            tags.extend(tweet["tags"])
        bookmark = dict(url=tweet["tweet_url"],
                        description=self.shorten_for_title(tweet["full_text"]),
                        extended=tweet["full_text"],
                        tags=self.tag_string(tags),
                        replace="yes" if self.replace else "no",
                        shared="yes" if self.shared else "no",
                        toread="yes" if self.toread else "no")
        return bookmark

    def shorten_for_title(self, text):
        result = text[:50]
        if len(text) > 50:
            split = result.split(" ")
            result = " ".join(split[:1] + split[1:-1])
            result = result + "..."
        return result

    def add_bookmark(self, bookmark):
        return self.take_action("add", bookmark)

    def tag_string(self, tags):
        return " ".join(tags)

    def take_action(self, action, action_params):
        self.sleep_if_needed(self.last_call)

        params = action_params.copy()
        params["auth_token"] = self.auth_token
        params["format"] = self.format
        response = self.call_api(action, params)
        response.raise_for_status()
        self.last_call = datetime.now()
        return response

    def call_api(self, action, params, timeout=3, call_count=0):
        try:
            resp = self.http.get(self.api_url + action, params=params, timeout=timeout)
        except requests.exceptions.ConnectTimeout:
            if call_count <= 1:  # tries 3 times in total
                resp = self.call_api(action, params, timeout=timeout, call_count=call_count+1)
            else:
                raise
        return resp

    def sleep_if_needed(self, last_call: datetime = None, wait=None):
        if wait is None:
            wait = self.api_wait
        if last_call is not None:
            end_of_wait = last_call + wait
            seconds_left = (end_of_wait - datetime.now()).total_seconds()
            logging.debug(f"Sleeping for {seconds_left} seconds...")
            sleep(seconds_left)
            logging.debug(f"Sleep over.")
        return
