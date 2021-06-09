import logging
import pathlib

from bird2board import Pinboard, Twitter


class Bird2Board:

    def __init__(self, pinboard_token, replace=False, shared=False, toread=False):
        self.pinboard = Pinboard(auth_token=pinboard_token, replace=replace, shared=shared, toread=toread)
        self.twitter = Twitter()

    def convert_single_file(self, file_path: pathlib.Path):
        try:
            json_text = file_path.read_text()
        except IOError:
            logging.error(f"Error reading file {file_path}")
            raise
        else:
            logging.info(f"Loaded JSON from file {file_path}.")

        try:
            tweets = self.twitter.parse_json(json_text)
        except Exception:
            logging.error("Error parsing bookmark data from file.")
            raise
        else:
            logging.info(f"Parsed {len(tweets)} tweets from file.")

        for tweet in tweets:
            bookmark = self.pinboard.tweet_to_bookmark(tweet)
            try:
                self.pinboard.add_bookmark(bookmark)
            except Exception:
                logging.error(f"Error saving bookmark to Pinboard {bookmark['url']}")
                raise
            else:
                logging.info(f"Saved bookmark to Pinboard: {bookmark['url']}")
        return

    def convert_directory(self, tweet_directory: pathlib.Path):
        if tweet_directory.is_file():
            self.convert_single_file(tweet_directory)
        else:
            for p in tweet_directory.iterdir():
                if p.suffix == ".json":
                    self.convert_single_file(p)
