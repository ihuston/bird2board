#!/usr/bin/env python

from bird2board import Twitter
from bird2board import Pinboard

import pathlib
import logging


logging.basicConfig(level=logging.DEBUG)


class Bird2Board:

    def __init__(self, pinboard_token):
        self.pinboard = Pinboard(auth_token=pinboard_token)
        self.twitter = Twitter()

    def convert_single_file(self, file_path: pathlib.Path):
        try:
            json_text = file_path.read_text()
        except IOError:
            logging.error(f"Error reading file {file_path}")
            raise

        logging.debug("Loaded JSON from file.")

        tweets = self.twitter.parse_json(json_text)
        logging.debug(f"Parsed {len(tweets)} tweets from file.")

        for tweet in tweets:
            bookmark = self.pinboard.tweet_to_bookmark(tweet)
            try:
                self.pinboard.add_bookmark(bookmark)
            except Exception:
                logging.error(f"Error saving bookmark to Pinboard {bookmark['url']}")
                raise
            else:
                logging.debug(f"Saved bookmark to Pinboard: {bookmark['url']}")
        return

    def convert_directory(self, tweet_directory: pathlib.Path):
        for p in tweet_directory.iterdir():
            print(p.suffix)
            if p.suffix == ".json":
                self.convert_single_file(p)


def convert():
    pass


if __name__ == "__main__":
    convert()
