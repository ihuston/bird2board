#!/usr/bin/env python

from bird2board import Twitter
from bird2board import Pinboard

import pathlib
import logging


logging.basicConfig(level=logging.DEBUG)


def convert_single_file(file_path: pathlib.Path, pinboard_token):
    try:
        json_text = file_path.read_text()
    except IOError:
        logging.error(f"Error reading file {file_path}")
        raise

    logging.debug("Loaded JSON from file.")

    tw = Twitter()
    tweets = tw.parse_json(json_text)
    logging.debug(f"Parsed {len(tweets)} tweets from file.")

    pb = Pinboard(auth_token=pinboard_token)
    for tweet in tweets:
        bookmark = pb.tweet_to_bookmark(tweet)
        try:
            pb.add_bookmark(bookmark)
        except Exception:
            logging.error(f"Error saving bookmark to Pinboard {bookmark['url']}")
            raise
        else:
            logging.debug(f"Saved bookmark to Pinboard: {bookmark['url']}")


def main():
    pass


if __name__ == "__main__":
    main()
